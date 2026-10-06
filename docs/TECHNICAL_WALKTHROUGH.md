# Technical Walkthrough

This walkthrough provides a compact path through the implemented Saudi Healthcare Analytics system.

## 60–90 second walkthrough

1. **Start with the source boundary**
   - Official Saudi Ministry of Health Statistical Yearbooks, 2021–2024.
   - Aggregate public statistics only; no patient-level data.

2. **Show discovery before modeling**
   - Python inventories workbooks and sheets, profiles structure, and separates yearbook-specific layouts before any analytical model is built.

3. **Show the grain-first canonical layer**
   - Nine governed canonical tables: four facts and five dimensions.
   - Capacity, activity, workforce-sector, and workforce-nationality remain separate fact grains.
   - National and Administrative Region are approved geography concepts; Health Region and Health Cluster are not silently equated.

4. **Show the SQL analytical layer**
   - SQL Server is the reporting engine using the `analytics` schema.
   - Surrogate keys, business-grain uniqueness, foreign-key validation, and canonical reconciliation protect the star schema.
   - SQLite is only a reproducible cross-engine reference, not the report source.

5. **Show the semantic model**
   - 10 tables total: nine SQL business tables plus disconnected `_Measures`.
   - 14 active M:1 single-direction relationships.
   - 15 current measures.
   - Auto Date/Time disabled; annual grain is preserved.

6. **Show KPI governance**
   - Additive counts and published non-additive rates are handled differently.
   - Saudi Workforce Share and Red Crescent resource ratios use governed ratio-of-totals logic.
   - Annual workforce snapshots are not summed across years.

7. **Show analytical delivery**
   - INDEX → Executive Overview → Capacity → Activity → Workforce & Nationalization → Red Crescent Regional Performance → Methodology & Validation.
   - The current PBIR release contains 7 pages and 121 saved visuals.

8. **Close with validation**
   - Canonical ↔ SQL Server reconciliation PASS.
   - FY006 ↔ FY008 workforce reconciliation: 24/24 PASS.
   - Original 12 governed DAX measures: 12/12 runtime PASS.
   - Current structural release audit verifies the 15-measure model, relationships, screenshots, links, source preservation, and publication hygiene.

## Key interpretation boundary

This is descriptive healthcare-system analytics based on published aggregate statistics. It does not establish patient outcomes, causality, service quality, or Red Crescent response-time performance.

## Useful entry points

- [README](../README.md)
- [Case study](CASE_STUDY.md)
- [Project evidence map](PROJECT_EVIDENCE_MAP.md)
- [Canonical data contract](architecture/CANONICAL_DATA_CONTRACT.md)
- [KPI contract](kpi/KPI_CONTRACT.md)
- [Semantic model](powerbi/POWER_BI_SEMANTIC_MODEL.md)
- [Final release validation](validation/FINAL_RELEASE_VALIDATION.md)
