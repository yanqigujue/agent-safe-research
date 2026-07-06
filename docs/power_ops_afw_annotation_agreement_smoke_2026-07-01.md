# AFW Annotation Agreement Report

## Summary

| Metric | Value |
|---|---:|
| agreement_id | power_ops_afw_annotation_agreement_smoke |
| agreement_source | machine_prefill_smoke_not_human |
| paired_items | 40 |
| missing_from_annotator_a | 0 |
| missing_from_annotator_b | 0 |
| threshold | 0.7 |
| min_kappa | 1.0 |
| mean_kappa | 1.0 |
| passes_threshold | True |
| human_kappa_status | not_human_double_annotation |

## Field Agreement

| Field | Items | Observed agreement | Expected agreement | Kappa |
|---|---:|---:|---:|---:|
| security_category | 40 | 1.000 | 0.138 | 1.000 |
| severity | 40 | 1.000 | 0.389 | 1.000 |
| expected_behavior | 40 | 1.000 | 0.650 | 1.000 |
| evaluation_standard | 40 | 1.000 | 0.680 | 1.000 |

## Boundary

This report may be generated from machine-prefilled smoke annotations. Only `agreement_source=human_double_annotation` should be used as evidence for the project Kappa target.
