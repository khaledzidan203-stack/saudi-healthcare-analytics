# SQL execution guide

Final source: SQL Server `localhost`, database `SaudiHealthcareAnalytics`, schema `analytics`, Windows Authentication. Install ODBC Driver 18 and `pyodbc`.

Create the empty database in SSMS first. The loader connects to that existing database; `00_create_database.sql` creates the schema, not the database.

**Use a dedicated development database:** `01_create_dimensions_sqlserver.sql` drops existing project facts and dimensions. A rebuild replaces their contents.

```powershell
python scripts/build_sqlserver_model.py
python scripts/validate_sqlserver_model.py
```

The loader executes:

1. `00_create_database.sql` — create `analytics` schema if absent.
2. `01_create_dimensions_sqlserver.sql` — recreate dimensions.
3. `02_create_facts_sqlserver.sql` — create facts and constraints.
4. Load canonical CSVs, mapping labels to surrogate keys.
5. `03_constraints_indexes_sqlserver.sql` — create indexes.

No password is embedded. Trusted-connection settings are local development settings, not a deployment security template. The validator checks keys, grains, counts, joins, canonical reconciliation and workforce contracts. Its SQLite count comparison requires `python scripts/build_sqlite_model.py` first.

## SQLite reference only

`00_create_database_or_schema.sql`, `01_create_dimensions.sql`, `02_create_facts.sql`, `05_constraints_indexes.sql` and `06_validation.sql` belong to the historical SQLite implementation, used by `scripts/build_sqlite_model.py` and `scripts/validate_sqlite_model.py`. Do not run them as SQL Server DDL. SQLite is not a Power BI source.

[Model and grain](../docs/architecture/SQL_STAR_SCHEMA.md) · [Validation](../outputs/validation/sqlserver_validation.json)
