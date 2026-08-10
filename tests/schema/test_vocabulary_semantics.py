from __future__ import annotations

import json
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from urllib.parse import urlparse

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource


ROOT = Path(__file__).resolve().parents[2]
SCHEMA_DIR = ROOT / "schemas" / "core"
UNIT_FILE = ROOT / "vocabularies" / "units" / "units.v0.1.0.json"
KIND_FILE = ROOT / "vocabularies" / "quantity-kinds" / "quantity-kinds.v0.1.0.json"
BASIS_FILE = ROOT / "vocabularies" / "reporting-bases" / "reporting-bases.v0.1.0.json"
VALID_DIR = ROOT / "examples" / "valid" / "semantic"
INVALID_DIR = ROOT / "examples" / "invalid" / "semantic"


def _load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"), parse_float=Decimal)


def _by_id(entries):
    return {entry["id"]: entry for entry in entries}


UNITS_DOC = _load(UNIT_FILE)
KINDS_DOC = _load(KIND_FILE)
BASES_DOC = _load(BASIS_FILE)
UNITS = _by_id(UNITS_DOC["entries"])
KINDS = _by_id(KINDS_DOC["entries"])
BASES = _by_id(BASES_DOC["entries"])


def _is_absolute_uri(value: str) -> bool:
    return bool(urlparse(value).scheme)


def _fraction(conv: dict, prefix: str = "factor") -> Fraction:
    return Fraction(int(conv[f"{prefix}_numerator"]), int(conv[f"{prefix}_denominator"]))


def _to_reference(value: Decimal, unit: dict) -> Decimal:
    conv = unit["conversion_to_dimension_reference"]
    f = _fraction(conv)
    factor = Decimal(f.numerator) / Decimal(f.denominator)
    if conv["type"] == "linear":
        return value * factor
    off = _fraction(conv, "offset")
    offset = Decimal(off.numerator) / Decimal(off.denominator)
    return value * factor + offset


def _registry():
    registry = Registry()
    for path in sorted(SCHEMA_DIR.glob("*.schema.json")):
        schema = json.loads(path.read_text(encoding="utf-8"))
        schema["$id"] = path.as_uri()
        registry = registry.with_resource(path.as_uri(), Resource.from_contents(schema))
    return registry


REGISTRY = _registry()


def _structurally_valid(case: dict) -> None:
    schema_path = SCHEMA_DIR / case["_schema"]
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    schema["$id"] = schema_path.as_uri()
    validator = Draft202012Validator(
        schema,
        registry=REGISTRY,
        format_checker=FormatChecker(),
    )
    errors = list(validator.iter_errors(case["instance"]))
    assert not errors, "\n".join(error.message for error in errors)


def semantic_errors(quantity: dict) -> list[str]:
    errors: list[str] = []
    kind_id = quantity["quantity_kind"]

    if _is_absolute_uri(kind_id):
        return errors

    kind = KINDS.get(kind_id)
    if kind is None:
        return ["unknown_core_quantity_kind"]

    canonical = quantity["canonical"]
    if canonical["unit"] != kind["canonical_unit"]:
        errors.append("wrong_canonical_unit")

    canonical_unit = UNITS.get(canonical["unit"])
    if canonical_unit is None:
        errors.append("unknown_core_unit")
    elif canonical_unit["dimension"] != kind["dimension"]:
        errors.append("canonical_unit_dimension_mismatch")

    reported = quantity.get("reported")
    if reported:
        unit_id = reported["unit"]
        if not _is_absolute_uri(unit_id):
            unit = UNITS.get(unit_id)
            if unit is None:
                errors.append("unknown_core_unit")
            elif unit["dimension"] != kind["dimension"]:
                errors.append("reported_unit_dimension_mismatch")

    for representation in (canonical, reported):
        if not representation:
            continue
        basis = representation.get("basis")
        if basis:
            basis_id = basis["kind"]
            if not _is_absolute_uri(basis_id):
                entry = BASES.get(basis_id)
                if entry is None:
                    errors.append("unknown_core_reporting_basis")
                elif entry.get("requires_substance") and not basis.get("substance"):
                    errors.append("reporting_basis_requires_substance")

    if reported and not errors:
        c_form = canonical["form"]
        r_form = reported["form"]
        if c_form["type"] == "exact" and r_form["type"] == "exact":
            c_unit = UNITS.get(canonical["unit"])
            r_unit = UNITS.get(reported["unit"])
            if c_unit and r_unit and c_unit["dimension"] == r_unit["dimension"]:
                expected = _to_reference(Decimal(r_form["value"]), r_unit)
                actual = _to_reference(Decimal(c_form["value"]), c_unit)
                if abs(expected - actual) > Decimal("1e-12"):
                    errors.append("canonical_value_conversion_mismatch")

    return errors


def test_vocabulary_ids_are_unique_and_well_formed() -> None:
    for document in (UNITS_DOC, KINDS_DOC, BASES_DOC):
        ids = [entry["id"] for entry in document["entries"]]
        assert len(ids) == len(set(ids))
        for identifier in ids:
            assert identifier == identifier.lower()
            assert identifier[0].isalpha()
            assert all(c.islower() or c.isdigit() or c == "_" for c in identifier)


def test_dimension_reference_units_exist() -> None:
    for dimension, metadata in UNITS_DOC["dimensions"].items():
        unit_id = metadata["reference_unit"]
        assert unit_id in UNITS
        assert UNITS[unit_id]["dimension"] == dimension


def test_every_core_quantity_kind_has_valid_canonical_unit() -> None:
    for kind in KINDS.values():
        unit = UNITS[kind["canonical_unit"]]
        assert unit["dimension"] == kind["dimension"]


def test_us_beer_barrel_definition_is_31_us_gallons() -> None:
    bbl = _fraction(UNITS["us_beer_barrel"]["conversion_to_dimension_reference"])
    gallon = _fraction(UNITS["us_liquid_gallon"]["conversion_to_dimension_reference"])
    assert bbl == 31 * gallon


def test_ambiguous_customary_names_are_not_core_units() -> None:
    assert "gallon" not in UNITS
    assert "fluid_ounce" not in UNITS
    assert "barrel" not in UNITS


def test_ppm_and_ppb_are_fraction_units() -> None:
    assert UNITS["part_per_million"]["dimension"] == "fraction"
    assert UNITS["part_per_billion"]["dimension"] == "fraction"


def test_valid_semantic_examples() -> None:
    for path in sorted(VALID_DIR.glob("*.json")):
        case = _load(path)
        _structurally_valid(case)
        assert semantic_errors(case["instance"]) == [], path.name


def test_invalid_semantic_examples() -> None:
    for path in sorted(INVALID_DIR.glob("*.json")):
        case = _load(path)
        _structurally_valid(case)
        errors = semantic_errors(case["instance"])
        assert case["_semantic_error"] in errors, (path.name, errors)
