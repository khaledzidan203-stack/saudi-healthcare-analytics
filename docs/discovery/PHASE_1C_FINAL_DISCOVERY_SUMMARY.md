# Phase 1C — Final Discovery Summary

## Project

**Saudi Healthcare Capacity & Performance Analytics 2021–2024**

## Current Gate

Discovery only. No source cleaning, joining, aggregation, KPI calculation, or analytical conclusion has been performed.

## Discovery Results

- Source workbooks: **8**
- Source worksheets cataloged: **644**
- Exact four-year structural candidate groups: **38**
- Core Population/Capacity/Workforce/Activity candidates: **31**
- Groups appearing region-level in all four years: **2**
- Groups showing mixed Region/Cluster geography clues: **0**

## Manual Review Classes

- Class A: **2** groups
- Class B: **3** groups
- Class C: **26** groups

## Core Topic Candidates

- Activity: 7
- Capacity | Activity: 6
- Capacity: 5
- Workforce: 5
- Capacity | Workforce: 3
- Population: 2
- Population | Activity: 1
- Population | Capacity: 1
- Workforce | Activity: 1

## Preliminary Business Problem — Candidate

Saudi healthcare decision-makers need a consistent multi-year view of healthcare capacity, workforce, and service activity across geographic areas to understand how resource availability and healthcare activity changed between 2021 and 2024 and where regional differences merit deeper review.

This wording is **provisional** until the selected source tables, grain, geography, and KPI definitions are manually validated.

## Preliminary Analytical Domains

- Population context
- Healthcare facilities and bed capacity
- Healthcare workforce
- Healthcare service activity
- Regional trend comparison
- Resource-to-population ratios where officially supported
- Resource-to-activity ratios only where compatible grains exist

## Geography Contract Rule

`Health Region`, `Administrative Region`, and `Health Cluster` must remain separate concepts until the official source structure proves a valid mapping. They must not be joined merely because their names appear geographically related.

## Candidate Model — Not Yet Approved

```text
Dim_Year
Dim_Geography
Dim_Indicator / Measure
Dim_Facility / Workforce / Activity Type as required

Fact_HealthCapacity
Fact_Workforce
Fact_HealthActivity
Fact_PopulationOrIndicators
```

Final fact-table boundaries will follow confirmed source grain, not this preliminary design.

## Approval Gate Before Cleaning

For each selected comparison group confirm:

1. Same business meaning across 2021–2024.
2. Same or reconcilable grain.
3. Same geography concept.
4. Same units and denominator definitions.
5. Total/subtotal behavior.
6. Header/data boundaries.
7. Source notes affecting interpretation.

**No cleaning starts until this validation gate is completed.**
