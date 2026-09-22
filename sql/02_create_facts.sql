CREATE TABLE IF NOT EXISTS fact_capacity (
    capacity_key INTEGER PRIMARY KEY,
    year_key INTEGER NOT NULL REFERENCES dim_year(year_key),
    geography_key INTEGER NOT NULL REFERENCES dim_geography(geography_key),
    sector_key INTEGER NOT NULL REFERENCES dim_sector(sector_key),
    capacity_measure TEXT NOT NULL,
    value REAL NOT NULL,
    unit TEXT NOT NULL,
    source_group TEXT NOT NULL,
    source_workbook TEXT NOT NULL,
    source_sheet TEXT NOT NULL,
    UNIQUE (year_key, geography_key, sector_key, capacity_measure)
);

CREATE TABLE IF NOT EXISTS fact_activity (
    activity_key INTEGER PRIMARY KEY,
    year_key INTEGER NOT NULL REFERENCES dim_year(year_key),
    geography_key INTEGER NOT NULL REFERENCES dim_geography(geography_key),
    sector_key INTEGER NOT NULL REFERENCES dim_sector(sector_key),
    activity_measure TEXT NOT NULL,
    value REAL NOT NULL,
    unit TEXT NOT NULL,
    source_group TEXT NOT NULL,
    source_workbook TEXT NOT NULL,
    source_sheet TEXT NOT NULL,
    UNIQUE (year_key, geography_key, sector_key, activity_measure)
);

CREATE TABLE IF NOT EXISTS fact_workforce_sector (
    workforce_sector_key INTEGER PRIMARY KEY,
    year_key INTEGER NOT NULL REFERENCES dim_year(year_key),
    geography_key INTEGER NOT NULL REFERENCES dim_geography(geography_key),
    sector_key INTEGER NOT NULL REFERENCES dim_sector(sector_key),
    workforce_type_key INTEGER NOT NULL REFERENCES dim_workforce_type(workforce_type_key),
    workforce_count REAL NOT NULL,
    saudi_percent REAL,
    unit TEXT NOT NULL,
    source_group TEXT NOT NULL,
    source_workbook TEXT NOT NULL,
    source_sheet TEXT NOT NULL,
    UNIQUE (year_key, geography_key, sector_key, workforce_type_key)
);

CREATE TABLE IF NOT EXISTS fact_workforce_nationality (
    workforce_nationality_key INTEGER PRIMARY KEY,
    year_key INTEGER NOT NULL REFERENCES dim_year(year_key),
    geography_key INTEGER NOT NULL REFERENCES dim_geography(geography_key),
    scope TEXT NOT NULL CHECK (scope IN ('MOH Total', 'MOH Primary Health Care Centers')),
    workforce_type_key INTEGER NOT NULL REFERENCES dim_workforce_type(workforce_type_key),
    nationality_key INTEGER NOT NULL REFERENCES dim_nationality(nationality_key),
    workforce_count REAL NOT NULL,
    unit TEXT NOT NULL,
    source_group TEXT NOT NULL,
    source_workbook TEXT NOT NULL,
    source_sheet TEXT NOT NULL,
    UNIQUE (year_key, geography_key, scope, workforce_type_key, nationality_key)
);
