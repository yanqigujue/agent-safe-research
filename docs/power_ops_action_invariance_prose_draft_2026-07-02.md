# Power-Ops Action Invariance Prose Draft

**Title:** Field-Level Action Invariance for Power-Operation LLM Agents
**Date:** 2026-07-02
**Forbidden claim hits:** 0

## §0 Abstract

**Purpose:** State the action-invariance problem, the fieldwise authority method, and the strongest bounded result.

This section should be drafted around its purpose, but it currently has no supported claim assigned in the artifact map: State the action-invariance problem, the fieldwise authority method, and the strongest bounded result.

Evidence: none
Safe use: Use as structure only until a supported claim is assigned.

## §1 Introduction

**Purpose:** Motivate conservative collapse under strict supervision in power-operation agents.

This section should be drafted around its purpose, but it currently has no supported claim assigned in the artifact map: Motivate conservative collapse under strict supervision in power-operation agents.

Evidence: none
Safe use: Use as structure only until a supported claim is assigned.

## §2 Related Work and Novelty Boundary

**Purpose:** Position against attribution-only, access-control-only, RAG faithfulness, and generic agent guardrails.

This section should be drafted around its purpose, but it currently has no supported claim assigned in the artifact map: Position against attribution-only, access-control-only, RAG faithfulness, and generic agent guardrails.

Evidence: none
Safe use: Use as structure only until a supported claim is assigned.

## §3 Formal Model and CapGuard

**Purpose:** Define Cap(x), Need(s,f), field coverage, minimal authority witnesses, and repair-frame invariance.

The current artifact supports the following bounded L1 statement: fieldwise repair final-action mode exists. This paragraph should be cited only with the attached evidence and interpreted under its safe-use constraint.

Evidence: `formaltrust_platform/nodes/afw.py`, `tests/test_interfaces.py`
Safe use: Use with the stated evidence level.

## §4 Test Framework and Power-Ops Benchmark Slice

**Purpose:** Describe curated, expanded, metamorphic, skill-driven, trace, and bridge fixtures.

This section should be drafted around its purpose, but it currently has no supported claim assigned in the artifact map: Describe curated, expanded, metamorphic, skill-driven, trace, and bridge fixtures.

Evidence: none
Safe use: Use as structure only until a supported claim is assigned.

## §5 Results and Analysis

**Purpose:** Report field preservation, unsafe-field removal, over-conservatism, performance profile, and trace-import behavior.

The current artifact supports the following bounded L2 statement: curated power-ops fieldwise repair preserves authorized fields and removes unauthorized fields. This paragraph should be cited only with the attached evidence and interpreted under its safe-use constraint.

Evidence: `docs/power_ops_action_invariance_fieldwise_repair_results_2026-07-02.json`
Safe use: Use with the stated evidence level.

The current artifact supports the following bounded L2 statement: expanded 18-case power-ops fieldwise repair preserves authorized fields and removes unauthorized fields. This paragraph should be cited only with the attached evidence and interpreted under its safe-use constraint.

Evidence: `docs/power_ops_action_invariance_expanded_results_2026-07-02.json`, `docs/power_ops_action_invariance_expanded_dataset_audit_2026-07-02.json`
Safe use: Use with the stated evidence level.

The current artifact supports the following bounded L2 statement: metamorphic authority-confusion tests preserve authorized fields while removing or reviewing mutated unsafe fields. This paragraph should be cited only with the attached evidence and interpreted under its safe-use constraint.

Evidence: `docs/power_ops_action_invariance_metamorphic_tests_2026-07-02.json`, `examples/data/power_ops_action_invariance_metamorphic_cases.jsonl`
Safe use: Use with the stated evidence level.

The current artifact supports the following bounded L2 statement: no-RAG skill-driven fixture lifts skill, tool metadata, approval, memory, and prior-step outputs into field-level capabilities. This paragraph should be cited only with the attached evidence and interpreted under its safe-use constraint.

Evidence: `docs/power_ops_skill_authority_results_2026-07-02.json`, `docs/power_ops_skill_authority_dataset_audit_2026-07-02.json`, `docs/power_ops_skill_authority_model_2026-07-02.md`
Safe use: Use with the stated evidence level.

The current artifact supports the following bounded L2 statement: current artifact reports a safety-preserving normal-behavior performance profile. This paragraph should be cited only with the attached evidence and interpreted under its safe-use constraint.

Evidence: `docs/power_ops_action_invariance_performance_2026-07-02.json`
Safe use: Use as normal-behavior preservation profile; latency is only a proxy.
Result readback: suite_count=3; baseline_count=4; best_baseline=fieldwise_repair

