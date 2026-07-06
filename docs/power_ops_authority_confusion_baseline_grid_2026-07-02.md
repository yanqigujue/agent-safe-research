# Power-Ops Authority-Confusion Baseline Grid

This grid compares role-aware checking with boundary-only, attribution-only, permissive, and strict-block variants.

## Aggregate

| Metric | Value |
|---|---:|
| row_count | 10 |
| baseline_count | 5 |
| capguard_role_confusion_advantage | 1.000 |

## Baselines

| Baseline | Legal preservation | Confusion block | False allow | False block |
|---|---:|---:|---:|---:|
| `capguard` | 1.000 | 1.000 | 0.000 | 0.000 |
| `permission_only` | 1.000 | 0.000 | 1.000 | 0.000 |
| `boundary_scope_only` | 1.000 | 0.000 | 1.000 | 0.000 |
| `field_attribution_only` | 1.000 | 0.000 | 1.000 | 0.000 |
| `strict_block` | 0.000 | 1.000 | 0.000 | 1.000 |

## Diagnosis

- Boundary-blind baselines: `permission_only`, `boundary_scope_only`, `field_attribution_only`.
- Overconservative baselines: `strict_block`.
- Role-aware best baseline: `capguard`.
