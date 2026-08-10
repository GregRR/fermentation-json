# FermentationJSON conformance suites

The `conformance/` tree contains language-independent test vectors for normative
behavior that is not fully expressible in JSON Schema.

A conformance suite is independently versioned. A suite version identifies the
exact rule set and vector contents used for a conformance claim; it is not the
FermentationJSON specification version or schema-set version.

The current foundation suite is under
[`foundation/v0.1.0/`](foundation/v0.1.0/).

## Test-vector model

Each vector-set JSON file contains:

- `vector_set` — the semantic rule family;
- `suite_id` and `suite_version` — the exact suite to which it belongs;
- `cases` — language-independent input/expected-result pairs.

Each case contains:

- a stable `id`;
- an informative `description`;
- `input` data specific to the rule family;
- `expected.conformant`;
- `expected.errors`, containing stable machine-readable rule identifiers.

Error ordering is not significant. Implementations may emit additional
diagnostic detail, paths, or messages, but the applicable core rule identifiers
must remain recognizable.

The suite manifest records SHA-256 hashes of each vector-set file so that a
conformance claim can identify the exact test material used.
