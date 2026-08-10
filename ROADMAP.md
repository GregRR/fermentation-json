# FermentationJSON Roadmap

**Status:** Maintained project roadmap  
**Last updated:** 2026-08-09

This roadmap describes the intended development sequence for the modern FermentationJSON specification.

It is **informative**, not normative. Normative requirements live in the versioned specification, schemas, profiles, vocabularies, and compatibility artifacts. A roadmap item is not part of the FermentationJSON compatibility guarantee until it appears in a published normative release.

Detailed architectural rationale is maintained in [`docs/design/DESIGN.md`](docs/design/DESIGN.md), with durable implementation decisions recorded in [`docs/decisions/`](docs/decisions/).

---

## Roadmap principles

Development is ordered primarily by technical dependency and interoperability value.

The project should:

- stabilize reusable scientific and document foundations before duplicating them in domain schemas;
- validate architectural decisions with schemas and fixtures rather than prose alone;
- establish BeerJSON 1.0 compatibility early enough to influence the brewing data model;
- preserve source information before adding convenience calculations or transformations;
- distinguish structural JSON Schema validation from full semantic conformance;
- keep optional engineering capabilities from blocking a useful first stable brewing release;
- keep future fermentation domains from forcing premature complexity into the initial brewing profile;
- prefer small numbers of coherent, testable milestones over a large collection of loosely defined features.

Release labels and phase numbers describe intended sequencing, not calendar commitments.

---

# Phase 1 — Foundation

**Goal:** Establish the reusable document, scientific-data, compatibility, and conformance infrastructure on which all later FermentationJSON schemas depend.

**Current status:** In progress.

## 1.1 Architecture and design foundation

Completed:

- [x] Define FermentationJSON as a language-independent and platform-independent interchange standard.
- [x] Separate normative interchange semantics from application-internal data models.
- [x] Define recipe and executed batch as distinct concepts.
- [x] Define source-reported and derived information as distinct concepts.
- [x] Define canonical and reported quantity representations as independent from epistemic state.
- [x] Define ranges, bounds, non-detects, analytical limits, reported statistics, and qualified endpoints.
- [x] Define special logarithmic treatment for pH.
- [x] Define provenance and source-document metadata requirements.
- [x] Define profile, module, extension, compatibility, loss-reporting, versioning, and conformance architecture.
- [x] Define production-model boundaries for recipes, batches, processes, materials, cultures, water, equipment, and calculations.
- [x] Pressure-test the scientific-data model against real water-report requirements.
- [x] Reconcile Water Treatment Calculator interoperability requirements into the main design.
- [x] Establish pre-release change-control and design-status rules.

Primary artifact:

- [`docs/design/DESIGN.md`](docs/design/DESIGN.md)

## 1.2 JSON Schema architecture

Completed:

- [x] Select JSON Schema Draft 2020-12.
- [x] Define schema composition rules.
- [x] Define use of `$defs` and `$anchor`.
- [x] Define concrete-object closure using `unevaluatedProperties: false`.
- [x] Define the controlled extension mechanism.
- [x] Define the common document envelope.
- [x] Define document IDs, document-scoped object IDs, and internal/external reference semantics.
- [x] Define the pre-release `$id` policy.

Decision records:

- [`docs/decisions/ADR-0001-json-schema-dialect-and-composition.md`](docs/decisions/ADR-0001-json-schema-dialect-and-composition.md)
- [`docs/decisions/ADR-0002-document-envelope-identity-and-references.md`](docs/decisions/ADR-0002-document-envelope-identity-and-references.md)
- [`docs/decisions/ADR-0003-closed-objects-and-extensions.md`](docs/decisions/ADR-0003-closed-objects-and-extensions.md)
- [`docs/decisions/ADR-0005-public-schema-identifiers.md`](docs/decisions/ADR-0005-public-schema-identifiers.md)
- [`docs/decisions/ADR-0006-vocabulary-and-declaration-policy.md`](docs/decisions/ADR-0006-vocabulary-and-declaration-policy.md)

## 1.3 Initial foundation schemas

Completed:

