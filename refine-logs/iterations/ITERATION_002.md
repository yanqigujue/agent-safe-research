# Iteration 002: Frontier Check and Novelty Repositioning

Date: 2026-06-17

## Core Hypothesis

EAIR remains viable only if framed as evidence-to-action admissibility for context-dependent high-risk actions, not as a generic action attribution or indirect prompt-injection defense.

## Frontier Evidence Checked

Areas checked:

- RAG poisoning / retrieval exposure
- RAG traceback / source attribution
- RAGAS / ARES / RAGChecker-style faithfulness evaluation
- ConflictRAG / FaithfulRAG / TruthfulRAG / conflicting-evidence RAG
- AgentDojo / Agent Security Bench / MT-AgentRisk
- PromptArmor / PlanGuard / AttriGuard / AgentSentry / Agent-Sentry / IntentGuard

Representative primary sources were recorded directly in `findings.md` and `refine-logs/CLAIM_EVIDENCE_AUDIT.md`.

## Changed Novelty Positioning

Downgraded unsafe claims:

- Do not claim EAIR is the first action-level RAG safety method.
- Do not claim action-level causal influence is itself the novelty.
- Do not claim AttriGuard/AgentSentry/PlanGuard/PromptArmor are subsumed.

Strengthened safer positioning:

```text
EAIR-Bench evaluates whether retrieved evidence should be allowed to influence high-risk RAG-agent actions, based on evidence sufficiency, trust, freshness, conflict, poison risk, and hard action policy constraints.
```

## Supported Conclusions

- Retrieval poisoning is a crowded background area; PRE/RHE are baselines.
- RAG source attribution is close but usually explains generated output responsibility rather than action admissibility.
- Claim-level faithfulness is necessary but insufficient for action decision/tool/approval/parameter safety.
- Conflict-aware RAG is useful but does not cover conflict-free evidence insufficiency.
- Agent IPI defenses are the closest novelty risk; EAIR must compare against them explicitly.

## Weakened / Unresolved

- Official AttriGuard/AgentSentry/PlanGuard/PromptArmor limitations are not yet proven by reproduction.
- “EAIR-Bench is first” remains unsupported.
- We still need a deeper per-paper table for related-work writing, including exact abstract-level deltas and official implementation assumptions.

## Files Updated

- `findings.md`
- `refine-logs/CLAIM_EVIDENCE_AUDIT.md`
- `progress.md`
- `task_plan.md`

## Decision

`revise + keep`

Keep the EAIR-Bench direction, but revise novelty wording downward. The paper should sell the benchmark/evidence-admissibility framing, not the existence of action attribution.

## Next Iteration Questions

1. Can we construct ablations that separate `HardGate`, `EvidenceSufficient`, and soft `EAIR(q,a)`?
2. Does the official AttriGuard method over-block legitimate evidence influence, or only our style baseline?
3. Which agent-security systems should be reimplemented as stronger baselines rather than described as related work?
4. Can we connect the benchmark to real LLM structured action generation without weakening deterministic oracle clarity?
