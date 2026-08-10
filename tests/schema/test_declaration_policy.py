from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_DIR = ROOT / "schemas" / "core"
VALID_DIR = ROOT / "examples" / "valid" / "declarations"
INVALID_DIR = ROOT / "examples" / "invalid" / "declarations"
VOCAB_CATALOG = ROOT / "vocabularies" / "catalog.v0.1.0.json"
FOUNDATION_VOCAB = ROOT / "vocabularies" / "foundation" / "foundation.v0.1.0.json"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _registry() -> Registry:
    registry = Registry()
    for path in sorted(SCHEMA_DIR.glob("*.schema.json")):
        schema = _load(path)
        schema["$id"] = path.as_uri()
        registry = registry.with_resource(path.as_uri(), Resource.from_contents(schema))
    return registry


REGISTRY = _registry()
FORMAT_CHECKER = FormatChecker()


def _validation_errors(case: dict) -> list:
    schema_path = SCHEMA_DIR / case["_schema"]
    schema = _load(schema_path)
    schema["$id"] = schema_path.as_uri()
    validator = Draft202012Validator(
        schema,
        registry=REGISTRY,
        format_checker=FORMAT_CHECKER,
    )
    return list(validator.iter_errors(case["instance"]))


def _duplicates(declarations: list[dict]) -> bool:
    identifiers = [declaration["identifier"] for declaration in declarations]
    return len(identifiers) != len(set(identifiers))


def interpretation_errors(
    document: dict,
    *,
    supported_profiles: set[tuple[str, str]] | None = None,
    supported_modules: set[tuple[str, str]] | None = None,
    supported_vocabularies: set[tuple[str, str]] | None = None,
    supported_extensions: set[tuple[str, str | None]] | None = None,
) -> list[str]:
    profiles = document.get("profiles", [])
    modules = document.get("modules", [])
    vocabularies = document.get("vocabularies", [])
    extensions = document.get("extensions", {})

    errors: list[str] = []
    if _duplicates(profiles):
        errors.append("duplicate_profile_identifier")
    if _duplicates(modules):
        errors.append("duplicate_module_identifier")
    if _duplicates(vocabularies):
        errors.append("duplicate_vocabulary_identifier")

    supported_profiles = supported_profiles or set()
    supported_modules = supported_modules or set()
    supported_vocabularies = supported_vocabularies or set()
    supported_extensions = supported_extensions or set()

    for declaration in profiles:
        key = (declaration["identifier"], declaration["version"])
        if key not in supported_profiles:
            errors.append("unsupported_profile")

    for declaration in modules:
        key = (declaration["identifier"], declaration["version"])
        if key not in supported_modules:
            errors.append("unsupported_module")

    for declaration in vocabularies:
        key = (declaration["identifier"], declaration["version"])
        if declaration["required"] and key not in supported_vocabularies:
            errors.append("unsupported_required_vocabulary")

    for identifier, extension in extensions.items():
        key = (identifier, extension.get("version"))
        if extension["required"] and key not in supported_extensions:
            errors.append("unsupported_required_extension")

    return errors


def test_valid_declaration_examples_are_structurally_valid() -> None:
    for path in sorted(VALID_DIR.glob("*.json")):
        case = _load(path)
        assert not _validation_errors(case), path.name


def test_structurally_invalid_declaration_examples_fail() -> None:
    for path in sorted(INVALID_DIR.glob("*.json")):
        case = _load(path)
        if "_semantic_error" in case:
            continue
        assert _validation_errors(case), path.name


def test_duplicate_declaration_identifiers_are_semantic_errors() -> None:
    case = _load(INVALID_DIR / "document-duplicate-profile-identifier.json")
    assert not _validation_errors(case)
    assert case["_semantic_error"] in interpretation_errors(case["instance"])


