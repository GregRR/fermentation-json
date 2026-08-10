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
