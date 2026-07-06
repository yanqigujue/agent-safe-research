# EAIR Design Pattern Spine

This file defines the reviewer-facing design pattern for **WarrantGuard: Evidence Warrants for High-Risk RAG-Agent Actions**. It does not add a new contribution or module. It binds Figure 1, the method algorithm, the formal warrant object, and the rejection-response story into one memorable pattern.

Use with:

- `figures/fig1_eair_main_chain.svg` for the hero figure.
- `docs/eair_warrant_formalism_kernel.md` for notation and validity semantics.
- `docs/eair_experiment_spine.md` for the experiment table admission rule.
- `docs/eair_claim_ledger.md` for evidence tiers and forbidden claims.

## Reviewer Memory Hook

Ambient retrieved evidence is not field authority, and execution authority is not evidence authority. A high-risk RAG agent must externalize which evidence is allowed to govern which protected action field, and WarrantGuard executes the action only when that field-scoped evidence jurisdiction is valid.

Stronger version:

```text
Retrieved evidence is not context; it is a bounded capability to change fields.
```

Operational version:

```text
No evidence jurisdiction, no field authority.
```

Longer version:

```text
Retrieve evidence -> emit proof-carrying action `(a, W_a)`
                  -> verify field-scoped evidence jurisdiction
                  -> execute / block / replace / route to review
```

Operational fallback:

```text
No valid warrant, no high-risk action.
```

The memorable design object is not the verifier and not the list of checks. It is the **evidence field capability** carried by the warrant: evidence may change `decision`, `parameters`, `requires_human_approval`, `risk_level`, or `risk_report` only if the warrant gives that evidence a bounded capability for the specific field, operation, force, time scope, provenance scope, and hard obligations. `Jurisdiction(f, a, W_a, K_q)` is the operational predicate that checks whether the field capability was consumed within scope.

Threat short name:

```text
Evidence-authority laundering.
```

This is the RAG-agent analogue of a confused-deputy failure, but the borrowed authority is evidentiary rather than executable. Capability and ambient-authority defenses ask which actor, tool, or credential may act; WarrantGuard asks which retrieved claim may govern a protected action field after execution permission is already satisfied.

The sharpest threat framing is **evidence-capability laundering**: evidence with a limited capability for one field, operation, force, time window, provenance scope, or conflict state is laundered into broader authority over another protected field.

## What Figure 1 Must Teach

Figure 1 should make one thing obvious before the reader reaches the method: WarrantGuard verifies a warrant-bearing action, not an unstructured answer and not a tool call alone.

Required visual order:

```text
Retrieved Evidence -> Proof-Carrying Action `(a, W_a)` -> WarrantGuard -> Execution Decision
```

Required visual meaning:

| Figure element | Reviewer takeaway |
|---|---|
| Retrieved evidence | Evidence may be fresh, stale, source-collapsed, conflicting, legitimate, or hijack-style. |
| Proof-carrying action `(a, W_a)` | The agent must state which evidence claims have jurisdiction over which action fields before execution. |
| `W_a` contents | Protected fields, required claims, support paths, freshness, conflicts, and hard obligations define the evidence field capabilities that may be consumed. |
| WarrantGuard | The system checks evidence authority for fields, not only permission, attribution, or answer faithfulness. |
| Execution decision | Failure routes to block, replace, or review; success permits execution for the warranted action. |

Caption draft:

> WarrantGuard turns evidence-to-action safety into field-capability control. The agent emits a structured high-risk action together with an evidence warrant `(a, W_a)` that states which retrieved evidence has a bounded capability to govern each protected field. WarrantGuard verifies that each action field consumes only in-scope evidence capabilities before allowing execution; permission, source attribution, and answer faithfulness are necessary context but not sufficient field authority.

## Method Algorithm Shape

The main method should have one algorithm, not a list of independent checkers.

```text
Algorithm 1: WarrantGuard for field-scoped evidence jurisdiction

Input:
  q        task/query
  K_q      retrieved evidence
  (a,W_a)  agent-emitted proof-carrying action

For each protected field f in F_a:
  check HardOK(f, a, H_a)
  check SupportOK(f, C_a, S_a, K_q)
  check FreshOK(f, T_a, K_q)
  check DiversityOK(f, S_a)
  check ConflictOK(f, X_a)
  check CounterEvidenceExposed(f, X_a)

If all protected fields pass:
  execute a
Else:
  block, replace, or route a to review with failed field obligations
```

The equation in the method should remain:

```text
Execute(a) iff
  HardGate(a, H_a) = PASS
  and VerifyWarrant(a, W_a, K_q) = PASS
  and CounterWarrant(a, W_a, K_q) = CLEAR.
```

## Component Status

