# Power BI DAX Validation

## Status

Historical runtime checkpoint `99b573f`: the 12-measure/one-page inventory
below describes that checkpoint only. The final report has seven pages and
15 measures. See [current release validation](FINAL_RELEASE_VALIDATION.md).

**RUNTIME PASS — 12/12 MEASURES**

Tabular Editor 2.28.0 successfully loaded the TMDL model with 10 tables, 12
measures, and 14 relationships. The active PBIP runtime validated all 12
measures against the approved SQL baselines.

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

## Runtime validation

The active PBIP was confirmed at
`D:\Saudi_Healthcare_Analytics_Raw_Data\powerbi\SaudiHealthcareAnalytics.pbip`.
All 12 measures executed successfully and reconciled to SQL for 2021–2024.
The known 2021 MOH Total / Pharmacists / Non-Saudi regression returned 131.
Runtime structure passed: 14 relationships, 0 M:M, 0 bidirectional, 0
inactive, 0 `_Measures` relationships, 10 tables, 1 page, and 0 visuals.

`Cases per Center` and `Cases per Ambulance` were corrected from the failing
single-line multi-`VAR` serialization to direct ratio-of-totals
`DIVIDE(CALCULATE(...), CALCULATE(...))` expressions. The direct expressions
execute successfully in the live model. SQL baselines are rounded to six
decimals; runtime comparison allows the corresponding absolute rounding
envelope.

The repository static validator's placeholder and relationship-property checks
are stale artifacts: the current TMDL stores the valid defaults/runtime
metadata rather than explicit relationship property lines, and the placeholder
check assumes an older line layout. The live model confirms the required
structure and no semantic-model discrepancy was found.

Machine-readable result:
`outputs/validation/powerbi_dax_runtime_validation.json`.
