from collections import defaultdict
from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]
CAN = ROOT / "data" / "processed" / "canonical"
OUT = ROOT / "outputs" / "analysis"
OUT.mkdir(parents=True, exist_ok=True)


def read(name):
    with (CAN / name).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write(name, rows, fields):
    with (OUT / name).open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader(); w.writerows(rows)


def main():
    capacity = read("fact_capacity.csv")
    activity = read("fact_activity.csv")
    workforce = read("fact_workforce_sector.csv")

    cap = defaultdict(float)
    for r in capacity:
        if r["CapacityMeasure"] in {"Hospitals", "Beds"}:
            cap[(r["Year"], r["CapacityMeasure"])] += float(r["Value"])
    write("national_capacity_trend.csv", [{"Year": y, "Measure": m, "Value": v} for (y, m), v in sorted(cap.items())], ["Year", "Measure", "Value"])

    wf = defaultdict(float)
    for r in workforce:
        wf[(r["Year"], r["WorkforceType"])] += float(r["WorkforceCount"])
    write("national_workforce_by_type.csv", [{"Year": y, "WorkforceType": t, "WorkforceCount": v} for (y, t), v in sorted(wf.items())], ["Year", "WorkforceType", "WorkforceCount"])

    act = defaultdict(float)
    for r in activity:
        if r["ActivityMeasure"] in {"Encounters", "Inpatients / Admissions"}:
            act[(r["Year"], r["ActivityMeasure"])] += float(r["Value"])
    write("national_activity_trend.csv", [{"Year": y, "Measure": m, "Value": v} for (y, m), v in sorted(act.items())], ["Year", "Measure", "Value"])

    regional = defaultdict(float)
    for r in activity:
        if r["ActivityMeasure"] == "Cases offered first aid / transported to hospitals":
            regional[(r["Year"], r["Geography"], "Cases")] += float(r["Value"])
    for r in capacity:
        if r["CapacityMeasure"] in {"First Aid Centers", "Ambulances"}:
            regional[(r["Year"], r["Geography"], r["CapacityMeasure"])] += float(r["Value"])
    rows = []
    grouped = defaultdict(dict)
    for (year, geo, measure), value in regional.items(): grouped[(year, geo)][measure] = value
    for (year, geo), v in sorted(grouped.items()):
        rows.append({"Year": year, "Geography": geo, "Cases": v.get("Cases"), "FirstAidCenters": v.get("First Aid Centers"), "Ambulances": v.get("Ambulances"), "CasesPerCenter": v["Cases"] / v["First Aid Centers"] if v.get("First Aid Centers") else None, "CasesPerAmbulance": v["Cases"] / v["Ambulances"] if v.get("Ambulances") else None})
    write("red_crescent_regional_profile.csv", rows, ["Year", "Geography", "Cases", "FirstAidCenters", "Ambulances", "CasesPerCenter", "CasesPerAmbulance"])
    print(f"EDA outputs written: {len(list(OUT.glob('*.csv')))} files")


if __name__ == "__main__": main()
