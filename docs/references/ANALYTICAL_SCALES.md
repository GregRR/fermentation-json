# Analytical and measurement scale sources

**Status:** Maintained source record for pre-release FermentationJSON semantics

This document records the source basis for brewing measurement scales used by
FermentationJSON and its BeerJSON 1.0 compatibility work. It deliberately
distinguishes **measurement scales and analytical indices** from ordinary
physical units.

FermentationJSON does not reproduce restricted analytical procedures. A public
method listing or technical source can establish the identity and nature of a
method without implying that the complete proprietary/restricted procedure was
reviewed.

## Gravity and extract

### Specific gravity / Plato

ASBC publicly lists Wort methods for specific gravity and extract, and its tools
include an Apparent Extract (Plato or Balling) to Specific Gravity calculator.
Analytica EBC Method 9.4 calculates original, real, and apparent extract and
original gravity from specific-gravity determinations.

Sources:

- ASBC Wort Methods: https://www.asbcnet.org/Methods/WortMethods/pages/default.aspx
- ASBC Calculators & eXtras: https://www.asbcnet.org/Methods/Tools/extras/pages/default.aspx
- Analytica EBC 9.4 listing: https://brewup.eu/ebc-analytica/category/chemical-physical/beer

**FermentationJSON policy:** `specific_gravity` and `degrees_plato` are separate
scale semantics. Conversion requires an identified model or table and applicable
reference conditions; it is not a unit conversion.

### Brix

OIML R 142-1 describes the International Sucrose Mass Fraction Scale, % mass
(Brix), as a scale used by refractometers and requires conversion information
when a refractometer presents such a scale.

Source:

- OIML R 142-1:2025: https://www.oiml.org/en/files/pdf_r/r142-1-e25.pdf

**FermentationJSON policy:** Brix is retained as a separate sucrose-scale
reading. A Brix reading from wort or another non-sucrose matrix is not silently
renamed Plato or treated as exact wort extract. Any correction is derived data.

## Beer color

Analytica EBC 9.6 identifies beer colour as a spectrophotometric method. ASBC
technical material describes the ASBC reference color metric as a spectral
absorbance measurement at 430 nm of clarified beer.

Sources:

- Analytica EBC 9.6: https://brewup.eu/ebc-analytica/beer/colour-of-beer-spectrophotometric-method-im/9.6
- ASBC 2017 presentation, *Measuring beer color—A different language*:
  https://www.asbcnet.org/events/archives/2017ASBCMeeting/proceedings/Pages/55.aspx

**FermentationJSON policy:** SRM and EBC are explicit analytical-index scales.
Lovibond remains a distinct visual/material color scale. FermentationJSON does
not encode SRM/EBC or Lovibond relationships as physical-unit conversions. If a
consumer performs a scale conversion, the result is derived and records the
chosen relationship/model.

## Bitterness

ASBC Beer-23 and Analytica EBC 9.8 are method-defined determinations of beer
bitterness. EBC describes the result as determination of bitter substances,
mainly iso-alpha-acids. ASBC notes known behavior differences for dry-hopped beer
in the current method family.

Sources:

- ASBC Beer-23 Master the Method:
  https://www.asbcnet.org/Methods/BeerMethods/Pages/Beer-23-MasterMethod.aspx
- ASBC Beer Methods: https://www.asbcnet.org/Methods/BeerMethods/pages/default.aspx
- Analytica EBC 9.8: https://brewup.eu/ebc-analytica/beer/bitterness-of-beer-im/9.8

**FermentationJSON policy:** IBU is an operational analytical index. It is not
serialized as an alias for mg/L iso-alpha-acids and is not a direct measure of
perceived bitterness.

## Diastatic power

ASBC Malt Methods identifies multiple procedures for evaluating malt diastatic
power. Analytica EBC 4.12.1/4.12.2/4.12.3 define methods for determining the
combined activity of alpha- and beta-amylase under standardized reaction
conditions.

Sources:

- ASBC Malt Methods: https://www.asbcnet.org/Methods/MaltMethods/pages/default.aspx
- Analytica EBC 4.12.1:
  https://brewup.eu/ebc-analytica/malt/diastatic-power-of-malt-by-spectrophotometry-manual-method/4.12.1
- Analytica EBC 4.12.3:
  https://brewup.eu/ebc-analytica/malt/diastatic-power-of-malt-by-automated-discrete-analysis/4.12.3

**FermentationJSON policy:** degrees Lintner and Windisch-Kolbach are explicit
scale semantics. FermentationJSON does not encode the commonly cited numerical
relationship as a unit conversion. A conversion may be added later only with
identified method/source provenance.

## Carbonation

The Brewers Association *Draught Beer Quality Manual* defines "volumes of CO2"
as gas volume relative to beverage volume and distinguishes that representation
from grams of CO2 per liter. Its appendix discusses conversion using stated
standard gas conditions and gives a more precise reference-density approach.

Source:

- Brewers Association, *Draught Beer Quality Manual*, 4th ed., Appendix C.
  Project source copy is retained separately from this specification repository.

**FermentationJSON policy:** `volumes` and `g/L` are not two ordinary units of a
single quantity family. `g/L` is mass concentration. `volumes` is a
reference-condition-dependent gas-volume ratio. Conversion is a derived
calculation whose reference conditions must be stated.

## General rule

A source-format token may look like a unit while actually naming a scale, index,
or method-defined result. FermentationJSON preserves the source token but maps it
to the appropriate quantity kind and measurement-scale identifier. Cross-scale
normalization is performed only as an explicit derivation.
