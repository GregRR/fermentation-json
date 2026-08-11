from __future__ import annotations

import argparse
import html
import json
import re
import shutil
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[2]
CATALOG_PATH = ROOT / "schemas" / "catalog.v0.1.0.json"
DEFAULT_SCHEMA_PATH = "core/document.schema.json"
STUDIO_SESSION_SCHEMA_KEY = "ioflux.schema.editor.content"
STUDIO_SESSION_FORMAT_KEY = "ioflux.schema.editor.format"
STUDIO_VERSION = "0.9.1"
STUDIO_SOURCE_URL = "https://github.com/ioflux-org/studio-json-schema"
PROJECT_SOURCE_URL = "https://github.com/GregRR/fermentation-json"


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _catalog() -> dict:
    catalog = _load_json(CATALOG_PATH)
    if catalog.get("status") != "pre-release":
        raise ValueError("schema explorer build currently expects a pre-release schema catalog")
    return catalog


def _validate_catalog(catalog: dict) -> tuple[str, list[dict]]:
    version = catalog["version"]
    namespace = catalog["schema_set_namespace"]
    parsed_namespace = urlparse(namespace)
    if parsed_namespace.scheme != "https" or not namespace.endswith(f"/{version}/"):
        raise ValueError(f"unexpected schema-set namespace: {namespace}")

    schemas = catalog["schemas"]
    if not schemas:
        raise ValueError("schema catalog is empty")

    seen_paths: set[str] = set()
    for entry in schemas:
        relative_path = entry["path"]
        if relative_path.startswith("/") or ".." in Path(relative_path).parts:
            raise ValueError(f"unsafe schema path in catalog: {relative_path}")
        if relative_path in seen_paths:
            raise ValueError(f"duplicate schema path in catalog: {relative_path}")
        seen_paths.add(relative_path)

        source = ROOT / "schemas" / relative_path
        if not source.is_file():
            raise FileNotFoundError(source)

        schema = _load_json(source)
        expected_id = namespace + relative_path
        if entry["id"] != expected_id or schema.get("$id") != expected_id:
            raise ValueError(f"catalog/schema $id mismatch for {relative_path}")

    if DEFAULT_SCHEMA_PATH not in seen_paths:
        raise ValueError(f"default explorer schema is not cataloged: {DEFAULT_SCHEMA_PATH}")

    return version, schemas


def _copy_published_schemas(output: Path, version: str, schemas: list[dict]) -> None:
    version_root = output / "schemas" / version
    for entry in schemas:
        source = ROOT / "schemas" / entry["path"]
        destination = version_root / entry["path"]
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)

    shutil.copy2(CATALOG_PATH, output / "schemas" / CATALOG_PATH.name)


def _schema_options(schemas: list[dict]) -> str:
    options: list[str] = []
    for entry in schemas:
        path = entry["path"]
        label = f"{entry['name']} — {path}"
        selected = " selected" if path == DEFAULT_SCHEMA_PATH else ""
        options.append(
            f'<option value="{html.escape(path, quote=True)}"{selected}>'
            f"{html.escape(label)}</option>"
        )
    return "\n".join(options)


def _write_launcher(output: Path, version: str, schemas: list[dict]) -> None:
    allowed_paths = json.dumps([entry["path"] for entry in schemas], separators=(",", ":"))
    page = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Interactive explorer for the current pre-release FermentationJSON JSON Schema set.">
  <title>FermentationJSON Schema Explorer</title>
  <style>
    :root {{ color-scheme: light dark; font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; min-height: 100vh; background: Canvas; color: CanvasText; }}
    .page {{ min-height: 100vh; display: flex; flex-direction: column; }}
    header {{ display: flex; gap: 1rem; align-items: center; flex-wrap: wrap; padding: .75rem 1rem; border-bottom: 1px solid color-mix(in srgb, CanvasText 18%, transparent); }}
    .identity {{ display: flex; gap: .6rem; align-items: baseline; min-width: max-content; }}
    .identity strong {{ font-size: 1rem; }}
    .badge {{ font-size: .75rem; padding: .18rem .45rem; border: 1px solid currentColor; border-radius: 999px; opacity: .75; }}
    .controls {{ display: flex; gap: .65rem; align-items: center; flex: 1; min-width: min(100%, 24rem); }}
    label {{ font-size: .85rem; white-space: nowrap; }}
    select {{ flex: 1; min-width: 12rem; padding: .45rem .55rem; font: inherit; }}
    nav {{ display: flex; gap: .8rem; align-items: center; font-size: .85rem; }}
    a {{ color: LinkText; }}
    main {{ flex: 1; min-height: 34rem; position: relative; }}
    iframe {{ position: absolute; inset: 0; width: 100%; height: 100%; border: 0; background: Canvas; }}
    .status {{ padding: .45rem 1rem; font-size: .78rem; opacity: .72; border-top: 1px solid color-mix(in srgb, CanvasText 18%, transparent); }}
    @media (max-width: 720px) {{ .controls {{ order: 3; width: 100%; }} main {{ min-height: 42rem; }} }}
  </style>
