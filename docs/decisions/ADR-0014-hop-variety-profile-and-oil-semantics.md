# ADR-0014 — Hop variety profile and oil-analysis semantics

**Status:** Accepted for pre-release implementation
**Decision date:** 2026-08-10

## Context

BeerJSON `v1.0.2` defines `VarietyInformation` as an extension of `HopVarietyBase`. It adds descriptive use `type`, notes, a six-month alpha-loss percentage, free-text substitutes, `OilContentType`, and inventory.

`OilContentType` is not a scientifically uniform object. Its description says that individual compounds are percentages of total oil, but the fields also include cohumulone, total polyphenols, and xanthohumol. Established hop-analysis methods separate essential-oil content/composition from alpha- and beta-acid analysis, total polyphenols, and xanthohumol analysis. Copying the BeerJSON container directly would therefore import a source-model conflation into the native FermentationJSON model.

Inventory is also contextual stock state rather than intrinsic hop-variety identity.

## Decision

FermentationJSON defines a native **hop variety profile** as a descriptive extension of the reusable hop material definition.

The profile may contain:

- descriptive variety roles (`aroma`, `bittering`, `flavor`);
- non-empty notes;
- free-text substitution notes;
- the BeerJSON-defined six-month alpha-acid-loss fraction, explicitly without inventing unreported storage conditions;
- a hop essential-oil profile containing total oil and identified essential-oil component fractions.

The native hop schema uses a composable `hopDefinitionBase`. Closed `hopDefinition` and `hopVarietyProfile` objects are built from that base. This preserves the project rule that reusable bases may be composable while concrete normative objects remain closed.

### Variety roles

BeerJSON combined `type` tokens are mapped to a set of native descriptive roles. These roles describe catalog/reference characteristics; they MUST NOT be treated as instructions for a recipe addition.

### Total oil

BeerJSON `total_oil_ml_per_100g` is mapped to `quantity_kind: volume_per_mass`.

The reported representation uses the explicit unit `milliliter_per_100_gram`; the canonical representation uses `liter_per_kilogram`.

The conversion is exact:

```text
1 mL / 100 g = 0.01 L / kg
```

### Essential-oil components

BeerJSON fields that identify recognized essential-oil components and whose source object defines the percentages as fractions of total oil may map to an extensible native component list.

The initial mapping includes myrcene, humulene, caryophyllene, farnesene, geraniol, beta-pinene, linalool, limonene, and nerol.

The native representation uses an explicit component identifier plus a fraction-of-total-oil quantity rather than one fixed schema property per compound.

### Fields that remain source-preserved

`cohumulone`, `polyphenols`, `xanthohumol`, and generic `pinene` do not receive native analytical quantities in this mapping version.

Reasons:

- cohumulone is analytically associated with alpha-acid composition rather than essential-oil composition, while BeerJSON groups it inside `OilContentType`;
- total polyphenols and xanthohumol are separate hop analyses and BeerJSON does not provide the material/reporting basis needed for a scientifically unambiguous native percentage;
- generic `pinene` does not identify an isomer, while BeerJSON separately provides `b_pinene`.

The BeerJSON source fields MUST remain available for lossless round trip. A later mapping MAY add native semantics if the denominator, analytical method, and identity can be defined without guesswork.

### Inventory

BeerJSON `VarietyInformation.inventory` is source-preserved but MUST NOT be placed inside the native hop variety profile. A future inventory/lot model may map it contextually.

## Consequences

- FermentationJSON does not inherit BeerJSON's mixed analytical container as its native model.
- Native hop oil composition is extensible and does not require adding a schema property for every future compound.
- Material identity, variety-reference data, inventory, lot analysis, and recipe-use state remain separable.
- Compatibility can remain lossless even when only part of a BeerJSON object receives native interpretation.
- Cross-language implementations can reproduce the same decomposition from the machine-readable compatibility mapping and fixtures.

## References

See `docs/references/HOP_ANALYSIS.md` and the pinned BeerJSON source manifest.
