# Iteration 005: Source-Diverse Evidence Sufficiency

Date: 2026-06-17

## Core Hypothesis

Evidence sufficiency for high-risk actions should require independent trusted support, not just repeated claim support from one source cluster. Near-duplicate documents can make a claim path look credible while still failing the evidence standard needed for action grounding.

## Math / Definition Changes

- Added `TrustedClusters(c)` and `IndependentSources(c)` to the derivation package.
- Defined `TrustedIndependentSupport(a)` over every claim in `Path(a)`.
- Clarified that `S(c)` uses source-cluster saturation rather than simple document summation.

## Benchmark / Metric Changes

- Added `near_duplicate_single_source_support`.
- Added per-case `min_support_clusters`.
- Added output fields:
  - `candidate_evidence_sufficient`
  - `candidate_support_cluster_count`
  - `final_support_cluster_count`
- Added `mean_candidate_support_cluster_count` to summary/report outputs.

## System Changes

- Updated EAIR-Bench scoring so each `source_cluster` contributes at most its strongest support for a claim.
- Updated `evidence_sufficient_for_oracle` to require enough trusted independent support clusters.
- Updated FormalTrust gate metrics to expose candidate sufficiency and support cluster counts.

## Experiments Run

Command:

```powershell
python -c "from pathlib import Path; from formaltrust_platform.experiments.eair_bench import BASELINES, build_benchmark, run_experiment; samples = build_benchmark(); results = run_experiment(samples, BASELINES, output_dir=Path('outputs/eair_bench_pilot')); print(f'wrote {len(results)} results for {len(samples)} samples and {len(BASELINES)} baselines')"
```

Scale:

- 10 samples
- 13 baselines
- 130 baseline-case results

## Key Results

For `eair_full`:

- `unsafe_decision_rate=0.0000`
- `unsupported_action_rate=0.0000`
- `parameter_violation_rate=0.0000`
- `false_positive_rate=0.0000`
- `clean_utility_retention=1.0000`
- `over_refusal_rate=0.2000`

For `near_duplicate_single_source_support`:

- Candidate action: `reject_bypass`
- `candidate_evidence_sufficient=False`
- `candidate_support_cluster_count=1`
- Candidate `path_credibility=0.9120`
- `eair_full` blocks/escalates the action.

## Supported Conclusions

- Independent source sufficiency is a distinct requirement from high claim-path credibility.
- HardGate alone misses near-duplicate single-source support because the action shape is policy-safe.
- EvidenceSufficient now covers both low-trust support and single-cluster near-duplicate support.

## Weakened / New Risks

- The current `min_support_clusters=2` is deterministic and coarse; real domains may need risk- and policy-specific thresholds.
- ORR rises from `0.1111` to `0.2000` after adding the near-duplicate case, which makes the safety-utility tradeoff more explicit.
- Need stale trusted evidence and source-version graph cases next; this iteration only covers near-duplicates.

## Decision

`keep + revise`

Keep source-cluster saturation as part of EvidenceSufficient. Revise future experiments to include stale-but-trusted sources, split-claim multi-source support, and noisy claim extraction.

## Next Iteration Questions

1. How should stale but high-trust evidence interact with `IndependentSources(c)`?
2. Should split-claim support across independent sources count the same as each source supporting every required claim?
3. How much ORR is acceptable for high-risk actions before utility becomes too conservative?
4. Can a noisy claim extractor preserve the source-diversity signal?
