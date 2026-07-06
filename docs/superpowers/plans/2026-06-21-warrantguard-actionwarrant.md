# WarrantGuard ActionWarrant Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Upgrade the EAIR method framing from a gate-only design to WarrantGuard, where high-risk RAG-agent actions must carry verifiable evidence warrants.

**Architecture:** Add a minimal `ActionWarrant` representation and `verify_action_warrant` function beside the existing EAIR-Bench action/evidence logic. Keep the existing EAIR gate intact for compatibility, but add WarrantGuard as the method-level abstraction and a tested verifier that can later be wired into full baselines.

**Tech Stack:** Python dataclasses, pytest, existing `formaltrust_platform.experiments.eair_bench` module, Markdown/SVG documentation.

---

### Task 1: Minimal Warrant Verifier

**Files:**
- Modify: `formaltrust_platform/experiments/eair_bench.py`
- Test: `tests/test_eair_bench.py`

- [ ] **Step 1: Write the failing tests**

Add tests that import `ActionWarrant`, `verify_action_warrant`, `build_action_warrant`, and `WarrantVerification`.

Expected behaviors:

```python
def test_warrantguard_rejects_missing_high_risk_field_warrant() -> None:
    sample = _sample("risk_report_downgrade_no_tool")
    action = AgentAction(
        decision="reject_bypass",
        tool="none",
        risk_level="low",
        requires_human_approval=True,
        supporting_claims=sample.case.required_claims,
        rationale="Reject bypass but suppress review.",
        risk_report="safe_no_review",
    )
    warrant = ActionWarrant(
        decision_claims=sample.case.required_claims,
        parameter_claims={},
        approval_claims=(),
        risk_level_claims=(),
        risk_report_claims=(),
        counter_claims=(),
    )

    result = verify_action_warrant(sample.case, sample.evidence, action, warrant)

    assert result.passed is False
    assert "approval_warrant_missing" in result.errors
    assert "risk_level_warrant_missing" in result.errors
    assert "risk_report_warrant_missing" in result.errors
```

```python
def test_warrantguard_accepts_full_evidence_backed_action_warrant() -> None:
    sample = _sample("clean_sufficient_evidence")
    action = AgentAction(
        decision=sample.case.oracle_decision,
        tool=sample.case.oracle_tool,
        risk_level=sample.case.risk_level,
        requires_human_approval=sample.case.human_approval_required,
        supporting_claims=sample.case.required_claims,
        rationale="Evidence-backed action.",
        risk_report="human_review_required",
    )
    warrant = build_action_warrant(sample.case, sample.evidence, action)

    result = verify_action_warrant(sample.case, sample.evidence, action, warrant)

    assert result.passed is True
    assert result.errors == ()
    assert result.support_cluster_count >= sample.case.min_support_clusters
```

- [ ] **Step 2: Run tests to verify they fail**

Run:

```powershell
pytest tests/test_eair_bench.py -k "warrantguard" -q
```

Expected: FAIL because `ActionWarrant` / `verify_action_warrant` do not exist.

- [ ] **Step 3: Implement minimal verifier**

Add dataclasses:

```python
@dataclass(frozen=True)
class ActionWarrant:
    decision_claims: tuple[str, ...]
    parameter_claims: dict[str, tuple[str, ...]] = field(default_factory=dict)
    approval_claims: tuple[str, ...] = ()
    risk_level_claims: tuple[str, ...] = ()
    risk_report_claims: tuple[str, ...] = ()
    counter_claims: tuple[str, ...] = ()


@dataclass(frozen=True)
class WarrantVerification:
    passed: bool
    errors: tuple[str, ...]
    warnings: tuple[str, ...]
    support_cluster_count: int
    support_freshness: float
    support_current: bool
    superseded_support_count: int
```

Add:

```python
def build_action_warrant(case, evidence, action) -> ActionWarrant:
    ...

def verify_action_warrant(case, evidence, action, warrant) -> WarrantVerification:
    ...
```

Use existing support helpers: `support_cluster_count`, `support_freshness`, `support_current`, `superseded_support_count`, `evidence_sufficient_for_action`, and `hard_gate_violation`.

- [ ] **Step 4: Run focused tests**

Run:

```powershell
pytest tests/test_eair_bench.py -k "warrantguard" -q
```

Expected: PASS.

### Task 2: Method Reframing Docs And Figure

**Files:**
- Modify: `DERIVATION_PACKAGE.md`
- Modify: `PAPER_PLAN.md`
- Modify: `refine-logs/FINAL_PROPOSAL.md`
- Modify: `docs/rag_agent_research_directions.md`
- Modify: `figures/fig1_eair_main_chain.svg`
- Create: `refine-logs/iterations/ITERATION_047.md`
- Modify: `task_plan.md`
- Modify: `progress.md`

- [ ] **Step 1: Update derivation**

Add:

```text
Agent(q, K) -> (a, W_a)
Execute(a) iff HardGate(a)=PASS and VerifyWarrant(a,W_a)=PASS and CounterWarrant(a,W_a)=CLEAR.
```

- [ ] **Step 2: Update paper narrative**

Make WarrantGuard / ActionWarrant the primary method name and keep EAIR-Bench as the benchmark.

- [ ] **Step 3: Update figure**

Replace the old main chain with:

```text
Retrieved Evidence -> Claim Graph -> Warrant Builder -> Warrant Verifier -> Proof-Carrying Action -> Execute / Abstain / Escalate
```

- [ ] **Step 4: Record iteration**

Create `ITERATION_047.md` with motivation, design, implementation, tests, claim boundary, and next steps.

### Task 3: Verification

**Files:**
- Read: all modified docs and tests

- [ ] **Step 1: Run full tests**

Run:

```powershell
pytest -q
```

Expected: all tests pass.

- [ ] **Step 2: Run textual consistency checks**

Run:

```powershell
rg -n "WarrantGuard|ActionWarrant|Proof-Carrying|VerifyWarrant" DERIVATION_PACKAGE.md PAPER_PLAN.md refine-logs docs figures formaltrust_platform tests
```

Expected: new method appears in math, paper plan, docs, figure, code, and tests.

- [ ] **Step 3: Confirm no overclaim**

Run:

```powershell
rg -n "first action-level|official .*fails|outperforms official" DERIVATION_PACKAGE.md PAPER_PLAN.md refine-logs docs
```

Expected: only cautionary or unsupported-claim boundary text, not positive claims.
