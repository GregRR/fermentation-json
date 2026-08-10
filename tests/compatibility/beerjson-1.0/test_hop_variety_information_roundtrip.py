from __future__ import annotations

import json
from decimal import Decimal
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[3]
COMPAT = ROOT / "compatibility/beerjson-1.0"
MAPPING = json.loads((COMPAT / "mappings/hop-variety-information.v0.1.0.json").read_text())
BASE_MAPPING = json.loads((COMPAT / "mappings/hop-variety-base.v0.1.0.json").read_text())
VECTORS = json.loads(
    (COMPAT / "fixtures/hop-variety-information-roundtrip-v0.1.0.json").read_text()
)
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
PROFILE_SCHEMA = {"$ref": f"{HOP_SCHEMA['$id']}#hopVarietyProfile"}
VALIDATOR = Draft202012Validator(PROFILE_SCHEMA, registry=REGISTRY, format_checker=FormatChecker())
BASE_RULES = {entry["source_field"]: entry for entry in BASE_MAPPING["field_mappings"]}
FORM_REVERSE = {native: source for source, native in BASE_RULES["form"]["token_map"].items()}
VARIETY_RULES = {entry["source_field"]: entry for entry in MAPPING["field_mappings"]}
ROLE_REVERSE = {
    tuple(sorted(native)): source for source, native in VARIETY_RULES["type"]["token_map"].items()
}
OIL_RULES = {entry["source_field"]: entry for entry in MAPPING["oil_content_field_mappings"]}
COMPONENT_REVERSE = {
    entry["component"]: entry["source_field"]
    for entry in MAPPING["oil_content_field_mappings"]
    if entry["mode"] == "percent_of_total_oil_component"
}


def _source_percent(quantity: dict) -> dict:
    reported = quantity["reported"]
    return {"unit": reported["original_unit_text"], "value": reported["form"]["value"]}


def _reconstruct_base(native: dict) -> dict:
    source: dict = {"name": native["name"]}
    if "producer_name" in native:
        source["producer"] = native["producer_name"]
    if "product_identifier" in native:
        source["product_id"] = native["product_identifier"]
    if "origin_text" in native:
        source["origin"] = native["origin_text"]
    if "form" in native:
        source["form"] = FORM_REVERSE[native["form"]]
    for source_field in ("alpha_acid", "beta_acid"):
        if source_field in native:
            source[source_field] = _source_percent(native[source_field])
    return source


def _reconstruct(native: dict, retained: dict) -> dict:
    source = _reconstruct_base(native)
    if "variety_roles" in native:
        source["type"] = ROLE_REVERSE[tuple(sorted(native["variety_roles"]))]
    if "notes" in native:
        source["notes"] = native["notes"]
    if "alpha_acid_loss_after_six_months" in native:
        source["percent_lost"] = _source_percent(native["alpha_acid_loss_after_six_months"])
    if "substitution_notes" in native:
        source["substitutes"] = native["substitution_notes"]
    if "oil_profile" in native:
        oil: dict = {}
        profile = native["oil_profile"]
        if "total_oil" in profile:
            oil["total_oil_ml_per_100g"] = profile["total_oil"]["reported"]["form"]["value"]
        for component in profile.get("components", []):
            oil[COMPONENT_REVERSE[component["component"]]] = _source_percent(
                component["fraction_of_total_oil"]
            )
        oil.update(retained.get("oil_content", {}))
        source["oil_content"] = oil
    source.update({key: value for key, value in retained.items() if key != "oil_content"})
    return source


def test_mapping_covers_variety_information_fields_exactly_once() -> None:
    expected = set(INVENTORY["types"]["hop.json#VarietyInformation"]["fields"])
    actual = [entry["source_field"] for entry in MAPPING["field_mappings"]]
    assert len(actual) == len(set(actual))
    assert set(actual) == expected


def test_mapping_covers_oil_content_fields_exactly_once() -> None:
    expected = set(INVENTORY["types"]["hop.json#OilContentType"]["fields"])
    actual = [entry["source_field"] for entry in MAPPING["oil_content_field_mappings"]]
    assert len(actual) == len(set(actual))
    assert set(actual) == expected


def test_native_variety_vectors_validate() -> None:
    for vector in VECTORS["vectors"]:
        native = vector["expected"].get("native_object")
        if native is None:
            continue
        errors = list(VALIDATOR.iter_errors(native))
        assert not errors, f"{vector['id']}: " + "; ".join(error.message for error in errors)


def test_variety_roundtrip_reconstructs_beerjson_source() -> None:
    for vector in VECTORS["vectors"]:
        expected = vector["expected"]
        reconstructed = _reconstruct(expected["native_object"], expected["retained_source_fields"])
        assert reconstructed == vector["source"], vector["id"]
        assert expected["roundtrip_source"] == vector["source"]


def test_total_oil_conversion_is_exact_and_field_basis_is_not_lost() -> None:
    vector = next(
        item
        for item in VECTORS["vectors"]
        if item["id"] == "variety_profile_decomposes_oil_and_preserves_ambiguous_fields"
    )
    total_oil = vector["expected"]["native_object"]["oil_profile"]["total_oil"]
    assert Decimal(str(total_oil["canonical"]["form"]["value"])) == Decimal("0.012")
    assert total_oil["canonical"]["unit"] == "liter_per_kilogram"
    assert total_oil["reported"]["unit"] == "milliliter_per_100_gram"
    assert Decimal(str(total_oil["reported"]["form"]["value"])) == Decimal("1.2")


def test_ambiguous_oil_fields_remain_source_only_while_inventory_is_contextual() -> None:
    for field in ("cohumulone", "pinene", "polyphenols", "xanthohumol"):
        assert OIL_RULES[field]["mode"] == "source_preservation_only"
        assert OIL_RULES[field]["target_path"] is None

    inventory = VARIETY_RULES["inventory"]
    assert inventory["mode"] == "contextual_object_mapping"
    assert inventory["mapping"] == "hop-inventory.v0.1.0.json"
    assert "separate inventoryPosition" in inventory["target_path"]


def test_oil_component_mapping_does_not_include_ambiguous_beerjson_fields() -> None:
    mapped = {
        entry["source_field"]
        for entry in MAPPING["oil_content_field_mappings"]
        if entry["mode"] == "percent_of_total_oil_component"
    }
    assert {"cohumulone", "pinene", "polyphenols", "xanthohumol"}.isdisjoint(mapped)
    assert mapped == {
        "humulene",
        "caryophyllene",
        "myrcene",
        "farnesene",
        "geraniol",
        "b_pinene",
        "linalool",
        "limonene",
        "nerol",
    }
