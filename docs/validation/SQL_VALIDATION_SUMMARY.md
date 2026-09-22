# SQL Validation Summary

The final SQL Server model is independently reconciled back to the validated
canonical CSVs and the SQLite reference by
`scripts/validate_sqlserver_model.py`.

Connection: `localhost` / `SaudiHealthcareAnalytics` / Windows Authentication.

Required results:

- fact_capacity: 132 rows
- fact_activity: 84 rows
- fact_workforce_sector: 72 rows
- fact_workforce_nationality: 96 rows
- duplicate business keys: 0
- broken foreign keys: 0
- joined fact rows preserved without multiplication
- FY-006 ↔ FY-008 workforce reconciliation passed

Machine-readable output: `outputs/validation/sql_validation.json`.

SQL Server machine-readable output: `outputs/validation/sqlserver_validation.json`.
