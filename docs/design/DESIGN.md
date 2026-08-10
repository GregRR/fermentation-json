# FermentationJSON Design Specification

**Status:** Working Draft  
**Document version:** 0.11
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


### 7.4 Document envelope

All normative FermentationJSON document types MUST use the common document envelope.

The envelope uses the following top-level fields:

- `specification_version` — REQUIRED FermentationJSON specification version;
- `document_type` — REQUIRED document-type identifier;
- `schema_id` — REQUIRED identifier of the normative schema used to validate the document;
- `document_id` — REQUIRED globally unique document identifier;
- `profiles` — OPTIONAL array of declared profile identifiers and versions;
- `modules` — OPTIONAL array of declared optional-module identifiers and versions;
- `metadata` — OPTIONAL document metadata;
- `content` — REQUIRED document-type-specific payload;
- `extensions` — OPTIONAL controlled extension container.

Document-type-specific data MUST be placed under `content` rather than adding arbitrary top-level fields.

The `metadata` object MAY contain creation and modification timestamps, title, description, generator information, authorship or responsible organization, language, locale, licensing, tags, revision information, citations, and source relationships as permitted by the applicable schema.

Published schemas MAY add further required envelope fields only through a versioned specification change or applicable profile requirement.

`schema_id`, profile identifiers, and module identifiers that claim normative conformance MUST use stable absolute identifiers. Repository-relative paths are not normative conformance identifiers.

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


### 8.6 Identifier and reference serialization

`document_id` MUST be an absolute URI. A UUID URN is the RECOMMENDED default for newly created documents when no existing persistent URI is appropriate.

`object_id` is a stable opaque string scoped to the containing document. It MUST be unique within that document. Applications MUST NOT derive semantic meaning from the lexical form of an `object_id`.

A FermentationJSON data reference is an object that contains one or both of:

- `document_id`;
- `object_id`.

The following interpretations apply:

- `object_id` without `document_id` references an object in the current document;
- `document_id` without `object_id` references another document as a whole;
- both fields together reference an object within the identified document.

A reference MAY additionally contain:

- `expected_type`;
- `schema_id`;
- `media_type`;
- `checksum`;
- `label`.

Data references MUST NOT use JSON Pointer paths as persistent object identity. Structural paths may be retained as provenance locators, but object references must remain valid when unrelated document structure changes.

External object references SHOULD include both `document_id` and `object_id` rather than constructing an undocumented fragment identifier from the two values.

---

## 9. Universal quantity model

### 9.1 Purpose

The quantity model preserves the scientific meaning of a quantity while providing a normalized representation for interoperability.

A quantity may contain several independent dimensions of information:

- a canonical representation;
- an optional reported representation;
- value form, such as exact value, bound, range, or non-detect;
- source or derivation status;
- reported statistic;
- uncertainty or measurement-quality information;
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

### 9.4 Representation, epistemic state, and derivation are independent

`canonical` and `reported` describe representations of a quantity. They do not by themselves state whether a value came from a source, was observed, or was derived.

The data model MUST be able to distinguish, where relevant:

- reported;
- measured or observed;
- user-entered;
- calculated;
- derived;
- estimated;
- inferred;
- predicted;
- target or specification;
- nominal or default.

A single value MAY have more than one applicable characterization when the applicable schema defines their relationship. For example, an instrument measurement may also be a reported value imported from a laboratory report.

Derived information includes values produced by:

- mathematical derivation;
- interpolation;
- midpoint calculation;
- averaging or aggregation not explicitly reported by the source;
- chemical conversion or estimation;
- predictive models;
- optimization;
- inference.

A derived value MUST identify its derivation method or calculation provenance when the derivation affects scientific interpretation.

A derived value MUST NOT be serialized as though it had been reported by the source.

### 9.5 Value forms and qualified endpoints

The quantity model MUST support, as applicable:

- exact values;
- approximate values;
- lower bounds;
- upper bounds;
- open and closed bounds;
- numerical ranges;
- non-detects;
- detection limits;
- reporting limits;
- quantification limits;
- uncertainty;
- tolerance;
- confidence intervals;
- source-reported summary statistics.

The representations of these forms MUST remain distinguishable.

A range endpoint MUST be capable of preserving the endpoint's own result form when required by the source. An endpoint MAY therefore be exact, bounded, or non-detected.

Examples such as `ND–11.1 mg/L` and `<3–14 mg/L` MUST be representable without inventing a numerical value for the qualified endpoint.

### 9.6 Non-detects and analytical limits

A non-detect is a statement about an analytical result and is not numerically equivalent to zero.

If a source reports only a non-detect, FermentationJSON MUST preserve the non-detect without inventing a detection, reporting, or quantification limit.

If a detection limit, reporting limit, or quantification limit is explicitly supplied, it SHOULD be preserved separately from the result status or bound.

Statements such as `ND`, `<5`, and `0` represent different conditions and MUST NOT be treated as interchangeable.

### 9.7 Reported statistics and derived statistics

Result form and reported statistic are separate concepts.

The reported-statistic model MUST be able to distinguish at least:

- single observation;
- ordinary reported average or mean;
- running annual average;
- locational running annual average;
- percentile, including the percentile rank when known;
- highest result;
- lowest result;
- other explicitly named statistics while retaining the source label.

Profiles MAY define additional statistics.

An ordinary average explicitly supplied by a source MAY be preserved as a reported average.

An ordinary reported-average concept MUST NOT be used as a generic container for a running annual average, locational running annual average, percentile, highest result, lowest result, or another separately named statistic.

A value calculated by an importer or consuming application MUST NOT be labeled or represented as a reported statistic unless the source itself reported that statistic.

Reported minimum and maximum values over an observation period MUST NOT automatically be interpreted as uncertainty bounds, specification limits, or confidence limits.

### 9.8 Representative calculation values

Some applications require a single representative scalar for calculations even when the source supplies multiple values or a range.

For linearly scaled quantities, an applicable profile MAY define a default representative-value policy. Unless the profile specifies otherwise, the recommended precedence is:

1. an ordinary average explicitly reported by the source;
2. an exact reported value;
3. an on-demand midpoint of a numerical range whose endpoints are both exact.

A midpoint calculated from a range is derived information. It MUST NOT be serialized as a reported value or reported average.

A qualified or censored range has no automatic midpoint unless an applicable profile defines a scientifically justified method.

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
- disinfectant concentration reported as Cl2;
- concentration reported as an ion;
- concentration reported as an element;
- percent by mass;
- percent by volume;
- mass per volume;
- hydrated versus anhydrous chemical additions.

Dimensionally compatible representations MUST NOT be treated as semantically interchangeable when their chemical or reporting bases differ.

A conversion or estimate between chemically different reporting forms MUST be represented as derived information and MUST identify the assumptions or chemical model used.

