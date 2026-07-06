# Iteration 004: Effective Path-Poison Discount

Date: 2026-06-17

## Core Hypothesis

Poisoned co-support should not automatically block a high-risk action when the action is independently and sufficiently supported by trusted evidence. The system should preserve the poisoned support signal for audit, but use an effective path-poison value for blocking.

## System Changes

Updated EAIR-Bench scoring:

- Added `raw_path_poison`: raw poison pressure on the action support path.
- Kept `path_poison` as the effective gate value.
- Added `poison_support_warning`: true when poisoned support is present but independent trusted evidence fully supports the oracle action.

Updated FormalTrust node metrics:

- `guardrail.eair_full`
- `guardrail.eair_soft_score`
- `guardrail.eair_hard_gate`
- `guardrail.eair_evidence_sufficiency`

All continue returning only `metrics` patches.

## Experiments Run

Command:

```powershell
python -c "from pathlib import Path; from formaltrust_platform.experiments.eair_bench import BASELINES, build_benchmark, run_experiment; run_experiment(build_benchmark(), BASELINES, output_dir=Path('outputs/eair_bench_pilot'))"
```

Scale:

- 9 samples
- 13 baselines
- 117 baseline-case results

## Key Results

For `eair_full`:

- `unsafe_decision_rate=0.0000`
- `unsupported_action_rate=0.0000`
- `parameter_violation_rate=0.0000`
- `false_positive_rate=0.0000`
- `poison_support_warning_rate=0.1111`
- `over_refusal_rate=0.1111`

## Supported Conclusions

- Mixed clean+poison support can be handled as allow-with-warning when trusted independent evidence is sufficient.
- Raw poison pressure remains visible for audit, so the system does not silently erase contaminated evidence paths.
- Hijack cases are still handled via `influence_type="hijack"` and action replacement.

## Weakened / New Risks

- The discount rule currently uses a deterministic oracle-action condition. It must be generalized carefully before real LLM experiments.
- The remaining over-refusal comes from low-trust oracle-looking actions, which may be acceptable for high-risk contexts but needs threshold/utility analysis.
- `DERIVATION_PACKAGE.md` still needs to formalize raw vs effective poison pressure.

## Decision

`revise + keep`

Keep the raw/effective distinction. Revise the mathematical package and reporting so this is presented as an audit-aware risk decomposition, not an ad hoc threshold patch.

## Next Iteration Questions

1. How should `RawPathPoison(a)` and `EffectivePathPoison(a)` be written in the derivation?
2. Should warning-level poisoned co-support affect downstream human-review routing even when action is allowed?
3. How does the discount behave with multiple independent sources, near-duplicates, and stale trusted evidence?
4. Should `poison_support_warning_rate` become a headline metric alongside false positive and unsafe action rate?
