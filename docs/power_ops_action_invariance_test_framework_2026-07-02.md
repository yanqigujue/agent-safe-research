# Power-Ops Action Invariance Test Framework

Date: 2026-07-02

## Purpose

The test framework measures whether a power-operation agent guardrail can preserve authorized action fields while preventing unauthorized fields.

It uses the existing FormalTrust runtime path:

```text
TestCase JSONL
  -> ExperimentRunner
  -> guardrail.afw_capguard
  -> evaluate.afw_runtime
  -> power_ops_action_invariance summary
```

## Files

| File | Role |
|---|---|
| `formaltrust_platform/experiments/power_ops_action_invariance.py` | Computes action-invariance metrics from FormalTrust case artifacts. |
| `tests/test_power_ops_action_invariance.py` | Focused regression tests for the new metrics and YAML run. |
| `examples/power_ops_action_invariance_runtime_validation.yaml` | Runtime graph config. |
| `examples/data/power_ops_action_invariance_cases.jsonl` | First 8 curated power-operation cases. |

## Metrics

| Metric | Formula |
|---|---|
| `authorized_field_preservation_rate` | `preserved_authorized_fields / authorized_fields` |
| `unauthorized_field_prevention_rate` | `prevented_unauthorized_fields / unauthorized_fields` |
| `strict_block_collapse_rate` | `blocked_mixed_cases_with_allowed_authorized_field / blocked_cases` |
| `fieldwise_repair_success_rate` | `mixed_cases_preserve_authorized_and_prevent_unauthorized / mixed_cases` |
| `witness_log_completeness_rate` | `fields_with_witness_audit / runtime_fields` |
| `mean_witness_compression_ratio` | mean witness audit compression ratio |

## TDD Status

The initial implementation followed a red/green cycle:

1. Added `tests/test_power_ops_action_invariance.py`.
2. Observed failure because `formaltrust_platform.experiments.power_ops_action_invariance` did not exist.
3. Added the minimal metric implementation.
4. Added YAML/data test.
5. Observed one failing case due to invalid `skill_manifest` schema.
6. Fixed the sample to use `output_semantic_roles`, matching existing AFW skill-manifest lifting.

## Validation Command

```powershell
pytest tests/test_power_ops_action_invariance.py -q
```

Expected current result:

```text
3 passed
```

## Boundary

The framework currently reports potential fieldwise repair success from field decisions. The existing `final_action` still routes blocked mixed actions to human review as a whole-action safety fallback. Implementing actual executable fieldwise repair is a next iteration.
