# FermentationJSON schema explorer

The public GitHub Pages site is built from the repository's versioned schema
catalog and the tagged MIT-licensed JSON Schema Studio application.

The repository schemas remain authoritative. The Pages build:

1. validates the repository test suite;
2. builds JSON Schema Studio from the pinned upstream tag;
3. publishes every cataloged schema at the path implied by its canonical `$id`;
4. generates a visualization-only Draft 2020-12 Compound Schema Document for
   each catalog entry so Studio can resolve cross-schema `$ref` values locally;
5. generates a FermentationJSON schema selector from `schemas/catalog.v0.1.0.json`;
6. preloads the selected compound schema into the unmodified Studio application; and
7. deploys the resulting static site to GitHub Pages.

The generated compound schemas are derived publication artifacts only. They do
not replace or modify the authoritative modular schemas, and their embedded
resources retain the original `$id` and `$ref` values.

JSON Schema Studio is not vendored into this repository. The deployment workflow
checks out the pinned upstream release and includes its MIT license in the
published site.

The current integration targets JSON Schema Studio `v0.9.1`.
