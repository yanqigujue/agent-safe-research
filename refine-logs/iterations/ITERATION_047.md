# Iteration 047: WarrantGuard Method Upgrade

## Motivation

The previous novelty triage showed that action attribution, runtime authority control, provenance bounding, and plan verification are crowded. The user explicitly encouraged a more breakthrough-style method design and approved upgrading the main method to WarrantGuard / ActionWarrant.

## Method Shift

Old framing:

```text
retrieved evidence -> action -> EAIR gate
```

New framing:

```text
retrieved evidence -> claim graph -> warrant builder -> warrant verifier -> proof-carrying action
```

The agent emits:

```text
Agent(q, K) -> (a, W_a)
```

and execution is allowed only when:

```text
Execute(a) iff
  HardGate(a) = PASS
  and VerifyWarrant(a, W_a) = PASS
  and CounterWarrant(a, W_a) = CLEAR.
```

## Implementation

Added minimal WarrantGuard objects to `formaltrust_platform.experiments.eair_bench`:

- `ActionWarrant`
- `WarrantVerification`
- `build_action_warrant`
- `verify_action_warrant`

The current verifier checks:

- decision warrant sufficiency;
- approval warrant presence for approval-required cases;
- risk-level warrant presence for high-risk cases;
- risk-report warrant presence for high-risk cases;
- parameter warrant presence for bounded/action parameters;
- hard-gate violation;
- counter-warrant presence.

## TDD

Added tests:

- `test_warrantguard_rejects_missing_high_risk_field_warrant`
- `test_warrantguard_accepts_full_evidence_backed_action_warrant`

Red step:

```text
pytest tests/test_eair_bench.py -k "warrantguard" -q
```

failed because `ActionWarrant` did not exist.

Green step:

```text
pytest tests/test_eair_bench.py -k "warrantguard" -q
```

passed with `2 passed`.

Full verification:

```text
pytest -q
```

passed with `81 passed`.

## Documentation Updated

- `DERIVATION_PACKAGE.md`
- `PAPER_PLAN.md`
- `refine-logs/FINAL_PROPOSAL.md`
- `docs/rag_agent_research_directions.md`
- `task_plan.md`
- `progress.md`
- `refine-logs/CLAIM_EVIDENCE_AUDIT.md`
- `figures/fig1_eair_main_chain.svg`
- `docs/superpowers/plans/2026-06-21-warrantguard-actionwarrant.md`

## Claim Boundary

This iteration establishes the method abstraction and a minimal verifier interface. It does not yet:

- integrate WarrantGuard as a separate baseline in the deterministic pilot;
- make live-model claims;
- reproduce official AttriGuard, CausalArmor, PlanGuard, AIRGuard, Agent-Sentry, PromptArmor, RAGForensics, RAGChecker, or ARES.

## Decision

Revise and strengthen. EAIR-Gate becomes the verifier component inside WarrantGuard, while the paper's sharper method identity becomes:

```text
proof-carrying RAG-agent actions
```
