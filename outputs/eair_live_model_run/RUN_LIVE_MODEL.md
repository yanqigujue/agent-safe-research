# EAIR Live Model Runbook

This runbook records the command sequence for collecting live provider transcripts and turning them into verified replay artifacts.

## Claim Boundary

Do not cite sampler logs as safety evidence. Cite saved transcript JSONL, replay artifacts, verified manifests, and coverage-gated summaries.

## Config

- config: examples/eair_sampler_live_template.yaml
- model: gpt-4.1-mini
- api_key_env: OPENAI_API_KEY
- transcript_output: C:\Users\wang\Documents\agent-safe-research\outputs\eair_live_model_run\sampled_transcripts.jsonl
- replay_output_dir: C:\Users\wang\Documents\agent-safe-research\outputs\eair_live_model_run\replay
- summary_output_dir: C:\Users\wang\Documents\agent-safe-research\outputs\eair_live_model_run\summary

## Expected Conditions

- approval_bypass::clean_sufficient_evidence
- approval_bypass::risk_report_downgrade_no_tool
- parameter_setting::parameter_level_hijack
- policy_update::legitimate_evidence_update

## Commands

1. Run live preflight doctor.

```powershell
formaltrust eair-doctor-live-run --config examples/eair_sampler_live_template.yaml --output-dir C:\Users\wang\Documents\agent-safe-research\outputs\eair_live_model_run\live_preflight
```

2. Check live config readiness.

```powershell
formaltrust eair-check-live-config --config examples/eair_sampler_live_template.yaml
```

3. Run provider sampling and deterministic replay.

```powershell
formaltrust eair-sample --config examples/eair_sampler_live_template.yaml
```

4. Verify the replay artifact manifest.

```powershell
formaltrust eair-verify-artifact --manifest C:\Users\wang\Documents\agent-safe-research\outputs\eair_live_model_run\replay\artifact_manifest.json
```

5. Generate coverage-gated summary tables.

```powershell
formaltrust eair-summarize-artifacts --manifest C:\Users\wang\Documents\agent-safe-research\outputs\eair_live_model_run\replay\artifact_manifest.json --expected-condition approval_bypass::clean_sufficient_evidence --expected-condition approval_bypass::risk_report_downgrade_no_tool --expected-condition parameter_setting::parameter_level_hijack --expected-condition policy_update::legitimate_evidence_update --require-complete-coverage --output-dir C:\Users\wang\Documents\agent-safe-research\outputs\eair_live_model_run\summary
```

6. Audit whether the run is reportable as live-provider evidence.

```powershell
formaltrust eair-audit-reportable-run --manifest C:\Users\wang\Documents\agent-safe-research\outputs\eair_live_model_run\replay\artifact_manifest.json --summary C:\Users\wang\Documents\agent-safe-research\outputs\eair_live_model_run\summary\artifact_summary.json --output-dir C:\Users\wang\Documents\agent-safe-research\outputs\eair_live_model_run\reportability
```

7. Export paper-facing model-condition tables only after reportability passes.

```powershell
formaltrust eair-export-reportable-results --summary C:\Users\wang\Documents\agent-safe-research\outputs\eair_live_model_run\summary\artifact_summary.json --audit C:\Users\wang\Documents\agent-safe-research\outputs\eair_live_model_run\reportability\reportable_run_audit.json --output-dir C:\Users\wang\Documents\agent-safe-research\outputs\eair_live_model_run\paper_tables
```

## Required Artifacts

- transcript JSONL
- live preflight doctor JSON/Markdown
- `artifact_manifest.json`
- replay result JSON
- replay report Markdown
- artifact summary JSON/CSV/Markdown
- coverage audit JSON/CSV/Markdown
- reportable-run audit pass
- reportable model-condition paper table
