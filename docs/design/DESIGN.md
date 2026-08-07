# FermentationJSON Design Specification

**Status:** Working Draft  
**Document version:** 0.5  
**Repository path:** `docs/design/DESIGN.md`

---

## 1. Purpose

FermentationJSON defines a language-independent and platform-independent JSON interchange standard for fermentation data.

The specification defines data structures, validation requirements, compatibility behavior, and conformance requirements for exchanging recipes, production records, ingredients, equipment, processes, calculations, measurements, and related metadata.

FermentationJSON is intended for file exchange, APIs, archival records, reference libraries, validation workflows, and production systems. It does not prescribe an application's internal database schema, object model, user interface, or implementation language.

## 2. Scope

### 2.1 Initial specification scope

The initial specification consists of reusable, domain-neutral foundation schemas and a brewing-oriented profile.

Initial scope includes:

- document metadata;
- identifiers and references;
- quantities and measurements;
- canonical and reported representations;
- ranges, bounds, estimates, and uncertainty;
- provenance;
- recipes and executed production batches;
- ingredients, cultures, material lots, and basic inventory references;
- equipment;
- process definitions and execution records;
- water profiles, blending, and treatment;
- calculation results;
- compatibility and loss reports;
- external-format compatibility profiles;
- profile and extension mechanisms.

### 2.2 Planned extension scope

Later profiles and optional modules may define:

- laboratory and sampling data;
- sensors, calibration, telemetry, and automation;
- detailed equipment topology;
- batch genealogy and traceability;
- serving and draft-system engineering;
- richer sensory and quality records;
- wine, cider, perry, mead, sake, kombucha, vinegar, and other fermentation domains.

Planned scope does not create a requirement for all listed capabilities to appear in one schema or release.

### 2.3 Non-goals

FermentationJSON does not define:

- an application's internal persistence model;
- executable equipment-control logic or a safety-control protocol;
- accounting, payroll, or general-purpose enterprise resource planning;
- complete laboratory information management;
- full supply-chain or customer-relationship management;
- proprietary user-interface state;
- a binary storage format for high-frequency telemetry;
- a required dependency on a specific implementation or unit library.

Applications MAY maintain private or application-specific data outside FermentationJSON. Such data is not interoperable unless represented through a conforming extension.

## 3. Normative language

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**, **SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **NOT RECOMMENDED**, **MAY**, and **OPTIONAL** in this document are to be interpreted as described in BCP 14, RFC 2119 and RFC 8174, when and only when they appear in all capitals.

Text that does not use these terms is informative unless a section explicitly states otherwise. Examples and rationale are informative and do not override normative requirements.

## 4. Design principles

### 4.1 Information preservation

A conforming transformation MUST preserve all information required by the applicable schema or compatibility profile.

An importer or exporter MUST NOT silently omit, reinterpret, or approximate required information. A transformation that cannot preserve all required information MUST fail explicitly or produce a loss report as specified by the applicable profile.

### 4.2 Explicit semantics

Physical units MUST NOT be used as substitutes for chemical identity, reporting basis, hydration state, analytical method, reference conditions, measurement status, or other semantic qualifiers.

Where such distinctions affect interpretation, they MUST be represented explicitly.

### 4.3 Recipe and batch separation

A recipe describes intended formulation and procedure. A batch describes an executed production run.

FermentationJSON MUST represent recipes and batches as distinct concepts. A batch MAY reference the recipe or recipe revision from which it was executed.

Planned and actual values MUST remain distinguishable.

### 4.4 Modular composition

FermentationJSON MUST use modular schemas composed from reusable definitions.

Core schemas SHOULD contain only concepts that are broadly reusable across fermentation domains. Domain-specific requirements SHOULD be defined by profiles or optional modules.

### 4.5 Versioned compatibility

A normative compatibility claim with an external format MUST be defined by a versioned compatibility profile.

The profile MUST define the applicable format version, mappings, preservation requirements, export behavior, round-trip expectations, known limitations, conformance fixtures, and loss-reporting behavior.

### 4.6 Provenance

The data model MUST permit provenance to be associated with documents, imported values, measurements, calculations, historical records, and published reference data.

Profiles SHOULD require provenance where source identity or method is necessary for interpretation, reproducibility, or audit.

### 4.7 Controlled extensibility

The specification MUST provide an extension mechanism that prevents naming collisions.

An extension MUST NOT redefine the meaning of a normative field, bypass a required validation rule, or claim conformance to a profile that it violates.

### 4.8 Managed evolution

The specification MUST define versioning, compatibility, deprecation, and migration rules for normative artifacts.

Published identifiers MUST NOT be reassigned to incompatible definitions.

## 5. Implementation independence

Normative FermentationJSON artifacts define serialization, validation, unit identifiers, interpretation, and conformance independently of any implementation.

A conforming implementation MAY use any programming language, schema validator, unit library, database, or storage architecture that correctly implements the normative requirements.

Conformance is determined by externally observable behavior and valid output, not by an implementation's internal data model.

Normative behavior MUST NOT depend on undocumented behavior in a particular library or application. Reference implementations MAY demonstrate expected behavior but do not override the normative specification.

## 6. Specification organization

FermentationJSON is organized into the following classes of artifacts:

1. **Core schemas**  
   Document metadata, identity, references, quantities, measurements, provenance, extensions, and common reporting structures.

2. **Shared production schemas**  
   Recipes, batches, materials, processes, events, calculations, equipment, and other domain-neutral production concepts.

3. **Domain profiles**  
   Requirements and constraints for beer and later fermentation domains.

4. **Optional capability modules**  
   Independently adoptable capabilities such as water treatment, laboratory records, telemetry, serving systems, controllers, and advanced equipment.

5. **Compatibility profiles**  
   Versioned mappings and conformance requirements for external interchange formats.

6. **Versioned vocabularies**  
   Controlled identifiers and terms referenced by schemas and profiles.