If `ppm` or `ppb` is permitted by a profile, the applicable mass, volume, or solution-density basis MUST be defined or otherwise unambiguous. An implementation MUST NOT silently assume that all uses of `ppm` or `ppb` are equivalent to `mg/L` or `µg/L`.

### 9.12 Unit and quantity-kind identifiers

Normative persisted unit identifiers MUST be unambiguous.

FermentationJSON core unit and quantity-kind identifiers use stable lower-case snake-case tokens defined by versioned vocabularies. Non-core extension identifiers MUST use collision-resistant absolute URIs.

Human-readable unit symbols, abbreviations, aliases, and source spellings are not normative persisted identifiers.

Where a customary unit name has materially different definitions, the identifier MUST distinguish the applicable definition. For example:

- `us_liquid_gallon` and `imperial_gallon` are distinct;
- `us_fluid_ounce` and `imperial_fluid_ounce` are distinct;
- `us_beer_barrel` is distinct from other units called barrel.

`us_beer_barrel` is exactly 31 `us_liquid_gallon`.

The exact source unit spelling SHOULD be preservable separately from the normalized reported-unit identifier.

### 9.13 Canonical-unit policy

Every registered core quantity kind MUST declare exactly one canonical unit in the applicable versioned quantity-kind vocabulary.

For a registered core quantity kind, a quantity's canonical representation MUST use that declared canonical unit.

Canonical units are selected for interoperability, scientific meaning, and domain practicality. A canonical unit need not be an SI base unit.

The initial foundation policy includes, among others:

- volume in `liter`;
- mass in `kilogram`;
- temperature in `degree_celsius`;
- temperature difference in `kelvin_difference`;
- pressure in `kilopascal`;
- mass concentration in `milligram_per_liter`;
- amount concentration in `mole_per_liter`;
- equivalent concentration in `milliequivalent_per_liter`;
- conductivity in `microsiemens_per_centimeter`;
- pH using `ph_scale`.

Profiles MAY define additional quantity kinds and canonical units through versioned profile vocabularies.

A quantity kind describes the quantity being represented, not the identity of an analyte or material. For example, calcium and sulfate measurements can both use `mass_concentration` while the enclosing measurement identifies the analyte.

### 9.14 Reported-unit policy and aliases

A reported representation SHOULD use a registered FermentationJSON unit identifier when the source unit can be identified without inventing meaning.

Source symbols and aliases MAY be preserved for round-trip fidelity, but aliases MUST NOT be treated as normative persisted identifiers.

An importer MUST NOT map an ambiguous source token such as an unqualified `gallon`, `fluid ounce`, or `barrel` to a specific FermentationJSON unit without sufficient source context.

### 9.15 Ratio units and concentration semantics

`part_per_million` and `part_per_billion` are ratio units.

They MUST NOT be treated as universally equivalent to `milligram_per_liter` or `microgram_per_liter`.

When a source reports `ppm` or `ppb`, the source meaning MUST be preserved. A mass-per-volume concentration MAY be derived only when the necessary reporting basis, density assumption, or other scientific relationship is known and documented.

### 9.16 External unit systems

FermentationJSON does not normatively depend on an external unit code system or software unit library.

Implementations MAY use external unit systems or libraries for parsing, conversion, validation, or display when their semantics are compatible with FermentationJSON.

External mappings are adapter behavior and MUST NOT silently change a FermentationJSON unit's meaning.

## 10. Measurements and observations

### 10.1 Measurement record

A measurement or observation SHOULD identify:

- the property or analyte;
- the result;
- the subject, material, or sample;
- the observation time or observation period when known;
- observation or sampling location when known and material;
- process or material stage when known and material;
- provenance;
- measurement or reference conditions when relevant.

A report publication date MUST NOT be used as a substitute for an observation date or observation period.

### 10.2 Temporal applicability and coverage

The data model MUST be able to distinguish:

- a single observation time or date;
- an observation period;
- a report or publication date;
- a profile or result intended to represent typical, historical, reference, or otherwise aggregated conditions.

Where a schema provides both a single observation field and an observation-period field for the same scope, they SHOULD be mutually exclusive unless the profile defines a specific combined meaning.

An observation period SHOULD identify its start and end when known.

An individual measurement or reported result MUST be able to carry a more specific observation time or period than its enclosing document, report, or profile.

A calendar year, report year, or publication year MUST NOT be converted into an invented observation date merely to satisfy a schema.

### 10.3 Result status

A measurement result MAY carry status including:

- valid;
- invalid;
- missing;
- not detected;
- below detection limit;
- below reporting limit;
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

### 10.5 Measurement context

Sample location, process stage, water stage, vessel, or other observation context MUST remain separate from the identity of the measured material when the distinction is relevant.

A context value MUST NOT be inferred when the source does not identify it.

### 10.6 Measurement conditions

When a result depends materially on conditions such as temperature, pressure, sample preparation, analytical basis, or instrument configuration, those conditions SHOULD be preserved.

A reference condition SHOULD be omitted rather than guessed when the source does not provide it, unless a governing analytical method or profile supplies a normative default.

### 10.7 Time series

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

## 11. Provenance and source-document metadata

### 11.1 General requirements

The provenance model MUST permit provenance to be attached to documents, objects, measurements, quantities, calculations, statistical summaries, derived values, and imported source fragments.

Provenance SHOULD identify, where applicable:

- source document;
- source location or field;
- person;
- organization;
- laboratory or analysis provider;
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

### 11.3 Source-document metadata

Source-document metadata MUST be capable of distinguishing the document or report from the physical material, product, source, or sample described by that document.

Source-document metadata SHOULD support, where known:

- publisher;
- analysis provider or laboratory;
- document title;
- publication date;
- source URI or external reference;
- retrieval date;
- page, table, section, record, or field locator;
- notes.

Publisher and analysis provider are separate concepts. An implementation MUST NOT infer that the publisher performed the analysis, or infer the publisher from the analytical laboratory, unless the source explicitly establishes that relationship.

### 11.4 Imported data

Imported data MUST preserve the source format and source-format version when known.

An importer SHOULD preserve source paths, source field names, source text, page or table references, or other locators when useful for verification.

Canonicalization during import MUST NOT erase the source representation.

### 11.5 Automated extraction and interpretation

Automated extraction from documents, images, PDF files, natural-language reports, or other semi-structured sources MAY be used as an ingestion aid.

Automatically extracted or interpreted data SHOULD retain:

- the original source reference;
- a locator to the supporting source material when practical;
- the extraction software or method;
- extraction confidence when available;
- validation status;
- human-review status;
- warnings.

A system MUST NOT represent an inferred or guessed value as though it were explicitly reported by the source.

