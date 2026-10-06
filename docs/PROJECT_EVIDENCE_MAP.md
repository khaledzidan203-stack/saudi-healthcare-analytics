# Project Evidence Map

This map connects the repository's main public claims to the files that define or validate them. The README and presentation graphics are navigation layers, not evidence by themselves.

| Project claim | Primary evidence |
|---|---|
| Source is official Saudi Ministry of Health Statistical Yearbooks, 2021–2024 | [`data/README.md`](../data/README.md), [`CANONICAL_DATA_CONTRACT.md`](architecture/CANONICAL_DATA_CONTRACT.md) |
| Core analytical domains are capacity, activity, workforce, and Red Crescent regional resources/activity | [`CANONICAL_DATA_CONTRACT.md`](architecture/CANONICAL_DATA_CONTRACT.md), [`KPI_CONTRACT.md`](kpi/KPI_CONTRACT.md) |
| Core geography is National + Administrative Region | [`CANONICAL_DATA_CONTRACT.md`](architecture/CANONICAL_DATA_CONTRACT.md) |
| Canonical layer contains four facts and five dimensions | [`CANONICAL_DATA_CONTRACT.md`](architecture/CANONICAL_DATA_CONTRACT.md), [`data/processed/canonical/`](../data/processed/canonical/) |
| SQL Server is the final reporting engine; SQLite is a reference baseline | [`SQL_STAR_SCHEMA.md`](architecture/SQL_STAR_SCHEMA.md), [`sql/README.md`](../sql/README.md) |
| SQL fact row counts are 132 / 84 / 72 / 96 and canonical reconciliation passed | [`sqlserver_validation.json`](../outputs/validation/sqlserver_validation.json), [`FINAL_RELEASE_VALIDATION.md`](validation/FINAL_RELEASE_VALIDATION.md) |
| Broken foreign keys and duplicate fact grains are zero | [`sqlserver_validation.json`](../outputs/validation/sqlserver_validation.json) |
| FY006 ↔ FY008 workforce reconciliation is 24/24 PASS | [`workforce_cross_source_reconciliation.csv`](../outputs/validation/workforce_cross_source_reconciliation.csv) |
| Semantic model contains 10 total tables, 15 measures and 14 active M:1 single-direction relationships | [`POWER_BI_SEMANTIC_MODEL.md`](powerbi/POWER_BI_SEMANTIC_MODEL.md), saved TMDL under [`powerbi/`](../powerbi/) |
| Original 12 governed DAX measures passed runtime reconciliation | [`powerbi_dax_runtime_validation.json`](../outputs/validation/powerbi_dax_runtime_validation.json), [`DAX_MEASURE_DICTIONARY.md`](powerbi/DAX_MEASURE_DICTIONARY.md) |
| Three later Red Crescent measures are current model additions but not part of the earlier 12-measure runtime suite | [`DAX_MEASURE_DICTIONARY.md`](powerbi/DAX_MEASURE_DICTIONARY.md), [`FINAL_RELEASE_VALIDATION.md`](validation/FINAL_RELEASE_VALIDATION.md) |
| Report contains 7 pages and 121 uniquely identified visuals | [`final_release_validation.json`](../outputs/validation/final_release_validation.json), [`screenshots/`](../screenshots/) |
| INDEX is opening page and Executive Overview is saved at Year = 2024 | [`final_release_validation.json`](../outputs/validation/final_release_validation.json) |
| Release checks include PBIR/JSON parsing, navigation, screenshot integrity, local links, source preservation and credential-pattern scans | [`scripts/validate_release.py`](../scripts/validate_release.py), [`final_release_validation.json`](../outputs/validation/final_release_validation.json) |
| No patient-level data is included | [`data/README.md`](../data/README.md), [`FINAL_RELEASE_VALIDATION.md`](validation/FINAL_RELEASE_VALIDATION.md) |
| Current source-scope interpretation supersedes the historical all-PENDING source-review artifact | [`SOURCE_GOVERNANCE_STATUS.md`](SOURCE_GOVERNANCE_STATUS.md) |

## Evidence precedence

For the current release, use this precedence when historical planning files, presentation material and implemented artifacts differ:

1. governed canonical data and explicit contracts for business meaning and grain;
2. SQL DDL/load/validation evidence for the analytical database;
3. saved PBIP/PBIR/TMDL source for implemented Power BI structure;
4. final release validation and recorded reconciliation artifacts for tested status;
5. README, case study and visual assets for explanation and navigation only.

Presentation graphics must not introduce new metrics, grains, source scopes or validation claims.
