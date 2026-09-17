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
MATERIAL_USE_SCHEMA = json.loads((ROOT / "schemas/production/material-use.schema.json").read_text())


def _validator(anchor: str) -> Draft202012Validator:
    schema = {"$ref": f"{MATERIAL_USE_SCHEMA['$id']}#{anchor}"}
    return Draft202012Validator(schema, registry=REGISTRY, format_checker=FormatChecker())


def _load_example(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text())["instance"]


def test_valid_planned_material_use_validates() -> None:
    errors = list(
        _validator("plannedMaterialUse").iter_errors(
            _load_example("examples/valid/production/planned-material-use.json")
        )
    )
    assert not errors, "; ".join(error.message for error in errors)


def test_planned_material_use_may_omit_quantity() -> None:
    errors = list(
        _validator("plannedMaterialUse").iter_errors(
            _load_example("examples/valid/production/planned-material-use-without-quantity.json")
        )
    )
    assert not errors, "; ".join(error.message for error in errors)


def test_planned_material_use_requires_material_reference() -> None:
    errors = list(
        _validator("plannedMaterialUse").iter_errors(
            _load_example(
                "examples/invalid/production/planned-material-use-missing-material-reference.json"
            )
        )
    )
    assert errors


def test_planned_material_use_rejects_undeclared_timing_shape() -> None:
    errors = list(
        _validator("plannedMaterialUse").iter_errors(
            _load_example("examples/invalid/production/planned-material-use-unknown-field.json")
        )
    )
    assert errors


def test_planned_quantity_uses_generic_quantity_schema() -> None:
    planned_properties = MATERIAL_USE_SCHEMA["$defs"]["planned_material_use"]["properties"]
    assert planned_properties["planned_quantity"] == {
        "$ref": "../core/quantity.schema.json#quantity"
    }


def test_valid_actual_material_use_validates() -> None:
    errors = list(
        _validator("actualMaterialUse").iter_errors(
            _load_example("examples/valid/production/actual-material-use.json")
        )
    )
    assert not errors, "; ".join(error.message for error in errors)


def test_actual_material_use_may_omit_lot_reference() -> None:
    errors = list(
        _validator("actualMaterialUse").iter_errors(
            _load_example("examples/valid/production/actual-material-use-without-lot.json")
        )
    )
    assert not errors, "; ".join(error.message for error in errors)


def test_actual_material_use_requires_actual_quantity() -> None:
    errors = list(
        _validator("actualMaterialUse").iter_errors(
            _load_example("examples/invalid/production/actual-material-use-missing-quantity.json")
        )
    )
    assert errors


def test_actual_material_use_rejects_inline_inventory_state() -> None:
    errors = list(
        _validator("actualMaterialUse").iter_errors(
            _load_example("examples/invalid/production/actual-material-use-unknown-field.json")
        )
    )
    assert errors


def test_actual_quantity_uses_generic_quantity_schema() -> None:
    actual_properties = MATERIAL_USE_SCHEMA["$defs"]["actual_material_use"]["properties"]
    assert actual_properties["actual_quantity"] == {"$ref": "../core/quantity.schema.json#quantity"}