If automated extraction cannot determine a value, unit, reporting basis, qualifier, reference condition, observation date, stage, source identity, or other semantic field with sufficient confidence, the unresolved information SHOULD remain unresolved pending review rather than being silently inferred.

### 11.6 Derived and calculated data

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

### 17.1 Scope and domain neutrality

The water model is a reusable scientific and engineering capability. Its source-water, target-water, blend, treatment, treated-water, provenance, and calculation structures MUST NOT encode an assumption that the water is used only for beer.

The same source-water profile MAY be evaluated or treated for brewing, mead, distilling, coffee, tea, bread, sourdough, cleaning, boiler feed, or another application without duplicating or mutating the source-water chemistry.

Support for a non-fermentation water-use context does not imply that FermentationJSON defines the complete recipe or process model for that external domain.

### 17.2 Water object types

The water model MUST distinguish:

- source-water profile;
- target-water profile;
- treated-liquor or treated-water profile;
- water blend;
- treatment ingredient or treatment material;
- water-treatment plan;
- calculation or optimization result;
- regulatory or advisory reference.

The architecture MUST also permit future treatment-operation objects for non-additive treatments.

These concepts represent different states, identities, or purposes and MUST NOT be treated as semantically equivalent.

### 17.3 Source-water identity and physical source

A source-water profile SHOULD support distinct information for:

- provider or utility;
- brand, where applicable;
- product name or water type, where applicable;
- high-level source or water classification;
- one or more physical water sources, where known;
- geographic area;
- treatment plant, facility, spring, well, reservoir, aquifer, or bottling location where known;
- provenance.

Provider, brand, product, water type, treatment facility, and physical source MUST NOT be treated as interchangeable concepts.

A source-water profile MUST permit multiple physical sources because a supplied water may be drawn from or blended from multiple sources.

Source types MAY include:

- municipal;
- well;
- spring;
- artesian;
- mineral;
- rainwater;
- reverse osmosis;
- purified;
- distilled;
- bottled;
- laboratory-prepared;
- process water;
- reused water;
- blended water.

Unknown source identity MUST remain unknown rather than being inferred.

### 17.4 Source-document metadata

A source-water profile MAY reference one or more source documents using the provenance and source-document metadata model in Section 11.

Water-report metadata SHOULD distinguish:

- publisher;
- analysis provider or laboratory;
- document title;
- publication date;
- source URI or external reference;
- retrieval date;
- page, table, section, or result locator;
- notes.

A source document is not the water itself. Document identity MUST remain separate from provider, brand, physical water source, treatment facility, and sample location.

### 17.5 Temporal basis and coverage

A source-water profile MUST be able to distinguish:

- a single observation;
- an observation-period summary;
- a typical or representative analysis;
- a seasonal profile;
- a historical or reference profile.

A profile MAY contain an observation date, an observation period, or neither when the source provides only looser coverage semantics.

A single observation date and an observation period for the same profile scope SHOULD be mutually exclusive.

An individual reported result MUST be able to carry a more specific observation date, observation period, or coverage statement than the enclosing profile.

A report year or publication year MUST NOT be converted into an invented sample date.

### 17.6 Water stage and sampling context

A source-water profile or individual result MUST be able to identify water stage or sampling context when explicitly reported.

Supported contexts SHOULD include:

- raw source water;
- finished water;
- treatment-plant output;
- distribution-system water;
- customer-tap water;
- bottled finished product;
- other explicitly identified stages.

A result MAY identify a sample location independently of the profile's general geographic or source identity.

Water stage and sample location MUST NOT be inferred when the source does not identify them.

### 17.7 Source-reported chemistry and statistics

Source-water chemistry MUST preserve source-reported semantics.

For an analyte or property, a source profile or result MUST be able to represent:

- an exact reported value;
- a numerical range;
- a one-sided bound;
- a non-detect;
- qualified or censored range endpoints;
- an explicitly reported ordinary average;
- running annual average;
- locational running annual average;
- percentile with percentile rank where known;
- highest result;
- lowest result;
- another explicitly named source statistic.

Result form and reported statistic MUST remain separate concepts.

A derived midpoint, converted chemical species concentration, inferred reference condition, inferred source identity, or other calculated value MUST NOT be serialized as source-reported data.

For linearly scaled quantities, software MAY derive a representative scalar according to Section 9.8. That value remains derived.

For pH, the restrictions in Section 9.9 and Section 17.18 apply.

### 17.8 Analytes and water properties

The water schema MUST permit additional analytes and properties without requiring a core schema revision.

Stable analyte or property identifiers SHOULD be used where available while preserving source labels and synonyms.

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
- silica or silicate;
- fluoride;
- ammonium;
- lithium and other reported trace minerals;
- arsenic;
- lead;
- cadmium;
- chromium;
- nickel;
- selenium;
- aluminum;
- alkalinity;
- total hardness;
- total dissolved solids;
- conductivity;
- pH;
- dissolved oxygen;
- hydrogen sulfide;
- trihalomethanes;
- turbidity;
- odor;
- color;
- disinfectants.

Preserving an analyte or property MUST NOT imply that a consuming calculator has a validated treatment, sensory, health, or process model for it.

### 17.9 Reporting basis, alkalinity, hardness, TDS, and conductivity

Reporting basis MUST be explicit where required for interpretation.

In particular:

- total alkalinity and bicarbonate concentration MUST remain distinct;
- total hardness and component hardness MUST preserve their stated reporting basis;
- alkalinity or hardness reported as CaCO3 MUST remain identified as such;
- elemental, ionic, and molecular concentrations MUST remain distinguishable when the distinction affects meaning.

An implementation MUST NOT silently reinterpret total alkalinity as bicarbonate concentration or total hardness as a specific dissolved-ion concentration.

If a source explicitly identifies bicarbonate alkalinity on a CaCO3 equivalent basis, a normalized bicarbonate value MAY coexist as a derived representation when the relationship and assumptions are explicit. This permission MUST NOT be generalized to total alkalinity.

Conductivity MUST permit an optional measurement or reference temperature. A reference temperature MUST NOT be invented when the source does not provide one.

Total dissolved solids SHOULD permit analytical method or conversion-basis metadata where supplied by the source.

### 17.10 Disinfectants

Chloride concentration and disinfectant residuals are different chemical concepts and MUST NOT be substituted for one another.

The water model MUST be able to preserve at least:

- free chlorine;
- total chlorine;
- combined chlorine;
- chloramine reported generically;
- named chloramine species when explicitly identified;
- chlorine dioxide.

The reported analytical label, method, and reporting basis, including a basis such as `as Cl2`, SHOULD be preserved when supplied.

An implementation MUST NOT derive combined chlorine or chloramine by subtracting free chlorine from total chlorine unless it applies an explicit documented analytical rule. Any such result is derived information.

