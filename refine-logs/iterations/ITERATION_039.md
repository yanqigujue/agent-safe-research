# Iteration 039: Live Provider Readiness Check

## Motivation

Before running a live provider, the sampler config should be checked for secret handling, replay artifact paths, expected coverage, and accidental dry-run settings. Otherwise a model call can be expensive but unusable for paper evidence.

## Added Capability

New CLI:

```text
formaltrust eair-check-live-config --config examples/eair_sampler_live_template.yaml
python -m formaltrust_platform eair-check-live-config --config examples/eair_sampler_live_template.yaml
```

The check verifies:

- `api_key_env` exists;
- inline `api_key` is not present;
- `dry_run_responses` is not present;
- `base_url`, `model`, `output_path`, and `replay_output_dir` exist;
- `expected_conditions` exists;
- scenarios cover expected conditions;
- a coverage-gate command can be constructed.

## Updated Template

```text
examples/eair_sampler_live_template.yaml
```

now includes:

- 4 expected conditions;
- matching scenarios;
- `summary_output_dir`;
- no inline secret.

## Current Result

Passing check:

```text
Live config ready: examples\eair_sampler_live_template.yaml
model: gpt-4.1-mini
api_key_env: OPENAI_API_KEY
expected_conditions: 4
coverage gate command: formaltrust eair-summarize-artifacts ...
```

Failure check on a bad config reports:

```text
api_key_env is required for live sampling
inline api_key is not allowed for live sampling
dry_run_responses is not allowed for live sampling
missing expected conditions: [...]
```

## Claim Boundary

This check validates live-run configuration readiness. It does not call a provider, sample a model, or prove model behavior.

## Tests

- `test_eair_live_config_checker_accepts_live_template`
- `test_eair_live_config_checker_rejects_inline_secret_and_incomplete_coverage`

## Verification

- `pytest -q`: 70 passed
- `python -m formaltrust_platform eair-check-live-config --config examples/eair_sampler_live_template.yaml`: passed
- readiness output reported:
  - model `gpt-4.1-mini`
  - api key env `OPENAI_API_KEY`
  - expected conditions `4`
  - resolved coverage gate command
- bad-config smoke check failed as expected for:
  - missing `api_key_env`
  - inline `api_key`
  - `dry_run_responses`
  - missing expected condition
