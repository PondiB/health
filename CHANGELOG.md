# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Definitions (value/meaning tables) for all Health enum fields in the README.

### Changed

### Deprecated

### Removed

### Fixed

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
