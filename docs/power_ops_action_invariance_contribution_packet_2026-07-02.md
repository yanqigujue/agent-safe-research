# Power-Ops Contribution Packet

**Status:** ready

**Safe headline:** Field-level action invariance for power-operation agents: preserve authorized fields, remove unsupported fields, and keep every paper claim evidence-bound.

| Metric | Value |
|---|---:|
| Claims | 3 |
| Forbidden headline hits | 0 |
| All claims have code evidence | True |
| All claims have result evidence | True |
| All claims have boundary | True |

## Claims

### C1_field_level_authority_witness

The method checks authority at the action-field level and records the minimal capability evidence behind preserved fields.

Why it matters: This narrows runtime supervision from whole-action refusal to auditable field-level authority coverage.

Evidence:
- `docs/power_ops_action_invariance_results_2026-07-02.json`
- `docs/power_ops_action_invariance_claim_to_paragraph_map_2026-07-02.json`
- `docs/power_ops_action_invariance_paragraph_evidence_packets_2026-07-02.json`

Code:
- `formaltrust_platform/experiments/power_ops_action_invariance.py`
- `formaltrust_platform/nodes/afw.py`

Boundaries:
- `not_generic_agent_guardrail_firstness`
- `not_production_telemetry`

### C2_fieldwise_action_invariance

Under strict intervention, fieldwise repair preserves authorized final-action fields while removing unauthorized fields.

Why it matters: This directly targets over-conservatism: safe fields remain executable instead of being lost in whole-action blocking.

Evidence:
- `docs/power_ops_action_invariance_fieldwise_repair_results_2026-07-02.json`
- `docs/power_ops_action_invariance_baseline_grid_2026-07-02.json`
- `docs/power_ops_action_invariance_table_evidence_binding_2026-07-02.json`

Code:
- `formaltrust_platform/experiments/power_ops_action_invariance.py`
- `formaltrust_platform/experiments/power_ops_action_invariance_baselines.py`

Boundaries:
- `fixture_level_result`
- `not_operator_workload_reduction`
- `not_wall_clock_latency`

### C3_non_rag_authority_sources

The authority abstraction can consume skill manifests, tool metadata, memory, prior-step outputs, and approvals, not only RAG documents.

Why it matters: This lets the same action-invariance check apply to skill-driven agents where retrieval is absent or secondary.

Evidence:
- `docs/power_ops_skill_authority_results_2026-07-02.json`
- `docs/power_ops_skill_authority_dataset_audit_2026-07-02.json`
- `docs/power_ops_trace_import_results_2026-07-02.json`
- `docs/power_ops_multistep_trace_import_results_2026-07-02.json`
- `docs/power_ops_planner_skill_tool_memory_results_2026-07-02.json`

Code:
- `formaltrust_platform/experiments/power_ops_trace_import.py`
- `formaltrust_platform/experiments/power_ops_planner_skill_tool_memory.py`
- `formaltrust_platform/experiments/power_ops_action_invariance.py`

Boundaries:
- `not_rag_only`
- `not_deployment_claim`
- `not_official_benchmark_superiority`
