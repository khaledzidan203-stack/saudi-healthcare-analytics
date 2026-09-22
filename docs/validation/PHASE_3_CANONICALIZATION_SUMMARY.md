# Phase 3 — Canonicalization Summary

## Outputs

- `fact_capacity`: **132 rows**, 4 years, source groups: FY-005 | FY-018
- `fact_activity`: **84 rows**, 4 years, source groups: FY-018 | FY-020 | FY-023
- `fact_workforce_sector`: **72 rows**, 4 years, source groups: FY-006
- `fact_workforce_nationality`: **95 rows**, 4 years, source groups: FY-008 | FY-010

## Validation

- Validation checks: **51**
- Failed checks: **35**
- Review checks: **0**
- Workforce cross-source reconciliations: **24**
- Workforce reconciliation failures: **1**

## Source Protection

**Raw Excel workbooks were not modified.**

## Next Gate

Do not load the canonical facts into SQL until `validation_reconciliation.csv` and `workforce_cross_source_reconciliation.csv` are reviewed.
