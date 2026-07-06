# Novelty Dossier: Action-Field Authority Warrants

Date: 2026-07-01

Proposed method:

> Action-field authority warrants require every protected agent step field to expose which authority source it consumed and prove that the source is valid for the field's semantic role, operation, data scope, side effect, and delegation chain.

## Core Claims

| Claim | Novelty | Closest pressure | Assessment |
|---|---|---|---|
| C1: Field-level authority consumption | Medium | AuthGraph; formal protocol composition; WarrantGuard; MCP runtime invariants | Keep only after narrowing. The novelty is not field-level source authorization broadly, but semantic-role authority over non-parameter protected fields. |
| C2: Same-source legal-vs-laundered paired benchmark | High | SkillsBench; ToolPrivBench; WarrantGuard paired evidence rows | Keep. Existing work often compares malicious/benign artifacts or high/low privilege choices, not the same artifact consumed in two semantic roles. |
| C3: Skill/RAG/tool/memory/approval as authority sources under one field-level relation | Medium | SkillGuard; proof-carrying skill artifacts; learned capability governance | Keep only if framed as source unification under field consumption, not as first capability governance. |
| C4: Verifier preserves legitimate influence while blocking laundering | Medium-high | Attribution systems; tool guards; WarrantGuard legitimate-vs-hijack contrast | Keep. The preservation requirement is important; a pure safety blocker is not enough. |
| C5: Skill warrant compiler or skill manifest | Low | SkillGuard; formal verification of agent skills; SkillFortify | Drop as main contribution. Use only as input/baseline. |
| C6: Minimal authority witness for protected fields | Medium | AuthGraph; provenance summarization; proof-carrying action certificates | Keep as supporting algorithmic object. It must expose field-role coverage and missing roles, not merely summarize provenance. |

## Closest Prior Work

