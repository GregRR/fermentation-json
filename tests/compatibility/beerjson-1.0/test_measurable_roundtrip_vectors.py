from __future__ import annotations

import copy
import json
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[3]
COMPAT = ROOT / "compatibility" / "beerjson-1.0"
SCHEMA_DIR = ROOT / "schemas" / "core"
VECTORS = json.loads(
    (COMPAT / "fixtures/measurable-roundtrip-vectors.v0.1.0.json").read_text(),
    parse_float=Decimal,
)
TYPE_MAPPING = json.loads((COMPAT / "mappings/measurable-types.v0.1.0.json").read_text())
UNIT_MAPPING = json.loads((COMPAT / "mappings/unit-tokens.v0.1.0.json").read_text())
ANALYTICAL_MAPPING = json.loads((COMPAT / "mappings/analytical-scales.v0.1.0.json").read_text())
INVENTORY = json.loads((COMPAT / "inventory/beerjson-v1.0.2-inventory.json").read_text())
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


def _schema_with_retrieval_id(path: Path) -> dict:
    schema = copy.deepcopy(json.loads(path.read_text(encoding="utf-8")))
    schema["$id"] = path.as_uri()
    return schema


def _registry() -> Registry:
    registry = Registry()
    for path in sorted(SCHEMA_DIR.glob("*.schema.json")):
        schema = _schema_with_retrieval_id(path)
        registry = registry.with_resource(path.as_uri(), Resource.from_contents(schema))
    return registry


REGISTRY = _registry()


def _quantity_errors(quantity: dict) -> list:
    schema_path = SCHEMA_DIR / "quantity.schema.json"
    validator = Draft202012Validator(
        _schema_with_retrieval_id(schema_path),
        registry=REGISTRY,
        format_checker=FormatChecker(),
    )
    return list(validator.iter_errors(quantity))


def _fraction(conversion: dict, prefix: str = "factor") -> Fraction:
    return Fraction(
        int(conversion[f"{prefix}_numerator"]),
        int(conversion[f"{prefix}_denominator"]),
    )


def _to_reference(value: Decimal, unit_id: str) -> Decimal:
    conversion = UNITS[unit_id]["conversion_to_dimension_reference"]
    factor = _fraction(conversion)
    result = value * Decimal(factor.numerator) / Decimal(factor.denominator)
    if conversion["type"] == "affine":
        offset = _fraction(conversion, "offset")
        result += Decimal(offset.numerator) / Decimal(offset.denominator)
    return result


def _tokens(source_type: str, source: dict) -> list[str]:
    if source_type.endswith("RangeType"):
        return [source["minimum"]["unit"], source["maximum"]["unit"]]
    return [source["unit"]]


def _base_type(source_type: str) -> str:
    if source_type.endswith("RangeType"):
        return TYPE_MAPPING["range_type_mappings"][source_type]["base_type"]
    return source_type


def _source_unit_type(source_type: str) -> str:
    return TYPE_MAPPING["quantity_type_mappings"][_base_type(source_type)]["source_unit_type"]


def _reconstruct_source(source_type: str, quantity: dict) -> dict:
    reported = quantity["reported"]
    form = reported["form"]
    if source_type.endswith("RangeType"):
        if "endpoint_original_unit_text" in reported:
            tokens = reported["endpoint_original_unit_text"]
        else:
            tokens = {
                "minimum": reported["original_unit_text"],
                "maximum": reported["original_unit_text"],
            }
        return {
            "minimum": {"unit": tokens["minimum"], "value": form["minimum"]["value"]},
            "maximum": {"unit": tokens["maximum"], "value": form["maximum"]["value"]},
        }
    return {"unit": reported["original_unit_text"], "value": form["value"]}


def test_roundtrip_vector_sources_match_inventory_shapes() -> None:
    ids: set[str] = set()
    for vector in VECTORS["vectors"]:
        assert vector["id"] not in ids
        ids.add(vector["id"])

        definition = INVENTORY["types"][f"measureable_units.json#{vector['source_type']}"]
        assert definition["kind"] == "object"
        assert set(vector["source"]) == set(definition["fields"])

        if vector["source_type"].endswith("RangeType"):
            base_definition = INVENTORY["types"][
                f"measureable_units.json#{_base_type(vector['source_type'])}"
            ]
            for endpoint in ("minimum", "maximum"):
                assert set(vector["source"][endpoint]) == set(base_definition["fields"])


def test_roundtrip_vectors_use_known_beerjson_measurable_types_and_tokens() -> None:
    quantity_types = TYPE_MAPPING["quantity_type_mappings"]
    range_types = TYPE_MAPPING["range_type_mappings"]

    for vector in VECTORS["vectors"]:
        source_type = vector["source_type"]
        assert source_type in quantity_types or source_type in range_types
        unit_type = _source_unit_type(source_type)
        registered_tokens = UNIT_MAPPING["unit_types"][unit_type]
        assert all(token in registered_tokens for token in _tokens(source_type, vector["source"]))


