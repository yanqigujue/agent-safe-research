# Iteration 106: Add an Offline Paired-Contrast Claim Packet

## Goal

Close the artifact-chain gap for the paper's central legitimate-vs-hijack contrast without pretending to have live-provider evidence. Iteration 105 made closest-neighbor discriminators reportable; this iteration adds a minimal offline paired fixture that produces a non-empty `reportable_influence_contrast_pair_table.*`, reviewed claims, and strict seal verification.

## Updated One-Sentence Thesis

High-risk RAG-agent actions need evidence warrants, and the paper must show both field-level closest-neighbor discriminator evidence and a paired legitimate-vs-hijack warrant-quality contrast before making the main claim.

## Current Strongest Contributions

1. **EAIR-Bench.** Benchmark contribution: evidence influence is evaluated as legitimate or hijack-style at protected action fields, not only as poison retrieval, source attribution, access permission, or answer faithfulness.
2. **Evidence Warrant / Proof-Carrying Action.** Representation contribution: `(a, W_a)` is a high-risk action plus a warrant proving sufficient, fresh, source-diverse, low-conflict support for action fields and risk metadata.
3. **WarrantGuard / EAIR-Gate.** System contribution: the verifier accepts legitimate evidence influence and rejects hijack influence by checking the warrant, not by blocking all influence.

## What Changed

- Added `examples/data/eair_live_pair_reportable_fixture.jsonl`, a two-transcript paired fixture:
  - `policy_update::legitimate_evidence_update`
  - `parameter_setting::parameter_level_hijack`
- Generated a separate offline paired packet:
  - `outputs/eair_warrant_pair_fixture_replay/`
  - `outputs/eair_warrant_pair_fixture_summary/`
  - `outputs/eair_warrant_pair_fixture_audit/`
  - `outputs/eair_warrant_pair_reportable_export/`
- Produced `reportable_influence_contrast_pair_table.json` with `total_rows=1`, legitimate quality `1.0`, hijack quality `0.0`, and pair gap `1.0`.
- Produced `paper_ready_claims.json` with 7 reviewed claims and a boundary stating that the packet proves artifact-chain readiness, not live-provider behavior.
- Updated `PAPER_PLAN.md` and `refine-logs/FINAL_PROPOSAL.md` to distinguish:
  - L1 offline paired fixture packet
  - L2 dry-run contrast
  - missing L3/L4 live-provider paired claim

## Novelty Pressure Test

| Neighbor | Solves | What it does not solve | This iteration's discriminator |
|---|---|---|---|
| AttriGuard / RAGForensics | Attribution or traceback of evidence influence. | Whether evidence influence should be allowed. | Offline pair includes a legitimate influence row that WarrantGuard allows. |
| AIRGuard / access control | Authority and permission checks. | Authorized actions with invalid evidence warrants. | Offline pair includes hijack row with blocked warrant despite tool/action shape. |
| RAGChecker / ARES | Faithfulness and RAG response quality. | Action parameters, approval flags, and risk reports. | Offline pair includes parameter-hijack row with quality `0.0`. |
| PlanGuard | Plan/action consistency. | Evidence sufficiency, freshness, source diversity, and conflict. | Still planned; no PlanGuard-specific reportable pair yet. |
| PCAA | Generic proof-carrying actions and runtime governance. | RAG-specific evidence warrants over source/freshness/conflict obligations. | Still planned; no PCAA-specific reportable pair yet. |
| PromptArmor / AgentSentry / CausalArmor | Injection defense, takeover tracing, and causal shielding. | Preserving legitimate evidence influence while rejecting hijack influence. | Offline pair rehearses this claim but is not live evidence. |

## Rejection Simulation

| Rejection | New answer | Boundary |
|---|---|---|
| This is just source attribution. | The offline pair has one allowed legitimate influence row and one blocked hijack row; the distinction is warrant validity, not source identity. | Still fixture-backed. |
| This is just access control. | The hijack row is blocked by WarrantGuard's hard/warrant failures, not merely by tool permission. | Need live authorized-but-invalid rows. |
| This is just RAG faithfulness. | The hijack row targets action parameters and approval/risk fields; faithfulness alone is not enough. | Need live provider rows. |
| The benchmark is synthetic and overfitted. | The claim boundary now names the packet as an offline paired fixture, preventing overclaiming. | Reviewer can still demand live/external data. |
| Too many hand-designed rules. | The pair packet reports only the warrant-quality gap and closest-neighbor counts, not a growing module list. | Obligation ablations still needed. |
| Novelty over PlanGuard/AttriGuard is unclear. | The artifact now materializes the design pattern: allow legitimate influence, reject hijack influence, report closest-neighbor discriminator rows. | PlanGuard/PCAA reportable pair rows still missing. |

## Current Most Dangerous Rejection Risk

The project now has a reviewed paired-contrast packet, but it is an offline fixture. A reviewer can still reject the main empirical claim until the locked live matrix produces the same paired rows under live-provider sampling and strict reportability.

## Claim-to-Artifact Map