A treatment model MAY predict disinfectant removal or transformation. Predicted removal MUST remain distinct from a measured post-treatment residual.

### 17.11 Target-water profiles

A target-water profile describes desired, acceptable, or reference chemistry. It MUST remain distinguishable from source-water observations and treated-water results.

A target-water profile MUST support exact target values and acceptable ranges where applicable.

A target MAY also include:

- a preferred or nominal value within an acceptable range;
- hard minimum or maximum constraints;
- optimization weight or priority;
- flavor, process, or application priority;
- required or prohibited conditions;
- notes.

A target-water profile MUST identify its target or reference role where material. Roles MAY include:

- custom target;
- prior successful batch or treated-water state;
- style recommendation;
- published brewery profile;
- historical city or regional profile;
- application-provided recommendation;
- other referenced target.

A target derived from historical or published data MUST preserve source attribution.

Conflicting published versions of a historical or locality profile MUST remain separately attributable records and MUST NOT be silently averaged into a single target.

A historical locality profile SHOULD NOT be represented as source water unless it actually describes a specific measured source-water analysis.

### 17.12 Intended water use and process context

Intended use belongs to the calculation, treatment, target, recipe, batch, or process context. It is not part of immutable source-water identity.

The water model SHOULD provide an extensible intended-use concept capable of representing, as applicable:

- general brewing liquor;
- mash water;
- sparge water;
- dilution or high-gravity brewing water;
- fermentation or process water;
- spirit-proofing water;
- coffee-brewing water;
- tea-brewing water;
- bread-dough water;
- sourdough starter or dough water;
- service or cleaning water;
- CIP water;
- boiler-feed water;
- another defined use.

Use context MAY select different targets, requirements, warnings, or calculation models without changing the source-water profile.

A treatment plan or treated-water state SHOULD be referenceable from a recipe, batch, or process stage.

### 17.13 Regulatory and advisory references

Regulatory limits, treatment targets, product specifications, action levels, notification levels, advisory values, and other reference thresholds MUST remain distinguishable from observed source-water chemistry.

A regulatory or advisory value MUST NOT be imported as though it were an observed concentration.

The reference model MUST permit source-specific labels and SHOULD support commonly encountered threshold categories.

A regulatory or advisory reference SHOULD identify its issuing authority, source document, and effective period when known.

### 17.14 Water blending

A water blend MUST support two or more source-water references.

Each component MUST be able to carry an actual amount when known. Fractions MAY also be stored or derived.

A water blend SHOULD record:

- source-water references;
- amount of each source;
- fraction of each source when useful;
- blending order where operationally relevant;
- derived blended profile;
- uncertainty;
- assumptions;
- provenance.

The derived blended profile MUST NOT alter the preserved source-water profiles.

A blend calculation MUST NOT imply that every property was linearly averaged merely because conservative ion concentrations were linearly combined. In particular, pH and censored values MUST obey their applicable quantity-specific rules.

A blend or treatment workflow SHOULD permit explicit pre-treatment and post-treatment states.

If a blend is physically executed in a batch, actual amounts used SHOULD be recorded separately from the planned blend.

### 17.15 Treatment ingredients and additions

A treatment ingredient is a material used in a water-treatment role. Chemical identity MUST remain separate from product packaging, inventory, or supplier information.

A treatment ingredient MUST be able to identify, where applicable:

- stable chemical or material identity;
- display name;
- chemical formula or composition;
- hydration state or exact chemical form;
- molar or stoichiometric identity;
- composition evidence or provenance;
- purity or assay;
- solution concentration or strength.

A liquid treatment product SHOULD permit density when mass-to-volume dosing depends on it.

Hydration state is part of chemical identity and MUST NOT be treated as a unit conversion.

A treatment addition MUST be able to record:

- treatment-ingredient reference;
- planned amount;
- actual amount when executed;
- target liquor or water state;
- intended water use or process stage;
- timing or order when relevant;
- mathematically ideal dose when applicable;
- practical rounded dose when different;
- expected contribution;
- measured post-treatment result when later observed.

Planned and actual additions MUST remain distinguishable.

### 17.16 Non-additive treatment operations

The architecture MUST remain capable of representing non-additive water-treatment operations without redesigning source-water or treatment-plan semantics.

Optional or future treatment-operation definitions MAY include:

- dilution;
- reverse osmosis;
- activated-carbon filtration;
- dechlorination;
- boiling;
- lime softening;
- ion exchange;
- acidification;
- alkalization;
- deaeration;
- mineral removal;
- staged treatment.

A treatment operation MUST distinguish, when represented:

- declared or actual process settings;
- modeled expected effect;
- measured post-operation result;
- model or method;
- assumptions.

### 17.17 Water-treatment plans

A water-treatment plan describes intended transformation of source water into treated water or liquor.

A plan SHOULD be able to record:

- source-water references;
- source-water amounts or blend fractions;
- required final or batch volume when applicable;
- target-water profile;
- intended water use or process context;
- treatment additions;
- treatment operations when supported;
- predicted final profile;
- target deviations;
- objective components;
- constraint outcomes;
- assumptions;
- warnings and explanation codes;
- calculation status;
- chemistry-model version;
- optimization-policy version;
- solver or implementation version;
- reference-data version;
- relevant schema or adapter compatibility versions.

For additive ion modeling, the plan or associated calculation result MUST be able to expose a contribution matrix or equivalent structured explanation showing, for each modeled ion:

- initial source-water contribution;
- blend-component contribution where applicable;
- contribution from each treatment ingredient;
- final modeled total.

A treatment plan and its optimization results are derived planning information. They MUST NOT silently mutate source-water profiles or be represented as measured reality.

### 17.18 Treated-water profiles and pH

A treated-water or treated-liquor profile describes water after blending or treatment.

It MUST distinguish:

- predicted or calculated chemistry;
- measured chemistry.

Predicted chemistry is derived information. Measured chemistry is observational information and MUST preserve measurement provenance and conditions.

Calculated working-water pH MUST remain distinct from reported source-water pH and measured post-treatment pH.

A calculated working-water pH SHOULD identify:

- model name and version;
- assumptions;
- source or input references;
- relevant temperature or reference conditions;
- warning or approximation status;
- insufficient-data status when applicable.

Mash-pH prediction is a recipe- and process-dependent calculation and MUST remain distinct from working-water pH and from measured mash pH.

### 17.19 Optimization results

Water optimization MUST support multiple distinct ranked candidate plans when the optimizer produces more than one meaningful solution.

An optimization result MUST be able to identify a versioned named policy or explicit objective and constraint definitions.

Policies MAY include:

- closest match;
- fewest treatment products;
- lowest total addition;
- least dilution;
- no dilution;
- water-only;
- permitted ingredients only;
- another explicitly defined policy.

An optimization result MUST permit objective components to be represented separately rather than only as an opaque aggregate score.

