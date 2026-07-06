# Iteration 086: Block Template Claims From Paper-Ready Review

## Goal

Close a claim-discipline loophole: a claim manifest could pass value/hash checks and be declared `human_reviewed` while the claim text still said `Template claim:`. That weakens the paper because it proves artifact integrity but not paper-ready claim wording.

## Updated One-Sentence Thesis

High-risk RAG-agent actions should execute only with an evidence warrant proving that the action, arguments, approval status, and risk report are grounded in sufficient, fresh, source-diverse, low-conflict evidence; paper claims about those warrants should themselves be tied to reviewed, hash-pinned artifacts rather than placeholder manifests.

## Current Strongest Contributions

1. **EAIR-Bench.** Benchmark object: evidence-to-action admissibility and legitimate-vs-hijack evidence influence.
2. **Evidence Warrant / Proof-Carrying Action.** Representation object: `(a, W_a)` binds action fields to replayable evidence obligations.
3. **WarrantGuard / EAIR-Gate.** System object: verifies hard action obligations and evidence-warrant sufficiency before execution.
4. **Claim-to-artifact discipline.** Supporting infrastructure only: paper-facing claims are structured, citation-audited, self-sealed, and now blocked if the reviewed manifest still carries template claim text.

## Novelty Pressure Test

| Neighbor | Solves | Remaining distinction |
|---|---|---|
| AttriGuard / CausalArmor | Causal attribution or dominance of untrusted context at action/tool points. | WarrantGuard asks whether evidence influence is admissible support, not merely whether it influenced the action. |
| PlanGuard / PromptArmor | Plan consistency, hard constraints, and IPI sanitization. | EAIR-Bench labels evidence sufficiency, freshness/currentness, source diversity, and risk-report grounding. |
| AIRGuard / Agent-Sentry / AgentSentry | Runtime authority, provenance, and temporal takeover. | The object here is a proof-carrying evidence artifact for allowed high-risk actions. |
| RAGForensics / RAGChecker / ARES | RAG traceback and answer/claim evaluation. | These do not make high-risk action fields carry replayable warrants. |

Pressure-test result: the claim-manifest work is not a standalone novelty contribution. It is useful only because it prevents the WarrantGuard paper from citing placeholder text as if it were a reviewed scientific claim.

## Rejection Simulation

| Rejection | Current answer |
|---|---|
| This is just source attribution. | The reviewed claims now cite action-warrant metrics and protocol-legitimacy gaps, not only source responsibility. |
| This is just access control. | The cited reportable row concerns warrant quality and evidence insufficiency after reportability checks, not permission alone. |
| This is just RAG faithfulness. | The paper-ready chain points to WarrantGuard action legitimacy and protocol-vs-legitimacy gaps. |
| The benchmark is synthetic and overfitted. | Still a live risk; the refreshed claims explicitly remain fixture/reportability claims, not live-model claims. |
| The method has too many hand-designed rules. | This iteration removes a weak artifact path instead of adding a new method component. |
| Novelty over PlanGuard/AttriGuard is unclear. | The next live matrix must compare against action-only/proof-carrying prompting and closest-neighbor style baselines without claiming official failures. |

## Claim-to-Artifact Map

| Claim | Artifact / table / test | Status |
|---|---|---|
| Template claim text cannot be promoted to paper-ready review. | `test_eair_audit_reportable_claims_require_reviewed_rejects_template_manifest`; `record_reportable_claim_review` rejects `Template claim:` text. | Code/test-supported. |
| Paper-ready fixture claims no longer contain placeholder text. | `outputs/eair_warrant_reportable_export/paper_ready_claims.json`. | Artifact-supported. |
| Strict paper-ready claim audit still passes after replacing template text. | `outputs/eair_warrant_reportable_export/paper_ready_claim_audit/reportable_claim_citation_audit.json`, 3/3 claims passed. | Artifact-supported. |
| Strict paper-ready claim bundle seal verifies the refreshed reviewed manifest. | `outputs/eair_warrant_reportable_export/paper_ready_claim_bundle_seal/verification/reportable_claim_bundle_seal_verification.json`. | Artifact-supported. |

## Claims Not Yet Safe To Write

- Live-model WarrantGuard reliability.
- Superiority over official AttriGuard, CausalArmor, AIRGuard, AgentSentry, Agent-Sentry, PlanGuard, PromptArmor, RAGForensics, RAGChecker, or ARES.
- Any claim that reviewed-manifest integrity proves scientific importance or external validity.
- Any deployment safety claim.

## Next Killer Experiment

Use the refreshed claim gate as the final reporting filter for the locked live-transcript matrix. The experiment should only admit paper claims whose rows pass prompt adherence, WarrantGuard legitimacy, reportability, source-hash integrity, reviewed-claim verification, strict claim audit, and strict seal verification.

## Changes Made

- Added a `record_reportable_claim_review` check that rejects source claims whose text still starts with `Template claim:`.
- Updated tests so passing review declarations use paper-facing claim text and the template-leak path is explicitly rejected.
- Rewrote the local reportable claim fixture from template text to author-prepared paper claims.
- Refreshed diagnostic claim audit, reviewed claim declaration, review verification, strict claim audit, strict claim bundle seal, and strict seal verification.
- Documented the new boundary in `docs/eair_artifact_readme.md` and `PAPER_PLAN.md`.

## Claim Boundary

This iteration improves paper-claim discipline and artifact review integrity. It does not add new model behavior evidence or reduce the need for live-model and closest-neighbor experiments.