- [x] Identity primitives.
- [x] Common document metadata.
- [x] Reusable document envelope.
- [x] Internal and external references.
- [x] Controlled extension container.
- [x] Exact, approximate, bound, range, qualified-range, and non-detect result forms.
- [x] Reported-statistic representation.
- [x] Canonical and reported quantity representations.
- [x] Analytical detection, reporting, and quantification limits.
- [x] Basic derivation metadata.
- [x] Measurements and observations.
- [x] Source-document metadata.
- [x] Provenance.
- [x] Positive and negative foundation fixtures.
- [x] Draft 2020-12 schema-validation tests.

Current implementation:

- [`schemas/core/`](schemas/core/)
- [`examples/valid/foundation/`](examples/valid/foundation/)
- [`examples/invalid/foundation/`](examples/invalid/foundation/)
- [`tests/schema/`](tests/schema/)

## 1.4 Remaining foundation decisions

These items should be resolved before the foundation is considered stable enough for broad domain-schema work.

### Unit and quantity vocabulary

- [x] Define the canonical-unit policy.
- [x] Define stable unit identifiers and alias policy.
- [x] Define initial quantity-kind identifiers.
- [x] Define initial reporting-basis vocabulary and extensibility rules.
- [x] Define semantics for customary concentration notation such as ppm and ppb.
- [x] Add initial fixtures for ambiguous customary units, explicit U.S./Imperial units, chemical reporting bases, and canonical conversion preservation.

The normative standard must remain independent of any particular unit library.

### Published schema identifiers

- [x] Select a canonical public schema URI namespace controlled by the project.
- [x] Define immutable versioned `$id` structure.
- [x] Define convenience/unversioned identifier policy: none initially.
- [x] Add versioned `$id` values to core schemas.
- [x] Verify canonical-ID resolution with registry-based Draft 2020-12 validator tests.

### Reusable semantic schemas

- [x] Add generic calculation/model-result schema.
- [x] Add machine-readable warning/explanation schema.
- [x] Add constraint and constraint-outcome schema.
- [x] Add loss-report schema.
- [x] Add import/export/transcode report structures.
- [x] Add structured profile/module and additional-vocabulary declarations.
- [ ] Add reference-integrity semantic validation.

### Vocabulary policy

- [x] Define closed, extensible, stable-identifier, and free-source-label categories.
- [x] Define vocabulary artifact and term versioning policy.
- [x] Define unknown core-token and unknown URI-term behavior.
- [x] Establish initial foundation vocabularies and catalog.
- [ ] Establish water-specific vocabularies alongside the first water schemas.

### Foundation conformance

- [ ] Define a machine-readable conformance-suite version.
- [ ] Add semantic tests that JSON Schema alone cannot express.
- [x] Verify required-extension and required-vocabulary interpretation behavior.
- [ ] Verify reference resolution and unresolved-reference failures.
- [ ] Verify source-reported versus derived-data invariants.
- [ ] Verify loss-report behavior with representative transformations.
- [ ] Add cross-implementation test-vector format suitable for independent implementations.

## 1.5 Foundation exit criteria

Phase 1 is complete when:

- all foundation schemas have stable versioned public identifiers;
- canonical and reported quantities round-trip without loss of semantic form;
- exact values, ranges, qualified ranges, bounds, non-detects, and analytical limits remain distinct;
- reported statistics remain distinct from derived statistics;
- pH cannot be accidentally reduced to an arithmetic midpoint or mean;
- reporting bases and reference conditions can be represented without being hidden in unit strings;
- object and document references resolve under documented rules;
- unknown required extensions fail predictably;
- provenance and source-document metadata are reusable across domains;
- loss reports have a defined machine-readable structure;
- structural validation and semantic conformance are both testable;
- the foundation has enough implementation experience to support concrete domain schemas without repeated redesign.

---

# Phase 2 — Core Brewing and First Stable Release

**Goal:** Deliver a practical brewing-oriented FermentationJSON profile built on the shared foundation, with formal BeerJSON 1.0 compatibility and preservation-oriented BeerXML 1.0 import.

Development within this phase should be iterative. Pre-1.0 releases may expose pieces of the profile as they stabilize.

## 2.1 BeerJSON 1.0 compatibility baseline

BeerJSON compatibility should be developed **before or alongside** the brewing schemas, not bolted on afterward.

