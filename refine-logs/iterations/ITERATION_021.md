# Iteration 021: Frontiers Re-tighten Around Evidence Sufficiency

Date: 2026-06-20

## Goal

Answer the practical question: after 20 implementation iterations, what should the project do next?

## Frontier Update

The next step should be novelty-risk reduction, not more UI/figure polishing. Fresh search surfaced additional close neighbors:

- AttriGuard: action-level causal attribution of tool invocations.
- CausalArmor: attribution-margin defense at privileged decision points.
- AIRGuard: runtime authority control for side-effecting agent actions.
- AgentSentry / Agent-Sentry: temporal causal takeover and execution-provenance bounds.
- PlanGuard: isolated planner and hierarchical hard/intent verification.
- Evidence Tracing and Execution Provenance survey: provenance is now a broad organizing framework for agent trust.

## Decision

Revise the paper positioning.

Keep:

- EAIR-Bench as the primary contribution.
- EvidenceSufficient as the main method/property axis.
- Legitimate-vs-hijack evidence influence as the conceptual hook.
- HardGate + EvidenceSufficient + soft EAIR as the final allow rule.

Downgrade:

- Any claim that action-level attribution itself is novel.
- Any claim that HardGate/runtime action guarding is novel by itself.
- Any claim of superiority over official AttriGuard, CausalArmor, AIRGuard, AgentSentry, Agent-Sentry, PlanGuard, or PromptArmor implementations.

## Current Evidence

The latest deterministic EAIR-Bench pilot has:

- 12 conditions.
- 13 baselines.
- 156 baseline-case results.
- `eair_full` at `unsafe_decision_rate=0.0000`, `unsupported_action_rate=0.0000`, `parameter_violation_rate=0.0000`, `false_positive_rate=0.0000`.
- `eair_full` over-refusal remains `0.3333`, so utility/sufficiency tradeoff is not solved.

## What This Supports

- The synthetic pilot supports system-behavior claims about targeted failure modes.
- It supports the decomposition of HardGate, EvidenceSufficient, and soft EAIR/path-poison warning.
- It supports benchmark-driven positioning more than method-superiority positioning.

## What It Does Not Support Yet

- It does not prove deployment safety.
- It does not prove official AttriGuard/CausalArmor/AIRGuard/Agent-Sentry failures.
- It does not prove novelty of generic action attribution, runtime authority control, or execution provenance.
- It does not yet support a strong real-world effectiveness claim because the pilot is deterministic and synthetic.

## Next Iteration

The next concrete iteration should add a stronger closest-neighbor baseline slice:

1. AIRGuard-style authority-control baseline.
2. CausalArmor-style dominance-attribution baseline.
3. Agent-Sentry-style provenance-bound baseline.
4. A less naive AttriGuard-style baseline that blocks dominance by untrusted control signals rather than all external evidence influence.
5. A case-type robustness sweep over all EAIR-Bench case types with coverage gates enabled.

## Bottom Line

Do not polish `figures/fig1_eair_main_chain.svg` yet. First, make the figure and paper story reflect the narrowed thesis:

```text
EAIR-Bench evaluates whether retrieved claims provide sufficient, trusted, current, source-diverse, policy-compatible evidence for high-risk RAG-agent actions.
```
