# PROJECT PLAN

## Project

Saudi Healthcare Capacity & Performance Analytics 2021–2024

## Primary Goal

Build a professional end-to-end Healthcare Analytics portfolio project
using official Saudi Ministry of Health data.

## Current Phase

Final portfolio release — completed analytics packaged for public GitHub publication.

Completed analytical baseline: `a4f47c5` (Methodology & Validation). The report
has INDEX plus six approved pages. Publication keeps Executive Overview Year
= 2024 and opens at INDEX. See [release validation](docs/validation/FINAL_RELEASE_VALIDATION.md).

The following phase list preserves the original plan, not a claim that every
proposed feature was implemented. The delivered SQL model loads canonical CSVs
directly into `analytics`; no separate RAW/STAGING SQL layers are claimed.

## Planned Phases

### Phase 0 — Project Bootstrap
- Repository structure
- Python environment
- Git initialization
- Project control documents

### Phase 1 — Data Discovery
- Inventory all workbooks
- Inventory all worksheets
- Inspect worksheet structures
- Identify real table boundaries
- Identify candidate dimensions and measures
- Identify year fields
- Identify health-region fields
- Define candidate grain
- Identify structural differences across years

### Phase 2 — Data Quality Assessment
- Missing values
- Duplicate business keys
- Structural rows
- Mixed data types
- Region-name inconsistencies
- Year inconsistencies
- Numeric parsing risks
- Totals/subtotals
- Notes/footnotes mixed with data

### Phase 3 — Canonical Data Contracts
- Region mapping
- Dataset contracts
- Grain contracts
- Key definitions
- Inclusion/exclusion rules

### Phase 4 — Python Data Preparation
- Reusable ingestion
- Header normalization
- Region canonicalization
- Type normalization
- Structural-row handling
- Validation

### Phase 5 — SQL Foundation
- RAW
- STAGING
- ANALYTICS
- Star schema
- Validation queries
- Analytical views

### Phase 6 — KPI Contracts
- Business definitions
- Numerator
- Denominator
- Grain
- Population
- Filters
- Time logic
- Total behavior
- Validation baseline

### Phase 7 — Python EDA
- National trends
- Regional trends
- Capacity analysis
- Workforce analysis
- Healthcare activity analysis
- Resource/activity relationships

### Phase 8 — Power BI
- Power Query
- Semantic model
- Explicit DAX measures
- Validation
- Analytical report pages

### Phase 9 — QA & Reconciliation
- Source vs Python
- Python vs SQL
- SQL vs DAX
- Sample validation
- Total reconciliation

### Phase 10 — Portfolio Release
- GitHub README
- Architecture
- Data dictionary
- KPI dictionary
- Screenshots
- Insights
- Limitations
- Reproduction instructions
- LinkedIn case study

## Historical restrictions during discovery (superseded by completed checkpoints)

- Cleaning source files
- Final KPI selection
- Final star schema
- DAX
- Dashboard visuals
- Statistical conclusions
- Business recommendations
