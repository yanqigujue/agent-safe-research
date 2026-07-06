# Power-Ops Action Invariance Draft Skeleton

**Title:** Field-Level Action Invariance for Power-Operation LLM Agents
**Date:** 2026-07-02
**Claim-bound paragraphs:** 11
**Evidence-bound paragraphs:** 11
**Forbidden claim hits:** 0

## Draft Sections

## §0 Abstract

**Purpose:** State the action-invariance problem, the fieldwise authority method, and the strongest bounded result.
**Evidence discipline:** Summarize L1-L4 evidence without promoting it to production evidence.

- Draft note: no supported claim is currently assigned to this section.

## §1 Introduction

**Purpose:** Motivate conservative collapse under strict supervision in power-operation agents.
**Evidence discipline:** Use safe claims and forbidden-claim boundary from the claim ledger.

- Draft note: no supported claim is currently assigned to this section.

## §2 Related Work and Novelty Boundary

**Purpose:** Position against attribution-only, access-control-only, RAG faithfulness, and generic agent guardrails.
**Evidence discipline:** Use the claim ledger to avoid firstness or official-baseline superiority claims.

- Draft note: no supported claim is currently assigned to this section.

## §3 Formal Model and CapGuard

**Purpose:** Define Cap(x), Need(s,f), field coverage, minimal authority witnesses, and repair-frame invariance.
**Evidence discipline:** Map implementation claims to FormalTrust nodes and tests.

- Claim (L1): fieldwise repair final-action mode exists
  Evidence: `formaltrust_platform/nodes/afw.py`, `tests/test_interfaces.py`
  Safe use: Use with the stated evidence level.
  Draft stub: Use this L1 claim only with evidence from afw.py and test_interfaces.py.

## §4 Test Framework and Power-Ops Benchmark Slice

**Purpose:** Describe curated, expanded, metamorphic, skill-driven, trace, and bridge fixtures.
**Evidence discipline:** Bind each fixture to dataset/YAML/report artifacts.

- Draft note: no supported claim is currently assigned to this section.

## §5 Results and Analysis

**Purpose:** Report field preservation, unsafe-field removal, over-conservatism, performance profile, and trace-import behavior.
**Evidence discipline:** Use result JSON files as the source for every numeric claim.

- Claim (L2): curated power-ops fieldwise repair preserves authorized fields and removes unauthorized fields
  Evidence: `docs/power_ops_action_invariance_fieldwise_repair_results_2026-07-02.json`
  Safe use: Use with the stated evidence level.
  Draft stub: Use this L2 claim only with evidence from power_ops_action_invariance_fieldwise_repair_results_2026-07-02.json.

- Claim (L2): expanded 18-case power-ops fieldwise repair preserves authorized fields and removes unauthorized fields
  Evidence: `docs/power_ops_action_invariance_expanded_results_2026-07-02.json`, `docs/power_ops_action_invariance_expanded_dataset_audit_2026-07-02.json`
  Safe use: Use with the stated evidence level.
  Draft stub: Use this L2 claim only with evidence from power_ops_action_invariance_expanded_results_2026-07-02.json and power_ops_action_invariance_expanded_dataset_audit_2026-07-02.json.

- Claim (L2): metamorphic authority-confusion tests preserve authorized fields while removing or reviewing mutated unsafe fields
  Evidence: `docs/power_ops_action_invariance_metamorphic_tests_2026-07-02.json`, `examples/data/power_ops_action_invariance_metamorphic_cases.jsonl`
  Safe use: Use with the stated evidence level.
  Draft stub: Use this L2 claim only with evidence from power_ops_action_invariance_metamorphic_tests_2026-07-02.json and power_ops_action_invariance_metamorphic_cases.jsonl.

- Claim (L2): no-RAG skill-driven fixture lifts skill, tool metadata, approval, memory, and prior-step outputs into field-level capabilities
  Evidence: `docs/power_ops_skill_authority_results_2026-07-02.json`, `docs/power_ops_skill_authority_dataset_audit_2026-07-02.json`, `docs/power_ops_skill_authority_model_2026-07-02.md`
  Safe use: Use with the stated evidence level.
  Draft stub: Use this L2 claim only with evidence from power_ops_skill_authority_results_2026-07-02.json and power_ops_skill_authority_dataset_audit_2026-07-02.json.

- Claim (L2): current artifact reports a safety-preserving normal-behavior performance profile
  Evidence: `docs/power_ops_action_invariance_performance_2026-07-02.json`
  Safe use: Use as normal-behavior preservation profile; latency is only a proxy.
  Draft stub: Use this L2 claim only with evidence from power_ops_action_invariance_performance_2026-07-02.json.

