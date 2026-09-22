# Saudi Healthcare Capacity & Performance Analytics 2021–2024

## Project Status

Current validated stage:

**Phase 3 — Canonical Dataset Validated; SQL Foundation Next**

Next planned stage:

**SQL Environment Discovery and Star Schema**

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

## Next Gate

Phase 3 passed. The SQL star schema, SQL validation, KPI contracts, EDA
outputs, and Power BI handoff package are now prepared. Power BI implementation
is the next user-owned step.

