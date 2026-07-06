# Iteration 013: Robustness Sweep Seed Grid

Date: 2026-06-17

## Core Hypothesis

Artifact-backed robustness sweeps should support compact multi-seed studies without requiring a user to hand-write every retrieval-noise and claim-noise run. The expansion should still be a FormalTrust evaluator node, not a separate script path.

## Interface Decision

Extend:

```text
evaluate.eair_robustness_sweep
```

with optional config:

- `seed_grid.retrieval_seeds`
- `seed_grid.claim_noise_seeds`

Each base run expands to the Cartesian product of the two seed axes. Expanded run names append replay suffixes such as `::r7::c4`.

## Outputs

New or extended metrics:

- `robustness_sweep_expanded_count`
- `robustness_sweep_base_count`
- `robustness_sweep_seed_grid`
- `robustness_sweep_rows[*].retrieval_seed`
- `robustness_sweep_rows[*].claim_noise_seed`

Artifacts:

- `robustness_sweep.json` includes `seed_grid`.
- `robustness_sweep.csv` includes `retrieval_seed` and `claim_noise_seed`.

## TDD Evidence

RED:

```powershell
pytest tests/test_eair_bench.py -k "seed_grid" -q
```

Failed because `evaluate.eair_robustness_sweep` rejected unknown config field `seed_grid` during graph assembly.

GREEN:

```powershell
pytest tests/test_eair_bench.py -k "seed_grid" -q
pytest tests/test_eair_bench.py -k "robustness_sweep" -q
pytest tests/test_interfaces.py -q
```

## Checked Run

Base run:

- retrieval: `top_k=2`
- claim noise: `candidate_inject_claims=["approval_can_be_skipped"]`, `inject_probability=0.5`
- retrieval seeds: `[7, 8]`
- claim-noise seeds: `[4, 5]`

Expanded result:

- `robustness_sweep_count=4`
- `robustness_sweep_expanded_count=4`
- pass rate `1.0`
- outcome counts: `{"allowed_supported_action": 2, "replaced_unsafe_candidate": 2}`

## Decision

Keep and revise.

Seed-grid expansion is a useful bridge from deterministic graph checks to larger robustness studies. Next, add case-level sweep reports and model-backed action generation.

## Next Questions

1. Should sweep reports aggregate over case ids as well as perturbation configs?
2. Should sweep rows include model/extractor identifiers when those components become non-deterministic?
3. What confidence interval or bootstrap summary should accompany multi-seed outcome distributions?
