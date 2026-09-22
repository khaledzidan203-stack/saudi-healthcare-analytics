from pathlib import Path
import csv
import json
import sqlite3

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "data" / "processed" / "canonical"
SQL = ROOT / "sql"
DB_DIR = ROOT / "data" / "processed" / "sqlite"
DB_DIR.mkdir(parents=True, exist_ok=True)
DB = DB_DIR / "healthcare_analytics.sqlite"


def read_csv(name):
    with (CANONICAL / name).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def run_sql(conn, name):
    conn.executescript((SQL / name).read_text(encoding="utf-8"))


def insert_dimensions(conn):
    years = read_csv("dim_year.csv")
    geographies = read_csv("dim_geography.csv")
    sectors = read_csv("dim_sector.csv")
    workforce = read_csv("dim_workforce_type.csv")
    nationalities = read_csv("dim_nationality.csv")
    conn.executemany("INSERT INTO dim_year(year_key, year_value) VALUES (?, ?)", [(int(r["Year"]), int(r["Year"])) for r in years])
    conn.executemany("INSERT INTO dim_geography(geography_key, geography_type, geography_name) VALUES (?, ?, ?)", [(i + 1, r["GeographyType"], r["Geography"]) for i, r in enumerate(geographies)])
    conn.executemany("INSERT INTO dim_sector(sector_key, sector_name) VALUES (?, ?)", [(i + 1, r["Sector"]) for i, r in enumerate(sectors)])
    conn.executemany("INSERT INTO dim_workforce_type(workforce_type_key, workforce_type_name) VALUES (?, ?)", [(i + 1, r["WorkforceType"]) for i, r in enumerate(workforce)])
    conn.executemany("INSERT INTO dim_nationality(nationality_key, nationality_name) VALUES (?, ?)", [(i + 1, r["Nationality"]) for i, r in enumerate(nationalities)])


def key_maps(conn):
    return {
        "year": {r[1]: r[0] for r in conn.execute("SELECT year_value, year_key FROM dim_year")},
        "geo": {(r[1], r[2]): r[0] for r in conn.execute("SELECT geography_key, geography_type, geography_name FROM dim_geography")},
        "sector": {r[1]: r[0] for r in conn.execute("SELECT sector_key, sector_name FROM dim_sector")},
        "workforce": {r[1]: r[0] for r in conn.execute("SELECT workforce_type_key, workforce_type_name FROM dim_workforce_type")},
        "nationality": {r[1]: r[0] for r in conn.execute("SELECT nationality_key, nationality_name FROM dim_nationality")},
    }


def load_facts(conn):
    m = key_maps(conn)
    for r in read_csv("fact_capacity.csv"):
        conn.execute("INSERT INTO fact_capacity(year_key, geography_key, sector_key, capacity_measure, value, unit, source_group, source_workbook, source_sheet) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (m["year"][int(r["Year"])], m["geo"][(r["GeographyType"], r["Geography"])], m["sector"][r["Sector"]], r["CapacityMeasure"], float(r["Value"]), r["Unit"], r["SourceGroup"], r["SourceWorkbook"], r["SourceSheet"]))
    for r in read_csv("fact_activity.csv"):
        conn.execute("INSERT INTO fact_activity(year_key, geography_key, sector_key, activity_measure, value, unit, source_group, source_workbook, source_sheet) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (m["year"][int(r["Year"])], m["geo"][(r["GeographyType"], r["Geography"])], m["sector"][r["Sector"]], r["ActivityMeasure"], float(r["Value"]), r["Unit"], r["SourceGroup"], r["SourceWorkbook"], r["SourceSheet"]))
    for r in read_csv("fact_workforce_sector.csv"):
        conn.execute("INSERT INTO fact_workforce_sector(year_key, geography_key, sector_key, workforce_type_key, workforce_count, saudi_percent, unit, source_group, source_workbook, source_sheet) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (m["year"][int(r["Year"])], m["geo"][(r["GeographyType"], r["Geography"])], m["sector"][r["Sector"]], m["workforce"][r["WorkforceType"]], float(r["WorkforceCount"]), float(r["SaudiPercent"]) if r["SaudiPercent"] else None, r["Unit"], r["SourceGroup"], r["SourceWorkbook"], r["SourceSheet"]))
    for r in read_csv("fact_workforce_nationality.csv"):
        conn.execute("INSERT INTO fact_workforce_nationality(year_key, geography_key, scope, workforce_type_key, nationality_key, workforce_count, unit, source_group, source_workbook, source_sheet) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (m["year"][int(r["Year"])], m["geo"][(r["GeographyType"], r["Geography"])], r["Scope"], m["workforce"][r["WorkforceType"]], m["nationality"][r["Nationality"]], float(r["WorkforceCount"]), r["Unit"], r["SourceGroup"], r["SourceWorkbook"], r["SourceSheet"]))


def main():
    if DB.exists():
        DB.unlink()
    conn = sqlite3.connect(DB)
    try:
        run_sql(conn, "00_create_database_or_schema.sql")
        run_sql(conn, "01_create_dimensions.sql")
        run_sql(conn, "02_create_facts.sql")
        insert_dimensions(conn)
        load_facts(conn)
        run_sql(conn, "05_constraints_indexes.sql")
        conn.commit()
    finally:
        conn.close()
    print(DB)


if __name__ == "__main__":
    main()
