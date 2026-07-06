# Power-Ops Action Invariance

This README tracks the first runnable slice of the power large-model safety plan in `task_plan.md`.

## Goal

Build a FormalTrust-compatible research slice for power-operation LLM agents where a safety guardrail preserves authorized action fields while blocking, abstaining, or routing unauthorized fields to human review.

Plain version:

> A power agent may answer, summarize, cite, format, or schedule when it has the right authority. It must not silently turn that authority into dispatch, energization, private data access, certification, or approval waiver authority.

## Current Artifacts

| Artifact | Path |
|---|---|
| Formal model | `docs/power_ops_action_invariance_formal_model_2026-07-02.md` |
| Test framework note | `docs/power_ops_action_invariance_test_framework_2026-07-02.md` |
| Sample catalog | `docs/power_ops_action_invariance_sample_catalog_2026-07-02.md` |
| Strict-block results | `docs/power_ops_action_invariance_results_2026-07-02.md` |
| Fieldwise-repair results | `docs/power_ops_action_invariance_fieldwise_repair_results_2026-07-02.md` |
| Strict vs repair comparison | `docs/power_ops_action_invariance_repair_comparison_2026-07-02.md` |
| Repair validity note | `docs/power_ops_action_invariance_repair_validity_2026-07-02.md` |
| Trace repair note | `docs/power_ops_action_invariance_trace_repair_2026-07-02.md` |
| Trace repair results | `docs/power_ops_action_invariance_trace_repair_results_2026-07-02.md` |
| Span/OTLP repair note | `docs/power_ops_action_invariance_span_otlp_repair_2026-07-02.md` |
| Span/OTLP repair results | `docs/power_ops_action_invariance_span_otlp_repair_results_2026-07-02.md` |
| Literature review | `docs/power_ops_action_invariance_lit_review_2026-07-02.md` |
| Novelty firewall | `docs/power_ops_action_invariance_novelty_firewall_2026-07-02.md` |
| Baseline grid | `docs/power_ops_action_invariance_baseline_grid_2026-07-02.md` |
| Human-review burden | `docs/power_ops_action_invariance_human_review_burden_2026-07-02.md` |
| Severity-weighted review | `docs/power_ops_action_invariance_severity_weighted_review_2026-07-02.md` |
| AgentDojo-style mapping | `docs/power_ops_action_invariance_agentdojo_style_mapping_2026-07-02.md` |
| AgentDojo-style results | `docs/power_ops_action_invariance_agentdojo_style_results_2026-07-02.md` |
| Semi-real trace replay | `docs/power_ops_action_invariance_semireal_trace_2026-07-02.md` |
| Semi-real trace results | `docs/power_ops_action_invariance_semireal_trace_results_2026-07-02.md` |
| Claim ledger | `docs/power_ops_action_invariance_claim_ledger_2026-07-02.md` |
| Paper kernel | `docs/power_ops_action_invariance_paper_kernel_2026-07-02.md` |
| Paper outline / artifact map | `docs/power_ops_action_invariance_paper_outline_2026-07-02.md` |
| Evidence-bound draft skeleton | `docs/power_ops_action_invariance_draft_skeleton_2026-07-02.md` |
| Evidence-constrained prose draft | `docs/power_ops_action_invariance_prose_draft_2026-07-02.md` |
| Numeric claim audit | `docs/power_ops_action_invariance_numeric_claim_audit_2026-07-02.md` |
| Table evidence binding | `docs/power_ops_action_invariance_table_evidence_binding_2026-07-02.md` |
| Residual numeric triage | `docs/power_ops_action_invariance_residual_numeric_triage_2026-07-02.md` |
| Paper claim readiness | `docs/power_ops_action_invariance_paper_claim_readiness_2026-07-02.md` |
| Claim ledger readiness | `docs/power_ops_action_invariance_claim_ledger_readiness_2026-07-02.md` |
| Readiness-bound abstract skeleton | `docs/power_ops_action_invariance_readiness_bound_abstract_2026-07-02.md` |
| Evidence-bound abstract prose | `docs/power_ops_action_invariance_evidence_bound_abstract_2026-07-02.md` |
| Evidence-bound introduction outline | `docs/power_ops_action_invariance_evidence_bound_intro_2026-07-02.md` |
| Evidence-bound introduction prose | `docs/power_ops_action_invariance_evidence_bound_intro_prose_2026-07-02.md` |
| Evidence-bound method outline | `docs/power_ops_action_invariance_evidence_bound_method_outline_2026-07-02.md` |
| Evidence-bound method prose | `docs/power_ops_action_invariance_evidence_bound_method_prose_2026-07-02.md` |
| Evidence-bound related-work outline | `docs/power_ops_action_invariance_evidence_bound_related_work_outline_2026-07-02.md` |
| Evidence-bound related-work prose | `docs/power_ops_action_invariance_evidence_bound_related_work_prose_2026-07-02.md` |
| Evidence-bound results outline | `docs/power_ops_action_invariance_evidence_bound_results_outline_2026-07-02.md` |
| Evidence-bound results prose | `docs/power_ops_action_invariance_evidence_bound_results_prose_2026-07-02.md` |
| Evidence-bound limitations outline | `docs/power_ops_action_invariance_evidence_bound_limitations_outline_2026-07-02.md` |
| Evidence-bound limitations prose | `docs/power_ops_action_invariance_evidence_bound_limitations_prose_2026-07-02.md` |
| Evidence-bound evaluation setup | `docs/power_ops_action_invariance_evidence_bound_evaluation_setup_2026-07-02.md` |
| Evidence-bound conclusion | `docs/power_ops_action_invariance_evidence_bound_conclusion_2026-07-02.md` |
| Evidence-bound paper draft | `docs/power_ops_action_invariance_evidence_bound_paper_draft_2026-07-02.md` |
| Paper draft consistency audit | `docs/power_ops_action_invariance_paper_draft_consistency_audit_2026-07-02.md` |
| Claim-to-paragraph map | `docs/power_ops_action_invariance_claim_to_paragraph_map_2026-07-02.md` |
| Paragraph evidence packets | `docs/power_ops_action_invariance_paragraph_evidence_packets_2026-07-02.md` |
| Paper draft edit gate | `docs/power_ops_action_invariance_paper_draft_edit_gate_2026-07-02.md` |
| LaTeX manuscript | `paper/power_ops_action_invariance/main.tex` |
| LaTeX compile audit | `docs/power_ops_action_invariance_latex_compile_audit_2026-07-02.md` |
| Citation scaffold | `docs/power_ops_action_invariance_citation_scaffold_2026-07-02.md` |
| BibTeX scaffold | `paper/power_ops_action_invariance/references_scaffold.bib` |
| Citation metadata seed | `docs/power_ops_action_invariance_primary_metadata_seed_2026-07-02.json` |
| Citation metadata audit | `docs/power_ops_action_invariance_citation_metadata_audit_2026-07-02.md` |
| Checked BibTeX | `paper/power_ops_action_invariance/references_checked.bib` |
| LaTeX citation gate | `docs/power_ops_action_invariance_latex_citation_gate_2026-07-02.md` |
| Contribution packet | `docs/power_ops_action_invariance_contribution_packet_2026-07-02.md` |
| Figure/table package | `docs/power_ops_action_invariance_figure_table_package_2026-07-02.md` |
| Architecture figure | `figures/power_ops_action_invariance_architecture.svg` |
| Repair-frame figure | `figures/power_ops_action_invariance_repair_frame.svg` |
| Evidence ladder figure | `figures/power_ops_action_invariance_result_ladder.svg` |
| Expanded dataset audit | `docs/power_ops_action_invariance_expanded_dataset_audit_2026-07-02.md` |
| Expanded results | `docs/power_ops_action_invariance_expanded_results_2026-07-02.md` |
| Expanded runtime report | `docs/power_ops_action_invariance_expanded_runtime_report_2026-07-02.md` |
| Metamorphic tests | `docs/power_ops_action_invariance_metamorphic_tests_2026-07-02.md` |
| Metamorphic runtime report | `docs/power_ops_action_invariance_metamorphic_runtime_report_2026-07-02.md` |
| Skill authority model | `docs/power_ops_skill_authority_model_2026-07-02.md` |
| Skill authority audit | `docs/power_ops_skill_authority_dataset_audit_2026-07-02.md` |
| Skill authority results | `docs/power_ops_skill_authority_results_2026-07-02.md` |
| Skill authority runtime report | `docs/power_ops_skill_authority_runtime_report_2026-07-02.md` |
| Performance profile | `docs/power_ops_action_invariance_performance_2026-07-02.md` |
| Trace import contract | `docs/power_ops_trace_import_contract_2026-07-02.md` |
| Trace import results | `docs/power_ops_trace_import_results_2026-07-02.md` |
| Trace import runtime report | `docs/power_ops_trace_import_runtime_report_2026-07-02.md` |
| Multi-step trace import results | `docs/power_ops_multistep_trace_import_results_2026-07-02.md` |
| Multi-step trace import runtime report | `docs/power_ops_multistep_trace_import_runtime_report_2026-07-02.md` |
| Planner-skill-tool-memory results | `docs/power_ops_planner_skill_tool_memory_results_2026-07-02.md` |
| Planner-skill-tool-memory runtime report | `docs/power_ops_planner_skill_tool_memory_runtime_report_2026-07-02.md` |
| Normal-behavior stress results | `docs/power_ops_normal_behavior_stress_results_2026-07-02.md` |
| Normal-behavior stress runtime report | `docs/power_ops_normal_behavior_stress_runtime_report_2026-07-02.md` |
| External 50-case results | `docs/power_ops_external_case_50_results_2026-07-02.md` |
| External 50-case HTML report | `docs/power_ops_external_case_50_results_2026-07-02.html` |
| Trace-derived authority-confusion results | `docs/power_ops_trace_authority_confusion_results_2026-07-02.md` |
| Runtime overhead audit | `docs/power_ops_runtime_overhead_audit_2026-07-02.md` |
| Authority-confusion baseline grid | `docs/power_ops_authority_confusion_baseline_grid_2026-07-02.md` |
| Statistical robustness summary | `docs/power_ops_statistical_robustness_2026-07-02.md` |
| Paper figure/table package | `docs/power_ops_paper_figure_table_package_2026-07-02.md` |
| Metric implementation | `formaltrust_platform/experiments/power_ops_action_invariance.py` |
| Baseline implementation | `formaltrust_platform/experiments/power_ops_action_invariance_baselines.py` |
| Dataset audit implementation | `formaltrust_platform/experiments/power_ops_action_invariance_dataset_audit.py` |
| Metamorphic implementation | `formaltrust_platform/experiments/power_ops_action_invariance_metamorphic.py` |
| Performance implementation | `formaltrust_platform/experiments/power_ops_action_invariance_perf.py` |
| Trace import implementation | `formaltrust_platform/experiments/power_ops_trace_import.py` |
| Planner-skill-tool-memory implementation | `formaltrust_platform/experiments/power_ops_planner_skill_tool_memory.py` |
| Normal-behavior stress implementation | `formaltrust_platform/experiments/power_ops_normal_behavior_stress.py` |
| External 50-case implementation | `formaltrust_platform/experiments/power_ops_external_case_50.py` |
| Trace-derived authority-confusion implementation | `formaltrust_platform/experiments/power_ops_trace_authority_confusion.py` |
| Runtime overhead audit implementation | `formaltrust_platform/experiments/power_ops_runtime_overhead_audit.py` |
| Authority-confusion baseline-grid implementation | `formaltrust_platform/experiments/power_ops_authority_confusion_baseline_grid.py` |
| Statistical robustness implementation | `formaltrust_platform/experiments/power_ops_statistical_robustness.py` |
| Paper figure/table package implementation | `formaltrust_platform/experiments/power_ops_paper_figure_table_package.py` |
| Paper artifact-map implementation | `formaltrust_platform/experiments/power_ops_paper_artifact_map.py` |
| Draft skeleton implementation | `formaltrust_platform/experiments/power_ops_draft_skeleton.py` |
| Prose draft implementation | `formaltrust_platform/experiments/power_ops_prose_draft.py` |
| Numeric audit implementation | `formaltrust_platform/experiments/power_ops_numeric_claim_audit.py` |
| Table evidence binding implementation | `formaltrust_platform/experiments/power_ops_table_evidence_binding.py` |
| Residual numeric triage implementation | `formaltrust_platform/experiments/power_ops_residual_numeric_triage.py` |
| Paper claim readiness implementation | `formaltrust_platform/experiments/power_ops_paper_claim_readiness.py` |
| Claim ledger readiness implementation | `formaltrust_platform/experiments/power_ops_claim_ledger_readiness.py` |
| Readiness-bound abstract implementation | `formaltrust_platform/experiments/power_ops_readiness_bound_abstract.py` |
| Evidence-bound abstract implementation | `formaltrust_platform/experiments/power_ops_evidence_bound_abstract.py` |
| Evidence-bound introduction implementation | `formaltrust_platform/experiments/power_ops_evidence_bound_intro.py` |
| Evidence-bound introduction prose implementation | `formaltrust_platform/experiments/power_ops_evidence_bound_intro_prose.py` |
| Evidence-bound method outline implementation | `formaltrust_platform/experiments/power_ops_evidence_bound_method_outline.py` |
| Evidence-bound method prose implementation | `formaltrust_platform/experiments/power_ops_evidence_bound_method_prose.py` |
| Evidence-bound related-work outline implementation | `formaltrust_platform/experiments/power_ops_evidence_bound_related_work_outline.py` |
| Evidence-bound related-work prose implementation | `formaltrust_platform/experiments/power_ops_evidence_bound_related_work_prose.py` |
| Evidence-bound results outline implementation | `formaltrust_platform/experiments/power_ops_evidence_bound_results_outline.py` |
| Evidence-bound results prose implementation | `formaltrust_platform/experiments/power_ops_evidence_bound_results_prose.py` |
| Evidence-bound limitations outline implementation | `formaltrust_platform/experiments/power_ops_evidence_bound_limitations_outline.py` |
| Evidence-bound limitations prose implementation | `formaltrust_platform/experiments/power_ops_evidence_bound_limitations_prose.py` |
| Evidence-bound evaluation setup implementation | `formaltrust_platform/experiments/power_ops_evidence_bound_evaluation_setup.py` |
| Evidence-bound conclusion implementation | `formaltrust_platform/experiments/power_ops_evidence_bound_conclusion.py` |
| Evidence-bound paper draft implementation | `formaltrust_platform/experiments/power_ops_evidence_bound_paper_draft.py` |
| Paper draft consistency audit implementation | `formaltrust_platform/experiments/power_ops_paper_draft_consistency_audit.py` |
| Claim-to-paragraph map implementation | `formaltrust_platform/experiments/power_ops_claim_to_paragraph_map.py` |
| Paragraph evidence packet implementation | `formaltrust_platform/experiments/power_ops_paragraph_evidence_packets.py` |
| Paper draft edit gate implementation | `formaltrust_platform/experiments/power_ops_paper_draft_edit_gate.py` |
| LaTeX manuscript implementation | `formaltrust_platform/experiments/power_ops_latex_manuscript.py` |
| LaTeX compile audit implementation | `formaltrust_platform/experiments/power_ops_latex_compile_audit.py` |
| Citation scaffold implementation | `formaltrust_platform/experiments/power_ops_citation_scaffold.py` |
| Citation metadata audit implementation | `formaltrust_platform/experiments/power_ops_citation_metadata_audit.py` |
| LaTeX citation gate implementation | `formaltrust_platform/experiments/power_ops_latex_citation_gate.py` |
| Contribution packet implementation | `formaltrust_platform/experiments/power_ops_contribution_packet.py` |
| Runtime YAML | `examples/power_ops_action_invariance_runtime_validation.yaml` |
| Fieldwise-repair YAML | `examples/power_ops_action_invariance_fieldwise_repair_validation.yaml` |
| Trace-repair YAML | `examples/power_ops_action_invariance_trace_repair_validation.yaml` |
| Span/OTLP repair YAML | `examples/power_ops_action_invariance_span_otlp_repair_validation.yaml` |
| AgentDojo-style YAML | `examples/power_ops_action_invariance_agentdojo_style_validation.yaml` |
| Semi-real trace YAML | `examples/power_ops_action_invariance_semireal_trace_validation.yaml` |
| Expanded YAML | `examples/power_ops_action_invariance_expanded_validation.yaml` |
| Metamorphic YAML | `examples/power_ops_action_invariance_metamorphic_validation.yaml` |
| Skill authority YAML | `examples/power_ops_skill_authority_validation.yaml` |
| Trace import YAML | `examples/power_ops_trace_import_validation.yaml` |
| Multi-step trace import YAML | `examples/power_ops_multistep_trace_import_validation.yaml` |
| Planner-skill-tool-memory YAML | `examples/power_ops_planner_skill_tool_memory_validation.yaml` |
| Normal-behavior stress YAML | `examples/power_ops_normal_behavior_stress_validation.yaml` |
| Runtime cases | `examples/data/power_ops_action_invariance_cases.jsonl` |
| Trace repair cases | `examples/data/power_ops_action_invariance_trace_repair_cases.jsonl` |
| Span/OTLP repair cases | `examples/data/power_ops_action_invariance_span_otlp_repair_cases.json` |
| AgentDojo-style cases | `examples/data/power_ops_action_invariance_agentdojo_style_cases.json` |
| Semi-real trace cases | `examples/data/power_ops_action_invariance_semireal_trace_cases.json` |
| Expanded cases | `examples/data/power_ops_action_invariance_expanded_cases.jsonl` |
| Metamorphic cases | `examples/data/power_ops_action_invariance_metamorphic_cases.jsonl` |
| Skill authority cases | `examples/data/power_ops_skill_authority_cases.jsonl` |
| Trace import fixture | `examples/data/power_ops_trace_import_fixture.json` |
| Multi-step trace import fixture | `examples/data/power_ops_multistep_trace_import_fixture.json` |
| Planner-skill-tool-memory fixture | `examples/data/power_ops_planner_skill_tool_memory_fixture.json` |
| Normal-behavior stress fixture | `examples/data/power_ops_normal_behavior_stress_fixture.json` |
| Trace-derived authority-confusion rows | `examples/data/power_ops_trace_authority_confusion_rows.json` |
| Tests | `tests/test_power_ops_action_invariance.py` |

