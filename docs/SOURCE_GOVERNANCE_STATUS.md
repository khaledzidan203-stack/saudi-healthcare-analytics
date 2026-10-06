# Source Governance Status

## Current release interpretation

The implemented 2021–2024 analytical release uses official Saudi Ministry of Health Statistical Yearbook sources and a governed subset of source families defined by the canonical contract and validated analytical outputs.

Core source families used by the current analytical model:

- FY-005 — Hospitals / Beds / population-adjusted capacity rates
- FY-006 — Health workforce by sector
- FY-008 — MOH workforce by nationality
- FY-010 — Primary Health Care Center workforce scope
- FY-018 — Saudi Red Crescent first-aid centers and ambulances by Administrative Region
- FY-020 — Healthcare encounters and official encounter rates
- FY-023 — Inpatients / admissions and official admission rates

FY-029 Blood Bank is excluded from the comparable multi-year core because the available definitions change materially across years.

## Historical review artifact

`outputs/validation/FINAL_SOURCE_APPROVAL.csv` is retained as an earlier manual-review artifact from the discovery/contract phase. Its rows remain marked `PENDING` and must **not** be interpreted as the current release-status register.

The current implemented source scope is evidenced by:

- `docs/architecture/CANONICAL_DATA_CONTRACT.md`
- `data/processed/canonical/`
- `outputs/validation/source_lineage.csv`
- `outputs/validation/sqlserver_validation.json`
- `docs/validation/FINAL_RELEASE_VALIDATION.md`

The historical file is preserved rather than silently rewritten so that the project history remains auditable.

## Source replacement rule

Provider workbooks are not pinned to a permanent provider archive in this repository. If a Ministry of Health workbook is replaced or revised upstream, compare its workbook/sheet structure and source lineage before accepting it as an equivalent input. A future source revision requires revalidation of canonical outputs and dependent analytical evidence.
