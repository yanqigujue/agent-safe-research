# Prompt-Protocol Matrix Plan

Date: 2026-06-21

## Checklist

- [x] Add failing test for sampler-driven summary generation.
- [x] Verify the test fails before implementation.
- [x] Make `summary_output_dir` trigger artifact summary generation after replay.
- [x] Support config-level `expected_conditions` and `require_complete_coverage`.
- [x] Print `Summary report:` from the CLI.
- [x] Add a 3-condition x 3-prompt deterministic matrix fixture.
- [x] Run the fixture and inspect JSON/CSV outputs.
- [x] Run full pytest before final reporting.

## Commands

```text
pytest tests/test_mvp.py::test_eair_sampler_cli_writes_multi_condition_prompt_matrix_summary -q
pytest tests/test_mvp.py -k "eair_sampler_cli or prompt_variant or artifact_summary" -q
python -m formaltrust_platform eair-sample --config examples/eair_prompt_protocol_matrix_dry_run.yaml
pytest -q
```

## Final Verification

```text
88 passed
summary_exists=True
matrix_exists=True
leaderboard_exists=True
coverage_complete=True
total_transcripts=9
warrant_quality_score=0.4444
rows_in_matrix_csv=9
```
