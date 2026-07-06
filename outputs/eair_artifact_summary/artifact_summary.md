# EAIR Replay Artifact Summary

Aggregates verified replay manifests; it does not sample or replay transcripts.

- total_artifacts: 2
- total_transcripts: 6
- parse_error_count: 1
- candidate_unsafe_count: 3
- final_unsafe_count: 0
- gate_counts: {'allow': 3, 'replace': 3}

| manifest_path | total_transcripts | candidate_unsafe | final_unsafe | gate_allow | gate_replace | models | claim_boundary |
|---|---:|---:|---:|---:|---:|---|---|
| outputs\eair_replay_cli_pilot\artifact_manifest.json | 4 | 2 | 0 | 2 | 2 | {"replay-fixture": 4} | Replay evaluates saved transcripts; it does not sample a live model. |
| outputs\eair_sampler_cli_dry_run\replay\artifact_manifest.json | 2 | 1 | 0 | 1 | 1 | {"cli-dry-run-openai-compatible": 2} | Replay evaluates saved transcripts; it does not sample a live model. |
