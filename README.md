# Saudi Healthcare Analytics 2021–2024

[![Repository Validation](https://github.com/khaledzidan203-stack/saudi-healthcare-analytics/actions/workflows/portfolio-validation.yml/badge.svg)](https://github.com/khaledzidan203-stack/saudi-healthcare-analytics/actions/workflows/portfolio-validation.yml)

An end-to-end healthcare analytics implementation built from **official Saudi Ministry of Health Statistical Yearbooks for 2021–2024**. The project moves from workbook discovery and governed canonical modeling to SQL Server, a source-controlled Power BI semantic model, explicit DAX measures, report delivery, and layered validation.

> **Scope boundary:** this repository contains aggregate public healthcare statistics, not patient-level data. Results are descriptive and do not establish patient outcomes, causality, service quality, or emergency response-time performance.

<img src="docs/assets/Saudi%20Healthcare%20Analytics%20Pipeline%20Infographic.png" alt="Saudi Healthcare Analytics end-to-end project pipeline" width="100%">

**Start here:** [Case study](docs/CASE_STUDY.md) · [Technical walkthrough](docs/TECHNICAL_WALKTHROUGH.md) · [Evidence map](docs/PROJECT_EVIDENCE_MAP.md) · [Project index](docs/PROJECT_INDEX.md) · [Final validation](docs/validation/FINAL_RELEASE_VALIDATION.md)

## Project at a glance

| Area | Implemented state |
|---|---|
| Source | Saudi MOH Statistical Yearbooks — 2021–2024 |
| Analytical domains | Capacity · Activity · Workforce · Red Crescent regional resources/activity |
| Geography | National + Administrative Region; Health Region/Cluster kept separate |
| Canonical layer | 9 governed CSV tables: 4 facts + 5 dimensions |
| SQL | SQL Server `SaudiHealthcareAnalytics`, schema `analytics` |
| Semantic model | 10 tables total · 14 active M:1 single-direction relationships |
| Measures | 15 current measures; original 12 have recorded runtime reconciliation |
| Power BI | 7 PBIR pages · 121 uniquely identified saved visuals |
| Validation | Canonical↔SQL PASS · workforce 24/24 PASS · original DAX 12/12 PASS |
| Reproducibility | Included canonical CSVs + SQL loaders + PBIP/PBIR/TMDL source + release audit |

## Why the modeling matters

The source is not one flat, perfectly consistent table. Annual workbooks combine changing layouts, multiple healthcare domains, national totals, Administrative Region detail, sector splits, workforce snapshots, and published non-additive rates. A naive merge can duplicate historical observations, mix geography concepts, multiply joins, or aggregate rates incorrectly.

The implementation therefore follows these controls:

1. **Source and grain before aggregation** — each fact has an explicit business grain and source lineage.
2. **Separate analytical facts** — capacity, activity, workforce-by-sector, and workforce-by-nationality are not collapsed into one ambiguous table.
3. **Published rates stay non-additive** — official rates are never blindly summed across categories.
4. **Geography remains governed** — National and Administrative Region are approved concepts; Health Region and Health Cluster are not silently treated as equivalent.
5. **Validation is layered** — canonical data, SQL integrity, DAX behavior, report structure, screenshots, and release hygiene are checked separately.

## End-to-end architecture

```mermaid
flowchart LR
    A[Official Saudi MOH yearbooks] --> B[Python discovery & profiling]
    B --> C[Governed canonical layer]
    C --> D[4 facts + 5 dimensions]
    D --> E[SQL Server analytics schema]
    E --> F[Power BI semantic model]
    F --> G[Governed DAX measures]
    G --> H[7-page PBIR report]
    C --> V[Canonical validation]
    E --> V
    F --> V
    H --> V
    V --> Q[Release audit / CI]
```

### 1. Source discovery

Python inventories workbooks and worksheets, profiles structure, reviews candidate grains and geography concepts, and narrows the usable cross-year scope before transformation.

Raw yearbook files remain outside Git. The repository includes aggregate canonical outputs and lineage needed for reproducible analytical reconstruction. See [data provenance](data/README.md) and [current source governance](docs/SOURCE_GOVERNANCE_STATUS.md).

### 2. Canonical data layer

The governed canonical model contains four facts:

| Fact | Rows | Natural grain |
|---|---:|---|
| `FactCapacity` | 132 | Year × geography type/name × sector × capacity measure |
| `FactActivity` | 84 | Year × geography type/name × sector × activity measure |
| `FactWorkforceSector` | 72 | Year × national geography × sector × workforce type |
| `FactWorkforceNationality` | 96 | Year × national geography × scope × workforce type × nationality |

Dimensions are Year, Geography, Sector, WorkforceType, and Nationality.

The canonical contract prevents duplicate rolling historical observations by taking each reporting year from its corresponding Statistical Yearbook rather than loading repeated historical columns from later editions. See [Canonical Data Contract](docs/architecture/CANONICAL_DATA_CONTRACT.md).

### 3. SQL Server analytical model

SQL Server is the final reporting engine. The `analytics` schema loads the five dimensions and four facts using surrogate keys, unique grain constraints, retained lineage, and decimal precision suitable for published rates.

Validated controls include:

- broken foreign keys = **0**;
- duplicate fact grains = **0**;
- canonical ↔ SQL Server reconciliation = **PASS**;
- joined row-count preservation = **PASS**.

SQLite is retained only as a reproducible cross-engine reference baseline. It is **not** the Power BI reporting source. See [SQL Star Schema](docs/architecture/SQL_STAR_SCHEMA.md).

### 4. Power BI semantic model

The saved PBIP/TMDL model contains:

- nine SQL-backed business tables;
- one disconnected `_Measures` table;
- **10 total semantic tables**;
- **14 active M:1 single-direction relationships**;
- no fact-to-fact, many-to-many, bidirectional, or inactive relationships;
- **15 current measures**.

This is an annual-grain model. Auto Date/Time is disabled and no artificial daily date table is introduced. See [Power BI Semantic Model](docs/powerbi/POWER_BI_SEMANTIC_MODEL.md).

## KPI governance

The [KPI contract](docs/kpi/KPI_CONTRACT.md) defines numerator, denominator, grain, filters, aggregation behavior, and null handling.

Examples:

- **Hospitals / Beds / Encounters / Admissions** — compatible additive counts.
- **Beds per 10,000 Population / Encounters per Person / Admissions per 100 Persons** — official published rates, treated as non-additive.
- **Saudi Workforce Share** — Saudi ÷ (Saudi + Non-Saudi) over the governed `MOH Total` scope.
- **Cases per Center / Cases per Ambulance** — ratio of totals, never average of row-level ratios.

Missing, blank, and zero are not interchangeable. Annual workforce snapshots are not summed across years.

## Power BI report

| Page | Purpose |
|---|---|
| INDEX | Opening navigation page |
| Executive Overview | Selected-year headlines and full-period trends; saved at 2024 |
| Healthcare Capacity | Hospitals, beds, sector mix, and official capacity rates |
| Healthcare Activity | Encounters, admissions, sector volume, and official activity rates |
| Workforce & Nationalization | Workforce composition and MOH nationality mix |
| Red Crescent Regional Performance | Cases, first-aid centers, ambulances, and regional resource ratios |
| Methodology & Validation | Source lineage, model rules, validation, and limitations |

The current release contains **121 uniquely identified visuals**. Genuine report captures are preserved in [screenshots](screenshots/README.md).

## Validation evidence

Validation statements are deliberately separated by evidence type:

| Validation layer | Recorded result |
|---|---|
| Canonical fact grain / required coverage | PASS |
| SQL Server canonical reconciliation | PASS |
| Broken foreign keys | 0 |
| Duplicate fact grains | 0 |
| FY006 ↔ FY008 workforce reconciliation | 24 / 24 PASS; zero count variance |
| Original governed DAX suite | 12 / 12 runtime PASS |
| Current semantic structure | 10 tables · 15 measures · 14 relationships |
| Report structure | 7 pages · 121 visuals · navigation checks PASS |
| Release audit | PBIR/JSON parsing, links, screenshots, source preservation, exclusions, credential scan |

The current model has **15 measures**, while the retained runtime JSON covers the **original 12 governed measures**. The later `First Aid Centers`, `Ambulances`, and `Ambulances Card` additions are approved current-model additions, but they are not presented as if they were part of that earlier 12-measure runtime suite. See [DAX Measure Dictionary](docs/powerbi/DAX_MEASURE_DICTIONARY.md) and [Final Release Validation](docs/validation/FINAL_RELEASE_VALIDATION.md).

## Selected validated 2024 observations

The release audit reconciles these current canonical headlines with recorded SQL evidence:

| Indicator | 2024 value | Scope |
|---|---:|---|
| Hospitals | 516 | National, all sectors |
| Beds | 82,721 | National, all sectors |
| Workforce Count | 681,914 | National, approved sector/profession detail |
| Saudi Workforce Share | 74.29% | `MOH Total` nationality workforce only |
| Encounters | 170,231,304 | National, all sectors |
| Admissions | 3,630,334 | National, all sectors |
| Red Crescent Cases | 566,288 | Administrative Regions aggregated |

These are descriptive observations, not performance ratings.

## Source governance and exclusions

The current analytical core uses FY-005, FY-006, FY-008, FY-010, FY-018, FY-020, and FY-023. FY-029 Blood Bank is excluded from the comparable multi-year core because available definitions change materially across years.

`outputs/validation/FINAL_SOURCE_APPROVAL.csv` is preserved as a **historical discovery-stage review artifact** and still contains `PENDING` values. It is not the current release-status register. The implemented scope is documented in [Source Governance Status](docs/SOURCE_GOVERNANCE_STATUS.md).

## Reproduce the analytical project

Prerequisites:

- Python 3
- dependencies in [`requirements.txt`](requirements.txt)
- SQL Server
- Microsoft ODBC Driver 18
- Windows Authentication
- Power BI Desktop supporting PBIP/PBIR/TMDL

```powershell
git clone https://github.com/khaledzidan203-stack/saudi-healthcare-analytics.git
cd saudi-healthcare-analytics
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python scripts/verify_repository_baseline.py
```

For SQL/report reproduction, the included canonical CSVs are sufficient. Create a dedicated local `SaudiHealthcareAnalytics` database, then follow [`sql/README.md`](sql/README.md). The SQL loader drops and recreates the analytical tables, so it should be used only in a dedicated development database.

```powershell
python scripts/build_sqlite_model.py
python scripts/build_sqlserver_model.py
python scripts/validate_sqlserver_model.py
```

Open `powerbi/SaudiHealthcareAnalytics.pbip`, authenticate to SQL Server, and refresh in Import mode. If downloading the repository as ZIP, extract it completely before opening the PBIP file.

Offline publication validation:

```powershell
python scripts/validate_release.py
```

Full Excel-to-canonical reproduction requires separately downloaded official MOH workbooks. Source files can change upstream, so replacement inputs must be revalidated rather than assumed identical. See [data reproduction](data/README.md).

## Repository structure

```text
data/          Aggregate canonical data and source/reproduction policy
docs/          Contracts, case study, governance, semantic model, validation
outputs/       Discovery, reconciliation, and validation evidence
powerbi/       PBIP entry point, PBIR report, TMDL semantic model
screenshots/   Seven approved report captures
scripts/       SQL loaders, model validators, and release audit
sql/           SQL Server DDL plus labeled SQLite reference SQL
src/           Workbook discovery and canonical transformation
```

## Interpretation limits

Published rates retain source definitions and precision. Geography and scope differences constrain comparisons. Workforce counts are annual snapshots. Red Crescent cases, centers, and ambulances describe workload/resources, not response time or service quality. Screenshots validate captured states, not every possible interactive filter combination.

## Source attribution and license

Saudi Ministry of Health — official Statistical Yearbook publications. See [Data Attribution and Usage Boundary](DATA_ATTRIBUTION.md).

[MIT](LICENSE) applies to original project code and documentation. Provider data and third-party materials remain subject to their original terms.
