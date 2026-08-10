# FermentationJSON quantity-kind vocabulary

A quantity kind defines what a numeric quantity means and selects the one
canonical unit required for its canonical representation.

Quantity kind does not identify an analyte. Calcium and sulfate measurements,
for example, both use `mass_concentration`; the measurement `property`
identifies which analyte was measured.

Profiles may define additional quantity kinds using absolute URI identifiers.
