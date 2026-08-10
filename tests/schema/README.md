# Foundation schema tests

The test suite validates every core schema against Draft 2020-12, validates all
positive fixtures, and confirms rejection of all negative fixtures.

Because pre-release schemas intentionally omit `$id`, the test harness injects
a temporary `file://` `$id` in memory only. This establishes the retrieval base
needed for repository-relative `$ref` resolution without altering the schemas
or publishing filesystem identifiers.

`FormatChecker` is enabled because FermentationJSON treats URI/date/time
semantics as part of full conformance even though Draft 2020-12 does not
require format assertion by default.

## Vocabulary semantic tests

`test_vocabulary_semantics.py` verifies relationships that JSON Schema cannot
express by itself:

- vocabulary identifier uniqueness;
- dimension/reference-unit consistency;
- one canonical unit per registered quantity kind;
- canonical-unit use in examples;
- reported-unit dimensional compatibility;
- reporting-basis requirements;
- exact scalar conversion in representative fixtures;
- the 31-U.S.-gallon definition of `us_beer_barrel`;
- rejection of ambiguous unregistered customary unit identifiers;
- `ppm` and `ppb` remaining fraction units.

## Result and report semantic tests

`test_result_report_semantics.py` checks relationships that cross object
boundaries and therefore are not fully expressible in the individual schemas:

- constraint identifiers are unique within a calculation result;
- constraint outcomes reference declared constraints;
- ranked candidate numbers are unique;
- an embedded loss report describes the same source and target formats as its
  enclosing interchange report.

## Canonical schema identifier tests

`test_schema_identifiers.py` verifies that:

- every core schema has one cataloged canonical `$id`;
- the schema IDs use the current versioned public namespace;
- relative cross-schema references stay inside that exact schema set;
- valid fixtures resolve through a canonical-ID registry without network or
  filesystem-based reference retrieval.

The older structural tests intentionally remain separate so that canonical-ID
resolution and ordinary schema validation fail independently when either layer
is broken.

## Declaration and vocabulary-policy tests

`test_declaration_policy.py` verifies structured profile/module/vocabulary declarations, duplicate-identifier semantics, required-versus-optional interpretation behavior, vocabulary catalog metadata, and synchronization between the foundation vocabulary registry and schema-enforced control terms.

## Relationship to semantic conformance

These tests establish structural and schema-adjacent invariants. Full foundation
semantic behavior that is intentionally not encoded in JSON Schema is exercised
through the versioned vectors under `conformance/` and the runners in
`tests/conformance/`.
