# Iteration 062: Protocol-Legitimacy Prompt Aggregate

## Goal

Turn the condition-level protocol-legitimacy table into a paper-facing prompt-ablation artifact.

## Added Artifacts

```text
outputs/eair_prompt_protocol_matrix_dry_run/protocol_legitimacy/protocol_legitimacy_by_prompt_variant.json
outputs/eair_prompt_protocol_matrix_dry_run/protocol_legitimacy/protocol_legitimacy_by_prompt_variant.csv
outputs/eair_prompt_protocol_matrix_dry_run/protocol_legitimacy/protocol_legitimacy_by_prompt_variant.md
```

## Readback

```text
artifact_type=eair_protocol_legitimacy_by_prompt_variant
total_rows=3
legacy_action_only transcripts=3 adherence=1.0 quality=0.0 gap=1.0 high_gap=3 errors={}
proof_carrying transcripts=3 adherence=1.0 quality=0.6667 gap=0.3333 high_gap=1 errors={"decision_support": 1, "hard_gate": 1}
proof_carrying_strict transcripts=3 adherence=1.0 quality=0.6667 gap=0.3333 high_gap=1 errors={"decision_support": 1, "hard_gate": 1}
```

## Interpretation

The aggregate supports a cleaner paper table: action-only output can fully obey its prompt protocol while carrying no evidence warrant, and proof-carrying output can improve WarrantGuard quality while still failing on parameter hijack.

## Boundary

This is deterministic pilot evidence. It is not live-provider behavior evidence.

## Verification

```text
pytest tests/test_mvp.py::test_eair_protocol_legitimacy_export_joins_adherence_and_warrant_quality -q
1 passed

pytest tests/test_mvp.py::test_eair_protocol_legitimacy_export_joins_adherence_and_warrant_quality tests/test_mvp.py::test_eair_live_runbook_command_writes_prompt_matrix_json_sidecar -q
2 passed

pytest tests/test_mvp.py -k "protocol_legitimacy or prompt_adherence or reportable or artifact_summary" -q
12 passed, 23 deselected

pytest -q
92 passed
```

Final artifact readback:

```text
all_protocol_artifacts_exist=True
aggregate_rows=3
runbook_command_count=9
has_aggregate_required=True
```