## Interface Contract

This slice reuses existing FormalTrust and AFW interfaces:

```text
ExperimentRunner
  -> guardrail.afw_capguard
  -> evaluate.afw_runtime
  -> power_ops_action_invariance report helper
```

No new top-level `FormalTrustState` fields are introduced. Intermediate values remain under `metrics`; large report files are written under `docs` or `runs`.

## Metrics

| Metric | Meaning |
|---|---|
| `authorized_field_preservation_rate` | Fraction of authorized fields that remain allowed. |
| `unauthorized_field_prevention_rate` | Fraction of unauthorized fields blocked or abstained. |
| `strict_block_collapse_rate` | Fraction of blocked mixed cases where whole-action blocking would also suppress authorized work. |
| `fieldwise_repair_success_rate` | Fraction of mixed cases where authorized fields are preserved and unauthorized fields are prevented. |
| `whole_action_block_rate` | Fraction of cases whose final action still becomes whole-action human review. |
| `authorized_final_field_preservation_rate` | Fraction of authorized fields still present in the final executable action. |
| `unauthorized_final_field_removal_rate` | Fraction of unauthorized fields removed from the final executable action. |
| `executable_fieldwise_repair_success_rate` | Fraction of mixed cases where final action actually preserves authorized fields and removes unauthorized fields. |
| `repair_frame_validity_rate` | Fraction of repaired final actions that only edit the invalid authority frame. |
| `mean_partial_human_review_fields` | Average number of fields per case routed to local human review. |
| `auto_executable_field_ratio` | Auto-executable fields divided by auto-executable plus partial-review fields. |
| `mean_partial_human_review_severity` | Average severity weight routed to local human review per case. |
| `auto_executable_severity_ratio` | Auto-executable severity divided by auto plus partial-review severity. |
| `witness_log_completeness_rate` | Fraction of runtime fields with witness audit records. |
| `mean_witness_compression_ratio` | Mean audit-context reduction from minimal authority witnesses. |
| `multi_step_source_type_coverage.coverage_rate` | Fraction of required multi-step trace source types covered by an import fixture. |

