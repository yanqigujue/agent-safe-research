# Iteration 096: Promote Reviewer-Rejection Field Rows Into Paper-Ready Claims

## Goal

Close the gap left by Iteration 095: the reportable table could show `reviewer_rejection x protected_action_field`, but the reviewed paper-claim packet did not yet cite those rows. This iteration makes the reviewer-objection table part of the paper-ready claim chain.

## Updated One-Sentence Thesis

High-risk RAG-agent actions should carry evidence warrants whose field-level legitimacy can be audited not only by condition and prompt protocol, but also by the reviewer objections those fields are meant to answer.

## Current Strongest Contributions

1. **EAIR-Bench.** Benchmark contribution: conditions are organized by evidence-to-action admissibility and explicit reviewer-rejection coverage.
2. **Evidence Warrant / Proof-Carrying Action.** Representation contribution: `(a, W_a)` makes each protected field's evidence support citeable and replayable.
3. **WarrantGuard / EAIR-Gate.** System contribution: field-level verifier outcomes now flow through reportable export, child-table integrity checks, and reviewed paper-ready claims.

## What Changed

- `eair-write-reportable-claim-template` now emits starter claims for every `reviewer_rejection_protected_field_rows.*.warrant_quality_score`.
- Added a red-green test proving that reviewer-rejection protected-field rows produce claim-template entries and pass citation audit.
- Regenerated `reportable_claims_template.json`; it now contains 12 starter claims.
- Expanded `reportable_claims.json` from 6 to 12 author-prepared claims.
- Regenerated the diagnostic citation audit, reviewed `paper_ready_claims.json`, strict paper-ready audit, diagnostic seal, paper-ready strict seal, and both seal verifications.
- Updated active paper narrative so `paper_ready_claims.json` is no longer just field-level; it now includes reviewer-rejection field claims.

## Novelty Pressure Test

| Neighbor | Solves | Remaining difference |
|---|---|---|
| AttriGuard / CausalArmor | Which untrusted context causally affects an action/tool decision. | Our cited claim object is a protected field's warrant quality under an explicit reviewer objection, not merely an influence attribution. |
| PlanGuard / PromptArmor | Plan/prompt consistency, prompt-injection defense, and action-intent checks. | A plan can be consistent while a `risk_report` or `tool` field remains insufficiently warranted; the claim packet now cites those field rows directly. |
| AIRGuard / AgentSentry | Runtime authority, provenance, and execution-integrity boundaries. | Authority can be valid while evidence is stale, single-source, or insufficient; the paper-ready claims target warrant validity, not permission. |
| RAGForensics / RAGChecker / ARES | Source tracing and retrieval/answer quality diagnostics. | The reviewed claims are about action-field warrant quality, including `decision`, `risk_report`, and `tool`, not answer faithfulness. |

## Rejection Simulation

| Rejection | Current answer |
|---|---|
| This is just source attribution. | `paper_ready_claims.json` now contains reviewed claims for `source_attribution_only x decision/risk_report/tool` rows. |
| This is just access control. | The live matrix still includes access-control pressure rows; this iteration ensures analogous reviewer objections can become paper-ready field claims. |
| This is just RAG faithfulness. | The reviewed claims are field-level action warrant claims, not answer-context faithfulness claims. |
| The benchmark is synthetic and overfitted. | The current claims remain fixture-backed and say so; the same claim path is now prepared for the 24-transcript live matrix. |
| The method has too many hand-designed rules. | This iteration adds claim plumbing only. It adds no new verifier rule or score. |
| Novelty over PlanGuard/AttriGuard is unclear. | The paper claim artifact now makes the distinction concrete: reviewer objections are crossed with protected action fields and warrant quality. |

## Current Most Dangerous Rejection Risk

The claim chain is stronger, but live-provider evidence is still absent. `outputs/eair_prompt_protocol_matrix_live/workflow_status/live_workflow_status.json` remains blocked at `live_preflight` because `OPENAI_API_KEY` is not set.

## Claim-to-Artifact Map

| Claim | Artifact / table / test | Status |
|---|---|---|
| Reviewer-rejection protected-field rows can be promoted into starter claims. | `tests/test_mvp.py::test_eair_write_reportable_claim_template_includes_protected_field_claims`; `outputs/eair_warrant_reportable_export/reportable_claims_template.json`. | Tested and regenerated. |
| Reviewer-rejection protected-field rows are now paper-ready reviewed claims. | `outputs/eair_warrant_reportable_export/paper_ready_claims.json`; `outputs/eair_warrant_reportable_export/paper_ready_claim_audit/reportable_claim_citation_audit.json`. | Strict audit passes 12/12. |
| The reviewed claim packet is sealed and verifiable. | `outputs/eair_warrant_reportable_export/paper_ready_claim_bundle_seal/verification/reportable_claim_bundle_seal_verification.json`. | Strict seal verification passes. |
| The underlying table remains integrity-checked against export. | `outputs/eair_warrant_reportable_export/integrity/reportable_export_integrity_audit.json`. | Already passed in Iteration 095 and remains the source export gate. |

## Claims Not Yet Safe To Write

- Live-model reliability of proof-carrying prompts.
- Superiority over official AttriGuard, PlanGuard, PromptArmor, AgentSentry, CausalArmor, AIRGuard, RAGForensics, RAGChecker, or ARES.
- Real-world deployment safety.
- Firstness claims over all RAG evaluation or agent-security benchmarks.
- Any conclusion from the locked live matrix until provider sampling completes and the reviewed claim packet is regenerated from live transcripts.

## Next Killer Experiment

Run the locked 24-transcript live matrix and regenerate the 12-claim packet from live-provider artifacts. The decisive table should report `model x prompt_variant x reviewer_rejection x protected_action_field`, then compare whether proof-carrying and strict proof-carrying prompts improve warrant quality on the objections most likely to cause rejection.

## Verification

- Red test observed: `test_eair_write_reportable_claim_template_includes_protected_field_claims` failed because `reviewer_rejection_protected_field_warrant_quality_1` was missing.
- Focused test after implementation: 1 passed.
- Claim/export focused tests: `18 passed, 40 deselected`.
- `pytest tests\test_eair_bench.py -q`: 45 passed.
- `pytest -q`: 115 passed.
- `python -m compileall formaltrust_platform`: passed.
- `git diff --check -- formaltrust_platform\experiments\eair_bench.py tests\test_mvp.py PAPER_PLAN.md refine-logs\FINAL_PROPOSAL.md outputs\eair_warrant_reportable_export`: no whitespace errors; PowerShell reported the existing LF-to-CRLF warning for `tests/test_mvp.py`.

## Claim Boundary

This iteration strengthens the paper-ready claim chain for reviewer-objection field rows. It does not add live-provider evidence and does not change WarrantGuard verifier behavior.
