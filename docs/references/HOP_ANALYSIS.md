# Hop analysis references

This note records sources used to keep native FermentationJSON hop semantics separate from BeerJSON compatibility shape.

## BeerJSON 1.0.2 source model

Pinned BeerJSON `hop.json`:

- https://raw.githubusercontent.com/beerjson/beerjson/v1.0.2/json/hop.json

Relevant source definitions are `VarietyInformation` and `OilContentType`. BeerJSON places total oil, essential-oil component percentages, cohumulone, polyphenols, and xanthohumol in one `OilContentType` object. `total_oil_ml_per_100g` encodes its mL-per-100-g basis in the field name.

FermentationJSON preserves that source representation for compatibility but does not treat the source container as proof that every nested percentage has the same scientific denominator.

## Analytica EBC hop methods

Analytica EBC, Hops and Hop Products methods list:

- https://brewup.eu/ebc-analytica/category/chemical-physical/hops-and-hop-products

The method catalog treats these as distinct analytical areas:

- EBC 7.7 — alpha- and beta-acids in hops and hop products by HPLC;
- EBC 7.10 — hop oil content by steam distillation;
- EBC 7.12 — selected hop essential-oil components by capillary gas chromatography/FID;
- EBC 7.14 — total polyphenols in hops and hop pellets;
- EBC 7.15 — xanthohumol in hops and hop products by HPLC.

This separation is the main reason FermentationJSON does not copy BeerJSON `OilContentType` as one native analytical object.

## Industry reference presentation

BarthHaas hop-variety reference material reports total oil in `ml/100g` and presents selected aroma-oil constituents as percentages of total oil:

- https://www.barthhaas.com/hops-and-products/hop-varieties-overview

This corroborates the source interpretation used for the unambiguous total-oil and essential-oil-component mappings. It is informative support; the native model still preserves original source representation and analytical provenance where supplied.

## Conservative mapping rule

Where the pinned BeerJSON schema does not provide enough basis, method, or chemical identity to create a scientifically unambiguous native value, the compatibility mapping preserves the source field without manufacturing stronger semantics.