## Run

Run the focused tests:

```powershell
pytest tests/test_power_ops_action_invariance.py -q
```

Run the wider AFW interface regression used for this slice:

```powershell
pytest tests/test_interfaces.py tests/test_power_ops_action_invariance.py -q
```

Run the runtime validation and write a report:

```powershell
python -m formaltrust_platform.experiments.afw_runtime_suite `
  examples/power_ops_action_invariance_runtime_validation.yaml `
  --suite-id power_ops_action_invariance_runtime `
  --output-stem power_ops_action_invariance_runtime_report_2026-07-02
```

Then summarize action-invariance metrics from the produced run:

```powershell
python -m formaltrust_platform.experiments.power_ops_action_invariance `
  --run-dir runs/<run-id> `
  --out-md docs/power_ops_action_invariance_results_2026-07-02.md `
  --out-json docs/power_ops_action_invariance_results_2026-07-02.json
```

Run the fieldwise-repair variant by switching the config:

```powershell
python -m formaltrust_platform.experiments.power_ops_action_invariance `
  --run-dir runs/<fieldwise-repair-run-id> `
  --suite-id power_ops_action_invariance_fieldwise_repair `
  --out-md docs/power_ops_action_invariance_fieldwise_repair_results_2026-07-02.md `
  --out-json docs/power_ops_action_invariance_fieldwise_repair_results_2026-07-02.json
```

