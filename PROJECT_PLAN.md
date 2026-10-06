# PROJECT PLAN

## Project

Saudi Healthcare Capacity & Performance Analytics 2021–2024

## Primary goal

Build an end-to-end healthcare analytics implementation using official Saudi Ministry of Health statistical yearbooks, with governed data contracts, reproducible transformation, SQL modeling, Power BI semantic design, validation, and documented analytical boundaries.

## Current phase

**Completed analytical release — maintenance and evidence-preserving documentation only.**

Analytical baseline: `a4f47c5` (`feat(powerbi): finalize methodology validation page`). The current report contains INDEX plus six analytical/methodology pages, opens at INDEX, and preserves the approved Executive Overview Year = 2024 state.

Current release inventory:

- 4 canonical facts + 5 dimensions
- SQL Server `analytics` schema
- 10 Power BI semantic tables including `_Measures`
- 14 active M:1 single-direction relationships
- 15 current measures
- 7 report pages
- 121 saved visuals

See [Final Release Validation](docs/validation/FINAL_RELEASE_VALIDATION.md) and [Project Evidence Map](docs/PROJECT_EVIDENCE_MAP.md).

## Implementation phases

### Phase 0 — Project bootstrap
- Repository structure
- Python environment
- Git initialization
- Project control documents

### Phase 1 — Data discovery
- Inventory official workbooks and worksheets
- Inspect worksheet structures
- Identify true table boundaries
- Identify candidate dimensions and measures
- Identify year and geography concepts
- Review structural differences across years

### Phase 2 — Data quality and source assessment
- Missing values
- Duplicate business keys
- Structural rows
- Mixed data types
- Geography inconsistencies
- Year inconsistencies
- Numeric parsing risks
- Totals/subtotals
- Notes/footnotes mixed with data

### Phase 3 — Canonical contracts
- Geography contract
- Dataset contracts
- Grain contracts
- Key definitions
- Inclusion/exclusion rules
- Source lineage

### Phase 4 — Python transformation
- Workbook discovery
- Header normalization
- Geography normalization
- Type normalization
- Structural-row handling
- Canonical output generation
- Independent validation

### Phase 5 — SQL analytical foundation
The original plan considered RAW / STAGING / ANALYTICS SQL layers. The final implementation intentionally loads the governed canonical CSV layer directly into the SQL Server `analytics` star schema. No separate implemented RAW/STAGING SQL layers are claimed.

Implemented:
- SQL Server database and `analytics` schema
- Dimensions and facts
- Grain constraints and indexes
- Canonical loading
- SQL validation and reconciliation
- SQLite reference model for cross-engine comparison

### Phase 6 — KPI contracts
- Business definition
- Numerator / denominator
- Grain
- Filters
- Aggregation behavior
- Null / zero handling
- Validation baseline

### Phase 7 — Analytical review
- National trends
- Capacity
- Workforce
- Healthcare activity
- Red Crescent regional resources/activity
- Source and interpretation limits

### Phase 8 — Power BI
- SQL import model
- TMDL semantic model
- Explicit DAX measures
- Relationship hardening
- PBIR report pages
- Navigation and saved states

### Phase 9 — QA and reconciliation
- Canonical validation
- Canonical ↔ SQL reconciliation
- Cross-source workforce reconciliation
- SQL ↔ DAX runtime evidence for original governed measures
- PBIR/report structure validation
- Screenshot integrity
- Release audit

### Phase 10 — Publication and reproducibility
- README and architecture
- Data dictionary
- KPI/DAX documentation
- Evidence map and case study
- Screenshots
- Limitations and source governance
- Reproduction instructions
- Automated read-only repository validation

## Maintenance rule

Future work must not silently change canonical data, SQL/DAX logic, TMDL/PBIR source, or approved screenshots. Any analytical change requires a versioned change, targeted revalidation, and updated evidence.
