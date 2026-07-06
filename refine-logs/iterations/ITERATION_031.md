# ITERATION_031: Replay Artifact Manifest

Date: 2026-06-20

## Hypothesis

Replay artifacts should be self-describing and auditable. A paper reviewer or future run should be able to verify which transcript file was evaluated, what its hash was, which outputs were produced, and what claim boundary applies.

## Design Change

Replay output directories now include:

```text
artifact_manifest.json
```

The manifest records:

- artifact type;
- protocol;
- claim boundary;
- transcript path;
- transcript SHA256;
- result/report filenames;
- summary counts;
- model counts.

## Tests

Extended TDD coverage in:

```text
test_eair_replay_cli_evaluates_existing_transcript_jsonl
```

The test now verifies:

- `artifact_manifest.json` exists;
- transcript SHA256 matches the input file;
- manifest summary matches replay results;
- claim boundary explicitly says replay does not sample a live model.

Observed failure before implementation: `artifact_manifest.json` was missing.

## Experiment

Reran:

```text
python -m formaltrust_platform eair-replay \
  --transcripts examples/data/eair_structured_action_transcripts.jsonl \
  --output-dir outputs/eair_replay_cli_pilot
```

Manifest summary:

| field | value |
|---|---|
| artifact_type | `eair_transcript_replay` |
| protocol | `transcript_jsonl_to_eair_replay` |
| transcript_sha256 prefix | `6dbaedb069d3` |
| total transcripts | 4 |
| parse errors | 1 |
| candidate unsafe | 2 |
| final unsafe | 0 |
| gate counts | allow 2 / replace 2 |

## Supported Claim

EAIR-Bench replay artifacts are now auditable at the file level: the transcript input is hash-bound to the result and report artifacts.

## Claim Boundary

The manifest strengthens reproducibility, not benchmark scale. It does not add new model behavior evidence.

## Next Iteration

Add a human-readable artifact README / live-run checklist that points to transcript JSONL, replay report, manifest, and the exact commands used.
