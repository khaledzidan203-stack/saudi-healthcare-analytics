# Phase 3 — Cached Formula Extraction Fix

## Root Cause

The FY-008 source table for 2021 contains at least one numeric measure
stored as an Excel formula/external workbook reference rather than as a
literal numeric cell.

The affected canonical grain was:

- Year: 2021
- Scope: MOH Total
- Workforce Type: Pharmacists
- Nationality: Non-Saudi

The formula-preserving workbook returned a formula expression rather than
a numeric value, so the original extraction pipeline treated the source
value as missing.

## Corrective Design

The canonical extraction now opens every source workbook in two modes:

1. `data_only=False`
   - preserves formulas and source structure.

2. `data_only=True`
   - reads Excel cached calculated values.

Numeric extraction uses a literal value when available and falls back to
the cached Excel value when the source cell contains a formula.

Missing values are never converted to zero.

## Regression Contract

The corrected pipeline requires:

- 4 reporting years
- 2 scopes
- 6 workforce types
- 2 nationalities

Expected canonical rows:

`4 × 2 × 6 × 2 = 96`

The pipeline fails hard if the matrix is incomplete.

A dedicated regression assertion also verifies:

`2021 × MOH Total × Pharmacists × Non-Saudi = 131`

## Code Governance

The superseded script:

`src/transformation/07_build_canonical_dataset.py`

is removed.

The current production script is:

`src/transformation/08_build_canonical_dataset.py`

Git history is the archive of prior code. Superseded production scripts
are not retained in the active source tree.
