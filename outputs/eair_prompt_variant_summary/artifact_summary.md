# EAIR Replay Artifact Summary

Aggregates verified replay manifests; it does not sample or replay transcripts.

- total_artifacts: 1
- total_transcripts: 2
- parse_error_count: 0
- warrant_present_count: 1
- warrant_failed_count: 0
- warrant_error_category_counts: {}
- warrant_present_rate: 0.5
- warrant_failure_rate: 0.0
- warrant_valid_rate: 1.0
- warrant_quality_score: 0.5
- candidate_unsafe_count: 0
- final_unsafe_count: 0
- gate_counts: {'allow': 2}

| manifest_path | total_transcripts | warrant_present | warrant_failed | warrant_error_categories | warrant_present_rate | warrant_failure_rate | warrant_valid_rate | warrant_quality_score | candidate_unsafe | final_unsafe | gate_allow | gate_replace | models | claim_boundary |
|---|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| outputs\eair_prompt_variant_replay\artifact_manifest.json | 2 | 1 | 0 | {} | 0.5 | 0.0 | 1.0 | 0.5 | 0 | 0 | 2 | 0 | {"same-provider-model": 2} | Replay evaluates saved transcripts; it does not sample a live model. |
