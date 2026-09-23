"""Offline release checks. Does not rebuild data, query SQL or alter Power BI."""
from pathlib import Path
from decimal import Decimal
from urllib.parse import unquote
import ast
import csv
import hashlib
import io
import json
import re
import struct
import subprocess
import zipfile
import zlib

ROOT = Path(__file__).resolve().parents[1]
BASELINE = "a4f47c5"
REPORT = "powerbi/SaudiHealthcareAnalytics.Report/definition/pages"
MODEL = "powerbi/SaudiHealthcareAnalytics.SemanticModel/definition"
INDEX = "850ce1b1e37e9e00e59e"
OUTPUT = "outputs/validation/final_release_validation.json"
SHOTS = {
    "00_index.png": "E2F09EC821AAF042D0BEA117BADD6EC5E1F072DF67EA540A4AE0FE028D0A9E7B",
    "01_executive_overview.png": "2DF018CF5F266B21E67C812447C476B57B1D45CCD234E815B41D7E08A79A2C63",
    "02_healthcare_capacity.png": "19A0F254A5FC9A21CE7FA823EB13EA724E71B1B053DEC7F0CF06A619BA88AC0F",
    "03_healthcare_activity.png": "6B1E35444A280DFC5A865A79BA5E846D66795F8ECC1D0DEBC65E635DACE83B8D",
    "04_workforce_nationalization.png": "79372D86CBAC4D39AC6BA325DB1397156C374F6A6ABBE22856066580D5698FA2",
    "05_red_crescent_regional_performance.png": "7EB1530A095B6628C617B2E07D6B2348807EA29CCBF4C311EAA152F1616A907E",
    "06_methodology_validation.png": "D2AC9BB6D9605C418673BA4CC28DE3BA9DBF54D7E90956062C3FB5D12CA345BF",
}
checks = []


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def check(name, ok, details):
    checks.append({"name": name, "status": "PASS" if ok else "FAIL", "details": details})


