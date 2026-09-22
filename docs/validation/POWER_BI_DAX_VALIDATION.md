# Power BI DAX Validation

## Status

**STATIC PASS — RUNTIME PENDING**

Tabular Editor 2.28.0 successfully loaded the TMDL model with 10 tables, 12
measures, and 14 relationships. The repository static validator also passed.

## Static semantic checks

- `_Measures` exists with a hidden integer placeholder.
- Its calculated partition is `FILTER(ROW("Placeholder", 0), FALSE())`, so it
  contains zero business rows by definition.
- `_Measures` has zero relationships.
- All 12 explicit measures belong to `_Measures`.
- Dimensions and facts own zero explicit measures.
- Relationships remain 14 active single-direction M:1 relationships.
- Tables: 10; pages: 1; visuals: 0.
- Auto Date/Time remains disabled; no Date table was fabricated.
- All nine SQL Import partitions remain on `localhost` /
  `SaudiHealthcareAnalytics`.

Machine-readable result:
`outputs/validation/powerbi_dax_static_validation.json`.

## SQL baselines

Read-only SQL Server validation passed for all 12 approved KPI measures across
2021–2024. Riyadh 2024 regional ratio contexts were also captured. The known
2021 MOH Total / Pharmacists / Non-Saudi regression remains 131, and FY006 ↔
FY008 remains 24/24 PASS.

Machine-readable result:
`outputs/validation/powerbi_dax_sql_baselines.json`.

## Runtime limitation

The PBIP was not active after the external TMDL update, so the new measures
could not be queried through a live local Analysis Services endpoint. Runtime
results, differences, and final SQL ↔ DAX value reconciliation remain pending.

To complete runtime validation, reopen
`powerbi/SaudiHealthcareAnalytics.pbip` in Power BI Desktop, allow the model to
load, and expose the local model endpoint. No validation page or visual is
required.
