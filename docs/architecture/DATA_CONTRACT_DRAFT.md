# Data Contract Draft

## Project

**Saudi Healthcare Capacity & Performance Analytics 2021–2024**

## Status

**DRAFT — NOT YET APPROVED**

This contract is generated from source discovery and structural validation. No source table is approved for transformation until business meaning, grain, geography, units, totals, and source notes are manually reviewed.

## Source System

- Official Saudi Ministry of Health Statistical Yearbooks
- Years: 2021, 2022, 2023, 2024
- Original Excel workbooks remain immutable

## Candidate Analytical Domains

- Activity: 7 candidate groups
- Capacity | Activity: 6 candidate groups
- Workforce: 5 candidate groups
- Capacity: 5 candidate groups
- Capacity | Workforce: 3 candidate groups
- Population: 2 candidate groups
- Population | Capacity: 1 candidate groups
- Workforce | Activity: 1 candidate groups
- Population | Activity: 1 candidate groups

## Structural Validation Status

- REVIEW_REQUIRED: 30
- STRONG_CANDIDATE: 1

## Geography Contract

The project must distinguish at minimum:

1. National-level observations
2. Health Region observations
3. Health Cluster observations

`Health Region` and `Health Cluster` must not be merged into one entity without an explicit, validated mapping and compatible time logic.

## Grain Contract Rule

Every final fact table must have a documented statement:

`One row = <business dimensions>`

No joins, aggregations, or KPI calculations may be approved before that grain is validated against the source tables.

## Preliminary Fact Candidates

These are architecture candidates only:

- Fact_PopulationIndicators
- Fact_HealthcareCapacity
- Fact_HealthcareWorkforce
- Fact_HealthcareActivity

Final fact boundaries may change after manual source validation.

## Preliminary Shared Dimensions

- Dim_Year
- Dim_Geography
- Dim_Indicator
- Dim_FacilityType, if supported
- Dim_WorkforceType / Profession, if supported
- Dim_ActivityType, if supported

## Mandatory Validation Before Approval

For every source group:

- Same business definition across years
- Same or explicitly reconcilable grain
- Same geography concept
- Same unit / denominator definition
- Total and subtotal rows identified
- Footnotes and methodological notes reviewed
- Header and data boundaries confirmed
- Final source inclusion decision documented

## Cleaning Status

**NOT STARTED.**
