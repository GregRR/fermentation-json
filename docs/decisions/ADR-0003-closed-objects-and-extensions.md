# ADR-0003: Closed normative objects and controlled extensions

**Status:** Accepted  
**Date:** 2026-08-09

## Context

FermentationJSON needs to prevent misspelled or misunderstood fields from being silently accepted while still supporting application-specific extensions and later profiles.

Permitting arbitrary properties on normative objects would weaken interoperability. Closing reusable base schemas with `additionalProperties: false`, however, interferes with schema composition.

## Decision

Concrete normative FermentationJSON objects are closed.

Concrete/leaf schemas will normally apply:

```json
{
  "unevaluatedProperties": false
}
```

after all applicable composition.

Reusable base schemas will generally remain open until composed into a concrete schema.

Application-specific data must be placed in the explicit `extensions` container rather than inserted as undeclared fields.

The extension container is an object keyed by a collision-resistant extension identifier:

```json
{
  "extensions": {
    "https://example.org/my-extension/v1": {
      "required": false,
      "data": {
        "example": true
      }
    }
  }
}
```

Each extension entry contains:

- `required`: whether understanding the extension is necessary for correct interpretation;
- `data`: the extension payload.

Unknown optional extensions may be preserved without interpretation. An implementation that does not understand a required extension cannot claim full interpretation/conformance for that document.

## Rationale

This design catches ordinary schema mistakes and prevents accidental field-name divergence while retaining a deliberate, namespaced escape hatch for experimentation and application-specific data.

Using `unevaluatedProperties` at the concrete schema level works with composition because it can account for properties evaluated by referenced and combined schemas.

## Consequences

- Unknown standard fields are validation failures rather than silently ignored data.
- Forward compatibility depends on declared specification/profile versions and the extension mechanism, not permissive core objects.
- Extension processors must preserve unknown extensions when required by transformation rules.
- Extension promotion into the core requires an explicit migration path.
