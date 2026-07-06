# Iteration 057: Prompt-Protocol Matrix

Date: 2026-06-21

## Motivation

Iteration 056 made the sampler prompt-variant aware for one condition. This iteration turns that into a multi-condition prompt-protocol ablation matrix and makes `eair-sample` produce summary artifacts directly.

## Implemented

- `eair-sample` now honors `summary_output_dir`.
- Config-level `expected_conditions` and `require_complete_coverage` are passed into artifact summarization.
- The CLI prints `Summary report:` when summary artifacts are written.
- Added `examples/eair_prompt_protocol_matrix_dry_run.yaml`.
- Generated `outputs/eair_prompt_protocol_matrix_dry_run`.

## Verification

Red check:

```text
pytest tests/test_mvp.py::test_eair_sampler_cli_writes_multi_condition_prompt_matrix_summary -q
1 failed
```

Green checks so far:

```text
pytest tests/test_mvp.py::test_eair_sampler_cli_writes_multi_condition_prompt_matrix_summary -q
1 passed

pytest tests/test_mvp.py -k "eair_sampler_cli or prompt_variant or artifact_summary" -q
8 passed, 23 deselected

pytest -q
88 passed
```

Experiment command:

```text
python -m formaltrust_platform eair-sample --config examples/eair_prompt_protocol_matrix_dry_run.yaml
```

Readback:

```text
transcript_count=9
coverage_complete=True
warrant_quality_score=0.4444
prompt_variant_counts={'legacy_action_only': 3, 'proof_carrying': 3, 'proof_carrying_strict': 3}
parameter_proof_score=0.0
parameter_strict_score=0.0
warrant_error_category_counts={'decision_support': 2, 'hard_gate': 2}
summary_exists=True
matrix_exists=True
leaderboard_exists=True
rows_in_matrix_csv=9
```

## Interpretation

The matrix supports a sharper claim than the single-condition fixture: proof-carrying prompts can create valid warrants on clean and legitimate-evidence conditions, while still failing under parameter hijack when the warrant is backed by bad evidence or violates hard policy gates. This is exactly the protocol-plus-verifier distinction WarrantGuard needs.