</head>
<body>
  <div class="page">
    <header>
      <div class="identity">
        <strong>FermentationJSON Schema Explorer</strong>
        <span class="badge">pre-release schema set {html.escape(version)}</span>
      </div>
      <div class="controls">
        <label for="schema-select">Schema</label>
        <select id="schema-select">{_schema_options(schemas)}</select>
      </div>
      <nav>
        <a id="raw-schema-link" href="">Raw schema</a>
        <a href="{PROJECT_SOURCE_URL}">Repository</a>
      </nav>
    </header>
    <main><iframe id="studio-frame" title="Interactive JSON Schema visualization"></iframe></main>
    <div class="status">Visualization powered by <a href="{STUDIO_SOURCE_URL}">JSON Schema Studio {STUDIO_VERSION}</a> (MIT; <a href="./third-party/json-schema-studio-MIT.txt">license</a>). FermentationJSON schemas remain the authoritative source.</div>
  </div>
  <script>
    const schemaVersion = {json.dumps(version)};
    const defaultSchema = {json.dumps(DEFAULT_SCHEMA_PATH)};
    const allowedSchemas = new Set({allowed_paths});
    const select = document.getElementById("schema-select");
    const frame = document.getElementById("studio-frame");
    const rawLink = document.getElementById("raw-schema-link");

    function selectedFromLocation() {{
      const requested = new URLSearchParams(window.location.search).get("schema");
      return requested && allowedSchemas.has(requested) ? requested : defaultSchema;
    }}

    function showSchema(schemaPath, updateHistory) {{
      select.value = schemaPath;
      rawLink.href = `./schemas/${{schemaVersion}}/${{schemaPath}}`;
      frame.src = `./studio/?schema=${{encodeURIComponent(schemaPath)}}`;
      if (updateHistory) {{
        const url = new URL(window.location.href);
        url.searchParams.set("schema", schemaPath);
        window.history.replaceState(null, "", url);
      }}
    }}

    select.addEventListener("change", () => showSchema(select.value, true));
    showSchema(selectedFromLocation(), false);
  </script>
</body>
</html>
"""
    (output / "index.html").write_text(page, encoding="utf-8")


def _inject_studio_bootstrap(studio_index: Path, version: str, schemas: list[dict]) -> None:
    source = studio_index.read_text(encoding="utf-8")
    pattern = re.compile(r'<script\s+type="module"[^>]*\ssrc="([^"]+)"[^>]*></script>')
    match = pattern.search(source)
    if not match:
        raise ValueError("could not find Vite module entry script in JSON Schema Studio build")

    app_module = match.group(1)
    allowed_paths = json.dumps([entry["path"] for entry in schemas], separators=(",", ":"))
    bootstrap = f"""<script type="module">
const allowedSchemas = new Set({allowed_paths});
const defaultSchema = {json.dumps(DEFAULT_SCHEMA_PATH)};
const requested = new URLSearchParams(window.location.search).get("schema");
const schemaPath = requested && allowedSchemas.has(requested) ? requested : defaultSchema;
const schemaUrl = new URL(`../schemas/{version}/${{schemaPath}}`, window.location.href);

try {{
  const response = await fetch(schemaUrl, {{ cache: "no-cache" }});
  if (!response.ok) throw new Error(`HTTP ${{response.status}}`);
  const schema = await response.json();
  sessionStorage.setItem({json.dumps(STUDIO_SESSION_SCHEMA_KEY)}, JSON.stringify(schema));
  sessionStorage.setItem({json.dumps(STUDIO_SESSION_FORMAT_KEY)}, "json");
  await import({json.dumps(app_module)});
}} catch (error) {{
  document.getElementById("root").innerHTML = `
    <main style="font-family:system-ui,sans-serif;padding:2rem;max-width:50rem;margin:auto">
      <h1>Unable to load FermentationJSON schema</h1>
      <p>The schema explorer could not load <code>${{schemaPath}}</code>.</p>
      <pre style="white-space:pre-wrap">${{String(error)}}</pre>
    </main>`;
}}
</script>"""
    studio_index.write_text(pattern.sub(bootstrap, source, count=1), encoding="utf-8")


def build_site(studio_dist: Path, studio_license: Path, output: Path) -> None:
    catalog = _catalog()
    version, schemas = _validate_catalog(catalog)

    if not (studio_dist / "index.html").is_file():
        raise FileNotFoundError(studio_dist / "index.html")
    if not studio_license.is_file():
        raise FileNotFoundError(studio_license)

    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)

    _copy_published_schemas(output, version, schemas)
    _write_launcher(output, version, schemas)

    studio_output = output / "studio"
    shutil.copytree(studio_dist, studio_output)
    _inject_studio_bootstrap(studio_output / "index.html", version, schemas)

    third_party = output / "third-party"
    third_party.mkdir()
    shutil.copy2(studio_license, third_party / "json-schema-studio-MIT.txt")
    (output / ".nojekyll").write_text("", encoding="utf-8")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the FermentationJSON GitHub Pages site")
    parser.add_argument("--studio-dist", type=Path, required=True)
    parser.add_argument("--studio-license", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    build_site(args.studio_dist, args.studio_license, args.output)


if __name__ == "__main__":
    main()
