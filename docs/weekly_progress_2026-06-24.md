# Weekly Progress Summary - 2026-06-24

This week moved the project from a broad RAG-agent safety idea into a sharper paper object:

> High-risk RAG-agent actions should execute only when retrieved evidence has a field-scoped capability to govern the protected action fields it is used for.

The current name for that object is **field-scoped evidence capabilities**. The threat name is **evidence-capability laundering**: a retrieved item is valid evidence for one field, operation, force, time, provenance, or conflict scope, but the agent consumes it as authority for another protected field.

## Figures

| Figure | File | What it says |
|---|---|---|
| 1 | [`figures/weekly_progress_timeline.svg`](../figures/weekly_progress_timeline.svg) | The weekly arc from evidence factory to WarrantGuard to field-scoped evidence capabilities. |
| 2 | [`figures/weekly_contribution_shift.svg`](../figures/weekly_contribution_shift.svg) | The contribution narrowed from broad RAG safety to evidence capabilities over protected fields. |
| 3 | [`figures/weekly_evidence_capability_laundering.svg`](../figures/weekly_evidence_capability_laundering.svg) | The new same-evidence laundering failure mode. |
| 4 | [`figures/weekly_claim_readiness_ladder.svg`](../figures/weekly_claim_readiness_ladder.svg) | Which claims are safe now and which still need live-provider evidence. |

## What Was Built

1. **The paper object was compressed.** Older framing around retrieval-to-action pollution, EAIR, and generic guards has been narrowed into three objects: EAIR-Bench, Evidence Warrant / Proof-Carrying Action `(a, W_a)`, and WarrantGuard / EAIR-Gate.

2. **The novelty hook got sharper.** The current hook is not "better attribution", "better access control", or "better RAG faithfulness". It is: retrieved evidence is not ambient context; it is a bounded capability to change specific protected action fields.

3. **A new deterministic benchmark row was added.** `policy_update::same_evidence_field_capability_laundering` tests whether the same trusted signed policy evidence can be accepted for simulation routing while rejected when laundered into `requires_human_approval=false`, `risk_level=low`, or `risk_report=safe_no_review`.

4. **The paper claim firewall is now explicit.** `docs/eair_claim_ledger.md`, `docs/eair_front_matter_kernel.md`, `docs/eair_related_work_positioning.md`, `docs/eair_threat_model_kernel.md`, `docs/eair_warrant_formalism_kernel.md`, `docs/eair_experiment_spine.md`, and `docs/eair_design_pattern_spine.md` now separate safe design claims from live-provider claims that are not yet supported.

5. **The experiment path is ready but still blocked.** The live matrix is planned as 8 conditions x 3 prompt variants = 24 transcripts, with reportability, review, and seal gates. The current live workflow status remains blocked at `live_preflight` because `OPENAI_API_KEY` is not present.

## Safe Claims Today

- L0: WarrantGuard is a design pattern for proof-carrying high-risk RAG-agent actions.
- L1: The fixture/reportable artifact chain can export audited tables, reviewed claims, and seals.
- L2: Deterministic pilot rows exercise legitimate-vs-hijack contrast and the new same-evidence capability-laundering condition.

## Claims Not Yet Safe

- WarrantGuard distinguishes legitimate evidence influence from hijack influence on live-provider outputs.
- WarrantGuard outperforms PCAA, AttriGuard, PlanGuard, AIRGuard, RAGForensics, RAGChecker, ARES, or other official baselines.
- EAIR-Bench is realistic or non-overfit beyond current fixture/dry-run support.
- Evidence warrants are the first proof-carrying action mechanism.

## Current Research Risk

The main risk is no longer "we do not have a system". The risk is whether the paper can produce a live, sealed, same-model legitimate-vs-hijack pair that proves the object reviewers should remember:

> no valid evidence capability, no protected field update.

The next killer experiment is therefore the locked live matrix, followed by a 9th-condition extension for `same_evidence_field_capability_laundering` if the stronger field-capability headline stays central.

## Next Week

1. Unblock live-provider execution and run the 8-condition x 3-prompt matrix.
2. Require reportable rows, reviewed `paper_ready_claims.json`, strict claim audit, bundle seal, and seal verification before citing any live result.
3. Add the same-evidence capability-laundering condition as the follow-on 9th live condition.
4. Draft the paper around Figure 1 and the memory hook: **No warrant, no high-risk action.**
