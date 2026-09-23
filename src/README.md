# Source pipeline

`discovery/01_workbook_inventory.py` through `06_build_core_validation_pack.py` profile official workbooks, identify comparable tables and create approval evidence. They read local `row_data/` and produce discovery, contract and validation outputs.

`transformation/09_build_canonical_dataset.py` creates nine canonical CSVs from approved source groups. It preserves annual grain, compatible geography, workbook/sheet lineage, missing-value distinctions and conservative Excel formula resolution. It also regenerates contract/validation documentation.

Run discovery scripts in numeric order, then transformation, only when deliberately reproducing the source pipeline in a working copy. No analytics rebuild is needed to review the release.

[Source placement](../data/README.md) · [Script index](../docs/SCRIPT_INDEX.md) · [Canonical contract](../docs/architecture/CANONICAL_DATA_CONTRACT.md)

SQL loading and validation entry points live in `scripts/`. The release audit uses Python's standard library and writes only its validation JSON. Validation scripts are provided; there is no separate implemented unit-test suite.
