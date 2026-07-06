# Iteration 060: Prompt Protocol Adherence Audit

Date: 2026-06-21

## Motivation

Iteration 059 made the live prompt-matrix execution path auditable. The next missing layer is post-run protocol adherence: did the model follow the output protocol requested by each prompt variant?

## Implemented

- Added `eair-audit-prompt-adherence`.
- Added JSON/CSV/Markdown prompt adherence outputs.
- The audit checks:
  - action-only prompts do not emit warrants;
  - proof-carrying prompts emit top-level warrants;
  - strict proof-carrying prompts include required warrant fields.
- Generated:
  - `outputs/eair_prompt_protocol_matrix_dry_run/prompt_adherence/prompt_adherence_audit.json`
  - `outputs/eair_prompt_protocol_matrix_dry_run/prompt_adherence/prompt_adherence_audit.csv`
  - `outputs/eair_prompt_protocol_matrix_dry_run/prompt_adherence/prompt_adherence_audit.md`
- Updated the live prompt-matrix runbook to include prompt adherence as an explicit post-sampling step.

## Verification

Red check:

```text
pytest tests/test_mvp.py::test_eair_prompt_adherence_audit_flags_missing_warrant_for_proof_prompt -q
1 failed
```

Green checks so far:

```text
pytest tests/test_mvp.py::test_eair_prompt_adherence_audit_flags_missing_warrant_for_proof_prompt -q
1 passed

pytest tests/test_mvp.py -k "prompt_adherence or prompt_variant or eair_sampler_cli or artifact_summary" -q
9 passed, 25 deselected

pytest -q
91 passed
```

Prompt matrix audit:

```text
python -m formaltrust_platform eair-audit-prompt-adherence --transcripts outputs/eair_prompt_protocol_matrix_dry_run/sampled_transcripts.jsonl --output-dir outputs/eair_prompt_protocol_matrix_dry_run/prompt_adherence
```

Readback:

```text
total_transcripts=9
compliance_rate=1.0
legacy_rate=1.0
proof_rate=1.0
strict_rate=1.0
warrant_quality_score=0.4444
warrant_errors={'decision_support': 2, 'hard_gate': 2}
audit_exists=True
csv_exists=True
md_exists=True
artifact_type=eair_prompt_protocol_adherence_audit
runbook_command_count=9
runbook_has_prompt_adherence=True
```

## Interpretation

The matrix obeys the requested output protocols, but WarrantGuard still rejects invalid parameter-hijack warrants. This cleanly separates protocol adherence from evidence/action legitimacy.
