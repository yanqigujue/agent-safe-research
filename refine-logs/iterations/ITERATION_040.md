# Iteration 040: Live Model Runbook

## Motivation

The live config checker says whether a provider run is ready, but a paper-facing experiment still needs a concrete command bundle. The next failure mode is procedural: a researcher can pass readiness, then forget manifest verification or complete-coverage summarization.

## Added Capability

New CLI:

```text
formaltrust eair-write-live-runbook --config examples/eair_sampler_live_template.yaml --output outputs/eair_live_model_run/RUN_LIVE_MODEL.md
python -m formaltrust_platform eair-write-live-runbook --config examples/eair_sampler_live_template.yaml --output outputs/eair_live_model_run/RUN_LIVE_MODEL.md
```

The generated runbook includes:

- live config readiness command;
- provider sampling command;
- replay manifest verification command;
- coverage-gated artifact summary command;
- expected condition list;
- resolved transcript, replay, and summary paths;
- claim boundary for sampler logs.

## Generated Artifact

```text
outputs/eair_live_model_run/RUN_LIVE_MODEL.md
```

The runbook is generated from:

```text
examples/eair_sampler_live_template.yaml
```

## Claim Boundary

The runbook is a live-run protocol artifact, not model-behavior evidence. Do not cite sampler logs as safety evidence. Cite saved transcript JSONL, replay artifacts, verified manifests, and coverage-gated summaries.

## Tests

- `test_eair_live_runbook_command_writes_provider_workflow`

## Verification

- `pytest -q`: 71 passed
- `python -m formaltrust_platform eair-check-live-config --config examples/eair_sampler_live_template.yaml`: passed
- `python -m formaltrust_platform eair-write-live-runbook --config examples/eair_sampler_live_template.yaml --output outputs/eair_live_model_run/RUN_LIVE_MODEL.md`: passed
- targeted TDD test passed: `pytest tests/test_mvp.py::test_eair_live_runbook_command_writes_provider_workflow -q`
- generated runbook contains:
  - `formaltrust eair-check-live-config --config examples/eair_sampler_live_template.yaml`
  - `formaltrust eair-sample --config examples/eair_sampler_live_template.yaml`
  - `formaltrust eair-verify-artifact --manifest ...artifact_manifest.json`
  - `formaltrust eair-summarize-artifacts ... --require-complete-coverage`
  - `Do not cite sampler logs as safety evidence`
