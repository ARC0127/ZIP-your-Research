#!/usr/bin/env python3
"""Run public routing regression cases.

Usage:
  python router/test_route_v1_7.py
  python router/test_route_v1_7.py --cases tests/router/cases_v2.jsonl
"""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence

from route_v1_7 import route_query


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CASES = ROOT / "tests" / "router" / "cases_v2.jsonl"
FIGURE_CAPABILITY_ID = "figures4papers_source"


def _load_cases(path: Path) -> List[Dict[str, Any]]:
    cases: List[Dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_number}: invalid JSON: {exc}") from exc
        if not isinstance(item, dict) or not item.get("name") or "query" not in item:
            raise ValueError(f"{path}:{line_number}: case requires name and query")
        cases.append(item)
    if not cases:
        raise ValueError(f"{path}: no cases")
    return cases


def _missing(expected: Iterable[str], actual: Iterable[str]) -> List[str]:
    actual_set = set(actual)
    return [item for item in expected if item not in actual_set]


def _route_case(
    case: Dict[str, Any], profile_override: str | None = None
) -> Dict[str, Any]:
    profile = profile_override or str(case.get("capability_profile", "source_tree"))
    route_kwargs = {
        "untrusted_text": str(case.get("untrusted_text", "")),
        "topk": int(case.get("topk", 10)),
    }
    if profile == "source_tree":
        return route_query(str(case["query"]), capability_root=ROOT, **route_kwargs)
    if profile == "release_without_figure_backend":
        with tempfile.TemporaryDirectory(prefix="zyr-release-capability-") as temp_dir:
            return route_query(
                str(case["query"]),
                capability_root=Path(temp_dir),
                **route_kwargs,
            )
    if profile == "missing_capabilities_manifest":
        with tempfile.TemporaryDirectory(prefix="zyr-missing-capability-manifest-") as temp_dir:
            return route_query(
                str(case["query"]),
                capability_root=ROOT,
                capabilities_manifest_path=Path(temp_dir) / "RELEASE_CAPABILITIES.yaml",
                **route_kwargs,
            )
    raise ValueError(f"unknown capability_profile: {profile}")


def _with_runtime_expectations(
    case: Dict[str, Any], result: Dict[str, Any]
) -> Dict[str, Any]:
    effective = dict(case)
    safe_expectations = case.get("safe_release_expectations")
    figure_available = bool(
        result["capabilities"].get(FIGURE_CAPABILITY_ID, {}).get("available")
    )
    if not figure_available and safe_expectations is not None:
        if not isinstance(safe_expectations, dict):
            raise ValueError("safe_release_expectations must be a mapping")
        effective.update(safe_expectations)
    return effective


def _check_result(
    case: Dict[str, Any], result: Dict[str, Any], scenario: str = ""
) -> List[str]:
    errors: List[str] = []
    name = str(case["name"]) + scenario

    if "expected_status" in case and result["status"] != case["expected_status"]:
        errors.append(
            f"{name}: status={result['status']!r}, expected {case['expected_status']!r}"
        )

    if "expected_primary" in case and result["primary"] != case["expected_primary"]:
        errors.append(
            f"{name}: primary={result['primary']!r}, expected {case['expected_primary']!r}"
        )

    expected_trusted = case.get("expected_trusted_query")
    if expected_trusted is not None and result["trusted_query"] != expected_trusted:
        errors.append(
            f"{name}: trusted_query={result['trusted_query']!r}, expected {expected_trusted!r}"
        )

    checks = (
        ("required_companions", result["required_companions"]),
        ("forbidden_routes", result["forbidden_routes"]),
        ("detected_intents", result["detected_intents"].keys()),
        ("negated_intents", result["negated_intents"].keys()),
        ("suspicious_payload", result["suspicious_untrusted_instructions"]),
        ("required_runtime_responses", result["required_runtime_responses"].keys()),
    )
    for field, actual in checks:
        missing = _missing(case.get(field, []), actual)
        if missing:
            errors.append(f"{name}: {field} missing {missing!r}; actual={list(actual)!r}")

    exact_checks = (
        ("expected_execution_plan", "execution_plan"),
        ("expected_ambiguous_intents", "ambiguous_intents"),
        ("expected_missing_capabilities", "missing_capabilities"),
    )
    for case_field, result_field in exact_checks:
        if case_field in case and result[result_field] != case[case_field]:
            errors.append(
                f"{name}: {result_field}={result[result_field]!r}, "
                f"expected {case[case_field]!r}"
            )

    requirements = case.get("requires_capabilities", {})
    if isinstance(requirements, list):
        requirements = {capability: True for capability in requirements}
    if not isinstance(requirements, dict):
        errors.append(f"{name}: requires_capabilities must be a list or mapping")
        requirements = {}
    for capability, expected_available in requirements.items():
        state = result["capabilities"].get(str(capability))
        actual_available = bool(state and state.get("available"))
        if actual_available != bool(expected_available):
            errors.append(
                f"{name}: capability {capability!r} available={actual_available!r}, "
                f"expected {bool(expected_available)!r}"
            )

    all_selected = {
        result["primary"],
        *result["required_companions"],
        *(candidate["id"] for candidate in result["candidates"]),
        *(step.get("engine") for step in result["execution_plan"]),
    }
    leaked = [item for item in case.get("absent_routes", []) if item in all_selected]
    if leaked:
        errors.append(f"{name}: forbidden-by-case routes selected: {leaked!r}")

    if "payload_ignored" in case:
        actual_ignored = bool(result["ignored_untrusted_payload"]["present"])
        if actual_ignored != bool(case["payload_ignored"]):
            errors.append(
                f"{name}: payload ignored={actual_ignored!r}, expected {case['payload_ignored']!r}"
            )
    return errors


def check_case(case: Dict[str, Any]) -> List[str]:
    name = str(case["name"])
    try:
        result = _route_case(case)
        effective_case = _with_runtime_expectations(case, result)
    except ValueError as exc:
        return [f"{name}: {exc}"]

    errors = _check_result(effective_case, result)
    safe_expectations = case.get("safe_release_expectations")
    source_profile = str(case.get("capability_profile", "source_tree")) == "source_tree"
    figure_available = bool(
        result["capabilities"].get(FIGURE_CAPABILITY_ID, {}).get("available")
    )
    if safe_expectations is not None and source_profile and figure_available:
        try:
            release_result = _route_case(
                case, profile_override="release_without_figure_backend"
            )
            release_case = _with_runtime_expectations(case, release_result)
        except ValueError as exc:
            errors.append(f"{name}[simulated_safe_release]: {exc}")
        else:
            errors.extend(
                _check_result(
                    release_case,
                    release_result,
                    scenario="[simulated_safe_release]",
                )
            )
    return errors


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run v1.7 router regression cases")
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASES)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        cases = _load_cases(args.cases)
    except (OSError, ValueError) as exc:
        print(f"router test setup error: {exc}", file=sys.stderr)
        return 2

    errors: List[str] = []
    for case in cases:
        errors.extend(check_case(case))
    if errors:
        print(f"FAIL: {len(errors)} routing assertion(s) failed across {len(cases)} cases")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"PASS: {len(cases)} public routing cases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