Run the trace-adapter repair replay:

```powershell
python -m formaltrust_platform.experiments.power_ops_action_invariance `
  --run-dir runs/<trace-repair-run-id> `
  --suite-id power_ops_action_invariance_trace_repair `
  --out-md docs/power_ops_action_invariance_trace_repair_results_2026-07-02.md `
  --out-json docs/power_ops_action_invariance_trace_repair_results_2026-07-02.json
```

Run the span/OTLP repair replay:

```powershell
python -m formaltrust_platform.experiments.power_ops_action_invariance `
  --run-dir runs/<span-otlp-repair-run-id> `
  --suite-id power_ops_action_invariance_span_otlp_repair `
  --out-md docs/power_ops_action_invariance_span_otlp_repair_results_2026-07-02.md `
  --out-json docs/power_ops_action_invariance_span_otlp_repair_results_2026-07-02.json
```

## Current Result

Rows below combine the current curated-suite summaries, trace replays, bridge fixtures, expanded cases, skill cases, trace-import summaries, planner-chain cases, and normal-behavior stress cases:

| Mode | Passed | Whole-action block rate | Executable repair success | Repair frame validity |
|---|---:|---:|---:|---:|
| strict-block | 10/10 | 1.000 | 0.000 | 1.000 |
| fieldwise-repair | 10/10 | 0.000 | 1.000 | 1.000 |
| trace-repair | 2/2 | 0.000 | 1.000 | 1.000 |
| span-otlp-repair | 2/2 | 0.000 | 1.000 | 1.000 |
| agentdojo-style | 2/2 | 0.000 | 1.000 | 1.000 |
| semireal-trace | 2/2 | 0.000 | 1.000 | 1.000 |
| expanded-fieldwise | 18/18 | 0.000 | 1.000 | 1.000 |
| metamorphic | 4/4 | 0.000 | 1.000 | 1.000 |
| skill-authority | 8/8 | 0.000 | 1.000 | 1.000 |
| trace-import | 4/4 | 0.000 | 1.000 | 1.000 |
| multistep-trace-import | 1/1 | 0.000 | 1.000 | 1.000 |
| planner-skill-tool-memory | 2/2 | 0.000 | 1.000 | 1.000 |
| normal-behavior-stress | 4/4 | 0.000 | 1.000 | 1.000 |
| external-50-full-agent-cases | 50/50 | 0.000 | 1.000 | 1.000 |

