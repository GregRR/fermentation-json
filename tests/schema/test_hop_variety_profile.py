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
HOP_SCHEMA = json.loads((ROOT / "schemas/ingredients/hop.schema.json").read_text())
PROFILE_SCHEMA = {"$ref": f"{HOP_SCHEMA['$id']}#hopVarietyProfile"}
VALIDATOR = Draft202012Validator(PROFILE_SCHEMA, registry=REGISTRY, format_checker=FormatChecker())
ROLES = json.loads(
    (ROOT / "vocabularies/hop-variety-roles/hop-variety-roles.v0.1.0.json").read_text()
)
COMPONENTS = json.loads(
    (ROOT / "vocabularies/hop-oil-components/hop-oil-components.v0.1.0.json").read_text()
)
UNITS = {
    entry["id"]: entry
    for entry in json.loads((ROOT / "vocabularies/units/units.v0.1.0.json").read_text())["entries"]
}


def _load_example(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text())["instance"]


def test_hop_variety_role_schema_matches_vocabulary() -> None:
    schema_roles = set(HOP_SCHEMA["$defs"]["hop_variety_role"]["oneOf"][0]["enum"])
    vocabulary_roles = {entry["id"] for entry in ROLES["entries"]}
    assert schema_roles == vocabulary_roles


def test_hop_oil_component_schema_matches_vocabulary() -> None:
    schema_components = set(HOP_SCHEMA["$defs"]["hop_oil_component"]["oneOf"][0]["enum"])
    vocabulary_components = {entry["id"] for entry in COMPONENTS["entries"]}
    assert schema_components == vocabulary_components


def test_valid_hop_variety_profile_validates() -> None:
    errors = list(
        VALIDATOR.iter_errors(_load_example("examples/valid/ingredients/hop-variety-profile.json"))
    )
    assert not errors, "; ".join(error.message for error in errors)


def test_unknown_core_hop_variety_role_is_rejected() -> None:
    errors = list(
        VALIDATOR.iter_errors(
            _load_example("examples/invalid/ingredients/hop-variety-profile-unknown-role.json")
        )
    )
    assert errors


def test_hop_oil_component_requires_fraction_quantity() -> None:
    errors = list(
        VALIDATOR.iter_errors(
            _load_example("examples/invalid/ingredients/hop-oil-component-wrong-kind.json")
        )
    )
    assert errors


def test_milliliter_per_100_gram_is_exactly_one_hundredth_liter_per_kilogram() -> None:
    unit = UNITS["milliliter_per_100_gram"]
    assert unit["dimension"] == "specific_volume"
    conversion = unit["conversion_to_dimension_reference"]
    assert conversion["type"] == "linear"
    assert conversion["factor_numerator"] == "1"
    assert conversion["factor_denominator"] == "100"
