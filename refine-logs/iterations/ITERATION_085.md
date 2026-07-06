# Iteration 085: Compress Novelty Around Evidence Warrants

## Goal

Stop treating the project as a growing stack of gates, scores, sweeps, and artifact utilities. Recenter the paper on one memorable design pattern: high-risk RAG-agent actions must be proof-carrying.

## Updated One-Sentence Thesis

High-risk RAG-agent actions should not merely be checked for tool permission, source attribution, or answer faithfulness; they should execute only with an evidence warrant proving that the action, arguments, approval status, and risk report are grounded in sufficient, fresh, source-diverse, low-conflict evidence.

## Current Strongest Contributions

1. **EAIR-Bench.** A benchmark for evidence-to-action admissibility, where the label asks whether evidence influence is legitimate or hijack-style.
2. **Evidence Warrant / Proof-Carrying Action.** A replayable artifact `(a, W_a)` that binds action fields to required claims, support paths, source clusters, freshness/currentness, conflict and counter-evidence, and hard action obligations.
3. **WarrantGuard / EAIR-Gate.** A verifier that executes, blocks, or routes high-risk actions based on warrant validity, not merely on retrieved-document attribution or tool permission.

HardGate, EvidenceSufficient, soft EAIR score, robustness sweeps, reportability audits, and claim seals are implementation obligations or appendix infrastructure unless a main-table claim directly uses them.

## Novelty Pressure Test

| Neighbor | Solves | Does not solve as the primary object |
|---|---|---|
| RAGForensics / RAG attribution | Tracks which retrieved text caused answer or output corruption. | Whether a high-risk action field is admissible under sufficient evidence. |
| RAGAS / ARES / RAGChecker | Evaluates answer faithfulness, context relevance, and claim-level RAG behavior. | Tool arguments, approval flags, risk reports, and action-parameter safety. |
| PromptArmor / PlanGuard | Sanitizes indirect prompt injection and checks plans, constraints, or intent consistency. | Whether the action is warranted by fresh, source-diverse, current evidence. |
| AttriGuard / CausalArmor | Attributes tool/action behavior to untrusted context or causal dominance. | Whether evidence influence is legitimate support rather than hijack or insufficiency. |
| AIRGuard / Agent-Sentry / AgentSentry | Enforces runtime authority, execution provenance, or temporal takeover diagnostics. | Evidence sufficiency for allowed high-risk decisions. |
| Evidence-tracing / execution-provenance surveys | Broaden the provenance taxonomy for safe agents. | A concrete proof-carrying action artifact plus benchmark labels and verifier obligations. |

Pressure-test result: do not claim novelty for action attribution, hard runtime gates, source tracing, provenance, or generic agent-security benchmarking. Claim novelty only for the warrant-based evidence-admissibility object and its benchmarked legitimate-vs-hijack distinction.

## Rejection Simulation

| Rejection | Current answer |
|---|---|
| This is just source attribution. | The warrant proves action-field admissibility, not just document responsibility. |
| This is just access control. | Access control allows many allowed-tool or no-tool dangerous decisions; WarrantGuard also checks evidence sufficiency and risk-report integrity. |
| This is just RAG faithfulness. | Faithful claims can still produce unsafe parameters, approval bypasses, or risk downgrades. |
| The benchmark is synthetic and overfitted. | Current claims are explicitly pilot-level; the next decisive experiment must use locked live transcripts and reportability gates. |
| The method has too many hand-designed rules. | The rules instantiate verifier obligations for proof-carrying actions; they are not separate novelty claims. |
| Novelty over PlanGuard/AttriGuard is unclear. | The paper should present them as closest neighbors and frame the gap as evidence-warrant admissibility, not action attribution or plan verification. |

## Claim-to-Artifact Map

| Claim | Artifact / table / test | Current status |
|---|---|---|
| PRE/RHE can false-positive when poison is retrieved but does not influence action. | `outputs/eair_bench_pilot/report.md`, `poison_exposure_no_action_influence`. | Pilot-supported only. |
| Attribution-style blocking can reject legitimate evidence influence. | `outputs/eair_bench_pilot/report.md`, `legitimate_evidence_update`. | Style-baseline only, not official AttriGuard. |
| RAGAS-style faithfulness misses action-parameter risk. | `outputs/eair_bench_pilot/report.md`, `parameter_level_hijack`. | Pilot-supported only. |
| Access control misses evidence-insufficient dangerous decisions. | `outputs/eair_bench_pilot/report.md`, `insufficient_evidence_dangerous_decision`. | Pilot-supported only. |
| WarrantGuard separates protocol adherence from warrant legitimacy. | `outputs/eair_warrant_reportable_export/reportable_results_export.json`; protocol adherence `1.0`, warrant quality `0.0`, gap `1.0`. | Fixture/reportability-supported, not live-provider evidence. |
| Paper-facing claim artifacts can be hash-pinned and strictly reviewed. | `outputs/eair_warrant_reportable_export/paper_ready_claim_audit/reportable_claim_citation_audit.md`; strict seal verification passes. | Artifact-chain claim only. |

## Claims Not Yet Safe To Write

- Superiority over official AttriGuard, CausalArmor, AIRGuard, AgentSentry, Agent-Sentry, PlanGuard, PromptArmor, RAGForensics, RAGChecker, or ARES.
- "First benchmark" or "first proof-carrying action system" before a final citation audit.
- Live-model warrant reliability, because current reportable rows are fixtures or deterministic pilots.
- Deployment safety for power-grid or other real operational agents.
- Official prior-work failure claims without either reproduction or detailed textual audit.

## Next Killer Experiment

Run a locked live-transcript matrix over the smallest decisive slice:

- `legitimate_evidence_update`
- `parameter_level_hijack`
- `insufficient_evidence_dangerous_decision`
- `near_duplicate_single_source_support`
- `stale_trusted_policy_support`
- `superseded_trusted_policy_support`
- `risk_report_downgrade_no_tool`

Compare action-only, proof-carrying, and strict proof-carrying prompts across at least two model families. Report only rows that pass prompt-adherence, WarrantGuard legitimacy, reportability, claim audit, and strict reviewed-claim seal verification.

## Changes Made

- Rewrote the active positioning block in `PAPER_PLAN.md` around the three contribution objects: EAIR-Bench, Evidence Warrant, and WarrantGuard.
- Demoted HardGate, EvidenceSufficient, soft EAIR, robustness sweeps, reportability audits, and claim seals from standalone contributions to verifier obligations or appendix infrastructure.
- Added an explicit closest-neighbor pressure test, rejection simulation, claim-to-artifact map, unsupported-claim boundary, and next killer experiment.

## Claim Boundary

This iteration strengthens paper positioning and claim discipline. It does not add new experimental evidence, reproduce official close-neighbor systems, or prove live-model warrant reliability.
