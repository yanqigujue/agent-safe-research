# Multi-Prompt Sampler Plan

Date: 2026-06-21

## Scope

Implement a deterministic multi-prompt dry-run sampler for WarrantGuard experiments.

## Checklist

- [x] Add a failing CLI test for `prompt_variants`.
- [x] Verify the test fails before implementation.
- [x] Expand sampler scenarios across prompt variants.
- [x] Preserve `prompt_variant` in transcript rows.
- [x] Inject variant instructions into the prompt.
- [x] Wrap mapping dry-run responses into OpenAI-compatible response shape.
- [x] Keep explicit transcript IDs unique under prompt expansion.
- [x] Add an example config.
- [x] Run sampler, replay, and summary on the deterministic fixture.
- [x] Run full pytest before final reporting.

## Commands

```text
pytest tests/test_mvp.py::test_eair_sampler_cli_expands_prompt_variants_for_dry_run -q
python -m formaltrust_platform eair-sample --config examples/eair_multi_prompt_sampler_dry_run.yaml
python -m formaltrust_platform eair-summarize-artifacts --manifest outputs/eair_multi_prompt_sampler_dry_run/replay/artifact_manifest.json --expected-condition approval_bypass::clean_sufficient_evidence --require-complete-coverage --output-dir outputs/eair_multi_prompt_sampler_dry_run/summary
pytest -q
```

## Final Verification

```text
87 passed
```
