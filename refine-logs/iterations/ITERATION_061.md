# Iteration 061: Protocol-Legitimacy Table

Date: 2026-06-21

## Motivation

Iteration 060 separated prompt adherence from WarrantGuard legitimacy. This iteration creates a paper-facing table that puts both metrics on the same row.

## Implemented

- Added `eair-export-protocol-legitimacy-table`.
- Added JSON/CSV/Markdown outputs:
  - `protocol_legitimacy_table.json`
  - `protocol_legitimacy_table.csv`
  - `protocol_legitimacy_table.md`
- Joined prompt adherence and WarrantGuard metrics by:
  - model;
  - prompt variant;
  - condition.
- Added `adherence_legitimacy_gap`.
- Updated the live prompt-matrix runbook to include protocol-legitimacy export as an explicit step.

## Verification

Red check:

```text
pytest tests/test_mvp.py::test_eair_protocol_legitimacy_export_joins_adherence_and_warrant_quality -q
1 failed
```

Green checks so far:

```text
pytest tests/test_mvp.py::test_eair_protocol_legitimacy_export_joins_adherence_and_warrant_quality -q
1 passed

pytest tests/test_mvp.py -k "protocol_legitimacy or prompt_adherence or reportable or artifact_summary" -q
12 passed, 23 deselected

pytest -q
92 passed
```

Export command:

```text
python -m formaltrust_platform eair-export-protocol-legitimacy-table --adherence outputs/eair_prompt_protocol_matrix_dry_run/prompt_adherence/prompt_adherence_audit.json --summary outputs/eair_prompt_protocol_matrix_dry_run/summary/artifact_summary.json --output-dir outputs/eair_prompt_protocol_matrix_dry_run/protocol_legitimacy
```

Readback:

```text
table_artifact_type=eair_protocol_legitimacy_table
table_rows=9
hijack_adherence=1.0
hijack_quality=0.0
hijack_gap=1.0
runbook_command_count=9
runbook_has_protocol_table=True
protocol_table_exists=True
protocol_csv_exists=True
protocol_md_exists=True
```

## Interpretation

The table makes the core WarrantGuard distinction paper-visible: a model can follow the requested proof-carrying protocol while still failing evidence/action legitimacy.
