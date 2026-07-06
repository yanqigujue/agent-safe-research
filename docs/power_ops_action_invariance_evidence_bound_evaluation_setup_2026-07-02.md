# Power-Ops Evidence-Bound Evaluation Setup

**Status:** ready

## 4 Evaluation Setup

We evaluate field-level action invariance with a bounded power-operation setup: a 10-case curated baseline grid, an 18-case expanded suite, and trace replay fixtures that are treated as audit inputs rather than production telemetry.

<!-- slot: benchmark_scope; sources: docs/power_ops_action_invariance_baseline_grid_2026-07-02.json, docs/power_ops_action_invariance_expanded_dataset_audit_2026-07-02.json, docs/power_ops_trace_import_results_2026-07-02.json -->

The expanded dataset audit reports 18 cases with oracle coverage 1.000 across source types evidence, memory, prior_step_output, skill, tool_metadata, user_approval; this is the current dataset boundary for section 4.

<!-- slot: dataset_and_cases; sources: docs/power_ops_action_invariance_expanded_dataset_audit_2026-07-02.json -->

The 10-case curated baseline grid compares 4 modes: strict-block, fieldwise-decision-only, provenance-only, and fieldwise-repair.

<!-- slot: baselines; sources: docs/power_ops_action_invariance_baseline_grid_2026-07-02.json -->

The trace-import path contributes 4 trace-import boundary cases and 1 multi-step source-chain case, plus 2 planner-skill-tool-memory cases; these fixtures check malformed, missing-source, duplicate-approval, expired-epoch, and multi-source import behavior.

<!-- slot: trace_imports; sources: docs/power_ops_trace_import_results_2026-07-02.json, docs/power_ops_multistep_trace_import_results_2026-07-02.json, docs/power_ops_planner_skill_tool_memory_results_2026-07-02.json -->

Table evidence binding currently marks 21 table rows as fully supported, while the assembled draft audit reports source-link completeness 1.000 and text match rate 1.000.

<!-- slot: metrics_and_audits; sources: docs/power_ops_action_invariance_table_evidence_binding_2026-07-02.json, docs/power_ops_action_invariance_paper_draft_consistency_audit_2026-07-02.json -->

This setup supports fixture-level evaluation claims only: it does not claim production telemetry, wall-clock latency, operator workload reduction, or official benchmark superiority.

<!-- slot: claim_boundary; sources: docs/power_ops_action_invariance_expanded_dataset_audit_2026-07-02.json, docs/power_ops_action_invariance_table_evidence_binding_2026-07-02.json, docs/power_ops_action_invariance_paper_draft_consistency_audit_2026-07-02.json -->
