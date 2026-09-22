CREATE TABLE analytics.FactCapacity (
    CapacityKey bigint IDENTITY(1,1) NOT NULL CONSTRAINT PK_FactCapacity PRIMARY KEY,
    YearKey int NOT NULL CONSTRAINT FK_FactCapacity_Year REFERENCES analytics.DimYear(YearKey),
    GeographyKey int NOT NULL CONSTRAINT FK_FactCapacity_Geography REFERENCES analytics.DimGeography(GeographyKey),
    SectorKey int NOT NULL CONSTRAINT FK_FactCapacity_Sector REFERENCES analytics.DimSector(SectorKey),
    CapacityMeasure varchar(100) NOT NULL,
    Value decimal(28,15) NOT NULL,
    Unit varchar(100) NOT NULL,
    SourceGroup varchar(20) NOT NULL,
    SourceWorkbook nvarchar(255) NOT NULL,
    SourceSheet nvarchar(255) NOT NULL,
    CONSTRAINT UQ_FactCapacity_Grain UNIQUE (YearKey, GeographyKey, SectorKey, CapacityMeasure)
);

CREATE TABLE analytics.FactActivity (
    ActivityKey bigint IDENTITY(1,1) NOT NULL CONSTRAINT PK_FactActivity PRIMARY KEY,
    YearKey int NOT NULL CONSTRAINT FK_FactActivity_Year REFERENCES analytics.DimYear(YearKey),
    GeographyKey int NOT NULL CONSTRAINT FK_FactActivity_Geography REFERENCES analytics.DimGeography(GeographyKey),
    SectorKey int NOT NULL CONSTRAINT FK_FactActivity_Sector REFERENCES analytics.DimSector(SectorKey),
    ActivityMeasure varchar(150) NOT NULL,
    Value decimal(28,15) NOT NULL,
    Unit varchar(100) NOT NULL,
    SourceGroup varchar(20) NOT NULL,
    SourceWorkbook nvarchar(255) NOT NULL,
    SourceSheet nvarchar(255) NOT NULL,
    CONSTRAINT UQ_FactActivity_Grain UNIQUE (YearKey, GeographyKey, SectorKey, ActivityMeasure)
);

CREATE TABLE analytics.FactWorkforceSector (
    WorkforceSectorKey bigint IDENTITY(1,1) NOT NULL CONSTRAINT PK_FactWorkforceSector PRIMARY KEY,
    YearKey int NOT NULL CONSTRAINT FK_FactWorkforceSector_Year REFERENCES analytics.DimYear(YearKey),
    GeographyKey int NOT NULL CONSTRAINT FK_FactWorkforceSector_Geography REFERENCES analytics.DimGeography(GeographyKey),
    SectorKey int NOT NULL CONSTRAINT FK_FactWorkforceSector_Sector REFERENCES analytics.DimSector(SectorKey),
    WorkforceTypeKey int NOT NULL CONSTRAINT FK_FactWorkforceSector_Type REFERENCES analytics.DimWorkforceType(WorkforceTypeKey),
    WorkforceCount int NOT NULL,
    SaudiPercent decimal(5,1) NULL,
    Unit varchar(30) NOT NULL,
    SourceGroup varchar(20) NOT NULL,
    SourceWorkbook nvarchar(255) NOT NULL,
    SourceSheet nvarchar(255) NOT NULL,
    CONSTRAINT UQ_FactWorkforceSector_Grain UNIQUE (YearKey, GeographyKey, SectorKey, WorkforceTypeKey)
);

CREATE TABLE analytics.FactWorkforceNationality (
    WorkforceNationalityKey bigint IDENTITY(1,1) NOT NULL CONSTRAINT PK_FactWorkforceNationality PRIMARY KEY,
    YearKey int NOT NULL CONSTRAINT FK_FactWorkforceNationality_Year REFERENCES analytics.DimYear(YearKey),
    GeographyKey int NOT NULL CONSTRAINT FK_FactWorkforceNationality_Geography REFERENCES analytics.DimGeography(GeographyKey),
    Scope varchar(100) NOT NULL CONSTRAINT CK_FactWorkforceNationality_Scope CHECK (Scope IN ('MOH Total', 'MOH Primary Health Care Centers')),
    WorkforceTypeKey int NOT NULL CONSTRAINT FK_FactWorkforceNationality_Type REFERENCES analytics.DimWorkforceType(WorkforceTypeKey),
    NationalityKey int NOT NULL CONSTRAINT FK_FactWorkforceNationality_Nationality REFERENCES analytics.DimNationality(NationalityKey),
    WorkforceCount int NOT NULL,
    Unit varchar(30) NOT NULL,
    SourceGroup varchar(20) NOT NULL,
    SourceWorkbook nvarchar(255) NOT NULL,
    SourceSheet nvarchar(255) NOT NULL,
    CONSTRAINT UQ_FactWorkforceNationality_Grain UNIQUE (YearKey, GeographyKey, Scope, WorkforceTypeKey, NationalityKey)
);