## Baseline Grid

On the 10-case curated power-ops suite:

| Baseline | Authorized final preservation | Unauthorized final removal | Whole-action block | Executable invariance | False allow fields |
|---|---:|---:|---:|---:|---:|
| strict-block | 0.000 | 1.000 | 1.000 | 0.000 | 0.000 |
| fieldwise-decision-only | 0.000 | 1.000 | 1.000 | 0.000 | 0.000 |
| provenance-only | 1.000 | 0.000 | 0.000 | 0.000 | 1.000 |
| fieldwise-repair | 1.000 | 1.000 | 0.000 | 1.000 | 0.000 |

## Performance Profile

The current performance profile treats "performance" as safety-preserving normal behavior, not wall-clock speed:

| Profile | Normal preservation | Safety removal | Whole-action block | Latency proxy | Audit compression |
|---|---:|---:|---:|---:|---:|
| expanded-fieldwise | 1.000 | 1.000 | 0.000 | 36 | 0.500 |
| metamorphic | 1.000 | 1.000 | 0.000 | 8 | 0.688 |
| skill-authority | 1.000 | 1.000 | 0.000 | 16 | 0.500 |

On the curated baseline grid, `fieldwise_repair` is the only current baseline with normal preservation 1.000, safety removal 1.000, whole-action block 0.000, and false allow 0.000.

