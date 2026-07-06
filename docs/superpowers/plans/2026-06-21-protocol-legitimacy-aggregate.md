# Protocol-Legitimacy Aggregate Plan

## Acceptance Criteria

- Extend the existing protocol-legitimacy export instead of adding a new command.
- Write JSON/CSV/Markdown aggregate artifacts by `prompt_variant`.
- Add tests that fail before implementation.
- Regenerate the deterministic prompt-protocol matrix artifacts.
- Update the live runbook required artifact list.
- Document that the aggregate is a prompt-ablation table, not live-model evidence.

## Verification Commands

```powershell
pytest tests/test_mvp.py::test_eair_protocol_legitimacy_export_joins_adherence_and_warrant_quality -q
pytest tests/test_mvp.py::test_eair_protocol_legitimacy_export_joins_adherence_and_warrant_quality tests/test_mvp.py::test_eair_live_runbook_command_writes_prompt_matrix_json_sidecar -q
python -m formaltrust_platform eair-export-protocol-legitimacy-table --adherence outputs/eair_prompt_protocol_matrix_dry_run/prompt_adherence/prompt_adherence_audit.json --summary outputs/eair_prompt_protocol_matrix_dry_run/summary/artifact_summary.json --output-dir outputs/eair_prompt_protocol_matrix_dry_run/protocol_legitimacy
python -m formaltrust_platform eair-write-live-runbook --config examples/eair_prompt_protocol_matrix_live_template.yaml --output outputs/eair_prompt_protocol_matrix_live/RUN_LIVE_PROMPT_MATRIX.md
pytest -q
```

## Readback Targets

```text
artifact_type=eair_protocol_legitimacy_by_prompt_variant
total_rows=3
legacy_action_only: quality=0.0, gap=1.0
proof_carrying: quality=0.6667, gap=0.3333
proof_carrying_strict: quality=0.6667, gap=0.3333
```
