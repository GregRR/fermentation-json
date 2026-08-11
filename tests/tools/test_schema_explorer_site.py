from __future__ import annotations

import importlib.util
import json
from pathlib import Path

from jsonschema import Draft202012Validator
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

ROOT = Path(__file__).resolve().parents[2]
BUILD_SCRIPT = ROOT / "tools" / "schema-explorer" / "build_site.py"
CATALOG_PATH = ROOT / "schemas" / "catalog.v0.1.0.json"

spec = importlib.util.spec_from_file_location("schema_explorer_build_site", BUILD_SCRIPT)
assert spec is not None and spec.loader is not None
build_site_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build_site_module)


def _fake_studio(tmp_path: Path) -> tuple[Path, Path]:
    studio = tmp_path / "studio-dist"
    (studio / "assets").mkdir(parents=True)
    (studio / "assets" / "index-test.js").write_text("export {};\n", encoding="utf-8")
    (studio / "index.html").write_text(
        (
            '<!doctype html><div id="root"></div>'
            '<script type="module" crossorigin '
            'src="/fermentation-json/studio/assets/index-test.js"></script>'
        ),
        encoding="utf-8",
    )
    license_path = tmp_path / "LICENSE"
    license_path.write_text("MIT test license\n", encoding="utf-8")
    return studio, license_path


def test_pages_build_publishes_cataloged_schemas_at_canonical_paths(tmp_path: Path) -> None:
    studio, license_path = _fake_studio(tmp_path)
    output = tmp_path / "site"

    build_site_module.build_site(studio, license_path, output)

    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    version = catalog["version"]
    for entry in catalog["schemas"]:
        published = output / "schemas" / version / entry["path"]
        assert published.read_bytes() == (ROOT / "schemas" / entry["path"]).read_bytes()


def test_pages_build_creates_compound_schemas_for_studio(tmp_path: Path) -> None:
    studio, license_path = _fake_studio(tmp_path)
    output = tmp_path / "site"

    build_site_module.build_site(studio, license_path, output)

    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    version = catalog["version"]
    selected_path = "core/quantity.schema.json"
    selected = next(entry for entry in catalog["schemas"] if entry["path"] == selected_path)
    source = json.loads((ROOT / "schemas" / selected_path).read_text(encoding="utf-8"))
    bundle = json.loads(
        (output / "explorer-schemas" / version / selected_path).read_text(encoding="utf-8")
    )

    assert bundle["$id"] == source["$id"] == selected["id"]
    assert bundle["properties"] == source["properties"]
    assert bundle["$defs"]["reporting_basis"] == source["$defs"]["reporting_basis"]

    embedded_ids = {
        key for key in bundle["$defs"] if key.startswith(catalog["schema_set_namespace"])
    }
    namespace = catalog["schema_set_namespace"]
    assert f"{namespace}core/result-form.schema.json" in embedded_ids
    assert f"{namespace}core/identity.schema.json" in embedded_ids
    assert f"{namespace}ingredients/hop.schema.json" not in embedded_ids
    for resource_id in embedded_ids:
        assert bundle["$defs"][resource_id]["$id"] == resource_id


def test_document_bundle_resolves_cross_schema_anchor_locally(tmp_path: Path) -> None:
    studio, license_path = _fake_studio(tmp_path)
    output = tmp_path / "site"

    build_site_module.build_site(studio, license_path, output)

    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    version = catalog["version"]
    bundle_path = output / "explorer-schemas" / version / "core/document.schema.json"
    bundle = json.loads(bundle_path.read_text(encoding="utf-8"))

    resource = Resource.from_contents(bundle, default_specification=DRAFT202012)
    registry = Registry().with_resource(bundle["$id"], resource).crawl()
    semantic_version_uri = (
        "https://gregrr.github.io/fermentation-json/schemas/0.1.0/"
        "core/identity.schema.json#semanticVersion"
    )

    resolved = registry.resolver().lookup(semantic_version_uri)
    assert resolved.contents["$anchor"] == "semanticVersion"

    Draft202012Validator(bundle, registry=registry).validate(
        {
            "specification_version": "0.1.0",
            "document_type": "test",
            "schema_id": "https://example.com/schema",
            "document_id": "urn:uuid:123",
            "content": None,
        }
    )


def test_pages_launcher_and_studio_bootstrap_are_catalog_driven(tmp_path: Path) -> None:
    studio, license_path = _fake_studio(tmp_path)
    output = tmp_path / "site"

    build_site_module.build_site(studio, license_path, output)

    launcher = (output / "index.html").read_text(encoding="utf-8")
    studio_index = (output / "studio" / "index.html").read_text(encoding="utf-8")

    assert "FermentationJSON Schema Explorer" in launcher
    assert "pre-release schema set 0.1.0" in launcher
    assert "core/document.schema.json" in launcher
    assert "ingredients/hop.schema.json" in launcher
    assert "ioflux.schema.editor.content" in studio_index
    assert "../explorer-schemas/0.1.0/${schemaPath}" in studio_index
    assert 'await import("/fermentation-json/studio/assets/index-test.js")' in studio_index
    assert '<script type="module" crossorigin src=' not in studio_index
    assert (output / ".nojekyll").is_file()
    assert (output / "third-party" / "json-schema-studio-MIT.txt").read_text(
        encoding="utf-8"
    ) == "MIT test license\n"
