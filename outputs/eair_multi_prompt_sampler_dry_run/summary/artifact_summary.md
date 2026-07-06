# EAIR Replay Artifact Summary

Aggregates verified replay manifests; it does not sample or replay transcripts.

- total_artifacts: 1
- total_transcripts: 3
- parse_error_count: 0
- warrant_present_count: 2
- warrant_failed_count: 0
- warrant_error_category_counts: {}
- warrant_present_rate: 0.6667
- warrant_failure_rate: 0.0
- warrant_valid_rate: 1.0
- warrant_quality_score: 0.6667
- candidate_unsafe_count: 0
- final_unsafe_count: 0
- gate_counts: {'allow': 3}

| manifest_path | total_transcripts | warrant_present | warrant_failed | warrant_error_categories | warrant_present_rate | warrant_failure_rate | warrant_valid_rate | warrant_quality_score | candidate_unsafe | final_unsafe | gate_allow | gate_replace | models | claim_boundary |
|---|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| outputs\eair_multi_prompt_sampler_dry_run\replay\artifact_manifest.json | 3 | 2 | 0 | {} | 0.6667 | 0.0 | 1.0 | 0.6667 | 0 | 0 | 3 | 0 | {"prompt-variant-dry-run-model": 3} | Replay evaluates saved transcripts; it does not sample a live model. |
