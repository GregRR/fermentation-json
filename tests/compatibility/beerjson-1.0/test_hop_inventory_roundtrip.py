from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "compatibility/beerjson-1.0"
MAPPING = json.loads((BASE / "mappings/hop-inventory.v0.1.0.json").read_text())
VECTORS = json.loads((BASE / "fixtures/hop-inventory-roundtrip-v0.1.0.json").read_text())
CATALOG = json.loads((ROOT / "schemas/catalog.v0.1.0.json").read_text())
INVENTORY_SCHEMA = json.loads((ROOT / "schemas/production/inventory.schema.json").read_text())
UNITS = json.loads((ROOT / "vocabularies/units/units.v0.1.0.json").read_text())
UNIT_BY_ID = {entry["id"]: entry for entry in UNITS["entries"]}


def _registry() -> Registry:
    registry = Registry()
    for entry in CATALOG["schemas"]:
        schema = json.loads((ROOT / "schemas" / entry["path"]).read_text())
        registry = registry.with_resource(entry["id"], Resource.from_contents(schema))
    return registry


REGISTRY = _registry()
POSITION_VALIDATOR = Draft202012Validator(
    {"$ref": f"{INVENTORY_SCHEMA['$id']}#inventoryPosition"},
    registry=REGISTRY,
    format_checker=FormatChecker(),
)


def test_mapping_requires_contextual_material_reference_and_never_invents_lot() -> None:
    assert MAPPING["source_type"] == "hop.json#HopInventoryType"
    assert MAPPING["source_context"] == "hop.json#VarietyInformation.inventory"
    assert "material_reference" in MAPPING["context_requirements"][0]
    assert "Do not create a native materialLot" in MAPPING["lot_policy"]


def test_native_inventory_vectors_validate_when_present() -> None:
    for vector in VECTORS["vectors"]:
        native = vector["expected_native_inventory_position"]
        if native is None:
            continue
        errors = list(POSITION_VALIDATOR.iter_errors(native))
        assert not errors, (vector["id"], [error.message for error in errors])


def test_mass_and_volume_vectors_preserve_reported_source_units() -> None:
    by_id = {vector["id"]: vector for vector in VECTORS["vectors"]}

    mass = by_id["mass_amount_maps_to_separate_inventory_position"]
    mass_quantity = mass["expected_native_inventory_position"]["quantity"]
    assert mass_quantity["quantity_kind"] == "mass"
    assert mass_quantity["canonical"]["unit"] == "kilogram"
    assert mass_quantity["reported"]["original_unit_text"] == "kg"

    volume = by_id["volume_amount_maps_without_inventing_lot"]
    volume_quantity = volume["expected_native_inventory_position"]["quantity"]
    assert volume_quantity["quantity_kind"] == "volume"
    assert volume_quantity["canonical"]["unit"] == "liter"
    assert volume_quantity["reported"]["unit"] == "us_liquid_gallon"
    assert volume["expected_native_lot"] is None

    gallon = UNIT_BY_ID["us_liquid_gallon"]["conversion_to_dimension_reference"]
    factor = float(gallon["factor_numerator"]) / float(gallon["factor_denominator"])
    assert abs(volume_quantity["canonical"]["form"]["value"] - factor) < 1e-12


def test_empty_inventory_is_not_reinterpreted_as_zero() -> None:
    vector = next(
        vector
        for vector in VECTORS["vectors"]
        if vector["id"] == "empty_inventory_object_is_preserved_not_zeroed"
    )
    assert vector["source_inventory"] == {}
    assert vector["expected_native_inventory_position"] is None
    assert vector["expected_roundtrip_inventory"] == {}
    assert vector["source_preservation_required"] is True


def test_missing_material_context_uses_source_preservation() -> None:
    vector = next(
        vector
        for vector in VECTORS["vectors"]
        if vector["id"] == "missing_native_material_context_uses_source_preservation"
    )
    assert vector["context"]["native_material_reference"] is None
    assert vector["expected_native_inventory_position"] is None
    assert vector["expected_roundtrip_inventory"] == vector["source_inventory"]


def test_all_vectors_roundtrip_the_beerjson_inventory_object_exactly() -> None:
    for vector in VECTORS["vectors"]:
        assert vector["expected_roundtrip_inventory"] == vector["source_inventory"], vector["id"]
