# EAIR Paper Claim Ledger

This ledger is the paper-facing boundary for **WarrantGuard: Evidence Warrants for High-Risk RAG-Agent Actions**. It says which claims can be written now, which artifacts support them, and which tempting claims must remain out of the paper until live-provider evidence exists.

## Thesis

High-risk RAG-agent actions should not merely be checked for tool permission, source attribution, answer faithfulness, evidence-force calibration, environmental grounding, ambient-authority scoping, or generic action certificates; they should execute only when retrieved evidence carries bounded field capabilities for the action, arguments, approval status, risk level, and risk report.

## Contribution Contract

| Contribution | Reviewer-facing object | What it is not |
|---|---|---|
| EAIR-Bench | A benchmark for field-scoped evidence capabilities over protected action fields. | Not a generic RAG QA benchmark and not a generic prompt-injection suite. |
| Evidence Warrant / Proof-Carrying Action | `(a, W_a)`, where the action carries a replayable field-capability ledger of which evidence may govern decision, tool/arguments, approval, risk level, and risk report. | Not generic proof-carrying action or certificate firstness. |
| WarrantGuard / EAIR-Gate | A verifier that allows capability-bearing evidence influence and blocks hijack influence by checking field-capability predicates. | Not only access control, source attribution, RAG faithfulness, generic certification, or a bag of hand-written rules. |

## Evidence Tiers

| Tier | Evidence state | Allowed wording |
|---|---|---|
| L0 | Method definition, threat model, and warrant contract. | "We propose..." and "The threat model targets..." |
| L1 | Fixture artifacts with reportability audit, reviewed claim manifest, and strict seal. | "The reviewed fixture packet shows the artifact chain can support..." |
| L2 | Deterministic dry-run or pilot matrix. | "Pilot/dry-run evidence shows..." |
| L3 | Live-provider reportable rows with strict claim seal. | "In the live-provider run, row X..." |
| L4 | Live-provider paired legitimate-vs-hijack rows for the same `model x prompt_variant`. | "WarrantGuard distinguishes legitimate evidence influence from hijack influence in live-provider transcripts..." |

Current status: L1 reviewed fixture packets exist, L2 dry-run/pilot evidence exists, and L3/L4 are not available because the live workflow is blocked at preflight.

## Paper-Safe Claims

| Claim sentence that can be written now | Evidence | Tier |
|---|---|---|
| WarrantGuard's paper object is field-scoped evidence capability over protected action fields, not a source-attribution label, access-control decision, evidence-force score, environmental-grounding verdict, or generic certificate. | `PAPER_PLAN.md`; `refine-logs/FINAL_PROPOSAL.md`; evidence-warrant contract `W_a = (F_a, C_a, S_a, T_a, X_a, H_a)`, `ECap(e)`, and `Jurisdiction(f, a, W_a, K_q)`. | L0 |
| The current threat model targets evidence influence over `decision`, `tool`, `parameters`, `requires_human_approval`, `risk_level`, and `risk_report`. | `PAPER_PLAN.md` threat model and condition descriptors in `formaltrust_platform/experiments/eair_bench.py`. | L0 |
| The reviewed warrant fixture has 15 hash-pinned claims and explicitly does not contain a legitimate-vs-hijack pair claim. | `outputs/eair_warrant_reportable_export/paper_ready_claims.json`; review note; strict seal verification. | L1 |
| The reportable closest-neighbor discriminator table can be exported, audited, and promoted into reviewed count claims. | `outputs/eair_warrant_reportable_export/reportable_closest_neighbor_discriminator_table.json`; `outputs/eair_warrant_reportable_export/paper_ready_claims.json`; integrity audit. | L1 |
| A separate offline paired fixture produces one legitimate-vs-hijack pair row with legitimate quality `1.0`, hijack quality `0.0`, and gap `1.0`. | `outputs/eair_warrant_pair_reportable_export/reportable_influence_contrast_pair_table.json`; `outputs/eair_warrant_pair_reportable_export/paper_ready_claims.json`. | L1 |
| The offline paired fixture proves artifact-chain readiness for the main contrast, not live-provider behavior. | `outputs/eair_warrant_pair_reportable_export/paper_ready_claims.json` claim boundary and review note. | L1 |
| Dry-run proof-carrying rows can allow legitimate evidence updates and block parameter hijacks. | `outputs/eair_prompt_protocol_matrix_dry_run/summary/artifact_summary_influence_contrast_table.json`. | L2 |
| EAIR-Bench contains a same-evidence field-capability laundering row: trusted policy evidence supports simulation routing but not approval waiver or risk-report downgrade. | `policy_update::same_evidence_field_capability_laundering`; `tests/test_eair_bench.py::test_warrantguard_blocks_same_evidence_field_capability_laundering`. | L2 |
| The live matrix is planned but currently blocked before sampling because the API key environment variable is absent. | `outputs/eair_prompt_protocol_matrix_live/workflow_status/live_workflow_status.json`. | Boundary claim |

