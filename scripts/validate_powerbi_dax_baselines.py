from decimal import Decimal
from pathlib import Path
import json
import pyodbc

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "validation" / "powerbi_dax_sql_baselines.json"
CONNECTION = (
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=localhost;"
    "DATABASE=SaudiHealthcareAnalytics;Trusted_Connection=yes;"
    "Encrypt=no;TrustServerCertificate=yes"
)

QUERIES = {
    "KPI-01 Hospitals": """
        SELECT y.YearValue, SUM(f.Value) Value
        FROM analytics.FactCapacity f JOIN analytics.DimYear y ON y.YearKey=f.YearKey
        WHERE f.CapacityMeasure='Hospitals' GROUP BY y.YearValue ORDER BY y.YearValue""",
    "KPI-02 Beds": """
        SELECT y.YearValue, SUM(f.Value) Value
        FROM analytics.FactCapacity f JOIN analytics.DimYear y ON y.YearKey=f.YearKey
        WHERE f.CapacityMeasure='Beds' GROUP BY y.YearValue ORDER BY y.YearValue""",
    "KPI-03 Beds per 10,000 Population": """
        SELECT y.YearValue, MAX(f.Value) Value
        FROM analytics.FactCapacity f JOIN analytics.DimYear y ON y.YearKey=f.YearKey
        WHERE f.CapacityMeasure='Beds per 10,000 population'
        GROUP BY y.YearValue HAVING COUNT(*)=1 ORDER BY y.YearValue""",
    "KPI-04 Workforce Count": """
        SELECT y.YearValue, SUM(f.WorkforceCount) Value
        FROM analytics.FactWorkforceSector f JOIN analytics.DimYear y ON y.YearKey=f.YearKey
        GROUP BY y.YearValue ORDER BY y.YearValue""",
    "KPI-05 Saudi Workforce Share": """
        SELECT y.YearValue,
          SUM(CASE WHEN n.NationalityName='Saudi' THEN f.WorkforceCount ELSE 0 END)*1.0
          / NULLIF(SUM(f.WorkforceCount),0) Value
        FROM analytics.FactWorkforceNationality f
        JOIN analytics.DimYear y ON y.YearKey=f.YearKey
        JOIN analytics.DimNationality n ON n.NationalityKey=f.NationalityKey
        WHERE f.Scope='MOH Total' GROUP BY y.YearValue ORDER BY y.YearValue""",
    "KPI-06 Encounters": """
        SELECT y.YearValue, SUM(f.Value) Value
        FROM analytics.FactActivity f JOIN analytics.DimYear y ON y.YearKey=f.YearKey
        WHERE f.ActivityMeasure='Encounters' GROUP BY y.YearValue ORDER BY y.YearValue""",
    "KPI-07 Encounters per Person": """
        SELECT y.YearValue, MAX(f.Value) Value
        FROM analytics.FactActivity f JOIN analytics.DimYear y ON y.YearKey=f.YearKey
        WHERE f.ActivityMeasure='Encounters per person per year'
        GROUP BY y.YearValue HAVING COUNT(*)=1 ORDER BY y.YearValue""",
    "KPI-08 Admissions": """
        SELECT y.YearValue, SUM(f.Value) Value
        FROM analytics.FactActivity f JOIN analytics.DimYear y ON y.YearKey=f.YearKey
        WHERE f.ActivityMeasure='Inpatients / Admissions' GROUP BY y.YearValue ORDER BY y.YearValue""",
    "KPI-09 Admissions per 100 Persons": """
        SELECT y.YearValue, MAX(f.Value) Value
        FROM analytics.FactActivity f JOIN analytics.DimYear y ON y.YearKey=f.YearKey
        WHERE f.ActivityMeasure='Admissions per 100 persons'
        GROUP BY y.YearValue HAVING COUNT(*)=1 ORDER BY y.YearValue""",
    "KPI-10 Red Crescent Cases": """
        SELECT y.YearValue, SUM(f.Value) Value
        FROM analytics.FactActivity f JOIN analytics.DimYear y ON y.YearKey=f.YearKey
        WHERE f.ActivityMeasure='Cases offered first aid / transported to hospitals'
        GROUP BY y.YearValue ORDER BY y.YearValue""",
    "KPI-11 Cases per Center": """
        SELECT y.YearValue, SUM(a.Value)/NULLIF(MAX(c.Centers),0) Value
        FROM analytics.FactActivity a
        JOIN analytics.DimYear y ON y.YearKey=a.YearKey
        CROSS APPLY (
          SELECT SUM(fc.Value) Centers FROM analytics.FactCapacity fc
          WHERE fc.YearKey=a.YearKey AND fc.CapacityMeasure='First Aid Centers'
        ) c
        WHERE a.ActivityMeasure='Cases offered first aid / transported to hospitals'
        GROUP BY y.YearValue ORDER BY y.YearValue""",
    "KPI-12 Cases per Ambulance": """
        SELECT y.YearValue, SUM(a.Value)/NULLIF(MAX(c.Ambulances),0) Value
        FROM analytics.FactActivity a
        JOIN analytics.DimYear y ON y.YearKey=a.YearKey
        CROSS APPLY (
          SELECT SUM(fc.Value) Ambulances FROM analytics.FactCapacity fc
          WHERE fc.YearKey=a.YearKey AND fc.CapacityMeasure='Ambulances'
        ) c
        WHERE a.ActivityMeasure='Cases offered first aid / transported to hospitals'
        GROUP BY y.YearValue ORDER BY y.YearValue""",
}


