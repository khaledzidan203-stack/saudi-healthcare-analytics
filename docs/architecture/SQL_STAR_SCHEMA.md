# SQL Star Schema

## Final Engine

The final Power BI analytical source is SQL Server 2025 Developer Edition,
server `localhost`, database `SaudiHealthcareAnalytics`, schema `analytics`,
using Windows Authentication. The validated SQLite database remains an
intermediate/reference baseline only.

## Reference Engine

SQLite 3.50.4 remains available at
`data/processed/sqlite/healthcare_analytics.sqlite` for cross-engine
reconciliation.

## Tables and grain

- `dim_year`: one row per reporting year.
- `dim_geography`: one row per geography type/name; National and Administrative
  Region remain separate concepts.
- `dim_sector`: one row per approved sector.
- `dim_workforce_type`: six approved leaf workforce types.
- `dim_nationality`: Saudi and Non-Saudi.
- `fact_capacity`: Year × Geography × Sector × CapacityMeasure.
- `fact_activity`: Year × Geography × Sector × ActivityMeasure.
- `fact_workforce_sector`: Year × National Geography × Sector × WorkforceType.
- `fact_workforce_nationality`: Year × National Geography × Scope ×
  WorkforceType × Nationality.

All facts use surrogate integer dimension keys, retained source lineage, NOT
NULL primary measures, and unique constraints on their business grain. SQL
Server fact values use `decimal(28,15)` to preserve published rates exactly.

## Load order

`00_create_database.sql` → dimensions → facts → indexes. The
`scripts/build_sqlserver_model.py` loader maps canonical CSV labels to
dimension keys and refuses duplicate business grains through database
constraints. Validation is executed by `scripts/validate_sqlserver_model.py`.
