# Iteration 009: Seeded Stochastic Claim Extraction Noise

Date: 2026-06-17

## Core Hypothesis

Claim extraction noise should be replayable before it is scaled. A deterministic drop/inject node is useful for unit perturbations, but robustness sweeps need fixed-seed stochastic false-negative and false-positive schedules.

## Interface Decision

Extend the existing FormalTrust node:

```text
attack.eair_claim_extraction_noise
```

The node remains a graph-level attack/claim-extraction perturbation node. It still returns only:

- `retrieval_context`
- `metrics`

## Config Changes

Added:

- `drop_probability`: per-claim stochastic drop probability.
- `candidate_inject_claims`: claim ids considered for stochastic injection.
- `inject_probability`: per-candidate stochastic injection probability.
- `seed`: fixed random seed for replayable perturbations.

Existing deterministic configs (`drop_claims`, `inject_claims`, `target_doc_id`, `target_rank`, `prepend_injected`) remain unchanged.

## Math / Model Update

```text
C_hat_seed(d) =
  Drop_p(C_hat(d), seed)
  union Inject_p(C_candidates(d), seed).
```

This separates:

- false-negative extraction schedules from retrieval failure;
- false-positive unsafe claim schedules from document poisoning;
- seeded robustness sweeps from one-off hand-authored perturbations.

## TDD Evidence

RED:

```powershell
pytest tests/test_eair_bench.py -k "seeded" -q
```

Failed at graph assembly because `attack.eair_claim_extraction_noise` did not declare `drop_probability`, `candidate_inject_claims`, `inject_probability`, or `seed`.

GREEN:

```powershell
pytest tests/test_eair_bench.py -k "seeded" -q
pytest tests/test_eair_bench.py -k "claim_extraction_noise" -q
```

## Results

- `drop_probability=0.5`, `seed=3`, `target_rank=1` drops exactly one rank-1 clean approval claim and preserves `pre_noise_claims`.
- `candidate_inject_claims=["approval_can_be_skipped", "stale_approval_can_be_skipped"]`, `inject_probability=0.5`, `seed=4`, `target_rank=1` injects two unsafe claims, produces candidate `allow_bypass`, and `eair_full` replaces it with `reject_bypass`.

## Decision

Keep and revise.

This is still metadata-level noise, not a real extractor. It is useful because it makes claim-noise schedules reproducible and keeps all perturbations inside the FormalTrust node interface.

## Next Questions

1. Add a small multi-seed sweep runner/report for graph-level claim-noise robustness.
2. Add retrieval perturbation as a separate graph node so retrieval noise and extraction noise can be crossed.
3. Add a real claim extractor adapter that emits `C_hat` for comparison against benchmark `C_true`.
