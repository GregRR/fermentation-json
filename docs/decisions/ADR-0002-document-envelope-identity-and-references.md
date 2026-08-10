# ADR-0002: Document envelope, identity, and data references

**Status:** Accepted  
**Date:** 2026-08-09

## Context

FermentationJSON supports multiple document types and must not assume that every document is a recipe. Documents and referenceable objects need stable identity that survives serialization, reordering, and unrelated structural edits.

Using JSON Pointer paths as object identity would make references fragile. The project also needs exact envelope field names before document schemas can be implemented.

## Decision

All normative FermentationJSON documents use the common top-level envelope:

```json
{
  "specification_version": "0.1.0",
  "document_type": "example",
  "schema_id": "schemas/example.schema.json",
  "document_id": "urn:uuid:00000000-0000-0000-0000-000000000000",
  "profiles": [],
  "modules": [],
  "metadata": {},
  "content": {},
  "extensions": {}
}
```

Required fields:

- `specification_version`
- `document_type`
- `schema_id`
- `document_id`
- `content`

Optional fields:

- `profiles`
- `modules`
- `metadata`
- `extensions`

`document_id` is an absolute URI. A UUID URN is the recommended default when no existing persistent URI is appropriate.

A referenceable embedded object uses `object_id`, an opaque string unique within its containing document.

A data reference contains one or both of:

```json
{
  "document_id": "urn:uuid:...",
  "object_id": "..."
}
```

Interpretation:

- only `object_id`: object in the current document;
- only `document_id`: referenced document as a whole;
- both: object within the referenced document.

References may additionally carry `expected_type`, `schema_id`, `media_type`, `checksum`, and `label`.

JSON Pointer may be used as a source/provenance locator but not as persistent object identity.

## Rationale

The envelope gives every FermentationJSON document predictable self-description while keeping document-type payloads isolated under `content`.

Document-scoped opaque object identifiers avoid tying object identity to schema layout. Pairing document and object identity provides simple internal and external references without inventing undocumented URI-fragment rules.

## Consequences

- Document schemas can share one reusable envelope definition.
- Importers must create stable document IDs when source formats lack them.
- Reference integrity requires semantic validation beyond ordinary JSON Schema.
- A future multi-document container can reuse the same document and object identifiers.
