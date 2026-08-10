# Unit and Quantity Vocabulary Sources

**Status:** Informative source record
**Date reviewed:** 2026-08-09

This document records primary sources consulted while defining the initial
FermentationJSON unit and quantity vocabulary. FermentationJSON defines its own
normative identifiers; the sources below establish physical meanings,
conversion relationships, compatibility constraints, and design boundaries.

## International System of Units

Bureau International des Poids et Mesures (BIPM), *The International System of
Units (SI), 9th edition*, current English text updated in 2026.

- https://www.bipm.org/en/publications/si-brochure
- https://doi.org/10.59161/AUEZ1291

## U.S. customary conversion references

National Institute of Standards and Technology (NIST), *Guide for the Use of
the International System of Units (SI), Special Publication 811*, including
Appendix B conversion factors.

- https://www.nist.gov/pml/special-publication-811
- https://www.nist.gov/pml/special-publication-811/nist-guide-si-appendix-b-conversion-factors

## U.S. beer barrel

### Primary regulatory definition

Electronic Code of Federal Regulations, 27 CFR Part 25, beer regulations.

- https://www.ecfr.gov/current/title-27/chapter-I/subchapter-A/part-25
- https://www.ecfr.gov/current/title-27/chapter-I/subchapter-A/part-25/subpart-B/section-25.11

For beer, one barrel as a unit of measure is 31 U.S. gallons. This federal
definition is the primary basis for FermentationJSON `us_beer_barrel`.

### TTB guidance

The Alcohol and Tobacco Tax and Trade Bureau (TTB) likewise states that one
barrel equals 31 U.S. gallons.

- https://www.ttb.gov/regulated-commodities/beverage-alcohol/beer/beer-faqs
- https://www.ttb.gov/about-ttb/glossary/glossary-b

TTB is a bureau of the U.S. Department of the Treasury.

- https://home.treasury.gov/about/bureaus

### Brewers Association industry usage

The Brewers Association also uses the 31-U.S.-gallon beer barrel in its
industry statistics and production reporting.

- https://www.brewersassociation.org/statistics-and-data/national-beer-stats/

The regulatory definition remains the normative source for the
FermentationJSON unit; the TTB and Brewers Association references provide
authoritative regulatory guidance and independent industry corroboration.


## International inch

NIST Office of Weights and Measures, *SI Units – Length*.

- https://www.nist.gov/pml/owm/si-units-length

The international inch is exactly 25.4 mm, or 0.0254 m. FermentationJSON uses this exact relationship for the core `inch` length unit needed by BeerJSON packaging-graphic compatibility.

## BeerJSON compatibility vocabulary

BeerJSON `v1.0.2` `measureable_units.json` schema and generated documentation.

- https://raw.githubusercontent.com/beerjson/beerjson/v1.0.2/json/measureable_units.json
- https://github.com/beerjson/beerjson/blob/v1.0.2/docs/measureable_units.json.md

BeerJSON uses compact source-format unit tokens. FermentationJSON does not
reuse those tokens as its core vocabulary; its BeerJSON compatibility profile
defines explicit mappings while preserving BeerJSON source values and units.

BeerJSON also serializes several measurement scales and analytical indices in its
unit-token position. FermentationJSON does not register `sg`, `plato`, `brix`,
`SRM`, `EBC`, `Lovi`, `vols`, `IBUs`, `Lintner`, or `WK` as physical units.
They map through the measurement-scale vocabulary documented in
`ANALYTICAL_SCALES.md`; cross-scale transformations are explicit calculations.
Composite specific-volume units added for compatibility are defined from the
already registered FermentationJSON volume and mass units. This includes
`milliliter_per_100_gram`, used for BeerJSON hop total oil, with the exact
relationship `1 mL/100 g = 0.01 L/kg`. Ambiguous BeerJSON tokens remain
unresolved rather than being assigned a guessed definition.

## UCUM evaluation

Unified Code for Units of Measure (UCUM), specification and license.

- https://ucum.org/
- https://ucum.org/ucum
- https://ucum.org/license

UCUM was evaluated as an external unit code system but is not a normative
dependency of FermentationJSON.

Relevant considerations include UCUM's license conditions on development of a
different unit-identification standard and the fact that UCUM's U.S. fluid
barrel is 42 U.S. gallons rather than the 31-U.S.-gallon beer barrel.

Any future UCUM mapping is non-normative adapter work and must independently
satisfy semantic and licensing requirements.

## Source policy

When a FermentationJSON unit definition depends on a legal or standards-based
definition, the vocabulary should retain a source reference.

Where similarly named units have different definitions, FermentationJSON must
use distinct identifiers rather than choosing one silently.