Objective components MAY include:

- weighted analyte deviation;
- hard-constraint violation penalty;
- number of treatment products;
- total treatment mass;
- dilution-water usage;
- dose-rounding deviation;
- application-provided cost.

Constraint outcomes MUST be able to state whether a constraint was satisfied, violated, or not evaluated.

A result-status vocabulary MUST be able to distinguish, as applicable:

- exact within declared numerical tolerance;
- all target ranges satisfied;
- closest feasible under constraints;
- mathematically feasible but operationally impractical;
- infeasible with supplied sources or treatments;
- solver failure;
- indeterminate or insufficient-data result.

Machine-readable warnings or explanation codes SHOULD be able to identify causes such as:

- source concentration already above target;
- coupled-ion tradeoff prevents simultaneous target satisfaction;
- required treatment ingredient excluded;
- practical dose rounding causes a constraint violation;
- insufficient source data;
- unsupported or unvalidated model.

A consuming application MUST NOT imply that target matching guarantees flavor, extraction quality, fermentation performance, food quality, or safety.

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

A calculation or model result MUST remain distinguishable from a measurement, observation, reported source value, target, or specification.

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
- named policy or policy version;
- assumptions;
- coefficients;
- constraints;
- constraint outcomes;
- objective components;
- rounding policy;
- uncertainty or sensitivity information;
- warnings or explanation codes;
- status;
- timestamp;
- acceptance or selection status.

A calculation that depends on independently versioned reference data SHOULD identify that reference-data version.

Profiles MAY require additional independently versioned artifacts, such as scientific-model versions, optimizer-policy versions, solver versions, or compatibility-adapter versions.

### 19.3 Reproducibility

A calculation result intended to be reproducible SHOULD preserve sufficient information to identify the exact inputs, model, policy, assumptions, and independently versioned reference data used.

If an input is referenced externally, the record SHOULD preserve a stable identifier, version, checksum, snapshot, or other mechanism sufficient to prevent silent changes to the calculation inputs.

A calculation MUST NOT modify the preserved source inputs.

### 19.4 Derived values

A derived value produced by a calculation MAY be embedded in another object when permitted by the applicable schema.

When embedded, the value MUST remain identifiable as derived and SHOULD reference or include the derivation provenance required by Section 11.

Selecting or accepting a calculated result MUST NOT cause it to be represented as a measurement or source-reported value.

### 19.5 Indeterminate and failed calculations

A calculation-result model MUST permit a calculation to terminate without a numeric result when the requested output cannot be determined scientifically or computationally.

Applicable statuses MAY include:

- successful;
- exact within declared tolerance;
- feasible;
- closest feasible;
- infeasible;
- operationally impractical;
- indeterminate;
- insufficient data;
- unsupported model;
- solver or implementation failure.

An implementation MUST NOT invent a numeric result merely because a result field would otherwise be empty.

A failed, infeasible, or indeterminate result SHOULD preserve enough warnings, explanation codes, or missing-input information for a consumer to understand why no valid result was produced.

### 19.6 Multiple candidate results

A calculation or optimization MAY produce multiple candidate results.

When candidates are ranked, the result SHOULD preserve:

- rank;
- named policy or objective;
- objective components;
- constraint outcomes;
- selection or rejection status;
- warnings.

The format MUST NOT require a multi-objective calculation to collapse all objective information into one opaque score.

### 19.7 Potential calculation types

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

## 20. Profiles and optional modules

### 20.1 Purpose

A profile defines a coherent set of requirements for a fermentation domain or interoperability use case.

An optional module defines an independently adoptable capability that may be used by one or more profiles.

A profile or module MAY:

- require fields that are optional in a core schema;
- define domain-specific object types;
- define or constrain controlled vocabularies;
- restrict permitted units or quantity kinds;
- impose additional semantic or validation requirements;
- define domain-specific reference rules;
- define compatibility behavior.

A profile or module MUST NOT weaken a normative core requirement.

### 20.2 Identification and versioning

Every normative profile and module MUST have a stable identifier and an explicit version.

A document claiming conformance to a profile or module MUST declare the exact identifier and version.

A published identifier MUST NOT be reassigned to incompatible content.

### 20.3 Multiple profiles and modules

A document MAY declare more than one compatible profile or module.

All declared requirements apply cumulatively unless the applicable specification explicitly defines another composition rule.

If two declared normative requirements conflict and no explicit composition rule resolves the conflict, the document is nonconforming.

### 20.4 Profile scope

Profiles SHOULD contain requirements specific to their domain or interoperability purpose rather than duplicate reusable core definitions.

The initial stable domain profile is expected to be brewing-oriented.

Later profiles MAY define wine, cider, perry, mead, sake, kombucha, vinegar, and other fermentation domains.

---

## 21. Extensions

### 21.1 Purpose

Extensions provide a controlled mechanism for representing information that is not defined by the applicable normative schemas or profiles.

Extensions are not a substitute for profiles when a capability requires shared interoperability rules.

### 21.2 Identification and collision avoidance

Every extension MUST use a collision-resistant identifier or namespace.

An extension identifier SHOULD be globally unique and SHOULD be URI-compatible.

An extension MUST NOT:

- redefine a normative field;
- change the meaning of a normative value;
- bypass a required validation or conformance rule;
- shadow a normative identifier;
- claim conformance to a profile that it violates.

### 21.3 Optional and required extensions

An extension MUST declare whether understanding it is optional or required for correct interpretation of the containing document.

An implementation MAY ignore an optional extension it does not understand.

An implementation that does not understand a required extension MUST report that it cannot fully interpret the document and MUST NOT claim full conformance for processing that document.

### 21.4 Preservation of unknown extensions

A processor that reads and rewrites a document without intentionally transforming an unknown extension SHOULD preserve that extension without semantic alteration.

If an implementation cannot preserve a required unknown extension during a transformation, the transformation MUST fail or report the loss as required by Section 23.

Preservation of unknown extension data does not imply validation or semantic understanding.

### 21.5 Extension validation

An extension MAY publish its own schema, vocabulary, or conformance requirements.

A document MUST NOT claim conformance to an extension unless it satisfies that extension's declared requirements.

### 21.6 Promotion into the specification

An experimental extension MAY be proposed for promotion into a normative schema, profile, module, or vocabulary.

Promotion SHOULD require:

- a documented interoperability problem;
- implementation experience;
- compatibility analysis;
- defined migration behavior;
- conformance fixtures or tests;
- review through the applicable proposal or decision process.

Promotion MUST NOT silently change the meaning of existing extension data.


### 21.7 Unknown fields and extension serialization

Concrete normative FermentationJSON object schemas MUST reject undeclared fields unless the applicable schema explicitly defines an open property set.