def test_native_quantity_vectors_are_structurally_and_semantically_consistent() -> None:
    for vector in VECTORS["vectors"]:
        expected = vector["expected"]
        if expected["import_status"] != "native_quantity":
            continue

        quantity = expected["native_quantity"]
        errors = _quantity_errors(quantity)
        assert not errors, f"{vector['id']}: " + "; ".join(error.message for error in errors)

        kind = KINDS[quantity["quantity_kind"]]
        assert quantity["canonical"]["unit"] == kind["canonical_unit"]
        if canonical_scale := kind.get("canonical_scale"):
            assert quantity["canonical"]["scale"] == canonical_scale
            assert quantity["reported"]["scale"] == canonical_scale


def test_native_quantity_canonical_values_match_registered_unit_conversions() -> None:
    tolerance = Decimal("1e-12")
    for vector in VECTORS["vectors"]:
        expected = vector["expected"]
        if expected["import_status"] != "native_quantity":
            continue

        quantity = expected["native_quantity"]
        canonical = quantity["canonical"]
        reported = quantity["reported"]
        canonical_form = canonical["form"]
        reported_form = reported["form"]

        if canonical_form["type"] == "exact":
            source_reference = _to_reference(Decimal(reported_form["value"]), reported["unit"])
            canonical_reference = _to_reference(Decimal(canonical_form["value"]), canonical["unit"])
            assert abs(source_reference - canonical_reference) <= tolerance, vector["id"]
            continue

        for endpoint in ("minimum", "maximum"):
            reported_unit = reported.get("unit") or reported["endpoint_units"][endpoint]
            source_reference = _to_reference(
                Decimal(reported_form[endpoint]["value"]), reported_unit
            )
            canonical_reference = _to_reference(
                Decimal(canonical_form[endpoint]["value"]), canonical["unit"]
            )
            assert abs(source_reference - canonical_reference) <= tolerance, (
                vector["id"],
                endpoint,
            )


def test_native_quantity_roundtrip_reconstructs_original_beerjson_object() -> None:
    for vector in VECTORS["vectors"]:
        expected = vector["expected"]
        if expected["import_status"] != "native_quantity":
            continue
        assert expected["round_trip"] == "reconstruct_from_reported"
        reconstructed = _reconstruct_source(vector["source_type"], expected["native_quantity"])
        assert reconstructed == vector["source"], vector["id"]


def test_carbonation_mass_concentration_retains_carbon_dioxide_subject() -> None:
    vector = next(
        vector
        for vector in VECTORS["vectors"]
        if vector["id"] == "carbonation_grams_per_liter_exact"
    )
    source_mapping = ANALYTICAL_MAPPING["type_dispatch"]["CarbonationType"]["g/l"]

    assert vector["expected"]["semantic_subject"] == "carbon_dioxide"
    assert vector["expected"]["semantic_subject"] == source_mapping["semantic_subject"]
    assert vector["expected"]["native_quantity"]["quantity_kind"] == "mass_concentration"


def test_source_preservation_only_vectors_roundtrip_without_inventing_quantity() -> None:
    preservation_vectors = [
        vector
        for vector in VECTORS["vectors"]
        if vector["expected"]["import_status"] == "source_preservation_only"
    ]
    assert preservation_vectors

    for vector in preservation_vectors:
        expected = vector["expected"]
        assert expected["native_quantity"] is None
        assert expected["preserved_source"] == vector["source"]
        assert expected["round_trip"] == "use_preserved_source"
        assert expected["reason"]


def test_unresolved_source_tokens_are_preserved_instead_of_guessed() -> None:
    by_id = {vector["id"]: vector for vector in VECTORS["vectors"]}
    for vector_id in (
        "volume_undefined_imperial_barrel_token",
        "specific_heat_undefined_calorie_token",
    ):
        vector = by_id[vector_id]
        unit_type = _source_unit_type(vector["source_type"])
        token = vector["source"]["unit"]
        mapping = UNIT_MAPPING["unit_types"][unit_type][token]
        assert mapping["fermentationjson_unit"] is None
        assert "pending" in mapping["status"]
        assert vector["expected"]["import_status"] == "source_preservation_only"


def test_mixed_analytical_scale_range_requires_explicit_normalization() -> None:
    vector = next(
        vector
        for vector in VECTORS["vectors"]
        if vector["id"] == "color_mixed_analytical_scale_range"
    )
    dispatch = ANALYTICAL_MAPPING["type_dispatch"]["ColorType"]
    minimum_scale = dispatch[vector["source"]["minimum"]["unit"]]["scale"]
    maximum_scale = dispatch[vector["source"]["maximum"]["unit"]]["scale"]

    assert minimum_scale != maximum_scale
    assert vector["expected"]["import_status"] == "source_preservation_only"
    assert vector["expected"]["native_quantity"] is None


def test_profile_advertises_measurable_roundtrip_fixture_set() -> None:
    profile = json.loads((COMPAT / "profile.v0.1.0.json").read_text())
    assert (
        profile["measurable_roundtrip_fixture_set"]
        == "fixtures/measurable-roundtrip-vectors.v0.1.0.json"
    )
    assert profile["status"] == "pre-release_behavioral_fixture_baseline"