| Component | Main-paper role | Do not sell as |
|---|---|---|
| `HardGate` | Hard action predicate for field jurisdiction. | Standalone contribution or access-control replacement. |
| `EvidenceSufficient` / `SupportOK` | Support predicate for field jurisdiction. | Separate method module. |
| `FreshOK` | Currentness predicate for field jurisdiction. | New freshness benchmark by itself. |
| `DiversityOK` | Source-cluster predicate for field jurisdiction. | Generic source-attribution method. |
| `ConflictOK` and `CounterEvidenceExposed` | Conflict and counter-evidence predicates for field jurisdiction. | Full causal or forensic system. |
| `warrant_quality_score` | Diagnostic summary of field-jurisdiction validity. | Safety proof or leaderboard objective. |
| reportability audits and seals | Reproducibility support. | Core technical novelty. |

Reviewer-facing sentence:

> These checks are not separate inventions; they are predicates that establish whether evidence has jurisdiction over a protected action field.

## How The Three Contributions Compose

| Contribution | Role in the pattern | One-line paper phrasing |
|---|---|---|
| EAIR-Bench | Defines when evidence influence has or lacks jurisdiction over action fields. | A benchmark for field-scoped evidence jurisdiction. |
| Evidence Warrant / Proof-Carrying Action | Defines the object that moves support from ambient context into field-scoped evidence authority. | A high-risk action executes as `(a, W_a)`, not as an unsupported tool call or answer. |
| WarrantGuard / EAIR-Gate | Verifies jurisdiction before execution. | A gate that checks field-level evidence authority and routes failures. |

This is the design pattern reviewers should remember:

```text
Benchmark labels evidence jurisdiction -> action carries evidence warrant -> gate verifies field authority.
```

## Novelty Pressure Test

| Neighbor | Solves | Does not solve for this design pattern | Safe delta |
|---|---|---|---|
| Proof-Carrying Certificates for LLM Pipelines | Universal assurance cards, Hoare-style action certificates, and action-gate residues for LLM pipelines. | Which retrieved evidence has authority to govern each protected RAG-agent action field. | WarrantGuard treats certification as insufficient unless the certificate establishes field-scoped evidence jurisdiction. |
| PCAA | Proof-carrying action framing and governance checkpoints. | RAG-specific evidence jurisdiction for protected fields. | WarrantGuard specializes proof-carrying actions to field-level evidence authority. |
| Confused deputy / ambient authority / capability security | Explains why ambient execution authority can be misused and motivates explicit capability boundaries. | Whether retrieved evidence has field-specific authority to govern a high-risk action after tool permission is valid. | WarrantGuard does not claim confused-deputy firstness; it adds an evidence-authority boundary for RAG action fields. |
| Tool/MCP capability laundering discussions | Explain borrowed or escalated execution privilege across tool/agent boundaries. | Whether a retrieved evidence item is consumed outside its valid field, operation, force, time, provenance, or conflict scope. | WarrantGuard targets evidence-capability laundering, not tool-capability laundering. |
| FORCEBENCH | Citation laundering and evidence-force calibration for cited RAG claims. | Whether calibrated evidence force may be consumed by protected action fields. | WarrantGuard lifts evidence force into field capabilities for high-risk actions. |
| EnvTrustBench | Evidence-grounding defects when agents overtrust stale, incorrect, or malicious environment claims. | A proof-carrying ledger of which evidence capability governed which protected field. | WarrantGuard localizes overtrust to field-capability laundering. |
| Prism-Reranker | Contribution statements and evidence passages for agentic retrieval. | Whether a useful passage has field authority for action execution. | Retrieval contribution is not a field capability. |
| MiniScope / ToolPrivBench | Least-privilege authorization and over-privileged tool selection. | Least authority for retrieved evidence after tool permission is satisfied. | WarrantGuard is least privilege for evidence-to-field authority, not tools. |
| Causality Laundering / ARM | Denial-aware causal provenance and field misuse around tool calls. | RAG evidence capabilities over decisions, parameters, approval, and risk reports. | WarrantGuard targets evidence-capability laundering rather than denial-feedback leakage. |
| AttriGuard | Causal attribution of context/tool influence. | Whether attributed influence has jurisdiction over each action field. | Attribution is input evidence; field jurisdiction is the decision object. |
| PlanGuard | Plan/action consistency under injection pressure. | Whether a consistent plan is governed by evidence with field jurisdiction. | A plan-consistent action can still fail field jurisdiction. |
| PromptArmor | Prompt-injection detection and sanitization. | Proof that emitted action fields are evidence-grounded. | The unit under verification is `(a, W_a)`, not only a prompt. |
| AgentSentry | Takeover tracing/provenance and compromised-agent defense. | Evidence sufficiency for an authorized high-risk action. | WarrantGuard targets evidence-insufficient actions even without takeover. |
| CausalArmor | Causal shielding or dominance against indirect prompt injection. | Preserving legitimate evidence influence while blocking unsupported field changes. | The pattern permits valid evidence influence instead of suppressing all influence. |
| AIRGuard | Runtime authority and least-privilege control. | Evidence jurisdiction after authority is satisfied. | Permission is a precondition; field jurisdiction decides evidence use. |
| RAGForensics | Poison-source traceback and forensic attribution. | Whether traced evidence should affect a protected action field. | Traceback is not enough; the action field needs a valid warrant. |
| RAGChecker | Fine-grained RAG retrieval/generation diagnostics. | Action parameters, approval, risk reports, and execution gates. | The output object is a proof-carrying action, not only a generated answer. |
| ARES | Automated RAG evaluation for context relevance, faithfulness, and answer relevance. | Evidence-to-action legitimacy and hard action obligations. | WarrantGuard evaluates action-field jurisdiction rather than answer quality. |

