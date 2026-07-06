# Iteration 038: Complete Dry-Run Coverage Fixture

## Motivation

Iteration 037 proved the failure path for `--require-complete-coverage`. The workflow also needs a passing fixture so the coverage gate can be tested end-to-end before running live providers.

## Added Artifact

```text
examples/eair_sampler_complete_dry_run.yaml
```

It covers the current expected condition set:

```text
approval_bypass::clean_sufficient_evidence
approval_bypass::risk_report_downgrade_no_tool
parameter_setting::parameter_level_hijack
policy_update::legitimate_evidence_update
```

## Generated Outputs

```text
outputs/eair_sampler_complete_dry_run/sampled_transcripts.jsonl
outputs/eair_sampler_complete_dry_run/replay/artifact_manifest.json
outputs/eair_sampler_complete_dry_run/summary/artifact_summary.json
outputs/eair_sampler_complete_dry_run/summary/artifact_summary_coverage.md
outputs/eair_sampler_complete_dry_run/summary/artifact_summary_by_model_condition.csv
```

## Current Result

| metric | value |
|---|---:|
| total transcripts | 4 |
| candidate unsafe | 2 |
| final unsafe | 0 |
| gate allow | 2 |
| gate replace | 2 |
| coverage complete | true |
| coverage rate | 1.0000 |

## Claim Boundary

This is a deterministic dry-run fixture. It proves the sampling -> replay -> manifest -> summary -> coverage-gate protocol can pass on complete coverage. It does not prove live-model behavior.

## Tests

- `test_complete_dry_run_sampler_fixture_passes_coverage_gate`

## Verification

- `pytest -q`: 68 passed
- `python -m formaltrust_platform eair-sample --config examples/eair_sampler_complete_dry_run.yaml`: passed
- `python -m formaltrust_platform eair-summarize-artifacts --manifest outputs/eair_sampler_complete_dry_run/replay/artifact_manifest.json --expected-condition approval_bypass::clean_sufficient_evidence --expected-condition approval_bypass::risk_report_downgrade_no_tool --expected-condition parameter_setting::parameter_level_hijack --expected-condition policy_update::legitimate_evidence_update --require-complete-coverage --output-dir outputs/eair_sampler_complete_dry_run/summary`: passed
- JSON readback confirmed:
  - total transcripts: 4
  - candidate unsafe: 2
  - final unsafe: 0
  - gate counts: allow 2 / replace 2
  - coverage complete: true
  - coverage rate: 1.0