- [ ] Preserve a versioned copy/reference of the BeerJSON 1.0 specification used for compatibility work.
- [ ] Inventory all BeerJSON 1.0 object types and fields.
- [ ] Define FermentationJSON mappings for every BeerJSON 1.0 field.
- [ ] Preserve original BeerJSON values and units.
- [ ] Preserve identifiers and references.
- [ ] Preserve optional metadata.
- [ ] Preserve semantically meaningful ordering.
- [ ] Define unknown/extension-data handling.
- [ ] Build representative BeerJSON import fixtures.
- [ ] Build round-trip fixtures for the BeerJSON-representable subset.
- [ ] Build loss-report fixtures for FermentationJSON-to-BeerJSON export.
- [ ] Publish a versioned BeerJSON 1.0 compatibility profile.

**Compatibility gate:** every valid BeerJSON 1.0 document must be importable without loss of BeerJSON-defined information before FermentationJSON 1.0 compatibility is claimed.

## 2.2 Shared production schemas

- [ ] Material definition.
- [ ] Material lot.
- [ ] Planned material use.
- [ ] Actual material-use/consumption record.
- [ ] Culture definition.
- [ ] Culture lot or inoculum.
- [ ] Process definition.
- [ ] Process stage and step.
- [ ] Process execution.
- [ ] Deviations and interventions.
- [ ] Equipment definition.
- [ ] Equipment instance.
- [ ] Calculation/model-result integration.
- [ ] Basic batch genealogy needed by brewing v1.

## 2.3 Recipe and batch schemas

### Recipe

- [ ] Stable logical recipe identity.
- [ ] Exact recipe revision identity.
- [ ] Revision lineage.
- [ ] Planned ingredients/materials and quantities.
- [ ] Planned process.
- [ ] Targets and acceptable ranges.
- [ ] Expected yield/output.
- [ ] Scaling and derivation metadata.

### Batch

- [ ] Batch identity and lifecycle status.
- [ ] Exact recipe-revision reference.
- [ ] Planned versus actual dates.
- [ ] Actual material lots and quantities.
- [ ] Actual equipment instances.
- [ ] Process execution records.
- [ ] Measurements and observations.
- [ ] Deviations and interventions.
- [ ] Transfers.
- [ ] Yields and losses.
- [ ] Packaging output.
- [ ] Quality disposition.

**Invariant:** actual batch information must never overwrite recipe intent.

## 2.4 Brewing ingredients and cultures

- [ ] Fermentables.
- [ ] Hops and hop-derived products.
- [ ] Cultures.
- [ ] Miscellaneous ingredients.
- [ ] Processing aids and additives.
- [ ] Lot references.
- [ ] Producer/origin metadata.
- [ ] Analysis fields required for BeerJSON compatibility.
- [ ] Extensible analysis/property mechanism for richer FermentationJSON data.

## 2.5 Brewing process profile

- [ ] Mash.
- [ ] Boil.
- [ ] Fermentation.
- [ ] Conditioning.
- [ ] Transfer.
- [ ] Packaging.
- [ ] Ingredient additions and timing.
- [ ] Planned targets.
- [ ] Actual execution.
- [ ] Threshold/event-trigger representation where needed.

## 2.6 Water schemas

Water is an early pressure test of the foundation and should be implemented early in Phase 2.

### Source water

- [ ] SourceWaterProfile.
- [ ] Water identity and multiple physical sources.
- [ ] Source-document metadata integration.
- [ ] Profile timing and result-specific timing.
- [ ] Water stage and sampling context.
- [ ] Extensible analyte/property identifiers.
- [ ] Alkalinity, hardness, TDS, conductivity, and pH semantics.
- [ ] Chlorine, chloramine, and other disinfectant semantics.
- [ ] Regulatory/advisory references kept separate from measured chemistry.

### Targets and treatment

- [ ] TargetWaterProfile.
- [ ] Intended-water-use context.
- [ ] WaterBlend.
- [ ] TreatmentIngredient.
- [ ] TreatmentAddition.
- [ ] TreatedWater/TreatedLiquor state.
- [ ] WaterTreatmentPlan.
- [ ] Predicted versus measured treated-water distinction.
- [ ] Future-ready non-additive treatment-operation interface.

### Optimization and calculation interchange

