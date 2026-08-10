# FermentationJSON foundation schemas

These are the first pre-release foundation schemas for FermentationJSON.

They use JSON Schema Draft 2020-12 and implement the accepted foundation ADRs as applicable.

## Current schemas

- `identity.schema.json` — document IDs, object IDs, schema IDs, semantic versions, checksums
- `declaration.schema.json` — profile, module, and additional-vocabulary declarations
- `vocabulary-identifier.schema.json` — core and extension vocabulary identifiers
- `extension.schema.json` — controlled extension container
- `reference.schema.json` — internal and external data references
- `result-form.schema.json` — exact, approximate, bound, range, and non-detect forms
- `reported-statistic.schema.json` — source-reported statistic vocabulary
- `source-document.schema.json` — source/report metadata
- `provenance.schema.json` — reusable provenance
- `quantity.schema.json` — canonical/reported quantity representation
- `measurement.schema.json` — measurements and observations
- `document-metadata.schema.json` — common document metadata
- `document.schema.json` — reusable document envelope
- `diagnostic.schema.json` — machine-readable warnings and explanations
- `constraint.schema.json` — generic constraint definitions
- `constraint-outcome.schema.json` — constraint evaluation outcomes
- `format-descriptor.schema.json` — source/target interchange format descriptors
- `calculation-result.schema.json` — calculations, models, optimization candidates, and statuses
- `loss-report.schema.json` — machine-readable transformation loss reports
- `interchange-report.schema.json` — import, export, and transcode operation reports

## Schema identifiers

Every core schema now has a canonical versioned `$id` under:

```text
https://gregrr.github.io/fermentation-json/schemas/0.1.0/core/
```

Relative cross-schema `$ref` values resolve against that canonical versioned
base URI. The repository file path is not the schema's normative identity.

The machine-readable mapping between canonical IDs and repository paths is in
[`../catalog.v0.1.0.json`](../catalog.v0.1.0.json). See
[`../README.md`](../README.md) and ADR-0005 for publication and immutability
rules.

## Composition policy

Concrete value objects are closed with `unevaluatedProperties: false`.
`document.schema.json` is intentionally a reusable envelope and therefore does
not close the root object. A concrete document-type schema must compose the
envelope, constrain `document_type` and `content`, and close the concrete root.

## Semantic validation

Passing JSON Schema validation establishes structural validity only. Full
FermentationJSON conformance also requires semantic validation, including
reference integrity and scientific rules that cannot be expressed completely
in JSON Schema.

## Declarations and vocabulary semantics

`document.schema.json` uses structured profile/module declarations and permits explicit declarations of additional vocabulary artifacts. Core vocabulary bindings are supplied by the governing schema set/profile/module and do not need to be repeated in each document.

`quantity.schema.json` validates vocabulary identifier syntax. Registry
membership, dimensional compatibility, and canonical-unit selection are
semantic conformance requirements checked by
`tests/schema/test_vocabulary_semantics.py`. A reported range may use one common
`unit` or explicit `endpoint_units` when the source expresses its minimum and
maximum in different units; non-range reported quantities continue to require one
common `unit`.

## Generic result and interchange semantics

`calculation-result.schema.json` deliberately permits failed, infeasible, or
indeterminate calculations without numeric outputs. A consuming implementation
must not manufacture an output merely to populate a field.

Constraint parameters and named calculation values are intentionally generic at
the foundation layer. Their detailed semantics are supplied by the applicable
constraint type, calculation type, profile, or module.

`interchange-report.schema.json` distinguishes operational completion from
information preservation:

- `lossless` means no loss report is permitted;
- `lossy` requires a machine-readable loss report;
- `not_completed` represents an operation that did not produce a completed
  transformation.

A failed interchange operation must use `not_completed`.


Required profiles and modules are always semantic requirements when declared. Additional vocabularies and extensions explicitly distinguish optional from required understanding. Unsupported required artifacts prevent a processor from claiming full interpretation even when the document is structurally valid.
