# ADR-0005: Public schema identifiers and resolution

**Status:** Accepted

**Date:** 2026-08-10

## Context

FermentationJSON foundation schemas previously omitted `$id` and used repository
files as temporary retrieval locations. That was appropriate while the document
envelope, reference model, and composition rules were still moving, but it is
not sufficient for published interoperability.

A schema resource needs an identity that is independent of where a particular
implementation stores a local copy. Versioned identity is also required so that
a document or validator cannot silently resolve a reference against different
schema content merely because the repository or deployment changed.

JSON Schema Draft 2020-12 defines `$id` as the canonical URI of a schema
resource. The URI is an identifier; network retrieval is not required by the
JSON Schema model. Relative references are resolved against the applicable base
URI established by `$id`.

The project therefore needs both:

1. stable versioned public identifiers; and
2. an offline resolution model that does not make conformance depend on network
   availability.

## Decision

### 1. Canonical public schema namespace

The FermentationJSON public schema namespace is:

```text
https://gregrr.github.io/fermentation-json/schemas/
```

The current pre-release schema-set version is:

```text
0.1.0
```

Core schema IDs in this set have the form:

```text
https://gregrr.github.io/fermentation-json/schemas/<schema-set-version>/core/<schema-filename>
```

For example:

```text
https://gregrr.github.io/fermentation-json/schemas/0.1.0/core/quantity.schema.json
```

The selected namespace is associated with the project's current GitHub-hosted
publication location. HTTP publication may be added independently of schema
validation.

The current IDs are pre-release candidates. If the project deliberately changes
the namespace before the first normative schema publication, this ADR must be
superseded and every affected candidate `$id` updated consistently.

After a versioned schema ID is published normatively, that identifier MUST NOT
be reassigned to different normative schema content.

### 2. Schema-set versioning is distinct from specification versioning

The schema-set version identifies a coordinated set of JSON Schema resources.

It is independent from:

- the FermentationJSON specification release version;
- individual controlled-vocabulary versions;
- implementation/tool versions.

Therefore schema-set version `0.1.0` does not itself announce a
FermentationJSON specification `0.1.0` release.

A change that alters already published schema content requires publication under
a new schema-set version. Historical published IDs remain valid.

### 3. Every normative schema resource has an absolute `$id`

Each core schema MUST declare:

- `$schema` for JSON Schema Draft 2020-12; and
- an absolute HTTPS `$id` in the applicable versioned FermentationJSON schema
  namespace.

Repository paths and `file:` retrieval URIs are not normative schema identity.

Document `schema_id` values and profile/module identifiers that claim normative
conformance MUST use absolute identifiers.

### 4. Relative `$ref` values are permitted only within a versioned schema set

A schema MAY use a fragment-only `$ref` for a local anchor.

A core schema MAY use a relative `$ref` to another resource in the same
versioned core-schema directory. Resolution occurs against the referring
schema's canonical `$id`.

A relative reference MUST NOT escape the current versioned schema-set namespace.

A reference to a separately versioned artifact MUST use that artifact's stable
absolute identifier.

This policy allows concise local references while preventing validation from
silently drifting to another schema-set version.

### 5. Network retrieval is not a conformance requirement

A conforming validator MUST be able to resolve the schema resources it claims to
support without assuming that canonical HTTPS IDs can be fetched at validation
time.

Implementations MAY use:

- an in-memory registry;
- a packaged schema catalog;
- a local cache;
- an application-specific resolver;
- a network resolver when appropriate.

The resolution mechanism MUST preserve canonical resource identity.

The repository provides `schemas/catalog.v0.1.0.json` as a machine-readable map
from canonical IDs to repository paths. The catalog is a distribution and
tooling aid; the `$id` inside each schema remains the authoritative schema
identity.

### 6. No unversioned convenience IDs are defined yet

The project does not currently define `latest`, unversioned, or floating schema
aliases.

A future convenience alias MAY be added for human navigation or tooling, but it
MUST NOT be used where immutable identity or reproducibility is required.

### 7. Resolution behavior is tested independently of repository paths

The conformance tests MUST verify that:

- every core schema has the expected canonical `$id`;
- catalog IDs are unique and match schema contents;
- cross-schema references resolve to registered resources in the same schema
  set;
- validation succeeds from a canonical-ID registry without network retrieval.

## Consequences

- Schema identity no longer depends on checkout paths.
- Relative references remain readable while becoming version-isolated through
  the canonical base URI.
- Validators can remain fully offline.
- A schema-set version becomes an immutable compatibility boundary once
  published.
- Moving repository files does not change schema identity.
- A future project-domain migration requires explicit identifier and
  compatibility handling rather than silently changing old IDs.

## References

- JSON Schema Core, Draft 2020-12:
  `https://json-schema.org/draft/2020-12/json-schema-core`
- Understanding JSON Schema, schema identification and structuring:
  `https://json-schema.org/understanding-json-schema/structuring`
