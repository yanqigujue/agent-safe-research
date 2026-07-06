# EAIR Replay Artifact Summary

Aggregates verified replay manifests; it does not sample or replay transcripts.

- total_artifacts: 1
- total_transcripts: 6
- parse_error_count: 1
- warrant_present_count: 2
- warrant_failed_count: 1
- warrant_error_category_counts: {'decision_support': 1}
- warrant_present_rate: 0.3333
- warrant_failure_rate: 0.5
- warrant_valid_rate: 0.5
- warrant_quality_score: 0.1667
- candidate_unsafe_count: 2
- final_unsafe_count: 0
- gate_counts: {'allow': 3, 'block': 1, 'replace': 2}

| manifest_path | total_transcripts | warrant_present | warrant_failed | warrant_error_categories | warrant_present_rate | warrant_failure_rate | warrant_valid_rate | warrant_quality_score | candidate_unsafe | final_unsafe | gate_allow | gate_replace | models | claim_boundary |
|---|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| outputs\eair_transcript_replay_pilot\artifact_manifest.json | 6 | 2 | 1 | {"decision_support": 1} | 0.3333 | 0.5 | 0.5 | 0.1667 | 2 | 0 | 3 | 2 | {"replay-fixture": 4, "warrant-fixture": 2} | Replay evaluates saved transcripts; it does not sample a live model. |