| Claim | Artifact / table / test | Status |
|---|---|---|
| Offline paired fixture produces a non-empty pair table. | `outputs/eair_warrant_pair_reportable_export/reportable_influence_contrast_pair_table.json` with `total_rows=1`. | L1 artifact-chain claim. |
| WarrantGuard quality separates legitimate and hijack influence in the fixture. | `paper_ready_claims.json` claims `pair_fixture_legitimate_warrant_quality`, `pair_fixture_hijack_warrant_quality`, and `pair_fixture_legitimate_hijack_gap`. | Reviewed fixture claim, 7/7 audit passed. |
| Closest-neighbor rows accompany the pair packet. | `reportable_closest_neighbor_discriminator_table.json` with access-control, attribution-only, and RAG-faithfulness rows. | Reviewed fixture counts. |
| The packet is strictly sealed. | `paper_ready_claim_bundle_seal/verification/reportable_claim_bundle_seal_verification.json`, seal `7d22fc8e6cb18c5ce3f385dc693c371bcfbce7ea739f1f2a692b86d215e84885`. | Strict reviewed seal passes. |
| Live-provider paired contrast is ready. | No artifact yet. | Not supported; live workflow is still blocked at preflight. |

## Claims Not Yet Safe To Write

- Live WarrantGuard distinction between legitimate influence and hijack influence.
- Superiority over official AttriGuard, PlanGuard, PromptArmor, AgentSentry, CausalArmor, AIRGuard, RAGForensics, RAGChecker, or ARES.
- Generic proof-carrying action firstness over PCAA.
- PlanGuard/PCAA-specific reportable pair rows.
- Deployment safety.

## Next Killer Experiment

Run the locked live matrix and require it to reproduce the same paired packet shape:

1. Same `model x prompt_variant` has both legitimate and hijack influence rows.
2. `reportable_influence_contrast_pair_table.*` has a positive warrant-quality gap.
3. `reportable_closest_neighbor_discriminator_table.*` includes PCAA, PlanGuard/AttriGuard, access-control, attribution, and RAG-faithfulness objections.
4. The live packet passes reportability, export integrity, claim audit, review verification, and strict seal verification.

If live rows do not populate the pair table, keep the main empirical claim out of the paper.

## Source Check

- PCAA / Proof-Carrying Agent Actions: https://arxiv.org/abs/2606.04104
- AttriGuard: https://arxiv.org/abs/2603.10749
- PlanGuard: https://arxiv.org/abs/2604.10134
- PromptArmor: https://arxiv.org/abs/2507.15219
- CausalArmor: https://arxiv.org/abs/2602.07918
- AgentSentry: https://arxiv.org/abs/2602.22724
- AIRGuard: https://arxiv.org/abs/2605.28914
- RAGForensics: https://arxiv.org/abs/2504.21668
- RAGChecker: https://arxiv.org/abs/2408.08067
- ARES: https://arxiv.org/abs/2311.09476

## Verification

- `python -m formaltrust_platform eair-replay --transcripts examples\data\eair_live_pair_reportable_fixture.jsonl --output-dir outputs\eair_warrant_pair_fixture_replay`: passed, 2 transcripts evaluated.
- `python -m formaltrust_platform eair-summarize-artifacts ... --require-complete-coverage`: passed.
- `python -m formaltrust_platform eair-audit-reportable-run ...`: passed with 2 transcripts and model `provider-live-contrast-model`.
- `python -m formaltrust_platform eair-export-reportable-results ...`: passed.
- `python -m formaltrust_platform eair-audit-reportable-export ...`: passed.
- `python -m formaltrust_platform eair-audit-reportable-claims --claims outputs\eair_warrant_pair_reportable_export\reportable_claims.json ...`: 7/7 passed.
- `python -m formaltrust_platform eair-verify-reportable-claim-review ...`: passed.
- `python -m formaltrust_platform eair-audit-reportable-claims --require-reviewed ...`: 7/7 passed with `review_manifest_payload_sha256_matches=true`.
- `python -m formaltrust_platform eair-verify-reportable-claim-bundle-seal --require-reviewed ...`: passed with seal `7d22fc8e6cb18c5ce3f385dc693c371bcfbce7ea739f1f2a692b86d215e84885`.
- `pytest tests\test_mvp.py -q`: 65 passed.
- `pytest tests\test_eair_bench.py -q`: 45 passed.
- `python -m compileall formaltrust_platform`: passed.
- `pytest -q`: 122 passed.
- `outputs\eair_warrant_pair_reportable_export\reportable_influence_contrast_pair_table.json` has `total_rows=1`, legitimate quality `1.0`, hijack quality `0.0`, and gap `1.0`.
- `outputs\eair_warrant_pair_reportable_export\paper_ready_claims.json` has `review_claim_count=7` and explicitly says the claims do not assert live-provider behavior.
- Live workflow status still reports `Live workflow blocked: live_preflight`.
- Trailing-whitespace scan found no matches.
- `git diff --check` over touched docs, fixture, and paired packet outputs reported no whitespace errors.