| Work | Status | What it covers | Overlap | Delta we can still claim |
|---|---|---|---|---|
| [Agent Skills for Large Language Models](https://arxiv.org/abs/2602.12430) | arXiv verified by API | Agent skills as composable packages of instructions, code, and resources; architecture/acquisition/security overview. | Establishes skill-driven agents as a real setting. | Our method targets runtime authority consumption by action fields, not a general skill architecture survey. |
| [SkillsBench](https://arxiv.org/abs/2602.12670) | arXiv verified by API | Benchmarks whether curated skills improve task performance across 87 tasks and multiple domains. | Skill benchmark framing. | Our benchmark is security/authority-focused and same-source paired, not task-capability evaluation. |
| [Skill-Inject](https://arxiv.org/abs/2602.20156) | arXiv verified by API | Measures agent vulnerability to skill-file attacks and prompt injection through skills. | Skill attack surface. | We cover laundering even when sources are benign/trusted and only consumed in the wrong field role. |
| [Formal Analysis and Supply Chain Security for Agentic AI Skills](https://arxiv.org/abs/2603.00195) | arXiv verified by API | Formal/static skill supply-chain security. | Static/formal skill risk. | We do not claim skill scanning; we check later action-field consumption. |
| [SkillGuard](https://arxiv.org/abs/2606.03024) | arXiv verified by API | Runtime permission framework for skills, including what a skill can inject and cause. | Strongest skill-permission neighbor. | We ask which later action fields consumed skill authority, evidence, memory, approval, or tool metadata, and whether that consumption is semantically valid. |
| [Methods for Formal Verification of Agent Skills](https://arxiv.org/abs/2605.23951) | arXiv page checked | Proof-carrying skill artifacts, capability-containment proofs, refinement types, bounded trace checking. | Blocks proof-carrying skill novelty. | We shift proof-carrying from skill artifact containment to action-field authority consumption across heterogeneous sources. |
| [ToolPrivBench](https://arxiv.org/abs/2606.20023) | arXiv verified by API | Over-privileged tool selection when lower-privilege tools suffice. | Tool privilege benchmark. | We also handle allowed tools whose parameters/side effects are justified by the wrong source role. |
| [ToolSafe](https://arxiv.org/abs/2601.10156) | arXiv verified by API | Step-level tool invocation safety guardrail and feedback. | Step-level runtime guard. | Our verifier checks warrant validity of consumed authority per field, not only unsafe invocation classification. |
| [Beyond Static Sandboxing](https://arxiv.org/abs/2604.11839) | arXiv verified by API | Learned capability governance and capability overprovisioning. | Capability governance language. | We must not claim broad capability governance; our object is narrower: proof-carrying field authority. |
| [MCP-Style Runtime Security Invariants](https://arxiv.org/abs/2606.29073) | arXiv verified by API | Explicit execution-layer invariants in MCP-style runtimes. | MCP runtime invariant layer. | We are not an MCP invariant framework; we verify semantic authority consumption inside concrete agent steps. |
| [Formal Security Analysis of Agent Protocol Composition](https://arxiv.org/abs/2606.28690) | arXiv page checked | Content-to-authority flow, semantic-to-authority isolation, authority monotonicity, bridge contracts, replayable counterexamples. | Hardest conceptual neighbor. | Avoid broad authority-flow claims. Our remaining delta is field-level warrants for agent action semantics and same-source paired evaluation. |
| [Intent-Governed Tool Authorization for AI Agents](https://arxiv.org/abs/2606.22916) | arXiv search checked | Intent certificates, policy narrowing, and consistency among user intent, tool call, and payload. | Pressures intent-bound authorization claims. | AFW should not claim intent authorization; it checks whether protected fields consumed sources with the required semantic roles and exposes a minimal witness. |
| [MCP Security Best Practices](https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices) | official page checked | Consent, permissions, confused deputy, tool safety best practices. | Deployment motivation and safety vocabulary. | We can cite as motivation, not as novelty contrast. |
| [AuthGraph: Aligning Provenance with Authorization](https://arxiv.org/abs/2605.26497) | arXiv page checked | Aligns an authorization specification graph with execution provenance at tool and parameter-source granularity. | Hardest implementation-level neighbor for field/source validity. | Do not compete on ordinary tool parameter provenance. Focus on semantic-role laundering in approval, risk/report, side-effect release, delegation, and data-scope fields. |
| [PCAA: Proof-Carrying Agent Actions](https://arxiv.org/abs/2606.04104) | arXiv page checked | Proof-carrying action certificates with authority, approval, receipts, and replay. | Blocks generic proof-carrying action/warrant novelty. | AFW can be positioned as payload semantics for protected fields, not a first proof-carrying action system. |
| [Securing LLM-Agent Long-Term Memory Against Poisoning](https://arxiv.org/abs/2606.24322) | arXiv page checked | Studies laundering of authority through memory transformations and proposes origin-bound authority. | Blocks broad "authority laundering" novelty. | AFW must say cross-field semantic-role laundering, not origin laundering. |
| [A Framework for Formalizing LLM Agent Security](https://arxiv.org/abs/2603.19469) | arXiv page checked | Contextual security via task alignment, action alignment, source authorization, and data isolation. | Blocks broad contextual/source authorization framing. | AFW should be a concrete proof object and benchmark for protected action fields. |
| [Authorization Propagation in Multi-Agent AI Systems](https://arxiv.org/abs/2605.05440) | arXiv page checked | Authorization invariants across retrieval, delegation, synthesis, temporal validity, and non-human principals. | Pressures delegation and prior-step authority claims. | Use delegation rows as field-level discriminators, not as first authorization propagation work. |
| [Cordon: Semantic Transactions](https://arxiv.org/abs/2606.17573) | arXiv page checked | Stages and validates irreversible effects across multi-step workflows with delegated authority and lineage. | Pressures side-effect release claims. | AFW asks which source authorizes a side-effect field, while Cordon focuses on transaction lifecycle. |
| [Consent Integrity](https://arxiv.org/abs/2606.02668) | arXiv page checked | Ensures the user's approval matches what executes. | Pressures approval-field novelty. | AFW should handle how non-approval sources are laundered into approval fields and how approval scope is consumed. |
| [Pre-Action Authorization / OAP](https://arxiv.org/abs/2603.20953) | arXiv page checked | Deterministic pre-action policy enforcement with signed audit records. | Pressures generic pre-execution gate claims. | AFW is not another gate; it defines semantic-role evidence for protected fields. |

## Overall Novelty Assessment

Score: **6.5/10, proceed with caution.**

The idea is not safe if presented as:

- unified capability governance,
- proof-carrying skills,
- skill permission,
- MCP authority flow,
- tool least privilege,
- step-level tool safety.

The idea is promising if presented as:

> A field-level proof object that records and checks which authority source each non-parameter protected agent action field consumed.

The main differentiator:

> Same-source, different-consumption cases over approval, risk/report, side-effect release, delegation, and data-scope fields: the same source must pass when consumed in scope and fail when laundered into another field or semantic role.

## Reviewer-Killing Example

Use this example early:

```text
Same source:
  signed_policy_v4 says N-1 simulation is required before changing operating mode.

Legal consumption:
  decision = route_to_simulation
  tool = simulate_grid

Laundered consumption:
  requires_human_approval = false
  risk_level = low
  risk_report = safe_no_review
```

Why it works:

- source is trusted,
- evidence is current,
- tool permission can pass,
- attribution can be correct,
- answer can be faithful,
- but authority is consumed by the wrong fields.

This is the clean bridge from existing WarrantGuard to the broader framework.

## Recommended Positioning

Use this phrase:

> field-level authority consumption

Even safer phrase:

> semantic-role authority for non-parameter protected fields

Avoid this phrase as a headline:

> authority flow

Reason: recent protocol-composition work already occupies content-to-authority flow and semantic-to-authority isolation. "Authority flow" is still useful in prose, but the title and contribution should say field-level/action-field consumption.

## Minimal Experiment Plan

Start with a deterministic paired benchmark, then run live models only after the rows are locked.

1. **RAG slice.** Reuse current WarrantGuard conditions and emphasize approval, risk, and report fields.
2. **Skill slice.** Construct skills with legal formatting/analysis authority and illegal data-scope, side-effect, or delegation consumptions.
3. **Tool/MCP metadata slice.** Tool descriptions define schema but cannot authorize approval, policy, or side-effect release.
4. **Approval/memory slice.** User approval and memory can support local roles but cannot be laundered into safety-policy or publication authority.

A main table should contain:

```text
source_type
same_source_id
legal_field
laundered_field
legal_preservation
laundering_block
same_source_gap
nearest_neighbor_objection
```

## Current Decision

Proceed with a narrowed action-field authority warrant pitch, not the broader "unified framework" pitch.

The paper should sell one memorable idea:

> No approval, risk/report, side-effect, delegation, or data-scope field should execute without a valid authority warrant for the source it consumed.
