# Power BI Baseline Validation

## Result

**PASS — read-only baseline inventory complete.**

The PBIP contains the approved SQL Server tables and expected star-schema
relationship topology. The current model has 14 active single-direction
dimension-to-fact relationships and no fact-to-fact or many-to-many joins.

## Structural checks

| Check | Result |
|---|---|
| PBIP, PBIR and TMDL files readable | PASS |
| Approved business tables present | 9 / 9 |
| Hidden tables | 0 |
| Relationships | 14 |
| Many-to-many relationships | 0 |
| Bidirectional relationships | 0 |
| Inactive relationships | 0 |
| Fact-to-fact relationships | 0 |
| Auto Date/Time / LocalDateTable | None |
| SQL Server Import partitions | 9 / 9 |
| Measures | 0 |
| Pages | 1 |
| Visuals | 0 |

## Validation limitation

This checkpoint is file-level discovery only. Power BI Desktop was not opened,
and no model refresh or visual rendering was performed. Cardinality and
cross-filter settings are not explicitly serialized in the relationship TMDL,
so their default interpretation should be confirmed during semantic-model
hardening.

## Next checkpoint

Semantic model hardening only: relationships, date/year behavior, technical
key visibility, sorting, and summarization safety. Do not add measures yet.
