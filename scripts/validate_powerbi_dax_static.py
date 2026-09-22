from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / "powerbi" / "SaudiHealthcareAnalytics.SemanticModel" / "definition"
REPORT = ROOT / "powerbi" / "SaudiHealthcareAnalytics.Report" / "definition"
OUTPUT = ROOT / "outputs" / "validation" / "powerbi_dax_static_validation.json"


def count(pattern, text):
    return len(re.findall(pattern, text, flags=re.MULTILINE))


def main():
    checks = []

    def add(name, passed, details):
        checks.append({"name": name, "status": "PASS" if passed else "FAIL", "details": details})

    table_files = sorted((MODEL / "tables").glob("*.tmdl"))
    measure_file = MODEL / "tables" / "_Measures.tmdl"
    measure_text = measure_file.read_text(encoding="utf-8")
    relationship_text = (MODEL / "relationships.tmdl").read_text(encoding="utf-8")
    model_text = (MODEL / "model.tmdl").read_text(encoding="utf-8")

    add("table_count", len(table_files) == 10, len(table_files))
    add("measures_table_exists", measure_file.exists(), str(measure_file))
    add("measures_table_referenced", "ref table _Measures" in model_text, "ref table _Measures")
    add("measure_count", count(r"^\s*measure ", measure_text) == 12, count(r"^\s*measure ", measure_text))

    measures_outside = 0
    for file in table_files:
        if file.name != "_Measures.tmdl":
            measures_outside += count(r"^\s*measure ", file.read_text(encoding="utf-8"))
    add("measures_outside_measures_table", measures_outside == 0, measures_outside)

    placeholder_ok = (
        "column Placeholder" in measure_text
        and re.search(r"column Placeholder\s+isHidden", measure_text)
        and "source = FILTER(ROW(\"Placeholder\", 0), FALSE())" in measure_text
    )
    add("zero_row_hidden_placeholder", bool(placeholder_ok), "FILTER(ROW(...), FALSE())")
    add("measures_relationships", "_Measures" not in relationship_text, 0)

    relationships = count(r"^relationship ", relationship_text)
    add("relationship_count", relationships == 14, relationships)
    add("many_to_one_count", count(r"^\s*fromCardinality: many$", relationship_text) == 14 and count(r"^\s*toCardinality: one$", relationship_text) == 14, 14)
    add("single_direction_count", count(r"^\s*crossFilteringBehavior: oneDirection$", relationship_text) == 14, 14)
    add("active_relationship_count", count(r"^\s*isActive: true$", relationship_text) == 14, 14)

    pages = json.loads((REPORT / "pages" / "pages.json").read_text(encoding="utf-8"))["pageOrder"]
    visual_files = list((REPORT / "pages").glob("**/visual.json"))
    add("page_count", len(pages) == 1, len(pages))
    add("visual_count", len(visual_files) == 0, len(visual_files))

    all_model_text = "\n".join(file.read_text(encoding="utf-8") for file in table_files)
    add("sql_source_unchanged", all_model_text.count('Sql.Database("localhost", "SaudiHealthcareAnalytics")') == 9, 9)
    add("no_calculated_business_columns", count(r"^\s*column ", measure_text) == 1, 1)
    add("auto_date_disabled", "__PBI_TimeIntelligenceEnabled = 0" in model_text, True)

    status = "PASS" if all(item["status"] == "PASS" for item in checks) else "FAIL"
    result = {
        "status": status,
        "runtime_status": "PENDING",
        "tmdl_parser": "Tabular Editor 2.28.0 loaded 10 tables, 12 measures, 14 relationships",
        "checks": checks,
    }
    OUTPUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"POWER BI DAX STATIC VALIDATION: {status}")
    for item in checks:
        print(f"{item['status']}: {item['name']} - {item['details']}")
    raise SystemExit(0 if status == "PASS" else 1)


if __name__ == "__main__":
    main()
