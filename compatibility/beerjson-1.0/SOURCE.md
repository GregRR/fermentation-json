# BeerJSON 1.0 source baseline

**Upstream project:** BeerJSON
**Compatibility document version:** 1.0
**Pinned upstream tag:** `v1.0.2`
**Pinned commit:** `fbe84b007f22205094493cce232b61d770ab8088`
**Tag date:** 2021-10-12

The upstream repository states that published versions are preserved by branch or tag. FermentationJSON therefore pins this compatibility baseline to the immutable `v1.0.2` tag rather than to BeerJSON `main`.

The `v1.0.2` tag commit itself changes only the npm package version from `1.0.1` to `1.0.2`. The BeerJSON schemas at that tag declare JSON Schema Draft-07 and continue to identify themselves using `master`/`main`-style raw GitHub URLs. Those embedded `$id` values are **not** used as FermentationJSON's version pin; the tag and commit in `source-manifest.v0.1.0.json` are authoritative for this compatibility work.

The upstream schema files are referenced rather than copied in this initial baseline. If FermentationJSON later vendors the BeerJSON schema snapshot for offline conformance testing, the upstream MIT license and required copyright notice must accompany the copied material.

Authoritative upstream references:

- repository: `https://github.com/beerjson/beerjson`
- tag: `https://github.com/beerjson/beerjson/tree/v1.0.2`
- generated BeerJSON 1.0 documentation: `https://beerjson.github.io/beerjson/`

The machine-readable manifest lists the exact raw URL for each schema file.