## Claim Boundary

This is a curated regression slice, not a production deployment claim. It shows that the current AFW runtime path can express, evaluate, and execute a first fieldwise-repair mode in power-operation settings, including block, abstain, canonical trace replay, and span/OTLP replay cases. The current repair includes frame-validity checks and structured partial-human-review fields. The literature pass narrows the safe novelty claim to field-level authority witnesses plus repair-frame action invariance, not generic runtime enforcement or least-privilege agent security. The next iterations should add stronger baselines and real or semi-real power-agent traces.

## Continuous Iteration Queue

The active plan is not finished at the current result. The next default iterations are tracked in `task_plan.md`:

| Round | Focus | Expected hard output |
|---|---|---|
| 14 | Paper kernel / figure-table package | Paper narrative, figure specs, SVG figures, result tables |
| 15 | Large-sample power-ops expansion | Completed: 18-case JSONL suite, dataset audit, expanded results |
| 16 | Action-invariance metamorphic tests | Completed: role/scope/counter/time mutations and preservation metrics |
| 17 | Skill-driven agent security | Completed: skill manifest cases, no-RAG authority model, results |
| 18 | Performance / over-conservatism evaluation | Completed: safety-preserving normal behavior profile |
| 19 | Realistic trace import path | Completed: trace import contract, fixture, runtime results |
| 20 | Paper draft integration | Completed: paper outline and artifact map generated |
| 21 | Draft skeleton / multi-step trace extension | Completed: multi-step source-chain trace import |
| 22 | Evidence-bound draft skeleton | Completed: 11 evidence-bound paragraphs, forbidden hits 0 |
| 23 | Evidence-constrained prose draft | Completed: prose draft with evidence/readback retained |
| 24 | Numeric claim audit | Completed: key numeric readbacks supported; table rows still needed binding |
| 25 | Table row evidence binding | Completed: 18/18 rows fully supported |
| 26 | Numeric audit integration | Completed: table binding support added; `needs_evidence` reduced from 218 to 43 |
| 27 | Residual needs-evidence triage | Completed: 25 context-only, 17 parser-extension, 1 rewrite-needed |
| 28 | Lead-in rewrite / parser refinement | Completed: Current Result lead-in rewritten; rewrite-needed reduced to 0 |
| 29 | Parser-extension cleanup | Completed: baseline/context readback rules added; residual parser-extension reduced to 0 |
| 30 | Context-only exclusion | Completed: structural numbers ignored before unsupported claim count; needs_evidence reduced to 0 |
| 31 | Paper-claim readiness gate | Completed: numeric/table/triage/forbidden checks combined into PASS readiness artifact |
| 32 | Claim-ledger readiness sync | Completed: readiness PASS attached to claim ledger companion and PAPER_PLAN |
| 33 | Readiness-bound abstract skeleton | Completed: abstract/introduction skeleton generated only from paper-ready claims |
| 34 | Evidence-bound abstract prose | Completed: 79-word abstract prose generated with sentence/source-claim binding |
| 35 | Evidence-bound introduction outline | Completed: five-slot introduction outline generated with source-claim binding |
| 36 | Evidence-bound introduction prose | Completed: five bounded introduction paragraphs with paragraph/source-claim binding |
| 37 | Writing-artifact readiness coverage | Completed: readiness forbidden scan now covers 6 current writing artifacts by default |
| 38 | Evidence-bound method outline | Completed: six-slot §3 method outline generated from formal model and paper-ready claims |
| 39 | Method-outline readiness coverage | Completed: readiness forbidden scan now covers 7 current writing artifacts by default |
| 40 | Evidence-bound method prose | Completed: six bounded §3 method paragraphs with formal refs and source-claim binding |
| 41 | Method-prose readiness coverage | Completed: readiness forbidden scan now covers 8 current writing artifacts by default |
| 42 | Evidence-bound related-work outline | Completed: six-slot §2 related-work outline from novelty firewall and literature review |
| 43 | Related-work readiness coverage | Completed: readiness forbidden scan now covers 9 current writing artifacts by default |
| 44 | Evidence-bound related-work prose | Completed: six bounded §2 related-work paragraphs with neighbor/source binding |
| 45 | Related-work prose readiness coverage | Completed: readiness forbidden scan now covers 10 current writing artifacts by default |
| 46 | Evidence-bound results outline | Completed: seven-slot §5 results outline with table/source binding |
| 47 | Results-outline readiness coverage | Completed: readiness forbidden scan now covers 11 current writing artifacts by default |
| 48 | Evidence-bound results prose | Completed: seven bounded §5 results paragraphs with row/source binding |
| 49 | Results-prose readiness coverage | Completed: readiness forbidden scan now covers 12 current writing artifacts by default |
| 50 | Evidence-bound limitations outline | Completed: six-slot §6 limitations outline from forbidden claims and future-work boundaries |
| 51 | Limitations-outline readiness coverage | Completed: readiness forbidden scan now covers 13 current writing artifacts by default |
| 52 | Evidence-bound limitations prose | Completed: six bounded §6 limitations paragraphs with excluded-claim binding |
| 53 | Limitations-prose readiness coverage | Completed: readiness forbidden scan now covers 14 current writing artifacts by default |
| 54 | Paper assembly skeleton refresh | Completed: current bounded section prose assembled into one evidence-bound paper draft artifact |
| 55 | Paper-draft readiness coverage | Completed: readiness forbidden scan now covers 15 current writing artifacts by default |
| 56 | Paper draft consistency audit | Completed: source-link completeness 1.000, text match rate 1.000, unresolved boundary hits 0 |
| 57 | Evidence-bound evaluation setup | Completed: section 4 added from dataset, baseline, trace, table-binding, and draft-audit sources |
| 58 | Assembled draft numeric audit | Completed: numeric audit now scans the assembled draft directly with unsupported=0 |
| 59 | Evidence-bound conclusion | Completed: bounded section 7 conclusion added from paper-ready claims and limitation boundaries |
| 60 | Claim-to-paragraph map | Completed: assembled draft paragraphs now map to source claims, evidence files, and forbidden-claim boundaries |
| 61 | Paragraph evidence compression audit | Completed: paragraph map summarized into reviewer-facing claim packets with source-only row audit |
| 62 | Paper draft edit gate | Completed: draft-map-packet hash chain detects stale paragraph artifacts after unsynchronized edits |
| 63 | Evidence-bound LaTeX manuscript | Completed: assembled bounded draft exported to source-commented LaTeX with edit-gate check |
| 64 | LaTeX compile audit | Completed: TeX file found; compile blocked by missing local LaTeX toolchain and recorded as audit artifact |
| 65 | Citation bibliography scaffold | Completed: BibTeX scaffold generated from local literature table with all metadata marked pending audit |
| 66 | Citation metadata audit | Completed: 10/11 entries confirmed from primary metadata seed; 1 OpenReview entry remains pending; invented references 0 |
| 67 | Cite-ready LaTeX gate | Completed: `main.tex` cites 10 checked keys, uses `references_checked`, and citation gate reports 0 unchecked citations |
| 68 | Contribution packet | Completed: 3 reviewer-facing contribution claims, each bound to code, result evidence, and explicit boundaries |
| 69 | Skill-driven power-agent expansion | Completed: 8-case no-RAG suite covering skill manifest, tool metadata, approval, memory, and prior-step output |
| 70 | Multi-step action-invariance benchmark | Completed: 2-case planner-skill-tool-memory trace benchmark with 5-source chain coverage |
| 71 | Normal-behavior preservation stress test | Completed: 4 fully authorized cases preserve 16/16 fields with false intervention 0.000 and whole-action intervention 0.000 |
| 72 | Authority-confusion generator | Completed: 10 trace-derived role-confusion rows preserve boundaries; CapGuard blocks 1.000 while boundary-scope-only falsely allows 1.000 |
| 73 | Runtime overhead audit | Completed: 6-suite proxy-only audit with 108 field-check units, max 6 checks/case, weighted audit compression 0.587963, and no wall-clock latency claim |
| 74 | Stronger baseline/ablation grid | Completed: authority-confusion grid shows CapGuard blocks role confusion at 1.000 while boundary/provenance-style variants falsely allow at 1.000 and strict-block falsely blocks legal rows at 1.000 |
| 75 | Statistical robustness | Completed: Wilson 95% intervals for normal-field preservation, CapGuard confusion blocking, false-allow risk, boundary-only false allow, and strict-block false block |
| 76 | Paper figures and tables | Completed: 2 evidence-bound SVG figures and 2 LaTeX tables generated from authority-confusion and statistical robustness JSON artifacts |
| 77 | External 50-case authority stress suite | Completed: 50 full agent task cases from NERC Lessons Learned metadata; 350 authorized fields preserved, 50 high-impact unauthorized fields removed, whole-action block 0.000; per-case HTML design report generated |
| 78 | Citation and novelty refresh | Planned: re-audit related work and novelty boundaries before paper claims |
| 79 | Adversarial reviewer pass | Planned: produce kill-argument risks and convert them into fixes |
| 80 | Reviewer-risk fixes | Planned: patch code, samples, tests, or prose based on the risk report |
| 81 | Next-cycle decision | Planned: keep/revise/reject and start the next loop |

Each round must update `task_plan.md`, `findings.md`, `progress.md`, this README, and the claim ledger when claims change.

Continuous iteration plan:

- See `docs/power_ops_action_invariance_continuous_iteration_plan_2026-07-02.md`.
- Default behavior is to continue after each completed round unless the user explicitly pauses or stops the task.
