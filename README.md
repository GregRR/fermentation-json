# FermentationJSON

FermentationJSON is an open, language-independent, platform-independent JSON interchange standard for fermentation data.

It is designed to represent recipes, executed production batches, ingredients and materials, processes, equipment, measurements, calculations, water chemistry, provenance, and related fermentation records without tying the data model to a particular application, programming language, database, or unit library.

> **Status:** Working draft. The modern FermentationJSON specification is under active development and is not yet a stable interoperability release.

## Design goals

FermentationJSON is being designed around a small set of durable principles:

- **Preserve information.** Import, normalization, and calculation should not silently discard or reinterpret source data.
- **Keep recipe intent separate from batch execution.** Planned values and actual observations are different data.
- **Treat scientific quantities explicitly.** Canonical representations are required for interoperability; originally reported representations can be preserved alongside them.
- **Preserve ranges, bounds, non-detects, uncertainty, reporting bases, and provenance.** A value such as `<5 mg/L`, `ND`, or `50–53 mg/L` is not equivalent to a single exact number.
- **Keep reported and derived data distinct.** Calculated, inferred, predicted, or normalized information must not masquerade as source-reported data.
- **Use modular schemas and profiles.** Reusable foundations are shared across domains, while domain-specific requirements belong in profiles or optional modules.
- **Make compatibility explicit and testable.** External-format compatibility is defined through versioned mappings, fixtures, and loss-reporting rules.
- **Remain implementation-independent.** Normative behavior is defined by the specification, not by a particular software library.

## Current scope

The initial specification is centered on reusable foundation schemas and a brewing-oriented first profile.

Current and planned v1 work includes:

- document metadata, identifiers, and references;
- quantities, measurements, ranges, bounds, and reported statistics;
- provenance and source-document metadata;
- recipes and executed batches;
- ingredients, cultures, materials, and lots;
- process definitions and execution records;
- equipment;
- water-source, target, blend, treatment, and treated-water models;
- calculation and optimization results;
- profiles and controlled extensions;
- compatibility and loss reporting.

Later profiles and optional modules may add richer laboratory records, sampling, sensors, calibration, telemetry, automation, detailed equipment topology, batch genealogy, serving-system engineering, sensory data, and additional fermentation domains such as wine, cider, perry, mead, sake, kombucha, and vinegar.

## Foundation schemas

The first pre-release foundation schemas are now implemented under [`schemas/core/`](schemas/core/).

They currently cover:

- document envelopes and common metadata;
- document and object identifiers;
- internal and external references;
- controlled extensions;
- exact, approximate, bounded, ranged, and non-detected result forms;
- source-reported statistics;
- canonical and reported quantity representations;
- analytical detection, reporting, and quantification limits;
- measurements and observations;
- source-document metadata;
- provenance;
- calculation and model results;
- structured diagnostics, constraints, and constraint outcomes;
- transformation loss reports;
- import, export, and transcode reports.

The schemas use **JSON Schema Draft 2020-12**. Current core schemas carry
versioned canonical `$id` values under
`https://gregrr.github.io/fermentation-json/schemas/0.1.0/core/` and can be resolved offline through the repository schema
catalog.

Passing JSON Schema validation establishes structural validity only. Full FermentationJSON conformance also includes semantic requirements that are not completely expressible in JSON Schema, such as reference integrity, scientific interpretation rules, compatibility preservation, and loss-reporting behavior.

## Quantity model

Every interoperable quantity has a canonical representation. A reported representation is optional but strongly recommended when the value originated from user input, an imported document, an instrument, a laboratory result, a product label, a publication, or another identifiable source.

For example:

```json
{
  "quantity_kind": "volume",
  "canonical": {
    "form": {
      "type": "exact",
      "value": 37.85411784
    },
    "unit": "liter"
  },
  "reported": {
    "form": {
      "type": "exact",
      "value": 10
    },
    "unit": "US_liquid_gallon",
    "original_text": "10 gal"
  },
  "epistemic_state": [
    "reported",
    "user_entered"
  ]
}
```

`canonical` describes the normalized interoperable representation. It does **not** mean that a value is exact, directly measured, authoritative, or free from uncertainty.

