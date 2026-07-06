# Power-Ops Action Invariance Performance Profile

## Inputs

| Item | Value |
|---|---:|
| Suite profiles | 3 |
| Baseline profiles | 4 |

## Suite Profiles

| Suite | Cases | Normal preservation | Safety removal | Whole-action block | Review fields/case | Latency proxy | Audit compression |
|---|---:|---:|---:|---:|---:|---:|---:|
| `power_ops_action_invariance_expanded` | 18 | 1.000 | 1.000 | 0.000 | 1.000 | 36 | 0.500 |
| `power_ops_action_invariance_metamorphic` | 4 | 1.000 | 1.000 | 0.000 | 1.000 | 8 | 0.688 |
| `power_ops_skill_authority` | 8 | 1.000 | 1.000 | 0.000 | 1.000 | 16 | 0.500 |

## Baseline Profiles

| Baseline | Cases | Normal preservation | Safety removal | Whole-action block | False allow | Latency proxy |
|---|---:|---:|---:|---:|---:|---:|
| `strict_block` | 10 | 0.000 | 1.000 | 1.000 | 0.000 | 20 |
| `fieldwise_decision_only` | 10 | 0.000 | 1.000 | 1.000 | 0.000 | 20 |
| `provenance_only` | 10 | 1.000 | 0.000 | 0.000 | 1.000 | 20 |
| `fieldwise_repair` | 10 | 1.000 | 1.000 | 0.000 | 0.000 | 20 |

## Best Current Baseline

- `fieldwise_repair` is the best current baseline under the safety-preserving normal-behavior score.
- This does not claim production superiority; it only summarizes the current curated baseline grid.
