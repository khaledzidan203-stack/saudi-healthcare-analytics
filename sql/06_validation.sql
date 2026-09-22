PRAGMA foreign_keys = ON;

-- Executed by scripts/validate_sqlite_model.py.
SELECT 'fact_capacity' AS table_name, COUNT(*) AS row_count FROM fact_capacity
UNION ALL SELECT 'fact_activity', COUNT(*) FROM fact_activity
UNION ALL SELECT 'fact_workforce_sector', COUNT(*) FROM fact_workforce_sector
UNION ALL SELECT 'fact_workforce_nationality', COUNT(*) FROM fact_workforce_nationality;

SELECT 'broken_foreign_keys' AS check_name, COUNT(*) AS failures
FROM pragma_foreign_key_check;
