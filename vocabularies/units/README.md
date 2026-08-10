# FermentationJSON unit vocabulary

This directory contains the versioned FermentationJSON unit vocabulary.

Normative persisted unit identifiers use stable FermentationJSON IDs such as
`liter`, `us_liquid_gallon`, `imperial_gallon`, `us_beer_barrel`,
`degree_celsius`, and `milligram_per_liter`.

Symbols and aliases are informative input/display metadata, not persisted
substitutes for the stable identifier.

Each unit has a conversion to the reference unit for its physical dimension.
Linear conversions use exact integer numerator/denominator pairs. Affine
conversions additionally provide an exact offset.

The conversion form is:

`reference_value = value * factor + offset`

`us_beer_barrel` is exactly 31 `us_liquid_gallon` and is intentionally
distinct from other units called barrel.

FermentationJSON does not normatively depend on UCUM, Pint, or another unit
library. External mappings are adapter concerns.