def read_json(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8-sig"))


def csv_rows(name):
    with (ROOT / "data/processed/canonical" / name).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def walk(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def main():
    files = sorted(set(git("ls-files", "--cached", "--others", "--exclude-standard").decode().splitlines()))
    check("approved_checkpoint", git("rev-parse", BASELINE).decode().strip().startswith(BASELINE), BASELINE)
    json_errors = []
    for name in files:
        if Path(name).suffix in (".json", ".pbip", ".pbir", ".pbism", ".platform"):
            try:
                read_json(name)
            except (ValueError, OSError) as exc:
                json_errors.append({"file": name, "error": str(exc)})
    check("json_parsing", not json_errors, json_errors)
    pages_meta = read_json(REPORT + "/pages.json")
    pages = [read_json(REPORT + "/" + pid + "/page.json") for pid in pages_meta["pageOrder"]]
    expected = ["INDEX", "Executive Overview", "Healthcare Capacity", "Healthcare Activity", "Workforce & Nationalization", "Red Crescent Regional Performance", "Methodology & Validation"]
    check("page_inventory_and_opening", [p["displayName"] for p in pages] == expected and pages_meta["activePageName"] == INDEX, expected)
    ids, inventory, home, destinations = [], {}, [], []
    for page in pages:
        visuals = sorted((ROOT / REPORT / page["name"] / "visuals").glob("*/visual.json"))
        inventory[page["displayName"]] = len(visuals)
        for path in visuals:
            visual = json.loads(path.read_text(encoding="utf-8-sig"))
            ids.append(visual["name"])
            for obj in walk(visual):
                if "navigationSection" in obj:
                    target = obj["navigationSection"]["expr"]["Literal"]["Value"].strip("'")
                    destinations.append(target)
                    if target == INDEX:
                        home.append(page["name"])
    check("visual_id_uniqueness", len(ids) == len(set(ids)), {"total": len(ids), "pages": inventory})
    check("home_and_navigation", set(home) == {p["name"] for p in pages if p["name"] != INDEX} and all(d in pages_meta["pageOrder"] for d in destinations), {"home_buttons": len(home), "navigation_targets": len(destinations)})
    check("methodology_visual_inventory", inventory["Methodology & Validation"] == 43, inventory["Methodology & Validation"])
    short_rows = list((ROOT / REPORT / "efc08ca01fea8d2326ac" / "visuals").glob("mv31*/visual.json"))
    check("methodology_short_rows", len(short_rows) == 29, len(short_rows))

    # Only the approved Year selection and opening page may differ from the report baseline.
    baseline_files = git("ls-tree", "-r", "--name-only", BASELINE, "powerbi").decode().splitlines()
    changes = []
    for name in baseline_files:
        old = git("show", f"{BASELINE}:{name}")
        new = (ROOT / name).read_bytes()
        if name.endswith("pages/pages.json"):
            before, after = json.loads(old), json.loads(new)
            after["activePageName"] = before["activePageName"]
            same = before == after
        elif name.endswith("hc_exec_000000000003/visual.json"):
            before, after = json.loads(old), json.loads(new)
            properties = after["visual"]["objects"]["general"][0]["properties"]
            saved = properties.pop("filter")
            expr = saved["filter"]
            check("executive_default_2024", expr["From"][0]["Entity"] == "analytics DimYear" and expr["Where"][0]["Condition"]["In"]["Values"] == [[{"Literal": {"Value": "2024L"}}]], "Year slicer saved at 2024")
            same = before == after
        else:
            same = old.replace(b"\r\n", b"\n") == new.replace(b"\r\n", b"\n")
        if not same:
            changes.append(name)
    check("powerbi_preserved_except_approved_state", not changes, changes)
    changed_analytics = git("diff", BASELINE, "--name-only", "--", "src", "sql", "data/processed/canonical", "powerbi/SaudiHealthcareAnalytics.SemanticModel").decode().splitlines()
    changed_analytics = [p for p in changed_analytics if Path(p).suffix != ".md"]
    check("analytical_sources_unchanged", not changed_analytics, changed_analytics)
    tmdl = sorted((ROOT / MODEL / "tables").glob("*.tmdl"))
    measures = sum(len(re.findall(r"^\s*measure ", p.read_text(encoding="utf-8-sig"), re.M)) for p in tmdl)
    relationships = (ROOT / MODEL / "relationships.tmdl").read_text(encoding="utf-8-sig")
    blocks = re.split(r"(?m)^relationship ", relationships)[1:]
    resolved = []
    for block in blocks:
        def prop(key, default):
            match = re.search(r"(?m)^\s*" + key + r":\s*(\S+)", block)
            return match.group(1) if match else default
        resolved.append({"from": prop("fromCardinality", "many"), "to": prop("toCardinality", "one"), "direction": prop("crossFilteringBehavior", "oneDirection"), "active": prop("isActive", "true")})
    check("semantic_inventory", len(tmdl) == 10 and measures == 15 and len(blocks) == 14, {"business_tables": 9, "total_tables": len(tmdl), "measures": measures, "relationships": len(blocks)})
    check("relationship_defaults", all(r == {"from": "many", "to": "one", "direction": "oneDirection", "active": "true"} for r in resolved) and "_Measures" not in relationships, resolved)
    edges = []
    for block in blocks:
        source = re.search(r"fromColumn: '([^']+)'\.(\w+)", block)
        target = re.search(r"toColumn: '([^']+)'\.(\w+)", block)
        if source and target:
            edges.append((source.group(1), target.group(1)))
    star_ok = len(edges) == 14 and len(set(edges)) == 14 and all(f.startswith("analytics Fact") and d.startswith("analytics Dim") for f, d in edges)
    check("unambiguous_star_paths", star_ok, "Unique single-direction dimension-to-fact edges; no chains or fact-to-fact edges" if star_ok else edges)
    model = (ROOT / MODEL / "model.tmdl").read_text(encoding="utf-8-sig")
    check("auto_date_disabled", "__PBI_TimeIntelligenceEnabled = 0" in model, "No auto date/time")
    check("sql_partitions", sum(p.read_text(encoding="utf-8-sig").count('Sql.Database("localhost", "SaudiHealthcareAnalytics")') for p in tmdl) == 9, "Nine SQL Import sources; unchanged from approved baseline")

    facts = {}
    for name, expected_count in {"fact_capacity": 132, "fact_activity": 84, "fact_workforce_sector": 72, "fact_workforce_nationality": 96}.items():
        rows = csv_rows(name + ".csv")
        facts[name] = rows
        check(name + "_rows", len(rows) == expected_count and {r["Year"] for r in rows} == {"2021", "2022", "2023", "2024"}, len(rows))
    claims = {}
    for measure, fact, label, field in [
        ("Hospitals", "fact_capacity", "CapacityMeasure", "Hospitals"),
        ("Beds", "fact_capacity", "CapacityMeasure", "Beds"),
        ("Encounters", "fact_activity", "ActivityMeasure", "Encounters"),
        ("Admissions", "fact_activity", "ActivityMeasure", "Inpatients / Admissions"),
        ("Red Crescent Cases", "fact_activity", "ActivityMeasure", "Cases offered first aid / transported to hospitals"),
    ]:
        claims[measure] = sum(Decimal(r["Value"]) for r in facts[fact] if r["Year"] == "2024" and r[label] == field)
    claims["Workforce Count"] = sum(Decimal(r["WorkforceCount"]) for r in facts["fact_workforce_sector"] if r["Year"] == "2024")
    moh = [r for r in facts["fact_workforce_nationality"] if r["Year"] == "2024" and r["Scope"] == "MOH Total"]
    claims["Saudi Workforce Share"] = sum(Decimal(r["WorkforceCount"]) for r in moh if r["Nationality"] == "Saudi") / sum(Decimal(r["WorkforceCount"]) for r in moh)
    runtime = read_json("outputs/validation/powerbi_dax_runtime_validation.json")
    for measure, value in claims.items():
        item = next(r for r in runtime["Results"] if r["Measure"] == measure)
        row = next(r for r in item["Comparisons"] if r["Year"] == 2024)
        check("headline_" + measure, abs(value - Decimal(str(row["SQL"]))) < Decimal("0.000001"), {"canonical": str(value), "recorded_SQL": row["SQL"]})
    check("historical_runtime_evidence", runtime["Status"] == "PASS" and len(runtime["Results"]) == 12 and all(r["Status"] == "PASS" for r in runtime["Results"]), "Recorded original 12-measure checkpoint; not a new live DAX execution")
    sql = read_json("outputs/validation/sqlserver_validation.json")
    check("historical_sql_evidence", sql["status"] == "PASS" and all(c["status"] == "PASS" for c in sql["checks"]), "Recorded SQL integrity and canonical reconciliation; no SQL rebuild")
    original = git("show", "99b573f:" + MODEL + "/tables/_Measures.tmdl").decode("utf-8-sig")
    current = (ROOT / MODEL / "tables/_Measures.tmdl").read_text(encoding="utf-8-sig")
    original_expressions = re.findall(r"(?m)^\s*measure .+$", original)
    check("original_runtime_measures_unchanged", len(original_expressions) == 12 and all(line.strip() in current for line in original_expressions), "All original 12 expressions match the runtime-approved checkpoint")
    with (ROOT / "outputs/validation/workforce_cross_source_reconciliation.csv").open(encoding="utf-8-sig", newline="") as f:
        workforce_recon = list(csv.DictReader(f))
    check("workforce_cross_source_evidence", len(workforce_recon) == 24 and all(r["Status"] == "PASS" and Decimal(r["CountVariance"]) == 0 for r in workforce_recon), "24/24 recorded PASS, count variance zero")

    screenshot_details = []
    for name, expected_hash in SHOTS.items():
        blob = (ROOT / "screenshots" / name).read_bytes()
        valid = blob.startswith(b"\x89PNG\r\n\x1a\n")
        offset, compressed = 8, b""
        while offset < len(blob):
            size = struct.unpack(">I", blob[offset:offset+4])[0]
            kind, data = blob[offset+4:offset+8], blob[offset+8:offset+8+size]
            crc = struct.unpack(">I", blob[offset+8+size:offset+12+size])[0]
            valid = valid and zlib.crc32(kind + data) & 0xffffffff == crc
            if kind == b"IDAT":
                compressed += data
            offset += 12 + size
        zlib.decompress(compressed)
        sha = hashlib.sha256(blob).hexdigest().upper()
        width, height = struct.unpack(">II", blob[16:24])
        check("screenshot_" + name, valid and sha == expected_hash, {"width": width, "height": height, "sha256": sha})
        screenshot_details.append(name)
    published_png = {Path(p).name for p in files if p.startswith("screenshots/") and p.endswith(".png")}
    check("exact_screenshot_set", published_png == set(SHOTS), sorted(published_png))

    broken = []
    for name in files:
        if not name.endswith(".md"):
            continue
        text = (ROOT / name).read_text(encoding="utf-8-sig")
        for link in re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", text):
            link = unquote(link.split("#", 1)[0].strip("<>"))
            if not link or re.match(r"[a-zA-Z]+:", link):
                continue
            target = (ROOT / name).parent / link
            if not target.exists() and target.resolve() != (ROOT / OUTPUT).resolve():
                broken.append({"file": name, "link": link})
    check("local_markdown_links", not broken, broken)
    syntax_errors = []
    for name in files:
        if name.endswith(".py"):
            try:
                ast.parse((ROOT / name).read_text(encoding="utf-8-sig"), filename=name)
            except SyntaxError as exc:
                syntax_errors.append({"file": name, "line": exc.lineno})
    check("python_syntax", not syntax_errors, syntax_errors)
    check("sql_sources_present", all((ROOT / "sql" / p).is_file() for p in ["00_create_database.sql", "01_create_dimensions_sqlserver.sql", "02_create_facts_sqlserver.sql", "03_constraints_indexes_sqlserver.sql"]), "SQL Server DDL present")
    forbidden = [p for p in files if re.search(r"(^|/)(row_data|\.venv[^/]*|\.vscode|__pycache__|\.pbi|DAXQueries)/|\.(sqlite|pbix|bak|mdf|ldf|log|tmp)$|(^|/)\.env$|localSettings\.json$", p)]
    check("publication_exclusions", not forbidden, forbidden)
    large = [p for p in files if (ROOT / p).is_file() and (ROOT / p).stat().st_size > 10 * 1024 * 1024]
    check("no_large_payloads", not large, large)
    patterns = {
        "access_token": rb"(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,}|AKIA[A-Z0-9]{16})",
        "private_key": rb"-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----",
        "credential_assignment": rb"(?i)(?:password|passwd|pwd|api_key|access_token)\s*[=:]\s*[\x22\x27]?[^\s\x22\x27;,#}{]{8,}",
    }
    secret_hits = []
    for name in files:
        if name.endswith(".png"):
            continue
        blob = (ROOT / name).read_bytes()
        if name.endswith(".xlsx"):
            with zipfile.ZipFile(io.BytesIO(blob)) as archive:
                blob = b"\n".join(archive.read(n) for n in archive.namelist() if n.endswith(".xml"))
        for label, pattern in patterns.items():
            if re.search(pattern, blob):
                secret_hits.append({"file": name, "pattern": label})
    check("credential_pattern_scan", not secret_hits, secret_hits)
    result = {
        "status": "PASS" if all(c["status"] == "PASS" for c in checks) else "FAIL",
        "analytical_baseline": BASELINE,
        "scope": "Offline publication checks; historical SQL/DAX evidence is not a new live execution",
        "checks": checks,
    }
    (ROOT / OUTPUT).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "checks": len(checks), "failures": [c for c in checks if c["status"] == "FAIL"]}, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
