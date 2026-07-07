# LLM Error Bench v1

This directory contains an internal 2,500-row benchmark for evaluating whether an LLM or safety algorithm can answer, identify, and correct high-risk mistakes.

The dataset intentionally contains many cases that low-end or overconfident LLMs are likely to answer incorrectly. Power-grid and electrical-safety scenarios are prioritized, with 500 non-power high-risk safety/generalization cases.

## Files

- `llm_error_bench_v1.jsonl`: main dataset, one `TestCase`-compatible JSON object per line.
- `schema.json`: row-level schema.
- `sources.json`: source catalog and source-type notes.
- `summary.json`: counts, generation seed, and dataset hash.
- `generate_llm_error_bench_v1.py`: deterministic generator.

## Distribution

Domain groups:

| value | count |
|---|---:|
| power_grid | 2000 |
| non_power | 500 |

Task types:

| value | count |
|---|---:|
| scenario_decision | 417 |
| multiple_choice | 417 |
| error_identification | 416 |
| direct_qa | 416 |
| correction | 416 |
| true_false | 418 |

Weak-answer labels:

| value | count |
|---|---:|
| incorrect | 2125 |
| correct | 375 |

Source types:

| value | count |
|---|---:|
| official_standard_anchor | 1009 |
| public_dataset_anchor | 900 |
| public_incident_anchor | 475 |
| synthetic_manual | 116 |

## Row Shape

Each row has the platform fields `id`, `input`, `expected_behavior`, `tags`, and `metadata`.
Important metadata fields:

- `correct_answer`: reference safe/correct answer.
- `weak_model_answer`: synthetic weak-model response; usually wrong, sometimes correct as a control.
- `weak_answer_label`: `incorrect` or `correct`.
- `trap_type`: expected failure mechanism, such as `safety_overconfidence`, `missing_condition`, or `constraint_violation`.
- `source_type`: `official_standard_anchor`, `public_incident_anchor`, `public_dataset_anchor`, or `synthetic_manual`.
- `verification_status`: whether the row is rule-checked, source-anchored, or still needs expert/domain review.

## Caveats

This is a benchmark seed, not an operational electrical-safety manual. Most cases are synthetic or source-anchored synthetic examples. Use it to evaluate model behavior and safety gates; do not use it to authorize real electrical, medical, legal, financial, cyber, or field operations.
