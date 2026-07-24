#!/usr/bin/env python3
"""Stable public CLI for repository integrity checks.

Usage:
  python tools/zyr.py manifest [--id S201] [--json]
  python tools/zyr.py init TARGET [--dry-run | --apply]
  python tools/zyr.py check
  python tools/zyr.py check --ci
  python tools/zyr.py build
  python tools/zyr.py build --check
  python tools/zyr.py route "trusted query" [--json]
  python tools/zyr.py route-test
  python tools/zyr.py skill-memory draft TRACE.yaml
  python tools/zyr.py skill-memory plan create --root ROOT --proposal PROPOSAL.yaml --trusted-consent-public-key HOST.pem
  python tools/zyr.py skill-memory apply create --root ROOT --proposal PROPOSAL.yaml --trusted-consent-public-key HOST.pem --consent-id ID --consent-attestation ATTESTATION.json
  python tools/zyr.py skill-memory list --root ROOT
  python tools/zyr.py skill-memory search --root ROOT --query QUERY
  python tools/zyr.py skill-memory verify --root ROOT
  python tools/zyr.py release-audit RELEASE.zip
"""

from __future__ import annotations

import argparse
import sys

sys.dont_write_bytecode = True

from zyr_lib.build import run_build, run_build_check
from zyr_lib.check import run_check
from zyr_lib.forward import run_repository_cli
from zyr_lib.init import run_init
from zyr_lib.manifest import run_manifest
from zyr_lib.skill_memory import (
    run_skill_memory_apply,
    run_skill_memory_draft,
    run_skill_memory_list,
    run_skill_memory_plan,
    run_skill_memory_search,
    run_skill_memory_verify,
)