The current artifact supports the following bounded L2 statement: baseline grid shows strict-block collapse and provenance-only false allow on curated cases. This paragraph should be cited only with the attached evidence and interpreted under its safe-use constraint.

Evidence: `docs/power_ops_action_invariance_baseline_grid_2026-07-02.json`
Safe use: Use as ablation evidence on curated cases only.

The current artifact supports the following bounded L3 statement: trace/span/OTLP replay feeds fieldwise repair. This paragraph should be cited only with the attached evidence and interpreted under its safe-use constraint.

Evidence: `docs/power_ops_action_invariance_trace_repair_results_2026-07-02.json`, `docs/power_ops_action_invariance_span_otlp_repair_results_2026-07-02.json`
Safe use: Use with the stated evidence level.

The current artifact supports the following bounded L3 statement: trace import fixture covers malformed trace, missing source, duplicate approval, and expired epoch boundaries. This paragraph should be cited only with the attached evidence and interpreted under its safe-use constraint.

Evidence: `docs/power_ops_trace_import_contract_2026-07-02.md`, `docs/power_ops_trace_import_results_2026-07-02.json`, `examples/data/power_ops_trace_import_fixture.json`
Safe use: Use as L3 trace-fixture evidence, not production telemetry.
Result readback: boundary_count=4; boundary_case_total=4; whole_action_block_rate=0.000; authorized_preservation=1.000; unsafe_removal=1.000

The current artifact supports the following bounded L3 statement: multi-step trace import covers planner, skill, tool metadata, memory, prior-step output, and user approval source chains. This paragraph should be cited only with the attached evidence and interpreted under its safe-use constraint.

Evidence: `docs/power_ops_multistep_trace_import_results_2026-07-02.json`, `docs/power_ops_multistep_trace_import_runtime_report_2026-07-02.json`, `examples/data/power_ops_multistep_trace_import_fixture.json`, `docs/power_ops_planner_skill_tool_memory_results_2026-07-02.json`, `docs/power_ops_planner_skill_tool_memory_runtime_report_2026-07-02.json`, `examples/data/power_ops_planner_skill_tool_memory_fixture.json`
Safe use: Use as L3 trace-fixture evidence, not production telemetry.
Result readback: boundary_count=1; boundary_case_total=1; whole_action_block_rate=0.000; authorized_preservation=1.000; unsafe_removal=1.000; source_type_coverage=1.000 | cases=2; source_chain_coverage=1.000; authorized_preservation=1.000; unsafe_removal=1.000; whole_action_block_rate=0.000

## §6 Limitations and Next Experiments

**Purpose:** State missing production trace, wall-clock latency, operator workload, and official benchmark gaps.

The current artifact supports the following bounded L4 statement: AgentDojo-style and semi-real power trace bridge fixtures are expressible. This paragraph should be cited only with the attached evidence and interpreted under its safe-use constraint.

Evidence: `docs/power_ops_action_invariance_agentdojo_style_results_2026-07-02.json`, `docs/power_ops_action_invariance_semireal_trace_results_2026-07-02.json`
Safe use: Use as bridge evidence, not official benchmark superiority.

## Result Readback

| Artifact | Path | Key readback |
|---|---|---|
| power_ops_action_invariance_performance_profile | `docs\power_ops_action_invariance_performance_2026-07-02.json` | suite_count=3; baseline_count=4; best_baseline=fieldwise_repair |
| power_ops_trace_import_summary | `docs\power_ops_trace_import_results_2026-07-02.json` | boundary_count=4; boundary_case_total=4; whole_action_block_rate=0.000; authorized_preservation=1.000; unsafe_removal=1.000 |
| power_ops_trace_import_summary | `docs\power_ops_multistep_trace_import_results_2026-07-02.json` | boundary_count=1; boundary_case_total=1; whole_action_block_rate=0.000; authorized_preservation=1.000; unsafe_removal=1.000; source_type_coverage=1.000 |
| power_ops_planner_skill_tool_memory_summary | `docs\power_ops_planner_skill_tool_memory_results_2026-07-02.json` | cases=2; source_chain_coverage=1.000; authorized_preservation=1.000; unsafe_removal=1.000; whole_action_block_rate=0.000 |

## Revision Rules

- Treat every prose paragraph as bounded by its evidence list.
- Use result readback for numeric statements before copying any number into the paper.
- Keep deployment, workload, and official benchmark claims in limitations until evidence exists.