- [ ] Multiple ranked candidate plans.
- [ ] Versioned named optimization policy.
- [ ] Explicit objective components.
- [ ] Constraint outcomes.
- [ ] Contribution matrix or equivalent structured explanation.
- [ ] Practical rounded doses distinct from ideal doses.
- [ ] Result-status vocabulary.
- [ ] Machine-readable infeasibility/warning explanations.
- [ ] Chemistry-model, policy, solver, reference-data, and adapter versions.
- [ ] Explicit indeterminate/insufficient-data results.

### Water conformance pressure tests

Implement the scientific pressure-test fixtures identified in the design, including:

- [ ] exact result;
- [ ] range plus independently reported average;
- [ ] `ND–11.1` qualified range;
- [ ] `<0.30` one-sided bound;
- [ ] `ND` without an invented analytical limit;
- [ ] RAA/LRAA/percentile/highest/lowest;
- [ ] result-specific timing;
- [ ] physical source versus report/document identity;
- [ ] water-stage context;
- [ ] separately reported alkalinity and bicarbonate;
- [ ] pH range with no invented midpoint;
- [ ] conductivity with and without reference temperature;
- [ ] chloride plus multiple disinfectant concepts;
- [ ] conflicting attributable target profiles;
- [ ] multi-source blend;
- [ ] hydrated versus anhydrous treatment ingredients;
- [ ] ranked optimization result;
- [ ] predicted versus measured treated water;
- [ ] BeerJSON export-loss report;
- [ ] reuse of one source profile under different intended-use contexts.

The Water Treatment interoperability handoff defines the detailed acceptance criteria for this work.

## 2.7 Equipment, packaging, styles, and basic calculations

- [ ] BeerJSON-compatible equipment representation.
- [ ] Vessel capacities and operational properties.
- [ ] Basic heating/cooling information.
- [ ] Packaging procedures and package types.
- [ ] Carbonation/conditioning representation.
- [ ] Beer styles and target specifications.
- [ ] Basic brewing calculations with explicit model provenance.

## 2.8 BeerXML 1.0 compatibility

- [ ] Define a versioned BeerXML 1.0 compatibility profile.
- [ ] Preserve all standard-defined information present in valid BeerXML 1.0 input.
- [ ] Preserve original values and units.
- [ ] Retain unknown application-specific elements opaquely where practical.
- [ ] Distinguish strict BeerXML 1.0 input from pragmatic compatibility mode.
- [ ] Report detected nonstandard behavior.
- [ ] Document information that cannot be reconstructed because the source file never contained it.
- [ ] Build import and preservation fixtures.

BeerXML compatibility is a migration requirement, not the architectural foundation for FermentationJSON.

## 2.9 Core brewing conformance suite

- [ ] Valid and invalid recipe fixtures.
- [ ] Valid and invalid batch fixtures.
- [ ] Planned-versus-actual semantic tests.
- [ ] Recipe revision immutability/reference tests.
- [ ] Material-definition versus lot tests.
- [ ] Equipment-definition versus instance tests.
- [ ] Process-definition versus execution tests.
- [ ] BeerJSON compatibility fixtures.
- [ ] BeerXML compatibility fixtures.
- [ ] Water scientific-pressure-test fixtures.
- [ ] Loss-report tests.
- [ ] Reference-integrity tests.
- [ ] At least one independent implementation or interoperability prototype.

## 2.10 First stable release gate

FermentationJSON 1.0 should not be declared stable until:

- foundation schemas and vocabularies have stable public identifiers;
- the brewing profile is complete enough for practical recipe and batch interchange;
- BeerJSON 1.0 lossless-import requirements are covered by published mapping and conformance fixtures;
- BeerXML 1.0 preservation behavior is documented and tested;
- scientific quantity semantics are covered by conformance fixtures;
- water objects pass the pressure-test cases;
- lossy export is always explicit;
- normative documentation and machine-readable schemas are consistent;
- migration and versioning guidance is published;
- at least one real implementation has exercised the principal workflows.

---

# Phase 3 — Engineering Extensions and Version 1.x Modules

**Goal:** Add richer production, laboratory, instrumentation, and engineering capabilities without destabilizing the core interchange model.

These capabilities should generally be optional modules or profiles unless implementation experience shows that a capability belongs in the shared core.

## 3.1 Laboratory and sampling

