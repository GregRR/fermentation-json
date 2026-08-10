# BeerJSON 1.0 compatibility

This directory develops the FermentationJSON compatibility profile for BeerJSON 1.0.

## Current baseline

Compatibility work is pinned to the upstream **BeerJSON `v1.0.2` tag**. The BeerJSON document version remains `1.0`; `v1.0.2` is the immutable upstream repository/package snapshot used for this work.

The current files establish a source baseline, exhaustive named-type/declared-field inventory, mapping framework, and executable representative measurable/range round-trip vectors. They do **not** yet constitute a completed compatibility implementation or conformance claim.

Files:

- `source-manifest.v0.1.0.json` — exact upstream source reference;
- `inventory/beerjson-v1.0.2-inventory.json` — named types and declared fields;
- `mappings/unit-tokens.v0.1.0.json` — BeerJSON unit-token handling;
- `mappings/measurable-types.v0.1.0.json` — concrete measurable/quantity type mapping;
- `mappings/analytical-scales.v0.1.0.json` — token-dispatched BeerJSON gravity, color, carbonation, bitterness, and diastatic-power semantics;
- `mappings/primitive-field-semantics.v0.1.0.json` — reusable rules for primitive carriers, percentages, field-encoded scales/bases, local date-times, and identity/absence semantics;
- `fixtures/primitive-field-vectors.v0.1.0.json` — representative source-to-semantic mapping vectors;
- `fixtures/measurable-roundtrip-vectors.v0.1.0.json` — representative measurable/range import and semantic round-trip vectors;
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

## Measurable round-trip fixtures

ADR-0012 adds executable, language-independent vectors for representative BeerJSON measurable objects and ranges. When the source semantics are defined, the expected native FermentationJSON quantity retains enough reported value/unit information to reconstruct the BeerJSON source object while its canonical value is independently checked against the registered unit vocabulary.

A valid BeerJSON measurable object does not have to receive an invented native quantity merely to satisfy compatibility. Unresolved source tokens and mixed analytical-scale ranges instead use a source-preservation-only path: the complete BeerJSON object remains available for lossless round trip, and native normalization waits for an explicit, supported interpretation or calculation. These vectors cover the measurable/range layer only; complete-document compatibility remains pending.

## Primitive and field-encoded semantics

BeerJSON primitive JSON types are treated as serialization carriers, not as complete semantic types. Optional omission remains distinct from `null`, zero, `false`, or an empty string. Enum tokens are preserved exactly even when a native FermentationJSON vocabulary later uses different identifiers.

The compatibility mapping also resolves source semantics encoded outside a value's immediate type. Examples include cell counts expressed in billions by the field name, hop oil reported as mL per 100 g, equipment rates whose time basis is in the field name, and packaging graphic dimensions whose unit is supplied by a sibling field. When BeerJSON does not provide enough semantics, such as its bare numeric carbonation fields or `calories_per_pint`, FermentationJSON preserves the source value rather than inventing missing units.

BeerJSON `DateType` uses an unanchored shape-only regex. Exact calendar-valid date and local-date-time strings can receive native semantics, while other strings accepted by that source regex remain preserved without being repaired or assigned an invented time zone. Distinct embedded BeerJSON objects are likewise not deduplicated merely because descriptive fields happen to match.
