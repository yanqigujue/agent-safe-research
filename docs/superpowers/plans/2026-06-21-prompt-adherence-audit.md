# Prompt Adherence Audit Plan

Date: 2026-06-21

## Checklist

- [x] Add failing test for prompt adherence CLI.
- [x] Verify the test fails before implementation.
- [x] Implement transcript-level prompt protocol audit.
- [x] Write JSON/CSV/Markdown outputs.
- [x] Add CLI command.
- [x] Run audit on the prompt-protocol matrix fixture.
- [x] Run full pytest before final reporting.

## Commands

```text
pytest tests/test_mvp.py::test_eair_prompt_adherence_audit_flags_missing_warrant_for_proof_prompt -q
pytest tests/test_mvp.py -k "prompt_adherence or prompt_variant or eair_sampler_cli or artifact_summary" -q
python -m formaltrust_platform eair-audit-prompt-adherence --transcripts outputs/eair_prompt_protocol_matrix_dry_run/sampled_transcripts.jsonl --output-dir outputs/eair_prompt_protocol_matrix_dry_run/prompt_adherence
pytest -q
```

## Final Verification

```text
91 passed
audit_exists=True
csv_exists=True
md_exists=True
artifact_type=eair_prompt_protocol_adherence_audit
total_transcripts=9
compliance_rate=1.0
warrant_quality_score=0.4444
runbook_command_count=9
runbook_has_prompt_adherence=True
```
