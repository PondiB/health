# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- GEOAI4EI minimalistic profile (branch `geoai4ei`): 16-field subset of the full specification.
- `host_distribution` value in the `data_type` enum for species distribution and suitability maps.
- MOOD metadata crosswalk table mapping ISO 19115 / INSPIRE attributes to STAC fields.
- Thirteen GEOAI4EI examples covering all MOOD data types:
  - Covariates (5): ERA5-Land temperature, ERA5 precipitation (Fourier), VIIRS vegetation (Fourier),
    ERA5 relative humidity (Fourier), wind speed and direction.
  - Vectors (2): *Aedes sticticus* mosquito, *Dermacentor reticulatus* tick.
  - Hosts (3): wild boar (*Sus scrofa*), Laridae seabirds, common vole (*Microtus arvalis*).
  - Epidemiological (2): RVF cases (Mauritania/Senegal), Ebola news (DRC/Uganda).
  - Model output (1): WNV *Culex* suitability (Europe).
- Disease scenario coverage table for RVF, CCHF, Ebola, HPAI, WNV, TBE, Hanta, MPOX.
- Collection example for GEOAI4EI environmental covariates.

### Changed

- Schema trimmed to 16 optional/conditional fields (from 30+ on `main`).
- Only one conditional requirement remains: `week_system` when `temporal_resolution` is `weekly`.
- Relaxed: `disease_codes` / `pathogen_taxon_ids` no longer conditionally required on non-covariate Items.
- `data_type` enum reduced to 9 values relevant to GEOAI4EI (dropped `hospitalisation`,
  `seroprevalence`, `syndromic_surveillance`).

### Removed

- Surveillance-vintage fields: `reference_date_type`, `reporting_lag_days`, `revision_status`.
- Disclosure-control fields: `minimum_cell_size`, `suppression_method`.
- Demographic-disaggregation fields: `population_denominator`, `sex_disaggregated`, `age_bands_available`.
- Surveillance fields: `surveillance_type`, `case_definition_url`, `ascertainment_note`.
- Governance fields: `data_use_agreement_url`, `data_controller`.
- Context fields: `countermeasures_period`, `outbreak_phase`.
- AI fairness field: `bias_evaluation_url`.
- All prior surveillance-oriented examples (ECDC, RKI, PCM-DPC, etc.) and `examples/assets/`.

## [0.1.0] - 2026-07-23

### Added

- Initial Health Extension Proposal (`v0.1.0`) for geospatial public-health and epidemic-intelligence datasets.
- Fields for data type, disease/pathogen coding, spatial reporting units, temporal cadence, privacy/disclosure control, and surveillance vintage.
- Examples (real open assets unless noted): ECDC / RKI / PCM-DPC surveillance; VectAbundance *Aedes* observations;
  WNV host competence tables; ERA5, WorldPop, hospital density, MODIS EVI covariates; *Culex* and
  *Ixodes* spatial model outputs (Zenodo DOIs from the open-data list).
- Byte-pinned provisional ECDC CSV under `examples/assets/` with `file:checksum`.
- Illustrative primary-suppression fixture (`minimum_cell_size: 5`, `suppression_method: primary_only`).
- RKI `incidence_rate` example with `population_denominator`; model Item `derived_from` → VectAbundance.
- Document reuse of the community Embedding extension (`emb:`) for geospatial FM embedding products.
- Reuse guidance for scientific, datacube, table, classification, projection, file, processing, authentication, anonymized-location, and MLM
  extensions.

### Changed

- Schema URI and package version set to Proposal `0.1.0` (not a stable `1.0.0` release).

[Unreleased]: <https://github.com/PondiB/health/compare/v0.1.0...HEAD>
[0.1.0]: <https://github.com/PondiB/health/releases/tag/v0.1.0>
