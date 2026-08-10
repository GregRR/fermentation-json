# FermentationJSON reporting-basis vocabulary

Reporting basis carries chemical/reporting semantics that must not be hidden
inside a physical unit identifier.

Example:

```json
{
  "unit": "milligram_per_liter",
  "basis": {
    "kind": "as_substance_equivalent",
    "substance": "calcium_carbonate"
  }
}
```

The initial vocabulary is deliberately small. Extensions use absolute URI
identifiers.
