# Data Dictionary and Source Mapping

| Canonical table | Source group | Main measures | Geography |
|---|---|---|---|
| fact_capacity | FY-005, FY-018 | Hospitals, Beds, Beds per 10,000, First Aid Centers, Ambulances | National / Administrative Region |
| fact_activity | FY-018, FY-020, FY-023 | Cases, Encounters, Admissions and official rates | National / Administrative Region |
| fact_workforce_sector | FY-006 | WorkforceCount, SaudiPercent | National |
| fact_workforce_nationality | FY-008, FY-010 | WorkforceCount | National |

Each fact retains `SourceGroup`, `SourceWorkbook`, and `SourceSheet`. The
source-to-target mapping is label-controlled in
`src/transformation/09_build_canonical_dataset.py`; aggregate workforce rows,
rolling historical columns, and FY-029 Blood Bank trend rows are excluded by
the approved contract.
