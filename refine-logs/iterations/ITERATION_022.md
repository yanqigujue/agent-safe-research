# Iteration 022: Closest-Neighbor Style Baselines

Date: 2026-06-20

## Goal

Turn the Iteration 021 novelty-risk diagnosis into executable evidence by adding style baselines for the closest 2026-era defenses.

## Baselines Added

- `attriguard_selective`
- `causalarmor_dominance`
- `airguard_authority`
- `agent_sentry_provenance`

These are explicitly style baselines, not official reproductions.

## TDD

Red tests were added first for:

- selective AttriGuard-style allowing legitimate evidence while blocking hijack;
- CausalArmor-style dominance blocking untrusted control but missing trusted policy gaps;
- AIRGuard-style authority control blocking hard policy/parameter violations but missing evidence sufficiency;
- Agent-Sentry-style provenance bounds blocking stale/superseded support but missing near-duplicate single-source support;
- pilot report text summarizing the closest-neighbor baselines.

The first run failed because the new baselines were unknown. After implementation, the targeted tests passed.

## Experiment

Reran deterministic EAIR-Bench pilot:

- conditions: 12
- baselines: 17
- results: 204
- outputs: `outputs/eair_bench_pilot/`

Key metrics:

| baseline | UDR | UAR | parameter violation | CUR | EATF | ORR |
|---|---:|---:|---:|---:|---:|---:|
| `attriguard_selective` | 0.0833 | 0.1667 | 0.0833 | 1.0000 | 0.7500 | 0.1667 |
| `causalarmor_dominance` | 0.0833 | 0.2500 | 0.0833 | 1.0000 | 0.6667 | 0.0833 |
| `airguard_authority` | 0.0000 | 0.3333 | 0.0000 | 1.0000 | 0.6667 | 0.0000 |
| `agent_sentry_provenance` | 0.0000 | 0.0833 | 0.0000 | 1.0000 | 0.9167 | 0.2500 |
| `eair_full` | 0.0000 | 0.0000 | 0.0000 | 1.0000 | 1.0000 | 0.3333 |

## Supported

- Authority control is not equivalent to evidence sufficiency.
- Dominance attribution is not equivalent to policy/parameter integrity.
- Provenance currentness is not equivalent to source-diverse support.
- Blanket attribution baselines are too conservative; selective attribution is more realistic but still incomplete.
- EAIR-Full currently covers all targeted synthetic cases but pays a conservative refusal cost.

## Not Yet Supported

- Superiority over official AttriGuard, CausalArmor, AIRGuard, or Agent-Sentry.
- Deployment safety.
- Robustness under real retrievers, real claim extractors, or real LLM planners.

## Next Iteration

The next best move is not more baseline names. It is to reduce `eair_full` over-refusal by distinguishing:

- genuinely insufficient evidence;
- source-diverse but partially noisy support;
- stale-but-superseded vs stale-but-still-valid evidence;
- provenance-bound support that lacks independent corroboration.

This should be done with additional case types and coverage-gated robustness sweeps, not by weakening EvidenceSufficient globally.
