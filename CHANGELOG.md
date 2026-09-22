# Changelog

All notable validated analytical changes to this project are documented here.

---

## Power BI Checkpoint 3 — Governed DAX Layer

### Added

- zero-business-row `_Measures` table with hidden placeholder
- 12 approved KPI measures, all owned by `_Measures`
- healthcare-specific display-folder organization and formats
- static TMDL validation and read-only SQL baselines for all KPIs
- governed DAX measure dictionary

### Validation

- static semantic validation: PASS
- SQL baselines: 12 / 12 PASS
- runtime DAX execution: PENDING Power BI Desktop reopen

---

## Power BI Checkpoint 1 — Baseline Discovery

### Documented

- inspected the user-created PBIP/PBIR/TMDL structure read-only
- confirmed nine visible SQL Server business tables and 14 star-schema
  relationships
- confirmed no measures, visuals, hidden tables, Auto Date/Time tables,
  many-to-many, bidirectional, inactive, or fact-to-fact relationships
- recorded summarization and technical-key hardening risks

Power BI artifacts were not modified.

---

## SQL Server Analytical Foundation

### Added

- SQL Server schema `analytics` in `SaudiHealthcareAnalytics`
- five dimensions and four validated fact tables
- governed canonical loader and independent SQL Server validation
- exact canonical and SQLite reference reconciliation

### Validation

- FactCapacity: 132
- FactActivity: 84
- FactWorkforceSector: 72
- FactWorkforceNationality: 96
- broken foreign keys: 0
- duplicate fact grains: 0
- FY006 ↔ FY008: 24 / 24 passed
- 2021 MOH Total Pharmacists Non-Saudi: 131

---

## Phase 3 — Canonical Validation Repair

### Fixed

- restored the 2021 FY-008 Pharmacists / Non-Saudi row from its cached source
  value of 131
- prevented aggregate workforce labels from inheriting the preceding leaf
  workforce type
- added conservative additive source-reference fallback handling
- added independent machine-readable Phase 3 validation and Saudi-percent
  reconciliation

### Validation

- `fact_capacity`: 132 rows
- `fact_activity`: 84 rows
- `fact_workforce_sector`: 72 rows
- `fact_workforce_nationality`: 96 rows
- FY-006 ↔ FY-008 reconciliation: 24 / 24 passed

---

## Phase 3 — Canonical Dataset

### Added

- Canonical capacity fact
- Canonical activity fact
- Workforce by sector fact
- Workforce by nationality fact
- Year dimension
- Geography dimension
- Sector dimension
- Workforce type dimension
- Nationality dimension
- Source lineage
- Canonical reconciliation
- Workforce cross-source reconciliation

### Fixed

Excel formula-based numeric source cells are now handled using cached Excel calculated values where appropriate.

Specific regression case restored:

- Year: 2021
- Scope: MOH Total
- Workforce Type: Pharmacists
- Nationality: Non-Saudi
- Value: 131

### Removed

Superseded:

`src/transformation/07_build_canonical_dataset.py`

Current:

`src/transformation/08_build_canonical_dataset.py`

---

## Phase 2B — Core Source Validation

Added cross-year source validation pack for shortlisted healthcare analytical domains.

---

## Phase 2A — Data Contract Validation

Added:

- source selection candidates
- cross-year structure validation
- header/unit evidence
- grain candidates
- manual approval register

---

## Phase 1C — Final Discovery Scope

Added:

- four-year comparability candidates
- core portfolio candidates
- geography contract review
- manual validation queue

---

## Phase 1B — Discovery Catalog

Added:

- discovery catalog
- cross-year matching candidates
- geography dictionary candidates
- priority review queue

---

## Phase 1A — Source Discovery

Added official workbook and worksheet inventory while preserving raw source immutability.

---

## Phase 3 — Final Formula Resolution Fix

### Fixed

The canonical extraction pipeline now resolves simple source formulas
whose Excel cached result is unavailable.

Confirmed regression:

- 2021
- MOH Total
- Pharmacists
- Non-Saudi
- WorkforceCount = 131

Expected workforce nationality fact:

- 96 rows
- zero duplicate natural keys

### Production script

Current:

`src/transformation/09_build_canonical_dataset.py`

Superseded and removed:

`src/transformation/08_build_canonical_dataset.py`
