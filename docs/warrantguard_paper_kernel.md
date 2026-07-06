# WarrantGuard Paper Kernel

> 2026-07-02 note: the current active power-ops paper slice has moved to
> `docs/power_ops_action_invariance_paper_outline_2026-07-02.md` and
> `docs/power_ops_action_invariance_paper_kernel_2026-07-02.md`.
> This WarrantGuard kernel remains useful as provenance for evidence-warrant
> framing, but the active section plan for the electric-power safety work is
> field-level action invariance under strict supervision.

This is the claim-safe paper skeleton for **WarrantGuard: Evidence Warrants for High-Risk RAG-Agent Actions**. It is written from the current evidence state, not from the hoped-for live result. Use `docs/eair_claim_ledger.md` as the authority for what may appear in the abstract, introduction, and results. Use `docs/eair_front_matter_kernel.md` as the copy-facing source for title, abstract, introduction, contribution preview, and front-matter novelty boundary. Use `docs/eair_design_pattern_spine.md` to keep Figure 1, Algorithm 1, method prose, and component naming centered on one evidence-warrant design pattern.

## Title

**WarrantGuard: Evidence Warrants for High-Risk RAG-Agent Actions**

## One-Sentence Contribution

High-risk RAG-agent actions need evidence warrants: replayable field-capability ledgers that prove whether retrieved evidence may govern the action, arguments, approval status, risk level, and risk report.

## Claim-Safe Abstract Draft

High-risk RAG agents increasingly turn retrieved evidence into actions: routing a simulation, setting a parameter, bypassing an approval, or writing a risk report. Existing defenses often check whether a tool call is authorized, whether a source influenced the output, whether an answer is faithful to retrieved text, whether cited evidence warrants claim wording, whether environment observations are trustworthy, or whether a generic certificate exists, but those checks do not by themselves prove that evidence has authority over the protected fields of a high-risk action. We introduce **evidence warrants**, a proof-carrying action representation in which an action records bounded evidence capabilities for its decision, tool arguments, approval status, risk level, and risk report. We instantiate this object in **WarrantGuard**, a verifier that checks support, freshness, source diversity, conflicts, counter-evidence, and hard action predicates as capability-boundary predicates, and we organize **EAIR-Bench** around legitimate versus hijack-style field authority. Current reviewed artifacts show that the reportable pipeline can audit closest-neighbor discriminator rows and an offline paired legitimate-vs-hijack contrast with a warrant-quality gap of `1.0`; live-provider superiority claims remain blocked until the planned live matrix passes reportability and strict reviewed sealing.

## Contributions

1. **EAIR-Bench: field-scoped evidence capabilities.** The benchmark labels whether evidence influence over protected action fields is capability-bearing or hijack-style, rather than only measuring poison retrieval, source attribution, access permission, answer faithfulness, force calibration, environmental grounding, or certificate presence.
2. **Evidence Warrant / Proof-Carrying Action.** A high-risk action is represented as `(a, W_a)`, where `W_a = (F_a, C_a, S_a, T_a, X_a, H_a)` records protected fields and the capability-boundary predicates that establish whether evidence may govern them.
3. **WarrantGuard / EAIR-Gate.** The verifier accepts an action only when protected fields consume valid evidence capabilities and no hard action obligation fails.

## Threat Model Kernel

Use `docs/eair_threat_model_kernel.md` as the paper-facing threat model.

The system under test is a RAG agent that retrieves evidence and emits a structured high-risk action. The protected fields are `decision`, `tool`, `parameters`, `requires_human_approval`, `risk_level`, `risk_report`, and the supporting claims behind each field.

The short threat name is **evidence-authority laundering**, sharpened as **evidence-capability laundering**: a RAG-specific confused-deputy variant where retrieved evidence borrows authority over protected fields, not credentials over tools.

The attacker can influence retrieved documents, stale records, near-duplicate source clusters, conflicting evidence, low-integrity support claims, or tool descriptions. The attacker does not control model weights, the WarrantGuard verifier, reportability audits, or the reviewed claim-seal chain.

An attack succeeds when a final high-risk action is unsafe, unsupported, approval-bypassing, parameter-violating, risk-downgraded, or justified by insufficient, stale, source-collapsed, or conflict-heavy evidence.

## Design Pattern

Use `docs/eair_design_pattern_spine.md` as the design-pattern authority.