Reusable base schemas intended for composition SHOULD NOT close themselves. The final concrete schema or profile SHOULD apply `unevaluatedProperties: false` after composition so that properties introduced by composed schemas are recognized before unknown fields are rejected.

Application-specific data MUST use the defined `extensions` container rather than arbitrary undeclared properties.

The `extensions` container is an object keyed by collision-resistant extension identifiers. Each extension entry MUST contain:

- `required` — boolean indicating whether understanding the extension is required for correct interpretation;
- `data` — the extension payload.

An extension entry MAY contain additional metadata defined by the extension's own schema.

An unknown extension identifier is not an unknown core field. It is handled according to Sections 21.3 through 21.5.

A newer specification version MAY define fields unknown to an older implementation. An older implementation MUST NOT silently accept such fields as though it understood their semantics. Version negotiation, declared conformance scope, or the extension mechanism MUST determine how they are handled.

---

## 22. External-format compatibility

### 22.1 Compatibility profiles

A normative compatibility claim with an external format MUST be defined by a versioned compatibility profile.

A compatibility profile MUST specify:

- the external format and applicable version;
- whether import, export, or both are supported;
- field and type mappings;
- unit and quantity handling;
- preservation requirements;
- treatment of unknown or extension data;
- round-trip expectations;
- known limitations;
- required conformance fixtures;
- loss-reporting behavior.

Compatibility claims MUST identify the exact compatibility-profile version being implemented.

### 22.2 Semantic and lexical preservation

Unless a compatibility profile explicitly states otherwise, "lossless" refers to preservation of defined information and meaning, not byte-for-byte reproduction of the source serialization.

Whitespace, object-member ordering that has no defined semantic meaning, XML formatting, comments, and other purely lexical details need not be preserved unless the compatibility profile requires them.

Original source values, units, qualifiers, identifiers, and other defined information MUST be preserved when required by the compatibility profile.

### 22.3 BeerJSON 1.0

Every valid BeerJSON 1.0 document MUST be importable into FermentationJSON without loss of BeerJSON-defined information.

The BeerJSON 1.0 compatibility profile MUST preserve:

- all standard-defined fields;
- original values and units;
- identifiers and references;
- optional metadata;
- ordering where BeerJSON assigns semantic meaning to ordering;
- source-format and version information.

Canonicalization or normalization performed during import MUST NOT erase the BeerJSON source representation required for lossless preservation.

The project MUST maintain documented mappings and conformance fixtures for BeerJSON 1.0.

For content representable in both formats, a BeerJSON-to-FermentationJSON-to-BeerJSON round trip MUST preserve all BeerJSON-defined information.

Export to BeerJSON 1.0 MAY be supported. Information not representable in BeerJSON 1.0 MUST cause the export to fail explicitly or MUST be identified by a loss report.

### 22.4 BeerXML 1.0

Every valid BeerXML 1.0 document MUST be importable while preserving all standard-defined information present in the source document.

The compatibility profile MUST distinguish BeerXML-defined information from application-specific extensions.

Unknown application-specific elements SHOULD be retained opaquely where practical. Opaque preservation does not imply semantic understanding.

An importer MUST NOT claim to reconstruct information that the BeerXML source did not contain, including information normalized or omitted by the source application before export.

Implementations MAY provide a compatibility mode for common nonstandard BeerXML output. Compatibility mode SHOULD report each detected deviation from BeerXML 1.0.

---

## 23. Loss reporting

### 23.1 Requirement

A transformation that omits, approximates, reinterprets, or otherwise cannot preserve information required by the source representation or applicable compatibility profile is lossy.

A lossy transformation MUST either:

- fail explicitly before producing a target document; or
- produce a machine-readable loss report.

A lossy transformation MUST NOT be described as lossless.

### 23.2 Loss entries

A loss report MUST identify the source format or profile and target format or profile.

Each loss entry SHOULD identify, when applicable:

- the source path or object identifier;
- the affected value or concept;
- the loss category;
- severity;
- transformation performed;
- explanation;
- remediation guidance.

Loss categories MAY include:

- omitted information;
- unsupported object or field;
- unsupported extension;
- unsupported semantic qualifier;
- unsupported unit or reporting basis;
- precision reduction or rounding;
- approximation;
- many-to-one mapping;
- ambiguous mapping.

### 23.3 Non-lossy transformations

A change in serialization form is not inherently lossy.

Examples of transformations that MAY be non-lossy when meaning and required source information are preserved include:

- exact unit conversion;
- canonicalization;
- member reordering where ordering has no defined meaning;
- whitespace changes;
- normalization that retains the source representation required by the applicable profile.

### 23.4 Severity

A loss-report vocabulary MAY define severities such as:

- informational;
- warning;
- error;
- fatal.

Severity MUST NOT be used to conceal the fact that a transformation is lossy.

---

## 24. Versioning and evolution

### 24.1 Versioned normative artifacts

The project MUST version normative artifacts whose evolution can affect conformance or interpretation, including:

- the overall specification;
- schemas;
- profiles;
- optional modules;
- vocabularies;
- compatibility profiles.

Tools and reference implementations SHOULD be versioned independently from the specification.

### 24.2 Release versioning

Published FermentationJSON specification releases MUST use semantic versioning.

A major version change indicates an incompatible change to normative behavior or document interpretation.

A minor version change MAY add backward-compatible capabilities, schemas, profiles, modules, vocabulary terms, or optional fields.

A patch version change MUST NOT intentionally change the set or meaning of conforming documents. Patch releases MAY correct documentation, tests, examples, or defects where the intended normative behavior is unchanged.

Pre-1.0 development releases MAY change incompatibly. Such changes MUST be identified in release notes.

### 24.3 Artifact identifiers

Every published normative schema, profile, module, vocabulary, and compatibility profile MUST have a stable versioned identifier.

A versioned identifier MUST NOT be reused for different normative content.

The canonical public namespace for FermentationJSON JSON Schema resources is:

```text
https://gregrr.github.io/fermentation-json/schemas/
```

Core schemas are published as coordinated schema sets. The current pre-release schema-set version is `0.1.0`, with core schema IDs under:

```text
https://gregrr.github.io/fermentation-json/schemas/0.1.0/core/
```

The schema-set version is an artifact-set version and MUST NOT be interpreted as the FermentationJSON specification release version unless a release explicitly makes those versions equal.

Each schema resource MUST declare its canonical absolute URI using `$id`.

A fragment-only `$ref` MAY address an anchor in the same resource. A relative cross-schema `$ref` MAY be used only when it resolves, from the referring schema's canonical `$id`, to another resource in the same versioned schema-set namespace. It MUST NOT escape that namespace.

Schema retrieval location is separate from schema identity. Conforming implementations MUST NOT require canonical schema URIs to be fetched over the network when the required resources are otherwise available through a registry, package, cache, or equivalent resolver.

