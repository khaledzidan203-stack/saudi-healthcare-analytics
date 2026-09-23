# Saudi Healthcare Analytics

An end-to-end analytics and analytics-engineering portfolio project using official Saudi Ministry of Health statistics for **2021–2024**. Python source profiling, governed canonical data, SQL Server and Power BI connect healthcare capacity, activity, workforce and regional emergency resources to traceable reporting.

[Report gallery](screenshots/README.md) · [Documentation index](docs/PROJECT_INDEX.md) · [Release validation](docs/validation/FINAL_RELEASE_VALIDATION.md) · [Power BI project](powerbi/README.md)

![Executive Overview — genuine Power BI capture with 2024 selected](screenshots/01_executive_overview.png)

## Executive Summary

Seven report pages bring annual healthcare resources and service volumes into a consistent analytical model. Each indicator is connected to its source, grain and validation evidence. This is a reproducible portfolio project, not a deployed or live embedded dashboard. Screenshots show captured filter states; source workbooks remain immutable and local.

## Business Problem

Official workbooks mix reporting years, geography concepts, subtotals, published rates and detailed counts. Comparing them without contracts can double-count workforce, combine incompatible geographic units or aggregate rates incorrectly. This project separates those concepts before reporting them.

## Analytical Questions

- How do hospital capacity and official population-adjusted rates vary by year?
- How do encounters and admissions compare across sectors and time?
- How do workforce scale, profession mix and MOH Saudi workforce share differ?
- Where are Red Crescent cases, centers and ambulances concentrated?
- Which source definitions and reconciliation checks support each result?

## Project Highlights

| Deliverable | Verified scope |
|---|---|
| Canonical layer | Four facts and five dimensions; explicit grains and source lineage |
| SQL Server | Governed `analytics` schema; canonical reconciliation recorded PASS |
| Semantic model | Nine SQL business tables plus disconnected `_Measures`: **10 tables total** |
| Relationships | **14** active M:1, single direction; no fact-to-fact relationships |
| Measures | **15** total: 12 original governed KPIs, two Red Crescent counts, one display helper |
| Report | INDEX plus six approved report pages |
| Evidence | Original 12 KPI measures have recorded SQL ↔ DAX runtime PASS; later report approval is tracked separately |

The [final validation record](docs/validation/FINAL_RELEASE_VALIDATION.md) separates current checks from historical evidence. The Methodology screenshot's “9 tables” counts business tables; `_Measures` makes the total ten.

## Technology Stack

Python, pandas, NumPy and openpyxl support discovery and workbook handling; canonical and SQL loaders also use Python's standard library. pyodbc connects SQL Server. Power Query imports SQL tables; TMDL, DAX and PBIR define the model and report. SQLite is a reproducible historical comparison baseline, not the reporting source.

## End-to-End Architecture

```mermaid
flowchart LR
    A[Official MOH workbooks] --> B[Profiling and contracts]
    B --> C[Canonical CSV facts and dimensions]
    C --> D[SQL Server analytics schema]
    C --> E[Validation and reconciliation]
    D --> E
    E --> F[Power BI semantic model]
    F --> G[Governed DAX]
    G --> H[PBIR report]
    H --> I[Healthcare management analysis]
```

[Canonical contract](docs/architecture/CANONICAL_DATA_CONTRACT.md) · [SQL model](docs/architecture/SQL_STAR_SCHEMA.md) · [Semantic model](docs/powerbi/POWER_BI_SEMANTIC_MODEL.md)

## Data Sources

Approved MOH yearbook source families are FY-005 Hospitals/Beds, FY-006 Health Manpower, FY-008 Workforce/Nationality, FY-010 Primary Health Care, FY-018 Red Crescent, FY-020 Encounters and FY-023 Admissions.

The core uses National and Administrative Region geography. FY-029 Blood Bank is excluded where changing definitions prevent comparable trends. Health Regions and Health Clusters are not assumed equivalent to Administrative Regions. Each year comes from its own yearbook, not duplicated rolling historical columns.

[Source acquisition](data/README.md) · [Source approval register](outputs/validation/FINAL_SOURCE_APPROVAL.csv)

## Canonical Data Model

| Fact | Rows | Natural grain |
|---|---:|---|
| FactCapacity | 132 | Year × geography type/name × sector × capacity measure |
| FactActivity | 84 | Year × geography type/name × sector × activity measure |
| FactWorkforceSector | 72 | Year × national geography × sector × workforce type |
| FactWorkforceNationality | 96 | Year × national geography × scope × workforce type × nationality |

Dimensions are Year, Geography, Sector, WorkforceType and Nationality. Facts remain separate; dimensions filter facts in one direction. Keys and grain constraints prevent join multiplication. [Data dictionary](docs/architecture/DATA_DICTIONARY.md).

## KPI Governance

The [KPI contract](docs/kpi/KPI_CONTRACT.md) and [DAX dictionary](docs/powerbi/DAX_MEASURE_DICTIONARY.md) specify numerator, denominator, grain, filters and aggregation.

- Capacity: Hospitals, Beds and official Beds per 10,000 Population.
- Activity: Encounters, Encounters per Person, Admissions and Admissions per 100 Persons.
- Workforce: Workforce Count and **MOH Total** Saudi Workforce Share; the share is not an all-sector nationalization rate.
- Red Crescent: Cases, First Aid Centers, Ambulances, Cases per Center and Cases per Ambulance. `Ambulances Card` is a display helper, not another KPI.

Annual workforce snapshots must not be summed across years. Official population rates are national, non-additive source values, not sector rates. Aggregate ratios use ratio of totals with `DIVIDE`; missing, blank and zero are not interchangeable.

