IF OBJECT_ID(N'analytics.FactWorkforceNationality', N'U') IS NOT NULL DROP TABLE analytics.FactWorkforceNationality;
IF OBJECT_ID(N'analytics.FactWorkforceSector', N'U') IS NOT NULL DROP TABLE analytics.FactWorkforceSector;
IF OBJECT_ID(N'analytics.FactActivity', N'U') IS NOT NULL DROP TABLE analytics.FactActivity;
IF OBJECT_ID(N'analytics.FactCapacity', N'U') IS NOT NULL DROP TABLE analytics.FactCapacity;
IF OBJECT_ID(N'analytics.DimNationality', N'U') IS NOT NULL DROP TABLE analytics.DimNationality;
IF OBJECT_ID(N'analytics.DimWorkforceType', N'U') IS NOT NULL DROP TABLE analytics.DimWorkforceType;
IF OBJECT_ID(N'analytics.DimSector', N'U') IS NOT NULL DROP TABLE analytics.DimSector;
IF OBJECT_ID(N'analytics.DimGeography', N'U') IS NOT NULL DROP TABLE analytics.DimGeography;
IF OBJECT_ID(N'analytics.DimYear', N'U') IS NOT NULL DROP TABLE analytics.DimYear;

CREATE TABLE analytics.DimYear (
    YearKey int IDENTITY(1,1) NOT NULL CONSTRAINT PK_DimYear PRIMARY KEY,
    YearValue smallint NOT NULL CONSTRAINT UQ_DimYear_YearValue UNIQUE,
    CONSTRAINT CK_DimYear_YearValue CHECK (YearValue BETWEEN 2021 AND 2024)
);

CREATE TABLE analytics.DimGeography (
    GeographyKey int IDENTITY(1,1) NOT NULL CONSTRAINT PK_DimGeography PRIMARY KEY,
    GeographyType varchar(40) NOT NULL,
    GeographyName nvarchar(100) NOT NULL,
    CONSTRAINT UQ_DimGeography_BusinessKey UNIQUE (GeographyType, GeographyName),
    CONSTRAINT CK_DimGeography_Type CHECK (GeographyType IN ('National', 'Administrative Region'))
);

CREATE TABLE analytics.DimSector (
    SectorKey int IDENTITY(1,1) NOT NULL CONSTRAINT PK_DimSector PRIMARY KEY,
    SectorName nvarchar(100) NOT NULL CONSTRAINT UQ_DimSector_SectorName UNIQUE
);

CREATE TABLE analytics.DimWorkforceType (
    WorkforceTypeKey int IDENTITY(1,1) NOT NULL CONSTRAINT PK_DimWorkforceType PRIMARY KEY,
    WorkforceTypeName nvarchar(100) NOT NULL CONSTRAINT UQ_DimWorkforceType_Name UNIQUE
);

CREATE TABLE analytics.DimNationality (
    NationalityKey int IDENTITY(1,1) NOT NULL CONSTRAINT PK_DimNationality PRIMARY KEY,
    NationalityName varchar(20) NOT NULL CONSTRAINT UQ_DimNationality_Name UNIQUE,
    CONSTRAINT CK_DimNationality_Name CHECK (NationalityName IN ('Saudi', 'Non-Saudi'))
);