def test_profiles_and_modules_require_exact_supported_versions() -> None:
    document = _load(VALID_DIR / "document-profile-module-vocabulary.json")["instance"]
    errors = interpretation_errors(document)
    assert "unsupported_profile" in errors
    assert "unsupported_module" in errors

    profile = document["profiles"][0]
    module = document["modules"][0]
    errors = interpretation_errors(
        document,
        supported_profiles={(profile["identifier"], profile["version"])},
        supported_modules={(module["identifier"], module["version"])},
    )
    assert errors == []


def test_unknown_optional_extension_does_not_block_interpretation() -> None:
    document = _load(VALID_DIR / "document-unknown-optional-extension.json")["instance"]
    assert interpretation_errors(document) == []


def test_required_extension_must_be_supported() -> None:
    document = _load(VALID_DIR / "document-required-extension-with-schema.json")["instance"]
    assert interpretation_errors(document) == ["unsupported_required_extension"]

    identifier, extension = next(iter(document["extensions"].items()))
    supported = {(identifier, extension["version"])}
    assert interpretation_errors(document, supported_extensions=supported) == []


def test_required_additional_vocabulary_must_be_supported() -> None:
    document = _load(VALID_DIR / "document-required-vocabulary.json")["instance"]
    assert interpretation_errors(document) == ["unsupported_required_vocabulary"]

    vocabulary = document["vocabularies"][0]
    supported = {(vocabulary["identifier"], vocabulary["version"])}
    assert interpretation_errors(document, supported_vocabularies=supported) == []


def test_vocabulary_catalog_matches_artifact_metadata() -> None:
    catalog = _load(VOCAB_CATALOG)
    identifiers = [entry["identifier"] for entry in catalog["vocabularies"]]
    assert len(identifiers) == len(set(identifiers))

    for entry in catalog["vocabularies"]:
        document = _load(ROOT / "vocabularies" / entry["path"])
        assert document["identifier"] == entry["identifier"]
        assert document["version"] == entry["version"]


def test_foundation_vocabulary_mirrors_schema_control_terms() -> None:
    foundation = _load(FOUNDATION_VOCAB)["vocabularies"]

    result_form = _load(SCHEMA_DIR / "result-form.schema.json")
    result_terms = {branch["properties"]["type"]["const"] for branch in result_form["oneOf"]}
    assert result_terms == set(foundation["result_form_type"]["terms"])

    statistic = _load(SCHEMA_DIR / "reported-statistic.schema.json")
    statistic_terms = {branch["properties"]["type"]["const"] for branch in statistic["oneOf"]}
    assert statistic_terms == set(foundation["reported_statistic_type"]["terms"])

    diagnostic = _load(SCHEMA_DIR / "diagnostic.schema.json")
    assert set(diagnostic["properties"]["severity"]["enum"]) == set(
        foundation["diagnostic_severity"]["terms"]
    )

    constraint = _load(SCHEMA_DIR / "constraint-outcome.schema.json")
    assert set(constraint["properties"]["status"]["enum"]) == set(
        foundation["constraint_outcome_status"]["terms"]
    )

    calculation = _load(SCHEMA_DIR / "calculation-result.schema.json")
    calculation_terms = set(calculation["properties"]["status"]["oneOf"][0]["enum"])
    assert calculation_terms == set(foundation["calculation_status"]["terms"])

    selection_terms = set(calculation["properties"]["selection_status"]["enum"])
    assert selection_terms == set(foundation["selection_status"]["terms"])

    loss_report = _load(SCHEMA_DIR / "loss-report.schema.json")
    loss_terms = set(
        loss_report["$defs"]["loss_entry"]["properties"]["category"]["oneOf"][0]["enum"]
    )
    assert loss_terms == set(foundation["loss_category"]["terms"])

    interchange = _load(SCHEMA_DIR / "interchange-report.schema.json")
    for property_name, vocabulary_name in (
        ("operation", "interchange_operation"),
        ("status", "interchange_status"),
        ("preservation_status", "preservation_status"),
    ):
        assert set(interchange["properties"][property_name]["enum"]) == set(
            foundation[vocabulary_name]["terms"]
        )
