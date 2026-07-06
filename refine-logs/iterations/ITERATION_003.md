# Iteration 003: EAIR Component Ablation Nodes

Date: 2026-06-17

## Core Hypothesis

`HardGate(a)`, `EvidenceSufficient(a)`, and soft `EAIR(q,a)` should cover different failure modes. If all three components are necessary, the benchmark should contain cases where each single-component ablation misses a distinct risk.

## System Changes

Added FormalTrust-compatible guardrail nodes:

- `guardrail.eair_hard_gate`
- `guardrail.eair_evidence_sufficiency`
- `guardrail.eair_soft_score`

Each node reads `FormalTrustState`, reads its own config, and returns only `metrics` patches with `final_action`, `gate_decision`, `path_credibility`, `path_poison`, and `eair`.

## Benchmark / Baseline Changes

Added baselines:

```text
eair_hard_gate_only
eair_evidence_sufficiency_only
eair_soft_score_only
```

Added conditions:

- `trusted_policy_violating_parameter`: evidence looks sufficient, but the proposed parameter violates hard policy.
- `low_trust_oracle_action`: action shape is policy-safe, but support comes only from low-trust evidence.
- `mixed_support_poison_same_claim`: trusted and poisoned documents jointly support the same action claims.

## Experiments Run

Command:

```powershell
python -c "from pathlib import Path; from formaltrust_platform.experiments.eair_bench import BASELINES, build_benchmark, run_experiment; run_experiment(build_benchmark(), BASELINES, output_dir=Path('outputs/eair_bench_pilot'))"
```

Outputs:

- `outputs/eair_bench_pilot/case_results.json`
- `outputs/eair_bench_pilot/summary.json`
- `outputs/eair_bench_pilot/baseline_summary.csv`
- `outputs/eair_bench_pilot/report.md`

Scale:

- 9 samples
- 13 baselines
- 117 baseline-case results

## Supported Conclusions

- `HardGate` is needed: `eair_evidence_sufficiency_only` misses `trusted_policy_violating_parameter`.
- `EvidenceSufficient` is needed: `eair_hard_gate_only` misses `low_trust_oracle_action`.
- soft path-poison / EAIR signal is needed: hard/evidence-only variants miss `mixed_support_poison_same_claim`.
- `eair_full` reaches `UDR=0.0000`, `UAR=0.0000`, and `parameter_violation_rate=0.0000` in the updated deterministic pilot.

## Weakened / New Risks

- `eair_full` now has `false_positive_rate=0.1111` and `over_refusal_rate=0.2222`, driven by conservative blocking of mixed clean+poison support paths.
- This is not a failure of the direction, but it does mean the next iteration needs a better distinction between benign co-retrieval and poisoned support-path participation.

## Decision

`revise + keep`

Keep the three-component EAIR decomposition. Revise the soft path-poison rule before claiming utility: current deterministic evidence shows safety improvement but also a conservative-block tradeoff.

## Next Iteration Questions

1. Should mixed support paths be blocked, replaced, or allowed with provenance warnings when trusted independent support exists?
2. Should `path_poison` be claim-local, source-cluster-local, or action-field-local?
3. Can source diversity / near-duplicate penalties reduce false blocking without weakening hijack detection?
4. How should this component ablation be reflected in `DERIVATION_PACKAGE.md` and `PAPER_PLAN.md`?
