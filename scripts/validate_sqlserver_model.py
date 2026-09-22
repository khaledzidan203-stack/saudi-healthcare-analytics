from collections import defaultdict
from pathlib import Path
import csv
import json
import sqlite3
import pyodbc

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "data" / "processed" / "canonical"
SQLITE = ROOT / "data" / "processed" / "sqlite" / "healthcare_analytics.sqlite"
OUTPUT = ROOT / "outputs" / "validation" / "sqlserver_validation.json"
CONNECTION = "DRIVER={ODBC Driver 18 for SQL Server};SERVER=localhost;DATABASE=SaudiHealthcareAnalytics;Trusted_Connection=yes;Encrypt=no;TrustServerCertificate=yes"


def read_csv(name):
    with (CANONICAL / name).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def main():
    checks = []

    def add(name, passed, details):
        checks.append({"name": name, "status": "PASS" if passed else "FAIL", "details": details})

    with pyodbc.connect(CONNECTION, timeout=10) as conn:
        cur = conn.cursor()
        counts = {
            "FactCapacity": ("analytics.FactCapacity", 132),
            "FactActivity": ("analytics.FactActivity", 84),
            "FactWorkforceSector": ("analytics.FactWorkforceSector", 72),
            "FactWorkforceNationality": ("analytics.FactWorkforceNationality", 96),
        }
        for label, (table, expected) in counts.items():
            actual = cur.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            add(f"{label}_row_count", actual == expected, {"expected": expected, "actual": actual})

        for label, table, key in [
            ("DimYear", "analytics.DimYear", "YearValue"),
            ("DimGeography", "analytics.DimGeography", "GeographyType, GeographyName"),
            ("DimSector", "analytics.DimSector", "SectorName"),
            ("DimWorkforceType", "analytics.DimWorkforceType", "WorkforceTypeName"),
            ("DimNationality", "analytics.DimNationality", "NationalityName"),
        ]:
            dup = cur.execute(f"SELECT COUNT(*) FROM (SELECT {key}, COUNT(*) AS c FROM {table} GROUP BY {key} HAVING COUNT(*) > 1) d").fetchone()[0]
            add(f"{label}_duplicate_business_keys", dup == 0, dup)

        fact_keys = {
            "FactCapacity": "YearKey, GeographyKey, SectorKey, CapacityMeasure",
            "FactActivity": "YearKey, GeographyKey, SectorKey, ActivityMeasure",
            "FactWorkforceSector": "YearKey, GeographyKey, SectorKey, WorkforceTypeKey",
            "FactWorkforceNationality": "YearKey, GeographyKey, Scope, WorkforceTypeKey, NationalityKey",
        }
        for label, key in fact_keys.items():
            dup = cur.execute(f"SELECT COUNT(*) FROM (SELECT {key}, COUNT(*) AS c FROM analytics.{label} GROUP BY {key} HAVING COUNT(*) > 1) d").fetchone()[0]
            add(f"{label}_duplicate_grain", dup == 0, dup)

        fk = cur.execute("SELECT COUNT(*) FROM (SELECT 1 AS bad FROM sys.foreign_keys fk JOIN sys.foreign_key_columns fkc ON fkc.constraint_object_id=fk.object_id JOIN sys.tables t ON t.object_id=fk.parent_object_id JOIN sys.tables rt ON rt.object_id=fk.referenced_object_id) x WHERE 1=0").fetchone()[0]
        # SQL Server enforces all declared FKs on load; additionally verify with orphan queries.
        orphan_queries = [
            "SELECT COUNT(*) FROM analytics.FactCapacity f LEFT JOIN analytics.DimYear d ON d.YearKey=f.YearKey WHERE d.YearKey IS NULL",
            "SELECT COUNT(*) FROM analytics.FactActivity f LEFT JOIN analytics.DimGeography d ON d.GeographyKey=f.GeographyKey WHERE d.GeographyKey IS NULL",
            "SELECT COUNT(*) FROM analytics.FactWorkforceSector f LEFT JOIN analytics.DimWorkforceType d ON d.WorkforceTypeKey=f.WorkforceTypeKey WHERE d.WorkforceTypeKey IS NULL",
            "SELECT COUNT(*) FROM analytics.FactWorkforceNationality f LEFT JOIN analytics.DimNationality d ON d.NationalityKey=f.NationalityKey WHERE d.NationalityKey IS NULL",
        ]
        orphan_total = sum(cur.execute(q).fetchone()[0] for q in orphan_queries)
        add("broken_foreign_keys", orphan_total == 0, orphan_total)

        for label, table, measure in [
            ("FactCapacity", "analytics.FactCapacity", "Value"),
            ("FactActivity", "analytics.FactActivity", "Value"),
            ("FactWorkforceSector", "analytics.FactWorkforceSector", "WorkforceCount"),
            ("FactWorkforceNationality", "analytics.FactWorkforceNationality", "WorkforceCount"),
        ]:
            nulls = cur.execute(f"SELECT COUNT(*) FROM {table} WHERE {measure} IS NULL").fetchone()[0]
            years = cur.execute(f"SELECT COUNT(DISTINCT y.YearValue) FROM {table} f JOIN analytics.DimYear y ON y.YearKey=f.YearKey").fetchone()[0]
            add(f"{label}_required_measure_nulls", nulls == 0, nulls)
            add(f"{label}_year_coverage", years == 4, years)

        joined = [
            ("FactCapacity", "analytics.FactCapacity f JOIN analytics.DimYear y ON y.YearKey=f.YearKey JOIN analytics.DimGeography g ON g.GeographyKey=f.GeographyKey JOIN analytics.DimSector s ON s.SectorKey=f.SectorKey"),
            ("FactActivity", "analytics.FactActivity f JOIN analytics.DimYear y ON y.YearKey=f.YearKey JOIN analytics.DimGeography g ON g.GeographyKey=f.GeographyKey JOIN analytics.DimSector s ON s.SectorKey=f.SectorKey"),
            ("FactWorkforceSector", "analytics.FactWorkforceSector f JOIN analytics.DimYear y ON y.YearKey=f.YearKey JOIN analytics.DimGeography g ON g.GeographyKey=f.GeographyKey JOIN analytics.DimSector s ON s.SectorKey=f.SectorKey JOIN analytics.DimWorkforceType w ON w.WorkforceTypeKey=f.WorkforceTypeKey"),
            ("FactWorkforceNationality", "analytics.FactWorkforceNationality f JOIN analytics.DimYear y ON y.YearKey=f.YearKey JOIN analytics.DimGeography g ON g.GeographyKey=f.GeographyKey JOIN analytics.DimWorkforceType w ON w.WorkforceTypeKey=f.WorkforceTypeKey JOIN analytics.DimNationality n ON n.NationalityKey=f.NationalityKey"),
        ]
        for label, join in joined:
            base = cur.execute(f"SELECT COUNT(*) FROM analytics.{label}").fetchone()[0]
            joined_count = cur.execute(f"SELECT COUNT(*) FROM {join}").fetchone()[0]
            add(f"{label}_joined_rows_preserved", joined_count == base, {"base": base, "joined": joined_count})

        # Independent canonical-to-SQL Server comparison using natural labels.
        sql_rows = {
            "FactCapacity": cur.execute("SELECT y.YearValue,g.GeographyType,g.GeographyName,s.SectorName,f.CapacityMeasure,CONVERT(float,f.Value) FROM analytics.FactCapacity f JOIN analytics.DimYear y ON y.YearKey=f.YearKey JOIN analytics.DimGeography g ON g.GeographyKey=f.GeographyKey JOIN analytics.DimSector s ON s.SectorKey=f.SectorKey").fetchall(),
            "FactActivity": cur.execute("SELECT y.YearValue,g.GeographyType,g.GeographyName,s.SectorName,f.ActivityMeasure,CONVERT(float,f.Value) FROM analytics.FactActivity f JOIN analytics.DimYear y ON y.YearKey=f.YearKey JOIN analytics.DimGeography g ON g.GeographyKey=f.GeographyKey JOIN analytics.DimSector s ON s.SectorKey=f.SectorKey").fetchall(),
            "FactWorkforceSector": cur.execute("SELECT y.YearValue,g.GeographyType,g.GeographyName,s.SectorName,w.WorkforceTypeName,f.WorkforceCount,CONVERT(float,f.SaudiPercent) FROM analytics.FactWorkforceSector f JOIN analytics.DimYear y ON y.YearKey=f.YearKey JOIN analytics.DimGeography g ON g.GeographyKey=f.GeographyKey JOIN analytics.DimSector s ON s.SectorKey=f.SectorKey JOIN analytics.DimWorkforceType w ON w.WorkforceTypeKey=f.WorkforceTypeKey").fetchall(),
            "FactWorkforceNationality": cur.execute("SELECT y.YearValue,g.GeographyType,g.GeographyName,f.Scope,w.WorkforceTypeName,n.NationalityName,f.WorkforceCount FROM analytics.FactWorkforceNationality f JOIN analytics.DimYear y ON y.YearKey=f.YearKey JOIN analytics.DimGeography g ON g.GeographyKey=f.GeographyKey JOIN analytics.DimWorkforceType w ON w.WorkforceTypeKey=f.WorkforceTypeKey JOIN analytics.DimNationality n ON n.NationalityKey=f.NationalityKey").fetchall(),
        }
        canonical = {
            "FactCapacity": [(int(r["Year"]), r["GeographyType"], r["Geography"], r["Sector"], r["CapacityMeasure"], float(r["Value"])) for r in read_csv("fact_capacity.csv")],
            "FactActivity": [(int(r["Year"]), r["GeographyType"], r["Geography"], r["Sector"], r["ActivityMeasure"], float(r["Value"])) for r in read_csv("fact_activity.csv")],
            "FactWorkforceSector": [(int(r["Year"]), r["GeographyType"], r["Geography"], r["Sector"], r["WorkforceType"], float(r["WorkforceCount"]), float(r["SaudiPercent"]) if r["SaudiPercent"] else None) for r in read_csv("fact_workforce_sector.csv")],
            "FactWorkforceNationality": [(int(r["Year"]), r["GeographyType"], r["Geography"], r["Scope"], r["WorkforceType"], r["Nationality"], float(r["WorkforceCount"])) for r in read_csv("fact_workforce_nationality.csv")],
        }
        sql_norm = {k: sorted(tuple(row) for row in v) for k, v in sql_rows.items()}
        can_norm = {"FactCapacity": sorted(canonical["FactCapacity"]), "FactActivity": sorted(canonical["FactActivity"]), "FactWorkforceNationality": sorted(canonical["FactWorkforceNationality"])}
        can_norm["FactWorkforceSector"] = sorted(canonical["FactWorkforceSector"])
        add("canonical_sqlserver_reconciliation", all(sql_norm[k] == can_norm[k] for k in can_norm), {k: len(sql_norm[k]) == len(can_norm[k]) and sql_norm[k] == can_norm[k] for k in can_norm})

        regression = cur.execute("SELECT f.WorkforceCount FROM analytics.FactWorkforceNationality f JOIN analytics.DimYear y ON y.YearKey=f.YearKey JOIN analytics.DimWorkforceType w ON w.WorkforceTypeKey=f.WorkforceTypeKey JOIN analytics.DimNationality n ON n.NationalityKey=f.NationalityKey WHERE y.YearValue=2021 AND f.Scope='MOH Total' AND w.WorkforceTypeName='Pharmacists' AND n.NationalityName='Non-Saudi'").fetchone()[0]
        add("fy008_regression", regression == 131, regression)

        reconciliation = cur.execute("""
            SELECT COUNT(*) FROM (
              SELECT y.YearValue, w.WorkforceTypeName,
                     s.WorkforceCount AS FY006,
                     SUM(n.WorkforceCount) AS FY008,
                     MAX(s.SaudiPercent) AS PublishedPct,
                     SUM(CASE WHEN dn.NationalityName='Saudi' THEN n.WorkforceCount ELSE 0 END) * 100.0 / SUM(n.WorkforceCount) AS CalculatedPct
              FROM analytics.FactWorkforceSector s
              JOIN analytics.DimYear y ON y.YearKey=s.YearKey
              JOIN analytics.DimSector sec ON sec.SectorKey=s.SectorKey
              JOIN analytics.DimWorkforceType w ON w.WorkforceTypeKey=s.WorkforceTypeKey
              JOIN analytics.FactWorkforceNationality n ON n.YearKey=s.YearKey AND n.WorkforceTypeKey=s.WorkforceTypeKey AND n.Scope='MOH Total'
              JOIN analytics.DimNationality dn ON dn.NationalityKey=n.NationalityKey
              WHERE sec.SectorName='Ministry of Health'
              GROUP BY y.YearValue,w.WorkforceTypeName,s.WorkforceCount
              HAVING s.WorkforceCount <> SUM(n.WorkforceCount)
                 OR ABS(MAX(s.SaudiPercent) - SUM(CASE WHEN dn.NationalityName='Saudi' THEN n.WorkforceCount ELSE 0 END) * 100.0 / SUM(n.WorkforceCount)) > 0.15
            ) x
        """).fetchone()[0]
        rows = cur.execute("SELECT COUNT(DISTINCT CONCAT(y.YearValue, '|', w.WorkforceTypeName)) FROM analytics.FactWorkforceSector s JOIN analytics.DimYear y ON y.YearKey=s.YearKey JOIN analytics.DimSector sec ON sec.SectorKey=s.SectorKey JOIN analytics.DimWorkforceType w ON w.WorkforceTypeKey=s.WorkforceTypeKey WHERE sec.SectorName='Ministry of Health'").fetchone()[0]
        add("fy006_fy008_reconciliation", reconciliation == 0 and rows == 24, {"passed": 24 - reconciliation, "expected": 24, "failures": reconciliation})

    # Compare table counts and additive totals to the validated SQLite reference.
    sql_conn = sqlite3.connect(SQLITE)
    with pyodbc.connect(CONNECTION, timeout=10) as server:
        cur = server.cursor()
        for sql_table, sqlite_table in [("FactCapacity", "fact_capacity"), ("FactActivity", "fact_activity"), ("FactWorkforceSector", "fact_workforce_sector"), ("FactWorkforceNationality", "fact_workforce_nationality")]:
            sql_count = cur.execute(f"SELECT COUNT(*) FROM analytics.{sql_table}").fetchone()[0]
            sqlite_count = sql_conn.execute(f"SELECT COUNT(*) FROM {sqlite_table}").fetchone()[0]
            add(f"{sql_table}_sqlite_baseline_count", sql_count == sqlite_count, {"sqlserver": sql_count, "sqlite": sqlite_count})
    sql_conn.close()

    status = "PASS" if all(c["status"] == "PASS" for c in checks) else "FAIL"
    result = {"status": status, "server": "localhost", "database": "SaudiHealthcareAnalytics", "checks": checks}
    OUTPUT.write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")
    print(f"SQL SERVER VALIDATION: {status}")
    for check in checks:
        print(f"{check['status']}: {check['name']} - {check['details']}")
    raise SystemExit(0 if status == "PASS" else 1)


if __name__ == "__main__":
    main()
