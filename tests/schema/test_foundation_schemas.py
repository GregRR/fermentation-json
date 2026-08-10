from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource


ROOT = Path(__file__).resolve().parents[2]
SCHEMA_DIR = ROOT / "schemas" / "core"
VALID_DIR = ROOT / "examples" / "valid" / "foundation"
INVALID_DIR = ROOT / "examples" / "invalid" / "foundation"


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _schema_with_retrieval_id(path: Path) -> dict:
    schema = copy.deepcopy(_load_json(path))
    schema["$id"] = path.as_uri()
    return schema


def _registry() -> Registry:
    registry = Registry()
    for path in sorted(SCHEMA_DIR.glob("*.schema.json")):
        schema = _schema_with_retrieval_id(path)
        registry = registry.with_resource(path.as_uri(), Resource.from_contents(schema))
    return registry


REGISTRY = _registry()
FORMAT_CHECKER = FormatChecker()


@pytest.mark.parametrize("schema_path", sorted(SCHEMA_DIR.glob("*.schema.json")))
def test_foundation_schema_is_valid_draft_2020_12(schema_path: Path) -> None:
    Draft202012Validator.check_schema(_load_json(schema_path))


def _validate_case(path: Path) -> list:
    case = _load_json(path)
    schema_path = SCHEMA_DIR / case["_schema"]
    schema = _schema_with_retrieval_id(schema_path)
    validator = Draft202012Validator(
        schema,
        registry=REGISTRY,
        format_checker=FORMAT_CHECKER,
    )
    return sorted(
        validator.iter_errors(case["instance"]),
        key=lambda error: list(error.absolute_path),
    )


@pytest.mark.parametrize("case_path", sorted(VALID_DIR.glob("*.json")))
def test_valid_foundation_examples(case_path: Path) -> None:
    errors = _validate_case(case_path)
    assert not errors, "\n".join(error.message for error in errors)


@pytest.mark.parametrize("case_path", sorted(INVALID_DIR.glob("*.json")))
def test_invalid_foundation_examples(case_path: Path) -> None:
    assert _validate_case(case_path), f"{case_path.name} unexpectedly validated"
