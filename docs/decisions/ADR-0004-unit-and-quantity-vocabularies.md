# ADR-0004: Unit, quantity-kind, and reporting-basis vocabularies

**Status:** Accepted
**Date:** 2026-08-09

## Context

FermentationJSON requires portable quantity semantics without depending on a
particular programming language or unit library. The quantity model also needs
to preserve source units while providing one predictable canonical
representation for interoperable comparison and calculation.

Persisted identifiers must be unambiguous, chemical reporting basis must remain
separate from physical units, `ppm` and `ppb` must not silently become
mass-per-volume concentrations, and brewing requires units whose ordinary names
collide with definitions used in other industries.

External unit systems were considered as possible normative dependencies.
FermentationJSON will not adopt or reproduce UCUM as its normative vocabulary.
UCUM's current license places conditions on use of the UCUM work in development
of another unit-identification standard. There is also a domain-semantic
collision: UCUM's U.S. fluid barrel is 42 U.S. gallons, while U.S. brewing law
defines a beer barrel as 31 U.S. gallons.

## Decision

### 1. FermentationJSON owns its normative persisted identifiers

FermentationJSON defines its own versioned unit, quantity-kind, and
reporting-basis vocabularies.

Core identifiers use lower-case snake case, for example:

- `liter`
- `us_liquid_gallon`
- `imperial_gallon`
- `us_beer_barrel`
- `milligram_per_liter`
- `degree_celsius`
- `mass_concentration`
- `as_substance_equivalent`

A non-core extension identifier must be an absolute URI.

Human symbols and source spellings such as `L`, `gal`, `°C`, `ppm`, or
`mg/L as CaCO3` are not normative persisted identifiers.

### 2. Canonical units are assigned by quantity kind

Every registered core quantity kind declares one canonical unit.

Examples:

- `volume` → `liter`
- `mass` → `kilogram`
- `temperature` → `degree_celsius`
- `pressure` → `kilopascal`
- `mass_concentration` → `milligram_per_liter`
- `equivalent_concentration` → `milliequivalent_per_liter`
- `conductivity` → `microsiemens_per_centimeter`
- `ph` → `ph_scale`

The canonical unit is selected for interoperability and domain practicality.
It is not required to be an SI base unit.

For a registered core quantity kind, `canonical.unit` MUST equal the canonical
unit declared by the applicable quantity-kind vocabulary version.

### 3. Reported representations use normalized identifiers plus source text

A reported representation SHOULD use a registered unit identifier when the
source unit can be identified without inventing meaning.

The exact source spelling, abbreviation, or combined source text may be
preserved separately using `original_unit_text` and `original_text`.

An importer MUST NOT map an ambiguous source token to a specific unit without
sufficient context.

### 4. Quantity kind describes the quantity, not the analyte

Analyte or property identity is separate from quantity kind.

For example, calcium and sulfate measurements can both use
`mass_concentration`; their measurement `property` identifies calcium or
sulfate.

Profiles may define specialized quantity kinds only when the represented
quantity has meaning or canonical-unit policy that differs from an existing
kind.

### 5. Reporting basis is separate from unit

A unit identifier MUST NOT encode chemical reporting basis.

For example:

- unit: `milligram_per_liter`
- reporting-basis kind: `as_substance_equivalent`
- substance: `calcium_carbonate`

This allows `mg/L as CaCO3` to remain distinct from `mg/L HCO3-` without
inventing compound unit identifiers.

### 6. `ppm` and `ppb` remain ratio units

`part_per_million` and `part_per_billion` are dimensionless ratio units.

They MUST NOT be treated as universally equivalent to `milligram_per_liter`
or `microgram_per_liter`.

A mass-per-volume concentration may be derived from a source ratio only when
the necessary basis, density assumption, or other scientific relationship is
known and documented.

### 7. Aliases are input/display aids only

Vocabulary aliases and display symbols are informative.

They may assist import, parsing, and display, but they are not valid persisted
substitutes for stable identifiers.

### 8. The U.S. beer barrel has its own identifier

`us_beer_barrel` is exactly 31 `us_liquid_gallon`.

It MUST NOT be treated as another 42-gallon U.S. fluid barrel merely because
both units may be called `barrel`.

### 9. External mappings are non-normative adapters

Implementations may map FermentationJSON identifiers to external unit systems
when licensing and semantics permit.

Such mappings are adapter behavior. They do not change FermentationJSON unit
meaning and are not a normative dependency of the core specification.

## Consequences

- Interchange files use stable, readable, unambiguous identifiers.
- Canonical-unit behavior is deterministic for registered core quantity kinds.
- Source spelling can still be preserved.
- Profiles can add units and quantity kinds using absolute URI identifiers.
- Chemical basis stays out of unit identifiers.
- Compatibility adapters can map source formats without importing their unit
  vocabularies into the core.
- Semantic validation is required for vocabulary membership, dimensional
  compatibility, and canonical-unit policy.

## References

Primary references used in this decision are recorded in
`docs/references/UNIT_SOURCES.md`.