A document MAY conform to one or more compatible profiles or modules. Each normative artifact MUST identify its version and status.

If normative artifacts conflict, the applicable release documentation MUST define precedence. An implementation MUST NOT infer precedence from repository location or filename alone.

## 7. Document architecture

### 7.1 General requirements

Every FermentationJSON document MUST declare:

- the FermentationJSON specification version;
- the document type;
- the normative schema or profile identifier used for validation;
- a stable document identifier.

A document MUST NOT require interpretation as a recipe unless its declared document type or profile defines it as one.

A document SHOULD include:

- a creation timestamp when known;
- a title or concise description when meaningful;
- the generating software and software version when software generated the document.

A document MAY include:

- a modification timestamp;
- author or responsible organization;
- language and locale;
- license and copyright information;
- tags or classifications;
- revision history;
- citations;
- parent and source relationships;
- checksums or signatures;
- extensions;
- warnings and loss reports.

When both creation and modification timestamps are present, the modification timestamp MUST NOT precede the creation timestamp.

### 7.2 Imported-source metadata

A document created by importing another format MUST identify:

- the source format;
- the source-format version when known;
- the importer identity and version;
- the import timestamp.

The importer SHOULD preserve source field paths, source identifiers, and source-document integrity information when they are available and useful for traceability.

Unknown source-format extensions MUST be handled as required by the applicable compatibility profile.

### 7.3 Document types

The architecture MUST support multiple document types and MUST NOT assume that all conforming documents contain the same root content.

The initial specification is expected to define document types for:

- recipe;
- batch;
- reference library;
- compatibility or loss report;
- calculation result;
- equipment profile;
- water profile;
- process profile;
- measurement collection.

Profiles MAY define additional document types. The normative schema for a document type MUST define its required root content.

## 8. Identifiers and references

### 8.1 Document identifiers

Every FermentationJSON document MUST have a stable identifier.

A document identifier MUST be globally unique, MUST NOT be reassigned to a different logical document, and SHOULD use a URI-compatible form. A UUID URN is an acceptable identifier.

A new revision MAY retain the same logical-document identifier only when the applicable revision policy defines the revisions as versions of the same resource. Otherwise, it MUST receive a new identifier.

### 8.2 Object identifiers

An object that is the target of a reference MUST have an identifier.

An object identifier MUST be unique within the document unless the applicable profile defines a broader scope. Identifiers SHOULD remain stable across serialization and round-trip conversion.

Embedded objects that cannot be referenced independently MAY omit identifiers unless required by their schema or profile.

### 8.3 Internal references

An internal reference MUST identify its target unambiguously within the document.

If a reference declares an expected target type, the referenced object MUST satisfy that type.

A validator or processor MUST report an error when a required internal reference cannot be resolved.

### 8.4 External references

An external reference MUST include a target URI or other globally unique identifier.

An external reference MAY include:

- an expected target type;
- an expected schema, profile, or version;
- a media type;
- a checksum or other integrity information;
- a human-readable label.

External references MAY remain unresolved during structural validation unless the applicable profile requires dereferencing.

For archival or reproducibility use cases, integrity information SHOULD be included when the referenced content is expected to remain unchanged.

### 8.5 Identity and content equivalence

Two objects with different identifiers MUST NOT be assumed to represent the same logical object solely because their serialized content is equal.

Two references to the same identifier assert identity of the referenced logical object unless the applicable profile defines version-specific semantics.

Copying an object does not preserve identity unless its identifier and revision rules explicitly state that it remains the same logical object.

---

## 9. Universal quantity model

### 9.1 Purpose

The quantity model preserves the scientific meaning of a quantity while providing a normalized representation for interoperability.

A quantity may contain several independent dimensions of information:

- a canonical representation;
- an optional reported representation;
- value form, such as exact value, bound, range, or non-detect;
- source or derivation status;
- uncertainty or statistical summary;
- chemical or reporting basis;
- reference conditions;
- provenance.

These dimensions MUST NOT be collapsed into a single unit string or scalar value when doing so would change meaning.

### 9.2 Canonical representation

Every quantity object MUST include a canonical representation.

The canonical representation is the normalized representation used for interoperable validation, comparison, and calculation. It MUST use units, reporting bases, and identifiers defined or permitted by the applicable FermentationJSON schema, profile, or versioned vocabulary.

Canonicalization MUST preserve the semantic form of the source quantity. In particular:

- an exact value MUST remain an exact value;
- an approximate value MUST remain approximate;
- a one-sided bound MUST remain a one-sided bound;
- a range MUST remain a range;
- a non-detect MUST NOT be converted to zero;
- a non-detect without a stated numerical limit MUST NOT be assigned an invented numerical limit.

A canonical representation therefore need not be a single scalar. It MAY represent a bound, interval, statistical summary, or other quantity form defined by the applicable schema.

The canonical representation does not imply that a quantity is exact, directly measured, authoritative, representative, or free from uncertainty.

### 9.3 Reported representation

A quantity MAY include a reported representation.

A reported representation SHOULD be included when the quantity originated from:

- user input;
- an imported document;
- an instrument;
- a laboratory result;
- a product label;
- a publication;
- a historical record;
- another identifiable source representation.

The reported representation MAY preserve:

- the reported value or values;
- the reported unit;
- original text;
- decimal precision;
- significant figures;
- formatting;
- locale;
- reporting basis;
- source qualifiers or symbols.

The reported representation MAY be identical to the canonical representation when preserving the source form remains relevant.

An implementation MUST NOT fabricate a reported representation when no original reported representation existed.

Canonicalization MUST NOT overwrite, replace, or reinterpret the reported representation.

### 9.4 Representation and derivation are independent

`canonical` and `reported` describe representations of a quantity. They do not by themselves state whether a value came from a source or was derived.

