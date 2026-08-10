# ADR-0011: BeerJSON primitive and field-encoded semantics

**Status:** Accepted for pre-release implementation

**Date:** 2026-08-10

## Context

The BeerJSON v1.0.2 schemas encode meaning at several levels beyond ordinary measurable objects. Some values are bare JSON numbers or integers whose scale or basis is carried by the field name, some measurements depend on a sibling field, `PercentType` is reused for semantically different fractions, and `DateType` permits a local date-time without a time-zone offset. BeerJSON also embeds objects rather than supplying stable cross-object identifiers.

Copying these source shapes directly into native FermentationJSON would repeat legacy modeling shortcuts. Aggressively normalizing them would instead risk inventing semantics that BeerJSON does not define.

## Decision

### 1. Primitive JSON types are carriers, not semantic types

A BeerJSON `string`, `number`, `integer`, or `boolean` MUST be interpreted in the context of its declaring field. The primitive carrier alone MUST NOT determine a FermentationJSON quantity kind, identifier class, vocabulary, score scale, unit, or reference semantics.

An omitted optional property is distinct from `null`, zero, `false`, and an empty string. The pinned BeerJSON schemas do not define `null` as a valid alternative for the fields in their 1.0 object model. An importer MUST NOT synthesize a default value merely because an optional property is absent.

### 2. Enum source tokens remain source tokens

BeerJSON enum spelling, capitalization, punctuation, and spacing MUST be preserved for compatibility. A native FermentationJSON vocabulary MAY map a BeerJSON enum token to a different stable identifier, but the mapping MUST remain reversible and MUST NOT treat the BeerJSON token itself as a FermentationJSON core identifier unless separately standardized.

### 3. Percentages are context-refined fractions

BeerJSON `PercentType` values convert numerically from percent to a canonical fraction by dividing by 100. The type-level native quantity kind is `fraction`.

A field MAY refine that kind only when BeerJSON establishes the basis. For example, `RecipeType.alcohol_by_volume` and the ABV-based culture alcohol-tolerance field map to `volume_fraction`. Protein, moisture, hop acids, and other percentage fields are not automatically promoted to `mass_fraction` merely because that interpretation may be conventional; absent an explicit BeerJSON basis, they remain generic fractions with their field semantics preserved.

BeerJSON does not impose a generic 0–100 bound on `PercentType`. The compatibility layer therefore MUST NOT clamp an otherwise valid source percentage into that range. A native field or domain profile MAY impose a scientifically justified range later, but that is separate from source preservation.

### 4. Field-encoded scale and basis are made explicit

When BeerJSON carries scale or basis in a field name, the compatibility mapping makes that meaning explicit rather than reproducing the field-name encoding in the native model.

Current mappings include:

- `cell_count_billions`: numeric count multiplied by `10^9`, mapped to quantity kind `count`;
- `total_oil_ml_per_100g`: exact mL-per-100-g volume/mass basis, mapped to `volume_per_mass` and canonical `liter_per_kilogram`;
- `boil_rate_per_hour` and `drain_rate_per_minute`: mapped to `volume_flow_rate` under ADR-0008/ADR-0009 policy;
- packaging graphic `width` and `height`: mapped to `length` using the sibling `units` field;
- water `pH`: mapped to one exact reported pH value.

The original BeerJSON representation remains preserved for round trip.

### 5. Missing source semantics remain missing

BeerJSON `RecipeType.carbonation` and `PackagingVesselType.carbonation` are bare numbers with no unit token. FermentationJSON MUST NOT infer volumes of CO2 or g/L.

`RecipeType.calories_per_pint` encodes a serving basis in the field name but BeerJSON does not define the calorie realization or pint system. The number is preserved without inventing either unit.

`FermentableType.alpha_amylase` is described using dextrinizing units but has neither an explicit unit token nor method identifier. It remains a source analytical number until a defensible analytical definition is standardized.

`TasteType.rating` has no BeerJSON scale bounds. It MUST NOT be normalized to an assumed rating scale.

### 6. BeerJSON DateType does not imply an instant

BeerJSON `DateType` uses an unanchored JSON Schema `pattern` containing the shapes `YYYY-MM-DD` and `YYYY-MM-DDTHH:MM:SS`. The latter form contains no offset or zone. Because JSON Schema `pattern` searches for a matching substring, the pinned schema can also accept strings with surrounding text. The expression checks digit shape rather than calendar validity, so values such as an impossible month can also satisfy the source schema.

Only a whole-string, calendar-valid `YYYY-MM-DD` value maps to calendar-date semantics. Only a whole-string, calendar-valid `YYYY-MM-DDTHH:MM:SS` value maps to local-date-time semantics. A schema-valid source string that fails those stronger interpretation checks MUST still be preserved for BeerJSON compatibility but MUST NOT be repaired or assigned invented date semantics.

A local date-time without an offset MUST NOT be converted to an RFC 3339 instant by assuming UTC or an implementation-local time zone. A later domain schema may attach an independently known zone or offset, but that is additional information rather than source reconstruction.

### 7. BeerJSON 1.0 version is a semantic profile constraint

BeerJSON's `VersionType` is only constrained to JSON `number` by the pinned schema even though the tagged branch identifies itself as BeerJSON 1.0. The FermentationJSON BeerJSON-1.0 compatibility profile therefore requires the root version's numeric value to equal `1.0`. A different number may satisfy the upstream structural schema but is outside this compatibility profile's BeerJSON-1.0 semantic claim.

JSON numeric lexical spelling is not treated as semantic, so `1` and `1.0` have the same numeric version value.

### 8. Embedded-object equality does not create identity

BeerJSON v1.0.2 does not provide stable cross-object identifiers for its embedded records. An importer MUST NOT merge separate source occurrences merely because fields such as name, producer, product ID, or full object content match.

An importer MAY generate FermentationJSON object identifiers for native representation. Such generated identifiers record native identity and provenance; they do not imply that the source contained reference identity.

## Consequences

- FermentationJSON preserves BeerJSON faithfully without copying source-format shortcuts into its native schemas.
- Missing information stays missing instead of being filled from brewing convention.
- Percentage semantics become safer and field-specific.
- Local civil times cannot accidentally be shifted by an invented time zone.
- Object deduplication becomes an explicit application decision rather than an import side effect.
- Several previously special BeerJSON fields now have complete native semantic mappings, while genuinely unresolved fields remain visibly unresolved.

## Related decisions

- ADR-0008: BeerJSON 1.0 compatibility baseline
- ADR-0009: BeerJSON measurable quantity mapping
- ADR-0010: measurement scales and analytical indices