- Claim (L2): baseline grid shows strict-block collapse and provenance-only false allow on curated cases
  Evidence: `docs/power_ops_action_invariance_baseline_grid_2026-07-02.json`
  Safe use: Use as ablation evidence on curated cases only.
  Draft stub: Use this L2 claim only with evidence from power_ops_action_invariance_baseline_grid_2026-07-02.json.

- Claim (L3): trace/span/OTLP replay feeds fieldwise repair
  Evidence: `docs/power_ops_action_invariance_trace_repair_results_2026-07-02.json`, `docs/power_ops_action_invariance_span_otlp_repair_results_2026-07-02.json`
  Safe use: Use with the stated evidence level.
  Draft stub: Use this L3 claim only with evidence from power_ops_action_invariance_trace_repair_results_2026-07-02.json and power_ops_action_invariance_span_otlp_repair_results_2026-07-02.json.

- Claim (L3): trace import fixture covers malformed trace, missing source, duplicate approval, and expired epoch boundaries
  Evidence: `docs/power_ops_trace_import_contract_2026-07-02.md`, `docs/power_ops_trace_import_results_2026-07-02.json`, `examples/data/power_ops_trace_import_fixture.json`
  Safe use: Use as L3 trace-fixture evidence, not production telemetry.
  Draft stub: Use this L3 claim only with evidence from power_ops_trace_import_contract_2026-07-02.md and power_ops_trace_import_results_2026-07-02.json.

- Claim (L3): multi-step trace import covers planner, skill, tool metadata, memory, prior-step output, and user approval source chains
  Evidence: `docs/power_ops_multistep_trace_import_results_2026-07-02.json`, `docs/power_ops_multistep_trace_import_runtime_report_2026-07-02.json`, `examples/data/power_ops_multistep_trace_import_fixture.json`, `docs/power_ops_planner_skill_tool_memory_results_2026-07-02.json`, `docs/power_ops_planner_skill_tool_memory_runtime_report_2026-07-02.json`, `examples/data/power_ops_planner_skill_tool_memory_fixture.json`
  Safe use: Use as L3 trace-fixture evidence, not production telemetry.
  Draft stub: Use this L3 claim only with evidence from power_ops_multistep_trace_import_results_2026-07-02.json and power_ops_multistep_trace_import_runtime_report_2026-07-02.json.

## §6 Limitations and Next Experiments

**Purpose:** State missing production trace, wall-clock latency, operator workload, and official benchmark gaps.
**Evidence discipline:** Keep future work separated from supported claims.

- Claim (L4): AgentDojo-style and semi-real power trace bridge fixtures are expressible
  Evidence: `docs/power_ops_action_invariance_agentdojo_style_results_2026-07-02.json`, `docs/power_ops_action_invariance_semireal_trace_results_2026-07-02.json`
  Safe use: Use as bridge evidence, not official benchmark superiority.
  Draft stub: Use this L4 claim only with evidence from power_ops_action_invariance_agentdojo_style_results_2026-07-02.json and power_ops_action_invariance_semireal_trace_results_2026-07-02.json.

## Result Readback

| Artifact | Path | Key readback |
|---|---|---|
| power_ops_action_invariance_performance_profile | `docs\power_ops_action_invariance_performance_2026-07-02.json` | suite_count=3; baseline_count=4; best_baseline=fieldwise_repair |
| power_ops_trace_import_summary | `docs\power_ops_trace_import_results_2026-07-02.json` | boundary_count=4; boundary_case_total=4; whole_action_block_rate=0.000; authorized_preservation=1.000; unsafe_removal=1.000 |
| power_ops_trace_import_summary | `docs\power_ops_multistep_trace_import_results_2026-07-02.json` | boundary_count=1; boundary_case_total=1; whole_action_block_rate=0.000; authorized_preservation=1.000; unsafe_removal=1.000; source_type_coverage=1.000 |
| power_ops_planner_skill_tool_memory_summary | `docs\power_ops_planner_skill_tool_memory_results_2026-07-02.json` | cases=2; source_chain_coverage=1.000; authorized_preservation=1.000; unsafe_removal=1.000; whole_action_block_rate=0.000 |

## Revision Rules

- Keep every result sentence attached to one or more evidence artifacts.
- Do not promote fixture evidence into production telemetry evidence.
- Keep wall-clock latency and operator workload as missing-evidence limitations.
