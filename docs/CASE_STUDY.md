# Project Case Study

## Saudi Healthcare Analytics 2021–2024

This project turns official Saudi Ministry of Health statistical yearbooks into a governed analytical model, SQL Server layer, source-controlled Power BI semantic model, and validated seven-page report.

## 1. Problem

Official annual healthcare workbooks contain multiple reporting concepts, changing structures, published rates, national totals, regional detail, sector splits, workforce snapshots, and source-specific definitions. Combining them without explicit contracts creates risks such as duplicate historical observations, incompatible geography joins, double counting, invalid rate aggregation, and inconsistent totals.

The implementation therefore starts with four controls:

1. define source and geography boundaries before modeling;
2. establish fact grain and additive behavior before aggregation;
3. preserve published rates separately from additive counts;
4. validate each analytical layer against independent evidence.

## 2. Source and scope

- Provider: Saudi Ministry of Health Statistical Yearbooks.
- Reporting period: 2021–2024.
- Data type: official aggregate public statistics; no patient-level records.
- Core domains: healthcare capacity, healthcare activity, workforce, and Saudi Red Crescent regional resources/activity.
- Approved geography concepts: National and Administrative Region.
- Health Region and Health Cluster remain separate concepts and are not automatically mapped into the core model.

The core source families implemented in the final analytical model are FY-005, FY-006, FY-008, FY-010, FY-018, FY-020, and FY-023. FY-029 Blood Bank is excluded from the comparable multi-year core because definitions change materially across years.

## 3. End-to-end architecture

```text
Official MOH yearbooks
        ↓
Python discovery and structural profiling
        ↓
Canonical contracts and transformation
        ↓
4 fact tables + 5 dimensions
        ↓
SQL Server analytics schema
        ↓
Power BI import semantic model (TMDL)
        ↓
15 current DAX measures
        ↓
7-page PBIR report
        ↓
Reconciliation + release audit
```

The canonical layer contains nine governed CSV tables: four facts and five dimensions.

## 4. Grain and aggregation governance

The model keeps the major analytical facts separate:

- `FactCapacity` — Year × Geography Type/Name × Sector × Capacity Measure.
- `FactActivity` — Year × Geography Type/Name × Sector × Activity Measure.
- `FactWorkforceSector` — Year × National Geography × Sector × Workforce Type.
- `FactWorkforceNationality` — Year × National Geography × Scope × Workforce Type × Nationality.

Counts are additive only across compatible dimensions. Published rates such as beds per 10,000 population, encounters per person, and admissions per 100 persons remain non-additive official values and are not summed.

Annual workforce snapshots are not summed across years.

## 5. SQL analytical layer

The final reporting engine is SQL Server using database `SaudiHealthcareAnalytics`, schema `analytics`.

The SQL model contains five dimensions and four fact tables with surrogate keys, retained lineage, business-grain uniqueness, and validation for broken foreign keys, duplicate grain, required measure nulls, and canonical reconciliation.

SQLite remains a reproducible historical/reference baseline for cross-engine checks; it is not the Power BI reporting source.

## 6. Power BI semantic model

The saved semantic model contains:

- nine SQL-backed business tables;
- one disconnected `_Measures` table;
- ten semantic tables total;
- 14 active many-to-one, single-direction relationships;
- no many-to-many, bidirectional, inactive, or fact-to-fact relationships;
- 15 current measures.

The model is annual-grain by design. Auto Date/Time is disabled and no artificial daily date table is introduced.

## 7. KPI governance

The governed KPI contract distinguishes additive counts, official published rates, and ratio-of-totals calculations.

Examples:

- Hospitals and Beds: additive compatible counts.
- Beds per 10,000 Population: official source rate, non-additive.
- Saudi Workforce Share: Saudi / (Saudi + Non-Saudi) over the governed `MOH Total` population.
- Cases per Center and Cases per Ambulance: ratio of totals, never average of row-level ratios.

Missing, blank, and zero are not treated as interchangeable.

## 8. Validation evidence

Validation is layered rather than represented by one generic pass/fail statement.

- Canonical ↔ SQL Server reconciliation: PASS.
- Broken foreign keys: 0.
- Duplicate fact grains: 0.
- FY006 ↔ FY008 workforce reconciliation: 24/24 PASS with zero count variance.
- Original governed DAX suite: 12/12 runtime PASS across annual contexts.
- Current release structure: 10 semantic tables, 15 measures, 14 relationships.
- Report structure: 7 pages and 121 uniquely identified visuals.
- Release audit: JSON/PBIR parsing, navigation, screenshot integrity, local links, source preservation, payload exclusions, and credential-pattern checks.

The three later Red Crescent report additions (`First Aid Centers`, `Ambulances`, and `Ambulances Card`) are part of the approved current model but are not represented as if they were included in the earlier 12-measure runtime suite.

## 9. Current analytical delivery

The report contains:

1. INDEX
2. Executive Overview
3. Healthcare Capacity
4. Healthcare Activity
5. Workforce & Nationalization
6. Red Crescent Regional Performance
7. Methodology & Validation

The default Executive Overview state is Year = 2024.

## 10. Interpretation boundaries

The project supports descriptive healthcare-system analytics, not patient outcomes or causal conclusions. Red Crescent case/resource volumes do not measure response time or service quality. National published rates are not sector rates. Source definitions and provider revisions can affect future reproduction and must be revalidated before accepting replacement workbooks.

## Evidence entry points

- [Project evidence map](PROJECT_EVIDENCE_MAP.md)
- [Canonical data contract](architecture/CANONICAL_DATA_CONTRACT.md)
- [SQL star schema](architecture/SQL_STAR_SCHEMA.md)
- [KPI contract](kpi/KPI_CONTRACT.md)
- [Power BI semantic model](powerbi/POWER_BI_SEMANTIC_MODEL.md)
- [Final release validation](validation/FINAL_RELEASE_VALIDATION.md)
