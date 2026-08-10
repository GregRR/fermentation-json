# BeerJSON 1.0 compatibility

This directory develops the FermentationJSON compatibility profile for BeerJSON 1.0.

## Current baseline

Compatibility work is pinned to the upstream **BeerJSON `v1.0.2` tag**. The BeerJSON document version remains `1.0`; `v1.0.2` is the immutable upstream repository/package snapshot used for this work.

The current files establish a source baseline, exhaustive named-type/declared-field inventory, unit-token mapping baseline, and field-mapping framework. They do **not** yet constitute a completed compatibility implementation or conformance claim.

Files:

- `source-manifest.v0.1.0.json` — exact upstream source reference;
- `inventory/beerjson-v1.0.2-inventory.json` — named types and declared fields;
- `mappings/unit-tokens.v0.1.0.json` — BeerJSON unit-token handling;
- `mappings/measurable-types.v0.1.0.json` — concrete measurable/quantity type mapping;
- `mappings/analytical-scales.v0.1.0.json` — token-dispatched BeerJSON gravity, color, carbonation, bitterness, and diastatic-power semantics;
- `mappings/field-mapping.v0.1.0.json` — one mapping row for every declared object field;
- `profile.v0.1.0.json` — pre-release compatibility-profile manifest.

## Preservation rule

An importer MUST preserve the BeerJSON-defined source value and source unit token even when it also produces a canonical FermentationJSON representation. Canonicalization MUST NOT erase the source representation needed for round trip.

Array item order MUST be preserved. JSON object-member order is not treated as semantic.

## Native-model rule

Compatibility is a translation requirement, not a requirement to reproduce BeerJSON's schema design inside FermentationJSON. For any nontrivial mapping, the mapping record separates:

1. source representation;
2. semantic interpretation;
3. native FermentationJSON representation; and
4. reverse/export mapping.

The native FermentationJSON schema SHOULD model the underlying concept directly. For example, BeerJSON `boil_rate_per_hour` and `drain_rate_per_minute` are `VolumeType` values whose field names supply the time basis; FermentationJSON treats them as `volume_flow_rate`, preserves the original BeerJSON value/unit token, and converts explicitly for its canonical representation.

This rule prevents compatibility work from importing dimensional shortcuts, field-name scales, or other legacy serialization compromises into the FermentationJSON native model.

## Unknown fields

The strict compatibility guarantee applies to documents valid under the pinned BeerJSON schemas. Nonstandard application fields are not BeerJSON-defined information. A pragmatic importer may preserve them opaquely, but it must report the source deviation rather than silently describing the input as strictly conforming BeerJSON.

## Important mapping pressure points

Several BeerJSON fields encode semantics partly in the field name rather than their value schema. Examples include `boil_rate_per_hour`, `drain_rate_per_minute`, `cell_count_billions`, `total_oil_ml_per_100g`, and `calories_per_pint`. Bare numeric carbonation fields also lack an explicit unit. These are marked `special_mapping_required` and MUST NOT be normalized by guesswork.

BeerJSON `ConcentrationType` permits `ppm`, `ppb`, and `mg/l`. FermentationJSON preserves `ppm` and `ppb` as ratio-unit source representations and does not silently reinterpret them as `mg/L` or `µg/L`.
## Measurable and quantity mapping

ADR-0009 defines the first concrete BeerJSON type mappings. Physical quantities such as volume, mass, temperature, pressure, duration, viscosity, and specific volume map to native FermentationJSON quantity kinds. `PercentType` maps neutrally to `fraction` until a field mapping justifies a more specific fraction kind. `ConcentrationType` is token-sensitive: `mg/l` maps to mass concentration, while `ppm` and `ppb` remain ratio quantities.

BeerJSON gravity, color, carbonation, bitterness, and diastatic-power values are mapped through explicit measurement-scale semantics rather than registered as ordinary physical-unit families. Distinct scales remain distinct native quantity kinds. Cross-scale relationships, where supported, are calculations with method/model/reference-condition provenance rather than unit conversions. Mixed-scale BeerJSON range endpoints remain independently preserved unless an explicit normalization calculation is performed.

BeerJSON range endpoints are complete measurable objects and may therefore use different source units. FermentationJSON reported ranges can preserve endpoint-specific units while canonical ranges remain normalized to one canonical unit.
