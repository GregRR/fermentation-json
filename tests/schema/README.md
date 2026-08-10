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
