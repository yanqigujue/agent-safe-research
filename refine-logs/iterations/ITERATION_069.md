# Iteration 069: Reportable Child Table Row Integrity

## Goal

Close the post-export child-table tampering loophole.

## Implemented

- Extended `eair-audit-reportable-export` to compare reportable child artifact rows against the main export payload.
- Added `rows_match_export`, `expected_row_count`, and `actual_row_count` to `checked_child_artifacts`.
- Updated the Markdown audit table to show row-match status.
- Added a TDD regression test for child table row tampering.

## Red-Green

Red check:

```text
pytest tests/test_mvp.py::test_eair_audit_reportable_export_detects_child_table_row_mismatch -q
failed because the audit exited 0 when child rows differed
```

Green check:

```text
pytest tests/test_mvp.py::test_eair_audit_reportable_export_detects_child_table_row_mismatch -q
1 passed
```

## Readback

Current fixture audit:

```text
reportable_protocol_legitimacy_table rows_match_export=true
reportable_protocol_legitimacy_by_prompt_variant rows_match_export=true
```

## Boundary

This proves reportable child JSON rows still match the main export. It does not prove live-provider safety behavior.
