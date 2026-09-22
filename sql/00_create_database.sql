-- SaudiHealthcareAnalytics is created and owned outside this repository.
-- Run this file while connected to that database.
IF NOT EXISTS (SELECT 1 FROM sys.schemas WHERE name = N'analytics')
    EXEC(N'CREATE SCHEMA analytics AUTHORIZATION dbo');
