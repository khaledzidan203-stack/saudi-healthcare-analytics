# Presentation Assets

This directory contains presentation-only visual assets for the Saudi Healthcare Analytics project.

## Current overview

`Saudi Healthcare Analytics Pipeline.png`

This is the evidence-aligned project overview used by the main README. It summarizes the implemented analytical path from official Saudi MOH Statistical Yearbooks through discovery and profiling, governed canonical contracts, SQL Server analytics, Power BI semantic modeling, reporting, and validation.

The current image intentionally reflects the validated release boundary:

- 2021–2024 official Saudi MOH statistical yearbooks;
- aggregate public statistics only;
- annual analytical grain;
- National + Administrative Region scope, with Health Region / Health Cluster kept separate from the core geography contract;
- 9 canonical tables: 4 facts + 5 dimensions;
- 10 semantic tables and 14 active single-direction relationships;
- 15 current measures;
- 7 report pages and 121 saved visuals;
- original governed DAX runtime checks: 12 / 12 PASS;
- FY006 ↔ FY008 workforce reconciliation: 24 / 24 PASS;
- canonical ↔ SQL reconciliation and release audit PASS;
- no patient-level data.

Presentation assets are not analytical source data, validation evidence, Power BI screenshots, or replacements for governed contracts and release records. Authoritative claims remain defined by the repository contracts, canonical data, SQL/Power BI sources, screenshots, and validation evidence.

See [`../PROJECT_EVIDENCE_MAP.md`](../PROJECT_EVIDENCE_MAP.md) for evidence mapping.
