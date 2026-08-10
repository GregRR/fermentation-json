from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
COMPAT_DIR = ROOT / "compatibility" / "beerjson-1.0"
INVENTORY_FILE = COMPAT_DIR / "inventory" / "beerjson-v1.0.2-inventory.json"
TYPE_MAPPING_FILE = COMPAT_DIR / "mappings" / "measurable-types.v0.1.0.json"
UNIT_MAPPING_FILE = COMPAT_DIR / "mappings" / "unit-tokens.v0.1.0.json"
ANALYTICAL_MAPPING_FILE = COMPAT_DIR / "mappings" / "analytical-scales.v0.1.0.json"
SCALE_FILE = ROOT / "vocabularies" / "measurement-scales" / "measurement-scales.v0.1.0.json"
UNIT_FILE = ROOT / "vocabularies" / "units" / "units.v0.1.0.json"
KIND_FILE = ROOT / "vocabularies" / "quantity-kinds" / "quantity-kinds.v0.1.0.json"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _by_id(entries: list[dict]) -> dict[str, dict]:
    return {entry["id"]: entry for entry in entries}


INVENTORY = _load(INVENTORY_FILE)
TYPE_MAPPING = _load(TYPE_MAPPING_FILE)
UNIT_MAPPING = _load(UNIT_MAPPING_FILE)
ANALYTICAL_MAPPING = _load(ANALYTICAL_MAPPING_FILE)
UNITS = _by_id(_load(UNIT_FILE)["entries"])
KINDS = _by_id(_load(KIND_FILE)["entries"])
SCALES = _by_id(_load(SCALE_FILE)["entries"])


def _factor(unit_id: str) -> Fraction:
    conversion = UNITS[unit_id]["conversion_to_dimension_reference"]
    return Fraction(
        int(conversion["factor_numerator"]),
        int(conversion["factor_denominator"]),
    )


def test_all_beerjson_measurable_object_types_are_accounted_for() -> None:
    quantity_types: set[str] = set()
    range_types: set[str] = set()

    for type_id, metadata in INVENTORY["types"].items():
        if not type_id.startswith("measureable_units.json#"):
            continue
        if metadata["kind"] != "object":
            continue

        name = type_id.split("#", maxsplit=1)[1]
        fields = set(metadata["fields"])
        if fields == {"unit", "value"}:
            quantity_types.add(name)
        elif fields == {"minimum", "maximum"}:
            range_types.add(name)

    assert set(TYPE_MAPPING["quantity_type_mappings"]) == quantity_types
    assert set(TYPE_MAPPING["range_type_mappings"]) == range_types


def test_all_native_quantity_kinds_named_by_mapping_exist() -> None:
    for mapping in TYPE_MAPPING["quantity_type_mappings"].values():
        kind = mapping.get("quantity_kind")
        if kind is not None:
            assert kind in KINDS

        for token_kind in mapping.get("token_quantity_kinds", {}).values():
            assert token_kind in KINDS


def test_every_resolved_beerjson_unit_maps_to_registered_unit() -> None:
    for unit_type in UNIT_MAPPING["unit_types"].values():
        for mapping in unit_type.values():
            unit_id = mapping["fermentationjson_unit"]
            if unit_id is not None:
                assert unit_id in UNITS


def test_specific_volume_composite_units_match_core_constituents() -> None:
    assert _factor("us_liquid_quart_per_pound") == _factor("us_liquid_quart") / _factor(
        "pound_avoirdupois"
    )
    assert _factor("us_liquid_gallon_per_pound") == _factor("us_liquid_gallon") / _factor(
        "pound_avoirdupois"
    )
    assert _factor("us_liquid_gallon_per_ounce") == _factor("us_liquid_gallon") / _factor(
        "ounce_avoirdupois"
    )
    assert _factor("us_fluid_ounce_per_ounce") == _factor("us_fluid_ounce") / _factor(
        "ounce_avoirdupois"
    )