The quantity model also permits ranges, one-sided bounds, qualified endpoints, non-detects, analytical limits, reporting bases, and derivation provenance without flattening them into an invented scalar value.

## Recipes and batches

FermentationJSON treats a recipe and an executed production batch as distinct concepts:

- a **recipe** describes intended formulation, process, and targets;
- a **batch** records what actually happened.

A batch may reference the exact recipe revision from which it was executed, while preserving actual material lots, quantities, equipment, measurements, deviations, interventions, transfers, yields, and other execution records separately from the plan.

## External-format compatibility

FermentationJSON uses versioned compatibility profiles for external interchange formats.

The planned **BeerJSON 1.0** compatibility profile is intended to guarantee that every valid BeerJSON 1.0 document can be imported without loss of BeerJSON-defined information. Export back to BeerJSON may be lossy for FermentationJSON-only information, but any such loss must be reported explicitly or the export must fail.

The planned **BeerXML 1.0** compatibility profile is preservation-oriented: standard-defined source information should be retained, and unknown application-specific extensions should be preserved opaquely where practical.

These compatibility profiles are still under development. They should not be treated as implemented compatibility guarantees until their mappings, fixtures, and conformance tests are published.

## Repository guide

Key areas of the repository are:

```text
docs/design/          normative and supporting design documentation
docs/decisions/       architecture decision records
schemas/core/         reusable foundation JSON Schemas
schemas/              production, domain, and optional schemas as they are added
profiles/             domain and interoperability profiles
vocabularies/         versioned controlled vocabularies
compatibility/        external-format mappings and fixtures
examples/             valid and intentionally invalid examples
tests/                schema, conformance, and compatibility tests
proposals/            substantial proposed changes and experimental work
tools/                validators, importers, exporters, and development tools
reference-implementations/
```

For the current architecture and normative design intent, start with [`docs/design/DESIGN.md`](docs/design/DESIGN.md).

Durable implementation decisions are recorded in [`docs/decisions/`](docs/decisions/).

## Development status

Current work is focused on the foundation required before stable domain schemas can be published.

Implemented so far:

- the main architecture and scientific-data design;
- JSON Schema Draft 2020-12 composition rules;
- the common document-envelope model;
- identifier and reference semantics;
- controlled extension rules;
- the first core foundation schemas;
- versioned unit, quantity-kind, and reporting-basis vocabularies;
- reusable calculation, diagnostic, constraint, loss-report, and interchange-report schemas;
- versioned canonical core-schema identifiers and an offline schema catalog;
- positive and negative schema fixtures;
- foundation schema tests.

Important work still in progress includes:

- profile/module declaration and vocabulary-evolution policy;
- foundation semantic-conformance rules;
- concrete document-type schemas;
- brewing production schemas and profile;
- water-treatment schemas;
- BeerJSON and BeerXML compatibility mappings and fixtures;
- full semantic conformance tooling.

See [`ROADMAP.md`](ROADMAP.md) for development sequencing as it is maintained.

## Validation

Foundation tests live under [`tests/schema/`](tests/schema/).

The test suite checks that:

1. core schemas are valid Draft 2020-12 schemas;
2. valid foundation fixtures are accepted;
3. intentionally invalid fixtures are rejected.

Semantic conformance tests will be added alongside the domain and compatibility profiles that require them.

## Contributing

FermentationJSON is being developed as an open specification. Contributions are welcome in areas such as schema design, scientific semantics, compatibility mappings, conformance fixtures, domain modeling, documentation, and implementation experience.

Before proposing a substantial schema or architectural change, review:

- [`docs/design/DESIGN.md`](docs/design/DESIGN.md)
- [`docs/decisions/`](docs/decisions/)
- [`CONTRIBUTING.md`](CONTRIBUTING.md)
- [`proposals/`](proposals/)

Changes that affect interoperability should include appropriate examples, compatibility analysis, and conformance tests where practical.

## Project history

FermentationJSON was originally started in 2015. The original experimental project is preserved on the [`legacy`](https://github.com/GregRR/fermentation-json/tree/legacy) branch.

Modern development restarted in 2026 as a ground-up redesign, retaining the project name and history while rebuilding the specification around modern JSON Schema, explicit scientific semantics, versioned compatibility, and conformance testing.
