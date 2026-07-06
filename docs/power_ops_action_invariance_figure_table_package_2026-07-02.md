# Power-Ops Action Invariance Figure/Table Package

## Purpose

This package collects the figures and tables that can be directly reused in a paper draft, weekly report, or defense slides for the power-ops action-invariance direction.

核心用途：

- 把当前工程结果变成论文图表。
- 约束论文 claim，不把 L2/L3/L4 结果说成生产部署结果。
- 给后续迭代一个稳定的图表入口。

## Figures

| Figure | Path | Role | Suggested Caption |
|---|---|---|---|
| Figure 1 | `figures/power_ops_action_invariance_architecture.svg` | 方法总览 | Field-level action-invariance architecture. CapGuard lifts capabilities from RAG documents, skill outputs, tool metadata, memory, approvals, and trace context; it checks each action field against its authority need and repairs only invalid fields. |
| Figure 2 | `figures/power_ops_action_invariance_repair_frame.svg` | 核心机制 | Repair-frame action invariance. A mixed action is decomposed into fields; authorized fields are preserved in the executable final action, while unauthorized or uncertain fields are routed to partial human review. |
| Figure 3 | `figures/power_ops_action_invariance_result_ladder.svg` | 证据边界 | Evidence and claim boundary ladder. The current artifact supports implementation, curated-suite, trace-fixture, and bridge evidence, but not production-safety or real-workload claims. |

## Figure Specs

| Spec | Rendered SVG |
|---|---|
| `figures/specs/power_ops_action_invariance_architecture.json` | `figures/power_ops_action_invariance_architecture.svg` |
| `figures/specs/power_ops_action_invariance_repair_frame.json` | `figures/power_ops_action_invariance_repair_frame.svg` |
| `figures/specs/power_ops_action_invariance_result_ladder.json` | `figures/power_ops_action_invariance_result_ladder.svg` |

Re-render command:

```powershell
$env:PYTHONIOENCODING='utf-8'
python C:\Users\wang\.codex\skills\figure-spec\scripts\figure_renderer.py render figures\specs\power_ops_action_invariance_architecture.json --output figures\power_ops_action_invariance_architecture.svg
python C:\Users\wang\.codex\skills\figure-spec\scripts\figure_renderer.py render figures\specs\power_ops_action_invariance_repair_frame.json --output figures\power_ops_action_invariance_repair_frame.svg
python C:\Users\wang\.codex\skills\figure-spec\scripts\figure_renderer.py render figures\specs\power_ops_action_invariance_result_ladder.json --output figures\power_ops_action_invariance_result_ladder.svg
```

## Table 1: Main Result Summary

| Suite / mode | Cases | Whole-action block rate | Executable repair success | Repair frame validity | Evidence level |
|---|---:|---:|---:|---:|---|
| strict-block | 10 | 1.000 | 0.000 | 1.000 | L2 |
| fieldwise-repair | 10 | 0.000 | 1.000 | 1.000 | L2 |
| trace-repair | 2 | 0.000 | 1.000 | 1.000 | L3 |
| span-otlp-repair | 2 | 0.000 | 1.000 | 1.000 | L3 |
| agentdojo-style | 2 | 0.000 | 1.000 | 1.000 | L4 |
| semireal-trace | 2 | 0.000 | 1.000 | 1.000 | L4 |
| expanded-fieldwise | 18 | 0.000 | 1.000 | 1.000 | L2 |
| metamorphic | 4 | 0.000 | 1.000 | 1.000 | L2 |
| skill-authority | 4 | 0.000 | 1.000 | 1.000 | L2 |
| trace-import | 4 | 0.000 | 1.000 | 1.000 | L3 |

Source:

- `README_POWER_OPS_ACTION_INVARIANCE.md`
- `docs/power_ops_action_invariance_fieldwise_repair_results_2026-07-02.md`
- `docs/power_ops_action_invariance_trace_repair_results_2026-07-02.md`
- `docs/power_ops_action_invariance_span_otlp_repair_results_2026-07-02.md`
- `docs/power_ops_action_invariance_agentdojo_style_results_2026-07-02.md`
- `docs/power_ops_action_invariance_semireal_trace_results_2026-07-02.md`
- `docs/power_ops_action_invariance_expanded_results_2026-07-02.md`
- `docs/power_ops_action_invariance_metamorphic_tests_2026-07-02.md`
- `docs/power_ops_skill_authority_results_2026-07-02.md`
- `docs/power_ops_trace_import_results_2026-07-02.md`

