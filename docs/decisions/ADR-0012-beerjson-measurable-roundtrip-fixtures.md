# ADR-0012: BeerJSON measurable import and round-trip fixtures

**Status:** Accepted

**Date:** 2026-08-10

## Context

ADRs 0008 through 0011 define the BeerJSON 1.0 compatibility baseline, measurable-type mappings, analytical-scale semantics, and primitive/field semantics. Those artifacts establish how BeerJSON values are to be interpreted, but mapping metadata alone does not demonstrate that a source measurable object can be converted into a valid native FermentationJSON quantity and then reconstructed without losing BeerJSON-defined information.

BeerJSON measurable objects also expose two materially different compatibility cases:

1. the source semantics are sufficiently defined to construct a native FermentationJSON quantity while retaining the reported BeerJSON representation; or
2. the source is valid BeerJSON but its semantics are insufficient for a safe native quantity, or a range combines analytical scales that require an explicit normalization calculation.

A lossless compatibility profile must handle both cases. Losslessness cannot depend on inventing a native interpretation for every valid source value.

## Decision

### 1. Maintain language-independent measurable round-trip vectors

The BeerJSON 1.0 compatibility profile SHALL publish versioned machine-readable vectors covering representative measurable and range objects. Each vector identifies:

- the BeerJSON source type;
- the BeerJSON source object;
- the expected import status;
- the expected native FermentationJSON quantity when one can be constructed safely;
- the required source-preservation result when one cannot;
- the reverse/round-trip path.

The initial vector set is `fixtures/measurable-roundtrip-vectors.v0.1.0.json`.

### 2. Native quantity is preferred only when semantics are defined

When the BeerJSON source type and token have sufficiently defined semantics, import SHALL construct the corresponding native FermentationJSON quantity according to ADR-0009 and ADR-0010.

The native quantity MUST retain a reported representation sufficient to reconstruct the BeerJSON numeric value and source unit token at the JSON data-model level. Canonicalization MUST NOT replace that reported representation.

Numeric lexical formatting such as insignificant trailing zeroes is not required to be reproduced unless a future compatibility profile explicitly makes such lexical detail semantic.

### 3. Canonical values are independently testable

For physical quantities and ratio units, the canonical value in a vector MUST agree with the registered FermentationJSON unit conversion. Test code SHALL compute that relationship independently rather than trusting a duplicated expected conversion constant alone.

Analytical-scale values that do not undergo a scale conversion retain their numeric value while carrying their native measurement-scale identifier.

### 4. Source-preservation-only is a valid lossless import result

A valid BeerJSON measurable object MAY have no safe native FermentationJSON quantity at import time.

Examples include:

- `VolumeType` using the unresolved BeerJSON `ibbl` token;
- `SpecificHeatType` using a calorie or BTU token whose realization is not defined by BeerJSON;
- an analytical range whose endpoints use different measurement scales.

In these cases, import MUST retain the complete BeerJSON source object required for round trip and MUST NOT fabricate a unit, scale, conversion, or common-range representation. A future native interpretation may be derived later only through an explicit, documented transformation.

The compatibility vectors describe the required preservation behavior without yet prescribing one universal storage layout for retained external-format fragments. That storage mechanism will be finalized with complete-document compatibility schemas.

### 5. Same-scale and mixed-scale analytical ranges differ

A BeerJSON analytical range whose endpoints map to the same native quantity kind and measurement scale MAY become one native FermentationJSON range without an additional scale transformation.

If the endpoints map to different analytical scales, the original endpoint objects MUST remain source-preserved. Constructing one native range requires an explicit normalization calculation with applicable model/method provenance.

### 6. Round trip is semantic, not byte-for-byte

For the vectors in this ADR, successful BeerJSON → FermentationJSON → BeerJSON round trip means reconstruction of the same BeerJSON JSON data-model value: the same defined fields, numeric values, and unit tokens. Object-member whitespace, insignificant number formatting, and member ordering are not part of this requirement.

## Consequences

- Compatibility behavior is now executable for representative measurable values instead of existing only as prose/mapping metadata.
- A missing native quantity is not automatically a compatibility failure when the complete BeerJSON source object is retained and no semantics are invented.
- Future implementations in any language can consume the same vectors as conformance cases.
- This ADR does not complete the BeerJSON 1.0 compatibility claim. Complete-document fixtures, domain mappings, identifier/reference preservation, and document-level round-trip behavior remain required.
