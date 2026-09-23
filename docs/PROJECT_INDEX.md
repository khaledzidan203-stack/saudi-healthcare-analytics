# Saudi Healthcare Capacity & Performance Analytics 2021–2024

## Project Status

Current validated stage:

**Completed analytics and approved seven-page report; final portfolio release**

Next planned stage:

**Public portfolio delivery; no further analytical build required**

## Reviewer navigation

- [Business context, architecture and findings](../README.md)
- [Source/data policy](../data/README.md)
- [Canonical data contract](architecture/CANONICAL_DATA_CONTRACT.md)
- [Data dictionary](architecture/DATA_DICTIONARY.md)
- [SQL star schema](architecture/SQL_STAR_SCHEMA.md)
- [KPI contract](kpi/KPI_CONTRACT.md)
- [DAX dictionary](powerbi/DAX_MEASURE_DICTIONARY.md)
- [Power BI opening and refresh guide](../powerbi/README.md)
- [Seven-page screenshot gallery](../screenshots/README.md)
- [Final validation and limitations](validation/FINAL_RELEASE_VALIDATION.md)
- [Script index](SCRIPT_INDEX.md)

---

## Analytical Workflow

Business Context  
→ Problem / Decision  
→ Analytical Questions  
→ Source Discovery  
→ Grain & Geography Review  
→ Data Quality  
→ Source Selection  
→ Data Contract  
→ Canonical Transformation  
→ Validation / Reconciliation  
→ SQL Model  
→ KPI Contracts  
→ Analysis  
→ Power BI  
→ Portfolio Publication

---

## Completed Phases

### Phase 1A — Workbook Inventory

Official MOH Excel workbooks were inventoried without modifying raw source files.

### Phase 1B — Comprehensive Discovery

All available worksheets were structurally profiled.

### Phase 1C — Discovery Catalog & Scope

Cross-year analytical candidates were identified and the project scope was narrowed to high-value healthcare domains.

### Phase 2A — Data Contract Validation

Shortlisted sources were inspected for structural, geography, unit and grain compatibility.

### Phase 2B — Core Source Validation

Selected source tables were manually reviewable side-by-side across 2021–2024.

### Phase 3 — Canonical Dataset

Validated source groups were transformed into canonical facts and dimensions with lineage and reconciliation.

---

## Current Core Analytical Scope

### Healthcare Capacity

- Hospitals
- Beds
- Beds per 10,000 population
- First Aid Centers
- Ambulances

### Healthcare Workforce

- Physicians
- Dentists
- Nurses
- Midwives
- Pharmacists
- Allied Health Personnel
- Saudi workforce percentage
- Saudi / Non-Saudi workforce
- PHC workforce

### Healthcare Activity

- Encounters
- Encounters per person
- Inpatients / admissions
- Admissions per 100 persons
- Saudi Red Crescent cases

---

## Geography Contract

Current Core model supports:

- National — Saudi Arabia
- Administrative Region

The following concepts remain separate and are not automatically mapped:

- Health Region
- Health Cluster
- Administrative Region

---

## Source Policy

Official raw source workbooks remain immutable and are excluded from Git.

Canonical analytical datasets are reproducible through project scripts.

---

## Current Production Scripts

See:

`docs/SCRIPT_INDEX.md`

---

## Completed report checkpoint

`a4f47c5` finalizes Methodology & Validation after the analytical page commits.
The original 12-measure runtime suite passed at `99b573f`. The current model
has 15 measures and ten total tables (nine business tables plus `_Measures`).
Earlier baseline and handoff documents remain useful historical records; use
the final validation record above for current inventory and evidence scope.

