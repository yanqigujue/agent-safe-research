# Power-Ops Action Invariance Paper Outline

**Title:** Field-Level Action Invariance for Power-Operation LLM Agents
**Venue:** ICLR
**Type:** method + empirical artifact
**Date:** 2026-07-02

**One-sentence contribution:** Strict supervision for high-risk power-operation agents should preserve authorized action fields while removing only fields whose authority needs are not covered by source-derived capabilities.

## Claims-Evidence Matrix

| Claim | Level | Section | Evidence | Safe use |
|---|---|---|---|---|
| fieldwise repair final-action mode exists | L1 | §3 Formal Model and CapGuard | `formaltrust_platform/nodes/afw.py`<br>`tests/test_interfaces.py` | Use with the stated evidence level. |
| curated power-ops fieldwise repair preserves authorized fields and removes unauthorized fields | L2 | §5 Results and Analysis | `docs/power_ops_action_invariance_fieldwise_repair_results_2026-07-02.json` | Use with the stated evidence level. |
| expanded 18-case power-ops fieldwise repair preserves authorized fields and removes unauthorized fields | L2 | §5 Results and Analysis | `docs/power_ops_action_invariance_expanded_results_2026-07-02.json`<br>`docs/power_ops_action_invariance_expanded_dataset_audit_2026-07-02.json` | Use with the stated evidence level. |
| metamorphic authority-confusion tests preserve authorized fields while removing or reviewing mutated unsafe fields | L2 | §5 Results and Analysis | `docs/power_ops_action_invariance_metamorphic_tests_2026-07-02.json`<br>`examples/data/power_ops_action_invariance_metamorphic_cases.jsonl` | Use with the stated evidence level. |
| no-RAG skill-driven fixture lifts skill, tool metadata, approval, memory, and prior-step outputs into field-level capabilities | L2 | §5 Results and Analysis | `docs/power_ops_skill_authority_results_2026-07-02.json`<br>`docs/power_ops_skill_authority_dataset_audit_2026-07-02.json`<br>`docs/power_ops_skill_authority_model_2026-07-02.md` | Use with the stated evidence level. |
| current artifact reports a safety-preserving normal-behavior performance profile | L2 | §5 Results and Analysis | `docs/power_ops_action_invariance_performance_2026-07-02.json` | Use as normal-behavior preservation profile; latency is only a proxy. |
| baseline grid shows strict-block collapse and provenance-only false allow on curated cases | L2 | §5 Results and Analysis | `docs/power_ops_action_invariance_baseline_grid_2026-07-02.json` | Use as ablation evidence on curated cases only. |
| trace/span/OTLP replay feeds fieldwise repair | L3 | §5 Results and Analysis | `docs/power_ops_action_invariance_trace_repair_results_2026-07-02.json`<br>`docs/power_ops_action_invariance_span_otlp_repair_results_2026-07-02.json` | Use with the stated evidence level. |
| trace import fixture covers malformed trace, missing source, duplicate approval, and expired epoch boundaries | L3 | §5 Results and Analysis | `docs/power_ops_trace_import_contract_2026-07-02.md`<br>`docs/power_ops_trace_import_results_2026-07-02.json`<br>`examples/data/power_ops_trace_import_fixture.json` | Use as L3 trace-fixture evidence, not production telemetry. |
| multi-step trace import covers planner, skill, tool metadata, memory, prior-step output, and user approval source chains | L3 | §5 Results and Analysis | `docs/power_ops_multistep_trace_import_results_2026-07-02.json`<br>`docs/power_ops_multistep_trace_import_runtime_report_2026-07-02.json`<br>`examples/data/power_ops_multistep_trace_import_fixture.json`<br>`docs/power_ops_planner_skill_tool_memory_results_2026-07-02.json`<br>`docs/power_ops_planner_skill_tool_memory_runtime_report_2026-07-02.json`<br>`examples/data/power_ops_planner_skill_tool_memory_fixture.json` | Use as L3 trace-fixture evidence, not production telemetry. |
| AgentDojo-style and semi-real power trace bridge fixtures are expressible | L4 | §6 Limitations and Next Experiments | `docs/power_ops_action_invariance_agentdojo_style_results_2026-07-02.json`<br>`docs/power_ops_action_invariance_semireal_trace_results_2026-07-02.json` | Use as bridge evidence, not official benchmark superiority. |