The data model MUST distinguish source-supplied information from derived information.

Derived information includes values produced by:

- unit-independent mathematical derivation;
- interpolation;
- midpoint calculation;
- averaging or aggregation not explicitly reported by the source;
- chemical conversion or estimation;
- predictive models;
- optimization;
- inference.

A derived value MUST identify its derivation method or calculation provenance when the derivation affects scientific interpretation.

A derived value MUST NOT be serialized as though it had been reported by the source.

### 9.5 Value forms

The quantity model MUST support, as applicable:

- exact values;
- approximate values;
- lower bounds;
- upper bounds;
- open and closed bounds;
- numerical ranges;
- non-detects;
- detection limits;
- quantification limits;
- uncertainty;
- tolerance;
- confidence intervals;
- source-reported summary statistics.

The representations of these forms MUST remain distinguishable.

A range or bound endpoint MAY itself carry a qualifier when required to preserve source meaning.

### 9.6 Non-detects and analytical limits

A non-detect is a statement about an analytical result and is not numerically equivalent to zero.

If a source reports only a non-detect, FermentationJSON MUST preserve the non-detect without inventing a detection limit.

If a detection limit or quantification limit is explicitly reported, it SHOULD be preserved separately from the result status.

A statement such as "ND", "<5", and "0" therefore represents three different conditions and MUST NOT be treated as interchangeable.

### 9.7 Reported statistics and derived statistics

A statistical value MUST identify the statistic it represents when that distinction is material.

Examples include:

- average or mean;
- median;
- minimum;
- maximum;
- percentile;
- standard deviation;
- confidence interval.

An average explicitly supplied by a source MAY be preserved as a reported average.

A value calculated by an importer or consuming application MUST NOT be labeled or represented as a reported average.

Reported minimum and maximum values over an observation period MUST NOT automatically be interpreted as uncertainty bounds, specification limits, or confidence limits.

### 9.8 Representative calculation values

Some applications require a single representative scalar for calculations even when the source supplies multiple values or a range.

For linearly scaled quantities, an applicable profile MAY define a default representative-value policy. Unless the profile specifies otherwise, the recommended precedence is:

1. an average explicitly reported by the source;
2. an exact reported value;
3. an on-demand midpoint of a numerical minimum/maximum range.

A midpoint calculated from a range is derived information. It MUST NOT be serialized as a reported value or reported average.

A representative value derived for calculation MUST NOT replace the preserved source range or source statistics.

Profiles MAY prohibit automatic representative-value derivation for particular quantity kinds.

### 9.9 Logarithmic quantities

A profile defining a logarithmic quantity MUST specify whether and how representative values, aggregation, interpolation, and uncertainty are calculated.

For pH:

- exact values, ranges, bounds, and explicitly reported averages MUST be preserved as supplied;
- an arithmetic midpoint or arithmetic mean of pH values MUST NOT be used as an automatic representative value;
- a pH range alone has no automatic representative calculation value;
- a derived aggregate pH, when required, MUST use an explicitly documented model operating in hydrogen-ion activity space, or in concentration space when that approximation is explicitly stated;
- a derived aggregate MUST NOT be represented as a reported average.

### 9.10 Reference conditions

A quantity MAY include conditions such as:

- reference temperature;
- measurement temperature;
- pressure;
- atmospheric pressure;
- sample state;
- dry basis;
- wet basis;
- mass basis;
- volume basis;
- density assumption;
- dissolved-gas state.

A profile MUST require reference conditions when omission would make the quantity ambiguous or materially change its interpretation.

An implementation MUST NOT invent an unstated reference condition merely to complete a conversion.

### 9.11 Chemical identity and reporting basis

Chemical identity and reporting basis MUST be represented separately from the physical unit when required for correct interpretation.

Examples include:

- alkalinity reported as CaCO3;
- hardness reported as CaCO3;
- concentration reported as an ion;
- concentration reported as an element;
- percent by mass;
- percent by volume;
- mass per volume;
- hydrated versus anhydrous chemical additions.

Dimensionally compatible representations MUST NOT be treated as semantically interchangeable when their chemical or reporting bases differ.

A conversion or estimate between chemically different reporting forms MUST be represented as derived information and MUST identify the assumptions or chemical model used.

Implementations MAY use external unit libraries for parsing, conversion, validation, and display. Normative unit identifiers and semantics remain defined by FermentationJSON artifacts.

## 10. Measurements and observations

### 10.1 Measurement record

A measurement or observation SHOULD identify:

- the property or analyte;
- the result;
- the subject, material, or sample;
- the observation time or observation period when known;
- provenance;
- measurement or reference conditions when relevant.

A report publication date MUST NOT be used as a substitute for an observation date or observation period.

### 10.2 Temporal applicability

The data model MUST be able to distinguish:

- a single observation time or date;
- an observation period;
- a report or publication date;
- a profile intended to represent typical, historical, reference, or otherwise aggregated conditions.

Where a schema provides both a single observation field and an observation-period field, they SHOULD be mutually exclusive unless the profile defines a specific combined meaning.

An observation period SHOULD identify its start and end when known.

### 10.3 Result status

A measurement result MAY carry status including:

- valid;
- invalid;
- missing;
- not detected;
- below detection limit;
- below quantification limit;
- above instrument range;
- provisional;
- verified;
- rejected.

Status and numeric value MUST remain distinct concepts.

### 10.4 Measurements versus derived results

A source measurement, observation, or explicitly reported statistic MUST remain distinguishable from a value calculated or inferred by an importer or consuming application.

A directly observed or instrument-derived result MUST NOT be represented as a calculation result merely because software converted its unit or canonicalized its representation.

A value produced by a scientific model, interpolation, aggregation, conversion between chemical reporting bases, optimization, or other derivation MUST identify its calculation or derivation provenance.

### 10.5 Measurement conditions

