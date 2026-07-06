# EAIR Related Work Positioning Kernel

This file is the paper-facing related-work kernel for **WarrantGuard: Evidence Warrants for High-Risk RAG-Agent Actions**. It compresses the nearest-work story into one safe claim: the paper's object is **field-scoped evidence capabilities for protected high-risk action fields**.

It should be used with `docs/eair_claim_ledger.md` and `docs/eair_live_killer_experiment_contract.md`. It does not claim that any official prior-work implementation fails on EAIR-Bench.

## Related-Work Thesis

Existing defenses ask whether an action is authorized, whether context influenced an action, whether a plan is consistent, whether a prompt injection occurred, whether a RAG answer is faithful, whether cited evidence calibrates claim wording, whether environment observations are trustworthy, whether ambient authority has been capability-scoped, or whether an LLM pipeline carries a generic certificate. WarrantGuard asks a different question: whether retrieved evidence carries a bounded field capability that may be consumed by each protected action field in a proof-carrying high-risk action.

## Safe Paragraph Skeleton

Use this structure in the Related Work section:

1. **Proof-carrying certificates, actions, and agent governance.** Proof-carrying certificate work and PCAA make certificate-bearing outputs and proof-carrying actions close neighbors, so this paper must not claim proof-carrying firstness. WarrantGuard's narrower claim is that high-risk RAG-agent actions need field-scoped evidence capabilities: the certificate must show which evidence may govern which protected field.
2. **Evidence-force calibration and environmental grounding.** FORCEBENCH and EnvTrustBench are the strongest new pressure points: they already argue that relevant citations and environment observations can be overtrusted. WarrantGuard narrows the contribution to field-capability consumption: calibrated evidence or grounded observations still must be valid for the protected action field they govern.
3. **Confused deputy, ambient authority, and capability security.** Classic confused-deputy and modern agent-authority work motivate explicit scoping of execution authority. WarrantGuard borrows that security instinct but applies it to a different object: evidence-authority laundering, where retrieved claims gain control over protected fields without field jurisdiction. Because "capability laundering" is also used in tool/MCP security discussions, paper wording should say **evidence-capability laundering** and define the borrowed capability as evidence-to-field authority, not tool privilege.
4. **Attribution, forensics, and causal influence.** AttriGuard, RAGForensics, and causal-influence defenses motivate action-level context influence as an important object. WarrantGuard does not replace attribution; it asks whether the attributed influence carries a field capability for the protected action field.
5. **Plan, prompt, takeover, and authority guards.** PlanGuard, PromptArmor, AgentSentry, CausalArmor, and AIRGuard address plan consistency, prompt injection, takeover provenance, causal shielding, or authority control. WarrantGuard begins after those checks: an authorized or plan-consistent action can still lack field-scoped evidence jurisdiction.
6. **RAG evaluation and faithfulness.** RAGChecker, ARES, Prism-Reranker, and RAGAS-style systems evaluate retrieval, contribution, evidence passages, and answer grounding. EAIR-Bench instead evaluates action parameters, approval flags, risk reports, and execution gates.

## Closest-Neighbor Delta Table

