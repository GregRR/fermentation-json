# FermentationJSON vocabularies

FermentationJSON uses versioned vocabulary artifacts independently from the
JSON Schema set and from the eventual specification release version.

The current pre-release vocabulary namespace is:

```text
https://gregrr.github.io/fermentation-json/vocabularies/
```

Each vocabulary artifact has an absolute `identifier`, an explicit semantic
`version`, a publication `status`, and vocabulary-class metadata where
applicable.

## Vocabulary classes

FermentationJSON distinguishes four representation choices:

1. **Closed vocabulary** — a finite protocol/control set. Unknown values are
   invalid for that vocabulary version.
2. **Extensible vocabulary** — registered core lower-case snake-case tokens plus
   collision-resistant absolute URI terms. Unknown core-style tokens are
   invalid; unfamiliar URI terms may be preserved but not semantically guessed.
3. **Stable identifier registry** — an open-world set of absolute identifiers.
   Unknown identifiers can remain valid identities even when their domain
   semantics are not locally understood.
4. **Free source label** — verbatim source text. It preserves what a source
   called something but does not itself establish interoperable identity.

The fourth category is intentionally not a controlled vocabulary.

## Versioning

Vocabulary versions use semantic version syntax.

- MAJOR: incompatible vocabulary-contract changes.
- MINOR: backward-compatible additions such as new core terms.
- PATCH: corrections that do not change term identity or normative semantics.

A published versioned vocabulary identifier must not be reused for different
normative content. A term identifier must not be reassigned to a different
meaning. Deprecated terms remain identifiable.

Pre-release artifacts may change until the project declares them normative.

## Document declarations

Core vocabulary versions required by a schema set are implicit in that schema
set and need not be repeated in every document.

A document may declare additional vocabulary artifacts through its
`vocabularies` array. Each declaration identifies an exact artifact version and
states whether understanding it is required for full interpretation.

See ADR-0006 and `schemas/core/declaration.schema.json`.

- `measurement-scales/` — numerical measurement scales and analytical indices that are semantically distinct from physical units.
