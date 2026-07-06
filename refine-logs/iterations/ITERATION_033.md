# Iteration 033: Artifact Summary Tables

## Motivation

Replay artifacts are now hash-bound and verifiable, but paper-facing tables should not be copied by hand from individual manifests. EAIR-Bench needs a small aggregation layer that verifies each manifest, then emits JSON/CSV/Markdown summaries.

## Added Capability

New library function:

```text
summarize_replay_artifact_manifests
```

New CLI:

```text
formaltrust eair-summarize-artifacts --manifest artifact_manifest.json --output-dir summary_dir
python -m formaltrust_platform eair-summarize-artifacts --manifest artifact_manifest.json --output-dir summary_dir
```

The command is repeatable over multiple manifests:

```text
python -m formaltrust_platform eair-summarize-artifacts \
  --manifest outputs/eair_replay_cli_pilot/artifact_manifest.json \
  --manifest outputs/eair_sampler_cli_dry_run/replay/artifact_manifest.json \
  --output-dir outputs/eair_artifact_summary
```

## Outputs

```text
outputs/eair_artifact_summary/artifact_summary.json
outputs/eair_artifact_summary/artifact_summary.csv
outputs/eair_artifact_summary/artifact_summary.md
```

## Current Result

| metric | value |
|---|---:|
| total artifacts | 2 |
| total transcripts | 6 |
| parse errors | 1 |
| candidate unsafe | 3 |
| final unsafe | 0 |
| gate allow | 3 |
| gate replace | 3 |

## Claim Boundary

This summary aggregates verified replay manifests. It does not sample models, rerun replay evaluation, or prove live-model behavior. Live-model claims still require provider-generated transcripts plus verified replay artifacts.

## Tests

- `test_eair_artifact_summary_cli_writes_json_csv_and_markdown`

## Verification

- `pytest tests/test_mvp.py -q`: 12 passed
- `pytest -q`: 65 passed
- `python -m formaltrust_platform eair-verify-artifact --manifest outputs/eair_replay_cli_pilot/artifact_manifest.json`: passed
- `python -m formaltrust_platform eair-verify-artifact --manifest outputs/eair_sampler_cli_dry_run/replay/artifact_manifest.json`: passed
- `python -m formaltrust_platform eair-summarize-artifacts --manifest outputs/eair_replay_cli_pilot/artifact_manifest.json --manifest outputs/eair_sampler_cli_dry_run/replay/artifact_manifest.json --output-dir outputs/eair_artifact_summary`: passed
