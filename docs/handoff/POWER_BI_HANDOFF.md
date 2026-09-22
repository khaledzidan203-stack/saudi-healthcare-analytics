# Pre-Power-BI Handoff

## Semantic model recommendation

Use the four validated facts and five dimensions from the SQLite model. Relate
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

## DAX backlog only

Create measures for additive counts, ratio-of-totals cases per center/ambulance,
Saudi share, and prior-year growth. Validate each measure against the KPI
contract and the canonical/SQL outputs before publishing.

## Limitations

Official rates are source-published and non-additive. Health Region and Health
Cluster are not mapped to Administrative Region. FY-029 Blood Bank is excluded
from the core trend. No causal inference is supported by these descriptive data.

Power BI files, semantic models, DAX, Power Query, and report pages are
intentionally not created in this repository.
