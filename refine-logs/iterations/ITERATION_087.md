# Iteration 087: Demote Legacy EAIR-Graph Outline

## Goal

Remove a narrative contradiction: `PAPER_PLAN.md` and `FINAL_PROPOSAL.md` still contained an older outline that framed the graph, `EAIR(q,a)`, and the gate as separate contributions. That framing is too close to RAG attribution, RAG evaluation, access control, and runtime agent guards, and it competes with the current WarrantGuard thesis.

## Updated One-Sentence Thesis

High-risk RAG-agent actions should execute only with an evidence warrant proving that the action, arguments, approval status, and risk report are legitimately grounded in sufficient, fresh, source-diverse, low-conflict evidence; the paper should be organized around proof-carrying actions, not around a list of gates and scores.

## Current Strongest Contributions

1. **EAIR-Bench.** Benchmark contribution for evidence-to-action admissibility and legitimate-vs-hijack evidence influence.
2. **Evidence Warrant / Proof-Carrying Action.** Representation contribution: `(a, W_a)` binds action fields to replayable evidence obligations.
3. **WarrantGuard / EAIR-Gate.** System contribution: verifies hard action obligations, warrant sufficiency, and counter-warrants before execution.

Everything else is demoted unless a main table directly cites it: `HardGate`, `EvidenceSufficient`, soft `EAIR(q,a)`, robustness/reportability utilities, and claim seals.

## Novelty Pressure Test

| Neighbor | Solves | Why the old outline was risky | Current distinction |
|---|---|---|---|
| RAGForensics | Source traceback and poisoned-output attribution. | An "Evidence-to-Action Graph" contribution could sound like source tracing. | WarrantGuard checks action-field admissibility. |
| RAGChecker / ARES | RAG evaluation and answer/claim diagnostics. | `EAIR(q,a)` as a score could sound like another RAG metric. | EAIR-Bench labels whether an action may legitimately use evidence. |
| AttriGuard / CausalArmor | Action/tool causal attribution and dominance. | Document-to-action influence is crowded. | The warrant decides whether influence is sufficient and legitimate. |
| PlanGuard / PromptArmor | Plan/intent consistency and IPI defense. | HardGate-only framing overlaps with constraints and sanitization. | WarrantGuard requires evidence support for action fields, not only plan consistency. |
| AIRGuard / Agent-Sentry / AgentSentry | Runtime authority, provenance, and temporal takeover. | External gate framing sounds like runtime authority/provenance control. | WarrantGuard centers a proof-carrying evidence artifact. |

## Rejection Simulation

| Rejection | Fix in this iteration |
|---|---|
| This is just source attribution. | `PAPER_PLAN.md` now says older graph/source-tracing style framing is superseded. |
| This is just access control. | HardGate is explicitly implementation obligation, not the contribution. |
| This is just RAG faithfulness. | The active outline centers action fields and evidence warrants. |
| The benchmark is synthetic and overfitted. | The outline explicitly limits current evidence to deterministic/fixture-backed pilot claims. |
| The method has too many hand-designed rules. | The contribution list is compressed to three objects; rules are verifier obligations. |
| Novelty over PlanGuard/AttriGuard is unclear. | The active outline makes them closest neighbors and rejects action-attribution novelty. |

## Claim-to-Artifact Map

| Claim | Artifact / table / test | Status |
|---|---|---|
| The active paper plan uses the three-object WarrantGuard contribution stack. | `PAPER_PLAN.md` active outline policy. | Narrative-supported. |
| Older EAIR graph/risk/gate contribution framing is no longer active. | `PAPER_PLAN.md` active outline policy; `refine-logs/FINAL_PROPOSAL.md` current proposal boundary. | Narrative-supported. |
| Current paper claims remain bounded to pilot/fixture evidence. | `PAPER_PLAN.md` claims-not-safe and active outline policy. | Narrative-supported. |

## Claims Not Yet Safe To Write

- "First action-level RAG safety function."
- "First general agent-security benchmark."
- Official AttriGuard, PlanGuard, AIRGuard, AgentSentry, Agent-Sentry, CausalArmor, PromptArmor, RAGForensics, RAGChecker, or ARES failure claims.
- Live-model WarrantGuard reliability.
- Deployment safety.

## Next Killer Experiment

Run the locked live-transcript matrix and report a single table that directly answers the core reviewer challenge: action-only, proof-carrying, and strict proof-carrying prompts under the same EAIR-Bench conditions, admitted only through reportability and strict reviewed-claim gates.

## Changes Made

- Added an active outline policy near the top of `PAPER_PLAN.md`.
- Marked older `Evidence-to-Action Integrity Graph`, `EAIR(q,a)`, `HardGate`, and `Evidence-Action Gate` contribution framing as superseded provenance.
- Added a current proposal boundary to `refine-logs/FINAL_PROPOSAL.md`.

## Claim Boundary

This iteration improves paper coherence and novelty discipline. It does not add new experiment results or official close-neighbor reproductions.