## Section Plan

| Section | Goal | Evidence role |
|---|---|---|
| §0 Abstract | State the action-invariance problem, the fieldwise authority method, and the strongest bounded result. | Summarize L1-L4 evidence without promoting it to production evidence. |
| §1 Introduction | Motivate conservative collapse under strict supervision in power-operation agents. | Use safe claims and forbidden-claim boundary from the claim ledger. |
| §2 Related Work and Novelty Boundary | Position against attribution-only, access-control-only, RAG faithfulness, and generic agent guardrails. | Use the claim ledger to avoid firstness or official-baseline superiority claims. |
| §3 Formal Model and CapGuard | Define Cap(x), Need(s,f), field coverage, minimal authority witnesses, and repair-frame invariance. | Map implementation claims to FormalTrust nodes and tests. |
| §4 Test Framework and Power-Ops Benchmark Slice | Describe curated, expanded, metamorphic, skill-driven, trace, and bridge fixtures. | Bind each fixture to dataset/YAML/report artifacts. |
| §5 Results and Analysis | Report field preservation, unsafe-field removal, over-conservatism, performance profile, and trace-import behavior. | Use result JSON files as the source for every numeric claim. |
| §6 Limitations and Next Experiments | State missing production trace, wall-clock latency, operator workload, and official benchmark gaps. | Keep future work separated from supported claims. |

## Figure And Table Plan

| ID | Type | Description | Data source | Priority |
|---|---|---|---|---|
| Fig. 1 | Architecture | Cap/Need/CapGuard field-level authorization path for power-operation agent actions. | `figures/power_ops_action_invariance_architecture.svg` | HIGH |
| Fig. 2 | Repair frame | Action-invariance repair: preserve authorized fields and remove unauthorized fields. | `figures/power_ops_action_invariance_repair_frame.svg` | HIGH |
| Fig. 3 | Evidence ladder | Claim boundary ladder from implementation to production evidence. | `figures/power_ops_action_invariance_result_ladder.svg` | MEDIUM |
| Table 1 | Main result table | Curated, expanded, metamorphic, skill, trace, and trace-import results. | `docs/power_ops_action_invariance_figure_table_package_2026-07-02.md` | HIGH |
| Table 2 | Over-conservatism profile | Normal behavior preservation versus unsafe-field removal and whole-action blocking. | `docs/power_ops_action_invariance_performance_2026-07-02.json` | HIGH |

## Result Artifacts

| Artifact | Path | Key readback |
|---|---|---|
| power_ops_action_invariance_performance_profile | `docs\power_ops_action_invariance_performance_2026-07-02.json` | suite_count=3; baseline_count=4; best_baseline=fieldwise_repair |
| power_ops_trace_import_summary | `docs\power_ops_trace_import_results_2026-07-02.json` | boundary_count=4; boundary_case_total=4; whole_action_block_rate=0.000; authorized_preservation=1.000; unsafe_removal=1.000 |
| power_ops_trace_import_summary | `docs\power_ops_multistep_trace_import_results_2026-07-02.json` | boundary_count=1; boundary_case_total=1; whole_action_block_rate=0.000; authorized_preservation=1.000; unsafe_removal=1.000; source_type_coverage=1.000 |
| power_ops_planner_skill_tool_memory_summary | `docs\power_ops_planner_skill_tool_memory_results_2026-07-02.json` | cases=2; source_chain_coverage=1.000; authorized_preservation=1.000; unsafe_removal=1.000; whole_action_block_rate=0.000 |

## Forbidden Claims

- first LLM-agent guardrail
- first runtime enforcement framework
- first least-privilege LLM-agent security framework
- solves prompt injection
- proves production safety
- outperforms official neighboring systems
- reduces real human workload without operator-time evidence

## Next Steps

- Draft LaTeX sections from this outline.
- Add real or semi-real multi-step trace import before any production-trace claim.
- Measure wall-clock latency; current latency remains a field-check proxy.
- Run official external benchmarks before any superiority claim.
