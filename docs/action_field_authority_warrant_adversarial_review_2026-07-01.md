# Adversarial Review: Action-Field Authority Warrants

Date: 2026-07-01

Boundary: this is a local adversarial review following the `kill-argument` and `research-review` protocols. The external `mcp__codex__codex` reviewer backend is not available in this session, so this is **not** a cross-model verdict.

## New High-Pressure Neighbors Found After the First Pitch

| Work | Why it pressures the idea |
|---|---|
| [AuthGraph: Aligning Provenance with Authorization](https://arxiv.org/abs/2605.26497) | The strongest new neighbor. It already compares an authorization graph against execution provenance at tool and parameter-source level, preserving legitimate observation flows while detecting injected parameter provenance. |
| [PCAA: Proof-Carrying Agent Actions](https://arxiv.org/abs/2606.04104) | It already centers runtime governance on certificate-bearing actions with authority, approval, receipts, and replayable proof. This blocks generic proof-carrying action/warrant language. |
| [Securing LLM-Agent Long-Term Memory Against Poisoning](https://arxiv.org/abs/2606.24322) | It explicitly studies laundering of authority through memory transformations and proposes non-malleable origin-bound authority. This blocks broad "authority laundering" novelty. |
| [A Framework for Formalizing LLM Agent Security](https://arxiv.org/abs/2603.19469) | It formalizes contextual security through task alignment, action alignment, source authorization, and data isolation. This blocks broad "context determines security" novelty. |
| [Authorization Propagation in Multi-Agent AI Systems](https://arxiv.org/abs/2605.05440) | It frames authorization invariants across retrieval, delegation, synthesis, temporal validity, and non-human principals. This pressures delegation and prior-step authority claims. |
| [Cordon: Semantic Transactions](https://arxiv.org/abs/2606.17573) | It stages and validates irreversible effects across multi-step workflows with delegated authority and lineage. This pressures side-effect and multi-step containment claims. |
| [Consent Integrity](https://arxiv.org/abs/2606.02668) | It isolates approval as its own integrity surface: what the user approves should match what executes. This pressures approval-field novelty. |
| [Pre-Action Authorization / OAP](https://arxiv.org/abs/2603.20953) | It provides deterministic pre-action policy enforcement and signed audit records. This pressures generic pre-execution gate claims. |
| [Intent-to-Execution Integrity](https://arxiv.org/abs/2605.16976) | It argues for end-to-end correctness over instruction, data flow, judgment, and tool integrity. This pressures broad correctness-property framing. |

## Hostile Rejection Memo

The proposed "action-field authority warrant" is currently a relabeling of several very recent agent-security lines rather than a new mechanism. AuthGraph already separates an authorization specification from execution provenance and checks parameter-source deviations while preserving legitimate observation flows; its case studies explicitly avoid overblocking multi-hop, mixed-source, and task-specific parameter flows. PCAA already makes agent actions proof-carrying with authority and approval semantics. Memory-authority work already uses the language of laundering and non-malleable authority. Contextual-security frameworks already state that the same action can be legitimate or malicious depending on source, task, and information flow. Against these neighbors, "each field must consume a valid source capability" reads like a restatement of source authorization plus data isolation at a different granularity. The proposed same-source benchmark also risks being synthetic: if the legal and illegal cases are hand-authored, then CapGuard wins by encoding the labels, while permission-only and attribution-only baselines are strawmen. Unless the paper identifies a field type, consumption relation, or empirical setting that AuthGraph/PCAA/contextual-security formulations cannot express, the contribution is mostly vocabulary and benchmark packaging.

## Atomic Rejection Points

| ID | Attack point | Current status | Severity | What would fix it |
|---|---|---|---|---|
| P1 | AuthGraph already covers provenance-vs-authorization at parameter-source granularity. | still_unresolved | critical | Define a concrete class of protected fields beyond tool parameters and show why graph alignment does not naturally cover their semantic authority. |
| P2 | PCAA already covers proof-carrying action governance with authority and approval receipts. | partially_answered | major | Stop using generic "proof-carrying action" as novelty; position AFW as the payload semantics inside or beside a certificate. |
| P3 | "Capability laundering" is no longer unique because memory work explicitly uses laundering and non-malleable authority. | partially_answered | major | Narrow laundering to same-source cross-field semantic-role laundering, not origin laundering or trust laundering. |
| P4 | Contextual-security frameworks already formalize source authorization, action alignment, and data isolation. | partially_answered | major | Phrase AFW as an instantiation/testable proof object for protected fields, not a new general security framework. |
| P5 | Same-source paired rows may be synthetic and label-coded. | still_unresolved | critical | Tie rows to real agent traces or existing benchmark tasks, and include adversarially selected baselines that are not obviously weak. |
| P6 | The unified source schema may be hand-written per source family. | partially_answered | major | Demonstrate that all rows use one machine-checkable `Cap(x)` / `Need(s,f)` schema with minimal source-specific predicates. |
| P7 | Warrant extraction is unsolved if the model lies about consumed sources. | partially_answered | major | Separate gold-warrant verifier claim from model-emitted warrant claim; add trace-derived or counterfactual extraction as a secondary experiment. |

## Net Assessment

The idea survives only if we shrink the claim further. The broad phrases "capability laundering," "authority flow," "proof-carrying agent action," and "unified capability warrant" are now unsafe as headline novelty. The remaining defensible object is:

> **semantic-role validity for non-parameter protected fields**, tested through same-source cross-field pairs.

This means the paper should not compete head-on with AuthGraph on tool parameter-source provenance. It should instead target fields that are not naturally just tool parameters:

- approval status,
- risk level,
- risk report,
- side-effect release,
- delegation,
- data-read/write scope,
- policy interpretation,
- evidence-to-report authority.

## Revised Innovation Claim

Old claim:

> Each protected field must prove it consumed a valid authority source.

Stronger and narrower claim:

> Existing provenance-vs-authorization systems primarily validate whether tool choices and parameters are sourced from authorized data. We study **semantic-role laundering across non-parameter action fields**, where the same source is valid for one field, such as routing or formatting, but invalid for another, such as approval, risk, side-effect release, delegation, or report conclusions.

This revision keeps the core WarrantGuard insight alive:

> A trusted source is not universally authoritative; it carries field-specific semantic roles.

## Reframed Benchmark Requirement

The main benchmark should not merely include source families. It must include field families that nearest neighbors under-cover:

| Field family | Why it matters | Example |
|---|---|---|
| Approval field | Consent and PCAA cover approvals, but not necessarily evidence/skill/tool metadata laundering into approval waiver. | A policy doc supports simulation but not `requires_human_approval=false`. |
| Risk/report field | RAG faithfulness and parameter-source checks do not decide if a source may downgrade risk or write "safe no review." | A maintenance note supports one parameter but not a global risk downgrade. |
| Side-effect release field | Cordon stages effects, but AFW asks which source authorizes release. | A report skill formats a file but cannot publish it. |
| Delegation field | Authorization propagation studies delegation globally; AFW checks whether this step consumed valid delegation authority. | A cleaning skill reads CSV but cannot spawn a subagent. |
| Data-scope field | Tool permission says read is possible; AFW says whether this source justified this read scope. | User approved one folder, not home directory. |

## Updated Score

Previous score: 7/10.

After AuthGraph and memory-authority pressure: **6.5/10, still proceed, but only with the narrower non-parameter field thesis.**

The idea is still worth pursuing because WarrantGuard already has the strongest example category: risk, approval, and report fields in high-risk RAG actions. The skill/tool expansion should support that insight, not replace it.

## Top Action Items

1. Rewrite the title/pitch around **non-parameter protected fields** or **semantic-role field authority**, not generic capability warrants.
2. Add AuthGraph, PCAA, origin-bound memory authority, contextual security, Cordon, Consent Integrity, OAP, and authorization propagation to every novelty table.
3. Redesign the benchmark so at least half of the rows involve approval, risk/report, side-effect release, delegation, or data-scope fields rather than ordinary tool parameters.
4. Make AuthGraph a respected closest neighbor, not a straw baseline. The discriminator must show a different question, not a failure.
5. Keep WarrantGuard as the anchor example because it already demonstrates same-source evidence valid for simulation but invalid for approval/risk/report fields.

