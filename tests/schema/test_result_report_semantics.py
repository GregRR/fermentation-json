from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VALID_DIR = ROOT / "examples" / "valid" / "foundation"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _constraint_ids(result: dict) -> set[str]:
    return {constraint["constraint_id"] for constraint in result.get("constraints", [])}


def _assert_outcomes_reference_constraints(result: dict) -> None:
    known = _constraint_ids(result)

    top_level_outcomes = result.get("constraint_outcomes", [])
    for outcome in top_level_outcomes:
        assert outcome["constraint_id"] in known

    for candidate in result.get("candidates", []):
        for outcome in candidate.get("constraint_outcomes", []):
            assert outcome["constraint_id"] in known


def test_calculation_constraint_ids_are_unique() -> None:
    for path in sorted(VALID_DIR.glob("calculation-result-*.json")):
        result = _load(path)["instance"]
        ids = [constraint["constraint_id"] for constraint in result.get("constraints", [])]
        assert len(ids) == len(set(ids)), path.name


def test_constraint_outcomes_reference_declared_constraints() -> None:
    for path in sorted(VALID_DIR.glob("calculation-result-*.json")):
        result = _load(path)["instance"]
        _assert_outcomes_reference_constraints(result)


def test_candidate_ranks_are_unique() -> None:
    for path in sorted(VALID_DIR.glob("calculation-result-*.json")):
        result = _load(path)["instance"]
        ranks = [candidate["rank"] for candidate in result.get("candidates", [])]
        assert len(ranks) == len(set(ranks)), path.name


def test_embedded_loss_report_matches_interchange_endpoints() -> None:
    for path in sorted(VALID_DIR.glob("interchange-report-*.json")):
        report = _load(path)["instance"]
        loss_report = report.get("loss_report")
        if loss_report is None:
            continue
        assert loss_report["source"] == report["source"], path.name
        assert loss_report["target"] == report["target"], path.name