def test_concentration_type_does_not_conflate_ratios_with_mass_concentration() -> None:
    mapping = TYPE_MAPPING["quantity_type_mappings"]["ConcentrationType"]
    token_kinds = mapping["token_quantity_kinds"]

    assert token_kinds["mg/l"] == "mass_concentration"
    assert token_kinds["ppm"] == "fraction"
    assert token_kinds["ppb"] == "fraction"


def test_analytical_scale_types_are_resolved_without_becoming_unit_families() -> None:
    expected_types = {
        "BitternessType",
        "CarbonationType",
        "ColorType",
        "DiastaticPowerType",
        "GravityType",
    }
    mappings = TYPE_MAPPING["quantity_type_mappings"]

    for type_name in expected_types:
        assert "pending" not in mappings[type_name]["status"]
        assert mappings[type_name]["analytical_scale_mapping"] == "analytical-scales.v0.1.0.json"

    for dispatch in ANALYTICAL_MAPPING["type_dispatch"].values():
        for mapping in dispatch.values():
            assert mapping["quantity_kind"] in KINDS
            if scale_id := mapping.get("scale"):
                assert scale_id in SCALES
                assert scale_id not in UNITS


def test_analytical_source_tokens_map_to_unit_plus_scale_not_fake_units() -> None:
    for unit_type in (
        "GravityUnitType",
        "ColorUnitType",
        "CarbonationUnitType",
        "BitternessUnitType",
        "DiastaticPowerUnitType",
    ):
        for source_token, mapping in UNIT_MAPPING["unit_types"][unit_type].items():
            if source_token == "g/l":
                assert mapping["fermentationjson_unit"] == "gram_per_liter"
                assert "fermentationjson_scale" not in mapping
                continue
            assert mapping["fermentationjson_unit"] == "one"
            assert mapping["fermentationjson_scale"] in SCALES
            assert source_token not in UNITS


def test_gravity_scales_remain_semantically_distinct() -> None:
    dispatch = ANALYTICAL_MAPPING["type_dispatch"]["GravityType"]
    assert dispatch["sg"]["quantity_kind"] == "specific_gravity"
    assert dispatch["plato"]["quantity_kind"] == "plato_extract"
    assert dispatch["brix"]["quantity_kind"] == "brix_reading"
    assert len({mapping["quantity_kind"] for mapping in dispatch.values()}) == 3


def test_carbonation_volumes_and_mass_concentration_are_distinct() -> None:
    dispatch = ANALYTICAL_MAPPING["type_dispatch"]["CarbonationType"]
    assert dispatch["vols"]["quantity_kind"] == "carbon_dioxide_volume_ratio"
    assert dispatch["vols"]["scale"] == "carbon_dioxide_volumes"
    assert dispatch["g/l"]["quantity_kind"] == "mass_concentration"
    assert dispatch["g/l"]["unit"] == "gram_per_liter"
    assert dispatch["g/l"]["scale"] is None


def test_cross_scale_relationships_are_not_unit_conversions() -> None:
    rules = ANALYTICAL_MAPPING["non_unit_conversion_rules"]
    assert rules
    for rule in rules:
        assert rule["status"] != "unit_conversion"


def test_range_mapping_requires_endpoint_source_preservation() -> None:
    mappings = TYPE_MAPPING["range_type_mappings"]
    for mapping in mappings.values():
        policy = mapping["reported_endpoint_unit_policy"]
        assert policy in {
            "preserve_independently_when_source_units_differ",
            "preserve_source_objects",
            "preserve_source_objects_and_scale_tokens",
        }


def test_compatibility_profile_and_field_mapping_reference_measurable_mapping() -> None:
    profile = _load(COMPAT_DIR / "profile.v0.1.0.json")
    field_mapping = _load(COMPAT_DIR / "mappings" / "field-mapping.v0.1.0.json")

    assert profile["measurable_type_mapping"] == "mappings/measurable-types.v0.1.0.json"
    assert profile["analytical_scale_mapping"] == "mappings/analytical-scales.v0.1.0.json"
    assert field_mapping["measurable_type_mapping"] == "measurable-types.v0.1.0.json"
    assert field_mapping["analytical_scale_mapping"] == "analytical-scales.v0.1.0.json"
