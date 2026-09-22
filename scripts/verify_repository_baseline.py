from pathlib import Path
import csv
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_SCRIPTS = [
    "src/discovery/01_workbook_inventory.py",
    "src/discovery/02_comprehensive_discovery.py",
    "src/discovery/03_build_discovery_catalog.py",
    "src/discovery/04_final_discovery_scope.py",
    "src/discovery/05_validate_data_contract.py",
    "src/discovery/06_build_core_validation_pack.py",
    "src/transformation/08_build_canonical_dataset.py",
]

REQUIRED_DOCS = [
    "README.md",
    "PROJECT_PLAN.md",
    "CHANGELOG.md",
    "docs/PROJECT_INDEX.md",
    "docs/SCRIPT_INDEX.md",
    "docs/architecture/CANONICAL_DATA_CONTRACT.md",
    "docs/validation/PHASE_3_CANONICALIZATION_SUMMARY.md",
]

CANONICAL_FILES = [
    "data/processed/canonical/fact_capacity.csv",
    "data/processed/canonical/fact_activity.csv",
    "data/processed/canonical/fact_workforce_sector.csv",
    "data/processed/canonical/fact_workforce_nationality.csv",
    "data/processed/canonical/dim_year.csv",
    "data/processed/canonical/dim_geography.csv",
    "data/processed/canonical/dim_sector.csv",
    "data/processed/canonical/dim_workforce_type.csv",
    "data/processed/canonical/dim_nationality.csv",
]


def git(*args):
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    return result


def fail(message):
    print(f"FAIL  {message}")
    return message


def passed(message):
    print(f"PASS  {message}")


