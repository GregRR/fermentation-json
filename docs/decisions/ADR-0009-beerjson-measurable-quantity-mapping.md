# ADR-0009: BeerJSON measurable and quantity mapping

**Status:** Accepted for pre-release implementation
**Date:** 2026-08-10

## Context

ADR-0008 pinned the BeerJSON 1.0 compatibility baseline to BeerJSON `v1.0.2`
and established that compatibility must preserve the source representation without
forcing FermentationJSON to reproduce source-schema design choices.

BeerJSON `measureable_units.json` defines several ordinary physical quantities,
several brewing analytical or empirical scales, generic concentration and percent
types whose meaning depends on the unit or field context, and range types whose
minimum and maximum are independent measurable objects.

A mechanically uniform mapping would introduce several semantic errors:

- treating `ppm`, `ppb`, and `mg/l` as interchangeable concentration units;
- treating specific gravity, Plato, and Brix as ordinary units of one physical
  dimension;
- treating SRM, EBC, and Lovibond as an ordinary physical unit family without
  preserving whether the source describes grain/material color or beer/wort color;
- treating IBU, carbonation scales, or diastatic-power scales as simple physical
  conversions before their method and reference semantics are documented;
- collapsing count-like `UnitType` values such as `pkg` into a mathematical
  dimensionless ratio; or
- forcing both endpoints of a BeerJSON range to share one reported unit when the
  BeerJSON schema does not require that.

## Decision

### 1. Map semantics, not source type names

A BeerJSON measurable type MUST be mapped according to its actual scientific or
operational semantics. The source type name alone does not establish a native
FermentationJSON quantity kind when the BeerJSON type combines multiple concepts.

Source value and unit tokens remain preserved independently from the native
FermentationJSON representation.

### 2. Direct physical mappings

The following BeerJSON types have direct type-level mappings to existing or newly
registered FermentationJSON quantity kinds:

| BeerJSON type | Native FermentationJSON quantity kind |
|---|---|
| `VolumeType` | `volume` |
| `MassType` | `mass` |
| `TemperatureType` | `temperature` |
| `PressureType` | `pressure` |
| `AcidityType` | `ph` |
| `TimeType` | `duration` |
| `ViscosityType` | `dynamic_viscosity` |
| `SpecificVolumeType` | `specific_volume` |
| `SpecificHeatType` | `specific_heat_capacity`, where the source unit is semantically resolved |

`PercentType` maps neutrally to `fraction` at the measurable-type layer. A
field-level mapping MAY refine it to `mass_fraction`, `volume_fraction`, or
another applicable fraction kind when the BeerJSON field semantics justify that
refinement.

### 3. Concentration is token-dispatched

BeerJSON `ConcentrationType` does not map to one FermentationJSON quantity kind:

- `mg/l` maps to `mass_concentration`;
- `ppm` maps to generic `fraction` using `part_per_million` as the reported unit;
- `ppb` maps to generic `fraction` using `part_per_billion` as the reported unit.

A domain mapping MAY derive a mass concentration from a ratio only when the
required analyte, density, solution, or reporting-basis assumptions are explicit.
Such a derivation MUST remain distinct from the preserved BeerJSON source value.

### 4. Analytical and empirical scales remain explicit

The following BeerJSON types MUST NOT be registered as ordinary physical-unit
families merely to complete the compatibility table:

- `DiastaticPowerType`;
- `ColorType`;
- `CarbonationType`;
- `BitternessType`;
- `GravityType`.

Their native FermentationJSON model and any conversion relationships require
separate, documented scientific/method provenance. Until that work is complete,
the compatibility mapping preserves the source representation and marks the
native mapping explicitly pending.

This is not data loss. It is a refusal to invent a scientific relationship that
the compatibility source does not itself define sufficiently.

### 5. `UnitType` is context-dependent

BeerJSON `UnitType` combines tokens for mathematical unitlessness and count-like
amounts, including `1`, `dimensionless`, `unit`, `each`, and `pkg`.

FermentationJSON MUST NOT assume that one package equals one item, or that an item
count is scientifically equivalent to a dimensionless ratio. Native mapping is
therefore deferred to the applicable material, culture, inventory, or process
field context while the BeerJSON source token is preserved.

### 6. Reported ranges may preserve endpoint-specific units

BeerJSON range types contain independent `minimum` and `maximum` measurable
objects. A valid source can therefore contain endpoints expressed in different
units.

FermentationJSON canonical ranges continue to use the quantity kind's single
canonical unit. A reported range MUST support either:

1. one common reported unit applying to both endpoints; or
2. explicit `endpoint_units.minimum` and `endpoint_units.maximum` values.

A non-range reported quantity MUST use one reported `unit` and MUST NOT use
`endpoint_units`.

When endpoint-specific units are used, source unit text MAY likewise be retained
per endpoint. Canonicalization MUST NOT erase those source endpoint units.

### 7. Resolve only unambiguous unit tokens

The compatibility map MAY add core units when the unit meaning is sufficiently
clear and independently defensible. This ADR adds the BeerJSON specific-volume
composite units and `J/(kg K)` specific heat capacity because they can be defined
from existing core physical units without importing a BeerJSON modeling shortcut.

The following remain unresolved rather than guessed:

- BeerJSON `ibbl`, because BeerJSON does not define which quantity named
  "Imperial barrel" the token denotes;
- `Cal/(g C)`, because the token does not identify the calorie realization and
  its capitalization is not a sufficient normative definition; and
- `BTU/(lb F)`, because the token does not identify the BTU realization.

## Consequences

### Positive

- FermentationJSON gains a concrete, testable BeerJSON quantity mapping without
  inheriting BeerJSON's semantic conflations.
- Ratio concentration remains distinct from mass concentration.
- Mixed-unit source ranges can now be preserved generically.
- Specific-volume units used by BeerJSON can be canonicalized without source loss.
- Future brewing analytical-scale work is forced to document its scientific basis
  before becoming normative.

### Costs

- Some BeerJSON measurable values remain source-preserved but not yet converted to
  a final native analytical quantity.
- Importers must perform token-sensitive and sometimes field-sensitive mapping
  rather than dispatching only on BeerJSON type name.
- Reported range validation is slightly more complex because common-unit and
  endpoint-unit forms are distinct.

## Alternatives rejected

### Copy every BeerJSON measurable type into FermentationJSON

Rejected because it would preserve source-schema architecture rather than model
scientific meaning.

### Treat all BeerJSON concentration tokens as mass concentration

Rejected because `ppm` and `ppb` are ratios and do not inherently mean `mg/L` or
`µg/L`.

### Require one unit for every reported range

Rejected because BeerJSON permits independently unit-bearing endpoints and because
source documents outside BeerJSON can also present mixed-unit intervals.

### Invent definitions for unresolved BeerJSON tokens

Rejected. Compatibility preservation is preferable to false precision.
