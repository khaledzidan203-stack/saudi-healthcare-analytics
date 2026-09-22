# Saudi Healthcare Capacity & Performance Analytics 2021–2024
## Data Model Contract V1 — Draft for Manual Approval

> Status: **DRAFT — source validation pending**

## Business Problem

Understand how healthcare capacity, workforce, and service activity evolved across Saudi Arabia from 2021 to 2024, and identify geographic differences that warrant deeper capacity and performance review.

## Portfolio Scope

The project intentionally uses a focused subset of the official Saudi Ministry of Health Statistical Yearbooks rather than all available worksheets.

Core domains:

1. Population context
2. Healthcare capacity
3. Healthcare workforce
4. Healthcare activity
5. Geographic comparison
6. Multi-year trend analysis

## Selected Source Groups for Validation

- `FY-005` — Population | Capacity — المستشفيات والأسرة بالقطاعات الصحية بالمملكة حسب الجهة ومعدل الأسرة لكل عشرة آلاف من السكان في الأعوام الخمسة الأخيرة
- `FY-006` — Workforce — Health Manpower in KSA Health Sectors in the Last Five Years
- `FY-008` — Workforce — Health Manpower in MOH by Nationality in the Last Five Years
- `FY-010` — Capacity | Workforce — Health Manpower in Primary Health Care Centers, MOH, in the last Five Years
- `FY-018` — Capacity — First Aid Centers and Ambulances of the Saudi Red Crescent Authority by Administrative Region, 2021G.
- `FY-020` — Population | Activity — زيارات المراجعين للقطاعات الصحية بالمملكة ومتوسط عدد الزيارات لكل فرد من السكان في الأعوام الخمسة الأخيرة
- `FY-023` — Capacity | Activity — Inpatients in Health Sectors Hospitals, KSA in the last Five Years
- `FY-029` — Activity — أنشطة بنوك الدم بوزارة الصحة حسب المنطقة الصحية عام 2021م.

## Geography Contract

The following concepts must remain distinct unless an official mapping proves equivalence:

- National
- Health Region
- Administrative Region
- Health Cluster

A Health Cluster must not automatically be treated as a Health Region merely because it contains the same city or regional name.

## Preliminary Star Schema

```text
                  Dim_Year
                     |
                  Dim_Geography
                     |
   -----------------------------------------
   |                 |                     |
Fact_Capacity   Fact_Workforce       Fact_Activity
   |                 |                     |
Dim_Facility    Dim_WorkforceType    Dim_ActivityType

Optional / separate:
Fact_PopulationIndicators
```

This model is not approved until source grain validation is completed.

## Grain Contract Template

Every approved fact table must document:

```text
One row = Year × Geography × Business Measure Dimension
```

Actual grain may differ by domain and must follow the official source table structure.

## KPI Families — Candidate Only

### Capacity
- Hospitals
- Beds
- PHC / healthcare facilities where supported
- Ambulances / emergency infrastructure where supported

### Workforce
- Physicians
- Nurses
- Pharmacists
- Allied healthcare workforce where supported

### Activity
- Visits
- Inpatients / admissions
- Selected healthcare activities

### Derived Rates
- Population-normalized capacity/workforce ratios only when numerator and denominator geography and year are compatible
- Resource-to-activity ratios only when fact grains are analytically compatible

## KPI Contract Rule

Before implementation every KPI must define:

Business Definition → Numerator → Denominator → Grain → Population → Filters → Time Logic → Unit → Total Behavior → Validation Baseline

## Validation Gate

Cleaning and canonicalization may begin only after each selected source group has been reviewed for:

- business meaning
- grain
- geography
- units
- totals/subtotals
- footnotes/source notes
- final KEEP / EXCLUDE decision

## Current Status

**Manual source validation required.**
