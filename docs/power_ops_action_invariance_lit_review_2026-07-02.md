# Power-Ops Action Invariance Literature Review

## Scope

This note checks the closest research around strict guardrails, LLM-agent runtime enforcement, prompt-injection defenses, least-privilege tool exposure, and over-defense. The goal is to position the current project slice:

```text
field-level authority witness + fieldwise repair + action invariance under intervention
```

not as "the first agent guardrail", but as a narrower mechanism for preserving authorized action fields while removing blocked or abstained fields.

## Search And Verification

- Date: 2026-07-02
- Sources: web search over arXiv/OpenReview/project docs
- Local paper library: no `papers/` or `literature/` directory found
- Helper verification: no local `verify_papers.py` or ARIS fetchers found under `.aris/tools` or `tools`
- Verification status convention:
  - `verified-arxiv`: title/authors/abstract checked on arXiv page
  - `verified-openreview-search`: OpenReview result found, but page blocked by browser challenge during open
  - `verified-project-doc`: already recorded in local project novelty docs
  - `caution`: source has metadata inconsistency or is too fresh to treat as a settled anchor

## Closest Work Table

| Paper | Status | Main Object | What It Pressures | Delta For Us |
|---|---|---|---|---|
| [AgentSpec: Customizable Runtime Enforcement for Safe and Reliable LLM Agents](https://arxiv.org/abs/2503.18666), Wang et al., 2025/ICSE 2026 | verified-arxiv | DSL for runtime constraints with triggers, predicates, enforcement | Blocks broad "runtime enforcement for LLM agents" novelty | We are not a general rule DSL; our object is field-level `Cap(x)` covers `Need(s,f)`, with repair preserving allowed fields. |
| [AgentVisor: Defending LLM Agents Against Prompt Injection via Semantic Virtualization](https://arxiv.org/abs/2604.24118), Ying et al., 2026 | verified-arxiv | Semantic privilege separation and trusted visor around tool calls | Pressures "security/utility tradeoff" and "semantic privilege separation" claims | Our repair acts inside a proposed action payload, not only at tool-call mediation; we output field witnesses and partial-human-review fields. |
| [AgentSentry: Mitigating Indirect Prompt Injection in LLM Agents via Temporal Causal Diagnostics and Context Purification](https://arxiv.org/abs/2602.22724), Zhang et al., 2026 | verified-arxiv | Temporal causal takeover localization and safe continuation | Directly overlaps with "avoid conservative blocking" motivation | AgentSentry purifies context after takeover diagnosis; our method checks source authority per action field and verifies the repaired final action frame. |
| [Defeating Prompt Injections by Design / CaMeL](https://arxiv.org/abs/2503.18813), Debenedetti et al., 2025 | verified-arxiv | Control/data-flow extraction plus capability-style policies | Pressures capability and provenance claims | CaMeL protects program flow and data exfiltration; our slice focuses on action-field authority consumption and local maximal preservation. |
| [Design Patterns for Securing LLM Agents against Prompt Injections](https://arxiv.org/html/2506.08837v3), Beurer-Kellner et al., 2025 | verified-arxiv | Secure design patterns and tradeoffs for application-specific agents | Blocks "application-specific secure agent design" novelty | We can cite this as system-design background; our contribution should be a specific formal relation plus benchmark metrics. |
| [Towards Verifiably Safe Tool Use for LLM Agents](https://arxiv.org/abs/2601.08012), Doshi et al., 2026 | verified-arxiv | STPA-derived enforceable specifications over data flows and tool sequences, capability-enhanced MCP | Pressures "formal guarantee for tool use" and MCP capability framing | We are not claiming the first verifiable tool-use framework; we define fieldwise authority and repair validity as a testable sub-property. |
| [When Lower Privileges Suffice / ToolPrivBench](https://arxiv.org/abs/2606.20023), Yang et al., 2026 | verified-arxiv | Over-privileged tool selection and least-privilege tool choice | Blocks simple "least-privilege agent tools" novelty | ToolPrivBench asks whether the chosen tool privilege is too high; we ask whether each action field is justified by the authority of its source. |
| [Capability Minimization as a Safety Primitive / RACG](https://arxiv.org/html/2606.13884v1), Iyer and Babu, 2026 | caution | High-risk tool exposure gated by causal necessity and authorization provenance | Strong pressure on "capability minimization preserves utility" | Closest conceptual neighbor. Our remaining delta is below tool exposure: once a mixed action exists, preserve allowed fields and remove invalid fields with witnesses. |
| [AgentDojo](https://arxiv.org/abs/2406.13352), Debenedetti et al., 2024 | verified-arxiv | Dynamic benchmark for prompt-injection attacks and defenses in tool agents | Benchmark baseline and evaluation pressure | We should eventually add AgentDojo-style tasks or map our fieldwise metrics onto its utility/security split. |
| [InjecGuard](https://arxiv.org/abs/2410.22770), Li and Liu, 2024/2025 | verified-arxiv | Over-defense in prompt-injection guard models | Pressures over-defense/false-positive motivation | It measures benign prompt false alarms; our over-conservatism metric is final-action loss of authorized fields. |
| [AI Agents with Formal Security Guarantees](https://openreview.net/forum?id=c6jNHPksiZ), Balunovic et al., 2024 | verified-openreview-search | Agent plus security analyzer for formal behavior guarantees | Blocks broad "formal security guarantee for agents" novelty | We should treat this as foundational related work; safe claim is a narrower field-repair invariant and artifacts. |

## Landscape Summary

The field has moved beyond simple post-hoc guardrails. AgentSpec, AgentVisor, CaMeL, formal-security-agent work, and verifiably safe tool-use work all push toward structured runtime enforcement, capability-style policy, or formal safety constraints. So the project must not claim novelty as a generic runtime guard, prompt-injection defense, capability system, or MCP safety layer.

The exact user concern, "strict intervention can make agents overly conservative", is also not new as motivation. InjecGuard studies over-defense in prompt injection guard models; AgentVisor explicitly frames a security/utility tradeoff; AgentSentry directly criticizes conservative blocking of high-risk actions and proposes safe continuation via context purification. This means our paper should not sell over-defense as a newly discovered problem.

The still defensible niche is lower-level and more auditable: define the action as a structured payload, define each field's required authority, and require a minimal witness for preserving that field. If a guard intervenes, it should satisfy a repair invariant: authorized fields remain unchanged, invalid fields are removed or routed to human review, and the final action carries evidence of exactly what was preserved and why.

The strongest conceptual pressure is RACG and ToolPrivBench. They ask whether a high-risk tool should be exposed or selected under least privilege. Our question starts after a candidate action exists: if it contains both safe and unsafe fields, should the whole action be killed, or can we preserve the authorized sub-action? That narrower question is where `whole_action_block_rate`, `executable_fieldwise_repair_success_rate`, and `repair_frame_validity_rate` matter.

## Positioning Takeaway

Safe headline:

> We study field-level action invariance under strict agent supervision: when a guard blocks or abstains on unsafe fields, the final executable action should preserve authorized fields and remove only the invalid authority frame.

Unsafe headlines:

- First LLM-agent guardrail.
- First runtime monitor for LLM agents.
- First formal security framework for agents.
- First least-privilege agent method.
- First over-defense benchmark.
- First prompt-injection defense that preserves utility.

## Immediate Research Gap

The current implementation has a useful artifact but a limited evaluation:

- Strong: formal objects, runnable FormalTrust nodes, curated power-ops cases, fieldwise repair, repair validity, trace/span/OTLP replay, 210 passing tests.
- Weak: no real production traces, no AgentDojo-style independent benchmark, no official baseline implementation comparison, no large-scale annotation agreement.

Next empirical step should be either:

1. Add a stronger baseline: strict block, tool-level least privilege, provenance-only, and fieldwise repair compared on the same mixed-action cases.
2. Add a real or semi-real power-agent trace suite with span/OTLP logs.
3. Map at least a small AgentDojo-like task into fieldwise action invariance to show the metric generalizes beyond curated power-ops cases.
