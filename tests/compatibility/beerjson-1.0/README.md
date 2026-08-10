# BeerJSON 1.0 compatibility tests

The current tests validate the **mapping baseline**, not a completed importer.

They ensure that:

- the external source is pinned to BeerJSON `v1.0.2`;
- the inventory is internally complete;
- every declared BeerJSON object field has exactly one mapping row;
- every BeerJSON unit token has an explicit mapping status;
- known semantic pressure points remain explicitly marked;
- ppm/ppb are not silently converted to mass-per-volume;
- the profile cannot be mistaken for a completed compatibility claim.

Import, upstream-schema validation, and round-trip tests will be added as concrete domain mappings become executable.

- `test_primitive_field_semantics.py` verifies conservative percentage refinement, bare-number/integer classification, absence/null semantics, local date-time/version rules, field-encoded bases, exact inch conversion, and representative primitive mapping vectors.