```text
Retrieve evidence
  -> Agent emits proof-carrying action (a, W_a)
  -> WarrantGuard verifies the evidence warrant
  -> Execute, block, replace, or route to review
```

WarrantGuard is not a new name for source attribution, access control, confused-deputy defense, RAG faithfulness, evidence-force calibration, environmental grounding, or generic action certification. Access control and confused-deputy defenses ask whether execution authority is properly scoped. Attribution asks which evidence influenced the action. RAG faithfulness asks whether text is grounded in retrieved context. Force calibration asks how strong a cited claim is. Environmental grounding asks whether observations track true state. Certification asks whether a proof object exists. WarrantGuard asks whether evidence carries the bounded capability consumed by each protected action field.

## Current Results Narrative

Use `docs/eair_experiment_spine.md` as the admission rule for main-paper result tables. A result table belongs in the main text only if it maps a reviewer objection to a nearest neighbor, condition, protected fields, cited artifact, allowed claim, and downgrade rule.

| Result slot | Claim-safe wording | Evidence |
|---|---|---|
| R1: claim boundary | The project currently supports L1 fixture claims and L2 dry-run/pilot claims, not live L4 claims. | `docs/eair_claim_ledger.md` |
| R2: closest-neighbor discriminator | Reviewed fixture artifacts can export and audit closest-neighbor discriminator rows for source-attribution and benchmark-overfit objections. | `outputs/eair_warrant_reportable_export/reportable_closest_neighbor_discriminator_table.json`; `paper_ready_claims.json` |
| R3: offline pair rehearsal | A separate offline paired fixture produces one pair row with legitimate quality `1.0`, hijack quality `0.0`, and warrant-quality gap `1.0`. | `outputs/eair_warrant_pair_reportable_export/reportable_influence_contrast_pair_table.json` |
| R4: dry-run behavior | In deterministic dry-run rows, proof-carrying prompts can allow legitimate evidence updates and block parameter hijacks. | `outputs/eair_prompt_protocol_matrix_dry_run/summary/artifact_summary_influence_contrast_table.json` |
| R5: same-evidence capability laundering | The deterministic benchmark now includes a row where trusted policy evidence supports simulation routing but not review waiver or risk-report downgrade. | `tests/test_eair_bench.py::test_warrantguard_blocks_same_evidence_field_capability_laundering` |
| R6: live status | Live-provider claims are not available because the live workflow is blocked at preflight. | `outputs/eair_prompt_protocol_matrix_live/workflow_status/live_workflow_status.json` |

## Results Sentences Allowed Now

- "The reviewed offline paired fixture demonstrates that the reportable claim chain can carry the legitimate-vs-hijack contrast."
- "The paired fixture records a warrant-quality gap of `1.0` between the legitimate evidence-update row and the parameter-hijack row."
- "The current live-provider workflow is blocked before sampling because `OPENAI_API_KEY` is absent."
- "The paper therefore treats live WarrantGuard superiority as a required next experiment, not as a current result."

## Results Sentences To Delete

- "WarrantGuard outperforms AttriGuard, PlanGuard, or RAG faithfulness baselines."
- "WarrantGuard distinguishes legitimate from hijack influence in live models."
- "PCAA, AttriGuard, or PlanGuard fail on EAIR-Bench."
- "EAIR-Bench proves deployment safety for high-risk RAG agents."
- "This is the first proof-carrying action or certificate system."

## Section Skeleton

### 1. Introduction

Open with high-risk RAG agents turning evidence into actions, not answers. Explain why tool permission, attribution, faithfulness, force calibration, environmental grounding, and generic certification leave a gap: none proves that evidence carries the field capability consumed by protected action fields. State the contribution as evidence warrants plus WarrantGuard plus EAIR-Bench. Preview only current evidence tiers: reviewed fixture packets, offline paired contrast, dry-run matrix, and blocked live run.

### 2. Related Work

Organize by question, not by paper list. Use `docs/eair_related_work_positioning.md` as the paper-facing related-work kernel, and keep older novelty matrices as provenance rather than copy-ready prose:

- **Proof-carrying certificates, actions, and agent governance:** Proof-carrying certificate work and PCAA are the closest certificate/action neighbors; WarrantGuard specializes the payload to RAG evidence jurisdiction.
- **Evidence-force calibration and environmental grounding:** FORCEBENCH and EnvTrustBench are the strongest recent pressure points; WarrantGuard treats force and grounding as dimensions of field-capability consumption.
- **Confused deputy and capability security:** Classic authority-boundary work and recent agent tool-use safety motivate explicit execution-authority scoping; WarrantGuard adds a separate evidence-authority boundary.
- **Attribution and forensics:** AttriGuard and RAGForensics track influence/source; WarrantGuard decides whether influence is legitimate for action fields.
- **Plan/action and authority guards:** PlanGuard and AIRGuard address plan consistency or permission; WarrantGuard adds field-scoped evidence capabilities.
- **Prompt and takeover defenses:** PromptArmor, AgentSentry, and CausalArmor target injection or takeover; WarrantGuard verifies the emitted action's warrant.
- **RAG evaluation:** RAGChecker and ARES assess RAG faithfulness/quality; WarrantGuard evaluates action parameters, approvals, risk reports, and execution gates.

### 3. Threat Model and Evidence Warrants

Define protected action fields and attacker capability from `docs/eair_threat_model_kernel.md`. Use `docs/eair_warrant_formalism_kernel.md` for the formal method object. Introduce `W_a = (F_a, C_a, S_a, T_a, X_a, H_a)`, interpret it as a field-capability ledger, and state the acceptance condition:

```text
Execute(a) iff
  HardGate(a) = PASS
  and VerifyWarrant(a, W_a) = PASS
  and CounterWarrant(a, W_a) = CLEAR.
```

Keep `HardGate`, `VerifyWarrant`, and `CounterWarrant` as verifier obligations, not standalone contributions.

### 4. EAIR-Bench

Define benchmark rows as field-scoped evidence-capability cases. Show how each condition maps to protected fields, warrant obligations, and reviewer objections. The table to foreground is the closest-neighbor discriminator table plus the legitimate-vs-hijack pair table, with `same_evidence_field_capability_laundering` as the stricter follow-on live extension for the evidence-capability headline.

### 5. WarrantGuard

Describe the verifier and the proof-carrying action interface. Explain how WarrantGuard differs from attribution-only, access-control-only, faithfulness-only, and generic certificate checks.

### 6. Experiments and Artifact Chain

Use current evidence tiers:

- fixture reportability packet with 15 reviewed claims,
- offline paired packet with 7 reviewed claims,
- dry-run prompt matrix,
- live runbook and blocked workflow status.

Do not claim live results. End this section with the live matrix as the next required experiment, and use `docs/eair_live_killer_experiment_contract.md` as the contract for what the live matrix must prove before any L3/L4 claim can enter the paper.

### 7. Limitations

State the central limitation directly: live-provider L3/L4 evidence is not yet available. Also state that official prior-work baselines have not been executed, so closest-neighbor rows are positioning evidence rather than failure claims.

## Figure and Table Plan

| ID | Type | Purpose | Current evidence |
|---|---|---|---|
| Fig. 1 | Design pattern diagram | Use `figures/fig1_eair_main_chain.svg` and `docs/eair_design_pattern_spine.md` to show evidence -> proof-carrying action `(a, W_a)` -> WarrantGuard -> execute/block/review. It should make the proof-carrying action the object being verified, not place the verifier before the warrant object. | Manual, L0. |
| Table 1 | Threat-model table | Protected fields, attacker capability, warrant obligations, and EAIR-Bench threat rows. | `docs/eair_threat_model_kernel.md`; runbook condition descriptors. |
| Table 2 | Closest-neighbor discriminator table | Show what each prior-work family solves and what WarrantGuard adds. | `docs/eair_related_work_positioning.md`; `docs/eair_claim_ledger.md`; reportable discriminator rows. |
| Table 3 | Formalism and metric table | Show `W_a`, `ValidField`, execution semantics, `warrant_quality_score`, and pair gap. | `docs/eair_warrant_formalism_kernel.md`; metric implementation/tests. |
| Table 4 | Artifact-chain results | Reviewed fixture claims, offline pair packet, dry-run rows, live blocked state. | Claim packets and workflow status. |
| Table 5 | Future live matrix gate | Conditions required before L4 claim and downgrade rules if the experiment fails. | `docs/eair_live_killer_experiment_contract.md`; live runbook. |

## Abstract Must Not Claim

The abstract must not say that WarrantGuard beats prior systems, solves deployment safety, or has live-provider results. It may say the current artifact chain demonstrates a reproducible fixture and dry-run basis for the proposed evidence-warrant object and identifies the exact live experiment required for the main empirical claim.
