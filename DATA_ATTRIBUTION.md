# Data Attribution and Usage Boundary

## Provider

Saudi Ministry of Health — Statistical Yearbook publications for 2021–2024.

Official source portal: https://www.moh.gov.sa/en/ministry/statistics/book/pages/default.aspx

## Repository scope

The repository contains project code, documentation, aggregate canonical datasets derived from public statistical yearbooks, validation outputs, Power BI project source, and report screenshots.

It does **not** contain patient-level records.

## Licensing boundary

The repository's `LICENSE` applies to original project code and documentation only.

Saudi Ministry of Health source data, provider-derived values, names, trademarks, and any third-party assets remain subject to their original provider terms. No ownership of Ministry data is claimed and the project license does not relicense provider data.

## Reproduction boundary

Raw yearbook workbooks are intentionally not redistributed in the current repository. Users reproducing the full Excel-to-canonical path should obtain the official source files directly from the Ministry of Health portal and revalidate workbook structure before accepting replacement inputs.

See:

- [`data/README.md`](data/README.md)
- [`docs/SOURCE_GOVERNANCE_STATUS.md`](docs/SOURCE_GOVERNANCE_STATUS.md)
- [`docs/validation/FINAL_RELEASE_VALIDATION.md`](docs/validation/FINAL_RELEASE_VALIDATION.md)
