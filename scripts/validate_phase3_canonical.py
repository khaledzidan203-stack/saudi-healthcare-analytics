from pathlib import Path
import csv
import sys


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
    errors.append(
        f"Expected 96 workforce nationality rows; "
        f"found {len(rows)}"
    )


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
    errors.append(
        f"Missing grain rows: {missing}"
    )


if not unexpected:
    print(
        "PASS: no unexpected workforce nationality grain rows"
    )
else:
    errors.append(
        f"Unexpected grain rows: {unexpected}"
    )


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

    errors.append(
        "Expected exactly one 2021 MOH Total / "
        "Pharmacists / Non-Saudi row."
    )

else:

    value = float(
        target[0]["WorkforceCount"]
    )

    print(
        "2021 MOH Total / Pharmacists / "
        f"Non-Saudi = {value:g}"
    )

    if value != 131:
        errors.append(
            "Regression value expected 131; "
            f"found {value:g}"
        )
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
    errors.append(
        f"Duplicate workforce nationality grain = {duplicates}"
    )


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
        errors.append(
            f"{filename} duplicate grain = "
            f"{duplicate_count}"
        )


    if missing_measure == 0:
        print(
            f"PASS: {filename} missing primary measures = 0"
        )
    else:
        errors.append(
            f"{filename} missing primary measures = "
            f"{missing_measure}"
        )


    if fact_years == years:
        print(
            f"PASS: {filename} year coverage = 2021-2024"
        )
    else:
        errors.append(
            f"{filename} year coverage = {fact_years}"
        )


# ============================================================
# FINAL
# ============================================================

print("")
print(
    "============================================================"
)

if errors:

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
print(
    "============================================================"
)

sys.exit(0)
