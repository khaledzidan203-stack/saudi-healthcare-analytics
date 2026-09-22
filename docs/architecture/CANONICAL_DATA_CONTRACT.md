# Canonical Data Contract

## Project

**Saudi Healthcare Capacity & Performance Analytics 2021–2024**

## Source Rule

For the canonical annual dataset, each reporting year is taken from the Statistical Yearbook published for that same year. Historical rolling-year columns contained in later yearbooks are not loaded as duplicate observations.

Example:

- 2021 → 2021 Yearbook
- 2022 → 2022 Yearbook
- 2023 → 2023 Yearbook
- 2024 → 2024 Yearbook

This prevents duplicated historical observations from rolling five-year tables.

## Fact_Capacity Grain

`One row = Year × Geography Type × Geography × Sector × Capacity Measure`

Current measure families:

- Hospitals
- Beds
- Beds per 10,000 population
- First Aid Centers
- Ambulances

## Fact_Activity Grain

`One row = Year × Geography Type × Geography × Sector × Activity Measure`

Current measure families:

- Encounters
- Encounters per person per year
- Inpatients / Admissions
- Admissions per 100 persons
- Saudi Red Crescent cases offered first aid / transported

## Fact_Workforce_Sector Grain

`One row = Year × National Geography × Health Sector × Workforce Type`

Measures:

- WorkforceCount
- SaudiPercent

## Fact_Workforce_Nationality Grain

`One row = Year × National Geography × Scope × Workforce Type × Nationality`

Scopes:

- MOH Total
- MOH Primary Health Care Centers

Nationalities:

- Saudi
- Non-Saudi

## Workforce Types

- Physicians
- Dentists
- Nurses
- Midwives
- Pharmacists
- Allied Health Personnel

Aggregate categories such as `Physicians & Dentists`, `Total Nurses and Midwives`, and grand totals are intentionally excluded from canonical detail facts to avoid double counting.

## Geography Contract

Current approved geography concepts:

- National → Saudi Arabia
- Administrative Region → 13 Saudi administrative regions

`Health Region` and `Health Cluster` are not currently loaded into the Core canonical model. They remain separate concepts for future extensions.

## Total Behavior

Source grand-total rows are not loaded as detail rows where they would duplicate lower-grain observations. Power BI / SQL totals should aggregate the canonical detail rows unless the KPI contract specifically defines an official published rate.

Published rates such as `Beds per 10,000 population`, `Encounters per person`, and `Admissions per 100 persons` are kept as separate official measures and must not be summed across categories.

## FY-029 Decision

Blood Bank Activity is excluded from the Core multi-year trend because the available measure definitions change materially between years. It may be analyzed separately under a dedicated measure-level contract.

## Null / Blank / Zero Rule

- NULL / missing source value = unknown or unavailable
- Blank label = structural / inherited header where applicable
- Zero = genuine reported zero only
- No missing numeric value is automatically converted to zero

## Validation Rule

Canonical outputs require:

- zero duplicate natural keys
- complete 2021–2024 coverage
- no missing primary measure values
- source lineage retained
- independent reconciliation where another official source table supports the same metric
