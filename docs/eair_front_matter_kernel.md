# EAIR Front Matter Kernel

This file is the copy-facing source for the title, abstract, introduction, and contribution preview of **WarrantGuard: Evidence Warrants for High-Risk RAG-Agent Actions**. It must be used with `docs/eair_claim_ledger.md`; if a sentence exceeds the ledger's current evidence tier, delete or downgrade it before drafting paper prose. Use `docs/eair_design_pattern_spine.md` for the Figure 1 / Algorithm 1 memory hook and component-demotion language.

## Title

**WarrantGuard: Evidence Warrants for High-Risk RAG-Agent Actions**

## One-Sentence Thesis

High-risk RAG-agent actions should execute only when a proof-carrying action `(a, W_a)` shows that retrieved evidence carries bounded field capabilities for the protected fields it governs.

## Claim-Safe Abstract

High-risk RAG agents increasingly turn retrieved evidence into actions: routing a simulation, setting a parameter, bypassing an approval, or writing a risk report. Existing checks can ask whether a tool call is authorized, whether a source influenced the output, whether a generated answer is faithful to retrieved text, whether cited evidence calibrates claim strength, whether environment observations are trustworthy, or whether an action carries a generic certificate. Those checks do not by themselves prove that evidence has authority over a protected action field. We introduce **evidence warrants**, a proof-carrying action representation in which an action records the bounded field capabilities that retrieved evidence has for its decision, tool arguments, approval status, risk level, and risk report. We instantiate this object in **WarrantGuard**, a verifier that checks field-capability consumption through support, freshness, source diversity, conflicts, counter-evidence, and hard action predicates, and we organize **EAIR-Bench** around legitimate versus hijack-style field authority. Current reviewed artifacts show that the reportable pipeline can audit closest-neighbor discriminator rows and that an offline paired fixture can carry a legitimate-vs-hijack contrast with warrant-quality gap `1.0`. Live-provider claims remain blocked until the planned live matrix passes reportability and strict reviewed sealing.

## Introduction Skeleton

1. High-risk RAG agents do not only answer questions; they convert retrieved documents into structured actions that may route a task, select a tool, set parameters, suppress approval, or summarize risk.
2. Tool permission, source attribution, RAG faithfulness, evidence-force calibration, environmental grounding, and generic certificates each answer a useful but insufficient question. Permission asks whether an action is allowed, attribution asks what influenced it, faithfulness asks whether text matches retrieved context, force calibration asks how strongly evidence warrants claim wording, grounding asks whether observations match environment state, and certification asks whether some proof object exists. None proves that evidence carries the field capability consumed by each protected action field.
3. The threat model is evidence-authority laundering, sharpened as evidence-capability laundering: a RAG-specific confused-deputy variant where an attacker shapes retrieved evidence, stale records, near-duplicate sources, conflicts, low-integrity support, or tool descriptions so that evidence with no field capability, or a capability for the wrong field/operation/force/time/provenance scope, governs protected action fields.
4. The design pattern is: retrieved evidence -> proof-carrying action `(a, W_a)` -> WarrantGuard verifies field-capability consumption -> execute, block, replace, or route to review.
5. The current evidence boundary is deliberately narrow: L1 reviewed fixture packets and an offline paired contrast, L2 dry-run prompt-matrix behavior, and no L4 live-provider result until the live workflow moves past the missing `OPENAI_API_KEY` preflight.

## Contribution List

1. **EAIR-Bench: benchmark contribution.** The benchmark object is field-scoped evidence capability. Rows label whether evidence influence over protected fields is capability-bearing or hijack-style, rather than only measuring poison retrieval, answer faithfulness, access permission, source attribution, force calibration, grounding, or certificate presence.
2. **Evidence Warrant / Proof-Carrying Action: representation contribution.** A high-risk action is represented as `(a, W_a)`, where `W_a = (F_a, C_a, S_a, T_a, X_a, H_a)` records the field-capability ledger establishing whether evidence may govern protected fields.
3. **WarrantGuard / EAIR-Gate: system contribution.** The verifier allows execution only when protected fields consume valid evidence capabilities and no hard obligation fails.
4. **Reportable artifact discipline: reproducibility support.** Claim ledgers, reviewed exports, live promotion contracts, and downgrade rules keep paper claims tied to artifacts. This is support infrastructure, not a fourth main novelty claim unless a venue requires a reproducibility contribution.

