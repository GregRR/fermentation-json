# ADR-0001: JSON Schema dialect and composition policy

**Status:** Accepted  
**Date:** 2026-08-09

## Context

FermentationJSON requires modular schemas, reusable definitions, profile composition, closed normative objects, stable references, and implementation-independent validation.

The project needs to choose a JSON Schema dialect before foundation schemas are written. It also needs a consistent rule for closing composed object schemas without preventing profiles or modules from adding defined properties.

## Decision

FermentationJSON normative schemas will use **JSON Schema Draft 2020-12**.

Schema resources will declare:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema"
}
```

The initial foundation will use standard Draft 2020-12 vocabularies and will not define a custom FermentationJSON JSON Schema dialect.

Authoring conventions:

- use `$defs` for reusable local schema definitions;
- use `$anchor` when a location-independent schema reference is preferable to a structural JSON Pointer;
- avoid references that depend on JSON Pointer paths across schema-resource boundaries;
- keep reusable base schemas composable;
- apply `unevaluatedProperties: false` at concrete/leaf schemas rather than closing reusable base schemas prematurely;
- use standard `format` annotations, while treating normative format checking as part of full FermentationJSON conformance unless the validator is explicitly configured to assert those formats.

Published schema resources will use immutable absolute `$id` values. During pre-release development, schemas may omit `$id` and use repository-relative `$ref` values until the canonical public schema namespace is selected.

## Rationale

Draft 2020-12 is the current published JSON Schema dialect and directly supports the modular composition required by FermentationJSON. `unevaluatedProperties` permits a concrete composed schema to reject undeclared fields while still recognizing properties evaluated by referenced or composed subschemas.

Deferring the final public `$id` namespace avoids publishing identifiers under a domain or URL structure that the project has not yet committed to.

## Consequences

- Validators used for FermentationJSON development must support Draft 2020-12.
- Schema tests must distinguish structural validation from semantic/full conformance.
- Reusable base schemas must not casually set `unevaluatedProperties: false`.
- The public schema URI namespace remains a release blocker, but not an implementation blocker.
- Changing JSON Schema dialect later is a specification-level compatibility decision.

## References

- JSON Schema Specification, Draft 2020-12.
- JSON Schema Core, `$id`, schema resources, and reference resolution.
- Understanding JSON Schema, `unevaluatedProperties`.
