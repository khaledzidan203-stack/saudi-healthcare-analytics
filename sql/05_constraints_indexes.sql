CREATE INDEX IF NOT EXISTS ix_capacity_year_geo ON fact_capacity(year_key, geography_key);
CREATE INDEX IF NOT EXISTS ix_activity_year_geo ON fact_activity(year_key, geography_key);
CREATE INDEX IF NOT EXISTS ix_workforce_sector_year_type ON fact_workforce_sector(year_key, workforce_type_key);
CREATE INDEX IF NOT EXISTS ix_workforce_nationality_year_type ON fact_workforce_nationality(year_key, workforce_type_key);
CREATE INDEX IF NOT EXISTS ix_workforce_nationality_scope ON fact_workforce_nationality(scope, nationality_key);
