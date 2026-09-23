# Governed DAX Measure Dictionary

The IDs below map in order to the 12 approved rows in
`docs/kpi/KPI_CONTRACT.md`; assigning IDs does not change their definitions.
All measures are owned by `_Measures`. The 12 rows below describe the original
runtime-validated KPI checkpoint. The final report has 15 measures after the
approved Red Crescent count/display additions described at the end.

Full four-year SQL baselines are stored in
`outputs/validation/powerbi_dax_sql_baselines.json`.

| ID | Measure | Business definition | Source / numerator / denominator | Grain, filters and time logic | Format, totals and blanks | SQL baseline / status |
|---|---|---|---|---|---|---|
| KPI-01 | Hospitals | Reported hospital count | FactCapacity.Value; no denominator | Year × National × Sector; CapacityMeasure = Hospitals; no time transformation | `#,0`; additive across sectors; missing remains blank | 2021: 497; 2024: 516; SQL ↔ DAX PASS |
| KPI-02 | Beds | Reported bed count | FactCapacity.Value; no denominator | Year × National × Sector; CapacityMeasure = Beds | `#,0`; additive across sectors; missing remains blank | 2021: 77,224; 2024: 82,721; SQL ↔ DAX PASS |
| KPI-03 | Beds per 10,000 Population | Official published rate | Official FactCapacity.Value row; no recalculation | Year × National; CapacityMeasure = Beds per 10,000 population | `0.00`; non-additive, SELECTEDVALUE; multi-value totals blank | 2021: 22.6; 2024: 23.433525173171432; SQL ↔ DAX PASS |
| KPI-04 | Workforce Count | Reported workforce persons | FactWorkforceSector.WorkforceCount; no denominator | Year × National × Sector × WorkforceType | `#,0`; additive across compatible detail; missing remains blank | 2021: 485,688; 2024: 681,914; SQL ↔ DAX PASS |
| KPI-05 | Saudi Workforce Share | Saudi / (Saudi + Non-Saudi) | FactWorkforceNationality counts; numerator Saudi, denominator both nationalities | Year × WorkforceType; Scope = MOH Total; nationality slicer removed for stable composition; ratio of totals | `0.0%`; DIVIDE; zero denominator returns blank | 2021: 70.3435%; 2024: 74.2870%; SQL ↔ DAX PASS |
| KPI-06 | Encounters | Reported encounters | FactActivity.Value; no denominator | Year × National × Sector; ActivityMeasure = Encounters | `#,0`; additive across sectors; missing remains blank | 2021: 146,627,997.222; 2024: 170,231,304; SQL ↔ DAX PASS |
| KPI-07 | Encounters per Person | Official published encounter rate | Official FactActivity.Value row; no recalculation | Year × National; ActivityMeasure = Encounters per person per year | `0.00`; non-additive, SELECTEDVALUE; multi-value totals blank | 2021: 4.3; 2024: 4.8; SQL ↔ DAX PASS |
| KPI-08 | Admissions | Reported inpatient/admission count | FactActivity.Value; no denominator | Year × National × Sector; ActivityMeasure = Inpatients / Admissions | `#,0`; additive across sectors; missing remains blank | 2021: 3,100,752; 2024: 3,630,334; SQL ↔ DAX PASS |
| KPI-09 | Admissions per 100 Persons | Official published admission rate | Official FactActivity.Value row; no recalculation | Year × National; non-additive, SELECTEDVALUE; multi-value totals blank | `0.00`; non-additive, SELECTEDVALUE; multi-value totals blank | 2021: 9.1; 2024: 10.3; SQL ↔ DAX PASS |
| KPI-10 | Red Crescent Cases | Reported cases offered first aid / transported | FactActivity.Value; no denominator | Year × Administrative Region; governed activity label | `#,0`; additive across regions; missing remains blank | 2021: 458,449; 2024: 566,288; SQL ↔ DAX PASS |
| KPI-11 | Cases per Center | Total Red Crescent cases / total first-aid centers | FactActivity cases / FactCapacity centers | Year × Administrative Region or national aggregate; ratio of totals | `#,0.0`; DIVIDE; zero denominator returns blank | 2021: 902.458661; 2024: 1,097.457364; SQL ↔ DAX PASS |
| KPI-12 | Cases per Ambulance | Total Red Crescent cases / total ambulances | FactActivity cases / FactCapacity ambulances | Year × Administrative Region or national aggregate; ratio of totals | `#,0.0`; DIVIDE; zero denominator returns blank | 2021: 326.530626; 2024: 538.296577; SQL ↔ DAX PASS |

## DAX expressions

