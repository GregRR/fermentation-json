# ADR-0013: First material and hop domain schema

**Status:** Accepted
**Date:** 2026-08-10

## Context

FermentationJSON foundation and BeerJSON measurable compatibility work are sufficiently mature to begin concrete domain schemas. BeerJSON `HopVarietyBase` is a useful first pressure test because it combines required identity text, optional producer/product/origin text, a source enum, and percent-valued analytical properties without requiring the recipe/process graph.

Beginning domain schemas also exposes a publication issue: ADR-0005 initially described the catalog primarily in terms of the `core/` directory. A coordinated schema set now needs canonical IDs and offline resolution for sibling domain directories as well.

## Decision

### 1. Schema-set IDs mirror the normative path under `schemas/`

Every normative schema in schema set `0.1.0` uses an identifier of the form:

```text
https://gregrr.github.io/fermentation-json/schemas/0.1.0/<path-relative-to-schemas/>
```

Existing core IDs are unchanged. Domain schemas may use relative references across sibling directories provided resolution remains inside the same versioned schema-set namespace. The schema catalog covers all normative schema resources in the set, not only `core/`. Network retrieval remains unnecessary.

### 2. Material identity is separated from hop-specific properties

`production/material.schema.json` defines a reusable material-definition base with stable object identity, meaningful name, textual producer/product/origin fields, provenance, and extensions. Text fields that are not yet structured identities are named explicitly (`producer_name`, `origin_text`) so consumers do not mistake source text for resolved organization or geography objects.

The reusable base remains composable. Concrete material definitions close their object shape with `unevaluatedProperties: false`.

### 3. Hop definitions extend material definitions

`ingredients/hop.schema.json` adds hop form plus alpha- and beta-acid properties. Native hop definitions require a non-empty material name but do not require alpha acid merely because BeerJSON does. BeerJSON compatibility MUST NOT dictate native requiredness.

Alpha and beta acid are represented as `fraction` quantities with canonical unit `one`. The BeerJSON compatibility mapping does not infer a more specific mass basis that BeerJSON does not state.

### 4. Hop form is a FermentationJSON vocabulary

Core hop-form terms are `extract`, `leaf`, `wet_leaf`, `pellet`, `powder`, and `plug`. Extension terms use absolute URI identifiers. BeerJSON source tokens remain source representations; for example, BeerJSON `leaf (wet)` maps to native `wet_leaf` through an explicit reversible compatibility token map.

### 5. BeerJSON `year` remains source-preserved

The pinned BeerJSON schema declares `HopVarietyBase.year` only as a string. FermentationJSON MUST NOT silently relabel it as crop year, harvest year, or production year. The first hop mapping therefore retains that field for BeerJSON round trip without populating a native year property.

Likewise, a BeerJSON value that is valid under weaker source constraints but cannot satisfy the native schema (for example an empty required BeerJSON name) remains source-preservable without weakening the native FermentationJSON model.

## Consequences

- FermentationJSON now has its first concrete non-core domain schemas.
- The schema catalog and offline resolver cover the full versioned schema set.
- BeerJSON `HopVarietyBase` has concrete native target paths for all safely interpreted fields.
- Compatibility may combine native representation with retained source-only fields.
- `VarietyInformation`, hop oil profiles, inventory, and `HopAdditionType` remain separate follow-up work so inventory and planned material use are not embedded into material identity merely because BeerJSON nests them together.
