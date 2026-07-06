# Live Prompt-Matrix Readiness Design

Date: 2026-06-21

## Problem

The deterministic prompt-protocol matrix has a clear shape, but the live readiness checker only reported condition coverage. Before using a provider, the preflight artifacts should state the full planned sampling scale:

```text
scenarios x prompt_variants = planned transcripts
```

## Design

Extend live readiness, doctor, and workflow-status artifacts with:

- `scenario_count`
- `prompt_variants`
- `prompt_variant_count`
- `planned_transcript_count`

The checker remains static and does not query a provider. The doctor still checks runtime secret availability without recording the secret value. Workflow status carries the same matrix metadata so a blocked live run still records what experiment was planned.

## Outputs

```text
examples/eair_prompt_protocol_matrix_live_template.yaml
outputs/eair_prompt_protocol_matrix_live/live_preflight/
outputs/eair_prompt_protocol_matrix_live/workflow_status/
```

## Boundary

This iteration proves live-run readiness accounting, not live-model behavior.

