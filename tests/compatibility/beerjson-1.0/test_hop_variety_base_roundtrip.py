from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[3]
COMPAT = ROOT / "compatibility/beerjson-1.0"
MAPPING = json.loads((COMPAT / "mappings/hop-variety-base.v0.1.0.json").read_text())
VECTORS = json.loads((COMPAT / "fixtures/hop-variety-base-roundtrip-v0.1.0.json").read_text())
INVENTORY = json.loads((COMPAT / "inventory/beerjson-v1.0.2-inventory.json").read_text())
CATALOG = json.loads((ROOT / "schemas/catalog.v0.1.0.json").read_text())


def _registry() -> Registry:
    registry = Registry()
    for entry in CATALOG["schemas"]:
        schema = json.loads((ROOT / "schemas" / entry["path"]).read_text())
        registry = registry.with_resource(entry["id"], Resource.from_contents(schema))
    return registry


REGISTRY = _registry()
HOP_SCHEMA = json.loads((ROOT / "schemas/ingredients/hop.schema.json").read_text())
VALIDATOR = Draft202012Validator(HOP_SCHEMA, registry=REGISTRY, format_checker=FormatChecker())
FIELD_RULES = {entry["source_field"]: entry for entry in MAPPING["field_mappings"]}
FORM_REVERSE = {native: source for source, native in FIELD_RULES["form"]["token_map"].items()}


def _required_source_fields() -> set[str]:
    definition = INVENTORY["types"]["hop.json#HopVarietyBase"]
    return {name for name, field in definition["fields"].items() if field["required"]}


def _reconstruct(native: dict, retained: dict) -> dict:
    source: dict = {}
    if "name" in native:
        source["name"] = native["name"]
    if "producer_name" in native:
        source["producer"] = native["producer_name"]
    if "product_identifier" in native:
        source["product_id"] = native["product_identifier"]
    if "origin_text" in native:
        source["origin"] = native["origin_text"]
    if "form" in native:
        source["form"] = FORM_REVERSE[native["form"]]
    for source_field, native_field in (("alpha_acid", "alpha_acid"), ("beta_acid", "beta_acid")):
        if native_field in native:
            reported = native[native_field]["reported"]
            source[source_field] = {
                "unit": reported["original_unit_text"],
                "value": reported["form"]["value"],
            }
    source.update(retained)
    return source


def test_mapping_covers_every_hop_variety_base_field_exactly_once() -> None:
    expected = set(INVENTORY["types"]["hop.json#HopVarietyBase"]["fields"])
    actual = [entry["source_field"] for entry in MAPPING["field_mappings"]]
    assert len(actual) == len(set(actual))
    assert set(actual) == expected


def test_source_vectors_include_all_beerjson_required_fields() -> None:
    required = _required_source_fields()
    for vector in VECTORS["vectors"]:
        assert required <= set(vector["source"]), vector["id"]


def test_native_hop_vectors_validate_without_weakening_native_schema() -> None:
    for vector in VECTORS["vectors"]:
        native = vector["expected"].get("native_object")
        if native is None:
            continue
        errors = list(VALIDATOR.iter_errors(native))
        assert not errors, f"{vector['id']}: " + "; ".join(error.message for error in errors)


def test_native_hop_roundtrip_reconstructs_beerjson_source() -> None:
    for vector in VECTORS["vectors"]:
        expected = vector["expected"]
        native = expected.get("native_object")
        if native is None:
            assert expected["retained_source_object"] == vector["source"]
            assert expected["roundtrip_source"] == vector["source"]
            continue
        reconstructed = _reconstruct(native, expected.get("retained_source_fields", {}))
        assert reconstructed == vector["source"], vector["id"]
        assert expected["roundtrip_source"] == vector["source"]


def test_beerjson_year_is_not_given_a_native_year_target() -> None:
    year = FIELD_RULES["year"]
    assert year["target_path"] is None
    assert year["mode"] == "source_preservation_only"
    vector = next(
        v for v in VECTORS["vectors"] if v["id"] == "free_form_year_is_retained_not_reinterpreted"
    )
    assert vector["expected"]["retained_source_fields"] == {"year": "2024 crop"}


def test_empty_beerjson_name_does_not_weaken_native_material_name_rule() -> None:
    vector = next(
        v
        for v in VECTORS["vectors"]
        if v["id"] == "empty_required_name_uses_source_preservation_only"
    )
    assert vector["expected"]["import_status"] == "source_preservation_only"
    assert vector["expected"]["native_object"] is None
