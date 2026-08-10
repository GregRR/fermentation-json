# ADR-0007: Foundation semantic conformance and test vectors

**Status:** Accepted

**Date:** 2026-08-10

## Context

JSON Schema establishes structural validity but cannot express every
FermentationJSON interoperability rule. The design already distinguishes
structural validation from full conformance and identifies reference integrity,
required-artifact handling, derivation rules, and loss-report behavior as
semantic requirements.

These rules must be testable across implementations without making Python or a
particular validation library normative.

## Decision

### 1. Foundation semantic conformance is independently versioned

The foundation semantic-conformance suite is identified by:

```text
https://gregrr.github.io/fermentation-json/conformance/foundation/0.1.0/manifest.json
```

Its current pre-release version is `0.1.0` and it currently targets
schema set `0.1.0`.

The conformance-suite version is independent from the specification version,
schema-set version, vocabulary versions, profile/module versions, and software
versions.

A conformance claim SHOULD identify the exact suite identifier and version used.

### 2. Conformance vectors are language independent

Normative semantic behavior that benefits from executable examples is
represented through JSON vector sets under:

```text
conformance/foundation/v0.1.0/vectors/
```

Each vector case contains a stable case identifier, input, expected conformance
status, and stable machine-readable error identifiers.

The Python tests in `tests/conformance/` are supporting test infrastructure.
They do not define the normative semantics and may be replaced by equivalent
implementations in other languages.

The suite manifest records SHA-256 hashes for the vector-set files so a test run
can identify the exact vector content it evaluated.

### 3. Local reference integrity

Within one FermentationJSON document scope:

- `object_id` values MUST be unique;
- a `dataReference` that omits `document_id`, or names the current document,
  and includes `object_id` MUST resolve to an object in that document;
- a reference naming a different `document_id` is external and is not required
  to resolve during local-document conformance validation.

A profile or package format MAY add stronger external-reference requirements.

The generic vectors separate known object identifiers from data references.
Concrete schema-aware validators are responsible for identifying instance
locations governed by object-identity and `dataReference` schemas; they MUST NOT
use an undocumented heuristic that confuses an object definition with a
reference.

### 4. Required declared artifacts are semantic requirements

Profiles and modules are requirements whenever declared and require support for
the exact identifier/version pair.

Additional vocabularies and extensions prevent full interpretation only when
marked `required`.

An implementation MUST NOT claim full semantic interpretation when a required
declared artifact is unsupported.

### 5. Explicit derivation must be reflected in epistemic state

`canonical` and `reported` are representation dimensions and remain independent
from origin/derivation.

When a quantity contains an explicit `derivation` object, its
`epistemic_state` MUST include at least one of:

- `calculated`;
- `derived`;
- `estimated`;
- `inferred`;
- `predicted`.

This is a one-way invariant. A reported representation may coexist with derived
canonical information, so `reported` and a derived-origin state MAY both be
present.

The absence of `derivation` is not by itself sufficient to prove that a value is
source-reported, and this foundation rule does not require derivation metadata
for every possible derived-state use. Profiles MAY define stronger rules where
scientific interpretation requires them.

### 6. Loss reports must be internally consistent and attributable

When an interchange report embeds a loss report:

- the loss report's source and target descriptors MUST exactly match those of
  the enclosing interchange report;
- compatibility-profile identifier/version metadata supplied by the enclosing
  report MUST agree with the embedded loss report;
- every loss entry MUST identify the affected source information using
  `source_path` or `source_object`;
- every loss entry MUST state the transformation in `transformation` or explain
  the loss in `explanation`.

These requirements supplement the existing structural rules that distinguish
`lossless`, `lossy`, and `not_completed` operations.

### 7. Error identifiers are stable conformance vocabulary

The foundation suite uses stable lower-case snake-case error identifiers listed
in its manifest.

Implementations MAY provide additional messages, paths, severity mapping, or
implementation-specific diagnostic metadata. Such additions MUST NOT alter the
meaning of the core error identifier.

## Consequences

- Full conformance becomes testable separately from JSON Schema validation.
- Cross-language implementations can consume the same semantic vector files.
- Reference integrity does not require unrestricted external dereferencing.
- Required artifact support is tested as an interpretation capability rather
  than a structural property.
- Source preservation and derived information can coexist without conflation.
- Lossy transformations become attributable and auditable.
- Conformance claims can identify an exact suite version and vector content.

## Related decisions

- ADR-0001: JSON Schema dialect and composition
- ADR-0002: document envelope, identity, and references
- ADR-0003: closed objects and extensions
- ADR-0005: public schema identifiers and resolution
- ADR-0006: vocabulary and declaration policy