No unversioned convenience schema identifiers are currently defined.

Where an unversioned convenience identifier is provided in the future, it MUST resolve according to a documented policy and MUST NOT be used when an immutable version reference is required for reproducibility.

### 24.4 Backward and forward compatibility

The versioning policy MUST define, for each class of normative artifact:

- what constitutes a breaking change;
- what constitutes an additive compatible change;
- how unknown future fields or vocabulary values are handled;
- migration requirements;
- deprecation and removal behavior.

Compatibility MUST NOT be inferred solely from numeric version ordering.

### 24.5 Deprecation and removal

A deprecated field, object type, vocabulary term, or behavior SHOULD remain documented for an announced transition period.

Deprecation SHOULD include:

- the replacement, if any;
- migration guidance;
- the version in which deprecation began;
- the earliest version in which removal may occur.

Removal of previously conforming normative behavior requires a major-version change unless the behavior was explicitly experimental or otherwise outside the compatibility guarantee.

### 24.6 Unknown fields and vocabulary values

Each normative schema or profile MUST define how unknown fields and unknown vocabulary values are handled.

The behavior MAY differ by context, but it MUST be explicit.

Extension fields governed by Section 21 are not considered unknown core fields when they are represented through the defined extension mechanism.

---

## 25. Conformance

### 25.1 Levels of validation

FermentationJSON distinguishes structural validation from full conformance.

**Structural validation** determines whether a document satisfies the applicable machine-readable schema constraints.

**Full conformance** additionally includes normative semantic and behavioral requirements that may not be expressible in JSON Schema, including reference integrity, compatibility preservation, derivation rules, required extension handling, and loss-reporting behavior.

A document MUST NOT be described as fully conforming solely because it passes JSON Schema validation.

### 25.2 Conforming document

A conforming document MUST:

- be syntactically valid JSON;
- validate against its declared normative schema and profile constraints;
- declare the applicable specification, profile, and module versions;
- satisfy all applicable semantic requirements;
- declare required extensions;
- satisfy required reference-integrity rules.

### 25.3 Conforming validator

A validator MAY perform structural validation only or full conformance validation.

A validator MUST accurately state which level it performs.

A structural validator MUST:

- evaluate the declared machine-readable schema constraints;
- report validation failures;
- avoid claiming that structural validity establishes full conformance.

A full-conformance validator MUST additionally evaluate all normative requirements within its declared conformance scope.

### 25.4 Conforming importer

An importer claiming compatibility with an external format MUST identify the compatibility-profile version it implements and MUST satisfy all applicable import requirements and conformance fixtures.

An importer MUST NOT claim lossless import when required source information is discarded, approximated, or silently reinterpreted.

### 25.5 Conforming exporter

An exporter claiming compatibility with an external format MUST:

- identify the compatibility-profile version it implements;
- produce structurally valid target documents;
- satisfy applicable target-format semantic requirements;
- preserve information required by the compatibility profile;
- fail explicitly or report every required lossy transformation.

### 25.6 Partial implementations

An implementation MAY support only selected schemas, profiles, modules, compatibility profiles, or operations.

A partial implementation MUST accurately declare its supported conformance scope and MUST NOT imply support for unimplemented capabilities.

### 25.7 Conformance fixtures

Normative compatibility profiles and profiles with behavior not fully expressible in schema SHOULD publish conformance fixtures or test vectors.

A conformance claim SHOULD identify the version of the conformance suite used for verification.

### 25.8 Scientific pressure-test fixtures

Profiles whose semantics include ranges, censored results, logarithmic values, derived states, or optimization behavior SHOULD publish fixtures that exercise those semantics rather than testing only ordinary scalar values.

The water capability SHOULD include conformance fixtures covering at least:

- exact values and ordinary reported averages;
- exact-ended ranges with an independently reported average;
- qualified ranges such as `ND–11.1`;
- one-sided bounds such as `<0.30`;
- non-detects without an invented detection limit;
- running annual average, locational running annual average, percentile, highest, and lowest statistics;
- result-specific timing that differs from the enclosing report period;
- separation of water identity, physical source, source-document publisher, analysis provider, and sample location;
- raw, finished, distribution, tap, or bottled stage context;
- separately reported alkalinity and bicarbonate;
- pH ranges without an invented midpoint;
- conductivity with and without an explicitly stated reference temperature;
- chloride and multiple disinfectant concepts coexisting without conflation;
- conflicting published target profiles remaining separate;
- multi-source blends with derived chemistry and nonlinearly treated properties;
- distinct treatment chemical forms such as anhydrous and hydrated salts;
- predicted treatment chemistry versus later measured chemistry;
- ranked optimization plans with policy, objective components, constraints, statuses, warnings, contribution explanations, and versions;
- explicit indeterminate or insufficient-data calculation results;
- external-format export with structured loss reporting;
- reuse of one source-water profile under different intended-use contexts.

---

## 26. Security, privacy, and operational safety

### 26.1 Untrusted input

Implementations MUST treat imported FermentationJSON and external-format documents as untrusted input.

Parsers, validators, importers, and processors SHOULD defend against:

- excessive nesting;
- oversized arrays or strings;
- resource-exhaustion inputs;
- malicious or cyclic references;
- path traversal;
- remote-reference abuse;
- parser discrepancies;
- duplicate JSON object member names;
- malformed numeric or Unicode input.

Processors SHOULD reject duplicate object member names before semantic interpretation because parser behavior may differ.

### 26.2 External references

Implementations SHOULD apply explicit policies to dereferencing external URIs.

Validation SHOULD NOT require unrestricted network access.

Implementations SHOULD support limits on:

- URI schemes;
- network destinations;
- redirects;
- response size;
- recursion depth;
- retrieval time;
- cached-content lifetime.

External resources used for reproducibility SHOULD support integrity verification where practical.

### 26.3 XML import

BeerXML and other XML importers SHOULD disable external entity resolution and other parser features that permit unintended local-file or network access unless explicitly required and safely sandboxed.

### 26.4 Personal and organizational information

FermentationJSON documents MAY contain names, contact details, locations, operator records, laboratory information, or other potentially sensitive metadata.

Applications SHOULD minimize collection, retention, and disclosure of personal information not required for the interchange purpose.

Profiles SHOULD NOT require personal information unless it is necessary for the domain use case.

### 26.5 Operational safety

FermentationJSON MAY describe equipment, controllers, setpoints, alarms, process instructions, or calculated operating conditions.

Successful validation establishes data conformance only. It does not establish that an instruction, setpoint, treatment, recipe, or control action is physically safe.

Systems that translate FermentationJSON data into physical actions MUST apply independent authorization, equipment limits, interlocks, process validation, and safety controls.

