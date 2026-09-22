from pathlib import Path
import csv
import json
import sys
from collections import defaultdict
from math import isclose


ROOT = Path(__file__).resolve().parents[1]

CANONICAL = (
    ROOT
    / "data"
    / "processed"
    / "canonical"
)


def read_csv(filename):
    path = CANONICAL / filename

    with path.open(
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as f:
        return list(
            csv.DictReader(f)
        )


errors = []
validation_output = {
    "status": "PASS",
    "checks": []
}


def check(name, passed, details):
    validation_output["checks"].append({
        "name": name,
        "status": "PASS" if passed else "FAIL",
        "details": details
    })
    if not passed:
        errors.append(details)


# ============================================================
# WORKFORCE NATIONALITY MATRIX
# ============================================================

rows = read_csv(
    "fact_workforce_nationality.csv"
)

expected_rows = 96

if len(rows) == expected_rows:
    print(
        "PASS: fact_workforce_nationality = 96 rows"
    )
else:
    check("fact_workforce_nationality_row_count", False,
          f"Expected 96 workforce nationality rows; found {len(rows)}")


years = [
    "2021",
    "2022",
    "2023",
    "2024",
]

scopes = [
    "MOH Total",
    "MOH Primary Health Care Centers",
]

workforce_types = [
    "Physicians",
    "Dentists",
    "Nurses",
    "Midwives",
    "Pharmacists",
    "Allied Health Personnel",
]

nationalities = [
    "Saudi",
    "Non-Saudi",
]


expected_matrix = {
    (
        year,
        scope,
        workforce,
        nationality
    )
    for year in years
    for scope in scopes
    for workforce in workforce_types
    for nationality in nationalities
}


actual_matrix = {
    (
        row["Year"],
        row["Scope"],
        row["WorkforceType"],
        row["Nationality"]
    )
    for row in rows
}


missing = sorted(
    expected_matrix - actual_matrix
)

unexpected = sorted(
    actual_matrix - expected_matrix
)


if not missing:
    print(
        "PASS: workforce nationality matrix complete"
    )
else:
    check("workforce_nationality_matrix", False, f"Missing grain rows: {missing}")


if not unexpected:
    print(
        "PASS: no unexpected workforce nationality grain rows"
    )
else:
    check("workforce_nationality_unexpected_grain", False, f"Unexpected grain rows: {unexpected}")


# ============================================================
# REGRESSION CELL
# ============================================================

target = [
    row
    for row in rows
    if (
        row["Year"] == "2021"
        and row["Scope"] == "MOH Total"
        and row["WorkforceType"] == "Pharmacists"
        and row["Nationality"] == "Non-Saudi"
    )
]


if len(target) != 1:

    check("fy008_regression_row", False, "Expected exactly one 2021 MOH Total / Pharmacists / Non-Saudi row.")

else:

    value = float(
        target[0]["WorkforceCount"]
    )

    print(
        "2021 MOH Total / Pharmacists / "
        f"Non-Saudi = {value:g}"
    )

    if value != 131:
        check("fy008_regression_value", False, f"Regression value expected 131; found {value:g}")
    else:
        print(
            "PASS: regression value = 131"
        )


# ============================================================
# DUPLICATE GRAIN
# ============================================================

keys = [
    (
        row["Year"],
        row["Geography"],
        row["Scope"],
        row["WorkforceType"],
        row["Nationality"]
    )
    for row in rows
]

duplicates = (
    len(keys)
    - len(set(keys))
)

if duplicates == 0:
    print(
        "PASS: workforce nationality duplicate grain = 0"
    )
else:
    check("workforce_nationality_duplicate_grain", False, f"Duplicate workforce nationality grain = {duplicates}")


# ============================================================
# CORE FACT CHECKS
# ============================================================

fact_tests = [
    (
        "fact_capacity.csv",
        [
            "Year",
            "GeographyType",
            "Geography",
            "Sector",
            "CapacityMeasure",
        ],
        "Value",
    ),
    (
        "fact_activity.csv",
        [
            "Year",
            "GeographyType",
            "Geography",
            "Sector",
            "ActivityMeasure",
        ],
        "Value",
    ),
    (
        "fact_workforce_sector.csv",
        [
            "Year",
            "Geography",
            "Sector",
            "WorkforceType",
        ],
        "WorkforceCount",
    ),
    (
        "fact_workforce_nationality.csv",
        ["Year", "GeographyType", "Geography", "Scope", "WorkforceType", "Nationality"],
        "WorkforceCount",
    ),
]


for filename, grain, measure in fact_tests:

    fact = read_csv(
        filename
    )

    fact_keys = [
        tuple(
            row[field]
            for field in grain
        )
        for row in fact
    ]

    duplicate_count = (
        len(fact_keys)
        - len(set(fact_keys))
    )

    missing_measure = sum(
        1
        for row in fact
        if row.get(measure, "") == ""
    )

    fact_years = sorted({
        row["Year"]
        for row in fact
    })


    if duplicate_count == 0:
        print(
            f"PASS: {filename} duplicate grain = 0"
        )
    else:
        check(f"{filename}_duplicate_grain", False, f"{filename} duplicate grain = {duplicate_count}")


    if missing_measure == 0:
        print(
            f"PASS: {filename} missing primary measures = 0"
        )
    else:
        check(f"{filename}_null_primary_measure", False, f"{filename} missing primary measures = {missing_measure}")


    if fact_years == years:
        print(
            f"PASS: {filename} year coverage = 2021-2024"
        )
    else:
        check(f"{filename}_year_coverage", False, f"{filename} year coverage = {fact_years}")


# ============================================================
# FY-006 ↔ FY-008 INDEPENDENT RECONCILIATION
# ============================================================

sector_rows = read_csv("fact_workforce_sector.csv")
sector_moh = {
    (row["Year"], row["WorkforceType"]): row
    for row in sector_rows
    if row["Sector"] == "Ministry of Health"
}

nationality_totals = defaultdict(lambda: {"Saudi": 0.0, "Non-Saudi": 0.0})
for row in rows:
    if row["Scope"] == "MOH Total":
        nationality_totals[(row["Year"], row["WorkforceType"])][row["Nationality"]] += float(row["WorkforceCount"])

reconciliation_failures = []
for key, source in sector_moh.items():
    saudi = nationality_totals[key]["Saudi"]
    non_saudi = nationality_totals[key]["Non-Saudi"]
    total = saudi + non_saudi
    workforce = float(source["WorkforceCount"])
    published_percent = float(source["SaudiPercent"])
    calculated_percent = saudi / total * 100 if total else None
    if workforce != total or calculated_percent is None or abs(published_percent - calculated_percent) > 0.15:
        reconciliation_failures.append({
            "Year": key[0], "WorkforceType": key[1],
            "FY006": workforce, "FY008": total,
            "PublishedSaudiPercent": published_percent,
            "CalculatedSaudiPercent": calculated_percent,
        })

if len(sector_moh) != 24:
    check("fy006_fy008_reconciliation_row_count", False, f"Expected 24 reconciliation rows; found {len(sector_moh)}")
elif reconciliation_failures:
    check("fy006_fy008_reconciliation", False, f"Reconciliation failures: {reconciliation_failures}")
else:
    print("PASS: FY006↔FY008 workforce reconciliation = 24 / 24")


# ============================================================
# FINAL
# ============================================================

print("")
print(
    "============================================================"
)

if errors:

    validation_output["status"] = "FAIL"

    print(
        f"FAIL: {len(errors)} PHASE 3 VALIDATION ISSUE(S)"
    )

    for error in errors:
        print(
            f"- {error}"
        )

    print(
        "============================================================"
    )

    sys.exit(1)


print(
    "PASS: PHASE 3 CANONICAL DATASET VALIDATED"
)
validation_output["status"] = "PASS"
(ROOT / "outputs" / "validation" / "phase3_independent_validation.json").write_text(
    json.dumps(validation_output, indent=2), encoding="utf-8"
)
print(
    "============================================================"
)

sys.exit(0)