When a result depends materially on conditions such as temperature, pressure, sample preparation, analytical basis, or instrument configuration, those conditions SHOULD be preserved.

A reference condition SHOULD be omitted rather than guessed when the source does not provide it, unless a governing analytical method or profile supplies a normative default.

### 10.6 Time series

Compact time series MAY be embedded.

Large or high-frequency time series SHOULD be referenced as external datasets with metadata including:

- format;
- location;
- checksum;
- time basis;
- measured channels;
- units;
- sampling interval;
- quality flags.

## 11. Provenance

### 11.1 General requirements

The provenance model MUST permit provenance to be attached to documents, objects, measurements, quantities, calculations, statistical summaries, derived values, and imported source fragments.

Provenance SHOULD identify, where applicable:

- source document;
- source location or field;
- person;
- organization;
- laboratory;
- instrument;
- analytical method;
- software;
- software version;
- formula or model;
- citation;
- timestamp;
- sample;
- confidence;
- verification status.

### 11.2 Source types

The provenance model SHOULD support at least:

- published source;
- book;
- journal;
- website;
- government or municipal report;
- manufacturer specification;
- certificate of analysis;
- laboratory report;
- personal observation;
- user entry;
- instrument result;
- imported software record;
- historical record.

Derived or reconstructed values SHOULD identify the source information from which they were derived when traceable.

### 11.3 Imported data

Imported data MUST preserve the source format and source-format version when known.

An importer SHOULD preserve source paths, source field names, source text, page or table references, or other locators when useful for verification.

Canonicalization during import MUST NOT erase the source representation.

### 11.4 Automated extraction and interpretation

Automated extraction from documents, images, PDF files, natural-language reports, or other semi-structured sources MAY be used as an ingestion aid.

Automatically extracted or interpreted data SHOULD retain:

- the original source reference;
- a locator to the supporting source material when practical;
- the extraction software or method;
- extraction or review status;
- warnings or confidence information where available.

A system MUST NOT represent an inferred or guessed value as though it were explicitly reported by the source.

If automated extraction cannot determine a value, unit, reporting basis, qualifier, or reference condition with sufficient confidence, the unresolved information SHOULD remain unresolved pending review rather than being silently inferred.

### 11.5 Derived and calculated data

A derived or calculated value SHOULD record, as applicable:

- derivation or calculation type;
- source inputs;
- outputs;
- formula or model identifier;
- formula or model version;
- software;
- software version;
- assumptions;
- coefficients;
- constraints;
- warnings;
- rounding;
- timestamp.

A transformation that changes chemical meaning or reporting basis MUST document the model and assumptions used.

---

## 12. Recipes

### 12.1 Definition

A recipe describes intended formulation, materials, process, and target outcomes.

A recipe MUST NOT use batch-execution fields to represent observations of what actually occurred.

A recipe SHOULD support:

- a stable logical recipe identity;
- a revision identifier or revision relationship;
- planned ingredient or material uses;
- planned quantities;
- planned process definitions;
- target values and acceptable ranges;
- expected yield or output;
- tolerances;
- scaling information;
- provenance.

Targets and expected outcomes are specifications or predictions, not measurements.

### 12.2 Recipe revisions

A recipe revision MUST be distinguishable from other revisions of the same logical recipe.

When a recipe revision is referenced by a batch, the reference MUST identify the exact revision used.

A published or otherwise fixed recipe revision SHOULD be immutable. A substantive change to an immutable revision SHOULD produce a new revision.

A revision MAY identify:

- its parent revision;
- the reason for revision;
- the author or software that produced it;
- the revision timestamp;
- source publications or external references.

### 12.3 Derived and scaled recipes

A recipe MAY be derived, cloned, translated, or scaled from another recipe.

A derived or scaled recipe SHOULD preserve:

- the source recipe and revision;
- the transformation or scaling method;
- relevant assumptions;
- the resulting planned values.

Scaling or derivation MUST NOT alter the preserved source revision.

### 12.4 Ingredient and material use

A recipe SHOULD distinguish an ingredient or material definition from its planned use in the recipe.

A planned use MAY include:

- a reference to the ingredient or material;
- planned quantity;
- process stage or step;
- timing or trigger;
- purpose;
- preparation or form;
- addition-specific instructions.

A recipe MAY embed a material definition or reference an external definition as permitted by the applicable profile.

---

## 13. Batches and production records

### 13.1 Definition

A batch is a production record for a specific execution of a recipe, process, or ad hoc production plan.

A batch MUST remain distinct from the recipe or process definition from which it was executed.

A batch SHOULD identify:

- batch identifier;
- lifecycle status;
- recipe revision or process reference when applicable;
- scheduled dates when applicable;
- actual start and completion dates when known;
- responsible operators or organization;
- actual material lots and quantities used;
- equipment instances used;
- process execution records;
- measurements and observations;
- deviations and interventions;
- transfers;
- yields and losses;
- packaging output;
- quality disposition.

A batch MAY exist without a recipe reference when the production run was not executed from a formal recipe.

### 13.2 Recipe and process references

When a batch was executed from a recipe, the batch SHOULD reference the exact recipe revision.

For reproducibility, a batch SHOULD preserve sufficient information to identify the referenced revision even if the recipe is stored externally. This MAY include a persistent identifier, version, checksum, or embedded snapshot.

A batch MUST NOT silently follow later changes to a mutable recipe reference.

### 13.3 Planned and actual information

Planned and actual information MUST remain distinguishable.

An implementation MUST NOT overwrite a planned value with an actual value or replace a source observation with a target value.

Actual quantities and conditions SHOULD be represented as measurements, observations, material-use records, process-execution records, or derived results according to their meaning.

### 13.4 Lifecycle status

A batch MAY have lifecycle states such as:

- planned;
- scheduled;
- in progress;
- completed;
- aborted;
- rejected;
- archived.