## Rejection Simulation

| Rejection | Design-pattern answer |
|---|---|
| "This is just source attribution." | Source attribution says what influenced the action; field jurisdiction says whether that influence has authority over each protected field. |
| "This is just access control." | Access control says whether the actor may execute; WarrantGuard asks whether the evidence may govern parameters, approval, risk, and report fields. |
| "This is just tool capability laundering." | Tool capability laundering scopes execution privilege; WarrantGuard scopes evidence capabilities consumed by protected fields. |
| "This is just RAG faithfulness." | Faithful text can still justify an unsafe parameter or stale risk report; `ValidField` is action-field validity, not answer grounding. |
| "This benchmark is synthetic and overfitted to the method." | The main design claim is L0; empirical promotion requires the live experiment spine and L4 sealed pair. |
| "The method has too many hand-designed rules." | The paper should present one field-jurisdiction object; the rules are predicates for whether evidence has authority over a field. |
| "The novelty over PlanGuard/AttriGuard is unclear." | Plan consistency and attribution can both hold while evidence lacks field jurisdiction; legitimate influence can pass when jurisdiction holds. |

## Claim-Safe Method Text

Allowed:

- "WarrantGuard implements an evidence-warrant design pattern for high-risk RAG-agent actions."
- "The verifier checks whether evidence has jurisdiction over protected action fields."
- "Evidence warrants represent retrieved evidence as bounded field capabilities."
- "Hard action constraints, evidence sufficiency, freshness, source diversity, conflict, and counter-evidence are predicates for field-scoped evidence jurisdiction inside `W_a`."
- "The current figure and formalism are L0 method artifacts; empirical claims require the evidence tiers in the claim ledger."

Avoid:

- "HardGate is our main contribution."
- "The EAIR score proves safety."
- "WarrantGuard is a better access-control system."
- "WarrantGuard is only a checklist over sufficiency, freshness, diversity, and conflict."
- "WarrantGuard beats PCAA, AttriGuard, PlanGuard, AIRGuard, RAGChecker, or ARES."
- "The design proves deployment safety."

## Artifact Map

| Design-pattern claim | Evidence tier | Artifact |
|---|---|---|
| Figure 1 shows the object being verified: `(a, W_a)`. | L0 | `figures/fig1_eair_main_chain.svg` |
| The formal method is one warrant object plus field-level validity. | L0 | `docs/eair_warrant_formalism_kernel.md` |
| The innovation pressure test frames evidence warrants as field-capability ledgers. | L0 | `docs/eair_innovation_pressure_test.md` |
| Same-evidence capability laundering is pinned as a deterministic benchmark row. | L2 | `tests/test_eair_bench.py::test_warrantguard_blocks_same_evidence_field_capability_laundering` |
| The paper's main text should foreground benchmark, warrant, and gate as the only three contributions. | L0 | `docs/eair_claim_ledger.md`; `docs/warrantguard_paper_kernel.md`; `PAPER_PLAN.md` |
| Current empirical support remains L1/L2, with no live-provider L4 claim. | Boundary | `docs/eair_claim_ledger.md`; `outputs/eair_prompt_protocol_matrix_live/workflow_status/live_workflow_status.json` |

## Source Anchors

- PCAA: https://arxiv.org/abs/2606.04104
- Proof-Carrying Certificates for LLM Pipelines: https://arxiv.org/abs/2605.16407
- Confused Deputy / capability security: https://dl.acm.org/doi/10.1145/54289.871709
- Towards Verifiably Safe Tool Use for LLM Agents: https://arxiv.org/abs/2601.08012
- FORCEBENCH / Relevant Is Not Warranted: https://arxiv.org/abs/2605.28044
- EnvTrustBench: https://arxiv.org/abs/2605.08828
- Prism-Reranker: https://arxiv.org/abs/2604.23734
- MiniScope: https://arxiv.org/abs/2512.11147
- ToolPrivBench / When Lower Privileges Suffice: https://arxiv.org/html/2606.20023
- Causality Laundering / ARM: https://arxiv.org/abs/2604.04035
- Tool/MCP capability laundering discussion, non-paper security-neighbor anchor: https://github.com/cosai-oasis/secure-ai-tooling/issues/196
- AttriGuard: https://arxiv.org/abs/2603.10749
- PlanGuard: https://arxiv.org/abs/2604.10134
- PromptArmor: https://arxiv.org/abs/2507.15219
- AgentSentry: https://arxiv.org/abs/2602.22724
- CausalArmor: https://arxiv.org/abs/2602.07918
- AIRGuard: https://arxiv.org/abs/2605.28914
- RAGForensics: https://arxiv.org/abs/2504.21668
- RAGChecker: https://arxiv.org/abs/2408.08067
- ARES: https://arxiv.org/abs/2311.09476
