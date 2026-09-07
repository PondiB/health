# Health Extension Specification — GEOAI4EI Profile

- **Title:** Health
- **Identifier:** <https://stac-extensions.github.io/health/v0.1.0/schema.json>
- **Field Name Prefix:** health
- **Scope:** Item, Collection, Asset
- **Extension [Maturity Classification](https://github.com/radiantearth/stac-spec/tree/master/extensions/README.md#extension-maturity):** Proposal
- **Owner**: [@PondiB](https://github.com/PondiB)
- **Profile:** GEOAI4EI minimalistic (branch `geoai4ei`)

This is a **minimalistic profile** of the [Health Extension](https://github.com/PondiB/health) for the
[GEOAI4EI](https://geoai4ei.eu/) project. It retains only the fields needed to catalogue the project's
geospatial epidemic-intelligence datasets — environmental covariates, vector and host distributions,
epidemiological case data, and model outputs — without the surveillance-vintage, disclosure-control,
and demographic-disaggregation machinery of the full specification on `main`.

Design principles:

1. **Single required field** — only `health:data_type` is required on Items.
2. **One conditional** — `health:week_system` is required when `temporal_resolution` is `weekly`.
3. **Reuse before reinvention** — CRS, grids, citations, and tabular schemas stay in existing STAC extensions.
4. **MOOD metadata alignment** — fields map to the ISO 19115 / INSPIRE subset used by the MOOD GeoNetwork catalogue.

Examples:

- [Collection](examples/collection.json): GEOAI4EI environmental covariates — Europe

Covariates (environmental and climatic determinants from Zenodo / GeoNetwork):

- [Temperature](examples/item-covariate-temperature.json): ERA5-Land daily 2 m air temperature (Zenodo)
- [Precipitation](examples/item-covariate-precipitation.json): ERA5 precipitation Fourier-processed (Zenodo)
- [Vegetation](examples/item-covariate-vegetation.json): VIIRS Fourier-processed 1 km — NDVI, EVI, LST (Zenodo)
- [Humidity](examples/item-covariate-humidity.json): ERA5 relative humidity Fourier-processed (Zenodo)
- [Wind](examples/item-covariate-wind.json): Wind speed and direction (E4Warning / Zenodo)

Vectors (arthropod occurrence and distribution):

- [*Aedes sticticus*](examples/item-vector-aedes.json): flood-water mosquito occurrence and suitability (RVF, WNV)
- [*Dermacentor reticulatus*](examples/item-vector-dermacentor.json): ornate cow tick distribution (CCHF, babesiosis)

Hosts (reservoir and sentinel species):

- [Wild boar](examples/item-host-wildboar.json): *Sus scrofa* distribution — TBE, HPAI (INRAE)
- [Seabirds](examples/item-host-laridae.json): Laridae (gulls, terns) colony density — HPAI (INRAE)
- [Common vole](examples/item-host-rodent.json): *Microtus arvalis* distribution — Hanta, tularaemia (CIRAD)

Epidemiological (case data and event-based surveillance):

- [RVF cases](examples/item-epidemiological-rvf.json): Rift Valley Fever — Mauritania and Senegal 2025 (CIRAD)
- [Ebola news](examples/item-epidemiological-ebola-news.json): Google News curated dataset — DRC and Uganda 2026 (CIRAD)

Model outputs:

- [WNV *Culex* suitability](examples/item-model-wnv-suitability.json): West Nile Virus vector suitability — Europe 2024

Disease scenario coverage in examples (via `health:disease_codes` / `health:pathogen_taxon_ids`):

| Disease | ICD-10 | Example(s) |
| --- | --- | --- |
| Rift Valley Fever (RVF) | A92.4 | RVF cases, *Aedes* vector |
| Crimean-Congo Haemorrhagic Fever (CCHF) | A98.0 | *Dermacentor* vector |
| Ebola | A98.4 | Ebola news |
| Highly Pathogenic Avian Influenza (HPAI) | J09 | Laridae seabirds, wild boar |
| West Nile Virus (WNV) | A92.3 | WNV model output, *Aedes* vector |
| Tick-borne Encephalitis (TBE) | A84 | Wild boar |
| Hantavirus | A98.5 | Common vole |
| Monkeypox (MPOX) | B04 | (no example yet — human-to-human scenario) |

Additional links: `SARSCov` is covered by the full spec on `main` (ECDC examples). Tularaemia (`A21`) appears
alongside hantavirus in the common vole example.

Further resources:

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
| health:disease_codes | \[string] | ICD-10/11 (or equivalent) disease/condition codes. |
| health:pathogen_taxon_ids | \[string] | NCBI Taxonomy IDs (or CURIE form). |
| health:vector_species | \[string] | GBIF or NCBI taxon IDs for vector species. |
| health:spatial_unit | string | Spatial reporting unit (e.g. `grid_1km`, `NUTS3`, `national`). |
| health:spatial_unit_version | string | Classification vintage of `spatial_unit` (e.g. `NUTS2021`). |
| health:temporal_resolution | [Temporal Resolution](#temporal-resolution) | Reporting or aggregation cadence. |
| health:week_system | [Week System](#week-system) | **REQUIRED** when `temporal_resolution` is `weekly`. |
| health:spatial_coverage | \[string] | ISO 3166-1 alpha-3 country codes. |
| health:access_level | [Access Level](#access-level) | How the data may be obtained. |
| health:gdpr_status | [GDPR Status](#gdpr-status) | Privacy / identifiability class of the payload. |
| health:data_version | string | Publisher version / release tag for this snapshot. |
| health:data_source_system | string | Source system or registry (e.g. `era5_land`, `gbif`, `cirad`). |
| health:data_as_of | string (RFC 3339) | Vintage datetime when this snapshot was current. |
| health:completeness_score | number (0–1) | Fraction of expected records present. |
| health:uncertainty_type | [Uncertainty Type](#uncertainty-type) | How uncertainty is represented for `model_output` assets. |

### Data Type

| Value | Meaning |
| --- | --- |
| `case_reports` | Case counts, line-list aggregates, or event-based reports |
| `mortality` | Death counts |
| `incidence_rate` | Incidence rates |
| `mortality_rate` | Mortality rates |
| `vector_occurrence` | Vector presence / abundance / suitability |
| `host_distribution` | Host species distribution, density, or suitability |
| `covariate` | Environmental or socio-demographic determinant |
| `model_output` | Predicted risk, nowcast, or similar product |
| `environmental_sampling` | Pathogen detection in environment |

### Temporal Resolution

| Value | Meaning |
| --- | --- |
| `event` | Individual events or irregular timestamps |
| `daily` | One value per calendar day |
| `weekly` | One value per epidemiological or calendar week |
| `monthly` | One value per calendar month |
| `quarterly` | One value per calendar quarter |
| `annual` | One value per calendar year |
| `multi_year` | Values over a span longer than one year (e.g. Fourier-processed composites) |
| `other` | Another cadence; explain in `description` |

### Week System

| Value | Meaning |
| --- | --- |
| `iso_8601` | ISO 8601 weeks (Monday start) |
| `ecdc` | ECDC epidemiological weeks |
| `mmwr` | US CDC MMWR weeks (Sunday start) |

### Access Level

| Value | Meaning |
| --- | --- |
| `open` | Freely downloadable without registration |
| `registered` | Requires account / registration |
| `controlled_access` | Requires application or DUA before download |
| `consortium_only` | Restricted to a named project or partnership |

### GDPR Status

| Value | Meaning |
| --- | --- |
| `open_data` | Non-personal or published as open data |
| `aggregated_published` | Aggregated statistics released publicly |
| `anonymised` | Treated as anonymised for release |
| `pseudonymised` | Identifiers replaced; re-identification possible with additional info |
| `restricted_identifiable` | Contains personal data; not safe for open release |

### Uncertainty Type

| Value | Meaning |
| --- | --- |
| `none` | Point estimate only |
| `prediction_interval` | Prediction or confidence intervals |
| `posterior_variance` | Bayesian posterior variance / credible intervals |
| `ensemble_spread` | Spread across ensemble members |

## MOOD Metadata Crosswalk

The MOOD project metadata requirements (ISO 19115 / INSPIRE subset from the GeoNetwork catalogue)
map to STAC fields as follows:

| MOOD attribute | STAC / extension field |
| --- | --- |
| Title | `title` (core STAC) |
| Abstract | `description` (core STAC) |
| Spatial resolution | `health:spatial_unit` or `proj:transform` |
| Temporal resolution | `health:temporal_resolution` |
| Temporal extent | `start_datetime` / `end_datetime` (core STAC) |
| Data unit | `description` or `cube:variables` |
| CRS (EPSG) | `proj:code` (Projection extension) |
| Download and links | `assets` + `links` (core STAC) |
| Categories / Keywords | `keywords` (Collection) or `description` |
| Status | `health:data_version` |
| Update frequency | `health:temporal_resolution` |
| Format | Asset `type` (media type) |
| Lineage | `description` or Processing extension |
| Contact | `health:data_source_system` or Collection `providers` |
| Identifier | `id` (core STAC) |

## Reused extensions

| Concern | Extension | Notes |
| --- | --- | --- |
| Citation / DOI | [scientific](https://github.com/stac-extensions/scientific) | `sci:doi`, `sci:citation` |
| CRS / grid | [projection](https://github.com/stac-extensions/projection) | `proj:code`, shape, transform |
| Multi-dimensional arrays | [datacube](https://github.com/stac-extensions/datacube) | `cube:dimensions` / variables |
| Tabular schema | [table](https://github.com/stac-extensions/table) | Column names and dtypes |
| File size / checksum | [file](https://github.com/stac-extensions/file) | `file:checksum`, size |
| ML model cards | [mlm](https://github.com/stac-extensions/mlm) | Model identity, artifacts, training refs |
| Item asset definitions | [item-assets](https://github.com/stac-extensions/item-assets) | Collection-level asset templates |

## Differences from the full specification (`main`)

This profile **removes** the following fields (available on `main` for surveillance-heavy use cases):

- Surveillance vintage: `health:reference_date_type`, `health:reporting_lag_days`, `health:revision_status`
- Disclosure control: `health:minimum_cell_size`, `health:suppression_method`
- Demographic: `health:population_denominator`, `health:sex_disaggregated`, `health:age_bands_available`
- Surveillance: `health:surveillance_type`, `health:case_definition_url`, `health:ascertainment_note`
- Governance: `health:data_use_agreement_url`, `health:data_controller`
- Context: `health:countermeasures_period`, `health:outbreak_phase`
- AI fairness: `health:bias_evaluation_url`

This profile **adds**:

- `host_distribution` to the `data_type` enum (species distribution and suitability maps).

This profile **relaxes**:

- Conditional requirement for `disease_codes` or `pathogen_taxon_ids` on non-covariate Items (now optional).
- Conditional requirement for `minimum_cell_size` and `suppression_method` on aggregated/anonymised data (fields removed).
- Conditional requirement for `population_denominator` on rate types (field removed).

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
