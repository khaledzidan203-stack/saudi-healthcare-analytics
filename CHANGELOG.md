# Changelog

All notable validated analytical changes to this project are documented here.

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