A lifecycle state MUST NOT imply that required measurements or process steps occurred unless those records are present.

### 13.5 Deviations and interventions

A production record SHOULD be able to represent a deviation or intervention with:

- the affected process step or condition;
- the planned state or target;
- the observed or actual state;
- time;
- reason;
- responsible person or system;
- corrective action;
- outcome.

A deviation or intervention SHOULD reference the underlying measurements or events rather than duplicating them when practical.

### 13.6 Batch genealogy

A batch MAY reference parent or child production records.

Profiles or optional modules MAY define:

- splits;
- combinations;
- blends;
- top-ups;
- dilution;
- partial transfers;
- recovered material;
- barrel allocation;
- package allocation;
- other material transformations.

Genealogy relationships SHOULD preserve source quantities and destination quantities where known.

---

## 14. Process model

### 14.1 Process definitions and executions

FermentationJSON MUST distinguish a process definition from a process execution.

A process definition describes intended operations, sequence, targets, conditions, and triggers.

A process execution records the operations and events that actually occurred.

A process execution MAY reference a process definition or a specific process step.

### 14.2 Process structure

A process definition SHOULD support:

- process;
- stage;
- step;
- operation;
- instruction;
- target;
- condition;
- trigger;
- duration;
- input;
- output;
- dependency;
- resource.

A step that may be referenced independently SHOULD have a stable identifier within the process definition.

### 14.3 Ordering and dependencies

A process definition MAY express:

- ordered steps;
- dependencies;
- repeated operations;
- optional operations;
- conditional operations;
- parallel operations.

Profiles MAY restrict these capabilities to a simpler subset.

A dependency MUST identify its prerequisite unambiguously.

### 14.4 Timing and triggers

A planned process step MAY be triggered by:

- elapsed time;
- absolute time;
- completion of another step;
- temperature threshold;
- gravity or extract threshold;
- pH threshold;
- pressure threshold;
- volume threshold;
- flow threshold;
- sensor condition;
- operator decision;
- calculated progress.

The planned trigger and the actual event that satisfied or bypassed the trigger MUST remain distinguishable.

### 14.5 Process execution

A process execution MAY record:

- referenced process definition or step;
- actual start and end;
- actual duration;
- setpoints;
- measured conditions;
- completion state;
- equipment instance;
- operator or controlling system;
- deviations;
- interventions;
- notes;
- related measurements and events.

Observed trajectories are measurements or time-series data and SHOULD be referenced rather than encoded as target values.

### 14.6 Operations

Profiles MAY define controlled operation vocabularies including:

- cleaning;
- sanitizing;
- milling;
- crushing;
- destemming;
- pressing;
- lautering;
- sparging;
- heating;
- cooling;
- boiling;
- holding;
- mixing;
- pumping;
- transfer;
- oxygenation;
- aeration;
- degassing;
- inoculation;
- fermentation;
- conditioning;
- filtration;
- clarification;
- fining;
- stabilization;
- blending;
- maturation;
- aging;
- carbonation;
- packaging;
- pasteurization;
- sampling.

Operation vocabularies SHOULD be extensible without requiring changes to unrelated core schemas.

---

## 15. Ingredients, materials, and lots

### 15.1 Material definitions

A material definition describes the identity and relatively stable characteristics of a material.

A material definition SHOULD support, as applicable:

- identifier;
- name;
- category and subtype;
- producer or manufacturer;
- product identifier;
- biological or chemical identity;
- geographic origin;
- crop or production year;
- form;
- processing method;
- composition;
- specification or typical analysis;
- allergens;
- certifications;
- storage requirements;
- shelf life;
- provenance.

Supplier, purchasing, cost, and inventory state are not intrinsic material identity and SHOULD be represented separately when needed.

### 15.2 Material lots

A material lot represents a specific produced, received, harvested, propagated, or otherwise traceable quantity of a material.

A lot SHOULD support, as applicable:

- lot identifier;
- material definition reference;
- producer or supplier lot code;
- production, harvest, or receipt date;
- lot-specific analysis;
- quantity;
- storage condition;
- expiration or best-use date;
- quality status;
- provenance.

Lot-specific analysis MUST remain distinguishable from a material specification or typical analysis.

### 15.3 Ingredient and process roles

A material's use as an ingredient, processing aid, cleaning agent, treatment chemical, packaging material, or other process input is a contextual role and SHOULD NOT require redefining the material itself.

Profiles MAY define specialized material types for:

- fermentables;
- hops and hop-derived products;
- cultures;
- fruit;
- juice and must;
- honey;
- rice;
- botanicals;
- enzymes;
- nutrients;
- finings and clarifiers;
- preservatives;
- acids and bases;
- salts;
- gases;
- cleaning or sanitizing agents;
- processing aids.

### 15.4 Planned and actual material use

A recipe SHOULD reference planned material uses.

A batch SHOULD reference actual material lots and quantities where traceability is required.

A planned material use and an actual material consumption record MUST remain distinguishable.

---

## 16. Cultures and microbiology

### 16.1 Culture definitions

A culture definition describes a microbial culture, commercial culture product, strain, defined blend, mixed culture, spontaneous culture, or other inoculum class.

A culture definition SHOULD support, where known:

- organism species;
- subspecies;
- strain;
- taxonomic identifier;
- commercial strain or product name;
- producer;
- product identifier;
- culture type;
- defined composition;
- expected attenuation or fermentation characteristics;
- recommended temperature range;
- alcohol tolerance;
- flocculation or equivalent behavior;
- provenance.

A culture record MUST NOT imply known taxonomic identity or composition when the culture is spontaneous, unknown, or incompletely characterized.

### 16.2 Culture lots and inocula

Lot- or inoculum-specific properties SHOULD be represented separately from stable culture-definition properties.

Such properties MAY include:

- lot identifier;
- cell concentration;
- viability;
- vitality;
- generation number;
- harvest count;
- storage age;
- storage medium;
- storage temperature;
- propagation history;
- contamination status;
- analysis date;
- provenance.

Viability, cell concentration, and similar condition-dependent values SHOULD be represented as measurements or observations with their temporal context.

### 16.3 Mixed and spontaneous cultures

A defined mixed culture MAY identify component organisms and proportions when known.

An undefined or spontaneous culture MAY identify known components without implying that the list is complete.

Component proportions MUST NOT be invented when they are unknown.

---

## 17. Water profiles and treatment

### 17.1 Water object types

The water model MUST distinguish:

- source-water profile;
- target-water profile;
- treated-liquor profile;
- water blend;
- water-treatment plan.

These object types represent different states or purposes and MUST NOT be treated as semantically equivalent.

### 17.2 Source-water identity

A source-water profile SHOULD support distinct fields for:

- provider or utility;
- brand or product, where applicable;
- physical source or source system, where known;
- source type;
- geographic area;
- treatment plant or bottling location;
- report title;
- report date;
- observation date or observation period;
- laboratory or reporting organization;
- citation;
- provenance.

Provider, brand or product, source type, and physical source MUST NOT be treated as interchangeable concepts.

Source types MAY include:

- municipal;
- well;
- spring;
- rainwater;
- reverse osmosis;
- distilled;
- bottled;
- laboratory-prepared;
- process water;
- reused water;
- blended water.

### 17.3 Temporal basis and profile character

A source-water profile MUST be able to distinguish a single observation from an observation period.

A single observation date and an observation period SHOULD be mutually exclusive.

The profile MAY identify itself as:

- observed;
- period summary;
- typical;
- representative;
- seasonal;
- historical;
- reference.

A report date MUST remain distinct from the period or date represented by the chemistry.

### 17.4 Source-reported chemistry

Source-water chemistry MUST preserve source-reported semantics.

For an analyte or property, a source profile MAY contain:

- an exact reported value;
- a reported minimum and maximum;
- a one-sided reported bound;
- a non-detect;
- an explicitly reported average;
- other explicitly identified reported statistics.

A derived midpoint, converted chemical species concentration, inferred reference condition, or other calculated value MUST NOT be serialized as source-reported data.

For linearly scaled quantities, software MAY derive a representative scalar according to the policy in Section 9.8. That value remains derived.

For pH, the restrictions in Section 9.9 apply.

### 17.5 Chemistry

The schema SHOULD support common brewing analytes and properties and MUST permit additional analytes without requiring a core schema revision.

Common analytes and properties include:

- calcium;
- magnesium;
- sodium;
- potassium;
- iron;
- manganese;
- zinc;
- copper;
- bicarbonate;
- carbonate;
- sulfate;
- chloride;
- nitrate;
- nitrite;
- phosphate;
- silicate;
- fluoride;
- ammonium;
- alkalinity;
- total hardness;
- total dissolved solids;
- conductivity;
- pH;
- dissolved oxygen;
- chlorine;
- chloramine.

Reporting basis MUST be explicit where required for interpretation. In particular, alkalinity or hardness reported as CaCO3 MUST remain identified as such.

An implementation MUST NOT silently reinterpret reported alkalinity as bicarbonate concentration or reported hardness as a specific dissolved-ion concentration.

Any such conversion or estimate MUST be represented as derived information with its assumptions.

Conductivity MAY include a reference temperature. A reference temperature MUST NOT be invented when the source does not provide one.

### 17.6 Target-water profiles

A target-water profile describes desired chemistry or acceptable chemistry ranges. It MUST remain distinguishable from source-water observations and treated-liquor results.

A target-water profile MAY originate from:

- a user-defined target;
- a style or product specification;
- a published brewery or locality profile;
- a historical reference;
- a prior successful batch;
- another cited source.

A target derived from historical or published data SHOULD preserve the provenance and reported form of that source while keeping the target interpretation distinct from the source observation.

### 17.7 Regulatory and specification values

Regulatory limits, treatment targets, product specifications, and other limits MUST remain distinguishable from observed source-water chemistry.

A regulatory maximum or action level MUST NOT be imported as though it were an observed concentration.

### 17.8 Water blending

A water blend SHOULD record:

- source-water references;
- amount of each source;
- blending order where relevant;
- calculated blended profile;
- uncertainty;
- assumptions;
- provenance.

The calculated blended profile is derived information and MUST NOT alter the preserved source-water profiles.

If a blend is physically executed in a batch, the actual amounts used SHOULD be recorded in the batch execution record separately from the planned blend.

### 17.9 Water-treatment plans and execution

A water-treatment plan describes intended transformation of source water into treated liquor.

A treatment plan SHOULD record:

- source waters;
- planned blend;
- treatment steps;
- treatment order;
- treatment materials and planned amounts;
- chemical identity;
- hydration state;
- purity;
- solution concentration;
- target-water profile;
- predicted treated-liquor profile;
- assumptions;
- constraints;
- warnings.

A batch execution SHOULD record actual treatment materials, actual amounts, execution events, and resulting measurements separately from the plan.

Reported chemical identities and hydration states MUST NOT be silently normalized to a different chemical form.

### 17.10 Treated-liquor profiles

A treated-liquor profile describes water after blending or treatment.

A treated-liquor profile MUST distinguish:

- predicted or calculated chemistry;
- measured chemistry.

Predicted chemistry is derived information. Measured chemistry is observational information and MUST preserve measurement provenance and conditions.

### 17.11 Optimization results

Optimization results MUST be represented as calculation results and MUST NOT silently modify the source profile, target profile, treatment plan, or recipe.

An optimization result MAY include:

- objective;
- constraints;
- ranked alternatives;
- target deviations;
- exact-match solution;
- minimal-addition solution;
- minimal-number-of-additions solution;
- blend-first solution;
- practical rounded solution;
- infeasible-target report.

