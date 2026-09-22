# Script Index

## Project

**Saudi Healthcare Capacity & Performance Analytics 2021–2024**

This document identifies the current validated production scripts.

Superseded scripts are removed from the active codebase.
Historical versions are retained through Git history.

---

## Phase 1 — Data Discovery

### 01_workbook_inventory.py

**Purpose**

Initial immutable inventory of official Saudi Ministry of Health Excel workbooks and worksheets.

**Primary outputs**

- Workbook count
- Worksheet count
- Workbook / sheet inventory

**Source modification**

None.

---

### 02_comprehensive_discovery.py

**Purpose**

Comprehensive structural profiling of all source worksheets.

**Functions**

- worksheet dimensions
- candidate header detection
- candidate data-start detection
- keyword discovery
- year discovery
- region discovery
- initial structural / data quality risks
- preview generation

**Source modification**

None.

---

### 03_build_discovery_catalog.py

**Purpose**

Convert hundreds of discovered worksheets into an analytical discovery catalog.

**Functions**

- topic classification
- geography-level candidates
- cross-year match candidates
- geography dictionary candidates
- priority review queue

---

### 04_final_discovery_scope.py

**Purpose**

Reduce the full source inventory to multi-year comparability candidates and portfolio-relevant healthcare domains.

**Functions**

- four-year comparison candidates
- core portfolio candidates
- geography contract review
- manual validation queue

---

## Phase 2 — Source & Data Contract Validation

### 05_validate_data_contract.py

**Purpose**

Validate the actual source worksheets behind shortlisted analytical groups.

**Functions**

- structural cross-year comparison
- header evidence
- unit evidence
- candidate grain definition
- manual approval register

---

### 06_build_core_validation_pack.py

**Purpose**

Produce a side-by-side validation pack for high-value analytical source groups across 2021–2024.

**Core domains reviewed**

- healthcare capacity
- healthcare workforce
- healthcare activity
- selected regional emergency infrastructure/activity

**Important rule**

A source group is not approved merely because its structure looks similar.
Business definition, grain, geography, units and totals must also be compatible.

---

## Phase 3 — Canonical Dataset

### 08_build_canonical_dataset.py

**Purpose**

Build the current canonical analytical datasets from approved core source groups.

**Canonical outputs**

- fact_capacity
- fact_activity
- fact_workforce_sector
- fact_workforce_nationality
- dim_year
- dim_geography
- dim_sector
- dim_workforce_type
- dim_nationality

**Important design rules**

- one reporting year is sourced from that year's own Statistical Yearbook
- historical rolling columns are not loaded as duplicate observations
- aggregate workforce rows that cause double counting are excluded
- Health Region, Administrative Region and Health Cluster are not assumed equivalent
- missing values are not converted to zero
- Excel formula cells can use cached calculated values
- canonical grain is explicitly validated
- source lineage is retained

**Regression requirement**

`fact_workforce_nationality` must contain:

`4 years × 2 scopes × 6 workforce types × 2 nationalities = 96 rows`

Specific regression case:

`2021 × MOH Total × Pharmacists × Non-Saudi = 131`

---

## Superseded Scripts

The following script was replaced and must not exist in the active codebase:

`src/transformation/07_build_canonical_dataset.py`

Its historical implementation is preserved only through Git history.

---

## Governance Rule

For every future analytical phase:

1. Define the business / analytical requirement.
2. Implement code inside the project.
3. Run the code.
4. Validate analytical correctness.
5. Fix root causes where required.
6. Remove superseded production code.
7. Update documentation.
8. Commit the validated phase locally to Git.
9. Continue to the next phase only after the validation gate passes.

Git is the official history of the analytical codebase.

---

## Repository Validation Utility

### verify_repository_baseline.py

**Location**

`scripts/verify_repository_baseline.py`

**Purpose**

Permanent regression and repository audit utility.

**Validates**

- required production scripts are Git tracked
- required project documentation is Git tracked
- official raw source workbooks are not Git tracked
- superseded Phase 3 script is absent
- canonical fact outputs exist
- canonical natural grains contain no duplicates
- primary measures are populated
- reporting years cover 2021–2024
- workforce nationality fact contains the complete 96-row matrix
- FY-008 regression case:
  `2021 × MOH Total × Pharmacists × Non-Saudi = 131`

**Gate**

A successful run must end with:

`PASS: PROJECT BASELINE AND PHASE 3 FULLY VERIFIED`

and

`READY FOR PHASE 4 — SQL FOUNDATION`
