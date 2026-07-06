# Power-Ops Evidence-Bound Results Prose

**Status:** ready
**Paper section:** §5 Results and Analysis
**Paragraph count:** 7
**Forbidden claim hits:** 0

## Results Prose

The curated fieldwise-repair row is the first §5 result paragraph: it is framed as field preservation for authorized fields and removal of unauthorized fields, with the claim bounded to the fieldwise-repair result JSON and its fully supported table row.

The expanded, metamorphic, and skill-authority fixtures extend the regression surface across larger case coverage, authority-confusion mutations, and no-RAG skill-driven multi-source authority without turning those fixtures into deployment evidence.

The baseline-grid paragraph should compare coarse intervention behavior with the fieldwise repair frame: strict blocking captures conservative collapse, provenance-only captures unsafe preservation, and fieldwise repair remains a bounded artifact result.

The performance paragraph treats performance as safety-preserving normal behavior under the current fixtures, not as wall-clock latency, human workload reduction, or production operator efficiency.

The trace paragraph groups trace replay, span/OTLP replay, and trace import as fixture evidence that external action records can feed the same fieldwise repair analysis; it does not claim production telemetry.

The multi-step trace paragraph reports source-chain coverage for planner outputs, skills, tool metadata, memory, prior-step output, and user approval as local fixture evidence for multi-source authority accounting.

The results section closes by keeping every empirical statement inside the current curated, bridge, and trace-fixture boundary: no production telemetry, no official neighboring-system superiority claim, no real workload reduction, and no wall-clock latency claim.

## Paragraph Evidence

| Slot | Paragraph | Evidence paths | Table refs | Source claims | Limitation reason |
|---|---|---|---|---|---|
| fieldwise_repair_result | The curated fieldwise-repair row is the first §5 result paragraph: it is framed as field preservation for authorized fields and removal of unauthorized fields, with the claim bounded to the fieldwise-repair result JSON and its fully supported table row. | docs/power_ops_action_invariance_fieldwise_repair_results_2026-07-02.json | Current Result:fieldwise-repair:fully_supported | L2:curated power-ops fieldwise repair preserves authorized fields and removes unauthorized fields |  |
| expanded_metamorphic_skill_results | The expanded, metamorphic, and skill-authority fixtures extend the regression surface across larger case coverage, authority-confusion mutations, and no-RAG skill-driven multi-source authority without turning those fixtures into deployment evidence. | docs/power_ops_action_invariance_expanded_results_2026-07-02.json; docs/power_ops_action_invariance_expanded_dataset_audit_2026-07-02.json; docs/power_ops_action_invariance_metamorphic_tests_2026-07-02.json; examples/data/power_ops_action_invariance_metamorphic_cases.jsonl | Current Result:expanded-fieldwise:fully_supported; Current Result:metamorphic:fully_supported; Current Result:skill-authority:fully_supported | L2:expanded 18-case power-ops fieldwise repair preserves authorized fields and removes unauthorized fields; L2:metamorphic authority-confusion tests preserve authorized fields while removing or reviewing mutated unsafe fields |  |
| baseline_grid | The baseline-grid paragraph should compare coarse intervention behavior with the fieldwise repair frame: strict blocking captures conservative collapse, provenance-only captures unsafe preservation, and fieldwise repair remains a bounded artifact result. | docs/power_ops_action_invariance_baseline_grid_2026-07-02.json | Baseline Grid:strict-block:fully_supported; Baseline Grid:fieldwise-decision-only:fully_supported; Baseline Grid:provenance-only:fully_supported; Baseline Grid:fieldwise-repair:fully_supported | L2:baseline grid shows strict-block collapse and provenance-only false allow on curated cases |  |
| performance_profile | The performance paragraph treats performance as safety-preserving normal behavior under the current fixtures, not as wall-clock latency, human workload reduction, or production operator efficiency. | docs/power_ops_action_invariance_performance_2026-07-02.json | Performance Profile:expanded-fieldwise:fully_supported; Performance Profile:metamorphic:fully_supported; Performance Profile:skill-authority:fully_supported | L2:current artifact reports a safety-preserving normal-behavior performance profile |  |
| trace_replay_and_import | The trace paragraph groups trace replay, span/OTLP replay, and trace import as fixture evidence that external action records can feed the same fieldwise repair analysis; it does not claim production telemetry. | docs/power_ops_action_invariance_trace_repair_results_2026-07-02.json; docs/power_ops_action_invariance_span_otlp_repair_results_2026-07-02.json; docs/power_ops_trace_import_contract_2026-07-02.md; docs/power_ops_trace_import_results_2026-07-02.json; examples/data/power_ops_trace_import_fixture.json | Current Result:trace-repair:fully_supported; Current Result:span-otlp-repair:fully_supported; Current Result:trace-import:fully_supported | L3:trace/span/OTLP replay feeds fieldwise repair; L3:trace import fixture covers malformed trace, missing source, duplicate approval, and expired epoch boundaries |  |
| multi_step_source_chain | The multi-step trace paragraph reports source-chain coverage for planner outputs, skills, tool metadata, memory, prior-step output, and user approval as local fixture evidence for multi-source authority accounting. | docs/power_ops_multistep_trace_import_results_2026-07-02.json; docs/power_ops_multistep_trace_import_runtime_report_2026-07-02.json; examples/data/power_ops_multistep_trace_import_fixture.json; docs/power_ops_planner_skill_tool_memory_results_2026-07-02.json; docs/power_ops_planner_skill_tool_memory_runtime_report_2026-07-02.json; examples/data/power_ops_planner_skill_tool_memory_fixture.json | Current Result:multistep-trace-import:fully_supported | L3:multi-step trace import covers planner, skill, tool metadata, memory, prior-step output, and user approval source chains |  |
| claim_boundary | The results section closes by keeping every empirical statement inside the current curated, bridge, and trace-fixture boundary: no production telemetry, no official neighboring-system superiority claim, no real workload reduction, and no wall-clock latency claim. |  | none | none | No production telemetry; no wall-clock latency claim; no real workload reduction; no official neighboring-system superiority claim. |
