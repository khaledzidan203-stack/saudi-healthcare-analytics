CREATE TABLE IF NOT EXISTS dim_year (
    year_key INTEGER PRIMARY KEY,
    year_value INTEGER NOT NULL UNIQUE CHECK (year_value BETWEEN 2021 AND 2024)
);

CREATE TABLE IF NOT EXISTS dim_geography (
    geography_key INTEGER PRIMARY KEY,
    geography_type TEXT NOT NULL CHECK (geography_type IN ('National', 'Administrative Region')),
    geography_name TEXT NOT NULL,
    UNIQUE (geography_type, geography_name)
);

CREATE TABLE IF NOT EXISTS dim_sector (
    sector_key INTEGER PRIMARY KEY,
    sector_name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS dim_workforce_type (
    workforce_type_key INTEGER PRIMARY KEY,
    workforce_type_name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS dim_nationality (
    nationality_key INTEGER PRIMARY KEY,
    nationality_name TEXT NOT NULL UNIQUE CHECK (nationality_name IN ('Saudi', 'Non-Saudi'))
);
