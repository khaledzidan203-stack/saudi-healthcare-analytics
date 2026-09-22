# Phase 1 — Automated Data Discovery Summary

## Project

Saudi Healthcare Capacity & Performance Analytics 2021–2024

## Discovery Scope

This phase inspects the official source workbooks without cleaning, reshaping, joining, or modifying source data.

## Inventory

- Workbooks discovered: **8**
- Worksheets profiled: **644**
- Sheets with region clues: **402**
- Sheets with year clues: **621**
- Sheets with total/subtotal clues: **516**

## Workbook Inventory

- `2022-Chapter-I-Health-Indicators.xlsx`: 13 sheets
- `2022-Chapter-II-Health-Resources.xlsx`: 46 sheets
- `2022-Chapter-IV-Health-Activities.xlsx`: 74 sheets
- `Statistical-Yearbook-2021-Chapter-I-Health-Indicators.xlsx`: 12 sheets
- `statistical-yearbook-2021-chapter-II-health-resources.xlsx`: 46 sheets
- `statistical-yearbook-2021-chapter-IV-health-activities.xlsx`: 76 sheets
- `Statistical-Yearbook-2023.xlsx`: 179 sheets
- `Statistical-Yearbook-2024.xlsx`: 198 sheets

## Detected Year Candidates

- 2022: 341 sampled occurrences
- 2021: 282 sampled occurrences
- 2023: 112 sampled occurrences
- 2024: 47 sampled occurrences

## Most Frequent Region-like Source Values

- `Riyadh`: 329
- `الرياض`: 317
- `Eastern`: 316
- `المدينة المنورة`: 311
- `القصيم`: 283
- `الشرقية`: 280
- `عسير`: 242
- `جازان`: 242
- `تبوك`: 239
- `نجران`: 236
- `حائل`: 235
- `Jazan`: 235
- `Najran`: 233
- `الباحة`: 229
- `الجوف`: 229
- `الحدود الشمالية`: 209
- `Al-Bahah`: 172
- `Al-Jouf`: 171
- `Northern Borders`: 97
- `Makkah`: 96
- `Madinah`: 74
- `مكة المكرمة`: 56
- `Qassim`: 40
- `تجمع الرياض الصحي الأول`: 31
- `تجمع الرياض الصحي الثاني`: 31
- `تجمع الرياض الصحي الثالث`: 31
- `تجمع المدينة المنورة الصحي`: 31
- `تجمع القصيم الصحي`: 31
- `تجمع الشرقية الصحي`: 31
- `تجمع تبوك الصحي`: 31
- `تجمع حائل الصحي`: 31
- `تجمع جازان الصحي`: 31
- `تجمع نجران الصحي`: 31
- `Madinah Health Cluster`: 31
- `Qassim Health Cluster`: 31
- `Hail`: 31
- `Hail Health Cluster`: 31
- `Jazan Health Cluster`: 31
- `Najran Health Cluster`: 31
- `تجمع الباحة الصحي`: 30

## Early Structural / Data Quality Risks

- TOTAL_OR_SUBTOTAL_ROWS_POSSIBLE: 516
- MULTIPLE_BLANK_ROWS_IN_SAMPLE: 225
- SOURCE_OR_FOOTNOTE_TEXT_POSSIBLE: 140
- VERY_SMALL_SHEET: 4
- SINGLE_COLUMN_OR_EMPTY_STRUCTURE: 4

## Important Interpretation Rule

Header rows, data-start rows, region values, and analytical clues in this phase are **candidates only**. They require manual validation before cleaning, joining, aggregation, or KPI implementation.

## Source Modification

**NO source workbook was modified.**