- sample identity and source;
- sampling point and method;
- chain of custody;
- laboratory and analyst;
- analytical method;
- instrument;
- uncertainty;
- detection/reporting/quantification limits;
- replicates;
- quality-control results;
- specification limits;
- pass/fail status;
- references to recognized or internal methods.

## 3.2 Rich process execution

- conditional steps;
- branches;
- repeated operations;
- parallel operations;
- threshold and sensor triggers;
- operator decisions;
- deviations;
- corrective actions;
- detailed event history.

## 3.3 Sensors and instruments

- sensor identity;
- channel identity;
- measurement range;
- accuracy and resolution;
- sampling rate;
- filtering/scaling;
- raw and processed values;
- quality flags;
- simulated versus physical data.

## 3.4 Calibration

- calibration standards;
- calibration points;
- coefficients;
- valid periods;
- operator;
- uncertainty;
- failures;
- adjustment history.

## 3.5 Telemetry

- time-series metadata;
- timestamped observations;
- raw and processed values;
- aggregation;
- data-quality flags;
- external dataset references;
- checksums;
- time basis;
- event annotations.

Large high-frequency datasets should normally remain external to ordinary recipe or batch documents.

## 3.6 Controllers and automation

- control-loop descriptions;
- setpoints;
- PID parameters;
- hysteresis;
- output ranges;
- actuators;
- manual override;
- alarms.

FermentationJSON data conformance must not be treated as executable safety logic. Physical-control systems require independent safety controls and authorization.

## 3.7 Advanced equipment

- ports and fittings;
- connections;
- valves and manifolds;
- pipes and hoses;
- pumps;
- flow paths;
- heating/cooling zones;
- calibrated vessel-volume tables;
- maintenance and calibration references;
- equipment topology.

## 3.8 Batch genealogy and traceability

- splits;
- combinations;
- blends;
- top-ups;
- dilution;
- partial transfers;
- losses;
- recovered material;
- culture propagation;
- barrel/vessel allocation;
- package allocation;
- parent-child batch relationships;
- packaging-material and process-aid traceability.

## 3.9 Serving-system engineering

Potential optional serving/draft module:

- beverage temperature and carbonation;
- carbonation-maintenance pressure;
- dispensing pressure;
- line material and inside diameter;
- length and elevation;
- fittings and components;
- predicted flow;
- alternative balancing solutions;
- assumptions and constraints;
- multi-tap system planning.

Carbonation-maintenance pressure and dispensing-path resistance must remain separate engineering concepts.

## 3.10 Attachments and richer records

- laboratory reports;
- certificates of analysis;
- photographs;
- graphs;
- equipment manuals;
- water reports;
- competition score sheets;
- telemetry exports;
- external URIs;
- MIME types;
- checksums;
- richer sensory evaluations.

---

# Phase 4 — Additional Fermentation Domains

**Goal:** Reuse the foundation and production architecture across additional fermentation domains instead of creating isolated formats.

A new domain should become a profile only after its requirements have been pressure-tested against real workflows and source data.

## 4.1 Wine

Potential profile areas include:

- grape variety and clone;
- vineyard/block/appellation/vintage;
- harvest and fruit chemistry;
- crushing, destemming, pressing;
- maceration and skin contact;
- cap management;
- malolactic fermentation;
- oak and maturation;
- blending;
- stabilization, fining, filtration;
- wine-specific analysis and style data.

## 4.2 Cider and perry

Potential areas include:

- apple and pear varieties;
- orchard and harvest;
- milling and pressing;
- juice yield;
- sugar, acid, and tannin classification;
- keeving;
- chaptalization;
- blending;
- bottle conditioning;
- cider and perry styles.

## 4.3 Mead

Potential areas include:

- honey variety and floral source;
- origin and harvest;
- must preparation;
- nutrient schedules;
- staggered nutrient additions;
- degassing;
- fruit, spice, and botanical additions;
- mead styles.

## 4.4 Sake

Potential areas include:

- rice variety;
- polishing ratio;
- washing, soaking, steaming, and cooling;
- kōji;
- shubo/yeast starter;
- sandan-jikomi;
- moromi;
- pressing;
- filtration;
- pasteurization;
- dilution;
- sake-specific measurements and styles.

## 4.5 Kombucha and cultured beverages

Potential areas include:

- tea and sugar source;
- culture/SCOBY;
- primary and secondary fermentation;
- flavor additions;
- acidity;
- carbonation;
- microbial-quality information.

## 4.6 Future profiles

Possible future domains include:

- vinegar;
- other fermented foods;
- nonalcoholic fermented beverages;
- mixed-fermentation products;
- pre-distillation fermentation;
- research fermentation;
- additional fermentation domains demonstrated by implementation need.

---

# Cross-cutting work

The following activities span multiple phases.

## Documentation

- [ ] Keep `README.md` aligned with implemented capabilities.
- [ ] Keep `docs/design/DESIGN.md` synchronized with accepted architectural changes.
- [ ] Record durable architectural decisions as ADRs.
- [ ] Publish normative specification text separately from implementation notes when the release process stabilizes.
- [ ] Add migration guidance before stable releases.
- [ ] Maintain examples that are understandable without reading the entire schema tree.

## Compatibility

- [ ] Keep compatibility behavior versioned.
- [ ] Maintain lossless-import guarantees with fixtures.
- [ ] Maintain explicit loss reports for lossy exports.
- [ ] Never silently reinterpret source data to satisfy a target format.

## Testing

- [ ] Test schemas themselves against Draft 2020-12.
- [ ] Maintain positive and negative structural fixtures.
- [ ] Maintain semantic conformance tests.
- [ ] Add compatibility round-trip fixtures.
- [ ] Add scientific edge-case fixtures.
- [ ] Add cross-language conformance vectors as independent implementations appear.

## Governance and proposals

- [ ] Use `proposals/` for substantial experimental ideas that are not ready to become normative.
- [ ] Require interoperability rationale and compatibility analysis for major schema changes.
- [ ] Require migration behavior for promoted experimental features.
- [ ] Keep experimental identifiers distinct from stable normative identifiers.

---

# Deferred design topics

These topics are intentionally not release blockers for the current foundation or core brewing work unless implementation experience demonstrates otherwise:

- JSON-LD integration;
- formal ontology integration;
- digital signatures beyond basic integrity references;
- multi-document packaging/container format;
- embedded binary attachment strategy;
- high-frequency streaming telemetry format;
- advanced vocabulary registry/governance infrastructure;
- long-term archival profile;
- advanced optimization-engine standardization;
- AI-assisted recommendations.

They should remain proposals or design notes until a concrete interoperability requirement justifies standardization.

---

# Immediate next work

The next development sequence is:

1. **Foundation semantic conformance**
   - reference integrity and unresolved-reference failures;
   - source-reported versus derived-data invariants;
   - representative loss-report transformations;
   - machine-readable conformance-suite versioning;
   - cross-implementation test-vector structure.

2. **BeerJSON 1.0 compatibility inventory and mapping**
   - begin before the brewing object model is considered stable.

3. **First concrete domain schemas**
   - shared materials/cultures/process/equipment;
   - recipe and batch;
   - water schemas as an early scientific pressure test.

This sequence may be adjusted when implementation reveals a dependency, but new work should not bypass unresolved foundation semantics merely to increase schema count.

---

# Milestone summary

| Milestone | Status | Exit signal |
|---|---|---|
| Architecture and design review | Complete | Main design and initial ADRs accepted |
| Initial foundation schemas | Complete | Core schemas and positive/negative fixtures validate |
| Foundation stabilization | In progress | Units, IDs, loss reporting, semantic conformance complete |
| BeerJSON compatibility baseline | Not started | Complete mapping and import fixtures |
| Core brewing schemas | Not started | Recipes, batches, materials, processes, equipment, water implemented |
| BeerXML compatibility | Not started | Preservation profile and fixtures implemented |
| First stable FermentationJSON release | Future | Published schemas, profiles, mappings, conformance suite |
| Engineering modules | Future | Optional v1.x capabilities implemented as needed |
| Additional fermentation domains | Future | Pressure-tested domain profiles |

---

## Definition of progress

FermentationJSON should measure progress by **interoperable behavior**, not by schema count.

A capability is meaningfully complete when:

- its semantics are documented;
- its machine-readable schema exists where applicable;
- representative valid examples exist;
- meaningful invalid examples exist;
- semantic invariants are tested;
- compatibility consequences are understood;
- independent implementations can interpret the same data consistently.