A FermentationJSON document MUST NOT be treated as executable safety logic solely because it conforms to the specification.

---

## 27. Normative and supporting specification artifacts

### 27.1 Artifact status

Every published specification artifact SHOULD clearly identify whether it is:

- normative;
- informative;
- experimental;
- deprecated.

An informative example, design note, proposal, or reference implementation MUST NOT override a normative requirement.

### 27.2 Normative release artifacts

A FermentationJSON release SHOULD include the normative artifacts required to implement and test the published behavior, including:

- normative schemas;
- normative specification documentation;
- versioned profiles and optional modules;
- versioned vocabularies;
- compatibility profiles and mappings where applicable.

### 27.3 Supporting artifacts

A release SHOULD also include supporting materials as appropriate:

- conformance fixtures and tests;
- valid and invalid examples;
- migration guidance;
- release notes.

Importers, exporters, validators, documentation generators, and reference implementations MAY be published with the specification but MUST be identified separately from normative artifacts.

### 27.4 Consistency of normative artifacts

Normative prose and normative machine-readable artifacts MUST be maintained consistently.

JSON Schemas define machine-validatable structural constraints. Normative documentation defines semantic and behavioral requirements, including requirements that cannot be expressed in JSON Schema.

A contradiction between normative artifacts is a specification defect and SHOULD be resolved through an erratum or subsequent release rather than by relying on undocumented implementation precedence.

Conformance tests MAY clarify intended behavior but MUST NOT introduce a normative requirement that is absent from the published normative specification.


### 27.5 JSON Schema dialect and authoring conventions

FermentationJSON normative schemas MUST use JSON Schema Draft 2020-12 unless a later FermentationJSON specification version deliberately adopts another dialect.

Each schema resource MUST declare the Draft 2020-12 dialect using `$schema`.

Normative schema resources MUST define a stable absolute `$id` using the versioned identifier policy in Section 24.3. Repository file paths and temporary retrieval URIs are not schema identity.

Schemas SHOULD:

- use `$defs` for reusable local definitions;
- use `$anchor` when a location-independent schema reference is useful;
- avoid JSON Pointer references that cross schema-resource boundaries;
- use `unevaluatedProperties` rather than duplicating property declarations solely to close composed schemas;
- avoid custom JSON Schema vocabularies in the initial foundation unless a requirement cannot be expressed interoperably through standard Draft 2020-12 mechanisms.

The default Draft 2020-12 dialect treats `format` primarily as annotation. FermentationJSON schemas MAY use standard `format` annotations, but full conformance tooling MUST enforce any date-time, URI, UUID, or other formatted-string semantics that FermentationJSON makes normative. Structural validation alone MUST NOT be assumed to enforce every `format` annotation.

The canonical JSON Schema URI namespace and schema-set resolution policy are defined in Section 24.3 and ADR-0005. Once published, an identifier MUST follow the immutability requirements in Section 24.

---

## 28. Development sequence

This section is informative. It describes the intended order of implementation and does not define release conformance.

Development is organized by technical dependency:

1. **Foundation**  
   Define document architecture, identifiers, references, quantities, measurements, provenance, profiles, extensions, compatibility, versioning, validation, and conformance.

2. **Core brewing**  
   Define brewing recipes and batches, ingredients and cultures, equipment, brewing processes, packaging, water, measurements, calculations, and external-format compatibility tooling.

3. **Engineering modules**  
   Add laboratory data, sampling, sensors, calibration, telemetry, automation, detailed process execution, batch genealogy, advanced water treatment, and serving-system engineering.

4. **Additional fermentation domains**  
   Add domain profiles for wine, cider, perry, mead, sake, kombucha, vinegar, and other fermentation processes.

Detailed milestones, release targets, and sequencing are maintained in `ROADMAP.md`.

A roadmap item is not part of the normative specification until it is incorporated into a published, versioned normative artifact.

---

## 29. Open design decisions

The following topics remain unresolved and require a proposal, architecture decision, implementation experiment, or combination of these before they become normative:

- canonical public URI namespace and final URI structure for published schemas, profiles, modules, vocabularies, and compatibility profiles;
- multi-document packaging or container format, if one is required;
- attachment and external-dataset representation;
- extension namespace registration and vocabulary governance;
- digital-signature and integrity mechanisms beyond basic checksums;
- JSON-LD or ontology integration;
- streaming or high-frequency telemetry representation;
- long-term archival and preservation guidance.

The existence of an open design decision MUST NOT be interpreted as permission for incompatible implementations to assign conflicting normative meanings to the same FermentationJSON identifier.

Experimental implementations MAY explore unresolved areas through the extension and proposal mechanisms defined by this specification.

Open design decisions are not normative requirements.

---

## 30. Document status and change control

This document is a working engineering design for the modern FermentationJSON specification.

Normative terms in this working draft state the current intended requirements, but they do not constitute a released compatibility guarantee until incorporated into a published FermentationJSON specification version.

During pre-release development:

- field names and schema structures MAY change;
- unresolved design decisions MAY result in incompatible revisions;
- normative requirements SHOULD change only with documented rationale;
- significant architectural changes SHOULD be recorded through an architecture decision or proposal;
- compatibility guarantees MUST NOT be advertised as final until corresponding schemas, mappings, fixtures, and conformance tests exist.

The following architectural decisions are considered established design constraints unless deliberately revised:

- recipes and executed batches are distinct concepts;
- canonical and reported quantity representations are distinct;
- source-reported and derived information are distinct;
- semantic qualifiers, ranges, bounds, non-detects, and uncertainty are preserved;
- logarithmic quantities such as pH require quantity-specific aggregation rules;
- provenance is a cross-cutting capability;
- external-format compatibility is versioned and testable;
- lossy transformations are explicit;
- profiles and extensions cannot weaken core requirements;
- JSON Schema validation alone does not establish full conformance;
- source-water identity is independent of intended use;
- water-report document identity, physical water source, water stage, and sample location are distinct concepts;
- regulatory or advisory thresholds are distinct from observed chemistry;
- predicted treatment results are distinct from measured treated-water results;
- treatment-chemical identity includes chemically meaningful form such as hydration state.
- normative unit and quantity-kind identifiers are defined by versioned FermentationJSON vocabularies;
- every registered core quantity kind has one declared canonical unit;
- normative JSON Schema resources have versioned absolute canonical `$id` values;
- schema resolution is independent of repository filesystem location and does not require network access;

Implementation-blocking architectural decisions SHOULD be recorded in `docs/decisions/` and reflected in this design document when they become established constraints.

Detailed vocabulary contents and profile-specific structures remain subject to implementation and review until published. The current schema identifier namespace is an accepted pre-release decision and remains changeable only through an explicit superseding decision before first normative publication.

A released version of this document MUST identify its specification version and normative status unambiguously.