## Power BI Report

| Page | Purpose |
|---|---|
| INDEX | Opening page; navigation to the six report pages |
| Executive Overview | Selected-year headlines and full-period trends; default year 2024 |
| Healthcare Capacity | Hospitals, beds, sector mix and national capacity rates |
| Healthcare Activity | Encounters, admissions, sector volumes and official rates |
| Workforce & Nationalization | Annual workforce mix and MOH nationality composition |
| Red Crescent Regional Performance | Regional cases, centers and ambulances |
| Methodology & Validation | Source lineage, contracts, validation and limitations |

HOME buttons return to INDEX. [Opening and refresh instructions](powerbi/README.md).

## Dashboard Gallery

Genuine, unaltered report captures, not live embedded reports. [View all seven pages](screenshots/README.md).

![Healthcare Capacity](screenshots/02_healthcare_capacity.png)

![Red Crescent Regional Performance](screenshots/05_red_crescent_regional_performance.png)

## Validation & Reconciliation

| Validation | Evidence |
|---|---|
| Broken foreign keys, duplicate fact grains and join multiplication: zero | [SQL Server validation](outputs/validation/sqlserver_validation.json) |
| Canonical ↔ SQL Server reconciliation: PASS | [SQL Server validation](outputs/validation/sqlserver_validation.json) |
| FY006 ↔ FY008: 24/24 PASS | [Cross-source reconciliation](outputs/validation/workforce_cross_source_reconciliation.csv) |
| Original governed DAX suite: 12/12 runtime PASS | [Runtime checkpoint](outputs/validation/powerbi_dax_runtime_validation.json) |
| Current structure, source preservation and publication checks | [Release audit](outputs/validation/final_release_validation.json) |
| Manual report QA, including Methodology | Approved checkpoints through `a4f47c5`; [evidence scope](docs/validation/FINAL_RELEASE_VALIDATION.md) |

Publication checks are not a new SQL rebuild, Power BI refresh or live retest of all 15 measures. Earlier one-page/12-measure outputs remain historical evidence, not current report inventories.

## Selected Validated Findings

The existing [SQL/DAX artifact](outputs/validation/powerbi_dax_runtime_validation.json) records these 2024 values; release checks compare them with the current canonical CSVs:

| Indicator | 2024 value | Scope |
|---|---:|---|
| Hospitals | 516 | National, all sectors |
| Beds | 82,721 | National, all sectors |
| Workforce Count | 681,914 | National, approved sector/profession detail |
| Saudi Workforce Share | 74.29% | MOH Total nationality workforce only |
| Encounters | 170,231,304 | National, all sectors |
| Admissions | 3,630,334 | National, all sectors |
| Red Crescent Cases | 566,288 | Administrative regions aggregated |

These are descriptive observations. Screenshot labels such as “83K” and “4M” are display rounding, not replacement baselines.

## Data Quality & Analytical Limitations

Published rates retain official definitions and precision. Geography, scope and definition differences restrict comparisons. Annual counts are not evidence of individual patient outcomes or causality. Red Crescent volumes describe workload and capacity, not response time or service quality. Screenshots do not prove every filter combination.

## Repository Structure

```text
data/          Canonical CSVs and source policy; local SQLite reference excluded
docs/          Contracts, model, KPIs, validation and handoff history
outputs/       Discovery, reconciliation and descriptive analytical evidence
powerbi/       PBIP entry point, PBIR report and TMDL model
screenshots/   Seven approved captures and gallery
scripts/       SQL loaders, validators and release audit
sql/           SQL Server DDL and labeled SQLite reference scripts
src/           Source discovery and canonical transformation
README.md
CHANGELOG.md
PROJECT_PLAN.md
requirements.txt
LICENSE
```

Local `row_data/`, environments and Power BI caches are excluded. Empty scaffold directories are not presented as implemented functionality.

## Reproduce the Project

Prerequisites: Python with the [listed dependencies](requirements.txt), SQL Server, Microsoft ODBC Driver 18, Windows Authentication, and Power BI Desktop supporting these PBIP/PBIR/TMDL files.

```powershell
git clone https://github.com/khaledzidan203-stack/saudi-healthcare-analytics.git
cd saudi-healthcare-analytics
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python scripts/verify_repository_baseline.py
```

Included canonical CSVs allow SQL/report reproduction without raw workbooks. To reproduce from Excel, follow [source placement and transformation instructions](data/README.md).

Create an empty dedicated `SaudiHealthcareAnalytics` database on `localhost` using SSMS and Windows Authentication. The SQL loader **drops and recreates the nine analytical tables**; use only a dedicated development database. [SQL execution order](sql/README.md).

```powershell
python scripts/build_sqlite_model.py
python scripts/build_sqlserver_model.py
python scripts/validate_sqlserver_model.py
```

SQLite is built because the SQL Server validator compares its reference counts. Open `powerbi/SaudiHealthcareAnalytics.pbip`, authenticate to SQL Server and refresh in Import mode. [Power BI guide](powerbi/README.md).

Offline publication checks: `python scripts/validate_release.py`.

## Source Attribution

Saudi Ministry of Health, [official Statistical Yearbook portal](https://www.moh.gov.sa/en/ministry/statistics/book/pages/default.aspx), checked during release preparation. Workbook/sheet lineage is retained in canonical data and the [lineage output](outputs/validation/source_lineage.csv).

## License

[MIT](LICENSE) applies to original project code and documentation. Official MOH data, derived source values and third-party assets remain subject to provider terms; no MOH data license or ownership is claimed. Screenshots contain provider-derived statistics.
