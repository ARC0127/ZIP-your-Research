"""Deterministic structure tests for the public epistemic mutation fixtures.

Usage:
    python3 -m unittest tests.evolution.test_public_mutations_v1
    python3 tests/evolution/test_public_mutations_v1.py
"""

from __future__ import annotations

import json
import unittest
from collections import Counter, defaultdict
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURE_PATH = REPO_ROOT / "tests/evolution/public_mutations_v1.jsonl"
MANIFEST_PATH = REPO_ROOT / "skills_manifest.yaml"
S660_PATH = REPO_ROOT / "skills/research_orchestrator/S660_epistemic_research_champion.md"
RUN_TEMPLATE_PATH = REPO_ROOT / "templates/orchestration/RESEARCH_RUN.md"
MEMORY_PROTOCOL_PATH = REPO_ROOT / "docs/memory/VISIBLE_MEMORY_PROTOCOL_v1.md"
HOST_CONTRACT_PATH = REPO_ROOT / "interfaces/host_adapter_contract.md"

REQUIRED_FIELDS = {
    "schema_version",
    "case_id",
    "pair_id",
    "variant",
    "domain",
    "title",
    "input",
    "expected_action",
    "must_detect",
    "must_not_claim",
    "oracle",
}


def load_cases() -> list[dict]:
    cases = []
    for line_number, line in enumerate(
        FIXTURE_PATH.read_text(encoding="utf-8").splitlines(), start=1
    ):
        if not line.strip():
            continue
        try:
            cases.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise AssertionError(f"invalid JSON on line {line_number}: {exc}") from exc
    return cases


class PublicEvolutionFixtureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.cases = load_cases()

    def test_exactly_twelve_mutation_clean_pairs(self) -> None:
        self.assertEqual(len(self.cases), 24)
        self.assertEqual(
            Counter(case["variant"] for case in self.cases),
            Counter({"mutation": 12, "clean": 12}),
        )

        by_pair = defaultdict(list)
        for case in self.cases:
            by_pair[case["pair_id"]].append(case)

        self.assertEqual(len(by_pair), 12)
        for pair_id, cases in by_pair.items():
            with self.subTest(pair_id=pair_id):
                self.assertEqual(len(cases), 2)
                self.assertEqual(
                    Counter(case["variant"] for case in cases),
                    Counter({"mutation": 1, "clean": 1}),
                )

    def test_ids_fields_and_actions_are_deterministic(self) -> None:
        case_ids = [case["case_id"] for case in self.cases]
        pair_ids = {case["pair_id"] for case in self.cases}
        self.assertEqual(len(case_ids), len(set(case_ids)))
        self.assertEqual(pair_ids, {f"M{index:02d}" for index in range(1, 13)})

        for case in self.cases:
            with self.subTest(case_id=case["case_id"]):
                self.assertEqual(set(case), REQUIRED_FIELDS)
                self.assertEqual(case["schema_version"], "1.0")
                self.assertTrue(case["input"].strip())
                self.assertTrue(case["must_detect"])
                self.assertTrue(case["must_not_claim"])
                expected = "REOPEN" if case["variant"] == "mutation" else "PROCEED"
                self.assertEqual(case["expected_action"], expected)

    def test_high_risk_renderer_figure_and_memory_pairs_exist(self) -> None:
        domains_by_pair = {
            pair_id: {case["domain"] for case in self.cases if case["pair_id"] == pair_id}
            for pair_id in ("M09", "M11", "M12")
        }
        self.assertEqual(domains_by_pair["M09"], {"rendering"})
        self.assertEqual(domains_by_pair["M11"], {"figure"})
        self.assertEqual(domains_by_pair["M12"], {"memory"})

    def test_s660_manifest_entry_and_path(self) -> None:
        manifest = yaml.safe_load(MANIFEST_PATH.read_text(encoding="utf-8"))
        entries = [item for item in manifest["skills"] if item.get("id") == "S660"]
        self.assertEqual(len(entries), 1)
        entry = entries[0]
        self.assertEqual(entry["name"], "epistemic_research_champion")
        self.assertEqual(entry["category"], "research_core")
        self.assertEqual(REPO_ROOT / entry["path"], S660_PATH)
        self.assertTrue(S660_PATH.is_file())

    def test_orchestration_and_memory_boundaries_are_present(self) -> None:
        s660 = S660_PATH.read_text(encoding="utf-8")
        run_template = RUN_TEMPLATE_PATH.read_text(encoding="utf-8")
        memory_protocol = MEMORY_PROTOCOL_PATH.read_text(encoding="utf-8")
        host_contract = HOST_CONTRACT_PATH.read_text(encoding="utf-8")

        for marker in (
            "MULTI_AGENT_UNAVAILABLE",
            "Scientific Decision Record",
            "read-only",
            "model-weight",
            "persistent-memory",
            "No majority vote",
        ):
            with self.subTest(file="S660", marker=marker):
                self.assertIn(marker, s660)

        for marker in (
            "Scientific Decision Record (SDR)",
            "Read-only rendering checks",
            "No persistent write is implied",
        ):
            with self.subTest(file="RESEARCH_RUN", marker=marker):
                self.assertIn(marker, run_template)

        for marker in (
            "Markdown is the authoritative representation",
            "second,",
            "write-specific",
            "No save authorizes Git staging",
            "Similarity is not truth",
        ):
            with self.subTest(file="memory protocol", marker=marker):
                self.assertIn(marker, memory_protocol)

        for marker in (
            "Invented personas",
            "exact records or diff",
            "second, write-specific",
        ):
            with self.subTest(file="host contract", marker=marker):
                self.assertIn(marker, host_contract)


if __name__ == "__main__":
    unittest.main()
