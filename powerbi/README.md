# Power BI project

## Opening the project

If you download the repository with GitHub's **Download ZIP**, extract the archive completely before opening `SaudiHealthcareAnalytics.pbip`. Power BI Project files depend on the adjacent `SaudiHealthcareAnalytics.Report` and `SaudiHealthcareAnalytics.SemanticModel` folders and will fail if opened from inside the compressed ZIP.

Open [SaudiHealthcareAnalytics.pbip](SaudiHealthcareAnalytics.pbip) in Power BI Desktop with PBIP/PBIR/TMDL support. The report is in `SaudiHealthcareAnalytics.Report/`; the model is in `SaudiHealthcareAnalytics.SemanticModel/`.

## Connection and refresh

| Setting | Value |
|---|---|
| Server | `localhost` |
| Database | `SaudiHealthcareAnalytics` |
| Authentication | Windows Authentication |
| Storage | Import |
| Schema | `analytics` |

Build and validate SQL using the [SQL guide](../sql/README.md). In Desktop, configure Windows credentials and refresh. Local caches and credentials are excluded, so a fresh clone must refresh to populate its model. There is no published Power BI service URL.

Imported tables: `DimYear`, `DimGeography`, `DimSector`, `DimWorkforceType`, `DimNationality`, `FactCapacity`, `FactActivity`, `FactWorkforceSector`, `FactWorkforceNationality`. Disconnected `_Measures` makes **ten semantic tables**. All 14 relationships are active M:1 with dimension-to-fact single-direction filtering. Auto Date/Time is disabled.

## Report state

INDEX is the opening page. Executive Overview retains the approved 2024 Year selection; its trends retain full history. Six HOME buttons return to INDEX. The [gallery](../screenshots/README.md) contains all seven approved pages as unaltered captures.

## Measures and validation scope

The model contains 15 measures: 12 original governed KPIs, `First Aid Centers`, `Ambulances`, and the text helper `Ambulances Card`. Original runtime evidence records 12/12 PASS at `99b573f`; later additions were included in the approved Red Crescent checkpoint `cae3706`.

Old DAX runtime/static scripts assert an earlier 12-measure, one-page model. Their results are historical, not final-report tests. Use `python scripts/validate_release.py` for current offline publication checks; this does not refresh SQL or execute live DAX. [Final evidence record](../docs/validation/FINAL_RELEASE_VALIDATION.md).
