#!/usr/bin/env python3
"""Trust-aware deterministic router for ZIP-your-Research.

Usage:
  python router/route_v1_7.py "不要画图，只检查论文逻辑"
  python router/route_v1_7.py "核查引用" --untrusted-text-file paper.txt --json
  python router/route_v1_7.py "润色摘要" --topk 5

The positional query is the trusted routing instruction. Paper text, abstracts,
web pages, and other quoted material belong in ``--untrusted-text`` or
``--untrusted-text-file``. Embedded payload markers are also split from the
trusted query before intent detection. Untrusted content is never used to pick
a route.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

try:
    import yaml
except Exception as exc:  # pragma: no cover - exercised by the CLI environment
    raise SystemExit("PyYAML required. Install with: pip install pyyaml") from exc


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "skills_manifest.yaml"
CAPABILITIES_MANIFEST_PATH = ROOT / "manifests" / "RELEASE_CAPABILITIES.yaml"
ROUTER_VERSION = "1.7.0"
FIGURE_CAPABILITY_ID = "figures4papers_source"

PAYLOAD_MARKER_RE = re.compile(
    r"(?im)^[ \t]*(?:"
    r"摘要内容|论文内容|文档内容|网页内容|引用材料|待分析文本|以下(?:是|为).{0,12}(?:内容|文本|摘要)"
    r"|abstract\s+content|paper\s+content|document\s+content|quoted\s+content"
    r")[ \t]*[:：][ \t]*"
)

SUSPICIOUS_PAYLOAD_RULES: Sequence[Tuple[str, re.Pattern[str]]] = (
    (
        "instruction_override",
        re.compile(
            r"(?i)(?:ignore|disregard|override).{0,40}(?:instruction|prompt|rule)"
            r"|(?:忽略|覆盖|绕过).{0,30}(?:指令|提示|规则)"
        ),
    ),
    (
        "route_override",
        re.compile(
            r"(?i)(?:route|primary|select|call|use).{0,30}(?:skill|engine|S\d{3})"
            r"|(?:路由|选择|调用|使用).{0,30}(?:技能|引擎|S\d{3}|[A-Za-z0-9_]+_engine)"
        ),
    ),
    (
        "role_or_secret_request",
        re.compile(
            r"(?i)(?:system\s+prompt|developer\s+message|reveal.{0,20}secret)"
            r"|(?:系统提示|开发者消息|泄露.{0,20}(?:密钥|秘密))"
        ),
    ),
)

# A trigger containing ASCII letters/digits is matched at ASCII word
# boundaries. This deliberately prevents "graph" from matching "paragraph".
FAMILY_HINTS: Mapping[str, Sequence[str]] = {
    "skill_memory": (
        "automatic skill generation",
        "auto-generate skill",
        "generated skill",
        "skill as memory",
        "procedural memory",
        "dynamic skill management",
        "update generated skill",
        "delete generated skill",
        "skill memory",
        "自动生成 skill",
        "skill 记忆",
        "程序性记忆",
        "动态技能管理",
        "更新技能",
        "删除技能",
    ),
    "evolution": (
        "self evolution",
        "self-evolution",
        "recursive improvement",
        "multi-agent",
        "multi agent",
        "authoritative search",
        "cross-refutation",
        "agentic evolution",
        "自进化",
        "自我进化",
        "多智能体",
        "多代理",
        "权威检索",
        "交叉反驳",
        "广泛搜索",
    ),
    "memory": (
        "visible memory",
        "explicit memory",
        "short-term memory",
        "long-term memory",
        "memory retrieval",
        "记忆存储",
        "显式记忆",
        "短期记忆",
        "长期记忆",
        "记忆检索",
        "记忆文档",
    ),
    "release": (
        "release audit",
        "release package",
        "package integrity",
        "secret scan",
        "license audit",
        "发布审计",
        "发布包",
        "打包完整性",
        "密钥扫描",
        "许可证审计",
        "完整性验证",
        "禁止遗漏",
    ),
    "coding": (
        "code review",
        "code audit",
        "debug",
        "traceback",
        "exception",
        "bug",
        "regression",
        "refactor",
        "unit test",
        "pytest",
        "lint",
        "代码审计",
        "代码评审",
        "代码检查",
        "修复代码",
        "调试",
        "报错",
        "回归测试",
        "重构",
        "单元测试",
    ),
    "figure": (
        "figure",
        "figures",
        "plot",
        "plots",
        "diagram",
        "diagrams",
        "visualization",
        "draw.io",
        "drawio",
        "matplotlib",
        "scientific figure",
        "architecture diagram",
        "workflow diagram",
        "科研绘图",
        "论文图",
        "图表设计",
        "图形摘要",
        "流程图",
        "架构图",
        "绘图脚本",
        "画图",
        "绘图",
        "可视化",
    ),
    "proof": (
        "proof",
        "theorem",
        "lemma",
        "corollary",
        "derivation",
        "formal proof",
        "proof audit",
        "证明",
        "定理",
        "引理",
        "推导",
        "数学证明",
        "形式化证明",
        "理论推导",
    ),
    "logic": (
        "research logic",
        "paper logic",
        "logic audit",
        "logical consistency",
        "storyline",
        "claim evidence",
        "claim-evidence",
        "论文逻辑",
        "科研逻辑",
        "逻辑核查",
        "逻辑审查",
        "逻辑一致性",
        "论文主线",
        "研究主线",
        "证据链",
    ),
    "method": (
        "method correctness",
        "method audit",
        "method design",
        "problem formulation",
        "assumption audit",
        "方法正确性",
        "方法审计",
        "方法设计",
        "问题定义",
        "问题设定",
        "假设审计",
        "贡献定义",
    ),
    "writing": (
        "rewrite",
        "revise",
        "polish",
        "copyedit",
        "writing",
        "write",
        "manuscript",
        "paper section",
        "abstract",
        "introduction",
        "related work",
        "caption",
        "paragraph",
        "润色",
        "改写",
        "重写",
        "写作",
        "措辞",
        "表达优化",
        "摘要",
        "引言",
        "相关工作",
        "图注",
        "段落",
    ),
    "citation": (
        "citation audit",
        "citation check",
        "reference audit",
        "bibliography",
        "source verification",
        "verify citations",
        "引用核查",
        "引文核查",
        "参考文献",
        "来源验证",
        "核查引用",
    ),
    "experiment": (
        "evaluation protocol",
        "experiment design",
        "experiment completeness",
        "ablation",
        "baseline",
        "benchmark",
        "statistical significance",
        "实验设计",
        "实验完整性",
        "消融",
        "基线",
        "评测协议",
        "统计显著性",
    ),
    "novelty": (
        "novelty search",
        "novelty audit",
        "prior art",
        "research gap",
        "innovation point",
        "创新性",
        "创新点",
        "新颖性",
        "研究空白",
        "现有工作检索",
    ),
    "route": (
        "route",
        "router",
        "skill selection",
        "routing policy",
        "路由",
        "技能选择",
        "选哪个技能",
    ),
}

NEGATION_PATTERNS: Mapping[str, Sequence[re.Pattern[str]]] = {
    "skill_memory": (
        re.compile(
            r"(?i)(?:不要|不用|不需要|无需|无须|别|禁止|不想|不打算|排除|避免)"
            r"(?:再|去|使用|调用|保存|生成|更新|删除|管理)?"
            r"(?:自动生成\s*skill|skill\s*记忆|程序性记忆|动态技能|生成技能)"
        ),
        re.compile(
            r"(?i)\b(?:do\s+not|don't|does\s+not|doesn't|no|not|never|without|"
            r"avoid|exclude|skip)\s+"
            r"(?:(?:want|plan|intend|need)\s+(?:to\s+)?)?"
            r"(?:use|save|store|write|create|generate|update|delete|manage)?\s*"
            r"(?:a\s+|an\s+|any\s+|the\s+)?"
            r"(?:generated\s+skill|skill\s+(?:memory|generation)|procedural\s+memory|"
            r"dynamic\s+skill)\b"
        ),
    ),
    "evolution": (
        re.compile(
            r"(?:不要|不用|不需要|无需|无须|别|禁止|不想|不打算|排除|避免)"
            r"(?:再|去|使用|调用|运行|做|开展|执行|采用)?"
            r"(?:多智能体|多代理|自进化|自我进化|权威检索|交叉反驳|广泛搜索)"
        ),
        re.compile(
            r"(?i)\b(?:do\s+not|don't|does\s+not|doesn't|no|not|never|without|"
            r"avoid|exclude|skip)\s+"
            r"(?:(?:want|plan|intend|need)\s+(?:to\s+)?)?"
            r"(?:use|run|perform|do|invoke|apply|enable)?\s*"
            r"(?:a\s+|an\s+|any\s+|the\s+)?"
            r"(?:multi-agent|multi\s+agent|self-evolution|self\s+evolution|"
            r"recursive\s+improvement|agentic\s+evolution|authoritative\s+search|"
            r"cross-refutation)\b"
        ),
    ),
    "memory": (
        re.compile(
            r"(?:不要|不用|不需要|无需|无须|别|禁止|不想|不打算|排除|避免)"
            r"(?:再|去|使用|调用|保存|存储|写入|创建|持久化|检索)?"
            r"(?:显式记忆|短期记忆|长期记忆|持久记忆|记忆存储|记忆检索|记忆文档|记忆)"
        ),
        re.compile(
            r"(?i)\b(?:do\s+not|don't|does\s+not|doesn't|no|not|never|without|"
            r"avoid|exclude|skip)\s+"
            r"(?:(?:want|plan|intend|need)\s+(?:to\s+)?)?"
            r"(?:use|save|store|write|create|persist|enable|retrieve)?\s*"
            r"(?:a\s+|an\s+|any\s+|the\s+)?"
            r"(?:(?:visible|explicit|short-term|long-term|persistent)\s+memory|"
            r"memory\s+(?:storage|retrieval)|memory)\b"
        ),
    ),
    "release": (
        re.compile(
            r"(?:不要|不用|不需要|无需|无须|别|禁止|不想|不打算|不做|不进行|排除|避免)"
            r"(?:再|去|做|运行|执行|创建|生成|进行)?"
            r"(?:发布审计|发布包|打包|完整性验证|密钥扫描|许可证审计)"
        ),
        re.compile(
            r"(?i)\b(?:do\s+not|don't|does\s+not|doesn't|no|not|never|without|"
            r"avoid|exclude|skip)\s+"
            r"(?:(?:want|plan|intend|need)\s+(?:to\s+)?)?"
            r"(?:run|perform|do|create|build|make)?\s*"
            r"(?:a\s+|an\s+|any\s+|the\s+)?"
            r"(?:release\s+audit|release\s+package|package\s+integrity|secret\s+scan|"
            r"license\s+audit|release|packaging)\b"
        ),
    ),
    "figure": (
        re.compile(
            r"(?:不要|不用|不需要|无需|无须|别|禁止|不想|不打算|不考虑|排除|省略|跳过)"
            r"(?:再|要|去|使用|调用|生成|制作|绘制|画|做|输出|包含|加入)?"
            r"(?:任何|一个|一张|这些)?(?:图|图表|图像|绘图|可视化|流程图|架构图)"
        ),
        re.compile(
            r"(?i)\b(?:do\s+not|don't|does\s+not|doesn't|no|not|never|without)\s+"
            r"(?:(?:want|plan|intend|need|expect)\s+(?:to\s+)?)?"
            r"(?:use|call|generate|create|draw|make|produce|include|show)?\s*"
            r"(?:a\s+|an\s+|any\s+|the\s+)?(?:figure|plot|diagram|visualization)s?\b"
        ),
        re.compile(
            r"(?i)\b(?:avoid|exclude|omit|skip)\s+"
            r"(?:a\s+|an\s+|any\s+|the\s+)?(?:figure|plot|diagram|visualization)s?\b"
        ),
        re.compile(r"(?i)\bfigure_engine\s+(?:is\s+)?not\s+applicable\b"),
    ),
    "proof": (
        re.compile(r"(?:不要|不用|不需要|无需|无须|别|禁止)(?:做|写|生成|检查|验证)?(?:证明|推导|定理证明)"),
        re.compile(
            r"(?i)\b(?:do\s+not|don't|no|not|without)\s+"
            r"(?:need(?:ed)?\s+to\s+)?(?:write|generate|check|verify)?\s*"
            r"(?:a\s+|any\s+)?(?:proof|derivation|theorem)s?\b"
        ),
        re.compile(r"(?i)\bnot\s+a\s+(?:proof|derivation)\s+task\b"),
    ),
    "writing": (
        re.compile(r"(?:不要|不用|不需要|无需|无须|别|禁止)(?:做|写|进行)?(?:润色|改写|重写|写作)"),
        re.compile(
            r"(?i)\b(?:do\s+not|don't|no|not|without)\s+"
            r"(?:need(?:ed)?\s+to\s+)?(?:rewrite|revise|polish|write|edit)\b"
        ),
    ),
    "coding": (
        re.compile(r"(?:不要|不用|不需要|无需|无须|别|禁止)(?:写|改|生成|检查)?(?:代码|编程|调试)"),
        re.compile(
            r"(?i)\b(?:do\s+not|don't|no|not|without)\s+"
            r"(?:need(?:ed)?\s+to\s+)?(?:write|change|generate|debug)?\s*(?:code|programming)\b"
        ),
    ),
    "citation": (
        re.compile(r"(?:不要|不用|不需要|无需|无须|别|禁止)(?:检查|核查|验证)?(?:引用|参考文献|来源)"),
        re.compile(
            r"(?i)\b(?:do\s+not|don't|no|not|without)\s+"
            r"(?:need(?:ed)?\s+to\s+)?(?:check|audit|verify)?\s*(?:citation|reference|source)s?\b"
        ),
    ),
}

FAMILY_PRIMARY: Mapping[str, str] = {
    "skill_memory": "S661",
    "evolution": "S660",
    "memory": "S660",
    "release": "S650",
    "coding": "coding_engine",
    "figure": "figure_engine",
    "proof": "proof_engine",
    "logic": "proof_engine",
    "method": "proof_engine",
    "writing": "writing_engine",
    "citation": "S424",
    "experiment": "S303",
    "novelty": "S234",
    "route": "S432",
}

PRIMARY_PRIORITY: Sequence[str] = (
    "skill_memory",
    "evolution",
    "memory",
    "release",
    "coding",
    "figure",
    "proof",
    "logic",
    "method",
    "writing",
    "citation",
    "experiment",
    "novelty",
    "route",
)

BASE_COMPANIONS: Mapping[str, Sequence[str]] = {
    "S661": ("S660", "S303", "S414", "S423", "S431"),
    "S660": ("S203", "S224", "S226", "S303", "S414", "S424", "S431"),
    "S650": ("S423", "S431"),
    "coding_engine": ("S430", "S431"),
    "figure_engine": ("S621", "S623"),
    "proof_engine": ("S203", "S226", "S227", "S230"),
    "writing_engine": ("S640",),
    "S424": ("S203",),
    "S303": ("S327",),
    "S234": ("S224",),
    "S432": (),
}

NEGATED_ROUTE_IDS: Mapping[str, Sequence[str]] = {
    "skill_memory": ("S661",),
    "evolution": ("S660",),
    "memory": ("S660",),
    "release": ("S650",),
    "figure": ("figure_engine", "S621", "S622", "S623"),
    "proof": ("proof_engine", "S230", "S235", "S237", "S240", "S241", "S433"),
    "writing": ("writing_engine", "S601", "S602", "S603", "S604", "S640"),
    "coding": ("coding_engine", "S402", "S408", "S430", "S431"),
    "citation": ("S424",),
}


def _ascii_bounded_pattern(hint: str) -> re.Pattern[str]:
    escaped = re.escape(hint)
    left = r"(?<![A-Za-z0-9_])" if hint[:1].isascii() and hint[:1].isalnum() else ""
    right = r"(?![A-Za-z0-9_])" if hint[-1:].isascii() and hint[-1:].isalnum() else ""
    return re.compile(left + escaped + right, re.IGNORECASE)


def _contains_hint(text: str, hint: str) -> bool:
    normalized = hint.strip()
    if not normalized:
        return False
    if not any(ch.isascii() and ch.isalnum() for ch in normalized):
        # One-character CJK triggers are too ambiguous for routing.
        return len(normalized) >= 2 and normalized in text
    return bool(_ascii_bounded_pattern(normalized).search(text))


def _dedupe(values: Iterable[str]) -> List[str]:
    seen = set()
    out: List[str] = []
    for value in values:
        if value and value not in seen:
            seen.add(value)
            out.append(value)
    return out


def split_trusted_and_payload(query: str, extra_payload: str = "") -> Tuple[str, str]:
    """Split explicit or embedded untrusted content from the routing request."""

    match = PAYLOAD_MARKER_RE.search(query)
    if match:
        trusted = query[: match.start()].strip()
        embedded = query[match.end() :].strip()
    else:
        trusted = query.strip()
        embedded = ""
    payload = "\n".join(part for part in (embedded, extra_payload.strip()) if part)
    return trusted, payload


@lru_cache(maxsize=8)
def _load_active_manifest_cached(
    path_text: str, modified_ns: int, size_bytes: int
) -> Dict[str, Dict[str, Any]]:
    """Load routable entries from the authoritative manifest.

    A manifest entry is active only when it has an id, a repository-relative
    path, and that path exists. Physical-tree aliases not present here are never
    considered.
    """

    # modified_ns and size_bytes intentionally participate in the cache key.
    del modified_ns, size_bytes
    path = Path(path_text)
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    raw_skills = data.get("skills", [])
    if not isinstance(raw_skills, list):
        raise ValueError("skills_manifest.yaml: 'skills' must be a list")

    active: Dict[str, Dict[str, Any]] = {}
    seen_paths: Dict[str, str] = {}
    errors: List[str] = []
    for index, raw in enumerate(raw_skills):
        if not isinstance(raw, dict):
            errors.append(f"manifest entry {index} is not a mapping")
            continue
        skill_id = str(raw.get("id", "")).strip()
        rel_path = str(raw.get("path", "")).strip()
        if not skill_id or not rel_path:
            errors.append(f"manifest entry {index} requires id and path")
            continue
        if skill_id in active:
            errors.append(f"duplicate active skill id: {skill_id}")
            continue
        if rel_path in seen_paths:
            errors.append(
                f"duplicate active skill path: {rel_path} ({seen_paths[rel_path]}, {skill_id})"
            )
            continue
        candidate = (ROOT / rel_path).resolve()
        try:
            candidate.relative_to(ROOT.resolve())
        except ValueError:
            errors.append(f"active skill path escapes repository: {rel_path}")
            continue
        if not candidate.is_file():
            errors.append(f"active skill path is missing: {rel_path}")
            continue
        entry = dict(raw)
        entry["id"] = skill_id
        entry["path"] = rel_path
        triggers = entry.get("triggers", [])
        if isinstance(triggers, str):
            triggers = [triggers]
        entry["triggers"] = [str(item).strip() for item in triggers if str(item).strip()]
        active[skill_id] = entry
        seen_paths[rel_path] = skill_id
    if errors:
        raise ValueError("invalid active manifest:\n- " + "\n- ".join(errors))
    return active


def load_active_manifest(path: Path = MANIFEST_PATH) -> Dict[str, Dict[str, Any]]:
    """Load the active manifest, invalidating the cache after file changes."""

    try:
        stat = path.stat()
    except OSError as exc:
        raise ValueError(f"manifest not found: {path}") from exc
    return _load_active_manifest_cached(str(path.resolve()), stat.st_mtime_ns, stat.st_size)


def _find_negations(trusted_query: str) -> Dict[str, List[Tuple[str, int, int]]]:
    found: Dict[str, List[Tuple[str, int, int]]] = {}
    for family, patterns in NEGATION_PATTERNS.items():
        matches: List[Tuple[str, int, int]] = []
        seen = set()
        for pattern in patterns:
            for match in pattern.finditer(trusted_query):
                record = (match.group(0).strip(), match.start(), match.end())
                if record not in seen:
                    seen.add(record)
                    matches.append(record)
        if matches:
            found[family] = matches
    return found


def detect_negations(trusted_query: str) -> Dict[str, List[str]]:
    return {
        family: _dedupe(match_text for match_text, _, _ in matches)
        for family, matches in _find_negations(trusted_query).items()
    }


def _mask_negated_spans(
    trusted_query: str, negation_matches: Mapping[str, Sequence[Tuple[str, int, int]]]
) -> str:
    """Mask only explicitly negated spans so separate positive requests survive."""

    masked = list(trusted_query)
    for matches in negation_matches.values():
        for _, start, end in matches:
            masked[start:end] = " " * (end - start)
    return "".join(masked)


def detect_intents(trusted_query: str, negated: Mapping[str, Sequence[str]]) -> Dict[str, List[str]]:
    intents: Dict[str, List[str]] = {}
    for family, hints in FAMILY_HINTS.items():
        if family in negated:
            continue
        matched = [hint for hint in hints if _contains_hint(trusted_query, hint)]
        if matched:
            intents[family] = matched
    if any(symbol in trusted_query for symbol in ("∀", "∃", "⇒", "⇔", "∵", "∴")) and "proof" not in negated:
        intents.setdefault("proof", []).append("mathematical_symbol")
    # Mentioning a denied engine is routing-policy discussion, not that engine's task.
    if not intents and re.search(r"(?i)\b(?:figure|proof|writing|coding)_engine\b", trusted_query):
        intents["route"] = ["engine_applicability"]
    return intents


def inspect_untrusted_payload(payload: str) -> List[str]:
    labels = [label for label, pattern in SUSPICIOUS_PAYLOAD_RULES if pattern.search(payload)]
    return labels


def _capability_relative_paths(raw: Mapping[str, Any]) -> List[Path]:
    values: List[str] = []
    bundled_path = raw.get("bundled_path")
    if bundled_path is not None:
        values.append(str(bundled_path).strip())
    prefixes = raw.get("allowed_missing_ref_prefixes", [])
    if not isinstance(prefixes, list):
        raise ValueError("allowed_missing_ref_prefixes must be a list")
    values.extend(str(item).strip().rstrip("/") for item in prefixes)

    relative_paths: List[Path] = []
    for value in _dedupe(values):
        if not value:
            continue
        relative_path = Path(value)
        if relative_path.is_absolute() or ".." in relative_path.parts:
            raise ValueError(f"capability path must be repository-relative: {value}")
        relative_paths.append(relative_path)
    return relative_paths


@lru_cache(maxsize=8)
def _load_capability_specs_cached(
    path_text: str, modified_ns: int, size_bytes: int
) -> Dict[str, Dict[str, Any]]:
    del modified_ns, size_bytes
    path = Path(path_text)
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError("capabilities manifest root must be a mapping")
    if str(data.get("policy", "")).strip() != "fail_closed":
        raise ValueError("capabilities manifest policy must be fail_closed")
    raw_capabilities = data.get("capabilities")
    if not isinstance(raw_capabilities, list):
        raise ValueError("capabilities manifest requires a capabilities list")

    specs: Dict[str, Dict[str, Any]] = {}
    for index, raw in enumerate(raw_capabilities):
        if not isinstance(raw, dict):
            raise ValueError(f"capability entry {index} must be a mapping")
        capability_id = str(raw.get("id", "")).strip()
        if not capability_id:
            raise ValueError(f"capability entry {index} requires id")
        if capability_id in specs:
            raise ValueError(f"duplicate capability id: {capability_id}")
        affected_skill_ids = raw.get("affected_skill_ids")
        if not isinstance(affected_skill_ids, list):
            raise ValueError(f"{capability_id}: affected_skill_ids must be a list")
        spec = dict(raw)
        spec["id"] = capability_id
        spec["affected_skill_ids"] = [
            str(item).strip() for item in affected_skill_ids if str(item).strip()
        ]
        spec["relative_paths"] = _capability_relative_paths(raw)
        specs[capability_id] = spec

    figure_spec = specs.get(FIGURE_CAPABILITY_ID)
    if figure_spec is None:
        raise ValueError(f"required capability missing from manifest: {FIGURE_CAPABILITY_ID}")
    required_affected_ids = {"figure_engine", "S621", "S622", "S623"}
    missing_affected_ids = sorted(
        required_affected_ids.difference(figure_spec["affected_skill_ids"])
    )
    if missing_affected_ids:
        raise ValueError(
            f"{FIGURE_CAPABILITY_ID}: affected_skill_ids missing {missing_affected_ids}"
        )
    if not figure_spec["relative_paths"]:
        raise ValueError(f"{FIGURE_CAPABILITY_ID}: no source path declared")
    if str(figure_spec.get("missing_behavior", "")).strip() != "SOURCE_UNAVAILABLE":
        raise ValueError(
            f"{FIGURE_CAPABILITY_ID}: missing_behavior must be SOURCE_UNAVAILABLE"
        )
    if not str(figure_spec.get("required_runtime_response", "")).strip():
        raise ValueError(f"{FIGURE_CAPABILITY_ID}: required_runtime_response is required")
    return specs


def _load_capability_specs(path: Path) -> Dict[str, Dict[str, Any]]:
    try:
        stat = path.stat()
    except OSError as exc:
        raise ValueError(f"capabilities manifest not found: {path}") from exc
    return _load_capability_specs_cached(
        str(path.resolve()),
        stat.st_mtime_ns,
        stat.st_size,
    )


def inspect_capabilities(
    capability_root: Path = ROOT,
    capabilities_manifest_path: Path = CAPABILITIES_MANIFEST_PATH,
) -> Dict[str, Dict[str, Any]]:
    """Inspect manifest-declared source capabilities relative to the runtime root."""

    root = Path(capability_root)
    try:
        specs = _load_capability_specs(capabilities_manifest_path)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        return {
            FIGURE_CAPABILITY_ID: {
                "available": False,
                "path": None,
                "manifest_valid": False,
                "manifest_error": str(exc),
            }
        }

    states: Dict[str, Dict[str, Any]] = {}
    for capability_id, spec in specs.items():
        relative_paths = spec["relative_paths"]
        selected_path = next(
            (relative_path for relative_path in relative_paths if (root / relative_path).exists()),
            None,
        )
        states[capability_id] = {
            "available": selected_path is not None,
            "path": (
                selected_path.as_posix()
                if selected_path is not None
                else (relative_paths[0].as_posix() if relative_paths else None)
            ),
            "manifest_valid": True,
            "declared_release_status": str(spec.get("status", "")).strip() or None,
            "affected_skill_ids": list(spec["affected_skill_ids"]),
            "required_runtime_response": str(
                spec.get("required_runtime_response", "")
            ).strip()
            or None,
        }
    return states


def _ordered_families(families: Iterable[str]) -> List[str]:
    family_set = set(families)
    ordered = [family for family in PRIMARY_PRIORITY if family in family_set]
    return ordered + sorted(family_set.difference(ordered))


def _select_primary(intents: Mapping[str, Sequence[str]], active: Mapping[str, Mapping[str, Any]]) -> str:
    for family in PRIMARY_PRIORITY:
        if family in intents:
            desired = FAMILY_PRIMARY[family]
            if desired in active:
                return desired
    if "S432" in active:
        return "S432"
    return sorted(active)[0] if active else ""


def _required_companions(
    primary: str,
    intents: Mapping[str, Sequence[str]],
    active: Mapping[str, Mapping[str, Any]],
    forbidden: Sequence[str],
) -> List[str]:
    requested: List[str] = list(BASE_COMPANIONS.get(primary, ()))
    if "citation" in intents:
        requested.append("S424")
    if "logic" in intents:
        requested.append("S226")
    if "method" in intents:
        requested.append("S227")
    if "proof" in intents:
        requested.append("S230")
    if "writing" in intents:
        requested.append("S640")
    if "figure" in intents:
        requested.append("S623")
        plotting_hints = ("plot", "plots", "matplotlib", "绘图脚本", "画图")
        if any(hint in intents["figure"] for hint in plotting_hints):
            requested.append("S622")
    if "experiment" in intents:
        requested.extend(("S303", "S327"))
    if "novelty" in intents:
        requested.append("S224")
    forbidden_set = set(forbidden)
    return [
        skill_id
        for skill_id in _dedupe(requested)
        if skill_id != primary and skill_id in active and skill_id not in forbidden_set
    ]


def _build_execution_plan(
    primary: str,
    intents: Mapping[str, Sequence[str]],
    active: Mapping[str, Mapping[str, Any]],
    missing_capabilities: Sequence[str],
) -> List[Dict[str, Any]]:
    if not primary:
        return []
    if primary != "S660":
        return [
            {
                "step": 1,
                "stage": "execute",
                "engine": primary,
                "status": "READY",
            }
        ]

    plan: List[Dict[str, Any]] = [
        {
            "step": 1,
            "stage": "epistemic_research",
            "engine": "S660",
            "status": "READY",
        },
        {
            "step": 2,
            "stage": "freeze_sdr",
            "artifact": "SDR",
            "status": "READY",
        },
    ]
    if "writing" in intents and "writing_engine" in active:
        plan.append(
            {
                "step": len(plan) + 1,
                "stage": "writing_engine",
                "engine": "writing_engine",
                "read_only_from": "SDR",
                "status": "READY",
            }
        )
    if "figure" in intents and "figure_engine" in active:
        figure_step: Dict[str, Any] = {
            "step": len(plan) + 1,
            "stage": "figure_engine",
            "engine": "figure_engine",
            "read_only_from": "SDR",
            "status": "READY",
        }
        if FIGURE_CAPABILITY_ID in missing_capabilities:
            figure_step["status"] = "BLOCKED_SOURCE_UNAVAILABLE"
            figure_step["missing_capabilities"] = [FIGURE_CAPABILITY_ID]
        plan.append(figure_step)
    return plan


def _score_candidates(
    trusted_query: str,
    intents: Mapping[str, Sequence[str]],
    primary: str,
    companions: Sequence[str],
    forbidden: Sequence[str],
    active: Mapping[str, Mapping[str, Any]],
    topk: int,
) -> List[Dict[str, Any]]:
    forbidden_set = set(forbidden)
    scores: Dict[str, float] = {}
    reasons: Dict[str, List[str]] = {}

    def add(skill_id: str, points: float, reason: str) -> None:
        if skill_id not in active or skill_id in forbidden_set:
            return
        scores[skill_id] = scores.get(skill_id, 0.0) + points
        reasons.setdefault(skill_id, []).append(reason)

    add(primary, 100.0, "primary_policy")
    for position, skill_id in enumerate(companions):
        add(skill_id, 50.0 - position * 0.1, "required_companion")

    for skill_id, entry in active.items():
        for trigger in entry.get("triggers", []):
            if _contains_hint(trusted_query, trigger):
                add(skill_id, 1.0 + min(len(trigger), 60) / 100.0, f"manifest_trigger:{trigger}")

    ordered = sorted(scores, key=lambda item: (-scores[item], item))[: max(1, topk)]
    return [
        {
            "id": skill_id,
            "path": str(active[skill_id]["path"]),
            "score": round(scores[skill_id], 3),
            "reasons": _dedupe(reasons[skill_id]),
        }
        for skill_id in ordered
    ]


def route_query(
    query: str,
    *,
    untrusted_text: str = "",
    topk: int = 5,
    manifest_path: Path = MANIFEST_PATH,
    capability_root: Path = ROOT,
    capabilities_manifest_path: Path = CAPABILITIES_MANIFEST_PATH,
) -> Dict[str, Any]:
    """Return a deterministic, serializable routing decision."""

    trusted_query, payload = split_trusted_and_payload(query, untrusted_text)
    active = load_active_manifest(manifest_path)
    negation_matches = _find_negations(trusted_query)
    negated = {
        family: _dedupe(match_text for match_text, _, _ in matches)
        for family, matches in negation_matches.items()
    }
    positive_query = _mask_negated_spans(trusted_query, negation_matches)
    intents = detect_intents(positive_query, {})
    if (
        "proof" in negated
        and intents.get("proof") == ["mathematical_symbol"]
    ):
        intents.pop("proof")
    if (
        not intents
        and re.search(r"(?i)\b(?:figure|proof|writing|coding)_engine\b", trusted_query)
    ):
        intents["route"] = ["engine_applicability"]
    ambiguous_intents = _ordered_families(set(negated).intersection(intents))
    forbidden = _dedupe(
        route_id
        for family in negated
        for route_id in NEGATED_ROUTE_IDS.get(family, ())
        if route_id in active
    )
    capabilities = inspect_capabilities(capability_root, capabilities_manifest_path)
    required_capabilities = [FIGURE_CAPABILITY_ID] if "figure" in intents else []
    missing_capabilities = [
        capability
        for capability in required_capabilities
        if not capabilities.get(capability, {}).get("available", False)
    ]
    required_runtime_responses = {
        capability: response
        for capability in missing_capabilities
        if (
            response := capabilities.get(capability, {}).get(
                "required_runtime_response"
            )
        )
    }

    status = "ROUTE_AMBIGUOUS" if ambiguous_intents else "ROUTED"
    primary = ""
    companions: List[str] = []
    candidates: List[Dict[str, Any]] = []
    execution_plan: List[Dict[str, Any]] = []
    if not ambiguous_intents:
        primary = _select_primary(intents, active)
        if primary in forbidden:
            primary = "S432" if "S432" in active and "S432" not in forbidden else ""
        if primary == "figure_engine" and FIGURE_CAPABILITY_ID in missing_capabilities:
            status = "SOURCE_UNAVAILABLE"
            primary = ""
        else:
            companions = _required_companions(primary, intents, active, forbidden)
            candidates = _score_candidates(
                trusted_query,
                intents,
                primary,
                companions,
                forbidden,
                active,
                topk,
            )
            execution_plan = _build_execution_plan(
                primary,
                intents,
                active,
                missing_capabilities,
            )
            if missing_capabilities:
                status = "SOURCE_UNAVAILABLE"

    payload_bytes = payload.encode("utf-8")
    return {
        "router_version": ROUTER_VERSION,
        "status": status,
        "manifest": str(manifest_path.relative_to(ROOT).as_posix())
        if manifest_path.is_relative_to(ROOT)
        else str(manifest_path),
        "trusted_query": trusted_query,
        "ignored_untrusted_payload": {
            "present": bool(payload),
            "bytes": len(payload_bytes),
            "sha256": hashlib.sha256(payload_bytes).hexdigest() if payload else None,
        },
        "suspicious_untrusted_instructions": inspect_untrusted_payload(payload),
        "negated_intents": {key: list(value) for key, value in sorted(negated.items())},
        "detected_intents": {key: list(value) for key, value in sorted(intents.items())},
        "ambiguous_intents": ambiguous_intents,
        "capabilities": capabilities,
        "missing_capabilities": missing_capabilities,
        "required_runtime_responses": required_runtime_responses,
        "primary": primary or None,
        "primary_path": str(active[primary]["path"]) if primary else None,
        "required_companions": companions,
        "forbidden_routes": forbidden,
        "candidates": candidates,
        "execution_plan": execution_plan,
        "fallback_used": status == "ROUTED" and not bool(intents),
    }


def _render_human(result: Mapping[str, Any]) -> str:
    lines = [
        f"ROUTER_VERSION: {result['router_version']}",
        f"STATUS: {result['status']}",
        f"PRIMARY: {result['primary'] or 'NONE'}",
    ]
    if result.get("primary_path"):
        lines.append(f"PRIMARY_PATH: {result['primary_path']}")
    companions = result.get("required_companions", [])
    lines.append("REQUIRED_COMPANIONS: " + (", ".join(companions) if companions else "NONE"))
    forbidden = result.get("forbidden_routes", [])
    lines.append("FORBIDDEN_ROUTES: " + (", ".join(forbidden) if forbidden else "NONE"))
    detected = result.get("detected_intents", {})
    lines.append("DETECTED_INTENTS: " + (", ".join(detected) if detected else "NONE"))
    negated = result.get("negated_intents", {})
    lines.append("NEGATED_INTENTS: " + (", ".join(negated) if negated else "NONE"))
    ambiguous = result.get("ambiguous_intents", [])
    lines.append("AMBIGUOUS_INTENTS: " + (", ".join(ambiguous) if ambiguous else "NONE"))
    missing = result.get("missing_capabilities", [])
    lines.append("MISSING_CAPABILITIES: " + (", ".join(missing) if missing else "NONE"))
    runtime_responses = result.get("required_runtime_responses", {})
    for capability, response in runtime_responses.items():
        lines.append(f"REQUIRED_RUNTIME_RESPONSE[{capability}]: {response}")
    plan = result.get("execution_plan", [])
    lines.append(
        "EXECUTION_PLAN: "
        + (json.dumps(plan, ensure_ascii=False, sort_keys=True) if plan else "NONE")
    )
    payload = result.get("ignored_untrusted_payload", {})
    lines.append(
        "UNTRUSTED_PAYLOAD: "
        + (f"IGNORED ({payload.get('bytes', 0)} bytes)" if payload.get("present") else "NONE")
    )
    suspicious = result.get("suspicious_untrusted_instructions", [])
    if suspicious:
        lines.append("SUSPICIOUS_UNTRUSTED_INSTRUCTIONS: " + ", ".join(suspicious))
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Trust-aware deterministic ZIP-your-Research router")
    parser.add_argument("query", help="trusted user routing request")
    payload_group = parser.add_mutually_exclusive_group()
    payload_group.add_argument("--untrusted-text", default="", help="quoted/untrusted content; ignored for routing")
    payload_group.add_argument(
        "--untrusted-text-file",
        type=Path,
        help="UTF-8 file containing quoted/untrusted content; ignored for routing",
    )
    parser.add_argument("--topk", type=int, default=5, help="number of ranked candidates")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    return parser


def cli_main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.topk < 1:
        raise SystemExit("--topk must be >= 1")
    untrusted_text = args.untrusted_text
    if args.untrusted_text_file:
        try:
            untrusted_text = args.untrusted_text_file.read_text(encoding="utf-8")
        except OSError as exc:
            raise SystemExit(f"cannot read untrusted text file: {exc}") from exc
    try:
        result = route_query(args.query, untrusted_text=untrusted_text, topk=args.topk)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        print(f"route error: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(_render_human(result))
    return 0 if result["status"] == "ROUTED" else 1


if __name__ == "__main__":
    raise SystemExit(cli_main())
