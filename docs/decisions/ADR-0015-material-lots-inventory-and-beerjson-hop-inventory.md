# ADR-0015: Material lots, inventory positions, and BeerJSON hop inventory

**Status:** Accepted
**Date:** 2026-08-10

## Context

FermentationJSON now has reusable material definitions and native hop material/variety schemas. BeerJSON `VarietyInformation` may contain a `HopInventoryType`, but the pinned BeerJSON v1.0.2 schema gives that object only one optional field: `amount`, which may be a mass or volume measurable value. The source object does not identify a lot, supplier, storage location, observation time, storage condition, or other stock metadata, and an empty object is schema-valid.

Inventory is contextual state. It changes independently of the relatively stable identity/specification of a hop variety or other material. A physical lot is also distinct from both: it identifies a traceable instance/batch of a material, while an inventory record states how much of a material or lot is present in some context.

The model should be reusable by fermentables, cultures, additives, packaging materials, treatment chemicals, and other domains rather than becoming a hop-only solution.

## Decision

FermentationJSON defines three separate concepts:

1. **Material definition** — relatively stable identity/specification of a material.
2. **Material lot** — a traceable physical lot/batch of a material, referencing the material definition.
3. **Inventory position** — a quantity-on-hand/state record referencing a material and optionally a material lot.

The initial `production/inventory.schema.json` defines closed `materialLot` and `inventoryPosition` objects.

A material lot requires `material_reference` and may additionally record document-scoped identity, source lot identifier, supplier name, receipt/open/expiration dates, provenance, and extensions. The initial schema intentionally does not put current quantity-on-hand on the lot object.

An inventory position requires:

- `material_reference`;
- `quantity`.

It may additionally carry:

- `lot_reference`;
- document-scoped identity;
- a free-text location label;
- an RFC 3339 `recorded_at` timestamp;
- provenance;
- extensions.

The initial inventory quantity kinds are `mass`, `volume`, and `count`. Their canonical units remain the registered quantity-kind canonical units: kilogram, liter, and one respectively.

A lot reference does not replace the material reference on an inventory position. Keeping the material reference explicit makes the stock record interpretable without dereferencing the lot. Semantic conformance may later verify that a referenced lot identifies the same material.

## BeerJSON HopInventoryType mapping

BeerJSON `HopInventoryType.amount` maps to a separate native `inventoryPosition.quantity` only when:

- the source `amount` is present; and
- the containing BeerJSON hop import has produced a referenceable native material/variety object that can supply `material_reference`.

BeerJSON mass and volume amounts map through the already-defined measurable/quantity rules. Their reported BeerJSON values and unit tokens remain retained for reverse mapping.

The mapping MUST NOT create a native material lot from `HopInventoryType`, because the BeerJSON object contains no lot identity.

An empty BeerJSON `HopInventoryType` MUST remain distinguishable from zero inventory. It is preserved as source data and produces no native inventory position.

If a containing BeerJSON hop cannot receive a referenceable native material representation, its inventory object remains source-preserved rather than creating a dangling or fabricated native stock record.

The importer MUST NOT infer from BeerJSON hop inventory:

- lot identity;
- supplier;
- storage location;
- stock timestamp;
- storage conditions;
- availability status;
- zero quantity when `amount` is absent.

## Rationale

Separating material identity, lot identity, and changing stock state prevents inventory updates from mutating ingredient definitions and avoids duplicating the same conceptual boundary across every ingredient domain.

Requiring contextual material identity for a native BeerJSON inventory record also preserves referential meaning. Compatibility is satisfied by retaining source information when the source lacks enough structure for the native object; it does not require creating incomplete native records.

## Consequences

- Native hop variety profiles no longer need to source-preserve all non-empty BeerJSON inventory records; safely mappable amounts can become separate inventory positions.
- BeerJSON inventory still round-trips through retained reported quantity data or source preservation.
- Material lots can be introduced independently when a source actually provides lot identity.
- Future ingredient domains can reuse the same inventory schema.
- Later work may add richer location, stock-status, transaction, reservation, or inventory-ledger concepts without changing the material-definition boundary.
