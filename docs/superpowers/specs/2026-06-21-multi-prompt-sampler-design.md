# Multi-Prompt Sampler Design

Date: 2026-06-21

## Problem

The prompt-variant leaderboard can rank replayed artifacts, but the sampler still treated a run as one prompt per scenario. That made the comparison surface depend on hand-written transcript fixtures.

## Design

Extend the OpenAI-compatible action sampler with `prompt_variants`.

Each scenario is expanded as:

```text
scenario x prompt_variant -> sampled transcript
```

Each sampled transcript preserves:

- `prompt_variant`
- variant-specific prompt instruction
- unique `transcript_id`
- raw response
- parsed replay result through the existing structured-action replay pipeline

Dry-run responses may be either full OpenAI-compatible payloads or direct model-output payloads. Direct mappings are wrapped into a chat-completion-shaped response so deterministic fixtures can express proof-carrying actions without boilerplate.

## Success Criteria

- A single scenario with three prompt variants produces three transcript rows.
- Replay preserves `prompt_variant_counts`.
- Artifact summary leaderboard ranks proof-carrying variants above action-only variants in the deterministic smoke test.
- Explicit scenario `transcript_id` values remain unique after prompt expansion.

