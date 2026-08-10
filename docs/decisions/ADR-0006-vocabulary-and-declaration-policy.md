# ADR-0006: Vocabulary classes and normative declarations

**Status:** Accepted

**Date:** 2026-08-10

## Context

FermentationJSON now has versioned schemas, reusable quantity vocabularies,
profiles/modules in the document envelope, and a controlled extension container.
The remaining ambiguity is semantic rather than syntactic: different kinds of
identifiers need different unknown-value behavior, and a document must be able
to state exactly which non-core artifacts are required for interpretation.

Treating every string as an open enumeration would make spelling errors and
semantic drift look valid. Treating every vocabulary as closed would make
scientific and domain extension unnecessarily brittle. Requiring every document
to repeat every core vocabulary version would add noise without adding useful
information.

## Decision

### 1. FermentationJSON distinguishes four representation categories

A concept MUST be assigned to the narrowest category that preserves the needed
interoperability and extension behavior.

#### Closed vocabulary

Use a closed vocabulary for finite protocol/control terms whose meaning depends
on the exact vocabulary version, such as diagnostic severity or interchange
status.

An unknown value is invalid for that vocabulary version.

#### Extensible vocabulary

Use an extensible vocabulary when FermentationJSON defines a shared core set but
independent domains may need additional terms.

Core terms use registered lower-case snake-case tokens. Non-core terms use
collision-resistant absolute URI identifiers.

An unknown core-style token MUST be rejected. An unfamiliar absolute URI term
MAY be preserved by identity, but an implementation MUST NOT invent or infer its
semantics.

Current unit, quantity-kind, reporting-basis, calculation-status, and
loss-category vocabularies follow this model where their schemas permit URI
extension terms.

#### Stable identifier registry

Use a stable identifier registry for open-world identities where membership is
not a finite enumeration. Unknown absolute identifiers may remain valid
identities even when a processor does not locally understand their domain
semantics.

Examples may later include analytes, organisms, methods, materials, or other
reference entities.

#### Free source label

Use free source text only when preserving what a source literally called
something or when no interoperable identifier is known.

A free source label MUST NOT silently substitute for a controlled identifier or
establish normative semantics.

### 2. Vocabulary artifacts are independently versioned

Normative vocabulary artifacts have:

- a stable absolute identifier;
- an explicit semantic version;
- publication status;
- a documented vocabulary class or classes;
- explicit unknown-value behavior where extensible.

The FermentationJSON vocabulary namespace is:

```text
https://gregrr.github.io/fermentation-json/vocabularies/
```

Vocabulary versions are independent from schema-set versions and specification
release versions.

Vocabulary versioning follows these rules:

- **MAJOR** for incompatible vocabulary-contract changes;
- **MINOR** for backward-compatible additions such as new core terms;
- **PATCH** for corrections that do not change term identity or normative
  semantics.

A published versioned vocabulary identifier MUST NOT be reused for different
normative content. A term identifier MUST NOT be reassigned to a different
meaning. A deprecated term remains identifiable.

Pre-release vocabulary artifacts may change until explicitly published as
normative.

### 3. Core vocabulary bindings are implicit in their governing artifact

A schema set, profile, or module may normatively bind exact versions of the core
vocabularies it uses.

A document does not need to repeat those bindings merely to use ordinary core
terms. The applicable schema/profile/module determines them.

### 4. Documents declare additional vocabulary artifacts explicitly

The document envelope provides an optional `vocabularies` array for vocabulary
artifacts not already fixed by the applicable schema set, profile, or module.

Each declaration contains:

- `identifier` — absolute artifact identifier;
- `version` — exact semantic version;
- `required` — whether understanding that vocabulary is necessary for full
  interpretation of the document.

An implementation MAY preserve or ignore an unsupported optional vocabulary as
allowed by the applicable schemas and profiles. It MUST NOT claim full
interpretation if a required vocabulary is unsupported.

### 5. Profile and module declarations are structured and exact

`profiles` and `modules` are arrays of declaration objects rather than bare
identifier strings.

Each declaration contains:

- `identifier` — absolute artifact identifier;
- `version` — exact semantic version.

Declaring a profile or module is a conformance claim. Its requirements therefore
apply and are not optional. A processor that does not support a declared profile
or module cannot claim full semantic interpretation of that document.

Within each declaration array, an artifact identifier MUST appear at most once.
A document MUST NOT declare two versions of the same profile, module, or
additional vocabulary under the same identifier.

### 6. Required and optional extensions retain their existing meaning

The extension-container key remains the extension identifier. An extension entry
continues to state whether it is `required`.

An extension entry may additionally provide:

- `version` for separately versioned extension semantics;
- `schema_id` for a published payload schema.

An unsupported optional extension may be preserved without interpretation. An
unsupported required extension prevents a processor from claiming full
interpretation of the document.

### 7. Structural validity and semantic understanding remain distinct

JSON Schema validates declaration shape, identifier syntax, closed vocabulary
membership, and other structural constraints.

Semantic conformance additionally checks matters such as:

- duplicate artifact identifiers across declaration entries;
- whether required profiles/modules/vocabularies/extensions are supported;
- whether a core token exists in the applicable vocabulary version;
- whether an unfamiliar URI term can be preserved but not interpreted.

A processor MUST NOT turn an unknown term into a guessed known term merely to
continue processing.

## Consequences

- Closed protocol vocabularies catch typos and future-version terms early.
- Extensible scientific/domain vocabularies remain open without sacrificing
  collision resistance.
- Source wording can be preserved without conflating labels with identifiers.
- Documents can state exact profile/module versions and additional vocabulary
  dependencies.
- Unsupported required artifacts fail predictably at semantic-conformance time.
- Core documents stay compact because schema-bound vocabulary versions are not
  repeated everywhere.

## Related decisions

- ADR-0002: document envelope, identity, and references
- ADR-0003: closed normative objects and controlled extensions
- ADR-0004: unit and quantity vocabularies
- ADR-0005: public schema identifiers and resolution
