# Literature Pressure Matrix for Agent-Safety Innovation Search

Date: 2026-07-01

## Verification Note

This matrix separates arXiv-API verified papers from items that still need re-checking. It is a pressure map for idea generation, not a final bibliography.

## arXiv-API Verified Neighbors

| Paper | arXiv | Date | What it pressures | Design implication |
|---|---|---:|---|---|
| Proof-Carrying Agent Actions: Model-Agnostic Runtime Governance for Heterogeneous Agent Systems | https://arxiv.org/abs/2606.04104 | 2026-06-02 | Generic proof-carrying action certificates, runtime governance, approval/receipt semantics | AFW must not claim proof-carrying action firstness; frame itself as field-authority payload semantics. |
| Aligning Provenance with Authorization: A Dual-Graph Defense for LLM Agents | https://arxiv.org/abs/2605.26497 | 2026-05-26 | Provenance-vs-authorization alignment for tools and parameter sources | AFW must focus on non-parameter protected fields and semantic-role validity. |
| SkillGuard: A Permission Framework for Agent Skills | https://arxiv.org/abs/2606.03024 | 2026-06-02 | Skill permissions and runtime effects | AFW cannot be a skill permission paper; focus on downstream action-field consumption of skill outputs. |
| When Lower Privileges Suffice: Investigating Over-Privileged Tool Selection in LLM Agents | https://arxiv.org/abs/2606.20023 | 2026-06-18 | Least-privilege tool choice | AFW should be least authority for source-to-field consumption, not least-privilege tool selection. |
| Formal Security Analysis of Agent Protocol Composition | https://arxiv.org/abs/2606.28690 | 2026-06-27 | Broad protocol-level content-to-authority and semantic-to-authority isolation | Avoid broad authority-flow claims; use concrete field-level verifier and benchmark. |
| Intent-Governed Tool Authorization for AI Agents | https://arxiv.org/abs/2606.22916 | 2026-06-22 | Intent certificates, session-scoped policy narrowing, intent-tool-payload consistency | AFW must not claim intent-governed authorization; frame itself as semantic-role witness extraction for protected fields. |
| Securing LLM-Agent Long-Term Memory Against Poisoning: Non-Malleable, Origin-Bound Authority with Machine-Checked Guarantees | https://arxiv.org/abs/2606.24322 | 2026-06-23 | Authority laundering through memory and origin-bound authority | Avoid generic laundering firstness; focus on cross-field semantic-role laundering and derived-artifact attenuation. |
| Cordon: Semantic Transactions for Tool-Using LLM Agents | https://arxiv.org/abs/2606.17573 | 2026-06-16 | Semantic transactions and irreversible effects | AFW side-effect release must be source-field authority, not transaction lifecycle. |
| Authorization Propagation in Multi-Agent AI Systems: Identity Governance as Infrastructure | https://arxiv.org/abs/2605.05440 | 2026-05-06 | Authorization propagation and delegation | AFW delegation rows must be field-level consumption checks, not global identity governance. |
| A Framework for Formalizing LLM Agent Security | https://arxiv.org/abs/2603.19469 | 2026-03-19 | Contextual security, source authorization, action/data isolation | AFW must be a concrete proof object, not a new general security framework. |
| Methods for Formal Verification of Agent Skills: Three Layers Toward a Mechanically Checkable Capability-Containment Proof | https://arxiv.org/abs/2605.23951 | 2026-05-09 | Proof-carrying skill containment | AFW should use skill artifacts as sources, not claim skill-containment novelty. |
| Formal Analysis and Supply Chain Security for Agentic AI Skills | https://arxiv.org/abs/2603.00195 | 2026-02-27 | Skill supply-chain security | AFW should avoid static skill scanning as the main contribution. |
| Skill-Inject: Measuring Agent Vulnerability to Skill File Attacks | https://arxiv.org/abs/2602.20156 | 2026-02-23 | Skill-file attack benchmark | AFW skill rows must be benign-skill downstream laundering, not malicious skill injection. |
| Agent Skills for Large Language Models: Architecture, Acquisition, Security, and the Path Forward | https://arxiv.org/abs/2602.12430 | 2026-02-12 | Skill-driven agent architecture and security framing | Supports skill-driven setting but blocks broad "skills are new" framing. |

## Needs Re-Check Before Final Bibliography

| Candidate | Why it matters | Current status |
|---|---|---|
| Consent Integrity for LLM agents | Very close to approval and consent scope | Mentioned in prior scans; exact arXiv/API verification pending. |
| MCP runtime security invariants | Very close to runtime/protocol safety | Mentioned in prior scans; exact arXiv/API verification pending. |
| SkillsBench | Skill benchmark framing | Query did not return in the latest arXiv API exact search; re-check title/id before citation. |

## Pressure Synthesis

The literature blocks four easy paper stories:

1. **Generic certificate story is blocked.** PCAA already owns proof-carrying action framing.
2. **Generic provenance/authorization story is blocked.** AuthGraph and protocol-composition work already cover broad source/authorization alignment.
3. **Generic skill-security story is blocked.** SkillGuard and formal skill verification already occupy permission and containment.
4. **Generic tool/intent/consent story is blocked.** ToolPrivBench, IGAC, Cordon, and consent/scope work pressure tool choice, user-intent narrowing, side effects, and approval.

The remaining viable innovation space is narrower:

> field-local semantic-role validity under source transformation, composition, and boundary-preserving role mismatch.

## Consequences for Our Direction

AFW should now be framed with three differentiators:

1. **Boundary-preserving role mismatch:** even when field, operation, data, effect, and delegation scopes are correct, the source may lack the semantic role required by the field.
2. **Derived-artifact attenuation:** summaries, skill outputs, and compressed traces must not inherit approval, risk-gate, publication, or delegation authority unless explicitly re-authorized.
3. **Compositional but non-amplifying authority:** multiple limited authorities can jointly satisfy a field, but cannot create a new semantic role absent from the consumed sources.
4. **Minimal authority witness:** the checker can expose the smallest capability subset that justifies a field, rather than only saying that an intent or credential was valid.

If the paper cannot demonstrate these, the novelty collapses back into authorization/provenance vocabulary.
