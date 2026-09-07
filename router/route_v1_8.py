#!/usr/bin/env python3
"""Route tasks without automatically activating a multi-agent workflow.

Usage:
  python router/route_v1_8.py "权威检索近期论文" --json
  python router/route_v1_8.py "Use multi-agent research, then write the manuscript" --json

Retains v1_7 trust, negation, ambiguity, and capability checks. The v1_7 CLI
remains available for its historical complete-workflow routing contract.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

# Also supports importlib loading by the installed manifest-router wrapper.
sys.path.insert(0, str(Path(__file__).resolve().parent))
import route_v1_7 as baseline


TEAM_REQUEST = re.compile(
    r"(?i)(?:\b(?:use|run|launch|conduct|coordinate|perform)\b|调度|使用|启动|调用|开展)"
    r".{0,30}(?:multi[- ]agent|independent.{0,12}(?:review|critic)|多智能体|多代理|独立交叉审查)"
    r"|^(?:multi[- ]agent research|多智能体科研|独立交叉审查)"
)
FULL_DOCUMENT = re.compile(r"(?i)full (?:manuscript|paper|workflow)|integrated manuscript|全文|统稿|全局审计")
NAMED_REQUEST = re.compile(
    r"(?i)(?:\b(?:use|run|invoke|select)\s+|(?:调用|使用|执行|选用)\s*)"
    r"([a-z][a-z0-9_]*)"
)
NAMED_NEGATION = re.compile(
    r"(?i)(?:\b(?:do not|don't|never)\s+|不要\s*|禁止\s*|不使用\s*)"
    r"(?:(?:use|run|invoke|select|调用|使用|执行)\s*)?([a-z][a-z0-9_]*)"
)


def route_query(query: str, **kwargs) -> dict:
    result = baseline.route_query(query, **kwargs)
    result["router_version"] = "1.8.0"
    result["execution_profile"] = "resource_proportional_v1"
    result["optional_companions"] = []
    result["agent_mode"] = "single"
    trusted = result["trusted_query"]
    positive = baseline._mask_negated_spans(trusted, baseline._find_negations(trusted))
    intents = result["detected_intents"]
    active = baseline.load_active_manifest(kwargs.get("manifest_path", baseline.MANIFEST_PATH))
    canonical_names = {sid.lower(): sid for sid in active}
    denied_names = [canonical_names[m.group(1).lower()] for m in NAMED_NEGATION.finditer(positive)
                    if m.group(1).lower() in canonical_names]
    positive = NAMED_NEGATION.sub(lambda m: " " * len(m.group(0)), positive)
    named = [canonical_names[m.group(1).lower()] for m in NAMED_REQUEST.finditer(positive)
             if m.group(1).lower() in canonical_names]
    result["forbidden_routes"] = baseline._dedupe(result["forbidden_routes"] + denied_names)
    team_requested = "S660" in named or bool(TEAM_REQUEST.search(positive))
    # v1_7 groups ordinary search and team research into one intent family.
    # A denied team plus a positive ordinary search is not a contradiction.
    if "evolution" in result["ambiguous_intents"] and not team_requested:
        result["ambiguous_intents"].remove("evolution")
    if set(named).intersection(result["forbidden_routes"]):
        result["ambiguous_intents"].append("explicit_route")
    if team_requested and "S660" in result["forbidden_routes"] and "evolution" not in result["ambiguous_intents"]:
        result["ambiguous_intents"].append("evolution")
    if result["ambiguous_intents"]:
        result.update(status="ROUTE_AMBIGUOUS", primary=None, primary_path=None,
                      required_companions=[], candidates=[], execution_plan=[])
        return result

    team = team_requested and "S660" not in result["forbidden_routes"]
    primary = named[0] if named else baseline._select_primary(intents, active)
    original_companions = baseline._required_companions(primary, intents, active, result["forbidden_routes"])

    if team and not named and primary != "S661":
        primary = "S660"
    elif primary == "S660" and not team:
        primary = "S204"  # single-agent literature triage, no worker capability gate
    elif not named and primary == "writing_engine" and set(intents) == {"writing"} and not FULL_DOCUMENT.search(positive):
        if re.search(r"(?i)polish|rewrite|润色|改写", positive):
            primary = "S603"
    elif not named and primary == "proof_engine" and set(intents) == {"logic"}:
        primary = "S226"

    result["status"] = "SOURCE_UNAVAILABLE" if result["missing_capabilities"] else "ROUTED"
    if primary in result["forbidden_routes"]:
        primary = "S432" if "S432" not in result["forbidden_routes"] else None
    if primary == "figure_engine" and not result["capabilities"].get(baseline.FIGURE_CAPABILITY_ID, {}).get("available", False):
        primary = None
        result["status"] = "SOURCE_UNAVAILABLE"
        capability = baseline.FIGURE_CAPABILITY_ID
        result["missing_capabilities"] = baseline._dedupe(result["missing_capabilities"] + [capability])
        response = result["capabilities"].get(capability, {}).get("required_runtime_response")
        if response:
            result["required_runtime_responses"][capability] = response
    if not primary:
        result.update(primary=None, primary_path=None, required_companions=[], candidates=[], execution_plan=[])
        return result  # e.g. unavailable requested figure backend

    if primary == "S660" and team:
        result["agent_mode"] = "multi_agent_requested"
        companions = baseline._required_companions(primary, intents, active, result["forbidden_routes"])
    elif primary == "S661" or named or FULL_DOCUMENT.search(positive):
        companions = original_companions
    else:
        # Keep obligations the user actually requested; related skills are optional.
        requested = {
            "citation": ["S424"], "logic": ["S226"], "method": ["S227"],
            "proof": ["S237", "S240"], "writing": ["writing_engine"],
            "figure": ["figure_engine", "S623"], "experiment": ["S303", "S327"],
            "novelty": ["S224"],
        }
        satisfied = {
            "writing_engine": {"writing"}, "S603": {"writing"},
            "S226": {"logic"}, "figure_engine": {"figure"},
        }.get(primary, set())
        companions = baseline._dedupe(
            sid for family, sids in requested.items()
            if family in intents and family not in satisfied for sid in sids
        )
    companions = [sid for sid in companions if sid != primary and sid in active and sid not in result["forbidden_routes"]]
    result["optional_companions"] = [sid for sid in original_companions if sid not in companions and sid != primary]
    result["primary"] = primary
    result["primary_path"] = str(active[primary]["path"])
    result["required_companions"] = companions
    result["candidates"] = baseline._score_candidates(trusted, intents, primary, companions, result["forbidden_routes"], active, kwargs.get("topk", 5))
    if not team and primary != "S661":
        result["candidates"] = [item for item in result["candidates"] if item["id"] != "S660"]
    plan = baseline._build_execution_plan(primary, intents, active, result["missing_capabilities"])
    if primary == "S204":
        # Preserve all requested outputs from a formerly S660-led compound task.
        prior_plan = baseline._build_execution_plan("S660", intents, active, result["missing_capabilities"])
        if len(prior_plan) > 2:
            plan.extend(prior_plan[1:])
    result["execution_plan"] = plan
    result["fallback_used"] = not (named or team or intents)
    return result


def cli_main(argv=None) -> int:
    parser = baseline.build_parser()
    args = parser.parse_args(argv)
    if args.topk < 1:
        raise SystemExit("--topk must be >= 1")
    payload = args.untrusted_text
    if args.untrusted_text_file:
        try:
            payload = args.untrusted_text_file.read_text(encoding="utf-8")
        except OSError as exc:
            parser.error(str(exc))
    result = route_query(args.query, untrusted_text=payload, topk=args.topk)
    print(json.dumps(result, ensure_ascii=False, indent=2) if args.json else baseline._render_human(result))
    return 0 if result["status"] == "ROUTED" else 2


if __name__ == "__main__":
    raise SystemExit(cli_main())
