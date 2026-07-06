# EAIR Live Workflow Status

| field | value |
|---|---|
| overall_status | blocked |
| blocked_stage | live_preflight |
| model | gpt-4.1-mini |
| api_key_env_present | false |
| secret_value_recorded | false |

## Stages

| stage | passed | artifact | errors |
|---|---|---|---|
| live_preflight | false | C:\Users\wang\Documents\agent-safe-research\outputs\eair_live_model_run\live_preflight\live_run_doctor.json | environment variable 'OPENAI_API_KEY' is not set |
| sampling | false | C:\Users\wang\Documents\agent-safe-research\outputs\eair_live_model_run\sampled_transcripts.jsonl | missing artifact: C:\Users\wang\Documents\agent-safe-research\outputs\eair_live_model_run\sampled_transcripts.jsonl |
| replay_manifest | false | C:\Users\wang\Documents\agent-safe-research\outputs\eair_live_model_run\replay\artifact_manifest.json | missing artifact: C:\Users\wang\Documents\agent-safe-research\outputs\eair_live_model_run\replay\artifact_manifest.json |
| coverage_summary | false | C:\Users\wang\Documents\agent-safe-research\outputs\eair_live_model_run\summary\artifact_summary.json | missing artifact: C:\Users\wang\Documents\agent-safe-research\outputs\eair_live_model_run\summary\artifact_summary.json |
| reportability | false | C:\Users\wang\Documents\agent-safe-research\outputs\eair_live_model_run\reportability\reportable_run_audit.json | missing artifact: C:\Users\wang\Documents\agent-safe-research\outputs\eair_live_model_run\reportability\reportable_run_audit.json |
| paper_table_export | false | C:\Users\wang\Documents\agent-safe-research\outputs\eair_live_model_run\paper_tables\reportable_model_condition_table.csv | missing artifact: C:\Users\wang\Documents\agent-safe-research\outputs\eair_live_model_run\paper_tables\reportable_model_condition_table.csv |
