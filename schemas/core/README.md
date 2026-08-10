# FermentationJSON foundation schemas

These are the first pre-release foundation schemas for FermentationJSON.

They use JSON Schema Draft 2020-12 and implement ADR-0001 through ADR-0003.

## Current schemas

- `identity.schema.json` — document IDs, object IDs, schema IDs, checksums
- `extension.schema.json` — controlled extension container
- `reference.schema.json` — internal and external data references
- `result-form.schema.json` — exact, approximate, bound, range, and non-detect forms
- `reported-statistic.schema.json` — source-reported statistic vocabulary
- `source-document.schema.json` — source/report metadata
- `provenance.schema.json` — reusable provenance
- `quantity.schema.json` — canonical/reported quantity representation
- `measurement.schema.json` — measurements and observations
- `document-metadata.schema.json` — common document metadata
- `document.schema.json` — reusable document envelope

## Pre-release `$id` policy

These schemas intentionally omit `$id` until FermentationJSON selects its
canonical public schema namespace. Repository-relative `$ref` values are used
during pre-release development.

## Composition policy

Concrete value objects are closed with `unevaluatedProperties: false`.
`document.schema.json` is intentionally a reusable envelope and therefore does
not close the root object. A concrete document-type schema must compose the
envelope, constrain `document_type` and `content`, and close the concrete root.

## Semantic validation

Passing JSON Schema validation establishes structural validity only. Full
FermentationJSON conformance also requires semantic validation, including
reference integrity and scientific rules that cannot be expressed completely
in JSON Schema.