def read_csv(path):
    with path.open(
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as f:
        return list(csv.DictReader(f))


def validate_tracked_files(errors):

    print("")
    print("===== TRACKED FILE AUDIT =====")

    for relative in REQUIRED_SCRIPTS + REQUIRED_DOCS + CANONICAL_FILES:

        path = ROOT / relative

        if not path.exists():
            errors.append(
                fail(f"Missing required file: {relative}")
            )
            continue

        result = git(
            "ls-files",
            "--error-unmatch",
            relative
        )

        if result.returncode == 0:
            passed(relative)
        else:
            errors.append(
                fail(f"Not tracked by Git: {relative}")
            )


def validate_superseded_code(errors):

    print("")
    print("===== SUPERSEDED CODE AUDIT =====")

    old_script = (
        ROOT
        / "src"
        / "transformation"
        / "07_build_canonical_dataset.py"
    )

    if old_script.exists():
        errors.append(
            fail(
                "Superseded script still exists: "
                "src/transformation/07_build_canonical_dataset.py"
            )
        )
    else:
        passed("Superseded Phase 3 script is absent")


def validate_raw_git_policy(errors):

    print("")
    print("===== RAW SOURCE GIT AUDIT =====")

    result = git(
        "ls-files",
        "row_data/*"
    )

    tracked_raw = [
        line
        for line in result.stdout.splitlines()
        if line.strip()
    ]

    if tracked_raw:
        errors.append(
            fail(
                f"{len(tracked_raw)} raw source files are tracked by Git"
            )
        )
    else:
        passed("Raw official source files are excluded from Git")


def validate_workforce_nationality(errors):

    print("")
    print("===== WORKFORCE NATIONALITY REGRESSION =====")

    path = (
        ROOT
        / "data"
        / "processed"
        / "canonical"
        / "fact_workforce_nationality.csv"
    )

    rows = read_csv(path)

    expected_count = 96

    if len(rows) == expected_count:
        passed(
            f"fact_workforce_nationality rows = {expected_count}"
        )
    else:
        errors.append(
            fail(
                "fact_workforce_nationality "
                f"expected {expected_count}, found {len(rows)}"
            )
        )

    expected_matrix = {
        (
            str(year),
            scope,
            workforce,
            nationality,
        )
        for year in [2021, 2022, 2023, 2024]
        for scope in [
            "MOH Total",
            "MOH Primary Health Care Centers",
        ]
        for workforce in [
            "Physicians",
            "Dentists",
            "Nurses",
            "Midwives",
            "Pharmacists",
            "Allied Health Personnel",
        ]
        for nationality in [
            "Saudi",
            "Non-Saudi",
        ]
    }

    actual_matrix = {
        (
            row["Year"],
            row["Scope"],
            row["WorkforceType"],
            row["Nationality"],
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
        passed("Workforce nationality matrix has no missing grain rows")
    else:
        errors.append(
            fail(
                f"Missing workforce grain rows: {missing}"
            )
        )

    if not unexpected:
        passed("Workforce nationality matrix has no unexpected grain rows")
    else:
        errors.append(
            fail(
                f"Unexpected workforce grain rows: {unexpected}"
            )
        )

    natural_keys = [
        (
            row["Year"],
            row["Geography"],
            row["Scope"],
            row["WorkforceType"],
            row["Nationality"],
        )
        for row in rows
    ]

    duplicate_count = (
        len(natural_keys)
        - len(set(natural_keys))
    )

    if duplicate_count == 0:
        passed("Workforce duplicate natural keys = 0")
    else:
        errors.append(
            fail(
                f"Workforce duplicate natural keys = {duplicate_count}"
            )
        )

    regression = [
        row
        for row in rows
        if row["Year"] == "2021"
        and row["Scope"] == "MOH Total"
        and row["WorkforceType"] == "Pharmacists"
        and row["Nationality"] == "Non-Saudi"
    ]

    if len(regression) != 1:
        errors.append(
            fail(
                "Expected exactly one regression row for "
                "2021 / MOH Total / Pharmacists / Non-Saudi"
            )
        )
    else:

        value = float(
            regression[0]["WorkforceCount"]
        )

        if value == 131:
            passed(
                "2021 MOH Total / Pharmacists / Non-Saudi = 131"
            )
        else:
            errors.append(
                fail(
                    "2021 MOH Total / Pharmacists / Non-Saudi "
                    f"expected 131, found {value}"
                )
            )


def validate_core_fact_grains(errors):

    print("")
    print("===== CANONICAL FACT GRAIN AUDIT =====")

    tests = [
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
            [
                "Year",
                "Geography",
                "Scope",
                "WorkforceType",
                "Nationality",
            ],
            "WorkforceCount",
        ),
    ]

    base = (
        ROOT
        / "data"
        / "processed"
        / "canonical"
    )

    for filename, key_fields, measure_field in tests:

        rows = read_csv(
            base / filename
        )

        keys = [
            tuple(
                row[field]
                for field in key_fields
            )
            for row in rows
        ]

        duplicates = (
            len(keys)
            - len(set(keys))
        )

        missing_measure = sum(
            1
            for row in rows
            if row.get(measure_field, "") == ""
        )

        years = sorted({
            row["Year"]
            for row in rows
        })

        if duplicates == 0:
            passed(
                f"{filename}: duplicate grain = 0"
            )
        else:
            errors.append(
                fail(
                    f"{filename}: duplicate grain = {duplicates}"
                )
            )

        if missing_measure == 0:
            passed(
                f"{filename}: missing primary measures = 0"
            )
        else:
            errors.append(
                fail(
                    f"{filename}: missing primary measures "
                    f"= {missing_measure}"
                )
            )

        if years == [
            "2021",
            "2022",
            "2023",
            "2024",
        ]:
            passed(
                f"{filename}: year coverage 2021-2024"
            )
        else:
            errors.append(
                fail(
                    f"{filename}: unexpected year coverage {years}"
                )
            )


def validate_git_working_tree():

    print("")
    print("===== CURRENT GIT STATUS =====")

    result = git(
        "status",
        "--short"
    )

    status = [
        line
        for line in result.stdout.splitlines()
        if line.strip()
    ]

    # The audit script itself can be untracked during first execution.
    allowed = {
        "?? scripts/verify_repository_baseline.py"
    }

    unexpected = [
        line
        for line in status
        if line not in allowed
    ]

    if unexpected:
        print("REVIEW  Current uncommitted files:")
        for line in unexpected:
            print(f"  {line}")
    else:
        passed(
            "Working tree contains no unexpected changes"
        )

    return unexpected


def main():

    errors = []

    print(
        "============================================================"
    )
    print(
        "SAUDI HEALTHCARE ANALYTICS — REPOSITORY AUDIT"
    )
    print(
        "============================================================"
    )

    validate_tracked_files(errors)
    validate_superseded_code(errors)
    validate_raw_git_policy(errors)
    validate_workforce_nationality(errors)
    validate_core_fact_grains(errors)

    unexpected_status = (
        validate_git_working_tree()
    )

    if unexpected_status:
        errors.append(
            "Unexpected uncommitted Git files remain."
        )

    print("")
    print(
        "============================================================"
    )

    if errors:

        print(
            f"FAIL: {len(errors)} AUDIT ISSUE(S) FOUND"
        )

        for error in errors:
            print(f"- {error}")

        print(
            "============================================================"
        )

        sys.exit(1)

    print(
        "PASS: PROJECT BASELINE AND PHASE 3 FULLY VERIFIED"
    )
    print(
        "READY FOR PHASE 4 — SQL FOUNDATION"
    )
    print(
        "============================================================"
    )

    sys.exit(0)


if __name__ == "__main__":
    main()
