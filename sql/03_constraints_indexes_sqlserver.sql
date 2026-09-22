CREATE INDEX IX_FactCapacity_YearGeography ON analytics.FactCapacity(YearKey, GeographyKey);
CREATE INDEX IX_FactActivity_YearGeography ON analytics.FactActivity(YearKey, GeographyKey);
CREATE INDEX IX_FactWorkforceSector_YearType ON analytics.FactWorkforceSector(YearKey, WorkforceTypeKey);
CREATE INDEX IX_FactWorkforceNationality_YearType ON analytics.FactWorkforceNationality(YearKey, WorkforceTypeKey);
CREATE INDEX IX_FactWorkforceNationality_ScopeNationality ON analytics.FactWorkforceNationality(Scope, NationalityKey);
