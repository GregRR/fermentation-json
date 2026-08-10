# Foundation semantic conformance suite 0.1.0

**Status:** Pre-release

**Suite identifier:** `https://gregrr.github.io/fermentation-json/conformance/foundation/0.1.0/manifest.json`

**Applicable schema set:** `0.1.0`

This suite covers foundation semantics that JSON Schema validation alone cannot
establish.

## Rule families

### Reference integrity

- `object_id` values must be unique within a document scope.
- A data reference that is local to the current document and includes an
  `object_id` must resolve to an object in that document.
- A reference whose `document_id` identifies another document is external and
  is not required to resolve during local-document validation.

The generic vectors express object definitions and data references separately.
A concrete schema-aware implementation is responsible for identifying which
instance locations are object definitions and which are `dataReference`
locations.

### Required artifact support

- Profiles and modules are requirements whenever declared and require exact
  identifier/version support.
- Additional vocabularies block full interpretation only when `required` is
  true.
- Extensions block full interpretation only when `required` is true.
- Unsupported optional vocabularies/extensions may remain uninterpreted as
  allowed by their governing schemas and profiles.

### Source and derivation semantics

`canonical` and `reported` remain representation dimensions. They do not alone
establish origin.

When a quantity explicitly contains `derivation`, its `epistemic_state` must
acknowledge at least one derived-origin state:

- `calculated`;
- `derived`;
- `estimated`;
- `inferred`;
- `predicted`.

This rule is intentionally one-way. The presence of `reported` data does not
forbid derived canonical information; `reported` and a derived-origin state may
coexist.

### Interchange and loss consistency

For an interchange report with an embedded loss report:

- source and target descriptors must match the enclosing report exactly;
- compatibility-profile metadata must match when supplied by the enclosing
  report;
- every loss entry must identify affected source information through
  `source_path` or `source_object`;
- every loss entry must state the transformation through `transformation` or
  provide an `explanation` of the loss.

Structural requirements such as `lossy` requiring a non-empty loss report remain
in JSON Schema and are complementary to these semantic rules.

## Conformance claims

A processor claiming foundation full-conformance against this suite should
identify both the suite identifier and exact suite version.

Passing this suite establishes only the rules in the declared suite scope. It
does not imply support for future domain profiles or external-format
compatibility profiles.
