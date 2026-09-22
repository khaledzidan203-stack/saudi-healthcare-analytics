from pathlib import Path
import json
import sqlite3

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "processed" / "sqlite" / "healthcare_analytics.sqlite"
OUT = ROOT / "outputs" / "validation" / "sql_validation.json"

EXPECTED = {
    "fact_capacity": 132,
    "fact_activity": 84,
    "fact_workforce_sector": 72,
    "fact_workforce_nationality": 96,
}


def main():
    conn = sqlite3.connect(DB)
    conn.execute("PRAGMA foreign_keys = ON")
    checks = []

    def add(name, passed, details):
        checks.append({"name": name, "status": "PASS" if passed else "FAIL", "details": details})

    for table, expected in EXPECTED.items():
        actual = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        add(f"{table}_row_count", actual == expected, {"expected": expected, "actual": actual})

    fk = conn.execute("SELECT COUNT(*) FROM pragma_foreign_key_check").fetchone()[0]
    add("broken_foreign_keys", fk == 0, fk)

    fact_specs = {
        "fact_capacity": "year_key, geography_key, sector_key, capacity_measure",
        "fact_activity": "year_key, geography_key, sector_key, activity_measure",
        "fact_workforce_sector": "year_key, geography_key, sector_key, workforce_type_key",
        "fact_workforce_nationality": "year_key, geography_key, scope, workforce_type_key, nationality_key",
    }
    for table, key in fact_specs.items():
        duplicate = conn.execute(f"SELECT COUNT(*) FROM (SELECT {key}, COUNT(*) c FROM {table} GROUP BY {key} HAVING c > 1)").fetchone()[0]
        add(f"{table}_duplicate_business_keys", duplicate == 0, duplicate)
        years = conn.execute(f"SELECT COUNT(DISTINCT year_key) FROM {table}").fetchone()[0]
        add(f"{table}_year_coverage", years == 4, years)

    joined = conn.execute("""SELECT COUNT(*) FROM fact_capacity f
        JOIN dim_year y ON y.year_key=f.year_key
        JOIN dim_geography g ON g.geography_key=f.geography_key
        JOIN dim_sector s ON s.sector_key=f.sector_key""").fetchone()[0]
    add("capacity_join_preserves_rows", joined == EXPECTED["fact_capacity"], joined)

    reconciliation = conn.execute("""
        SELECT COUNT(*) FROM (
          SELECT s.year_key, wt.workforce_type_name
          FROM fact_workforce_sector s
          JOIN dim_sector sec ON sec.sector_key=s.sector_key
          JOIN dim_workforce_type wt ON wt.workforce_type_key=s.workforce_type_key
          JOIN dim_nationality n ON 1=1
          WHERE sec.sector_name='Ministry of Health'
          GROUP BY s.year_key, wt.workforce_type_name
          HAVING MAX(s.workforce_count) != (
            SELECT SUM(nf.workforce_count) FROM fact_workforce_nationality nf
            WHERE nf.year_key=s.year_key AND nf.workforce_type_key=s.workforce_type_key
              AND nf.scope='MOH Total'
          )
        )
    """).fetchone()[0]
    add("fy006_fy008_reconciliation", reconciliation == 0, reconciliation)
    conn.close()

    status = "PASS" if all(c["status"] == "PASS" for c in checks) else "FAIL"
    result = {"status": status, "engine": "SQLite 3.50.4", "checks": checks}
    OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"SQL VALIDATION: {status}")
    for c in checks:
        print(f"{c['status']}: {c['name']} - {c['details']}")
    raise SystemExit(0 if status == "PASS" else 1)


if __name__ == "__main__":
    main()
