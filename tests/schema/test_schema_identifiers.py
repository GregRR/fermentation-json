from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urldefrag, urljoin, urlparse

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_ROOT = ROOT / "schemas"
CATALOG_PATH = ROOT / "schemas" / "catalog.v0.1.0.json"
VALID_ROOT = ROOT / "examples" / "valid"

EXPECTED_SET_VERSION = "0.1.0"
EXPECTED_PUBLIC_NAMESPACE = "https://gregrr.github.io/fermentation-json/schemas/"
EXPECTED_SET_NAMESPACE = f"{EXPECTED_PUBLIC_NAMESPACE}{EXPECTED_SET_VERSION}/"
EXPECTED_CORE_NAMESPACE = f"{EXPECTED_SET_NAMESPACE}core/"


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


CATALOG = _load_json(CATALOG_PATH)
CATALOG_BY_PATH = {entry["path"]: entry for entry in CATALOG["schemas"]}
CATALOG_BY_ID = {entry["id"]: entry for entry in CATALOG["schemas"]}


def _deny_retrieve(uri: str):
    raise AssertionError(f"unexpected external schema retrieval: {uri}")


def _canonical_registry() -> Registry:
    registry = Registry(retrieve=_deny_retrieve)
    for entry in CATALOG["schemas"]:
        schema = _load_json(ROOT / "schemas" / entry["path"])
        registry = registry.with_resource(
            entry["id"],
            Resource.from_contents(schema),
        )
    return registry


REGISTRY = _canonical_registry()
FORMAT_CHECKER = FormatChecker()


def _walk_refs(value):
    if isinstance(value, dict):
        for key, child in value.items():
            if key == "$ref":
                yield child
            else:
                yield from _walk_refs(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk_refs(child)


def test_schema_catalog_declares_expected_namespace() -> None:
    assert CATALOG["version"] == EXPECTED_SET_VERSION
    assert CATALOG["public_namespace"] == EXPECTED_PUBLIC_NAMESPACE
    assert CATALOG["schema_set_namespace"] == EXPECTED_SET_NAMESPACE
    assert CATALOG["core_namespace"] == EXPECTED_CORE_NAMESPACE


def test_every_catalog_schema_is_valid_draft_2020_12() -> None:
    for entry in CATALOG["schemas"]:
        Draft202012Validator.check_schema(_load_json(ROOT / "schemas" / entry["path"]))


def test_every_normative_schema_has_exactly_one_catalog_entry_and_canonical_id() -> None:
    schema_paths = sorted(SCHEMA_ROOT.rglob("*.schema.json"))
    relative_paths = {path.relative_to(SCHEMA_ROOT).as_posix() for path in schema_paths}
    catalog_paths = {entry["path"] for entry in CATALOG["schemas"]}

    assert catalog_paths == relative_paths

    ids = [entry["id"] for entry in CATALOG["schemas"]]
    assert len(ids) == len(set(ids))

    for path in schema_paths:
        relative_path = path.relative_to(SCHEMA_ROOT).as_posix()
        schema = _load_json(path)
        entry = CATALOG_BY_PATH[relative_path]
        expected_id = EXPECTED_SET_NAMESPACE + relative_path

        assert entry["id"] == expected_id
        assert schema["$id"] == expected_id
        assert urlparse(schema["$id"]).scheme == "https"


def test_cross_schema_refs_resolve_inside_the_same_schema_set() -> None:
    known_ids = set(CATALOG_BY_ID)

    for path in sorted(SCHEMA_ROOT.rglob("*.schema.json")):
        schema = _load_json(path)
        for ref in _walk_refs(schema):
            resolved, _fragment = urldefrag(urljoin(schema["$id"], ref))
            assert resolved in known_ids, (path.name, ref, resolved)
            assert resolved.startswith(EXPECTED_SET_NAMESPACE), (
                path.name,
                ref,
                resolved,
            )


def test_valid_examples_resolve_with_canonical_registry_without_retrieval() -> None:
    for case_path in sorted(VALID_ROOT.glob("*/*.json")):
        case = _load_json(case_path)
        schema_path = case.get("_schema_path")
        if schema_path is None:
            schema_filename = case.get("_schema")
            if schema_filename is None:
                continue
            schema_path = f"core/{schema_filename}"

        entry = CATALOG_BY_PATH[schema_path]
        schema = _load_json(ROOT / "schemas" / entry["path"])

        validator = Draft202012Validator(
            schema,
            registry=REGISTRY,
            format_checker=FORMAT_CHECKER,
        )
        errors = sorted(
            validator.iter_errors(case["instance"]),
            key=lambda error: list(error.absolute_path),
        )
        assert not errors, (
            case_path.name,
            "\n".join(error.message for error in errors),
        )
