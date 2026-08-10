# FermentationJSON foundation vocabulary

This directory records controlled terms used by reusable foundation schemas.

The vocabulary artifact mirrors terms that are enforced directly by JSON Schema.
Keeping the machine-readable registry alongside those schemas makes vocabulary
classification and versioning explicit without weakening structural validation.

Vocabulary classes are:

- `closed` — only terms defined by the applicable version are valid;
- `extensible` — registered core tokens are valid, and collision-resistant
  absolute URI terms may identify extension semantics.

An unfamiliar lower-case core-style token is never treated as a future term.
Unknown URI terms may be preserved by identity, but an implementation must not
invent their semantics.