| Neighbor | Solves | Does not solve for this paper | WarrantGuard delta | Current artifact boundary |
|---|---|---|---|---|
| Proof-Carrying Certificates for LLM Pipelines | Assurance cards, Hoare-style action certificates, and action-gate residues across LLM pipelines. | Which retrieved RAG evidence has authority over each action field. | A generic certificate is not enough; the certificate must establish field-scoped evidence jurisdiction. | Narrative boundary only; no failure claim. |
| PCAA | Proof-carrying action framing and verifiable agent governance. | RAG-specific field jurisdiction for action parameters, approval, risk level, and risk report. | Evidence warrant payload `(F_a, C_a, S_a, T_a, X_a, H_a)` specializes proof-carrying actions to field-scoped evidence authority. | Planned live PCAA discriminator only; no PCAA failure claim. |
| FORCEBENCH / Relevant Is Not Warranted | Citation laundering and evidence-force calibration across relation, modality, scope, temporal validity, and numeric specificity. | Whether calibrated evidence force grants authority over a protected action field. | Treat FORCE-style force as one dimension of an evidence field capability. | Narrative boundary only; no FORCEBENCH comparison. |
| EnvTrustBench | Evidence-grounding defects from stale, incorrect, or malicious environment-facing claims. | Which protected action field consumed which evidence capability, and whether legitimate field influence should pass. | Localize environmental overtrust as field-capability laundering. | Narrative boundary only; no EnvTrustBench comparison. |
| Prism-Reranker | Reranking beyond relevance by producing contribution statements and evidence passages. | Whether the passage may govern high-risk action fields. | Contribution/evidence extraction feeds `W_a`; it is not field authority by itself. | Narrative boundary only. |
| Confused deputy / ambient authority / capability security | Execution-authority separation, least privilege, and capability-scoped permission. | Whether retrieved evidence has field authority after execution permission is already satisfied. | WarrantGuard treats evidence-authority laundering as a RAG-specific authority boundary over `decision`, `parameters`, approval, risk, and report fields. | Narrative boundary only; no firstness claim. |
| Tool/MCP capability laundering discussions | How tool execution privilege or tool authority can be borrowed or escalated across agent/tool boundaries. | Whether a trusted retrieved evidence item is consumed outside its valid field, operation, force, time, provenance, or conflict scope. | WarrantGuard narrows the laundering object to evidence capabilities over protected action fields. | Non-paper naming neighbor; deterministic row `same_evidence_field_capability_laundering` is L2 only. |
| MiniScope / ToolPrivBench | Least-privilege authorization and over-privileged tool selection. | Least authority for retrieved evidence after the tool choice is permitted. | WarrantGuard is least privilege for evidence-to-field authority, not tool authority. | Narrative boundary only. |
| Causality Laundering / ARM | Denial-aware causal provenance, transitive dependencies, and field-level misuse around tool calls. | RAG evidence capabilities for protected decisions, parameters, approval, and risk reports. | Different laundering object: evidence authority, not denial-feedback leakage. | Narrative boundary only. |
| AttriGuard | Action-level context attribution and influence analysis. | Whether attributed influence has a capability for the field it changes. | Distinguish legitimate capability-bearing updates from hijack influence. | L2 dry-run and L1 offline pair readiness; live L4 missing. |
| PlanGuard | Plan/action consistency and alignment with isolated intent. | Whether a consistent plan is governed by current independent evidence with field jurisdiction. | Reject plan-consistent actions whose evidence lacks field jurisdiction because support is stale, source-collapsed, insufficient, or conflicted. | Planned live rows; no official PlanGuard comparison. |
| PromptArmor | Prompt-injection detection and defense. | Whether the emitted high-risk action carries field-scoped evidence jurisdiction. | Evaluate the proof-carrying action after retrieval and emission. | Threat-model/narrative boundary only. |
| AgentSentry | Takeover tracing, temporal provenance, and context purification. | Evidence jurisdiction for high-risk decisions that remain within authority. | Target evidence-insufficient dangerous decisions, not only takeover. | Planned live row `insufficient_evidence_dangerous_decision`. |
| CausalArmor | Causal shielding or dominance around privileged actions. | Preserving benign evidence influence while blocking hijack influence. | Main claim is positive separation, not blanket blocking of influence. | Requires same-model live pair row. |
| AIRGuard | Runtime authority, least privilege, and execution control. | Whether evidence has authority over an authorized action's fields. | Permission is a hard precondition; field jurisdiction is the paper object. | Planned live authorized/no-tool rows; no official AIRGuard comparison. |
| RAGForensics | Poison-source traceback and forensic attribution. | Whether traced evidence may change a protected action field. | Separates poison exposure, source attribution, and capability-bearing influence. | L1 source-attribution discriminator rows exist; live missing. |
| RAGChecker / ARES | RAG answer relevance, retrieval quality, and faithfulness-style evaluation. | Action parameters, approval flags, risk reports, and execution gates. | Field-scoped evidence jurisdiction replaces answer-only faithfulness as the measured object. | Planned parameter-hijack and risk-report rows; no official metric comparison. |

## Claims Allowed Now

- "PCAA, AttriGuard, PlanGuard, AIRGuard, RAGForensics, RAGChecker, and ARES are closest or complementary neighbors."
- "Confused-deputy, ambient-authority, and capability-security work are execution-authority neighbors; WarrantGuard's narrower object is evidence authority over action fields."
- "WarrantGuard's distinct object is field-scoped evidence capabilities over protected high-risk action fields."
- "Current reportable fixture artifacts include closest-neighbor discriminator rows for source-attribution and source-diversity objections."
- "The planned live matrix maps each closest-neighbor objection to conditions, protected fields, and warrant obligations."

## Claims To Delete

- "WarrantGuard outperforms these prior systems."
- "WarrantGuard is the first confused-deputy or capability-security defense for agents."
- "WarrantGuard is the first evidence-force calibration or environmental-grounding benchmark."
- "PCAA, AttriGuard, or PlanGuard fail on EAIR-Bench."
- "EAIR-Bench is the first agent safety benchmark."
- "Source attribution, access control, or RAG faithfulness are solved by WarrantGuard."
- "The live matrix proves the related-work delta."

## Artifact Map For Related Work

| Related-work sentence | Artifact to cite | Status |
|---|---|---|
| Source-attribution-only is not the paper object. | `outputs/eair_warrant_reportable_export/reportable_closest_neighbor_discriminator_table.json` | L1 fixture discriminator only. |
| The planned live matrix contains nearest-neighbor discriminator rows. | `outputs/eair_prompt_protocol_matrix_live/RUN_LIVE_PROMPT_MATRIX.json` | Runbook/protocol only. |
| Main empirical delta requires legitimate-vs-hijack separation. | `docs/eair_live_killer_experiment_contract.md` | Promotion contract; no live result. |
| Field-capability positioning is the current innovation pressure-test result. | `docs/eair_innovation_pressure_test.md` | L0 design pressure, not empirical evidence. |
| Same-evidence capability laundering is implemented as a deterministic benchmark row. | `tests/test_eair_bench.py::test_warrantguard_blocks_same_evidence_field_capability_laundering` | L2 deterministic/pilot evidence, not live-provider evidence. |
| Current paper wording must remain L0/L1/L2. | `docs/eair_claim_ledger.md` | Claim firewall. |

## If Novelty Pressure Gets Worse

If reviewers argue the delta over PCAA, AttriGuard, or PlanGuard is still too small, narrow the paper rather than defending a broad safety claim:

```text
Narrowed paper: EAIR-Bench and evidence-warrant artifacts for auditing
field-scoped evidence capabilities in high-risk RAG agents.
```

In that fallback, WarrantGuard becomes the reference verifier used to instantiate the benchmark, not the main novelty claim.
