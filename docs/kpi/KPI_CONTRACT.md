# KPI Contract

All measures use the canonical facts at their declared grain. Counts are
additive only across compatible dimensions. Published rates are non-additive
and are shown from their official source rows; they are never summed.

| KPI | Numerator / denominator | Grain and filters | Aggregation / null rule | Source |
|---|---|---|---|---|
| Hospitals | reported hospital count | Year × National × Sector | Sum across sectors; missing remains null | fact_capacity |
| Beds | reported beds | Year × National × Sector | Sum across sectors; missing remains null | fact_capacity |
| Beds per 10,000 population | official published rate | Year × National | Non-additive; use official row | fact_capacity |
| Workforce count | reported persons | Year × Geography × Sector × WorkforceType | Sum only across compatible detail | fact_workforce_sector |
| Saudi workforce share | Saudi / (Saudi + Non-Saudi) × 100 | Year × WorkforceType, MOH Total | Ratio of totals; published FY-006 percent is validation reference | both workforce facts |
| Encounters | reported encounters | Year × National × Sector | Sum sector counts | fact_activity |
| Encounters per person | official rate | Year × National | Non-additive; use official row | fact_activity |
| Admissions | reported inpatients/admissions | Year × National × Sector | Sum sector counts | fact_activity |
| Admissions per 100 persons | official rate | Year × National | Non-additive; use official row | fact_activity |
| Red Crescent cases | reported cases | Year × Administrative Region | Sum regions; compatible geography only | fact_activity |
| Cases per center | total cases / total centers | Year × Administrative Region or national total | Ratio of totals, never average row ratios | fact_activity + fact_capacity |
| Cases per ambulance | total cases / total ambulances | Year × Administrative Region or national total | Ratio of totals, never average row ratios | fact_activity + fact_capacity |

Growth KPIs use `(current year - prior year) / prior year`; if the prior year
is null or zero, the result is null. No KPI claims causality.
