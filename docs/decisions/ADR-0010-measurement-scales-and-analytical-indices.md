# ADR-0010: Measurement scales and analytical indices

**Status:** Accepted for pre-release implementation
**Date:** 2026-08-10

## Context

BeerJSON `v1.0.2` serializes several brewing measurements as though their scale
labels were unit tokens: specific gravity, Plato, Brix, SRM, EBC, Lovibond,
volumes of CO2, IBU, degrees Lintner, and Windisch-Kolbach.

ADR-0009 intentionally deferred these mappings because copying those tokens into
the FermentationJSON physical-unit vocabulary would incorrectly imply that all
values within each BeerJSON type are ordinary unit conversions.

The underlying standards and method listings instead show a mix of:

- dimensionless ratio readings;
- sucrose/extract scales;
- spectrophotometric color indices;
- a reference-condition-dependent dissolved-gas volume ratio;
- an operational bitterness index; and
- method-defined enzyme-activity scales.

## Decision

### 1. Measurement scale is distinct from physical unit

FermentationJSON introduces a versioned `measurement_scales` vocabulary. A
quantity representation MAY identify a `scale` independently from its `unit`.

A scale identifier MUST NOT be interpreted as a unit alias. The `unit` continues
to identify the numeric carrier/dimension while `scale` identifies the
method/scale semantics needed to interpret the number.

### 2. Scale-defined BeerJSON values use explicit native quantity kinds

The initial native mappings are:

| BeerJSON token | Native quantity kind | FJSON unit | Measurement scale |
|---|---|---|---|
| `sg` | `specific_gravity` | `one` | `specific_gravity` |
| `plato` | `plato_extract` | `one` | `degrees_plato` |
| `brix` | `brix_reading` | `one` | `degrees_brix` |
| `SRM` | `srm_color_index` | `one` | `srm_color_index` |
| `EBC` | `ebc_color_index` | `one` | `ebc_color_index` |
| `Lovi` | `lovibond_color_index` | `one` | `lovibond_color_scale` |
| `vols` | `carbon_dioxide_volume_ratio` | `one` | `carbon_dioxide_volumes` |
| `IBUs` | `bitterness_index` | `one` | `international_bitterness_units` |
| `Lintner` | `diastatic_power_lintner` | `one` | `degrees_lintner` |
| `WK` | `diastatic_power_windisch_kolbach` | `one` | `windisch_kolbach` |

BeerJSON carbonation `g/l` is not scale-defined. It maps to physical
`mass_concentration` with `gram_per_liter`, with carbon dioxide supplied by the
field/domain semantic context.

The use of `one` for a scale-defined index does **not** make the raw number an
ordinary mathematical fraction. The quantity kind and `scale` are required
semantic qualifiers.

### 3. Cross-scale transformations are calculations

FermentationJSON does not register SG/Plato, Brix/Plato, SRM/EBC,
Lovibond/SRM, volumes-CO2/g-L, IBU/concentration, or Lintner/WK relationships as
physical unit conversions.

Where a relationship is adopted, the converted value MUST be derived and SHOULD
record the formula/table/method, reference conditions where applicable, and
source references. The source-reported representation remains unchanged.

### 4. BeerJSON analytical ranges require scale-aware handling

BeerJSON range endpoints are complete measurable objects. Therefore a schema-valid
range can use different analytical scale tokens at its two endpoints.

When both endpoints map to the same native quantity kind and scale, an importer
MAY construct one native FermentationJSON range while preserving both source
objects.

When the endpoint scales differ, an importer MUST NOT place them into one native
range by pretending the scales are common units. It MUST preserve the two source
endpoints and may construct a normalized range only after an explicit conversion
calculation.

### 5. Missing source semantics remain missing

BeerJSON `RecipeType.carbonation` and `PackagingVesselType.carbonation` are bare
numbers rather than `CarbonationType`. This ADR does not invent `vols` or `g/l`
for those fields. They remain source-preserved special mappings until BeerJSON
normative material establishes the missing representation semantics.

Likewise, BeerJSON specific gravity values do not gain an invented reference
temperature during import.

## Consequences

### Positive

- FermentationJSON models analytical meaning rather than source-token shape.
- Scale labels do not pollute the physical-unit vocabulary.
- Method- and reference-condition-dependent transformations become auditable
  derived calculations.
- Brix is not silently equated with Plato.
- IBU is not silently equated with iso-alpha-acid concentration.
- Lovibond is not silently treated as a modern spectrophotometric color unit.
- Carbonation `vols` is not silently treated as a mass-concentration unit.

### Costs

- Importers need token-sensitive analytical mapping.
- Some values that software traditionally "converts" with a simple formula require
  explicit calculation metadata in FermentationJSON.
- Mixed-scale ranges may require source-preserving compatibility structures until a
  normalization model is selected.

## Alternatives rejected

### Register every BeerJSON analytical token as a unit

Rejected because it conflates measurement scales/method-defined indices with
physical units.

### Pick one canonical brewing scale and convert everything during import

Rejected because doing so would force provisional or context-dependent scientific
relationships into the core interchange model.

### Preserve only opaque BeerJSON values

Rejected because the source material supports useful native semantic distinctions
without requiring unsafe conversions.
