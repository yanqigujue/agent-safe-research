# Power-Ops Action Invariance Claim Ledger

## Purpose

This ledger separates what the current artifact proves from what remains planned or forbidden. It is meant to be the paper-writing safety rail for the action-invariance direction.

## Evidence Levels

| Level | Meaning |
|---|---|
| L0 narrative | Framing or motivation only. No empirical claim. |
| L1 implemented | Code path exists and has focused tests. |
| L2 curated result | Runnable curated suite produces a stable result. |
| L3 trace result | Trace/span/OTLP replay produces a stable result. |
| L4 externality bridge | Non-core benchmark shape or semi-real trace bridge exists. |
| L5 production evidence | Real deployment trace or operator workload data. Not present. |

## Supported Claims

| Claim | Level | Evidence | Safe Wording |
|---|---:|---|---|
| CapGuard can produce fieldwise repaired final actions. | L1 | `formaltrust_platform/nodes/afw.py`; `tests/test_interfaces.py` | "The implementation supports a `fieldwise_repair` final-action mode." |
| The action-invariance reporter measures authorized-field preservation, unsafe-field removal, whole-action block rate, repair validity, witness completeness, and human-review burden. | L1 | `formaltrust_platform/experiments/power_ops_action_invariance.py`; `tests/test_power_ops_action_invariance.py` | "The artifact reports final-action preservation and review-burden metrics." |
| On the 10-case curated power-ops suite, fieldwise repair preserves authorized final fields and removes unauthorized final fields. | L2 | `docs/power_ops_action_invariance_fieldwise_repair_results_2026-07-02.md/json` | "On curated power-operation regression cases, fieldwise repair achieves 1.000 authorized final-field preservation and 1.000 unauthorized final-field removal." |
| On the 18-case expanded power-ops suite, fieldwise repair preserves authorized final fields and removes unauthorized final fields. | L2 | `docs/power_ops_action_invariance_expanded_results_2026-07-02.md/json`; `docs/power_ops_action_invariance_expanded_dataset_audit_2026-07-02.md/json` | "On an expanded 18-case power-operation suite, fieldwise repair achieves 1.000 authorized final-field preservation and 1.000 unauthorized final-field removal." |
| Action-invariance metamorphic tests preserve authorized fields under role, scope, counter-authority, and expired-approval mutations. | L2 | `docs/power_ops_action_invariance_metamorphic_tests_2026-07-02.md/json`; `examples/data/power_ops_action_invariance_metamorphic_cases.jsonl` | "A deterministic metamorphic suite covers four authority-confusion mutations and preserves authorized fields while removing or reviewing mutated unsafe fields." |
| Skill-driven multi-source authority can be represented without RAG in a small fixture. | L2 | `docs/power_ops_skill_authority_results_2026-07-02.md/json`; `docs/power_ops_skill_authority_dataset_audit_2026-07-02.md/json`; `docs/power_ops_skill_authority_model_2026-07-02.md` | "A no-RAG skill-driven fixture lifts skill outputs, tool metadata, user approvals, memory preferences, and prior-step outputs into field-level capabilities while preventing escalation into risk, dispatch, switching, publishing, or approval-waiver authority." |
| The current artifact reports a safety-preserving normal-behavior performance profile. | L2 | `docs/power_ops_action_invariance_performance_2026-07-02.md/json` | "The performance profile compares normal-field preservation, unsafe-field removal, whole-action blocking, review burden, latency proxy, and audit compression across current suites and baselines." |
| Strict-block is safe but over-conservative on the curated mixed-action suite. | L2 | `docs/power_ops_action_invariance_baseline_grid_2026-07-02.md/json` | "In this curated suite, strict-block has whole-action block rate 1.000 and authorized final-field preservation 0.000." |
| Provenance-only is not sufficient for authority safety in the curated suite. | L2 | `docs/power_ops_action_invariance_baseline_grid_2026-07-02.md/json` | "The provenance-only ablation preserves utility but false-allows unauthorized fields in these cases." |
| Fieldwise repair validity can be checked as a frame property. | L2 | `validate_fieldwise_repair_frame`; `docs/power_ops_action_invariance_repair_validity_2026-07-02.md` | "The report checks whether repair edits only the invalid authority frame." |
| Trace-derived actions can pass through fieldwise repair. | L3 | `docs/power_ops_action_invariance_trace_repair_results_2026-07-02.md/json` | "Canonical trace replay supports the same fieldwise-repair path on two curated cases." |
| Span/OTLP trace shapes can feed the same repair path. | L3 | `docs/power_ops_action_invariance_span_otlp_repair_results_2026-07-02.md/json` | "The span/OTLP replay fixture exercises `span_log_v1` and `resourceSpans` inputs." |
| A trace-import fixture exercises malformed events, missing sources, duplicate approvals, and expired epochs. | L3 | `docs/power_ops_trace_import_contract_2026-07-02.md`; `docs/power_ops_trace_import_results_2026-07-02.md/json`; `examples/data/power_ops_trace_import_fixture.json` | "The trace-import fixture covers four import-boundary failures and still preserves authorized final fields while removing unauthorized fields." |
| Planner-skill-tool-memory trace-import fixtures cover planner, skill, tool metadata, memory, prior-step output, and user approval source chains. | L3 | `docs/power_ops_multistep_trace_import_results_2026-07-02.md/json`; `docs/power_ops_multistep_trace_import_runtime_report_2026-07-02.md/json`; `examples/data/power_ops_multistep_trace_import_fixture.json`; `docs/power_ops_planner_skill_tool_memory_results_2026-07-02.md/json`; `docs/power_ops_planner_skill_tool_memory_runtime_report_2026-07-02.md/json`; `examples/data/power_ops_planner_skill_tool_memory_fixture.json` | "The multi-step trace fixtures cover planner/prior-step, skill, tool metadata, memory, and user approval sources while preserving authorized final fields and removing unauthorized switching or public-publish fields." |
| The interface can represent AgentDojo-style task-plus-injection cases. | L4 | `docs/power_ops_action_invariance_agentdojo_style_results_2026-07-02.md/json` | "A small bridge suite maps AgentDojo-style tasks into action fields and authority needs." |
| Semi-real power-operation span traces with severity labels can be evaluated. | L4 | `docs/power_ops_action_invariance_semireal_trace_results_2026-07-02.md/json` | "The semi-real trace fixture evaluates SCADA/incident spans with severity-weighted review burden." |
| The current artifact can report severity-weighted human-review burden. | L2/L4 | `docs/power_ops_action_invariance_severity_weighted_review_2026-07-02.md` | "The artifact separates field-count review burden from severity-weighted review burden." |

