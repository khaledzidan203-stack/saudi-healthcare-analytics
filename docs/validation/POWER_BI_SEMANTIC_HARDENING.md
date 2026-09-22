# Power BI Semantic Hardening Validation

**Result: PASS**

- Tables: 9
- Relationships: 14
- Explicit M:1 relationships: 14
- Active relationships: 14
- Single-direction relationships: 14
- Many-to-many relationships: 0
- Bidirectional relationships: 0
- Inactive relationships: 0
- Fact-to-fact relationships: 0
- Hidden technical columns: 35
- Measures: 0
- Pages: 1
- Visuals: 0
- Auto Date/Time: disabled
- LocalDateTables: 0
- JSON/PBIR parse failures: 0

SQL Server source expressions remain unchanged. The approved year-grain
contract remains unchanged. No DAX, `_Measures` table, report page, visual,
SQL, or KPI definition was added or modified.

The next checkpoint may create exactly one dedicated `_Measures` table and
governed DAX measures.