## Results Preview Allowed Now

- L1 fixture claim packets support the claim that reviewed artifacts can export and audit closest-neighbor discriminator rows.
- L1 offline paired fixtures support the claim that the artifact chain can carry a legitimate-vs-hijack contrast with legitimate quality `1.0`, hijack quality `0.0`, and warrant-quality gap `1.0`.
- L2 dry-run prompt-matrix artifacts support the claim that deterministic proof-carrying prompts can allow legitimate evidence updates while blocking parameter hijacks.
- Live-provider distinction remains a required next experiment and is currently blocked by missing `OPENAI_API_KEY`.

## Must Not Say

- Do not say that WarrantGuard outperforms AttriGuard, PlanGuard, AIRGuard, PromptArmor, AgentSentry, CausalArmor, RAGForensics, RAGChecker, ARES, or any official baseline.
- Do not say that WarrantGuard distinguishes legitimate from hijack influence in live models.
- Do not say that this is the first proof-carrying action or certificate system.
- Do not say that EAIR-Bench proves deployment safety or real-world benchmark realism.
- Do not treat planned live rows, fixture rows, or dry-run behavior as live model behavior.

## Novelty Pressure Boundary

| Neighbor | What it solves | What it does not solve for this paper | Safe WarrantGuard delta |
|---|---|---|---|
| Proof-Carrying Certificates for LLM Pipelines | Assurance cards, Hoare-style action certificates, and action-gate residues. | Field-scoped authority of retrieved RAG evidence over action fields. | Treats certification as insufficient unless it establishes evidence capabilities for each protected field. |
| PCAA | Runtime-neutral proof-carrying action certificates and governance checkpoints. | RAG-specific evidence capabilities for protected action fields. | Specializes the proof-carrying-action payload to evidence warrants over decision, parameters, approval, risk, and report fields. |
| FORCEBENCH / Relevant Is Not Warranted | Citation laundering and evidence-force calibration. | Whether evidence force grants a capability for a protected action field. | Treats force calibration as one dimension of field-capability consumption. |
| EnvTrustBench | Evidence-grounding defects from stale, incorrect, or malicious environment-facing claims. | Which action field consumed which invalid evidence capability. | Localizes environmental overtrust into field-capability laundering. |
| Prism-Reranker | Contribution statements and evidence passages for agentic retrieval. | Whether a useful passage may govern high-risk action fields. | Treats contribution/evidence extraction as input to `W_a`, not field authority. |
| Confused deputy / ambient authority / capability security | Execution-authority separation and capability-scoped permission. | Evidence authority over protected action fields after execution permission is satisfied. | Treats field-scoped evidence capabilities as a separate boundary from credential or tool authority. |
| Tool/MCP capability laundering discussions | Borrowed or escalated execution privilege across tool/agent boundaries. | Retrieved evidence consumed outside its valid field, operation, force, time, provenance, or conflict scope. | Qualifies the threat as evidence-capability laundering rather than tool-capability laundering. |
| MiniScope / ToolPrivBench | Least-privilege tool authorization and over-privileged tool selection. | Least authority for retrieved evidence after tool permission holds. | Defines least privilege for evidence-to-field authority. |
| Causality Laundering / ARM | Causal provenance, denial-aware leakage, and field misuse around tool calls. | RAG evidence capabilities over decisions, parameters, approval, and risk reports. | Targets evidence-capability laundering rather than denial-feedback leakage. |
| AttriGuard | Causal attribution of tool invocations under indirect prompt injection. | Whether attributed evidence has jurisdiction over each protected field. | Treats attribution as an input to field authority, not as the final safety claim. |
| PlanGuard | Planning-based consistency verification against indirect prompt injection. | Field-level evidence warrant obligations for action arguments, approval, and risk reports. | Verifies whether evidence may legitimately influence action fields, not only whether a plan stays consistent. |
| PromptArmor | Prompt-injection detection and sanitization using modern LLM prompting. | Replayable evidence warrants for high-risk action fields. | Moves from contaminated-prompt detection to proof-carrying field support. |
| AgentSentry | Inference-time or provenance-style defenses for compromised agent execution. | Evidence jurisdiction per protected field. | Defines a narrower field-authority object. |
| CausalArmor | Causal ablation guardrails for indirect prompt injection. | Distinguishing legitimate evidence influence from hijack influence through warrant obligations. | Allows legitimate influence when the warrant is valid and blocks unsupported field changes. |
| AIRGuard | Runtime authority control: data may inform, only trusted authority may authorize side effects. | Evidence adequacy for action parameters and risk reports when authority exists. | Complements authority control by asking whether the informing evidence has field jurisdiction. |
| RAGForensics | Traceback of poisoned texts in RAG knowledge bases. | Whether an action field is warranted after retrieval. | Uses poisoning/forensics as neighbor context but targets action-field jurisdiction. |
| RAGChecker | Fine-grained RAG retrieval/generation diagnostics. | High-risk action parameter, approval, and risk-report field jurisdiction. | Moves from RAG response diagnostics to evidence-grounded action execution. |
| ARES | Automated RAG evaluation for context relevance, answer faithfulness, and answer relevance. | Evidence-to-action legitimacy and hard action obligations. | Adds an action-bearing object and verifier beyond answer-level RAG evaluation. |