---

## 18. Equipment

### 18.1 Equipment definitions and instances

FermentationJSON SHOULD distinguish an equipment definition or model from a specific physical equipment instance.

An equipment definition describes relatively stable properties shared by a class, model, or configured design.

An equipment instance represents a particular physical asset used in production.

### 18.2 Equipment definitions

An equipment definition MAY include:

- equipment class;
- manufacturer;
- model;
- material;
- nominal capacity;
- geometry or dimensions;
- pressure rating;
- heating capability;
- cooling capability;
- nominal dead space;
- nominal losses;
- other model-level specifications.

### 18.3 Equipment instances

An equipment instance SHOULD include:

- stable identifier;
- equipment definition reference where applicable;
- serial or asset number where applicable;
- installation or location information;
- current configuration;
- operational status;
- instance-specific calibrated capacity or geometry;
- calibration references;
- maintenance references.

Mutable state, calibration history, and maintenance history SHOULD NOT be represented as immutable model specifications.

### 18.4 Equipment use in production

A batch SHOULD reference the actual equipment instance used when that identity affects reproducibility, traceability, or process interpretation.

If a referenced equipment configuration may change over time, the production record SHOULD preserve a version, configuration identifier, or sufficient snapshot to identify the configuration used.

### 18.5 Advanced equipment modeling

Optional modules MAY define:

- ports and fittings;
- hoses and pipes;
- valves and manifolds;
- pumps;
- flow paths;
- heating zones;
- cooling zones;
- calibrated vessel-volume tables;
- sensors and instruments;
- equipment topology.

---

## 19. Calculations and model results

### 19.1 Distinction from observations

A calculation or model result MUST remain distinguishable from a measurement, observation, reported source value, or target.

Unit conversion and canonicalization alone do not transform a measurement or reported value into a calculation result.

### 19.2 Calculation record

A calculation result SHOULD include, as applicable:

- calculation or model type;
- input values or input references;
- output values;
- formula or model identifier;
- formula or model version;
- implementation or software identity;
- implementation version;
- assumptions;
- coefficients;
- constraints;
- rounding policy;
- uncertainty or sensitivity information;
- warnings;
- timestamp;
- acceptance or selection status.

### 19.3 Reproducibility

A calculation result intended to be reproducible SHOULD preserve sufficient information to identify the exact inputs and model used.

If an input is referenced externally, the record SHOULD preserve a stable identifier, version, checksum, snapshot, or other mechanism sufficient to prevent silent changes to the calculation inputs.

A calculation MUST NOT modify the preserved source inputs.

### 19.4 Derived values

A derived value produced by a calculation MAY be embedded in another object when permitted by the applicable schema.

When embedded, the value MUST remain identifiable as derived and SHOULD reference or include the derivation provenance required by Section 11.

Selecting or accepting a calculated result MUST NOT cause it to be represented as a measurement or source-reported value.

### 19.5 Potential calculation types

Profiles and optional modules MAY define calculations including:

- gravity or extract conversion;
- alcohol;
- attenuation;
- bitterness;
- color;
- mash water;
- heat requirements;
- water blending;
- salt or acid additions;
- mash pH;
- culture pitch rate;
- fermentation modeling;
- carbonation;
- priming;
- draft balancing;
- equipment sizing;
- yield;
- losses;
- optimization.

---

## 20. Profiles

### 20.1 Purpose

Profiles define coherent sets of requirements for a domain or use case.

A profile MAY:

- require specific core fields;
- define controlled vocabularies;
- add domain-specific object types;
- constrain units;
- define additional validation rules;
- define compatibility behavior.

### 20.2 Profile declaration

A document conforming to a profile MUST declare the profile and version.

### 20.3 Multiple profiles

A document MAY declare multiple compatible profiles.

When two declared profiles conflict, validation MUST fail unless the applicable specification defines precedence.

### 20.4 Initial profiles

The initial stable profile is expected to be beer-oriented.

Future profiles may include wine, cider, perry, mead, sake, kombucha, vinegar, and other fermentation domains.

---

## 21. Extensions

### 21.1 General rules

Extensions MUST use a collision-resistant namespace or identifier.

An extension MUST NOT:

- redefine a normative core field;
- change the meaning of a normative value;
- bypass a required validation rule;
- claim conformance to a profile it violates.

### 21.2 Unknown extensions

A conforming implementation SHOULD preserve unknown extensions when reading and writing a document without modification.

An implementation MAY ignore an extension it does not understand, unless the extension declares that it is required for interpretation.

### 21.3 Required extensions

A required extension MUST be declared explicitly.

An implementation that does not understand a required extension MUST report that it cannot fully interpret the document.

### 21.4 Promotion

Experimental extensions MAY be promoted into a normative schema or profile after:

- documented implementation experience;
- compatibility analysis;
- review;
- conformance tests;
- an approved proposal or decision record.

---

## 22. External-format compatibility

Compatibility with an external format MUST be defined by a versioned compatibility profile.

A compatibility profile MUST specify:

- the supported source or target format and version;
- import guarantees;
- export guarantees;
- field and type mappings;
- unit-handling behavior;
- preservation of unknown or extension data;
- round-trip expectations;
- known limitations;
- required conformance fixtures;
- loss-reporting behavior.

### 22.1 BeerJSON 1.0

Every valid BeerJSON 1.0 document MUST be importable without loss of BeerJSON-defined information.

The BeerJSON 1.0 compatibility profile MUST preserve:

- all standard-defined fields;
- original values and units;
- identifiers and references;
- optional metadata;
- ordering where semantically meaningful;
- source-format and version information.

The project MUST maintain documented mappings and conformance fixtures for BeerJSON 1.0.

A round trip through FermentationJSON MUST preserve all BeerJSON-defined information when the document remains within the BeerJSON-representable subset.