```DAX
Hospitals =
CALCULATE(
    SUM('analytics FactCapacity'[Value]),
    KEEPFILTERS('analytics FactCapacity'[CapacityMeasure] = "Hospitals")
)

Beds =
CALCULATE(
    SUM('analytics FactCapacity'[Value]),
    KEEPFILTERS('analytics FactCapacity'[CapacityMeasure] = "Beds")
)

Beds per 10,000 Population =
CALCULATE(
    SELECTEDVALUE('analytics FactCapacity'[Value]),
    KEEPFILTERS('analytics FactCapacity'[CapacityMeasure] = "Beds per 10,000 population")
)

Workforce Count =
SUM('analytics FactWorkforceSector'[WorkforceCount])

Saudi Workforce Share =
VAR SaudiCount =
    CALCULATE(
        CALCULATE(
            SUM('analytics FactWorkforceNationality'[WorkforceCount]),
            'analytics DimNationality'[NationalityName] = "Saudi"
        ),
        'analytics FactWorkforceNationality'[Scope] = "MOH Total",
        REMOVEFILTERS('analytics DimNationality')
    )
VAR TotalCount =
    CALCULATE(
        SUM('analytics FactWorkforceNationality'[WorkforceCount]),
        'analytics FactWorkforceNationality'[Scope] = "MOH Total",
        REMOVEFILTERS('analytics DimNationality')
    )
RETURN
    DIVIDE(SaudiCount, TotalCount)

Encounters =
CALCULATE(
    SUM('analytics FactActivity'[Value]),
    KEEPFILTERS('analytics FactActivity'[ActivityMeasure] = "Encounters")
)

Encounters per Person =
CALCULATE(
    SELECTEDVALUE('analytics FactActivity'[Value]),
    KEEPFILTERS('analytics FactActivity'[ActivityMeasure] = "Encounters per person per year")
)

Admissions =
CALCULATE(
    SUM('analytics FactActivity'[Value]),
    KEEPFILTERS('analytics FactActivity'[ActivityMeasure] = "Inpatients / Admissions")
)

Admissions per 100 Persons =
CALCULATE(
    SELECTEDVALUE('analytics FactActivity'[Value]),
    KEEPFILTERS('analytics FactActivity'[ActivityMeasure] = "Admissions per 100 persons")
)

Red Crescent Cases =
CALCULATE(
    SUM('analytics FactActivity'[Value]),
    KEEPFILTERS('analytics FactActivity'[ActivityMeasure] = "Cases offered first aid / transported to hospitals")
)

Cases per Center =
DIVIDE(
    CALCULATE(
        SUM('analytics FactActivity'[Value]),
        KEEPFILTERS('analytics FactActivity'[ActivityMeasure] = "Cases offered first aid / transported to hospitals")
    ),
    CALCULATE(
        SUM('analytics FactCapacity'[Value]),
        KEEPFILTERS('analytics FactCapacity'[CapacityMeasure] = "First Aid Centers")
    )
)

Cases per Ambulance =
DIVIDE(
    CALCULATE(
        SUM('analytics FactActivity'[Value]),
        KEEPFILTERS('analytics FactActivity'[ActivityMeasure] = "Cases offered first aid / transported to hospitals")
    ),
    CALCULATE(
        SUM('analytics FactCapacity'[Value]),
        KEEPFILTERS('analytics FactCapacity'[CapacityMeasure] = "Ambulances")
    )
)
```

## Classification

- Approved KPI measures: 12
- Original checkpoint supporting / utility measures: 0
- Year-comparison measures: 0; the approved 12-row contract does not request a
  growth KPI, so no additional YoY definition was invented.

## Final report additions — checkpoint `cae3706`

| Measure | Definition | Grain / behavior | Evidence |
|---|---|---|---|
| First Aid Centers | SUM of FactCapacity.Value filtered to First Aid Centers | Year × Administrative Region; count, compatible regional totals; missing stays blank | Current TMDL, canonical FY-018 rows and approved Red Crescent page |
| Ambulances | SUM of FactCapacity.Value filtered to Ambulances | Year × Administrative Region; count, compatible regional totals; missing stays blank | Current TMDL, canonical FY-018 rows and approved Red Crescent page |
| Ambulances Card | FORMAT([Ambulances], "#,0") | Text display helper, not a numeric analytical KPI; FORMAT blank renders empty text | Current TMDL and approved card |

Final inventory: 15 measures, including the original 12. The original runtime
JSON does not test these three additions; their report checkpoint and current
source-preservation checks are separate evidence. Annual capacity snapshots
should not be summed across years for headline reporting.
