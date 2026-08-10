from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
COMPAT = ROOT / "compatibility" / "beerjson-1.0"


def _load(relative: str) -> dict:
    return json.loads((COMPAT / relative).read_text(encoding="utf-8"))


def test_source_manifest_is_pinned_to_immutable_v1_0_2_tag() -> None:
    manifest = _load("source-manifest.v0.1.0.json")
    assert manifest["external_standard"]["document_version"] == "1.0"
    assert manifest["external_standard"]["repository_tag"] == "v1.0.2"
    assert manifest["tag_commit"] == "fbe84b007f22205094493cce232b61d770ab8088"
    assert len(manifest["schema_files"]) == 20
    assert len({item["name"] for item in manifest["schema_files"]}) == 20


def test_inventory_counts_match_contents() -> None:
    inventory = _load("inventory/beerjson-v1.0.2-inventory.json")
    types = inventory["types"]
    objects = [definition for definition in types.values() if definition["kind"] == "object"]
    enums = [definition for definition in types.values() if definition["kind"] == "enum"]
    scalars = [definition for definition in types.values() if definition["kind"] == "scalar"]

    assert inventory["counts"]["named_types"] == len(types)
    assert inventory["counts"]["object_types"] == len(objects)
    assert inventory["counts"]["enum_types"] == len(enums)
    assert inventory["counts"]["scalar_types"] == len(scalars)
    assert inventory["counts"]["declared_object_fields"] == sum(
        len(definition.get("fields", {})) for definition in objects
    )


def test_every_declared_object_field_has_exactly_one_mapping_row() -> None:
    inventory = _load("inventory/beerjson-v1.0.2-inventory.json")
    mapping = _load("mappings/field-mapping.v0.1.0.json")

    expected = {
        (type_id, field_name)
        for type_id, definition in inventory["types"].items()
        if definition["kind"] == "object"
        for field_name in definition.get("fields", {})
    }
    actual_rows = [(row["source_type"], row["source_field"]) for row in mapping["field_mappings"]]

    assert len(actual_rows) == len(set(actual_rows))
    assert set(actual_rows) == expected


def test_unit_mapping_covers_every_beerjson_unit_token() -> None:
    inventory = _load("inventory/beerjson-v1.0.2-inventory.json")
    mapping = _load("mappings/unit-tokens.v0.1.0.json")

    for unit_type, token_mappings in mapping["unit_types"].items():
        definition = inventory["types"][f"measureable_units.json#{unit_type}"]
        assert definition["kind"] == "enum"
        assert set(token_mappings) == set(definition["values"]), unit_type
        for token, entry in token_mappings.items():
            assert entry["status"], (unit_type, token)


def test_special_semantic_fields_remain_explicit() -> None:
    mapping = _load("mappings/field-mapping.v0.1.0.json")
    special = {
        (row["source_type"], row["source_field"])
        for row in mapping["field_mappings"]
        if row["status"] == "special_mapping_required"
    }
    assert ("equipment.json#EquipmentItemType", "boil_rate_per_hour") in special
    assert ("equipment.json#EquipmentItemType", "drain_rate_per_minute") in special
    assert ("culture.json#CultureAdditionType", "cell_count_billions") in special
    assert ("hop.json#OilContentType", "total_oil_ml_per_100g") in special
    assert ("recipe.json#RecipeType", "carbonation") in special
    assert ("water.json#WaterType", "pH") in special


def test_ppm_and_ppb_are_not_mapped_to_mass_per_volume() -> None:
    mapping = _load("mappings/unit-tokens.v0.1.0.json")
    concentration = mapping["unit_types"]["ConcentrationUnitType"]
    assert concentration["ppm"]["fermentationjson_unit"] == "part_per_million"
    assert concentration["ppb"]["fermentationjson_unit"] == "part_per_billion"
    assert "context_required" in concentration["ppm"]["status"]
    assert "context_required" in concentration["ppb"]["status"]


def test_profile_does_not_claim_completed_compatibility() -> None:
    profile = _load("profile.v0.1.0.json")
    assert profile["status"] == "pre-release_mapping_baseline"
    assert profile["directions"]["import"] == "required_target"
    assert "No FermentationJSON implementation may claim completed" in profile["claim_status"]


def test_special_mappings_separate_source_native_and_reverse_layers() -> None:
    mapping = _load("mappings/field-mapping.v0.1.0.json")
    required_layers = set(mapping["special_mapping_layers"])

    for row in mapping["field_mappings"]:
        if row["status"] != "special_mapping_required":
            continue
        assert set(row["mapping_layers"]) == required_layers
        assert all(row["mapping_layers"][layer] for layer in required_layers)


def test_beerjson_equipment_rates_map_to_native_volume_flow_rate() -> None:
    mapping = _load("mappings/field-mapping.v0.1.0.json")
    rows = {(row["source_type"], row["source_field"]): row for row in mapping["field_mappings"]}

    for field_name, time_basis in (
        ("boil_rate_per_hour", "hour"),
        ("drain_rate_per_minute", "minute"),
    ):
        row = rows[("equipment.json#EquipmentItemType", field_name)]
        layers = row["mapping_layers"]
        assert row["source_value_type"] == "VolumeType"
        assert row["target_concept"] == "volume_flow_rate"
        assert time_basis in layers["semantic_interpretation"]
        assert "volume_flow_rate" in layers["native_representation"]
        assert "plain volume" in layers["native_representation"]
