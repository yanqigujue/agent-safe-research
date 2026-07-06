# Iteration 056: Multi-Prompt Dry-Run Sampler

Date: 2026-06-21

## Motivation

Iteration 055 made WarrantGuard reporting prompt-variant aware, but it still relied on fixture transcripts. This iteration moves one step closer to live prompt ablations by letting the sampler generate multiple prompt variants for the same scenario.

## Implemented

- Added `prompt_variants` support to `eair-sample`.
- Expanded each configured scenario across prompt variants.
- Preserved `prompt_variant` in sampled transcript rows.
- Added prompt-variant headers and instructions to the model prompt.
- Allowed mapping-style dry-run responses to be wrapped as OpenAI-compatible chat completions.
- Kept explicit scenario transcript IDs unique by appending the prompt variant when expansion is active.
- Added `examples/eair_multi_prompt_sampler_dry_run.yaml`.
- Generated deterministic artifacts under `outputs/eair_multi_prompt_sampler_dry_run`.

## Verification

Red check:

```text
pytest tests/test_mvp.py::test_eair_sampler_cli_expands_prompt_variants_for_dry_run -q
1 failed
```

Green checks:

```text
pytest tests/test_mvp.py::test_eair_sampler_cli_expands_prompt_variants_for_dry_run -q
1 passed

pytest tests/test_mvp.py -k "eair_sampler_cli or prompt_variant or artifact_summary" -q
7 passed, 23 deselected

pytest tests/test_eair_bench.py -k "openai_compatible_sampler or structured_action_transcript" -q
3 passed, 42 deselected

pytest -q
87 passed
```

Artifact readback:

```text
transcript_variants=['legacy_action_only', 'proof_carrying', 'proof_carrying_strict']
replay_prompt_variant_counts={'legacy_action_only': 1, 'proof_carrying': 1, 'proof_carrying_strict': 1}
summary_coverage_complete=True
leaderboard_variants=['proof_carrying', 'proof_carrying_strict', 'legacy_action_only']
leaderboard_scores=[1.0, 1.0, 0.0]
prompt_instruction_present=True
```

## Interpretation

This iteration supports deterministic multi-prompt ablation mechanics. It does not yet support a claim that any live model or prompt is robust; that requires reportable live-provider runs with declared coverage.
