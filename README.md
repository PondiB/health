# Health Extension Specification

- **Title:** Health
- **Identifier:** <https://stac-extensions.github.io/health/v0.1.0/schema.json>
- **Field Name Prefix:** health
- **Scope:** Item, Collection, Asset
- **Extension [Maturity Classification](https://github.com/radiantearth/stac-spec/tree/master/extensions/README.md#extension-maturity):** Proposal
- **Owner**: [@PondiB](https://github.com/PondiB)

This document explains the Health Extension to the [SpatioTemporal Asset Catalog](https://github.com/radiantearth/stac-spec)
(STAC) specification.

It adds domain metadata for **geospatial epidemic-intelligence** datasets: environmental and climatic covariates,
vector and host species distributions, epidemiological case data, and model outputs such as risk maps.
The metadata requirements are aligned with the ISO 19115 / INSPIRE subset used by the
[MOOD](https://mood-h2020.eu/) GeoNetwork catalogue and the [GEOAI4EI](https://geoai4ei.eu/) project.

Design principles:

1. **Single required field** — only `health:data_type` is required on Items.
2. **One conditional** — `health:week_system` is required when `temporal_resolution` is `weekly`.
3. **Reuse before reinvention** — CRS, grids, citations, and tabular schemas stay in existing STAC extensions.
4. **MOOD metadata alignment** — fields map to the ISO 19115 / INSPIRE metadata attributes
   (title, abstract, spatial resolution, temporal resolution, CRS, lineage, etc.) used across
   the MOOD and GEOAI4EI data catalogues.

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

Tularaemia (`A21`) appears alongside hantavirus in the common vole example.

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
| health:keywords | \[string] | Subject keywords for faceted search (e.g. `["ERA5", "temperature", "reanalysis"]`). |
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
| Overview | `thumbnail` asset role (core STAC) |
| Spatial resolution | `health:spatial_unit` or `proj:transform` |
| Temporal resolution | `health:temporal_resolution` |
| Temporal extent | `start_datetime` / `end_datetime` (core STAC) |
| Data unit | `description` or `cube:variables` |
| Data type (format) | Asset `type` (media type) |
| CRS (EPSG) | `proj:code` (Projection extension) |
| Download and links | `assets` + `links` (core STAC) |
| Categories | `health:keywords` (Item) or `keywords` (Collection) |
| Other keywords | `health:keywords` (Item) or `keywords` (Collection) |
| Language | `description` (note in text) |
| Status | `health:data_version` |
| Update frequency | `health:temporal_resolution` |
| Representation type | Asset `type` (media type) + `roles` |
| Scale | `proj:transform` or `health:spatial_unit` |
| Format | Asset `type` (media type, e.g. `image/tiff; application=geotiff`) |
| Lineage | `description` or Processing extension |
| Contact | Collection `providers` or `health:data_source_system` |
| Metadata language | `description` (note in text) |
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

## Python (PySTAC) Usage

PySTAC reads and writes `health:` fields without any library changes — they are stored as plain
dictionary entries in `item.properties`. No fork or plugin is needed.

```python
import pystac

# Read an Item and access health fields
item = pystac.Item.from_file("examples/item-covariate-temperature.json")
print(item.properties["health:data_type"])           # "covariate"
print(item.properties["health:temporal_resolution"])  # "daily"

# Create a new Item with health fields
new_item = pystac.Item(
    id="era5-soil-moisture-weekly-eu",
    geometry={"type": "Polygon", "coordinates": [[[-25,34],[45,34],[45,72],[-25,72],[-25,34]]]},
    bbox=[-25, 34, 45, 72],
    datetime=None,
    properties={
        "start_datetime": "2020-01-01T00:00:00Z",
        "end_datetime": "2024-12-31T23:59:59Z",
        "health:data_type": "covariate",
        "health:temporal_resolution": "weekly",
        "health:week_system": "iso_8601",
        "health:spatial_unit": "grid_1km",
        "health:access_level": "open",
    },
)
new_item.stac_extensions = [
    "https://stac-extensions.github.io/health/v0.1.0/schema.json"
]

# Validate against the JSON Schema
item.validate()

# Filter a list of Items by health fields
def search_by_health(items, data_type=None, disease_code=None, country=None):
    results = items
    if data_type:
        results = [i for i in results if i.properties.get("health:data_type") == data_type]
    if disease_code:
        results = [i for i in results if disease_code in (i.properties.get("health:disease_codes") or [])]
    if country:
        results = [i for i in results if country in (i.properties.get("health:spatial_coverage") or [])]
    return results
```

**pystac-client** works the same way for searching STAC APIs — `health:` fields are queryable
if the API backend supports them (e.g. `stac-fastapi` with the filter extension):

```python
from pystac_client import Client

client = Client.open("https://your-stac-api.example.com")
results = client.search(
    collections=["geoai4ei-covariates-europe"],
    filter="health:data_type = 'covariate' AND health:temporal_resolution = 'daily'",
    filter_lang="cql2-text",
)
for item in results.items():
    print(item.id, item.properties["health:data_type"])
```

See [`examples/pystac_usage.py`](examples/pystac_usage.py) for a full runnable script.

## LLM Integration

The Health extension schema is designed to be machine-readable for LLM-powered search and
cataloguing workflows.

### 1. Metadata generation from descriptions

An LLM can populate `health:` fields from a dataset's free-text description:

```json
Input:  "MODIS vegetation index composites for tick habitat modelling in Sweden"

Output: {
    "health:data_type": "covariate",
    "health:spatial_coverage": ["SWE"],
    "health:data_source_system": "modis",
    "health:access_level": "open"
}
```

Feed the LLM the Data Type enum table and MOOD crosswalk as context to produce
valid field values. The disease scenario coverage table (RVF, CCHF, Ebola, HPAI,
WNV, TBE, Hanta, MPOX) and the ICD-10 / NCBI Taxonomy mappings in the examples
serve as few-shot references for LLMs populating `health:disease_codes` and
`health:pathogen_taxon_ids`.

### 2. Retrieval-Augmented Generation (RAG) with LangChain

A RAG pipeline lets researchers query the catalogue in natural language
(e.g. *"What mosquito data do we have for Scandinavia?"*) and get back the
matching STAC Items with an LLM-generated explanation.

**Indexing** — load each STAC Item as a LangChain `Document`.
Embed the human-readable fields (`title`, `description`, `health:keywords`)
and store the structured `health:` fields as metadata for filtered retrieval:

```python
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document
import json, glob

docs = []
for path in glob.glob("examples/item-*.json"):
    item = json.load(open(path))
    props = item["properties"]

    text = f"{props.get('title', '')}\n{props.get('description', '')}"
    if props.get("health:keywords"):
        text += f"\nKeywords: {', '.join(props['health:keywords'])}"

    docs.append(Document(
        page_content=text,
        metadata={
            "id": item["id"],
            "data_type": props.get("health:data_type"),
            "disease_codes": props.get("health:disease_codes", []),
            "spatial_coverage": props.get("health:spatial_coverage", []),
            "temporal_resolution": props.get("health:temporal_resolution"),
            "access_level": props.get("health:access_level"),
        },
    ))

vectorstore = Chroma.from_documents(docs, HuggingFaceEmbeddings())
```

**Hybrid retrieval** — combine vector similarity with metadata filters
using LangChain's `SelfQueryRetriever`. The LLM translates a
natural-language question into structured filters over the `health:` enums
*before* ranking by semantic similarity:

```python
from langchain.retrievers import SelfQueryRetriever

metadata_field_info = [
    {"name": "data_type", "type": "string",
     "description": "case_reports | vector_occurrence | host_distribution "
                    "| covariate | model_output | environmental_sampling"},
    {"name": "spatial_coverage", "type": "list[string]",
     "description": "ISO 3166-1 alpha-3 country codes, e.g. DEU, FRA, SWE"},
    {"name": "disease_codes", "type": "list[string]",
     "description": "ICD-10 codes, e.g. A92.4 (RVF), A92.3 (WNV)"},
    {"name": "access_level", "type": "string",
     "description": "open | registered | controlled_access | consortium_only"},
    {"name": "temporal_resolution", "type": "string",
     "description": "event | daily | weekly | monthly | annual | multi_year"},
]

retriever = SelfQueryRetriever.from_llm(
    llm=llm,
    vectorstore=vectorstore,
    document_contents="Geospatial epidemic-intelligence dataset metadata",
    metadata_field_info=metadata_field_info,
)
```

**Generation** — pass the retrieved items plus the Health schema context to
the LLM for a grounded answer:

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are an epidemic-intelligence catalogue assistant. "
     "Answer questions about available STAC Health datasets. "
     "Key codes: A92.4=RVF, A92.3=WNV, A98.0=CCHF, A98.4=Ebola, J09=HPAI."),
    ("human", "Catalogue records:\n{context}\n\nQuestion: {question}"),
])

rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

rag_chain.invoke("Which datasets cover Rift Valley Fever?")
```

The Health extension's controlled vocabularies (`data_type`, `access_level`,
`disease_codes`, `spatial_coverage`) work especially well as metadata
facets because the LLM can map natural language to enum values
(e.g. *"open-access tick data in France"* → `access_level == "open"` and
`"FRA" in spatial_coverage`).

For smaller catalogues or offline prototypes the approach above works
as-is. For production deployments backed by a STAC API, see the next
section.

### 3. Production RAG with stac-fastapi-pgstac

When the catalogue is served by
[stac-fastapi-pgstac](https://github.com/stac-utils/stac-fastapi-pgstac),
PgSTAC already provides CQL2 filtering over JSONB properties, PostGIS
spatial indexing, and temporal range queries — so the RAG architecture
shifts from *embed-then-search* to **LLM-as-query-translator**:

```text
User question (natural language)
        │
        ▼
   ┌─────────┐   CQL2 filter + bbox/datetime     ┌──────────────────┐
   │   LLM   │ ─────────────────────────────────▶ │ stac-fastapi     │
   │ (agent) │                                    │   + pgstac       │
   └─────────┘                                    │  (PostgreSQL)    │
        ▲                                         └──────┬───────────┘
        │   matched STAC Items (JSON)                    │
        └────────────────────────────────────────────────┘
        │
        ▼
   LLM generates grounded answer from retrieved Items
```

The LLM translates natural language into structured CQL2 filters and
calls the STAC API directly. PgSTAC handles spatial intersection,
temporal range, and exact filtering on `health:` fields stored in JSONB.

**Define the STAC search as a LangChain tool:**

```python
import httpx
from langchain_core.tools import tool

STAC_API = "https://your-stac-api.example.com"

@tool
def search_stac_catalogue(
    data_type: str = None,
    disease_codes: list[str] = None,
    spatial_coverage: list[str] = None,
    temporal_resolution: str = None,
    access_level: str = None,
    bbox: list[float] = None,
    datetime_range: str = None,
    limit: int = 10,
) -> str:
    """Search the STAC Health catalogue via the pgstac-backed API.

    Args:
        data_type: case_reports, vector_occurrence, host_distribution,
                   covariate, model_output, environmental_sampling
        disease_codes: ICD-10 codes, e.g. ["A92.4"] for RVF
        spatial_coverage: ISO 3166-1 alpha-3, e.g. ["FRA", "DEU"]
        temporal_resolution: daily, weekly, monthly, annual, multi_year
        access_level: open, registered, controlled_access, consortium_only
        bbox: [west, south, east, north] in EPSG:4326
        datetime_range: RFC 3339 range, e.g. "2020-01-01/2024-12-31"
        limit: max items to return
    """
    filters = []
    if data_type:
        filters.append({
            "op": "=",
            "args": [{"property": "health:data_type"}, data_type],
        })
    if disease_codes:
        for code in disease_codes:
            filters.append({
                "op": "a_contains",
                "args": [{"property": "health:disease_codes"}, [code]],
            })
    if spatial_coverage:
        for country in spatial_coverage:
            filters.append({
                "op": "a_contains",
                "args": [{"property": "health:spatial_coverage"}, [country]],
            })
    if temporal_resolution:
        filters.append({
            "op": "=",
            "args": [{"property": "health:temporal_resolution"}, temporal_resolution],
        })
    if access_level:
        filters.append({
            "op": "=",
            "args": [{"property": "health:access_level"}, access_level],
        })

    body = {"limit": limit}
    if bbox:
        body["bbox"] = bbox
    if datetime_range:
        body["datetime"] = datetime_range
    if filters:
        body["filter"] = (
            {"op": "and", "args": filters} if len(filters) > 1 else filters[0]
        )
        body["filter-lang"] = "cql2-json"

    resp = httpx.post(f"{STAC_API}/search", json=body)
    resp.raise_for_status()
    features = resp.json().get("features", [])

    results = []
    for item in features:
        props = item["properties"]
        results.append(
            f"- **{props.get('title', item['id'])}**\n"
            f"  type={props.get('health:data_type')} | "
            f"diseases={props.get('health:disease_codes', [])} | "
            f"countries={props.get('health:spatial_coverage', [])} | "
            f"access={props.get('health:access_level')}"
        )
    return "\n".join(results) if results else "No matching datasets found."
```

**Wire up the agent:**

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor, create_tool_calling_agent

prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are a GEOAI4EI catalogue assistant backed by a STAC API "
     "with the Health extension. Use the search tool to find datasets, "
     "then answer the user's question based on the results.\n\n"
     "Key disease codes: A92.4=RVF, A92.3=WNV, A98.0=CCHF, "
     "A98.4=Ebola, J09=HPAI.\n"
     "Countries use ISO 3166-1 alpha-3 (FRA, DEU, SWE, etc.)."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

agent = create_tool_calling_agent(llm, [search_stac_catalogue], prompt)
executor = AgentExecutor(agent=agent, tools=[search_stac_catalogue])

executor.invoke({"input": "What Rift Valley Fever data do we have?"})
executor.invoke({"input": "Find open-access daily covariates covering France"})
```

**Why pgstac-backed retrieval over a standalone vector store:**

| Concern | Vector store RAG | pgstac-backed agent |
| --- | --- | --- |
| Structured filtering | Approximate metadata filters | Exact CQL2 on indexed JSONB |
| Spatial queries | Not supported | PostGIS bbox / intersects |
| Temporal range | Stored as text metadata | First-class datetime indexing |
| Data freshness | Must re-index on changes | Always queries live catalogue |
| Scale | ~100K documents typical | Hundreds of millions of items |

**When to add a vector layer on top:**
For fuzzy semantic queries that CQL2 cannot express
(e.g. *"datasets related to climate-driven disease emergence"*),
add a [pgvector](https://github.com/pgvector/pgvector) column alongside
PgSTAC in the same PostgreSQL instance. Embed `title + description +
health:keywords` into the vector column, then combine CQL2 structured
filters with pgvector similarity ranking in a single query. This gives
exact structured retrieval and semantic search in one database.

Respect `health:access_level` and `health:gdpr_status` during retrieval
to enforce data-access policies — filter out `restricted_identifiable`
items unless the requesting user is authorised.

### 4. Multi-step Agent with LangGraph

[LangGraph](https://langchain-ai.github.io/langgraph/) enables stateful,
multi-step agent workflows with cycles and conditional branching. This is
useful when a single tool call is not enough — for example, an agent that
searches the catalogue, evaluates whether the results are sufficient,
refines the query if needed, and then synthesises a final answer.

```text
         ┌──────────────────────────────┐
         │          START               │
         └──────────┬───────────────────┘
                    ▼
         ┌──────────────────────────────┐
         │    plan_query                │
         │  (parse intent → filters)    │
         └──────────┬───────────────────┘
                    ▼
         ┌──────────────────────────────┐
         │    search_catalogue          │
         │  (call STAC API via tool)    │
         └──────────┬───────────────────┘
                    ▼
         ┌──────────────────────────────┐
         │    evaluate_results          │◀─────┐
         │  (enough? relevant?)         │      │
         └──────────┬───────────────────┘      │
                    │                          │
              ┌─────┴──────┐                   │
              │            │                   │
          sufficient   insufficient            │
              │            │                   │
              ▼            ▼                   │
         ┌─────────┐  ┌────────────┐           │
         │ respond  │  │  refine    │───────────┘
         └─────────┘  │  query     │
                      └────────────┘
```

**Define the agent state and graph:**

```python
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END

class CatalogueState(TypedDict):
    question: str
    filters: dict
    results: list[dict]
    refinement_count: int
    answer: str

def plan_query(state: CatalogueState) -> CatalogueState:
    """LLM translates the natural-language question into STAC filters."""
    from langchain_anthropic import ChatAnthropic

    llm = ChatAnthropic(model="claude-sonnet-5")
    plan_prompt = (
        "You are a STAC Health catalogue planner. Given a user question, "
        "extract structured search filters.\n\n"
        "Available filters:\n"
        "- data_type: case_reports | vector_occurrence | host_distribution "
        "| covariate | model_output | environmental_sampling\n"
        "- disease_codes: ICD-10 codes (A92.4=RVF, A92.3=WNV, A98.0=CCHF, "
        "A98.4=Ebola, J09=HPAI, A84=TBE, A98.5=Hanta)\n"
        "- spatial_coverage: ISO 3166-1 alpha-3 codes\n"
        "- temporal_resolution: daily | weekly | monthly | annual | multi_year\n"
        "- access_level: open | registered | controlled_access | consortium_only\n"
        "- bbox: [west, south, east, north]\n"
        "- datetime_range: RFC 3339 range\n\n"
        f"Question: {state['question']}\n\n"
        "Return a JSON object with only the relevant filters."
    )
    response = llm.invoke(plan_prompt)
    import json
    filters = json.loads(response.content)
    return {"filters": filters, "refinement_count": state.get("refinement_count", 0)}

def search_catalogue(state: CatalogueState) -> CatalogueState:
    """Call the STAC API with the planned filters."""
    import httpx

    STAC_API = "https://your-stac-api.example.com"
    body = {"limit": 10}

    filters = state["filters"]
    cql_filters = []
    if filters.get("data_type"):
        cql_filters.append({
            "op": "=",
            "args": [{"property": "health:data_type"}, filters["data_type"]],
        })
    if filters.get("disease_codes"):
        for code in filters["disease_codes"]:
            cql_filters.append({
                "op": "a_contains",
                "args": [{"property": "health:disease_codes"}, [code]],
            })
    if filters.get("spatial_coverage"):
        for country in filters["spatial_coverage"]:
            cql_filters.append({
                "op": "a_contains",
                "args": [{"property": "health:spatial_coverage"}, [country]],
            })
    if filters.get("temporal_resolution"):
        cql_filters.append({
            "op": "=",
            "args": [
                {"property": "health:temporal_resolution"},
                filters["temporal_resolution"],
            ],
        })
    if filters.get("access_level"):
        cql_filters.append({
            "op": "=",
            "args": [{"property": "health:access_level"}, filters["access_level"]],
        })
    if filters.get("bbox"):
        body["bbox"] = filters["bbox"]
    if filters.get("datetime_range"):
        body["datetime"] = filters["datetime_range"]
    if cql_filters:
        body["filter"] = (
            {"op": "and", "args": cql_filters}
            if len(cql_filters) > 1
            else cql_filters[0]
        )
        body["filter-lang"] = "cql2-json"

    resp = httpx.post(f"{STAC_API}/search", json=body)
    resp.raise_for_status()
    features = resp.json().get("features", [])

    results = []
    for item in features:
        props = item["properties"]
        results.append({
            "id": item["id"],
            "title": props.get("title", item["id"]),
            "data_type": props.get("health:data_type"),
            "disease_codes": props.get("health:disease_codes", []),
            "spatial_coverage": props.get("health:spatial_coverage", []),
            "access_level": props.get("health:access_level"),
            "temporal_resolution": props.get("health:temporal_resolution"),
        })
    return {"results": results}

def evaluate_results(state: CatalogueState) -> CatalogueState:
    """LLM decides whether the results sufficiently answer the question."""
    return state

def should_refine(state: CatalogueState) -> str:
    """Route to 'refine' if results are empty and we haven't retried too much."""
    if not state["results"] and state.get("refinement_count", 0) < 2:
        return "refine"
    return "respond"

def refine_query(state: CatalogueState) -> CatalogueState:
    """Broaden the filters — drop the most restrictive constraint."""
    from langchain_anthropic import ChatAnthropic
    import json

    llm = ChatAnthropic(model="claude-sonnet-5")
    refine_prompt = (
        "The STAC catalogue search returned no results with these filters:\n"
        f"{json.dumps(state['filters'], indent=2)}\n\n"
        f"Original question: {state['question']}\n\n"
        "Relax the filters to broaden the search. Remove or loosen the "
        "most restrictive constraint while keeping the query relevant. "
        "Return the revised JSON filters."
    )
    response = llm.invoke(refine_prompt)
    filters = json.loads(response.content)
    return {
        "filters": filters,
        "refinement_count": state.get("refinement_count", 0) + 1,
    }

def respond(state: CatalogueState) -> CatalogueState:
    """Generate a final grounded answer from the retrieved items."""
    from langchain_anthropic import ChatAnthropic
    import json

    llm = ChatAnthropic(model="claude-sonnet-5")
    context = json.dumps(state["results"], indent=2) if state["results"] else "No datasets found."
    response = llm.invoke(
        "You are an epidemic-intelligence catalogue assistant. "
        "Answer the question based on these STAC Health catalogue results.\n\n"
        f"Results:\n{context}\n\n"
        f"Question: {state['question']}"
    )
    return {"answer": response.content}

# Build the graph
graph = StateGraph(CatalogueState)
graph.add_node("plan_query", plan_query)
graph.add_node("search_catalogue", search_catalogue)
graph.add_node("evaluate_results", evaluate_results)
graph.add_node("refine_query", refine_query)
graph.add_node("respond", respond)

graph.set_entry_point("plan_query")
graph.add_edge("plan_query", "search_catalogue")
graph.add_edge("search_catalogue", "evaluate_results")
graph.add_conditional_edges("evaluate_results", should_refine, {
    "refine": "refine_query",
    "respond": "respond",
})
graph.add_edge("refine_query", "search_catalogue")
graph.add_edge("respond", END)

app = graph.compile()
```

**Run the agent:**

```python
result = app.invoke({"question": "What tick vector data do we have for Central Europe?"})
print(result["answer"])

result = app.invoke({
    "question": "Find open-access daily temperature covariates covering France and Germany"
})
print(result["answer"])
```

**When to use LangGraph over the simpler LangChain agent (section 3):**

| Concern | LangChain AgentExecutor | LangGraph |
| --- | --- | --- |
| Simple single-tool queries | Sufficient | Overkill |
| Multi-step reasoning with retries | Limited control | Explicit conditional edges |
| Custom evaluation / refinement loops | Hard to customise | Built-in cycles |
| Streaming intermediate steps | Basic | First-class support |
| Human-in-the-loop approval | Requires workarounds | Native interrupt/resume |
| Checkpointing and recovery | Not built-in | Persistent state via checkpointers |

For most catalogue search tasks, the LangChain agent in section 3 is
sufficient. Use LangGraph when you need query refinement loops,
multi-source aggregation (e.g. searching STAC + an external disease
database, then joining results), or human-in-the-loop approval before
returning results with `controlled_access` or `restricted_identifiable`
data.

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
