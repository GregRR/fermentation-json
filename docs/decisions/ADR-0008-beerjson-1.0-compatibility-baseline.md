# ADR-0008: BeerJSON 1.0 compatibility baseline

**Status:** Accepted

**Date:** 2026-08-10

## Context

FermentationJSON requires lossless import of BeerJSON 1.0-defined information. A compatibility guarantee cannot be tested against a mutable upstream branch or against an informal understanding of BeerJSON fields.

The BeerJSON repository publishes versioned tags and identifies its current specification as BeerJSON 1.0. The latest tag in the 1.0 release line is `v1.0.2`. Its tag commit changes the package version from 1.0.1 to 1.0.2; the BeerJSON document version remains 1.0.

BeerJSON schema resources at the tag still contain `$id` values that reference the repository's mutable development branch. Those embedded IDs therefore do not provide an immutable external-version pin for FermentationJSON.

## Decision

### 1. Pin compatibility work to BeerJSON v1.0.2

The BeerJSON 1.0 compatibility baseline MUST identify upstream tag `v1.0.2` and commit `fbe84b007f22205094493cce232b61d770ab8088`.

Compatibility tools MUST NOT silently substitute the current BeerJSON `main` branch for that snapshot.

### 2. Maintain a machine-readable inventory

FermentationJSON MUST maintain an inventory of the named BeerJSON types, declared object fields, requiredness, inheritance, and unit/enumeration vocabularies relevant to compatibility.

Every declared BeerJSON object field MUST have a mapping entry before the BeerJSON compatibility profile can be considered complete.

A mapping entry MAY remain explicitly pending while the target FermentationJSON domain schema is not yet defined. Pending status is preferable to inventing a premature target structure.

### 3. Preserve source representation

Import MUST preserve BeerJSON-defined source values and BeerJSON unit tokens required for round trip. A normalized or canonical FermentationJSON quantity MAY coexist with that source representation but MUST NOT replace it.

Array item ordering MUST be preserved. JSON object-member ordering is not treated as BeerJSON-defined semantic information.

### 4. Do not infer missing semantics

When BeerJSON encodes meaning in a field name, sibling field, or prose description rather than the value type, the mapping MUST make that semantic transformation explicit.

A mapping MUST NOT invent a unit for a bare numeric field merely because a likely convention exists.

BeerJSON `ppm` and `ppb` source units MUST be preserved as reported ratio units. Conversion to mass-per-volume requires explicit context or assumptions and is a separate canonicalization step.

### 5. Compatibility does not dictate native FermentationJSON representation

BeerJSON source schema shape MUST NOT determine the native FermentationJSON schema shape when the BeerJSON representation is dimensionally weak, encodes semantics in a field name, or otherwise conflates serialization convenience with the underlying concept.

For each nontrivial mapping, compatibility work MUST distinguish four layers:

1. the exact BeerJSON source representation;
2. the semantic interpretation of that representation;
3. the native FermentationJSON representation chosen for the semantic concept; and
4. the reverse/export rule used to reconstruct BeerJSON-representable information.

The native FermentationJSON representation SHOULD model the underlying concept directly even when doing so differs from BeerJSON's value type. Source preservation provides compatibility; structural imitation is not required.

For example, BeerJSON `boil_rate_per_hour` and `drain_rate_per_minute` use `VolumeType`, but their field names define rates. FermentationJSON MUST treat those concepts as `volume_flow_rate`, preserve the original BeerJSON `VolumeType` value and unit token as source representation, and perform any canonical rate conversion explicitly. It MUST NOT model the native concept as a plain volume merely to mirror BeerJSON.

Likewise, scales or reporting bases encoded in names such as `cell_count_billions` and `total_oil_ml_per_100g` MUST become explicit semantics in the native model while the original BeerJSON field representation remains preservable for round trip.

### 6. Strict and pragmatic handling of nonstandard fields

The normative lossless-import guarantee applies to documents valid under the pinned BeerJSON schemas.

An importer MAY offer a pragmatic mode for application-specific or otherwise nonconforming fields. Pragmatic mode SHOULD preserve such data opaquely where practical and MUST report the source deviation. Opaque preservation does not make a nonstandard field BeerJSON-defined information.

### 7. No compatibility claim yet

The source baseline and mapping inventory are necessary but not sufficient for a completed compatibility claim.

A completed BeerJSON 1.0 compatibility profile additionally requires concrete target mappings, representative import fixtures, round-trip tests, and validation of the BeerJSON-representable subset.

## Consequences

- Future FermentationJSON domain schemas are developed against an explicit external field inventory.
- Upstream changes on BeerJSON `main` cannot silently change the compatibility target.
- Fields with incomplete semantics remain visibly unresolved instead of being normalized by assumption.
- FermentationJSON domain schemas remain free to model the actual semantic concept correctly rather than copying a legacy source shape.
- The source representation remains available for lossless round trip even when FermentationJSON uses richer canonical semantics.
