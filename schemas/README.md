# FermentationJSON schema publication

FermentationJSON schemas use JSON Schema Draft 2020-12.

## Canonical identifiers

The current pre-release schema-set version is `0.1.0`.

The canonical public namespace reserved for schema identifiers is:

```text
https://gregrr.github.io/fermentation-json/schemas/
```

Normative schema resources in this schema set use identifiers that mirror their path beneath `schemas/`:

```text
https://gregrr.github.io/fermentation-json/schemas/<schema-set-version>/<path-relative-to-schemas/>
```

Core schema resources therefore continue to use identifiers of the form:

```text
https://gregrr.github.io/fermentation-json/schemas/<schema-set-version>/core/<filename>
```

For example:

```text
https://gregrr.github.io/fermentation-json/schemas/0.1.0/core/quantity.schema.json
```

The schema-set version is an independently versioned normative-artifact set. It
does **not** declare that FermentationJSON specification version
`0.1.0` has been released.

The current identifiers are pre-release candidates. Once a schema-set version
is published as a normative artifact, the content at its versioned identifiers
must not be replaced by different normative content.

## References and version isolation

Schemas may use relative `$ref` values for other schemas in the same versioned schema set and fragment-only references for local anchors. Relative references may cross sibling schema directories but must not escape the versioned schema-set namespace.

Because every schema has an absolute `$id`, those relative references resolve
against the schema's canonical versioned URI, not against the local repository
path. A reference must not escape its schema-set namespace.

This keeps ordinary cross-schema references within the same schema-set version
unless a future schema deliberately uses an explicit absolute reference to a
separately versioned artifact.

## Offline validation

A validator must not require network access merely because a schema uses an
HTTPS `$id`.

`catalog.v0.1.0.json` maps every normative schema resource in the schema set to the repository file that contains it. Implementations may construct an equivalent local
registry, cache, package, or resolver.

The repository tests build such a registry and fail if validation attempts an
unregistered retrieval.

## Convenience identifiers

No unversioned or `latest` schema aliases are defined at this stage.

If convenience aliases are added later, they are not suitable where immutable
identity or reproducibility is required.

## Domain-schema anchors

A normative schema resource may expose multiple named anchors when related concrete objects share a composable base. For example, `ingredients/hop.schema.json` exposes closed `hopDefinition` and `hopVarietyProfile` objects built from the composable `hopDefinitionBase`. Consumers should reference the concrete anchor matching the object they validate.

`production/inventory.schema.json` similarly exposes `materialLot` and `inventoryPosition` as distinct closed objects. Material identity, lot identity, and changing inventory quantity are separate concepts; an inventory position always references its material and may additionally reference a lot.
