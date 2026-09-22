from pathlib import Path
from openpyxl import load_workbook
from collections import Counter
import csv
import json
import re
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "row_data"
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "discovery"
DOCS_DIR = PROJECT_ROOT / "docs" / "discovery"

STRUCTURE_FILE = OUTPUT_DIR / "01_sheet_structural_profile.csv"
PREVIEW_FILE = OUTPUT_DIR / "02_sheet_previews.csv"

CATALOG_FILE = OUTPUT_DIR / "07_discovery_catalog.csv"
MATCH_FILE = OUTPUT_DIR / "08_cross_year_match_candidates.csv"
GEO_FILE = OUTPUT_DIR / "09_geography_dictionary_candidates.csv"
REVIEW_FILE = OUTPUT_DIR / "10_priority_manual_review.csv"
SUMMARY_FILE = DOCS_DIR / "PHASE_1B_DISCOVERY_CATALOG_SUMMARY.md"


# ------------------------------------------------------------
# HELPERS
# ------------------------------------------------------------

def clean_text(value):
    if value is None:
        return ""

    text = str(value).strip()
    text = text.replace("\n", " ").replace("\r", " ")
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def normalized(value):
    text = clean_text(value).lower()

    replacements = {
        "–": "-",
        "—": "-",
        "_": " ",
        ".": " ",
        "/": " ",
        "\\": " ",
        "(": " ",
        ")": " ",
        ":": " ",
        ";": " ",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def extract_source_year(filename):
    match = re.search(r"(2021|2022|2023|2024)", filename)

    if match:
        return int(match.group(1))

    return None


def infer_chapter(workbook, sheet):
    w = normalized(workbook)
    s = normalized(sheet)

    if "chapter-i-" in workbook.lower():
        return "Health Indicators"

    if "chapter-ii-" in workbook.lower():
        return "Health Resources"

    if "chapter-iv-" in workbook.lower():
        return "Health Activities"

    # 2023 / 2024 combined yearbooks
    if s.startswith("1 ") or s.startswith("1-"):
        return "Health Indicators"

    if s.startswith("2 ") or s.startswith("2-"):
        return "Health Resources"

    if s.startswith("4 ") or s.startswith("4-"):
        return "Health Activities"

    return "Unknown / Other"


def is_index_sheet(sheet):
    s = normalized(sheet)

    return (
        "فهرس" in s
        or "index" in s
        or "contents" in s
    )


def extract_preview_text(records):
    values = []

    for r in records:
        try:
            row_values = json.loads(r["values_json"])
        except Exception:
            continue

        for value in row_values:
            value = clean_text(value)

            if value:
                values.append(value)

    return values


def candidate_title(values):
    """
    Finds likely descriptive title from the first rows.
    Avoids short numeric table identifiers when possible.
    """

    candidates = []

    for value in values:
        text = clean_text(value)

        if len(text) < 6:
            continue

        # Skip pure numeric / table numbers
        if re.fullmatch(r"[\d\.\-\s]+", text):
            continue

        # Prefer descriptive titles
        score = len(text)

        lower = text.lower()

        if any(k in lower for k in [
            "table",
            "جدول",
            "health",
            "hospital",
            "population",
            "region",
            "bed",
            "physician",
            "nurse",
            "activity",
            "visits",
            "السكان",
            "المنطقة",
            "المستشفيات",
            "الأطباء",
            "التمريض",
            "الأسرة",
            "الزيارات"
        ]):
            score += 100

        candidates.append((score, text))

    if not candidates:
        return ""

    candidates.sort(reverse=True)

    return candidates[0][1][:500]


def topic_classification(text):
    t = normalized(text)

    topics = []

    rules = {
        "Population": [
            "population", "السكان"
        ],
        "Capacity": [
            "hospital", "hospitals",
            "bed", "beds",
            "مستشفى", "المستشفيات",
            "سرير", "أسرة", "الأسرة",
            "health center", "health centres",
            "primary health", "مركز صحي",
            "المراكز الصحية"
        ],
        "Workforce": [
            "physician", "physicians",
            "doctor", "doctors",
            "nurse", "nurses",
            "dentist", "pharmacist",
            "health manpower",
            "workforce",
            "طبيب", "الأطباء",
            "تمريض", "ممرض",
            "صيدلي", "الصيادلة",
            "قوى عاملة"
        ],
        "Activity": [
            "visits", "visit",
            "admission", "admissions",
            "outpatient",
            "emergency",
            "operation", "operations",
            "surgery", "surgeries",
            "discharge",
            "activity", "activities",
            "الزيارات", "المراجعين",
            "التنويم", "المنومين",
            "الطوارئ",
            "العمليات",
            "الأنشطة"
        ]
    }

    for topic, words in rules.items():
        if any(normalized(w) in t for w in words):
            topics.append(topic)

    if not topics:
        return "Other"

    return " | ".join(topics)


def geography_level(text):
    t = normalized(text)

    cluster_words = [
        "health cluster",
        "cluster",
        "تجمع صحي",
        "تجمع",
    ]

    region_words = [
        "health region",
        "region",
        "regions",
        "المنطقة الصحية",
        "المناطق الصحية",
        "المنطقة",
        "المناطق"
    ]

    if any(normalized(x) in t for x in cluster_words):
        return "Health Cluster"

    if any(normalized(x) in t for x in region_words):
        return "Health Region"

    return "Unknown / National / Other"


def normalize_title_for_matching(title):
    text = normalized(title)

    # Remove years
    text = re.sub(r"\b20\d{2}\b", " ", text)

    # Remove common table boilerplate
    stop_phrases = [
        "table",
        "جدول",
        "for the year",
        "لعام",
        "عام",
        "during",
        "حسب",
    ]

    for phrase in stop_phrases:
        text = text.replace(normalized(phrase), " ")

    text = re.sub(r"\d+", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def token_similarity(a, b):
    a_tokens = set(normalized(a).split())
    b_tokens = set(normalized(b).split())

    if not a_tokens or not b_tokens:
        return 0.0

    return len(a_tokens & b_tokens) / len(a_tokens | b_tokens)


# ------------------------------------------------------------
# LOAD DISCOVERY OUTPUTS
# ------------------------------------------------------------

if not STRUCTURE_FILE.exists() or not PREVIEW_FILE.exists():
    print("ERROR: Previous Phase 1 discovery outputs are missing.")
    sys.exit(1)


with STRUCTURE_FILE.open("r", encoding="utf-8-sig") as f:
    structure_rows = list(csv.DictReader(f))


with PREVIEW_FILE.open("r", encoding="utf-8-sig") as f:
    preview_rows = list(csv.DictReader(f))


previews_by_sheet = {}

for row in preview_rows:
    key = (
        row["workbook_name"],
        row["sheet_name"]
    )

    previews_by_sheet.setdefault(key, []).append(row)


# ------------------------------------------------------------
# BUILD DISCOVERY CATALOG
# ------------------------------------------------------------

catalog = []

for row in structure_rows:

    workbook = row["workbook_name"]
    sheet = row["sheet_name"]

    preview_records = previews_by_sheet.get(
        (workbook, sheet),
        []
    )

    preview_values = extract_preview_text(
        preview_records
    )

    preview_text = " | ".join(
        preview_values
    )

    title = candidate_title(
        preview_values
    )

    combined = (
        f"{sheet} | {title} | {preview_text}"
    )

    year = extract_source_year(
        workbook
    )

    chapter = infer_chapter(
        workbook,
        sheet
    )

    topics = topic_classification(
        combined
    )

    geo_level = geography_level(
        combined
    )

    index_flag = is_index_sheet(
        sheet
    )

    likely_analytical = (
        not index_flag
        and int(float(row.get("max_row_reported", 0) or 0)) >= 5
        and int(float(row.get("max_column_reported", 0) or 0)) >= 2
    )

    catalog.append({
        "source_year": year or "",
        "workbook_name": workbook,
        "sheet_name": sheet,
        "chapter": chapter,
        "likely_table_title": title,
        "topic": topics,
        "geography_level_candidate": geo_level,
        "is_index_sheet": "YES" if index_flag else "NO",
        "likely_analytical_table": "YES" if likely_analytical else "NO",
        "max_rows": row["max_row_reported"],
        "max_columns": row["max_column_reported"],
        "probable_header_row": row["probable_header_row"],
        "probable_data_start_row": row["probable_data_start_row"],
        "region_candidate_count": row["region_candidate_count"],
        "total_keyword_hits": row["total_keyword_hits"],
        "source_keyword_hits": row["source_keyword_hits"],
        "detected_years": row["detected_years"],
        "normalized_match_title": normalize_title_for_matching(title)
    })


# ------------------------------------------------------------
# CROSS-YEAR MATCHING
# ------------------------------------------------------------

analytical_catalog = [
    x for x in catalog
    if x["likely_analytical_table"] == "YES"
    and x["topic"] != "Other"
    and x["normalized_match_title"]
]


matches = []

for i, left in enumerate(analytical_catalog):

    for right in analytical_catalog[i + 1:]:

        if left["source_year"] == right["source_year"]:
            continue

        # Prefer same topic / chapter
        if left["topic"] != right["topic"]:
            continue

        similarity = token_similarity(
            left["normalized_match_title"],
            right["normalized_match_title"]
        )

        if similarity >= 0.35:

            matches.append({
                "year_a": left["source_year"],
                "workbook_a": left["workbook_name"],
                "sheet_a": left["sheet_name"],
                "title_a": left["likely_table_title"],

                "year_b": right["source_year"],
                "workbook_b": right["workbook_name"],
                "sheet_b": right["sheet_name"],
                "title_b": right["likely_table_title"],

                "topic": left["topic"],
                "similarity_score": round(similarity, 3),
                "manual_validation_required": "YES"
            })


matches.sort(
    key=lambda x: x["similarity_score"],
    reverse=True
)


# ------------------------------------------------------------
# GEOGRAPHY DICTIONARY CANDIDATES
# Scan actual source values conservatively
# ------------------------------------------------------------

region_patterns = [
    "riyadh", "الرياض",
    "makkah", "مكة",
    "madinah", "المدينة",
    "qassim", "القصيم",
    "eastern", "الشرقية",
    "asir", "عسير",
    "tabuk", "تبوك",
    "hail", "حائل",
    "jazan", "جازان",
    "najran", "نجران",
    "baha", "bahah", "الباحة",
    "jouf", "الجوف",
    "northern borders", "الحدود الشمالية",
    "health cluster", "تجمع"
]

geo_counter = Counter()

for records in previews_by_sheet.values():

    for record in records:

        try:
            values = json.loads(
                record["values_json"]
            )
        except Exception:
            continue

        for value in values:

            value = clean_text(value)

            if not value:
                continue

            nv = normalized(value)

            if any(
                normalized(pattern) in nv
                for pattern in region_patterns
            ):
                geo_counter[value] += 1


geo_rows = []

for value, count in geo_counter.most_common():

    geo_rows.append({
        "source_value": value,
        "occurrence_count": count,
        "candidate_level": geography_level(value),
        "canonical_value": "",
        "mapping_status": "REVIEW",
        "mapping_note": ""
    })


# ------------------------------------------------------------
# PRIORITY REVIEW QUEUE
# ------------------------------------------------------------

priority_rows = []

for row in catalog:

    if row["likely_analytical_table"] != "YES":
        continue

    priority_score = 0

    if row["topic"] != "Other":
        priority_score += 3

    if int(float(row["region_candidate_count"] or 0)) > 0:
        priority_score += 3

    if row["geography_level_candidate"] != "Unknown / National / Other":
        priority_score += 2

    if row["chapter"] in [
        "Health Indicators",
        "Health Resources",
        "Health Activities"
    ]:
        priority_score += 2

    priority_rows.append({
        **row,
        "priority_score": priority_score,
        "manual_review_status": "PENDING",
        "confirmed_grain": "",
        "confirmed_geography_level": "",
        "cross_year_merge_group": "",
        "review_notes": ""
    })


priority_rows.sort(
    key=lambda x: (
        -x["priority_score"],
        x["source_year"],
        x["workbook_name"],
        x["sheet_name"]
    )
)


# ------------------------------------------------------------
# WRITE OUTPUTS
# ------------------------------------------------------------

def write_csv(path, rows, fields):

    with path.open(
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=fields
        )

        writer.writeheader()
        writer.writerows(rows)


write_csv(
    CATALOG_FILE,
    catalog,
    list(catalog[0].keys())
)


if matches:
    write_csv(
        MATCH_FILE,
        matches,
        list(matches[0].keys())
    )
else:
    write_csv(
        MATCH_FILE,
        [],
        [
            "year_a",
            "workbook_a",
            "sheet_a",
            "title_a",
            "year_b",
            "workbook_b",
            "sheet_b",
            "title_b",
            "topic",
            "similarity_score",
            "manual_validation_required"
        ]
    )


write_csv(
    GEO_FILE,
    geo_rows,
    [
        "source_value",
        "occurrence_count",
        "candidate_level",
        "canonical_value",
        "mapping_status",
        "mapping_note"
    ]
)


write_csv(
    REVIEW_FILE,
    priority_rows,
    list(priority_rows[0].keys())
)


# ------------------------------------------------------------
# SUMMARY
# ------------------------------------------------------------

topic_counts = Counter(
    row["topic"]
    for row in catalog
)

geo_counts = Counter(
    row["geography_level_candidate"]
    for row in catalog
)

chapter_counts = Counter(
    row["chapter"]
    for row in catalog
)

high_similarity = [
    m for m in matches
    if m["similarity_score"] >= 0.60
]


with SUMMARY_FILE.open(
    "w",
    encoding="utf-8"
) as f:

    f.write(
        "# Phase 1B — Discovery Catalog Summary\n\n"
    )

    f.write(
        "## Scope\n\n"
        "This phase organizes the 644 discovered worksheets into a "
        "reviewable analytical catalog. All classifications remain "
        "discovery candidates until manually validated.\n\n"
    )

    f.write(
        f"- Sheets cataloged: **{len(catalog)}**\n"
    )

    f.write(
        f"- Priority analytical review candidates: "
        f"**{len(priority_rows)}**\n"
    )

    f.write(
        f"- Cross-year match candidates: "
        f"**{len(matches)}**\n"
    )

    f.write(
        f"- Strong cross-year matches (>= 0.60): "
        f"**{len(high_similarity)}**\n"
    )

    f.write(
        f"- Distinct geography-like source values: "
        f"**{len(geo_rows)}**\n\n"
    )


    f.write(
        "## Topic Classification\n\n"
    )

    for topic, count in topic_counts.most_common():
        f.write(
            f"- {topic}: {count}\n"
        )


    f.write(
        "\n## Geography-Level Candidates\n\n"
    )

    for level, count in geo_counts.most_common():
        f.write(
            f"- {level}: {count}\n"
        )


    f.write(
        "\n## Chapter Classification\n\n"
    )

    for chapter, count in chapter_counts.most_common():
        f.write(
            f"- {chapter}: {count}\n"
        )


    f.write(
        "\n## Important Finding\n\n"
        "The source contains both traditional regional labels and "
        "health-cluster terminology. These must not be assumed to "
        "represent the same geography grain. A governed geography "
        "contract is required before cross-year joins.\n"
    )


    f.write(
        "\n## Next Gate\n\n"
        "Manual validation should focus on the highest-priority tables "
        "and strongest cross-year matches before any cleaning or "
        "canonicalization begins.\n"
    )


    f.write(
        "\n## Source Modification\n\n"
        "**NO source workbook was modified.**\n"
    )


print("")
print("============================================================")
print("PHASE 1B COMPLETE")
print("============================================================")
print(f"Sheets cataloged:             {len(catalog)}")
print(f"Priority review candidates:   {len(priority_rows)}")
print(f"Cross-year match candidates:  {len(matches)}")
print(f"Strong matches >= 0.60:       {len(high_similarity)}")
print(f"Geography candidates:         {len(geo_rows)}")
print("Source files modified:        NO")

print("")
print("UPLOAD THESE FILES:")
print(CATALOG_FILE)
print(MATCH_FILE)
print(GEO_FILE)
print(REVIEW_FILE)
print(SUMMARY_FILE)

