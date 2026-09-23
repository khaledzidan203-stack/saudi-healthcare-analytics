# Data provenance and reproduction

Provider: Saudi Ministry of Health. Acquire workbooks from the [official Statistical Yearbook portal](https://www.moh.gov.sa/en/ministry/statistics/book/pages/default.aspx). The 2021–2024 inputs are public yearbook workbooks. Provider terms apply; the MIT license does not relicense the data.

## Included data

`processed/canonical/` contains nine small governed CSV tables with workbook/sheet lineage. These are aggregate public statistics, not patient-level records. Counts and grains are defined in the [canonical contract](../docs/architecture/CANONICAL_DATA_CONTRACT.md). Discovery and validation outputs document selection and exclusions.

## Local raw placement

Place the eight unchanged workbooks in root `row_data/` with these names (extract workbooks if distributed in archives):

- `Statistical-Yearbook-2021-Chapter-I-Health-Indicators.xlsx`
- `statistical-yearbook-2021-chapter-II-health-resources.xlsx`
- `statistical-yearbook-2021-chapter-IV-health-activities.xlsx`
- `2022-Chapter-I-Health-Indicators.xlsx`
- `2022-Chapter-II-Health-Resources.xlsx`
- `2022-Chapter-IV-Health-Activities.xlsx`
- `Statistical-Yearbook-2023.xlsx`
- `Statistical-Yearbook-2024.xlsx`

Raw files are excluded to avoid duplicating provider downloads. Preserve source sheets and cached formula values. Provider versions can change: compare the [workbook inventory](../outputs/tables/workbook_sheet_inventory.csv) and [approval register](../outputs/validation/FINAL_SOURCE_APPROVAL.csv) before accepting replacement inputs. No automatic downloader or pinned provider archive is implemented.

## Reproduction paths

For SQL/report reproduction, use included canonical CSVs and the [SQL guide](../sql/README.md).

For full Excel reproduction in a separate working copy, run `src/discovery/` scripts 01 through 06 in order, then:

```powershell
python src/transformation/09_build_canonical_dataset.py
python scripts/validate_phase3_canonical.py
python scripts/verify_repository_baseline.py
```

These scripts regenerate outputs and some documentation. FY-005, FY-006, FY-008, FY-010, FY-018, FY-020 and FY-023 form the core; FY-029 is excluded from comparable trends. National and Administrative Region remain distinct from Health Region/Cluster.

## Local database reference

`python scripts/build_sqlite_model.py` regenerates `processed/sqlite/healthcare_analytics.sqlite` for cross-engine checks. The release tree excludes generated databases, backups, raw workbooks and environments. A small public-data SQLite reference remains in pre-release Git history, which is preserved. Power BI uses SQL Server only.