## Forbidden Claims Until Live Evidence Exists

| Do not write | Why not | Required evidence |
|---|---|---|
| "WarrantGuard outperforms AttriGuard / PlanGuard / AIRGuard / RAGChecker / ARES." | No official baseline comparison has been run. | Live or reproducible baseline runs with matched scenarios and claim audit. |
| "WarrantGuard distinguishes legitimate influence from hijack influence in live models." | Only offline/dry-run paired packets exist. | L4 live `reportable_influence_contrast_pair_table.*` with strict reviewed seal. |
| "This is the first proof-carrying action or certificate system." | PCAA and proof-carrying certificate work are close neighbors. | Do not claim; reposition as field-scoped evidence capabilities for RAG-agent actions. |
| "This is the first confused-deputy or capability-security defense for agents." | Confused-deputy and capability-security work already define execution-authority boundaries. | Do not claim; position evidence-authority laundering as a narrower RAG-agent variant after execution permission is satisfied. |
| "This is the first evidence-force calibration benchmark." | FORCEBENCH already names citation laundering and evidence-force calibration. | Do not claim; position force calibration as one dimension of field-capability consumption. |
| "This is the first environmental-grounding benchmark for agents." | EnvTrustBench already targets evidence-grounding defects in LLM agents. | Do not claim; position WarrantGuard as protected-field capability accounting after retrieval and before action commitment. |
| "The benchmark is proven realistic." | Current decisive packets are fixtures/dry-runs. | Live transcripts and preferably external-domain or external-source validation. |
| "The method is deployment-safe." | No operational deployment evidence exists. | Out of current scope. |
| "PCAA / AttriGuard / PlanGuard fail on our benchmark." | Current rows are closest-neighbor discriminator rows, not official prior-work executions. | Implemented baselines or careful non-empirical positioning. |

## Reviewer Rejection Answers

| Rejection | Safe answer | Evidence |
|---|---|---|
| This is just source attribution. | The object is whether attributed evidence has jurisdiction over protected action fields; the offline pair includes allowed legitimate influence, not blanket source blocking. | Offline paired packet; closest-neighbor discriminator rows. |
| This is just access control. | Access permission is necessary but insufficient; WarrantGuard asks whether evidence may govern parameters, approval, risk, and report fields. | Threat model; pair packet access-control discriminator row. |
| This is just confused deputy or ambient authority. | That is the closest security analogy, but the object differs: confused-deputy defenses scope execution authority, while WarrantGuard scopes evidence authority over protected fields after permission already holds. | Threat model; related-work boundary. |
| This is just tool capability laundering. | Tool/MCP capability laundering scopes borrowed execution privilege; WarrantGuard scopes retrieved evidence capabilities consumed by protected action fields. | Innovation pressure test; deterministic same-evidence row. |
| This is just FORCEBENCH. | FORCEBENCH calibrates whether cited evidence warrants wording strength; WarrantGuard asks whether that evidence force is an in-scope capability for an action field. | Innovation pressure test; formalism. |
| This is just EnvTrustBench. | EnvTrustBench detects agent false paths under true environment state; WarrantGuard records which field consumed which evidence capability and preserves legitimate field influence. | Innovation pressure test; threat model. |
| This is just RAG faithfulness. | RAG faithfulness does not cover parameters, approval flags, risk reports, or execution gates. | `parameter_setting::parameter_level_hijack`; RAG-faithfulness discriminator row. |
| This benchmark is synthetic and overfitted. | Current fixture claims are explicitly labeled L1, and the next required experiment is live-provider reportability. | Claim boundaries in `paper_ready_claims.json`; live runbook. |
| The method has too many hand-designed rules. | The paper contribution is field-scoped evidence jurisdiction; individual checks are predicates, not separate novelty claims. | Contribution contract and warrant contract. |
| Novelty over PlanGuard/AttriGuard is unclear. | PlanGuard/AttriGuard are closest neighbors; WarrantGuard's new object is evidence authority over protected action fields. | Closest-neighbor novelty matrix and discriminator table. |