Export to BeerJSON 1.0 MAY be supported. Any FermentationJSON information that cannot be represented MUST be identified in a loss report or cause the export to fail explicitly.

### 22.2 BeerXML 1.0

Every valid BeerXML 1.0 document MUST be importable while preserving all standard-defined information present in the source document.

Unknown application-specific elements SHOULD be retained opaquely where practical. Opaque preservation does not imply semantic understanding.

An importer MUST NOT claim to reconstruct information that the source document did not contain.

Implementations MAY provide a compatibility mode for common nonstandard BeerXML output. Compatibility mode SHOULD report each detected deviation from the BeerXML specification.

## 23. Loss reporting

A loss report SHOULD identify:

- source format;
- target format;
- source path;
- omitted data;
- transformed data;
- approximated data;
- unsupported units;
- unsupported object types;
- dropped extensions;
- severity;
- explanation;
- remediation guidance.

Loss severity MAY include:

- informational;
- warning;
- error;
- fatal.

A lossy export MUST NOT be described as lossless.

---

## 24. Versioning and evolution

### 23.1 Versioned artifacts

The project SHOULD version independently:

- the overall specification;
- schemas;
- profiles;
- vocabularies;
- compatibility mappings;
- reference implementations.

### 23.2 Compatibility

A versioning policy MUST define:

- backward compatibility;
- forward compatibility;
- breaking changes;
- additive changes;
- deprecation;
- removal;
- migration.

### 23.3 Stable identifiers

Published schema identifiers MUST remain stable.

A schema identifier MUST NOT be reused for incompatible content.

### 23.4 Deprecation

Deprecated fields or vocabularies SHOULD remain documented for an announced transition period.

Deprecation SHOULD include migration guidance.

### 23.5 Unknown fields

The specification MUST define whether unknown fields are rejected, ignored, or preserved for each schema context.

A uniform global policy is not required, but behavior MUST be explicit.

---

## 25. Conformance

### 23.1 Conforming document

A conforming document:

- validates against the declared schema or profile;
- uses the declared specification version;
- satisfies all applicable normative requirements;
- declares required extensions;
- maintains reference integrity required by the profile.

### 23.2 Conforming validator

A conforming validator MUST:

- evaluate the declared schema and profile;
- report validation failures;
- distinguish errors from warnings where defined;
- avoid silently accepting violations of normative requirements.

### 23.3 Conforming importer

A conforming importer MUST satisfy the applicable compatibility profile.

### 23.4 Conforming exporter

A conforming exporter MUST:

- produce valid target documents;
- report lossy transformations;
- preserve required source information where the target format supports it.

### 23.5 Partial implementations

An implementation MAY support only selected profiles or modules.

A partial implementation MUST accurately declare what it supports.

---

## 26. Security, privacy, and safety considerations

### 23.1 Untrusted input

Implementations MUST treat imported documents as untrusted input.

Validators and importers SHOULD defend against:

- excessive nesting;
- oversized arrays;
- oversized strings;
- malicious references;
- path traversal;
- remote-reference abuse;
- resource exhaustion;
- malformed numbers;
- parser discrepancies.

### 23.2 External resources

Applications SHOULD apply explicit policies to dereferencing external URIs.

Validation SHOULD NOT require unrestricted network access.

### 23.3 Personal information

Documents MAY contain personal or organizational information.

Applications SHOULD minimize collection and disclosure of unnecessary personal data.

### 23.4 Equipment control

FermentationJSON documents may describe controllers, setpoints, alarms, or equipment operations.

A document MUST NOT be treated as safe executable control logic solely because it validates.

Systems that translate documents into physical control actions MUST apply independent authorization, safety limits, and operational validation.

---

## 27. Specification artifacts

A FermentationJSON release SHOULD include the artifacts required to implement and test the published behavior:

- normative schemas and documentation;
- versioned profiles and vocabularies;
- compatibility mappings;
- conformance fixtures and tests;
- valid and invalid examples;
- migration guidance;
- release notes.

Importers, exporters, validators, documentation generators, and reference implementations MAY be published with the specification but MUST be identified separately from normative artifacts.

Interoperable behavior is defined by the schemas together with normative documentation, compatibility profiles, and conformance tests.

## 28. Development staging

Development is organized by dependency and implementation risk:

1. **Foundation** — document architecture, identifiers, references, quantities, measurements, provenance, profiles, extensions, compatibility, versioning, validation, and conformance.
2. **Core brewing** — recipes, batches, ingredients, cultures, equipment, brewing processes, packaging, water, measurements, calculations, and external-format compatibility tooling.
3. **Engineering modules** — laboratory data, sampling, sensors, calibration, telemetry, automation, detailed process execution, batch genealogy, advanced water treatment, and serving-system engineering.
4. **Additional domains** — wine, cider, perry, mead, sake, kombucha, vinegar, and other fermentation profiles.

Release scope and milestones are maintained in `ROADMAP.md`. Roadmap entries do not become normative until incorporated into a versioned specification artifact.

## 29. Open design questions

The following topics require separate proposals or architecture decisions:

- exact document-envelope structure;
- canonical-unit and unit-vocabulary policy;
- object-reference syntax and resolution;
- unknown-field handling by schema layer;
- stable schema and profile identifiers;
- package or multi-document container format;
- attachment and external-dataset packaging;
- namespace and vocabulary governance;
- digital signatures and integrity metadata;
- JSON-LD or ontology integration;
- streaming telemetry;
- long-term archival guidance.

Open questions are not normative requirements.

## 30. Design status

This document is a working engineering design.

Sections describing foundation architecture, compatibility guarantees, recipe and batch separation, quantity semantics, provenance, extension rules, and conformance represent the current intended direction.

Detailed field names, schema identifiers, vocabulary values, and profile-specific structures remain subject to implementation and review.

No section of this working draft should be interpreted as a final compatibility commitment until published as part of a versioned FermentationJSON release.
