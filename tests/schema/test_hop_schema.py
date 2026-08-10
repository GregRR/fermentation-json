from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[2]
CATALOG = json.loads((ROOT / "schemas/catalog.v0.1.0.json").read_text())


def _registry() -> Registry:
    registry = Registry()
    for entry in CATALOG["schemas"]:
        schema = json.loads((ROOT / "schemas" / entry["path"]).read_text())
        registry = registry.with_resource(entry["id"], Resource.from_contents(schema))
    return registry


REGISTRY = _registry()
HOP_PATH = ROOT / "schemas/ingredients/hop.schema.json"
HOP_SCHEMA = json.loads(HOP_PATH.read_text())
VALIDATOR = Draft202012Validator(HOP_SCHEMA, registry=REGISTRY, format_checker=FormatChecker())
HOP_FORMS = json.loads((ROOT / "vocabularies/hop-forms/hop-forms.v0.1.0.json").read_text())


def _load_example(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text())["instance"]


def test_hop_form_schema_matches_registered_core_vocabulary() -> None:
    schema_forms = set(HOP_SCHEMA["$defs"]["hop_form"]["oneOf"][0]["enum"])
    vocabulary_forms = {entry["id"] for entry in HOP_FORMS["entries"]}
    assert schema_forms == vocabulary_forms


def test_valid_hop_definition_validates() -> None:
    errors = list(
        VALIDATOR.iter_errors(_load_example("examples/valid/ingredients/hop-definition.json"))
    )
    assert not errors, "; ".join(error.message for error in errors)


def test_hop_alpha_acid_rejects_wrong_quantity_kind() -> None:
    errors = list(
        VALIDATOR.iter_errors(
            _load_example("examples/invalid/ingredients/hop-alpha-acid-wrong-kind.json")
        )
    )
    assert errors


def test_unknown_core_style_hop_form_is_rejected() -> None:
    errors = list(
        VALIDATOR.iter_errors(
            _load_example("examples/invalid/ingredients/hop-unknown-core-form.json")
        )
    )
    assert errors
