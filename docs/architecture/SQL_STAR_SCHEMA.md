# SQL Star Schema

## Engine

The project uses SQLite 3.50.4 through the existing Python 3.13 standard
library. PostgreSQL 17 is installed and running but requires unavailable local
credentials; SQL Server is installed but local ODBC connectivity fails before
database authentication. SQLite is therefore the reproducible, portable
engine selected for this repository.

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
NULL primary measures, and unique constraints on their business grain.

## Load order

`00_create_database_or_schema.sql` → dimensions → facts → indexes. The
`scripts/build_sqlite_model.py` loader maps canonical CSV labels to dimension
keys and refuses duplicate business grains through database constraints.
