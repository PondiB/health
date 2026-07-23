# Health Extension Specification

- **Title:** Health
- **Identifier:** <https://stac-extensions.github.io/health/v0.1.0/schema.json>
- **Field Name Prefix:** health
- **Scope:** Item, Collection
- **Extension [Maturity Classification](https://github.com/radiantearth/stac-spec/tree/master/extensions/README.md#extension-maturity):** Proposal
- **Owner**: [@PondiB](https://github.com/PondiB)

This document explains the Health Extension to the [SpatioTemporal Asset Catalog](https://github.com/radiantearth/stac-spec) (STAC) specification.

It adds domain metadata for **geospatial public-health and epidemic-intelligence** datasets: disease outcomes and surveillance snapshots,
environmental and socio-demographic determinants (covariates), and model outputs such as risk maps. It is **not** a clinical EHR, imaging, or FHIR
profile.

Design principles:

1. **Thin required core** — only `health:data_type` is always required on Items; further fields are conditionally required.
2. **Reuse before reinvention** — citation, grids, tables, CRS, ML models, file checksums, and geometry anonymization stay in existing extensions (see
  [Reused extensions](#reused-extensions)). Examples demonstrate a subset; apply additional extensions when the asset type needs them.
3. **Privacy fields are first-class** — GDPR/access and statistical disclosure-control fields are defined in-schema. They are not always
  required: national open aggregates may honestly use `minimum_cell_size: 1` with `suppression_method: none`. Use a real suppression method
  (and cell size ≥ your rule) when small-area cells are protected — see the suppressed fixture example.
4. **Surveillance is versioned** — provisional counts are revised; vintage fields and byte-pinned assets make nowcasts reproducible.

- Examples (real open assets unless noted):
  - [Collection example](examples/collection.json): ECDC COVID-19 EU/EEA daily open data
  - [Surveillance Item](examples/item-surveillance.json): ECDC national daily CSV (`aggregated_published`,
    `suppression_method: none`) with `predecessor-version` link
  - [Provisional surveillance Item](examples/item-surveillance-provisional.json): byte-pinned CSV truncated at
    2021-06-30 (`revision_status: provisional`)
  - [Suppressed fixture](examples/item-surveillance-suppressed.json): illustrative NUTS-3 counts with
    `minimum_cell_size: 5` and `suppression_method: primary_only` (not an official release)
  - [NUTS-3 surveillance Item](examples/item-surveillance-nuts.json): Italy PCM-DPC province COVID CSV with
    `spatial_unit` / `spatial_unit_version` and GISCO NUTS 2021 join link
  - [Germany surveillance Item](examples/item-surveillance-germany.json): RKI COVID-19 hospitalisation counts by
    Bundesland (`hospitalisation`, `NUTS1` / `NUTS2021`, commit-pinned)
  - [Germany incidence Item](examples/item-surveillance-incidence.json): RKI 7-day hospitalisation incidence
    (`incidence_rate` + `population_denominator`)
  - [VectAbundance Item](examples/item-vector-vectabundance.json): *Aedes* observation database
    (`vector_occurrence`)
  - [WNV host competence Item](examples/item-host-wnv-competence.json): avian host competence / prevalence
    tables
  - [Covariate Item](examples/item-covariate.json): ERA5-Land weekly 2 m temperature (Zenodo)
  - [WorldPop covariate](examples/item-covariate-worldpop.json): gridded population total
  - [Hospital-density covariate](examples/item-covariate-hospital-density.json): admin-2 hospital density
  - [MODIS EVI covariate](examples/item-covariate-modis-evi.json): vegetation index 2022
  - [Model-output Item](examples/item-model-output.json): WNV *Culex* suitability models with MLM metadata
    and `derived_from` → VectAbundance (Zenodo)
  - [*Ixodes* model-output Item](examples/item-model-ixodes.json): tick suitability / presence–absence
    models
- [JSON Schema](json-schema/schema.json)
- [Changelog](./CHANGELOG.md)

## Fields

The fields in the table below can be used in these parts of STAC documents:

- [ ] Catalogs
- [x] Collections
- [x] Item Properties (incl. Summaries in Collections)
- [x] Assets (for both Collections and Items, incl. Item Asset Definitions in Collections)
- [ ] Links

| Field Name | Type | Description |
| --- | --- | --- |
| health:data_type | [Data Type](#data-type) | **REQUIRED** (Item). Semantic class of the record. |
| health:disease_codes | \[string] | ICD-10/11 (or equivalent) disease/condition codes. Conditionally required for non-covariate Items unless `pathogen_taxon_ids` is set (model outputs may omit both when the target is declared elsewhere). |
| health:pathogen_taxon_ids | \[string] | NCBI Taxonomy IDs (or CURIE form). Alternative or complement to disease codes. |
| health:spatial_unit | string | Spatial reporting unit (e.g. `NUTS3`, `NUTS2`, `LAU`, `MSOA`, `grid_1km`, `national`). |
| health:spatial_unit_version | string | Classification vintage of `spatial_unit` (e.g. `NUTS2021`, `NUTS2024`, `LAU2023`). |
| health:reference_date_type | [Reference Date Type](#reference-date-type) | Which event the temporal properties refer to. |
| health:reporting_lag_days | [Reporting Lag Object](#reporting-lag-object) | Days between the reference event and data availability. |
| health:temporal_resolution | [Temporal Resolution](#temporal-resolution) | Reporting cadence. |
| health:week_system | [Week System](#week-system) | **REQUIRED** when `temporal_resolution` is `weekly`. |
| health:spatial_coverage | \[string] | ISO 3166-1 alpha-3 country codes (typically Collection-level). |
| health:access_level | [Access Level](#access-level) | How the data may be obtained. |
| health:gdpr_status | [GDPR Status](#gdpr-status) | Privacy / identifiability class of the payload. |
| health:minimum_cell_size | integer | **REQUIRED** when `gdpr_status` is `aggregated_published` or `anonymised`. Smallest publishable count (or equivalent). |
| health:suppression_method | [Suppression Method](#suppression-method) | **REQUIRED** when `gdpr_status` is `aggregated_published` or `anonymised`. |
| health:population_denominator | [Population Denominator Object](#population-denominator-object) | **REQUIRED** when `data_type` is `incidence_rate` or `mortality_rate`. |
| health:vector_species | \[string] | GBIF or NCBI taxon IDs for vector species (vector-borne use cases). |
| health:sex_disaggregated | boolean | Whether sex-disaggregated values are present. |
| health:age_bands_available | \[string] | Age-band labels present in the data. |
| health:completeness_score | number | Fraction of expected records present (0–1). |
| health:surveillance_type | [Surveillance Type](#surveillance-type) | How cases are ascertained. |
| health:case_definition_url | string (URI) | Case-definition document. |
| health:data_source_system | string | Surveillance system or registry (e.g. `ecdc_tessy`, `ukhsa`, `gbif`). |
| health:ascertainment_note | string | Known under-reporting or ascertainment bias. |
| health:data_use_agreement_url | string (URI) | DUA / licence process for controlled data. |
| health:data_controller | string | Data controller (and optionally DPO contact). |
| health:countermeasures_period | boolean | Whether NPIs or vaccination campaigns were active in the period. |
| health:outbreak_phase | [Outbreak Phase](#outbreak-phase) | Epidemic phase label for the period. |
| health:data_version | string | Publisher version / release tag for this snapshot. |
| health:data_as_of | string (RFC 3339) | Vintage datetime when this snapshot was current at the source. |
| health:revision_status | [Revision Status](#revision-status) | provisional / revised / final. |
| health:uncertainty_type | [Uncertainty Type](#uncertainty-type) | How uncertainty is represented for `model_output` assets. |
| health:bias_evaluation_url | string (URI) | Bias evaluation (e.g. sex, age, geography) for health AI outputs. |

Collection placement: `health:spatial_coverage`, `health:access_level`, `health:data_use_agreement_url`, and `health:data_controller` are typically
set on the Collection as catalogue defaults. STAC does **not** inherit Collection properties onto Items — repeat or override fields on each Item
(and use Collection `summaries` for discovery). Summaries SHOULD list the `health:data_type` and `health:disease_codes` (or pathogen)
values present in member Items.

### Additional Field Information

#### health:data_type

Discriminates outcome, determinant, and prediction assets so one extension can cover all three without separate namespaces.
Covariate Items SHOULD use only light health tagging (`data_type` plus optional disease/pathogen keywords for discoverability); grid structure belongs
in [Datacube](https://github.com/stac-extensions/datacube) / [Raster](https://github.com/stac-extensions/raster) /
[Projection](https://github.com/stac-extensions/projection).

#### health:disease_codes and health:pathogen_taxon_ids

Prefer stable vocabularies (ICD-10/11, NCBI Taxonomy). At least one of these arrays is required for Items whose `data_type` is not `covariate`, except
`model_output` Items that declare their target via linked training labels or Collection summaries.

#### health:spatial_unit and health:spatial_unit_version

Administrative units change. A multi-year TESSy series can span several NUTS revisions; omitting the vintage silently breaks joins.

#### health:week_system

ISO weeks, ECDC epi weeks, and CDC MMWR weeks can disagree by up to a week at year boundaries. Required whenever `temporal_resolution` is `weekly`.

#### Privacy and disclosure control

`health:gdpr_status` describes the *payload*, not only the licence. Labels are GDPR-oriented (common for EU/EHDS
catalogues) but the field is usable as a general privacy/identifiability class elsewhere. When data are aggregated or
anonymised for release, `health:minimum_cell_size` and `health:suppression_method` are required so
secondary/complementary suppression is explicit. `suppression_method: none` with `minimum_cell_size: 1` means no
disclosure control was applied (valid for coarse national aggregates). For coarse geometries, also consider the [Anonymized
Location](https://github.com/stac-extensions/anonymized-location) extension (`anon:size`, `anon:warning`).

#### Surveillance vintage

`health:data_version`, `health:data_as_of`, and `health:revision_status` make each ingested snapshot reproducible.
Prefer byte-pinned assets (`file:checksum`, commit-pinned or repository-hosted snapshots) over mutable portal URLs for
provisional vintages. Prefer STAC link relation `predecessor-version` when an Item supersedes an earlier snapshot, and
`derived_from` from model-output Items back to the surveillance or observation Items used as labels.

#### Model outputs and embeddings

Describe the *model* with the [Machine Learning Model (MLM)](https://github.com/stac-extensions/mlm)
extension and scientific citations with [Scientific](https://github.com/stac-extensions/scientific).
This extension only adds health-specific prediction metadata: `health:uncertainty_type` and
`health:bias_evaluation_url` (set the latter when a bias/fairness evaluation is published).

Geospatial foundation-model **embedding tensors** (dimensions, chip layout, inference runtime, quantization,
`emb:source-data` / `emb:model` links) are **out of scope** for `health:`. Use the community
[Embedding extension](https://github.com/geo-embeddings/embeddings-stac-specification) (`emb:` prefix;
Proposal) together with MLM for the encoder. A health catalogue Item that *uses* embeddings as features
still declares `health:data_type` (`covariate` or `model_output` as appropriate) and links to the embedding
Items/Collections.

### Data Type

| Value | Meaning |
| --- | --- |
| `case_reports` | Case counts or line-list aggregates |
| `incidence_rate` | Incidence rates (requires population denominator) |
| `mortality` | Death counts |
| `mortality_rate` | Mortality rates (requires population denominator) |
| `hospitalisation` | Hospital admission / occupancy metrics |
| `seroprevalence` | Serological prevalence |
| `syndromic_surveillance` | Syndromic indicators |
| `environmental_sampling` | Pathogen detection in environment |
| `vector_occurrence` | Vector presence / abundance |
| `covariate` | Environmental or socio-demographic determinant |
| `model_output` | Predicted risk, nowcast, or similar product |

### Reference Date Type

`symptom_onset` | `diagnosis` | `notification` | `death` | `specimen_collection` | `other`

### Temporal Resolution

`event` | `daily` | `weekly` | `monthly` | `quarterly` | `annual` | `multi_year` | `other`

### Week System

`iso_8601` | `ecdc` | `mmwr`

### Access Level

`open` | `registered` | `controlled_access` | `consortium_only`

### GDPR Status

`open_data` | `aggregated_published` | `anonymised` | `pseudonymised` | `restricted_identifiable`

### Suppression Method

`none` | `primary_only` | `complementary` | `rounding` | `k_anonymity`

### Surveillance Type

`universal_mandatory` | `sentinel` | `voluntary` | `passive` | `active` | `other`

### Outbreak Phase

`endemic_baseline` | `emerging` | `epidemic_peak` | `declining` | `unknown`

### Revision Status

`provisional` | `revised` | `final`

### Uncertainty Type

`none` | `prediction_interval` | `posterior_variance` | `ensemble_spread`

### Reporting Lag Object

| Field Name | Type | Description |
| --- | --- | --- |
| min | number | **REQUIRED**. Minimum lag in days. |
| max | number | **REQUIRED**. Maximum lag in days (`max` MUST be ≥ `min`). |

### Population Denominator Object

| Field Name | Type | Description |
| --- | --- | --- |
| source | string | **REQUIRED**. Population dataset or statistic (e.g. `eurostat`, `worldpop`). |
| vintage_year | integer | **REQUIRED**. Reference year of the population figures. |
| value | number | Optional scalar denominator when a single value applies. |

## Relation types

Use STAC-native link relations rather than custom health relation types:

| Type | Description |
| --- | --- |
| predecessor-version | Prior surveillance snapshot superseded by this Item |
| successor-version | Newer revision of this snapshot |
| derived_from | Model-output or processed Item derived from this Item |
| cite-as | Canonical citation landing page (with `sci:` fields) |

## Reused extensions

| Concern | Extension | Notes |
| --- | --- | --- |
| Citation / DOI | [scientific](https://github.com/stac-extensions/scientific) | `sci:doi`, `sci:citation`, `sci:publications` |
| Class labels | [classification](https://github.com/stac-extensions/classification) | Risk categories, outbreak-phase codings in rasters |
| Tabular / GeoParquet schema | [table](https://github.com/stac-extensions/table) | Column names and dtypes |
| Multi-dimensional arrays | [datacube](https://github.com/stac-extensions/datacube) | `cube:dimensions` / variables |
| CRS / grid | [projection](https://github.com/stac-extensions/projection) | `proj:code`, shape, transform |
| File size / checksum | [file](https://github.com/stac-extensions/file) | `file:checksum`, size |
| Processing lineage | [processing](https://github.com/stac-extensions/processing) | Processing graph / facility |
| Auth to assets | [authentication](https://github.com/stac-extensions/authentication) | Controlled-access download flows |
| Coarse geometry | [anonymized-location](https://github.com/stac-extensions/anonymized-location) | `anon:size`, `anon:warning` |
| ML model cards / runtime | [mlm](https://github.com/stac-extensions/mlm) | Model identity, artifacts, training refs |
| Geospatial embeddings | [emb (Embedding)](https://github.com/geo-embeddings/embeddings-stac-specification) | FM embedding products (`emb:dimensions`, chip layout, inference provenance); do not fold into `health:` |

## HealthDCAT-AP / EHDS

Catalogues that also publish HealthDCAT-AP / EHDS secondary-use records can map from these fields (and core STAC) in a companion profile. That
crosswalk is **not** part of this JSON Schema. Pin the HealthDCAT-AP version used by any catalogue export in the deploying project's documentation.

## Contributing

All contributions are subject to the
[STAC Specification Code of Conduct](https://github.com/radiantearth/stac-spec/blob/master/CODE_OF_CONDUCT.md).
For contributions, please follow the
[STAC specification contributing guide](https://github.com/radiantearth/stac-spec/blob/master/CONTRIBUTING.md). Instructions
for running tests are copied here for convenience.

### Running tests

The same checks that run as checks on PR's are part of the repository and can be run locally to verify that changes are valid.
To run tests locally, you'll need `npm`, which is a standard part of any
[node.js installation](https://nodejs.org/en/download/).

First you'll need to install everything with npm once. Just navigate to the root of this repository and on
your command line run:

```bash
npm ci
```

Then to check markdown formatting and test the examples against the JSON schema, you can run:

```bash
npm test
```

This will spit out the same texts that you see online, and you can then go and fix your markdown or examples.

If the tests reveal formatting problems with the examples, you can fix them with:

```bash
npm run format-examples
```