## Planned But Not Yet Supported

| Claim | Missing Evidence | Required Next Step |
|---|---|---|
| The method reduces real operator workload. | No operator review-time data. | Collect real or expert-simulated review time per field. |
| The method has low wall-clock overhead. | Current latency is only a field-check proxy. | Measure runtime latency under repeated runs and larger traces. |
| The method generalizes to real power-agent production traces. | Trace import fixture exists, but no production trace export. | Import real/semi-real span or OTLP logs from an actual agent run. |
| The method outperforms official AgentDojo defenses. | No official AgentDojo environment or baseline comparison. | Reproduce a task family and compare against official baselines. |
| The method is calibrated for electric-grid field severity. | Current severity weights are engineering defaults. | Domain expert calibration or historical incident severity mapping. |
| The method handles arbitrary multi-step planners. | A single multi-step source-chain fixture exists, but no branching planner, memory mutation, or delegation chain. | Add multi-step planner traces with branching intermediate tool calls, memory writes, and delegated skill/tool authority. |
| The method generalizes to arbitrary skill-driven agents. | Current skill-driven evidence is an 8-case no-RAG fixture with skill, tool metadata, approval, memory, and prior-step sources. | Add larger skill manifests, multi-skill chains, branching planners, and external skill-agent benchmarks. |

## Forbidden Claims

- "First LLM-agent guardrail."
- "First runtime enforcement framework for agents."
- "First least-privilege LLM-agent security framework."
- "Solves prompt injection."
- "Proves production safety."
- "Outperforms AgentSpec, AgentVisor, AgentSentry, CaMeL, ToolPrivBench, RACG, AgentDojo, or InjecGuard."
- "Reduces real human workload" without operator-time evidence.
- "Severity weights are domain-calibrated" before expert calibration.

## Paper-Ready Contribution Shape

A safe contribution list right now:

1. A field-level authority and action-invariance formulation for high-risk power-operation agent actions.
2. A FormalTrust implementation of fieldwise repair with repair-frame validity checks.
3. A curated power-ops regression suite plus trace/span/OTLP, trace-import, planner-skill-tool-memory source-chain, and AgentDojo-style bridge fixtures.
4. Metrics for final-action preservation, unsafe-field removal, whole-action collapse, review burden, and severity-weighted review burden.

## One-Sentence Paper Kernel

> We study field-level action invariance under strict LLM-agent supervision: guard intervention should preserve authorized action fields, remove only fields without valid authority, and expose the residual review burden as auditable field-level evidence.
