# Power BI Semantic Model — Hardened Year-Grain Baseline

## Model contract

The semantic model contains five dimensions and four facts sourced from SQL
Server `localhost`, database `SaudiHealthcareAnalytics`, schema `analytics`.
The approved annual grain is preserved; no Date table or artificial dates are
introduced.

## Relationships

All 14 relationships resolve as active, many-to-one from
fact to dimension, with single-direction filtering. There are no fact-to-fact,
many-to-many, bidirectional, inactive, or ambiguous paths.

## Visibility and summarization

Surrogate keys, foreign keys, identity keys, and source-lineage columns are
hidden. YearValue and non-additive fields use `summarizeBy: none`. Workforce
counts retain Sum as additive base facts. The generic Capacity/Activity Value
columns are non-summarizable because each contains both additive counts and
published non-additive rates; future governed measures must apply the KPI
contract by measure label.

## Time behavior

This is a year-grain model. DimYear is not marked as a Date Table because no
genuine Date column exists. Future year-over-year logic must use explicit
year-based DAX rather than fabricated daily time intelligence.

## Governed measure layer

The model now contains exactly one dedicated `_Measures` table. It has a
hidden zero-row placeholder, no relationships, and owns all 15 current
measures: the original 12 KPIs plus two Red Crescent count measures and one
display helper. Nine SQL business tables plus `_Measures` make ten tables.

Original 12-measure runtime reconciliation passed at `99b573f`. Later report
additions are documented in the DAX dictionary. Default relationship
properties can be omitted by Desktop serialization; the final release audit
checks resolved defaults and preservation against `a4f47c5`.

See [final release validation](../validation/FINAL_RELEASE_VALIDATION.md) for
current checks and historical evidence boundaries.
