# Power BI Baseline Discovery

## Artifact

`powerbi/SaudiHealthcareAnalytics.pbip` was inspected read-only. The PBIP
references `SaudiHealthcareAnalytics.Report` and its semantic model.

## Model inventory

All nine business tables are visible; no hidden tables were found:

- Dimensions: analytics DimYear, DimGeography, DimSector,
  DimWorkforceType, DimNationality
- Facts: analytics FactCapacity, FactActivity,
  FactWorkforceSector, FactWorkforceNationality

There are no measures, calculation groups, or `_Measures` table.

## Relationships

Fourteen relationships exist. Each is an active dimension-to-fact key
relationship with the fact side many and dimension side one, using the default
single cross-filter direction. No many-to-many, bidirectional, inactive,
fact-to-fact, or ambiguous relationship paths were found.

- DimYear → all four facts
- DimGeography → all four facts
- DimSector → FactCapacity, FactActivity, FactWorkforceSector
- DimWorkforceType → FactWorkforceSector, FactWorkforceNationality
- DimNationality → FactWorkforceNationality

The TMDL relationship blocks omit explicit cardinality and cross-filter
properties; the inventory above reflects the Power BI relationship defaults
for these dimension-key joins and should be confirmed during hardening.

## Sources and partitions

All nine tables use Import-mode M partitions sourced from SQL Server
`localhost`, database `SaudiHealthcareAnalytics`, schema `analytics`. No raw
Excel, canonical CSV, or SQLite partition was found.

## Date and time

Auto Date/Time is disabled and no LocalDateTable exists. DimYear is present but
contains YearKey and YearValue only; it is not marked as a Date Table. A date
dimension is not required for the current annual grain, but time-intelligence
behavior should remain disabled unless a real date column is introduced.

## Current report topology

- Pages: 1 (`Page 1`)
- Visuals: 0
- Report-level measures: 0

## Baseline risks for Checkpoint 2

- Technical surrogate keys are visible and should likely be hidden.
- Fact identity keys currently use `count` summarization and should be hidden.
- Fact `Value` and `WorkforceCount` are additive source columns; governed
  measures should own user-facing aggregation later.
- `SaudiPercent` is currently summarized by `sum`, which is unsafe and should
  be changed to `Do not summarize` during semantic-model hardening.
- DimYear.YearValue is currently summarized by `sum`; it should be
  non-summarizable and used as a categorical year field.
- No explicit sort metadata is present; YearValue should sort by itself once
  its category behavior is hardened.

PBIP/PBIR/TMDL files were structurally readable and internally consistent for
this baseline inspection. No Power BI artifacts were modified.

## Checkpoint 2 outcome

The semantic model was hardened without changing tables, business logic,
measures, pages, visuals, SQL, or KPI definitions:

- all 14 relationships are explicitly active, M:1, and single-direction;
- surrogate, foreign, identity, and lineage columns are hidden;
- YearValue and non-additive percentage/value fields do not summarize;
- additive workforce counts retain Sum;
- the year-grain model remains unmarked as a Date Table.
