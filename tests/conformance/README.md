# Semantic conformance tests

These tests execute the language-independent vectors under `conformance/`.

The Python code is test infrastructure, not normative implementation code. The
normative behavior is defined by the design specification/ADRs and represented
by the versioned vector suite. Other language implementations should be able to
consume the same JSON vectors and produce the same core error identifiers.
