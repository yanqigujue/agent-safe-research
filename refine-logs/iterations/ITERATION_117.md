# Iteration 117 - Power-Ops Action Invariance Baselines

## Goal

Move the power-ops action-invariance direction from an idea about avoiding over-conservative guards into runnable artifacts: trace replay, span/OTLP replay, novelty firewall, and baseline comparison.

## Updated One-Sentence Thesis

Strict supervision of LLM agents should not collapse mixed actions wholesale: authorized fields should remain invariant while blocked or abstained fields are removed or routed to partial human review.

## What Changed

- Added span/OTLP replay cases and validation config:
  - `examples/data/power_ops_action_invariance_span_otlp_repair_cases.json`
  - `examples/power_ops_action_invariance_span_otlp_repair_validation.yaml`
- Added span/OTLP results and explanation:
  - `docs/power_ops_action_invariance_span_otlp_repair_2026-07-02.md`
  - `docs/power_ops_action_invariance_span_otlp_repair_results_2026-07-02.md/json`
- Added literature review and novelty firewall:
  - `docs/power_ops_action_invariance_lit_review_2026-07-02.md`
  - `docs/power_ops_action_invariance_novelty_firewall_2026-07-02.md`
- Added baseline grid implementation:
  - `formaltrust_platform/experiments/power_ops_action_invariance_baselines.py`
  - `docs/power_ops_action_invariance_baseline_grid_2026-07-02.md/json`
- Updated `README_POWER_OPS_ACTION_INVARIANCE.md`, `task_plan.md`, `findings.md`, and `progress.md`.

## Results

### Span/OTLP Replay

| Metric | Value |
|---|---:|
| total_cases | 2 |
| passed_cases | 2 |
| gate counts | block=1, abstain=1 |
| whole_action_block_rate | 0.000 |
| executable_fieldwise_repair_success_rate | 1.000 |
| repair_frame_validity_rate | 1.000 |

### Baseline Grid

| baseline | auth final preservation | unsafe final removal | whole-action block | executable invariance | false allow |
|---|---:|---:|---:|---:|---:|
| strict-block | 0.000 | 1.000 | 1.000 | 0.000 | 0.000 |
| fieldwise-decision-only | 0.000 | 1.000 | 1.000 | 0.000 | 0.000 |
| provenance-only | 1.000 | 0.000 | 0.000 | 0.000 | 1.000 |
| fieldwise-repair | 1.000 | 1.000 | 0.000 | 1.000 | 0.000 |

## Novelty Boundary

Unsafe claims:

- First LLM-agent guardrail.
- First runtime enforcement framework.
- First least-privilege LLM-agent method.
- First over-defense benchmark.
- Superiority over AgentSpec, AgentVisor, AgentSentry, CaMeL, ToolPrivBench, RACG, AgentDojo, or InjecGuard.

Safe claim:

> The artifact demonstrates field-level action invariance under strict supervision on curated power-operation cases: authorized fields are preserved in the final action, while blocked or abstained fields are removed or routed to partial human review.

## Verification

| Command | Result |
|---|---|
| `pytest tests/test_power_ops_action_invariance.py::test_power_ops_span_otlp_repair_yaml_runs_through_afw_runtime_graph -q` | 1 passed |
| `pytest tests/test_power_ops_action_invariance.py::test_baseline_grid_compares_coarse_and_fieldwise_final_actions tests/test_power_ops_action_invariance.py::test_power_ops_baseline_grid_from_fieldwise_repair_run -q` | 2 passed |
| `pytest tests/test_afw_bench.py tests/test_interfaces.py tests/test_power_ops_action_invariance.py -q` | 98 passed |
| `pytest -q` | 212 passed |

## Keep / Revise / Reject

Keep the technical direction, revise the paper framing. The broad framing is too close to existing runtime-enforcement, capability, least-privilege, and over-defense work. The paper should emphasize field-level authority witnesses, repair-frame validity, and final-action preservation under intervention.

## Next Iteration

Increase external validity:

1. Add real or semi-real power-agent span/OTLP traces.
2. Add AgentDojo-style task mapping into action fields and authority needs.
3. Add human-review burden metrics: average human-review fields, auto-executable field ratio, and repair compression.
