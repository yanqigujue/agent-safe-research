# Iteration 088: Sharpen WarrantGuard Threat Model

## Goal

Make the threat model reviewer-ready. The old project language still sounded like generic RAG poisoning or generic power-grid agent safety. The active paper needs a narrower threat model: adversarial or low-integrity evidence causes a structured high-risk action field to be executed without a valid evidence warrant.

## Updated One-Sentence Thesis

High-risk RAG-agent actions should execute only when every protected action field carries an evidence warrant proving sufficient, fresh/current, source-diverse, low-conflict support.

## Current Strongest Contributions

1. **EAIR-Bench.** Benchmark contribution: evidence-to-action admissibility over protected action fields.
2. **Evidence Warrant / Proof-Carrying Action.** Representation contribution: `(a, W_a)` binds action fields to replayable support obligations.
3. **WarrantGuard / EAIR-Gate.** System contribution: verifies hard action obligations, warrant sufficiency, and counter-warrants before execution.

## Threat Model Compression

| Element | Active definition |
|---|---|
| System under test | A RAG agent retrieves documents, emits a structured high-risk action, and may execute, recommend, or route the action. |
| Protected action fields | `decision`, `tool`, `parameters`, `requires_human_approval`, `risk_level`, `risk_report`, and supporting evidence claims. |
| Attacker capability | Influence retrieved documents, stale/superseded records, near-duplicate source clusters, conflicting evidence, tool descriptions, or low-integrity policy/support claims. |
| Trusted boundary | The attacker does not control model weights, WarrantGuard, reportability audits, or the reviewed claim-seal chain. |
| Attack success | A final high-risk action is unsafe, unsupported, approval-bypassing, parameter-violating, risk-downgraded, or justified by insufficient/freshness-invalid/source-collapsed evidence. |
| Warrant obligation | Every protected field in `a` must be backed by sufficient, fresh/current, source-diverse, low-conflict evidence, with counter-evidence and hard-policy violations exposed. |

## Novelty Pressure Test

| Neighbor | Solves | Difference |
|---|---|---|
| AttriGuard / CausalArmor | Action or tool-call causal attribution. | WarrantGuard asks whether evidence influence is legitimate and sufficient for each protected action field. |
| PlanGuard / PromptArmor | Planning consistency, hard constraints, parameter deviation checks, and IPI defenses. | WarrantGuard requires evidence support for the parameter/risk/approval fields, not only consistency with user intent or allowed actions. |
| AIRGuard / Agent-Sentry / AgentSentry | Runtime authority, execution provenance, temporal takeover. | WarrantGuard centers a proof-carrying evidence artifact, not only authority or provenance. |
| RAGForensics / RAGChecker / ARES | Source traceback, RAG diagnostics, answer/claim faithfulness. | They do not require high-risk action fields to carry evidence warrants. |

## Rejection Simulation

| Rejection | Current answer |
|---|---|
| This is just source attribution. | The threat model protects action fields, not only document responsibility. |
| This is just access control. | Allowed-tool and no-tool actions can still be attacks if evidence is insufficient or risk metadata is downgraded. |
| This is just RAG faithfulness. | Faithful claims can still be insufficient for parameters, approval status, and risk reports. |
| The benchmark is synthetic and overfitted. | Current claims remain pilot-level; the live matrix must test the same protected fields under fixed conditions. |
| The method has too many hand-designed rules. | The rules are verifier obligations induced by protected action fields. |
| Novelty over PlanGuard/AttriGuard is unclear. | The threat model now explicitly separates action-field warrant admissibility from action causality and plan consistency. |

## Claim-to-Artifact Map

| Claim | Artifact / table / test | Status |
|---|---|---|
| The active threat model is action-field warrant admissibility. | `PAPER_PLAN.md` WarrantGuard threat model. | Narrative-supported. |
| The proposal boundary uses the same protected-field threat model. | `refine-logs/FINAL_PROPOSAL.md` current threat model. | Narrative-supported. |
| Current pilot cases already cover protected fields such as approval, parameter, risk report, freshness/currentness, and source diversity. | `formaltrust_platform/experiments/eair_bench.py` case/sample definitions; `outputs/eair_bench_pilot/report.md`. | Pilot-supported. |

## Claims Not Yet Safe To Write

- Real-world operational safety.
- Official close-neighbor failures.
- Firstness over all action/provenance/RAG-evaluation work.
- Live-model warrant reliability.

## Next Killer Experiment

Use the threat model as the live-matrix schema: every planned row should name which protected action field is under attack, which warrant obligation should fail or pass, and which rejection it answers.

## Changes Made

- Added a WarrantGuard threat-model table to `PAPER_PLAN.md`.
- Added the same current threat model boundary to `refine-logs/FINAL_PROPOSAL.md`.
- Kept generic RAG poisoning and power-grid framing as background/provenance, not the active threat model.

## Claim Boundary

This iteration sharpens the paper's threat model. It does not add new experiment results or live-provider evidence.
