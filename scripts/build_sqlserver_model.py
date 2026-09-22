from pathlib import Path
import csv
import pyodbc

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "data" / "processed" / "canonical"
SQL = ROOT / "sql"
CONNECTION = "DRIVER={ODBC Driver 18 for SQL Server};SERVER=localhost;DATABASE=SaudiHealthcareAnalytics;Trusted_Connection=yes;Encrypt=no;TrustServerCertificate=yes"


def read_csv(name):
    with (CANONICAL / name).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def execute_file(cursor, name):
    cursor.execute((SQL / name).read_text(encoding="utf-8"))


def main():
    with pyodbc.connect(CONNECTION, timeout=10) as conn:
        cursor = conn.cursor()
        execute_file(cursor, "00_create_database.sql")
        execute_file(cursor, "01_create_dimensions_sqlserver.sql")
        execute_file(cursor, "02_create_facts_sqlserver.sql")

        cursor.fast_executemany = True
        cursor.executemany("INSERT INTO analytics.DimYear (YearValue) VALUES (?)", [(int(r["Year"]),) for r in read_csv("dim_year.csv")])
        cursor.executemany("INSERT INTO analytics.DimGeography (GeographyType, GeographyName) VALUES (?, ?)", [(r["GeographyType"], r["Geography"]) for r in read_csv("dim_geography.csv")])
        cursor.executemany("INSERT INTO analytics.DimSector (SectorName) VALUES (?)", [(r["Sector"],) for r in read_csv("dim_sector.csv")])
        cursor.executemany("INSERT INTO analytics.DimWorkforceType (WorkforceTypeName) VALUES (?)", [(r["WorkforceType"],) for r in read_csv("dim_workforce_type.csv")])
        cursor.executemany("INSERT INTO analytics.DimNationality (NationalityName) VALUES (?)", [(r["Nationality"],) for r in read_csv("dim_nationality.csv")])

        years = {r[0]: r[1] for r in cursor.execute("SELECT YearValue, YearKey FROM analytics.DimYear")}
        geos = {(r[0], r[1]): r[2] for r in cursor.execute("SELECT GeographyType, GeographyName, GeographyKey FROM analytics.DimGeography")}
        sectors = {r[0]: r[1] for r in cursor.execute("SELECT SectorName, SectorKey FROM analytics.DimSector")}
        workforce = {r[0]: r[1] for r in cursor.execute("SELECT WorkforceTypeName, WorkforceTypeKey FROM analytics.DimWorkforceType")}
        nationalities = {r[0]: r[1] for r in cursor.execute("SELECT NationalityName, NationalityKey FROM analytics.DimNationality")}

        capacity_sql = "INSERT INTO analytics.FactCapacity (YearKey, GeographyKey, SectorKey, CapacityMeasure, Value, Unit, SourceGroup, SourceWorkbook, SourceSheet) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
        cursor.executemany(capacity_sql, [(years[int(r["Year"])], geos[(r["GeographyType"], r["Geography"])], sectors[r["Sector"]], r["CapacityMeasure"], float(r["Value"]), r["Unit"], r["SourceGroup"], r["SourceWorkbook"], r["SourceSheet"]) for r in read_csv("fact_capacity.csv")])

        activity_sql = "INSERT INTO analytics.FactActivity (YearKey, GeographyKey, SectorKey, ActivityMeasure, Value, Unit, SourceGroup, SourceWorkbook, SourceSheet) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
        cursor.executemany(activity_sql, [(years[int(r["Year"])], geos[(r["GeographyType"], r["Geography"])], sectors[r["Sector"]], r["ActivityMeasure"], float(r["Value"]), r["Unit"], r["SourceGroup"], r["SourceWorkbook"], r["SourceSheet"]) for r in read_csv("fact_activity.csv")])

        sector_sql = "INSERT INTO analytics.FactWorkforceSector (YearKey, GeographyKey, SectorKey, WorkforceTypeKey, WorkforceCount, SaudiPercent, Unit, SourceGroup, SourceWorkbook, SourceSheet) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        cursor.executemany(sector_sql, [(years[int(r["Year"])], geos[(r["GeographyType"], r["Geography"])], sectors[r["Sector"]], workforce[r["WorkforceType"]], int(float(r["WorkforceCount"])), float(r["SaudiPercent"]) if r["SaudiPercent"] else None, r["Unit"], r["SourceGroup"], r["SourceWorkbook"], r["SourceSheet"]) for r in read_csv("fact_workforce_sector.csv")])

        nationality_sql = "INSERT INTO analytics.FactWorkforceNationality (YearKey, GeographyKey, Scope, WorkforceTypeKey, NationalityKey, WorkforceCount, Unit, SourceGroup, SourceWorkbook, SourceSheet) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        cursor.executemany(nationality_sql, [(years[int(r["Year"])], geos[(r["GeographyType"], r["Geography"])], r["Scope"], workforce[r["WorkforceType"]], nationalities[r["Nationality"]], int(float(r["WorkforceCount"])), r["Unit"], r["SourceGroup"], r["SourceWorkbook"], r["SourceSheet"]) for r in read_csv("fact_workforce_nationality.csv")])
        execute_file(cursor, "03_constraints_indexes_sqlserver.sql")
        conn.commit()
    print("SQL Server model loaded: SaudiHealthcareAnalytics.analytics")


if __name__ == "__main__":
    main()
