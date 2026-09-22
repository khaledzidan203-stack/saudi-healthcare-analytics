from pathlib import Path
from collections import defaultdict, Counter
import csv
import json
import re
import sys


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "outputs" / "discovery"
DOCS = ROOT / "docs" / "discovery"

CATALOG = OUT / "07_discovery_catalog.csv"
MATCHES = OUT / "08_cross_year_match_candidates.csv"
GEO = OUT / "09_geography_dictionary_candidates.csv"
PRIORITY = OUT / "10_priority_manual_review.csv"
PREVIEWS = OUT / "02_sheet_previews.csv"

FOUR_YEAR = OUT / "11_four_year_comparability_candidates.csv"
CORE = OUT / "12_core_portfolio_table_candidates.csv"
GEO_REVIEW = OUT / "13_geography_contract_review.csv"
VALIDATION = OUT / "14_manual_validation_queue.csv"
SELECTED_PREVIEWS = OUT / "15_selected_table_previews.csv"
SUMMARY = DOCS / "PHASE_1C_FINAL_DISCOVERY_SUMMARY.md"

REQUIRED_YEARS = {2021, 2022, 2023, 2024}

TARGET_TOPICS = {
    "Population",
    "Capacity",
    "Workforce",
    "Activity",
    "Population | Capacity",
    "Population | Activity",
    "Capacity | Workforce",
    "Capacity | Activity",
    "Workforce | Activity",
    "Capacity | Workforce | Activity",
    "Population | Capacity | Workforce",
}


def read_csv(path):
    if not path.exists():
        print(f"ERROR: Missing required file: {path}")
        sys.exit(1)

    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path, rows, fields=None):
    if fields is None:
        fields = list(rows[0].keys()) if rows else []

    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def safe_int(value):
    try:
        return int(float(value))
    except Exception:
        return None


