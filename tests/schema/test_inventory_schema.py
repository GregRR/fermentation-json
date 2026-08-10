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
INVENTORY_SCHEMA = json.loads((ROOT / "schemas/production/inventory.schema.json").read_text())


def _validator(anchor: str) -> Draft202012Validator:
    schema = {"$ref": f"{INVENTORY_SCHEMA['$id']}#{anchor}"}
    return Draft202012Validator(schema, registry=REGISTRY, format_checker=FormatChecker())


def _load_example(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text())["instance"]


def test_valid_material_lot_validates() -> None:
    errors = list(
        _validator("materialLot").iter_errors(
            _load_example("examples/valid/production/material-lot.json")
        )
    )
    assert not errors, "; ".join(error.message for error in errors)


def test_valid_inventory_position_validates() -> None:
    errors = list(
        _validator("inventoryPosition").iter_errors(
            _load_example("examples/valid/production/inventory-position.json")
        )
    )
    assert not errors, "; ".join(error.message for error in errors)


def test_inventory_position_requires_material_reference() -> None:
    errors = list(
        _validator("inventoryPosition").iter_errors(
            _load_example(
                "examples/invalid/production/inventory-position-missing-material-reference.json"
            )
        )
    )
    assert errors


def test_inventory_position_rejects_non_inventory_quantity_kind() -> None:
    errors = list(
        _validator("inventoryPosition").iter_errors(
            _load_example("examples/invalid/production/inventory-position-wrong-quantity-kind.json")
        )
    )
    assert errors


def test_material_lot_does_not_embed_current_inventory_quantity() -> None:
    lot_properties = INVENTORY_SCHEMA["$defs"]["material_lot"]["properties"]
    assert "quantity" not in lot_properties
    assert "quantity" in INVENTORY_SCHEMA["$defs"]["inventory_position"]["properties"]


def test_inventory_quantity_allows_mass_volume_and_count_only() -> None:
    refs = INVENTORY_SCHEMA["$defs"]["inventory_quantity"]["oneOf"]
    assert refs == [
        {"$ref": "#inventoryMassQuantity"},
        {"$ref": "#inventoryVolumeQuantity"},
        {"$ref": "#inventoryCountQuantity"},
    ]