def json_value(value):
    if isinstance(value, Decimal):
        return float(value)
    return value


def main():
    results = []
    failures = []
    with pyodbc.connect(CONNECTION, timeout=10) as conn:
        cursor = conn.cursor()
        for name, query in QUERIES.items():
            rows = [
                {"Year": int(row[0]), "Value": json_value(row[1])}
                for row in cursor.execute(query).fetchall()
            ]
            passed = len(rows) == 4 and all(row["Value"] is not None for row in rows)
            if not passed:
                failures.append(name)
            results.append({
                "kpi": name,
                "sql_baseline": rows,
                "dax_expected": rows,
                "dax_runtime_result": None,
                "difference": None,
                "status": "SQL_BASELINE_PASS_RUNTIME_PENDING" if passed else "FAIL",
            })

        regression = cursor.execute("""
            SELECT f.WorkforceCount
            FROM analytics.FactWorkforceNationality f
            JOIN analytics.DimYear y ON y.YearKey=f.YearKey
            JOIN analytics.DimWorkforceType w ON w.WorkforceTypeKey=f.WorkforceTypeKey
            JOIN analytics.DimNationality n ON n.NationalityKey=f.NationalityKey
            WHERE y.YearValue=2021 AND f.Scope='MOH Total'
              AND w.WorkforceTypeName='Pharmacists' AND n.NationalityName='Non-Saudi'
        """).fetchone()[0]

        reconciliation_rows = cursor.execute("""
            SELECT COUNT(*) FROM analytics.FactWorkforceSector s
            JOIN analytics.DimSector sec ON sec.SectorKey=s.SectorKey
            WHERE sec.SectorName='Ministry of Health'
        """).fetchone()[0]
        reconciliation_failures = cursor.execute("""
            SELECT COUNT(*) FROM (
              SELECT s.YearKey,s.WorkforceTypeKey
              FROM analytics.FactWorkforceSector s
              JOIN analytics.DimSector sec ON sec.SectorKey=s.SectorKey
              JOIN analytics.FactWorkforceNationality n
                ON n.YearKey=s.YearKey AND n.WorkforceTypeKey=s.WorkforceTypeKey
               AND n.Scope='MOH Total'
              WHERE sec.SectorName='Ministry of Health'
              GROUP BY s.YearKey,s.WorkforceTypeKey,s.WorkforceCount
              HAVING s.WorkforceCount<>SUM(n.WorkforceCount)
            ) x
        """).fetchone()[0]

        riyadh = cursor.execute("""
            SELECT SUM(a.Value), SUM(c.Value), SUM(b.Value)
            FROM analytics.DimYear y
            JOIN analytics.DimGeography g ON g.GeographyName='Riyadh'
            LEFT JOIN analytics.FactActivity a ON a.YearKey=y.YearKey AND a.GeographyKey=g.GeographyKey
              AND a.ActivityMeasure='Cases offered first aid / transported to hospitals'
            LEFT JOIN analytics.FactCapacity c ON c.YearKey=y.YearKey AND c.GeographyKey=g.GeographyKey
              AND c.CapacityMeasure='First Aid Centers'
            LEFT JOIN analytics.FactCapacity b ON b.YearKey=y.YearKey AND b.GeographyKey=g.GeographyKey
              AND b.CapacityMeasure='Ambulances'
            WHERE y.YearValue=2024
        """).fetchone()

    overall_pass = not failures and regression == 131 and reconciliation_rows == 24 and reconciliation_failures == 0
    output = {
        "status": "PASS" if overall_pass else "FAIL",
        "server": "localhost",
        "database": "SaudiHealthcareAnalytics",
        "kpis_tested": len(results),
        "runtime_status": "PENDING",
        "results": results,
        "sample_contexts": {
            "Riyadh_2024": {
                "Cases": json_value(riyadh[0]),
                "FirstAidCenters": json_value(riyadh[1]),
                "Ambulances": json_value(riyadh[2]),
                "CasesPerCenter": float(riyadh[0] / riyadh[1]) if riyadh[1] else None,
                "CasesPerAmbulance": float(riyadh[0] / riyadh[2]) if riyadh[2] else None,
            }
        },
        "known_regression": regression,
        "fy006_fy008": {
            "rows": reconciliation_rows,
            "passed": reconciliation_rows - reconciliation_failures,
            "failures": reconciliation_failures,
        },
    }
    OUTPUT.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(f"SQL DAX BASELINES: {output['status']} ({len(results)} KPIs)")
    print(f"Regression: {regression}; FY006/FY008: {reconciliation_rows - reconciliation_failures}/{reconciliation_rows}")
    raise SystemExit(0 if overall_pass else 1)


if __name__ == "__main__":
    main()