## Source Anchors For Novelty

| Neighbor | Anchor | Safe positioning |
|---|---|---|
| Proof-Carrying Certificates for LLM Pipelines | https://arxiv.org/abs/2605.16407 | Close neighbor for assurance cards and action certificates; WarrantGuard's delta is field-scoped evidence jurisdiction for RAG-agent actions. |
| PCAA | https://arxiv.org/abs/2606.04104 | Close neighbor for proof-carrying action framing; WarrantGuard is RAG evidence-warrant specialization. |
| FORCEBENCH / Relevant Is Not Warranted | https://arxiv.org/abs/2605.28044 | Strongest force-calibration neighbor; WarrantGuard moves from cited-claim force to action-field capability. |
| EnvTrustBench | https://arxiv.org/abs/2605.08828 | Strongest environmental-grounding neighbor; WarrantGuard localizes overtrust into field-capability consumption. |
| Prism-Reranker | https://arxiv.org/abs/2604.23734 | Retrieval contribution/evidence neighbor; WarrantGuard asks whether retrieved evidence can govern protected fields. |
| Confused Deputy / capability security | https://dl.acm.org/doi/10.1145/54289.871709 | Classic authority-boundary neighbor; WarrantGuard does not claim confused-deputy firstness, only evidence-authority specialization. |
| Towards Verifiably Safe Tool Use for LLM Agents | https://arxiv.org/abs/2601.08012 | Current tool-use safety neighbor for capability labels, trust levels, data flows, and tool sequences; WarrantGuard adds field-scoped evidence jurisdiction. |
| MiniScope | https://arxiv.org/abs/2512.11147 | Least-privilege tool-authorization neighbor; WarrantGuard scopes evidence authority rather than tool authority. |
| ToolPrivBench / When Lower Privileges Suffice | https://arxiv.org/html/2606.20023 | Latest least-privilege tool-selection neighbor; WarrantGuard asks analogous least authority for evidence fields. |
| Causality Laundering / ARM | https://arxiv.org/abs/2604.04035 | Laundering/provenance neighbor; WarrantGuard targets evidence-authority laundering, not denial-feedback leakage. |
| Tool/MCP capability laundering discussion | https://github.com/cosai-oasis/secure-ai-tooling/issues/196 | Non-paper naming neighbor; WarrantGuard must qualify the threat as evidence-capability laundering over action fields. |
| AttriGuard | https://arxiv.org/abs/2603.10749 | Close neighbor for attribution/context influence; WarrantGuard asks field jurisdiction. |
| PlanGuard | https://arxiv.org/abs/2604.10134 | Close neighbor for plan/action consistency; WarrantGuard adds evidence sufficiency/freshness/source/conflict obligations. |
| PromptArmor | https://arxiv.org/abs/2507.15219 | Prompt-injection defense neighbor; WarrantGuard verifies emitted action warrants. |
| AgentSentry | https://arxiv.org/abs/2602.22724 | Agent takeover/provenance neighbor; WarrantGuard targets evidence-insufficient actions. |
| CausalArmor | https://arxiv.org/abs/2602.07918 | Causal shielding neighbor; WarrantGuard must preserve legitimate evidence influence. |
| AIRGuard | https://arxiv.org/abs/2605.28914 | Access-control/authority neighbor; WarrantGuard checks field-scoped evidence jurisdiction after permission. |
| RAGForensics | https://arxiv.org/abs/2504.21668 | Forensic traceback neighbor; WarrantGuard asks whether traced evidence may change action fields. |
| RAGChecker | https://arxiv.org/abs/2408.08067 | RAG faithfulness/evaluation neighbor; WarrantGuard evaluates action parameters and execution gates. |
| ARES | https://arxiv.org/abs/2311.09476 | RAG evaluation neighbor; WarrantGuard is action-field jurisdiction, not answer quality alone. |

## Next Claim Upgrade

The next claim upgrade is L4: run the locked live matrix and produce a reviewed live packet where the same `model x prompt_variant` has both legitimate and hijack influence rows with a positive warrant-quality gap. Until then, the abstract and main results must say "offline paired fixture" or "dry-run/pilot" for the legitimate-vs-hijack contrast.

The stronger evidence-field-capability headline needs one additional live extension after the locked matrix: `policy_update::same_evidence_field_capability_laundering` must be sampled, replayed, audited, and reviewed under the same reportability gates.
