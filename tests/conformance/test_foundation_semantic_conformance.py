from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SUITE_DIR = ROOT / "conformance" / "foundation" / "v0.1.0"
MANIFEST_PATH = SUITE_DIR / "manifest.json"
DERIVED_STATES = {"calculated", "derived", "estimated", "inferred", "predicted"}


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _tuples(values: list[list[str]] | None) -> set[tuple[str, str]]:
    return {tuple(value) for value in (values or [])}


def _reference_errors(data: dict) -> list[str]:
    object_ids = data.get("object_ids", [])
    errors: list[str] = []

    if len(object_ids) != len(set(object_ids)):
        errors.append("duplicate_object_id")

    known = set(object_ids)
    current_document_id = data["document_id"]
    for reference in data.get("references", []):
        object_id = reference.get("object_id")
        if object_id is None:
            continue

        reference_document_id = reference.get("document_id")
        is_local = reference_document_id in (None, current_document_id)
        if is_local and object_id not in known:
            errors.append("unresolved_local_reference")

    return errors


def _artifact_errors(data: dict) -> list[str]:
    document = data["document"]
    supported = data.get("supported", {})
    supported_profiles = _tuples(supported.get("profiles"))
    supported_modules = _tuples(supported.get("modules"))
    supported_vocabularies = _tuples(supported.get("vocabularies"))
    supported_extensions = _tuples(supported.get("extensions"))

    errors: list[str] = []
    for declaration in document.get("profiles", []):
        key = (declaration["identifier"], declaration["version"])
        if key not in supported_profiles:
            errors.append("unsupported_profile")

    for declaration in document.get("modules", []):
        key = (declaration["identifier"], declaration["version"])
        if key not in supported_modules:
            errors.append("unsupported_module")

    for declaration in document.get("vocabularies", []):
        key = (declaration["identifier"], declaration["version"])
        if declaration["required"] and key not in supported_vocabularies:
            errors.append("unsupported_required_vocabulary")

    for identifier, extension in document.get("extensions", {}).items():
        key = (identifier, extension.get("version"))
        if extension["required"] and key not in supported_extensions:
            errors.append("unsupported_required_extension")

    return errors


def _quantity_errors(data: dict) -> list[str]:
    quantity = data["quantity"]
    if "derivation" not in quantity:
        return []

    states = set(quantity.get("epistemic_state", []))
    if not states.intersection(DERIVED_STATES):
        return ["derivation_missing_derived_epistemic_state"]
    return []


def _interchange_errors(data: dict) -> list[str]:
    report = data["report"]
    loss_report = report.get("loss_report")
    if loss_report is None:
        return []

    errors: list[str] = []
    if loss_report["source"] != report["source"] or loss_report["target"] != report["target"]:
        errors.append("loss_report_endpoint_mismatch")

    for field in ("compatibility_profile_id", "compatibility_profile_version"):
        if field in report and loss_report.get(field) != report[field]:
            errors.append("loss_report_compatibility_profile_mismatch")
            break

    for entry in loss_report["entries"]:
        if not entry.get("source_path") and "source_object" not in entry:
            errors.append("loss_entry_missing_source_attribution")
        if not entry.get("transformation") and not entry.get("explanation"):
            errors.append("loss_entry_missing_transformation_description")

    return errors


EVALUATORS = {
    "reference_integrity": _reference_errors,
    "required_artifact_support": _artifact_errors,
    "source_and_derivation_semantics": _quantity_errors,
    "interchange_loss_consistency": _interchange_errors,
}


def test_manifest_vector_hashes_are_exact() -> None:
    manifest = _load(MANIFEST_PATH)
    assert manifest["suite_version"] == "0.1.0"
    assert manifest["schema_set_version"] == "0.1.0"

    for vector_set in manifest["vector_sets"]:
        path = SUITE_DIR / vector_set["path"]
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        assert digest == vector_set["sha256"], path.name


def test_manifest_rule_ids_are_unique_and_covered() -> None:
    manifest = _load(MANIFEST_PATH)
    rule_ids = [rule["id"] for rule in manifest["rules"]]
    assert len(rule_ids) == len(set(rule_ids))

    expected_errors: set[str] = set()
    for vector_set in manifest["vector_sets"]:
        document = _load(SUITE_DIR / vector_set["path"])
        for case in document["cases"]:
            expected_errors.update(case["expected"]["errors"])

    assert expected_errors.issubset(set(rule_ids))


def test_foundation_semantic_vectors() -> None:
    manifest = _load(MANIFEST_PATH)

    for vector_set in manifest["vector_sets"]:
        document = _load(SUITE_DIR / vector_set["path"])
        assert document["suite_id"] == manifest["suite_id"]
        assert document["suite_version"] == manifest["suite_version"]
        evaluator = EVALUATORS[document["vector_set"]]

        case_ids = [case["id"] for case in document["cases"]]
        assert len(case_ids) == len(set(case_ids)), vector_set["path"]

        for case in document["cases"]:
            errors = evaluator(case["input"])
            expected_errors = case["expected"]["errors"]
            assert sorted(errors) == sorted(expected_errors), case["id"]
            assert (not errors) is case["expected"]["conformant"], case["id"]
