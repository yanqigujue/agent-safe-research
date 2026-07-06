# Power-Ops Claim Ledger Readiness

**Readiness status:** PASS
**Supported claims:** 11
**Paper-ready supported claims:** 11
**Blocked supported claims:** 0

## Readiness Blockers

- none

## Supported Claims

| Claim | Level | Paper ready | Evidence |
|---|---|---:|---|
| fieldwise repair final-action mode exists | L1 | yes | `formaltrust_platform/nodes/afw.py`; `tests/test_interfaces.py` |
| curated power-ops fieldwise repair preserves authorized fields and removes unauthorized fields | L2 | yes | `docs/power_ops_action_invariance_fieldwise_repair_results_2026-07-02.json` |
| expanded 18-case power-ops fieldwise repair preserves authorized fields and removes unauthorized fields | L2 | yes | `docs/power_ops_action_invariance_expanded_results_2026-07-02.json`; `docs/power_ops_action_invariance_expanded_dataset_audit_2026-07-02.json` |
| metamorphic authority-confusion tests preserve authorized fields while removing or reviewing mutated unsafe fields | L2 | yes | `docs/power_ops_action_invariance_metamorphic_tests_2026-07-02.json`; `examples/data/power_ops_action_invariance_metamorphic_cases.jsonl` |
| no-RAG skill-driven fixture lifts skill, tool metadata, approval, memory, and prior-step outputs into field-level capabilities | L2 | yes | `docs/power_ops_skill_authority_results_2026-07-02.json`; `docs/power_ops_skill_authority_dataset_audit_2026-07-02.json`; `docs/power_ops_skill_authority_model_2026-07-02.md` |
| current artifact reports a safety-preserving normal-behavior performance profile | L2 | yes | `docs/power_ops_action_invariance_performance_2026-07-02.json` |
| baseline grid shows strict-block collapse and provenance-only false allow on curated cases | L2 | yes | `docs/power_ops_action_invariance_baseline_grid_2026-07-02.json` |
| trace/span/OTLP replay feeds fieldwise repair | L3 | yes | `docs/power_ops_action_invariance_trace_repair_results_2026-07-02.json`; `docs/power_ops_action_invariance_span_otlp_repair_results_2026-07-02.json` |
| trace import fixture covers malformed trace, missing source, duplicate approval, and expired epoch boundaries | L3 | yes | `docs/power_ops_trace_import_contract_2026-07-02.md`; `docs/power_ops_trace_import_results_2026-07-02.json`; `examples/data/power_ops_trace_import_fixture.json` |
| multi-step trace import covers planner, skill, tool metadata, memory, prior-step output, and user approval source chains | L3 | yes | `docs/power_ops_multistep_trace_import_results_2026-07-02.json`; `docs/power_ops_multistep_trace_import_runtime_report_2026-07-02.json`; `examples/data/power_ops_multistep_trace_import_fixture.json`; `docs/power_ops_planner_skill_tool_memory_results_2026-07-02.json`; `docs/power_ops_planner_skill_tool_memory_runtime_report_2026-07-02.json`; `examples/data/power_ops_planner_skill_tool_memory_fixture.json` |
| AgentDojo-style and semi-real power trace bridge fixtures are expressible | L4 | yes | `docs/power_ops_action_invariance_agentdojo_style_results_2026-07-02.json`; `docs/power_ops_action_invariance_semireal_trace_results_2026-07-02.json` |

## Forbidden Claims

| Claim | Paper ready | Reason |
|---|---:|---|
| first LLM-agent guardrail | no | forbidden_claim |
| first runtime enforcement framework | no | forbidden_claim |
| first least-privilege LLM-agent security framework | no | forbidden_claim |
| solves prompt injection | no | forbidden_claim |
| proves production safety | no | forbidden_claim |
| outperforms official neighboring systems | no | forbidden_claim |
| reduces real human workload without operator-time evidence | no | forbidden_claim |