## Artifact Map

| Claim | Tier | Artifact |
|---|---|---|
| The paper object is field-scoped evidence capability for protected high-risk action fields. | L0 | `docs/eair_claim_ledger.md`, `docs/eair_threat_model_kernel.md`, `docs/eair_warrant_formalism_kernel.md`, `docs/eair_innovation_pressure_test.md` |
| The related-work delta is claim-safe and does not assert prior-work failure. | L0 | `docs/eair_related_work_positioning.md` |
| Reviewed fixture packets can carry reportable closest-neighbor discriminator rows. | L1 | `outputs/eair_warrant_reportable_export/paper_ready_claims.json` |
| Offline paired fixture can carry a legitimate-vs-hijack contrast with gap `1.0`. | L1 | `outputs/eair_warrant_pair_reportable_export/reportable_influence_contrast_pair_table.json` |
| Deterministic dry-run prompts can rehearse the legitimate-vs-hijack contrast. | L2 | `outputs/eair_prompt_protocol_matrix_dry_run/summary/artifact_summary_influence_contrast_table.json` |
| Same-evidence field-capability laundering is pinned in the deterministic benchmark. | L2 | `tests/test_eair_bench.py::test_warrantguard_blocks_same_evidence_field_capability_laundering` |
| Live-provider distinction is not yet reportable. | Blocked | `outputs/eair_prompt_protocol_matrix_live/workflow_status/live_workflow_status.json` |

## Source Anchors Checked

- PCAA: https://arxiv.org/abs/2606.04104
- Proof-Carrying Certificates for LLM Pipelines: https://arxiv.org/abs/2605.16407
- FORCEBENCH / Relevant Is Not Warranted: https://arxiv.org/abs/2605.28044
- EnvTrustBench: https://arxiv.org/abs/2605.08828
- Prism-Reranker: https://arxiv.org/abs/2604.23734
- Confused Deputy / capability security: https://dl.acm.org/doi/10.1145/54289.871709
- Towards Verifiably Safe Tool Use for LLM Agents: https://arxiv.org/abs/2601.08012
- MiniScope: https://arxiv.org/abs/2512.11147
- ToolPrivBench / When Lower Privileges Suffice: https://arxiv.org/html/2606.20023
- Causality Laundering / ARM: https://arxiv.org/abs/2604.04035
- Tool/MCP capability laundering discussion, non-paper security-neighbor anchor: https://github.com/cosai-oasis/secure-ai-tooling/issues/196
- AttriGuard: https://arxiv.org/abs/2603.10749
- PlanGuard: https://arxiv.org/abs/2604.10134
- PromptArmor: https://arxiv.org/abs/2507.15219
- AgentSentry: https://arxiv.org/html/2602.22724v1
- CausalArmor: https://arxiv.org/html/2602.07918v1
- AIRGuard: https://arxiv.org/html/2605.28914v1
- RAGForensics: https://arxiv.org/html/2504.21668v2
- RAGChecker: https://arxiv.org/abs/2408.08067
- ARES: https://arxiv.org/abs/2311.09476
