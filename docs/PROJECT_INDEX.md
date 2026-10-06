# Saudi Healthcare Analytics 2021–2024

## Current release status

The analytical build is complete and source-controlled as a seven-page Power BI project with governed canonical data, SQL Server modeling, explicit KPI contracts, validation evidence, and reproducible release checks.

## Navigation

| Area | Entry point |
|---|---|
| Project overview | [README](../README.md) |
| Visual architecture | [Project overview graphic](assets/Saudi%20Healthcare%20Analytics%20Pipeline%20Infographic.png) |
| Case study | [CASE_STUDY.md](CASE_STUDY.md) |
| Technical walkthrough | [TECHNICAL_WALKTHROUGH.md](TECHNICAL_WALKTHROUGH.md) |
| Evidence map | [PROJECT_EVIDENCE_MAP.md](PROJECT_EVIDENCE_MAP.md) |
| Current source governance | [SOURCE_GOVERNANCE_STATUS.md](SOURCE_GOVERNANCE_STATUS.md) |
| Source / data policy | [data/README.md](../data/README.md) |
| Canonical contract | [architecture/CANONICAL_DATA_CONTRACT.md](architecture/CANONICAL_DATA_CONTRACT.md) |
| Data dictionary | [architecture/DATA_DICTIONARY.md](architecture/DATA_DICTIONARY.md) |
| SQL star schema | [architecture/SQL_STAR_SCHEMA.md](architecture/SQL_STAR_SCHEMA.md) |
| KPI contract | [kpi/KPI_CONTRACT.md](kpi/KPI_CONTRACT.md) |
| DAX dictionary | [powerbi/DAX_MEASURE_DICTIONARY.md](powerbi/DAX_MEASURE_DICTIONARY.md) |
| Semantic model | [powerbi/POWER_BI_SEMANTIC_MODEL.md](powerbi/POWER_BI_SEMANTIC_MODEL.md) |
| Power BI opening / refresh | [powerbi/README.md](../powerbi/README.md) |
| Report captures | [screenshots/README.md](../screenshots/README.md) |
| Final validation | [validation/FINAL_RELEASE_VALIDATION.md](validation/FINAL_RELEASE_VALIDATION.md) |
| Script inventory | [SCRIPT_INDEX.md](SCRIPT_INDEX.md) |
| Data attribution | [DATA_ATTRIBUTION.md](../DATA_ATTRIBUTION.md) |

## Analytical workflow

```text
Business / analytical scope
        ↓
Source discovery
        ↓
Grain + geography review
        ↓
Canonical contracts
        ↓
Python transformation
        ↓
Canonical validation
        ↓
SQL Server analytical model
        ↓
KPI contracts
        ↓
Power BI semantic model + DAX
        ↓
PBIR report
        ↓
Reconciliation + release validation
```

## Implemented analytical scope

### Healthcare capacity

- Hospitals
- Beds
- Beds per 10,000 population
- First Aid Centers
- Ambulances

### Healthcare activity

- Encounters
- Encounters per person
- Inpatients / Admissions
- Admissions per 100 persons
- Saudi Red Crescent cases

### Healthcare workforce

- Physicians
- Dentists
- Nurses
- Midwives
- Pharmacists
- Allied Health Personnel
- Saudi / Non-Saudi workforce composition
- MOH Primary Health Care workforce scope

## Geography contract

Approved core concepts:

- National — Saudi Arabia
- Administrative Region — 13 Saudi administrative regions

Kept separate:

- Health Region
- Health Cluster

No automatic equivalence is assumed between those geography systems.

## Current model inventory

- Canonical layer: 4 facts + 5 dimensions
- SQL business tables: 9
- Power BI semantic tables: 10 total, including disconnected `_Measures`
- Relationships: 14 active M:1 single-direction
- Current measures: 15
- Report pages: 7
- Saved visuals: 121

## Validation boundary

The original 12 governed DAX measures have recorded runtime PASS evidence. The current model contains three later approved Red Crescent additions that are validated by source/model/release evidence but are not represented as if they belonged to the earlier 12-measure runtime suite.

The final release record remains the authoritative summary of current checks and historical evidence scope.

## Historical project records

Discovery summaries, handoff documents, earlier checkpoints, and the historical all-`PENDING` `FINAL_SOURCE_APPROVAL.csv` are intentionally preserved as development history. They should not override the implemented contracts, current source-governance note, saved Power BI model, or final release validation.