def norm(value):
    if value is None:
        return ""

    text = str(value).strip().lower()

    replacements = {
        "\n": " ",
        "\r": " ",
        "_": " ",
        "–": "-",
        "—": "-",
        "/": " ",
        "\\": " ",
        "(": " ",
        ")": " ",
        ":": " ",
        ";": " ",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    text = re.sub(r"\b(2021|2022|2023|2024)\b", " ", text)
    text = re.sub(r"\d+", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


catalog = read_csv(CATALOG)
matches = read_csv(MATCHES)
geo_rows = read_csv(GEO)
priority = read_csv(PRIORITY)
preview_rows = read_csv(PREVIEWS)


# ============================================================
# 1. EXACT FOUR-YEAR STRUCTURAL GROUPS
# ============================================================

groups = defaultdict(list)

for row in catalog:

    if row.get("likely_analytical_table") != "YES":
        continue

    key = norm(row.get("normalized_match_title") or row.get("likely_table_title"))

    if not key:
        continue

    groups[(key, row.get("topic", ""))].append(row)


four_year_rows = []
group_id_counter = 1

for (match_key, topic), rows in groups.items():

    years = {
        safe_int(r.get("source_year"))
        for r in rows
        if safe_int(r.get("source_year")) is not None
    }

    if not REQUIRED_YEARS.issubset(years):
        continue

    group_id = f"FY-{group_id_counter:03d}"
    group_id_counter += 1

    geo_levels = sorted({
        r.get("geography_level_candidate", "")
        for r in rows
        if r.get("geography_level_candidate")
    })

    for r in sorted(
        rows,
        key=lambda x: safe_int(x.get("source_year")) or 0
    ):
        four_year_rows.append({
            "comparison_group_id": group_id,
            "source_year": r.get("source_year", ""),
            "workbook_name": r.get("workbook_name", ""),
            "sheet_name": r.get("sheet_name", ""),
            "chapter": r.get("chapter", ""),
            "topic": topic,
            "likely_table_title": r.get("likely_table_title", ""),
            "geography_level_candidate": r.get(
                "geography_level_candidate", ""
            ),
            "max_rows": r.get("max_rows", ""),
            "max_columns": r.get("max_columns", ""),
            "probable_header_row": r.get("probable_header_row", ""),
            "probable_data_start_row": r.get(
                "probable_data_start_row", ""
            ),
            "region_candidate_count": r.get(
                "region_candidate_count", ""
            ),
            "detected_years": r.get("detected_years", ""),
            "group_geography_levels": " | ".join(geo_levels),
            "comparison_status": "CANDIDATE_ONLY",
            "manual_validation_required": "YES"
        })


write_csv(
    FOUR_YEAR,
    four_year_rows,
    [
        "comparison_group_id",
        "source_year",
        "workbook_name",
        "sheet_name",
        "chapter",
        "topic",
        "likely_table_title",
        "geography_level_candidate",
        "max_rows",
        "max_columns",
        "probable_header_row",
        "probable_data_start_row",
        "region_candidate_count",
        "detected_years",
        "group_geography_levels",
        "comparison_status",
        "manual_validation_required"
    ]
)


# ============================================================
# 2. CORE PORTFOLIO CANDIDATES
# ============================================================

by_group = defaultdict(list)

for row in four_year_rows:
    by_group[row["comparison_group_id"]].append(row)


core_rows = []

for group_id, rows in by_group.items():

    topic = rows[0]["topic"]

    if topic not in TARGET_TOPICS:
        continue

    geo_levels = {
        r["geography_level_candidate"]
        for r in rows
    }

    region_years = {
        safe_int(r["source_year"])
        for r in rows
        if r["geography_level_candidate"] == "Health Region"
    }

    cluster_years = {
        safe_int(r["source_year"])
        for r in rows
        if r["geography_level_candidate"] == "Health Cluster"
    }

    # Scoring for MANUAL REVIEW priority only.
    # This is NOT analytical ranking.
    score = 0

    if topic != "Other":
        score += 4

    if len(region_years) >= 2:
        score += 4

    if region_years == REQUIRED_YEARS:
        score += 5

    if "Health Cluster" in geo_levels:
        score -= 2

    if all(safe_int(r["max_rows"]) and safe_int(r["max_rows"]) >= 5 for r in rows):
        score += 1

    if all(safe_int(r["max_columns"]) and safe_int(r["max_columns"]) >= 2 for r in rows):
        score += 1

    title = rows[0]["likely_table_title"]

    core_rows.append({
        "comparison_group_id": group_id,
        "topic": topic,
        "representative_title": title,
        "years_available": "2021 | 2022 | 2023 | 2024",
        "region_year_count": len(region_years),
        "cluster_year_count": len(cluster_years),
        "geography_levels_seen": " | ".join(sorted(geo_levels)),
        "review_priority_score": score,
        "recommended_review_class":
            "A" if score >= 12
            else "B" if score >= 8
            else "C",
        "confirmed_same_business_definition": "",
        "confirmed_same_grain": "",
        "confirmed_same_geography": "",
        "keep_for_project": "",
        "notes": ""
    })


core_rows.sort(
    key=lambda x: (
        -int(x["review_priority_score"]),
        x["topic"],
        x["representative_title"]
    )
)


write_csv(
    CORE,
    core_rows,
    list(core_rows[0].keys()) if core_rows else [
        "comparison_group_id",
        "topic",
        "representative_title",
        "years_available",
        "region_year_count",
        "cluster_year_count",
        "geography_levels_seen",
        "review_priority_score",
        "recommended_review_class",
        "confirmed_same_business_definition",
        "confirmed_same_grain",
        "confirmed_same_geography",
        "keep_for_project",
        "notes"
    ]
)


# ============================================================
# 3. GEOGRAPHY CONTRACT REVIEW
# ============================================================

geo_review = []

for row in geo_rows:

    source_value = row.get("source_value", "").strip()

    if not source_value:
        continue

    text = source_value.lower()

    if "cluster" in text or "تجمع" in source_value:
        proposed_type = "HEALTH_CLUSTER"
    else:
        proposed_type = "HEALTH_REGION_OR_ADMIN_REGION_REVIEW"

    geo_review.append({
        "source_value": source_value,
        "occurrence_count": row.get("occurrence_count", ""),
        "original_candidate_level": row.get(
            "candidate_level", ""
        ),
        "proposed_geography_type": proposed_type,
        "canonical_health_region": "",
        "canonical_health_cluster": "",
        "parent_health_region": "",
        "valid_from_year": "",
        "valid_to_year": "",
        "mapping_status": "REVIEW",
        "mapping_note": ""
    })


geo_review.sort(
    key=lambda x: (
        x["proposed_geography_type"],
        -safe_int(x["occurrence_count"])
        if safe_int(x["occurrence_count"]) is not None
        else 0,
        x["source_value"]
    )
)


write_csv(
    GEO_REVIEW,
    geo_review,
    list(geo_review[0].keys()) if geo_review else []
)


# ============================================================
# 4. MANUAL VALIDATION QUEUE
# ============================================================

validation_rows = []

for core in core_rows:

    if core["recommended_review_class"] not in {"A", "B"}:
        continue

    group_rows = by_group[
        core["comparison_group_id"]
    ]

    for row in group_rows:

        validation_rows.append({
            "comparison_group_id": core["comparison_group_id"],
            "review_class": core["recommended_review_class"],
            "topic": core["topic"],
            "source_year": row["source_year"],
            "workbook_name": row["workbook_name"],
            "sheet_name": row["sheet_name"],
            "likely_table_title": row["likely_table_title"],
            "geography_level_candidate":
                row["geography_level_candidate"],
            "probable_header_row":
                row["probable_header_row"],
            "probable_data_start_row":
                row["probable_data_start_row"],
            "check_title_definition": "PENDING",
            "check_row_grain": "PENDING",
            "check_column_structure": "PENDING",
            "check_geography": "PENDING",
            "check_totals": "PENDING",
            "check_units": "PENDING",
            "final_validation_status": "PENDING",
            "review_notes": ""
        })


write_csv(
    VALIDATION,
    validation_rows,
    list(validation_rows[0].keys()) if validation_rows else []
)


# ============================================================
# 5. PREVIEWS FOR SELECTED REVIEW QUEUE
# ============================================================

selected_keys = {
    (
        r["workbook_name"],
        r["sheet_name"]
    )
    for r in validation_rows
}

selected_preview_rows = []

for row in preview_rows:

    key = (
        row.get("workbook_name", ""),
        row.get("sheet_name", "")
    )

    if key in selected_keys:
        selected_preview_rows.append(row)


write_csv(
    SELECTED_PREVIEWS,
    selected_preview_rows,
    [
        "workbook_name",
        "sheet_name",
        "row_number",
        "values_json"
    ]
)


# ============================================================
# 6. DISCOVERY SUMMARY / PRELIMINARY DATA CONTRACT
# ============================================================

four_year_group_count = len(by_group)

class_counts = Counter(
    r["recommended_review_class"]
    for r in core_rows
)

topic_counts = Counter(
    r["topic"]
    for r in core_rows
)

region_complete_groups = sum(
    1
    for r in core_rows
    if safe_int(r["region_year_count"]) == 4
)

mixed_geo_groups = sum(
    1
    for r in core_rows
    if safe_int(r["cluster_year_count"]) > 0
    and safe_int(r["region_year_count"]) > 0
)


with SUMMARY.open("w", encoding="utf-8") as f:

    f.write("# Phase 1C — Final Discovery Summary\n\n")

    f.write(
        "## Project\n\n"
        "**Saudi Healthcare Capacity & Performance Analytics 2021–2024**\n\n"
    )

    f.write(
        "## Current Gate\n\n"
        "Discovery only. No source cleaning, joining, aggregation, "
        "KPI calculation, or analytical conclusion has been performed.\n\n"
    )

    f.write("## Discovery Results\n\n")
    f.write(f"- Source workbooks: **8**\n")
    f.write(f"- Source worksheets cataloged: **{len(catalog)}**\n")
    f.write(
        f"- Exact four-year structural candidate groups: "
        f"**{four_year_group_count}**\n"
    )
    f.write(
        f"- Core Population/Capacity/Workforce/Activity candidates: "
        f"**{len(core_rows)}**\n"
    )
    f.write(
        f"- Groups appearing region-level in all four years: "
        f"**{region_complete_groups}**\n"
    )
    f.write(
        f"- Groups showing mixed Region/Cluster geography clues: "
        f"**{mixed_geo_groups}**\n\n"
    )

    f.write("## Manual Review Classes\n\n")

    for cls in ["A", "B", "C"]:
        f.write(
            f"- Class {cls}: **{class_counts.get(cls, 0)}** groups\n"
        )

    f.write("\n## Core Topic Candidates\n\n")

    for topic, count in topic_counts.most_common():
        f.write(f"- {topic}: {count}\n")

    f.write(
        "\n## Preliminary Business Problem — Candidate\n\n"
        "Saudi healthcare decision-makers need a consistent multi-year "
        "view of healthcare capacity, workforce, and service activity "
        "across geographic areas to understand how resource availability "
        "and healthcare activity changed between 2021 and 2024 and where "
        "regional differences merit deeper review.\n\n"
    )

    f.write(
        "This wording is **provisional** until the selected source tables, "
        "grain, geography, and KPI definitions are manually validated.\n\n"
    )

    f.write("## Preliminary Analytical Domains\n\n")
    f.write("- Population context\n")
    f.write("- Healthcare facilities and bed capacity\n")
    f.write("- Healthcare workforce\n")
    f.write("- Healthcare service activity\n")
    f.write("- Regional trend comparison\n")
    f.write("- Resource-to-population ratios where officially supported\n")
    f.write("- Resource-to-activity ratios only where compatible grains exist\n\n")

    f.write("## Geography Contract Rule\n\n")
    f.write(
        "`Health Region`, `Administrative Region`, and `Health Cluster` "
        "must remain separate concepts until the official source structure "
        "proves a valid mapping. They must not be joined merely because "
        "their names appear geographically related.\n\n"
    )

    f.write("## Candidate Model — Not Yet Approved\n\n")
    f.write("```text\n")
    f.write("Dim_Year\n")
    f.write("Dim_Geography\n")
    f.write("Dim_Indicator / Measure\n")
    f.write("Dim_Facility / Workforce / Activity Type as required\n")
    f.write("\n")
    f.write("Fact_HealthCapacity\n")
    f.write("Fact_Workforce\n")
    f.write("Fact_HealthActivity\n")
    f.write("Fact_PopulationOrIndicators\n")
    f.write("```\n\n")

    f.write(
        "Final fact-table boundaries will follow confirmed source grain, "
        "not this preliminary design.\n\n"
    )

    f.write("## Approval Gate Before Cleaning\n\n")
    f.write("For each selected comparison group confirm:\n\n")
    f.write("1. Same business meaning across 2021–2024.\n")
    f.write("2. Same or reconcilable grain.\n")
    f.write("3. Same geography concept.\n")
    f.write("4. Same units and denominator definitions.\n")
    f.write("5. Total/subtotal behavior.\n")
    f.write("6. Header/data boundaries.\n")
    f.write("7. Source notes affecting interpretation.\n\n")

    f.write(
        "**No cleaning starts until this validation gate is completed.**\n"
    )


print("")
print("============================================================")
print("PHASE 1C — FINAL DISCOVERY COMPLETE")
print("============================================================")
print(f"Sheets cataloged:                  {len(catalog)}")
print(f"Four-year comparison groups:       {four_year_group_count}")
print(f"Core portfolio candidate groups:   {len(core_rows)}")
print(f"Region-complete groups:            {region_complete_groups}")
print(f"Mixed Region/Cluster groups:       {mixed_geo_groups}")
print(f"Manual validation rows:            {len(validation_rows)}")
print("Source files modified:             NO")

print("")
print("UPLOAD THESE FILES:")
print(FOUR_YEAR)
print(CORE)
print(GEO_REVIEW)
print(VALIDATION)
print(SELECTED_PREVIEWS)
print(SUMMARY)
