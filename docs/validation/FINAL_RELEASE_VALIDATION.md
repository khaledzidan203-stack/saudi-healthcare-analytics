# Final release validation — 2026-09-23

Analytical baseline: `a4f47c5` — `feat(powerbi): finalize methodology validation page`.
This record separates current publication checks from earlier runtime tests and owner-approved visual QA. No SQL, canonical pipeline, DAX or report-page rebuild was performed for publication.

## Structural validation

Run `python scripts/validate_release.py`; results are in [release validation JSON](../../outputs/validation/final_release_validation.json).

The release has seven pages, 121 uniquely identified visuals and six HOME links to INDEX. Methodology retains 43 visuals and 29 short text rows. PBIR/project JSON parses; navigation destinations exist. INDEX is the opening page (`850ce1b1e37e9e00e59e`), and the Executive Overview Year slicer retains the approved 2024 selection.

The auditor compares all existing Power BI source against `a4f47c5`, allowing only those two saved-state changes. It checks screenshot PNG integrity, original SHA-256 hashes, local Markdown links, Python syntax and release exclusions. This is not a Power BI Desktop rendering test or complete JSON-schema validation.

## Semantic validation

Current source inventory: nine SQL business tables plus disconnected `_Measures` = **10 total tables**; **15 measures**; **14 active M:1 single-direction relationships**. No many-to-many, bidirectional, inactive or fact-to-fact relationships. Default TMDL relationship properties omitted by Desktop serialization are resolved as many/one, oneDirection and active; source matches the approved baseline. The star has one edge per dimension/fact pair, with no alternate filter paths. Auto Date/Time is disabled.

The original 12 measure expressions are unchanged from runtime-approved `99b573f`. [Runtime evidence](../../outputs/validation/powerbi_dax_runtime_validation.json) records 12/12 PASS across the annual contexts, including the workforce regression of 131. The later `First Aid Centers`, `Ambulances` and `Ambulances Card` additions belong to the approved Red Crescent checkpoint `cae3706`; they are not covered by that earlier 12-measure JSON. No fresh live DAX test of all 15 is claimed.

Earlier validators assume one page and 12 measures. Their historical inventories and previously documented placeholder/property-layout failures do not describe current report defects. The Methodology screenshot's “9 tables” label describes the nine business tables; the disconnected measure table must be counted separately.

## Data reconciliation

- [SQL Server evidence](../../outputs/validation/sqlserver_validation.json): fact counts 132 / 84 / 72 / 96; broken FK, duplicate grains and required-measure nulls zero; joined row counts preserved; canonical reconciliation PASS.
- [Workforce reconciliation](../../outputs/validation/workforce_cross_source_reconciliation.csv): FY006 ↔ FY008 24/24 PASS.
- `scripts/verify_repository_baseline.py`: current canonical grain, completeness, year coverage and 2021 MOH Total / Pharmacists / Non-Saudi = 131 checks.
- Release audit independently aggregates current canonical 2024 headline values and compares them with recorded SQL values. Saudi Workforce Share is **MOH Total**, not all-sector workforce.

SQL evidence is retained from validated checkpoints; release preparation did not reload the database or regenerate canonical data. The baseline script also requires a clean Git tree, so its final clean-tree check is run after committing the release.

## Power BI manual QA

Owner approval in the release brief confirms the six report pages plus INDEX. The Methodology checkpoint records Manual Visual QA APPROVED, persistence TRUE PASS, 43/43 visuals, 29/29 short rows and HOME → INDEX PASS. Its source is preserved in `a4f47c5`; prior page checkpoints are `93d864e`, `b06e591` and `cae3706`.

All eight supplied screenshots were visually inspected during packaging. Seven match the approved pages and show no visible private information. Their bytes are unchanged after renaming. The generic September 21 capture is an unrelated LinkedIn editing screen, not this report; it is excluded and retained locally. Screenshot review confirms captured appearance, not every interactive filter state. No new Desktop interaction QA is claimed.

## Publication audit

The pre-release history scan inspected 317 Git blobs for token/private-key/nonempty credential-assignment patterns, including XML inside the validation workbook, with zero matches. Current publishable files are rescanned by the release validator. Blank `.env.example` entries are placeholders; SQL uses Windows trusted authentication. No credential values are printed. Pattern scans are bounded checks, not a guarantee against every possible secret encoding.

Excluded: official `row_data/`, `.venv-1/`, `.vscode/`, Python caches, Power BI `.pbi/` local state, redundant PBIX/database/backups, local test DAXQueries and the unrelated screenshot. The small validation workbook is retained as source-review evidence, not a raw workbook dump. No release payload exceeds 10 MiB.

The 159,744-byte generated SQLite reference is removed from the current release tree while its local file is preserved. A historical public-data copy remains in Git history; no destructive history rewrite is performed. No raw source workbook or environment is tracked. Aggregate canonical CSVs and source lineage remain public for reproducibility; no patient data is included.

No remote existed before publication and the target repository did not exist at the initial check. GitHub authentication was verified for the requested owner. Branch migration from `master` to `main` is permitted only after preserving the analytical history and completing local validation. Remote visibility, contents, README/gallery responses and commit identity are checked after pushing; this document does not substitute for those remote checks.

## Reproduction and limitations

See [data policy](../../data/README.md), [SQL guide](../../sql/README.md), [Power BI guide](../../powerbi/README.md) and [KPI contracts](../kpi/KPI_CONTRACT.md). Empty local `config/`, `notebooks/` and `tests/` scaffold directories are not implemented pipelines or test suites. Available validators are used instead. A fresh clone needs local SQL setup and a Desktop refresh because caches are excluded.

Dependency smoke checks: NumPy, openpyxl and pyodbc imported successfully.
Pandas import in the existing system Python failed because Windows Application
Control blocks its installed optional PyArrow `_compute` DLL; retrying outside
the sandbox did not resolve it. No policy or analytical code was changed.
Python syntax and the standard-library release audit passed. Reproducing the
pandas-based discovery stages requires a working local dependency environment;
this release does not claim a fresh full-pipeline execution.

Original project code/documentation use MIT; MOH source data retains provider terms. Source revisions may require manual revalidation. Counts are descriptive, snapshots are not additive across years, national rates are not sector rates, and emergency capacity/volume is not response time or service quality.
