# Iteration 046: Frontier Novelty Re-Triage

## Motivation

The live-provider workflow is now machine-checkpointed, but the run is blocked by the missing `OPENAI_API_KEY`. The highest-value offline iteration is therefore to tighten Phase 1 novelty/citation risk before claiming the paper contribution.

## Sources Checked

This is a frontier triage, not a final manuscript citation audit. I checked primary arXiv pages for the closest agent-security neighbors:

| Work | Primary URL | Why it matters |
|---|---|---|
| AttriGuard | https://arxiv.org/abs/2603.10749 | Directly covers action-level causal attribution for tool invocations under indirect prompt injection. |
| CausalArmor | https://arxiv.org/abs/2602.07918 | Covers privileged-decision attribution and selective sanitization when untrusted context dominates user intent. |
| PlanGuard | https://arxiv.org/abs/2604.10134 | Covers isolated planning, hard constraints, and parameter-deviation verification. |
| PromptArmor | https://arxiv.org/abs/2507.15219 | Strong prompt-injection sanitization baseline; should be treated as a required baseline family. |
| AgentSentry | https://arxiv.org/abs/2602.22724 | Covers temporal causal takeover and context purification in multi-turn agents. |
| Agent-Sentry | https://arxiv.org/abs/2603.22868 | Covers execution provenance bounds, argument provenance, and sensitive-argument allowlists. |
| AIRGuard | https://arxiv.org/abs/2605.28914 | Covers action-time runtime authority control and least-privilege enforcement. |
| AgentSecBench | https://arxiv.org/abs/2605.26269 | Covers intent-to-execution noninterference, prompt injection, privacy leakage, and tool-use integrity. |
| MT-AgentRisk | https://arxiv.org/abs/2602.13379 | Covers multi-turn tool-using safety risk benchmark design. |
| Agent Security Bench | https://arxiv.org/abs/2410.02644 | Broad agent attack/defense benchmark; reduces novelty of generic agent-security benchmarking claims. |
| RAGForensics | https://arxiv.org/abs/2504.21668 | Covers traceback of poisoned texts in RAG systems. |
| RAGChecker | https://arxiv.org/abs/2408.08067 | Covers fine-grained RAG evaluation and diagnostic metrics. |
| ARES | https://arxiv.org/abs/2311.09476 | Covers automated RAG evaluation via lightweight judge training and component-level evaluation. |

## Novelty Verdict Update

### Reject Or Downgrade

- Reject as novelty: "EAIR is novel because it performs action-level causal attribution."
- Reject as standalone novelty: "HardGate is novel because it blocks unsafe tool actions."
- Downgrade: "EAIR-Bench is a first agent security benchmark." ASB, AgentSecBench, MT-AgentRisk, AgentDojo-style work, and related benchmarks make this too broad.
- Downgrade: "EAIR proves official AttriGuard/PlanGuard/AgentSentry fail." Current experiments only support style-baseline blind spots unless official methods are reproduced or textually audited in detail.

### Keep With Caution

- Keep: EAIR-Bench targets a narrower admissibility question: when retrieved evidence should be allowed to influence a high-risk action.
- Keep: Evidence sufficiency is the differentiator, especially independent source support, freshness/version currentness, conflict status, and parameter-level evidence backing.
- Keep: legitimate-vs-hijack evidence influence remains the cleanest hook, but it should be framed as a benchmark property and audit target, not a claim that no prior work considers benign influence.

## Revised Positioning

EAIR should be framed as:

```text
claim-level evidence-to-action admissibility for high-risk RAG-agent decisions
```

not as:

```text
the first action-level attribution or runtime guard framework
```

The closest prior works mainly ask whether untrusted context controlled or authorized a tool/action. EAIR-Bench should instead ask whether a retrieved evidence path is sufficiently trusted, source-diverse, fresh/current, low-conflict, and low-poison to legally support the specific decision, parameter value, approval flag, or risk report.

## Implication For Next Experiments

The next empirical step should compare against closer proxies, not only the original simple baselines:

- AttriGuard/CausalArmor-style dominance attribution;
- AIRGuard-style authority control;
- Agent-Sentry-style provenance/argument-bound check;
- PlanGuard-style intent and parameter consistency;
- PromptArmor-style sanitization;
- RAGForensics-style poison traceback;
- RAGChecker/ARES-style RAG faithfulness/evaluation.

These should be described as paper-faithful proxy baselines unless official implementations are integrated.

## Claim Boundary

This iteration strengthens novelty discipline. It does not complete the final citation audit, does not reproduce official systems, and does not add live-model evidence.

## Decision

Revise. The project remains viable, but the novelty claim must be narrower and more disciplined:

```text
EAIR-Bench + Evidence Sufficiency + Legitimate-vs-Hijack Evidence Influence
```

with action-level attribution and hard runtime gates treated as nearby prior-work territory rather than primary novelty.
