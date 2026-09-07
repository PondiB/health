"""
PySTAC usage examples for the STAC Health Extension.

Demonstrates reading, querying, creating, and validating Items
with health: fields — no PySTAC modifications required.

Requirements:
    pip install pystac jsonschema
"""

import json
from pathlib import Path

import pystac

EXAMPLES_DIR = Path(__file__).parent


def get_health_fields(item: pystac.Item) -> dict:
    """Return only the health: prefixed properties."""
    return {k: v for k, v in item.properties.items() if k.startswith("health:")}


def load_all_items(directory: Path) -> list[pystac.Item]:
    """Load all STAC Item JSON files from a directory."""
    items = []
    for f in sorted(directory.glob("item-*.json")):
        items.append(pystac.Item.from_file(str(f)))
    return items


def search_items_by_health(
    items: list[pystac.Item],
    data_type: str | None = None,
    disease_code: str | None = None,
    country: str | None = None,
    access_level: str | None = None,
) -> list[pystac.Item]:
    """Filter a list of STAC Items by health extension fields."""
    results = items
    if data_type:
        results = [
            it for it in results
            if it.properties.get("health:data_type") == data_type
        ]
    if disease_code:
        results = [
            it for it in results
            if disease_code in (it.properties.get("health:disease_codes") or [])
        ]
    if country:
        results = [
            it for it in results
            if country in (it.properties.get("health:spatial_coverage") or [])
        ]
    if access_level:
        results = [
            it for it in results
            if it.properties.get("health:access_level") == access_level
        ]
    return results


HEALTH_SCHEMA_CONTEXT = """
The STAC Health Extension adds these fields to geospatial datasets:

Required:
- health:data_type: one of case_reports, mortality, incidence_rate, mortality_rate,
  vector_occurrence, host_distribution, covariate, model_output, environmental_sampling

Optional:
- health:keywords: subject keywords for faceted search (e.g. ["ERA5", "temperature"])
- health:disease_codes: ICD-10/11 codes (e.g. "A92.3" for WNV, "A98.4" for Ebola)
- health:pathogen_taxon_ids: NCBI Taxonomy IDs (e.g. "NCBITaxon:11082" for WNV)
- health:vector_species: GBIF/NCBI taxon IDs for vector species
- health:spatial_unit: grid_1km, NUTS3, national, etc.
- health:temporal_resolution: event, daily, weekly, monthly, annual, multi_year
- health:week_system: iso_8601, ecdc, mmwr (required when weekly)
- health:spatial_coverage: ISO 3166-1 alpha-3 country codes
- health:access_level: open, registered, controlled_access, consortium_only
- health:gdpr_status: open_data, aggregated_published, anonymised, pseudonymised,
  restricted_identifiable
- health:data_version: publisher version string
- health:data_source_system: source registry (era5_land, gbif, cirad, etc.)
- health:data_as_of: RFC 3339 datetime of snapshot vintage
- health:completeness_score: 0-1 fraction of expected records present
- health:uncertainty_type: none, prediction_interval, posterior_variance, ensemble_spread
"""


def build_search_prompt(user_query: str) -> str:
    """Build a prompt that gives an LLM the schema context for STAC search."""
    return f"""{HEALTH_SCHEMA_CONTEXT}
Given the above schema, translate this natural-language query into a structured
STAC search filter:

Query: {user_query}

Return a JSON object with:
- "data_type": the health:data_type value to filter on (or null)
- "disease_codes": list of ICD-10 codes to match (or [])
- "spatial_coverage": list of ISO 3166-1 alpha-3 country codes (or [])
- "temporal_resolution": the resolution to filter on (or null)
- "access_level": the access level to filter on (or null)
"""


if __name__ == "__main__":
    # 1. Read an existing Item and access health fields
    item = pystac.Item.from_file(str(EXAMPLES_DIR / "item-covariate-temperature.json"))

    print("=== Read Item ===")
    print(f"ID:        {item.id}")
    print(f"Data type: {item.properties['health:data_type']}")
    print(f"Temporal:  {item.properties['health:temporal_resolution']}")
    print(f"Source:    {item.properties['health:data_source_system']}")
    print(f"Access:    {item.properties['health:access_level']}")
    print()

    # 2. Extract health fields
    print("=== Health fields ===")
    for key, val in get_health_fields(item).items():
        print(f"  {key}: {val}")
    print()

    # 3. Load all examples and filter by data_type
    all_items = load_all_items(EXAMPLES_DIR)

    print("=== All Items by data_type ===")
    for it in all_items:
        dt = it.properties.get("health:data_type", "—")
        print(f"  [{dt:20s}] {it.id}")
    print()

    covariates = [
        it for it in all_items if it.properties.get("health:data_type") == "covariate"
    ]
    print(f"Covariates: {len(covariates)} items")

    with_disease = [
        it for it in all_items if it.properties.get("health:disease_codes")
    ]
    print(f"Items with disease_codes: {len(with_disease)} items")
    for it in with_disease:
        codes = it.properties["health:disease_codes"]
        print(f"  {it.id}: {codes}")
    print()

    # 4. Create a new Item programmatically
    new_item = pystac.Item(
        id="era5-soil-moisture-weekly-eu-2020-2024",
        geometry={
            "type": "Polygon",
            "coordinates": [[[-25, 34], [45, 34], [45, 72], [-25, 72], [-25, 34]]],
        },
        bbox=[-25, 34, 45, 72],
        datetime=None,
        properties={
            "start_datetime": "2020-01-01T00:00:00Z",
            "end_datetime": "2024-12-31T23:59:59Z",
            "title": "ERA5-Land weekly volumetric soil moisture — Europe 1 km",
            "health:data_type": "covariate",
            "health:temporal_resolution": "weekly",
            "health:week_system": "iso_8601",
            "health:spatial_unit": "grid_1km",
            "health:access_level": "open",
            "health:gdpr_status": "open_data",
            "health:data_source_system": "era5_land",
        },
    )
    new_item.stac_extensions = [
        "https://stac-extensions.github.io/health/v0.1.0/schema.json"
    ]

    print("=== Created Item ===")
    print(f"ID: {new_item.id}")
    print(f"Extensions: {new_item.stac_extensions}")
    print(json.dumps(get_health_fields(new_item), indent=2))
    print()

    # 5. Validate an Item against the JSON Schema
    print("=== Validation ===")
    try:
        item.validate()
        print(f"{item.id}: valid")
    except Exception as e:
        print(f"{item.id}: INVALID — {e}")

    # 6. Search by health fields
    results = search_items_by_health(
        all_items, data_type="vector_occurrence", country="DEU"
    )
    print("\n=== Search: vector_occurrence in DEU ===")
    for it in results:
        print(f"  {it.id}")

    results = search_items_by_health(all_items, disease_code="A92.3")
    print("\n=== Search: disease A92.3 (WNV) ===")
    for it in results:
        dt = it.properties.get("health:data_type")
        print(f"  [{dt}] {it.id}")

    # 7. Build an LLM search prompt
    print("\n=== LLM prompt for: 'temperature data in France' ===")
    prompt = build_search_prompt("temperature data in France")
    print(prompt[:300] + "...")