## Table 2: Baseline Grid

| Baseline | Authorized final preservation | Unauthorized final removal | Whole-action block | Executable invariance | False allow fields |
|---|---:|---:|---:|---:|---:|
| strict-block | 0.000 | 1.000 | 1.000 | 0.000 | 0.000 |
| fieldwise-decision-only | 0.000 | 1.000 | 1.000 | 0.000 | 0.000 |
| provenance-only | 1.000 | 0.000 | 0.000 | 0.000 | 1.000 |
| fieldwise-repair | 1.000 | 1.000 | 0.000 | 1.000 | 0.000 |

Source: `docs/power_ops_action_invariance_baseline_grid_2026-07-02.md`

Takeaway:

- strict-block is safe but loses all authorized final fields in mixed cases.
- provenance-only keeps normal behavior but false-allows unauthorized fields.
- fieldwise-repair is the only current baseline that keeps authorized fields and removes unauthorized fields in the curated suite.

## Table 3: Review Burden Metrics

| Suite | Partial-review fields | Auto-executable fields | Partial-review severity | Auto-executable severity | Auto severity ratio |
|---|---:|---:|---:|---:|---:|
| agentdojo-style | 2 | 4 | 10.000 | 6.000 | 0.375 |
| semireal-trace | 2 | 4 | 10.000 | 6.000 | 0.375 |

Source:

- `docs/power_ops_action_invariance_agentdojo_style_results_2026-07-02.md`
- `docs/power_ops_action_invariance_semireal_trace_results_2026-07-02.md`

Interpretation:

字段数量和风险权重需要分开看。两个 suite 都只有 2 个字段转人工，但这些字段的 severity 总和为 10，高于自动执行字段的 severity 总和 6。这说明“转人工字段少”不等于“人审风险负担低”。

## Table 3b: Performance / Over-Conservatism Profile

| Profile | Normal preservation | Safety removal | Whole-action block | Review fields/case | Latency proxy | Audit compression |
|---|---:|---:|---:|---:|---:|---:|
| expanded-fieldwise | 1.000 | 1.000 | 0.000 | 1.000 | 36 | 0.500 |
| metamorphic | 1.000 | 1.000 | 0.000 | 1.000 | 8 | 0.688 |
| skill-authority | 1.000 | 1.000 | 0.000 | 1.000 | 8 | 0.500 |

Source: `docs/power_ops_action_invariance_performance_2026-07-02.md`

Interpretation:

这里的 performance 不是实际运行耗时，而是“严格监督下正常行为保留”的实验 profile。`latency proxy` 是 runtime field checks 数量，后续还需要真实 wall-clock latency。

## Table 4: Claim Ledger Summary

| Claim type | Current status | Safe wording |
|---|---|---|
| Implementation | Supported | The implementation supports a `fieldwise_repair` final-action mode. |
| Curated result | Supported on 10 cases | On curated power-operation cases, fieldwise repair preserves authorized fields and removes unauthorized fields. |
| Trace result | Supported on small fixtures | Canonical trace, span/OTLP replay, and trace-import boundary fixtures exercise the same fieldwise-repair path. |
| Bridge result | Supported as bridge only | AgentDojo-style and semi-real traces show representational fit, not official benchmark superiority. |
| Production claim | Not supported | Must be described as future work until real traces or operator workload data exist. |

Source: `docs/power_ops_action_invariance_claim_ledger_2026-07-02.md`

## Paper Placement

| Paper section | Use these artifacts |
|---|---|
| Introduction | Figure 2, one-sentence kernel, conservative-collapse motivation |
| Method | Figure 1, Cap/Need/Coverage definitions, repair invariant |
| Evaluation | Table 1, Table 2, Table 3 |
| Discussion | Figure 3, Table 4, forbidden claims |
| Appendix | Figure specs, YAML configs, result JSON files |

## Current Package Boundary

This package is paper-ready as a draft artifact, not a final camera-ready figure set. Before submission, the next iterations should:

1. expand sample size,
2. run metamorphic tests,
3. add no-RAG skill-driven cases,
4. add performance and latency proxy metrics,
5. import multi-step real/semi-real agent logs and measure wall-clock overhead.
