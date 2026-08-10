from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
COMPAT = ROOT / "compatibility" / "beerjson-1.0"
INVENTORY = json.loads((COMPAT / "inventory/beerjson-v1.0.2-inventory.json").read_text())
FIELD_MAPPING = json.loads((COMPAT / "mappings/field-mapping.v0.1.0.json").read_text())
PRIMITIVES = json.loads((COMPAT / "mappings/primitive-field-semantics.v0.1.0.json").read_text())
VECTORS = json.loads((COMPAT / "fixtures/primitive-field-vectors.v0.1.0.json").read_text())
UNITS = {
    entry["id"]: entry
    for entry in json.loads((ROOT / "vocabularies/units/units.v0.1.0.json").read_text())["entries"]
}
KINDS = {
    entry["id"]: entry
    for entry in json.loads(
        (ROOT / "vocabularies/quantity-kinds/quantity-kinds.v0.1.0.json").read_text()
    )["entries"]
}


def _domain_fields_with_type(type_name: str) -> set[tuple[str, str]]:
    return {
        (type_id, field_name)
        for type_id, definition in INVENTORY["types"].items()
        if definition["kind"] == "object" and not type_id.startswith("measureable_units.json#")
        for field_name, field in definition.get("fields", {}).items()
        if field["type"] == type_name
    }


def test_every_domain_percent_field_has_explicit_context_refinement() -> None:
    expected = _domain_fields_with_type("PercentType")
    actual = {
        (entry["source_type"], entry["source_field"])
        for entry in PRIMITIVES["percent_type"]["field_refinements"]
    }
    assert actual == expected


def test_bare_number_and_integer_fields_are_all_classified() -> None:
    expected_numbers = _domain_fields_with_type("number")
    expected_integers = _domain_fields_with_type("integer")
    actual_numbers = {
        (entry["source_type"], entry["source_field"]) for entry in PRIMITIVES["numeric_field_rules"]
    }
    actual_integers = {
        (entry["source_type"], entry["source_field"]) for entry in PRIMITIVES["integer_field_rules"]
    }
    assert actual_numbers == expected_numbers
    assert actual_integers == expected_integers


def test_beerjson_optional_fields_are_not_nullable_by_source_schema() -> None:
    for definition in INVENTORY["types"].values():
        if definition["kind"] != "object":
            continue
        for field in definition.get("fields", {}).values():
            assert "null" not in field["type"].split("|")


def test_version_and_local_datetime_policy_do_not_invent_semantics() -> None:
    assert (
        PRIMITIVES["version_type"]["compatibility_profile_requirement"]
        == "numeric_value_equals_1.0"
    )
    assert "MUST NOT" in PRIMITIVES["date_type"]["timezone_policy"]
    assert (
        PRIMITIVES["date_type"]["forms"]["local_date_time"]["native_semantics"]
        == "local_date_time_without_offset"
    )


def test_percentage_refinement_is_conservative() -> None:
    refinements = {
        (entry["source_type"], entry["source_field"]): entry
        for entry in PRIMITIVES["percent_type"]["field_refinements"]
    }
    assert (
        refinements[("recipe.json#RecipeType", "alcohol_by_volume")]["quantity_kind"]
        == "volume_fraction"
    )
    assert (
        refinements[("culture.json#CultureInformation", "alcohol_tolerance")]["quantity_kind"]
        == "volume_fraction"
    )
    assert (
        refinements[("fermentable.json#FermentableType", "protein")]["quantity_kind"] == "fraction"
    )
    assert refinements[("hop.json#HopVarietyBase", "alpha_acid")]["quantity_kind"] == "fraction"


def test_new_native_quantity_kinds_and_inch_are_registered() -> None:
    assert KINDS["count"]["canonical_unit"] == "one"
    assert KINDS["volume_per_mass"]["canonical_unit"] == "liter_per_kilogram"
    inch = UNITS["inch"]
    assert inch["dimension"] == "length"
    conversion = inch["conversion_to_dimension_reference"]
    assert Fraction(
        int(conversion["factor_numerator"]), int(conversion["factor_denominator"])
    ) == Fraction(127, 5000)


def test_previously_resolved_special_fields_are_marked_defined() -> None:
    status = {
        (row["source_type"], row["source_field"]): row["status"]
        for row in FIELD_MAPPING["field_mappings"]
    }
    for key in {
        ("culture.json#CultureAdditionType", "cell_count_billions"),
        ("equipment.json#EquipmentItemType", "boil_rate_per_hour"),
        ("equipment.json#EquipmentItemType", "drain_rate_per_minute"),
        ("hop.json#OilContentType", "total_oil_ml_per_100g"),
        ("packaging_graphic.json#PackagingGraphicType", "width"),
        ("packaging_graphic.json#PackagingGraphicType", "height"),
        ("water.json#WaterType", "pH"),
    }:
        assert status[key] == "special_mapping_defined"

    assert status[("recipe.json#RecipeType", "carbonation")] == "special_mapping_required"
    assert status[("recipe.json#RecipeType", "calories_per_pint")] == "special_mapping_required"


def test_representative_vectors_capture_non_guessing_policy() -> None:
    cases = {case["id"]: case for case in VECTORS["cases"]}
    assert cases["local_datetime_no_timezone_invented"]["expected"]["timezone"] is None
    assert (
        cases["unanchored_date_pattern_superstring_preserved"]["expected"]["native_date_semantics"]
        is None
    )
    assert (
        cases["impossible_calendar_date_not_repaired"]["expected"]["native_date_semantics"] is None
    )
    assert cases["bare_carbonation_has_no_invented_unit"]["expected"]["invented_unit"] is None
    assert cases["timing_step_preserves_one_based_ordinal"]["expected"]["value"] == 2
    assert (
        cases["beerjson_1_version_semantics"]["expected"]["beerjson_1_profile_compatible"] is True
    )
    assert (
        cases["other_numeric_version_outside_profile"]["expected"]["beerjson_1_profile_compatible"]
        is False
    )


def test_representative_numeric_conversions_are_exact_or_explicit() -> None:
    cases = {case["id"]: case for case in VECTORS["cases"]}
    assert cases["cell_count_billions_expanded"]["expected"]["canonical_value"] == 125_000_000_000
    assert cases["hop_oil_basis_expanded"]["expected"]["canonical_value"] == 0.015
    assert cases["graphic_inches_to_length"]["expected"]["canonical_value"] == 0.0889
    assert cases["abv_percent_to_volume_fraction"]["expected"]["canonical_value"] == 0.052
    assert (
        cases["beerjson_percent_not_clamped_by_compatibility_layer"]["expected"]["canonical_value"]
        == 1.05
    )


def test_profile_and_field_mapping_reference_primitive_semantics() -> None:
    profile = json.loads((COMPAT / "profile.v0.1.0.json").read_text())
    assert (
        profile["primitive_field_semantics_mapping"]
        == "mappings/primitive-field-semantics.v0.1.0.json"
    )
    assert profile["representative_fixture_set"] == "fixtures/primitive-field-vectors.v0.1.0.json"
    assert (
        FIELD_MAPPING["primitive_field_semantics_mapping"]
        == "primitive-field-semantics.v0.1.0.json"
    )
