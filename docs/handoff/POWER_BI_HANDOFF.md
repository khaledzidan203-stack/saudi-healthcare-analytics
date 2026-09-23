# Pre-Power-BI Handoff

## Semantic model recommendation

Historical pre-implementation handoff. The report is now complete at
`a4f47c5`; page suggestions and pending statuses below record the earlier
stage, not current tasks. Use the [Power BI guide](../../powerbi/README.md)
and [release validation](../validation/FINAL_RELEASE_VALIDATION.md) for the
delivered report. The connection and nine SQL import tables remain valid.

Use the four validated facts and five dimensions from the SQL Server model. Relate
each fact to `dim_year`; relate geography-compatible facts to `dim_geography`,
sector facts to `dim_sector`, and workforce facts to their workforce and
nationality dimensions. Keep filter direction single-direction from dimensions
to facts. Do not relate National and Administrative Region as if they were the
same hierarchy.

## Suggested pages

1. Overview — headline capacity, workforce, activity and data-quality status.
2. Trend — 2021–2024 counts and official rates.
3. Workforce — type, sector and Saudi/Non-Saudi composition.
4. Regional Emergency Capacity — Red Crescent cases, centers and ambulances.
5. Details — source-lineage and row-level drill-through.
6. Data Quality — contract, null, grain and reconciliation checks.

Recommended slicers: Year, Sector, WorkforceType, Nationality, Scope,
GeographyType and Geography, with geography-level selections kept explicit.

## Validated connection

- Server: `localhost`
- Database: `SaudiHealthcareAnalytics`
- Authentication: Windows Authentication
- Mode: Import

Import only these SQL Server tables from schema `analytics`:

- `DimYear`
- `DimGeography`
- `DimSector`
- `DimWorkforceType`
- `DimNationality`
- `FactCapacity`
- `FactActivity`
- `FactWorkforceSector`
- `FactWorkforceNationality`

## Governed DAX layer

The dedicated `_Measures` table contains the 12 approved KPI measures for
additive counts, official rates, Saudi workforce share, and Red Crescent
ratio-of-totals metrics. Static and SQL-baseline validation pass; runtime DAX
value reconciliation remains pending a Power BI Desktop reopen.

## Limitations

Official rates are source-published and non-additive. Health Region and Health
Cluster are not mapped to Administrative Region. FY-029 Blood Bank is excluded
from the core trend. No causal inference is supported by these descriptive data.

No report pages, visuals, or report-specific measures have been created. Do
not load raw Excel, canonical CSVs, or SQLite into the final Power BI model.