def positive_integer(raw: str) -> int:
    value = int(raw)
    if value < 1:
        raise argparse.ArgumentTypeError("value must be >= 1")
    return value


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="ZYR stable repository facade",
        epilog="Exit codes: 0=success, 1=contract/test/audit failure, 2=invalid usage or backend setup error.",
    )
    commands = parser.add_subparsers(dest="command", required=True)

    manifest_parser = commands.add_parser(
        "manifest", help="inspect validated active canonical skill metadata"
    )
    manifest_parser.add_argument("--id", default="", help="show one active skill id")
    manifest_parser.add_argument(
        "--json", action="store_true", dest="manifest_json", help="emit JSON"
    )

    init_parser = commands.add_parser(
        "init", help="plan or create a minimal research workspace"
    )
    init_parser.add_argument("target", help="explicit target directory")
    init_mode = init_parser.add_mutually_exclusive_group()
    init_mode.add_argument(
        "--dry-run",
        action="store_true",
        help="show the exact plan without writing (default)",
    )
    init_mode.add_argument(
        "--apply",
        action="store_true",
        help="write the displayed plan; default behavior is dry-run",
    )
    init_parser.add_argument(
        "--json", action="store_true", dest="init_json", help="emit JSON"
    )

    check_parser = commands.add_parser(
        "check", help="run strict canonical-skill and generated-artifact checks"
    )
    check_parser.add_argument(
        "--ci",
        action="store_true",
        help="emit CI-mode status; checks remain read-only and deterministic",
    )

    build_parser = commands.add_parser(
        "build", help="atomically build allowlisted outputs, or check without writing"
    )
    build_parser.add_argument(
        "--check",
        action="store_true",
        help="render in memory and fail if a generated artifact has drifted",
    )

    route_parser = commands.add_parser(
        "route", help="run the trust-aware deterministic router"
    )
    route_parser.add_argument("query", help="trusted user routing request")
    route_payload = route_parser.add_mutually_exclusive_group()
    route_payload.add_argument("--untrusted-text", default="")
    route_payload.add_argument("--untrusted-text-file", default="")
    route_parser.add_argument("--topk", type=positive_integer, default=5)
    route_parser.add_argument(
        "--json", action="store_true", dest="route_json", help="emit router JSON"
    )

    route_test_parser = commands.add_parser(
        "route-test", help="run public deterministic router regression cases"
    )
    route_test_parser.add_argument(
        "--cases", default="", help="optional cases JSONL path"
    )

    skill_memory_parser = commands.add_parser(
        "skill-memory",
        help="draft, evaluate, and govern user-generated procedural-memory Skills",
    )
    skill_memory_commands = skill_memory_parser.add_subparsers(
        dest="skill_memory_command", required=True
    )

    skill_memory_draft = skill_memory_commands.add_parser(
        "draft", help="render a Skill proposal from one VERIFIED_SUCCESS trace"
    )
    skill_memory_draft.add_argument("trace", help="verified trace YAML path")
    skill_memory_draft.add_argument(
        "--skill-id",
        default="",
        help="optional stable dyn-* id; otherwise derived from task_family",
    )
    skill_memory_draft.add_argument(
        "--json", action="store_true", dest="skill_memory_json"
    )

    skill_memory_operations = (
        "create",
        "update",
        "promote",
        "rollback",
        "deprecate",
        "delete",
        "recover",
    )
    for mode in ("plan", "apply"):
        mode_parser = skill_memory_commands.add_parser(
            mode,
            help=(
                "show an exact read-only change plan"
                if mode == "plan"
                else "apply an unchanged plan after host-attested exact consent"
            ),
        )
        mode_parser.add_argument("operation", choices=skill_memory_operations)
        mode_parser.add_argument(
            "--root",
            required=True,
            help="explicit dynamic Skill memory root outside this source repository",
        )
        mode_parser.add_argument(
            "--proposal",
            default="",
            help="content-bound proposal YAML; required for create/update",
        )
        mode_parser.add_argument(
            "--skill-id",
            default="",
            help="stable dyn-* id; required for promote/rollback/deprecate/delete",
        )
        mode_parser.add_argument(
            "--version",
            type=positive_integer,
            default=None,
            help="candidate or rollback version",
        )
        mode_parser.add_argument(
            "--evaluation",
            default="",
            help="independent behavioral evaluation YAML; required for promote",
        )
        mode_parser.add_argument(
            "--trusted-consent-public-key",
            required=True,
            help=(
                "host-controlled Ed25519 public key PEM; pinned when the store "
                "is created"
            ),
        )
        if mode == "apply":
            mode_parser.add_argument(
                "--consent-id",
                required=True,
                help="exact one-operation consent id emitted by the current plan",
            )
            mode_parser.add_argument(
                "--consent-attestation",
                required=True,
                help=(
                    "host-signed, short-lived user-consent JSON bound to this plan"
                ),
            )
        mode_parser.add_argument(
            "--json", action="store_true", dest="skill_memory_json"
        )

    skill_memory_list = skill_memory_commands.add_parser(
        "list", help="list dynamic Skill registry metadata"
    )
    skill_memory_list.add_argument("--root", required=True)
    skill_memory_list.add_argument("--include-deleted", action="store_true")
    skill_memory_list.add_argument(
        "--json", action="store_true", dest="skill_memory_json"
    )

    skill_memory_search = skill_memory_commands.add_parser(
        "search", help="search ACTIVE Skill metadata with progressive disclosure"
    )
    skill_memory_search.add_argument("--root", required=True)
    skill_memory_search.add_argument("--query", required=True)
    skill_memory_search.add_argument("--topk", type=positive_integer, default=5)
    skill_memory_search.add_argument(
        "--json", action="store_true", dest="skill_memory_json"
    )

    skill_memory_verify = skill_memory_commands.add_parser(
        "verify", help="verify registry, payload, audit, active projection, and index"
    )
    skill_memory_verify.add_argument("--root", required=True)
    skill_memory_verify.add_argument(
        "--json", action="store_true", dest="skill_memory_json"
    )

    release_parser = commands.add_parser(
        "release-audit", help="audit an existing release ZIP fail-closed"
    )
    release_parser.add_argument("archive", help="release ZIP to audit")
    release_parser.add_argument("--root", default="", dest="release_root")
    release_parser.add_argument("--policy", default="")
    release_parser.add_argument("--third-party", default="", dest="third_party")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.command == "manifest":
        return run_manifest(skill_id=args.id, json_output=args.manifest_json)
    if args.command == "init":
        return run_init(args.target, apply=args.apply, json_output=args.init_json)
    if args.command == "check":
        return run_check(ci_mode=args.ci)
    if args.command == "build":
        return run_build_check() if args.check else run_build()
    if args.command == "route":
        forwarded = [args.query, "--topk", str(args.topk)]
        if args.untrusted_text:
            forwarded.extend(("--untrusted-text", args.untrusted_text))
        if args.untrusted_text_file:
            forwarded.extend(("--untrusted-text-file", args.untrusted_text_file))
        if args.route_json:
            forwarded.append("--json")
        return run_repository_cli("router/route_v1_7.py", forwarded)
    if args.command == "route-test":
        forwarded = ["--cases", args.cases] if args.cases else []
        return run_repository_cli("router/test_route_v1_7.py", forwarded)
    if args.command == "skill-memory":
        if args.skill_memory_command == "draft":
            return run_skill_memory_draft(
                args.trace,
                skill_id=args.skill_id,
                json_output=args.skill_memory_json,
            )
        if args.skill_memory_command == "plan":
            return run_skill_memory_plan(
                args.operation,
                args.root,
                proposal=args.proposal,
                skill_id=args.skill_id,
                version=args.version,
                evaluation=args.evaluation,
                trusted_consent_public_key=args.trusted_consent_public_key,
                json_output=args.skill_memory_json,
            )
        if args.skill_memory_command == "apply":
            return run_skill_memory_apply(
                args.operation,
                args.root,
                consent_id=args.consent_id,
                consent_attestation=args.consent_attestation,
                trusted_consent_public_key=args.trusted_consent_public_key,
                proposal=args.proposal,
                skill_id=args.skill_id,
                version=args.version,
                evaluation=args.evaluation,
                json_output=args.skill_memory_json,
            )
        if args.skill_memory_command == "list":
            return run_skill_memory_list(
                args.root,
                include_deleted=args.include_deleted,
                json_output=args.skill_memory_json,
            )
        if args.skill_memory_command == "search":
            return run_skill_memory_search(
                args.root,
                args.query,
                topk=args.topk,
                json_output=args.skill_memory_json,
            )
        if args.skill_memory_command == "verify":
            return run_skill_memory_verify(
                args.root,
                json_output=args.skill_memory_json,
            )
    if args.command == "release-audit":
        forwarded = [args.archive]
        if args.release_root:
            forwarded.extend(("--root", args.release_root))
        if args.policy:
            forwarded.extend(("--policy", args.policy))
        if args.third_party:
            forwarded.extend(("--third-party", args.third_party))
        return run_repository_cli("tools/audit_release_v1_7.py", forwarded)
    raise SystemExit(f"Unsupported command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
