# Agent Action Invariance Experiment Seed

Date: 2026-07-01

This is a minimum viable experiment plan for the new direction:

```text
Policy-Supervised Agent Action Invariance
```

## 1. Core Claim To Test

Strict agent supervision can block attacks but also change legitimate behavior. A good guard should satisfy both:

```text
Soundness:
  unsafe / unauthorized fields do not execute.

Transparency:
  already-authorized fields are preserved.
```

AFW-specific claim:

> CapGuard preserves witness-backed action fields while blocking or routing only fields whose authority coverage fails.

## 2. Why Current AFW Data Is Enough For A First Probe

Existing project artifacts already contain the needed paired structure:

| Requirement | Existing artifact |
|---|---|
| Legal action fields | `examples/afw_*_rows.json` legal consumptions |
| Laundered action fields | `examples/afw_*_rows.json` laundered consumptions |
| Strict-block baseline | `strict_block` in AFW bench summaries |
| Weak permissive baselines | permission-only, attribution-only, boundary-scope-only |
| Field witness | CapGuard minimal authority witness |
| Runtime final-action rewrite | `guardrail.afw_capguard` routes unauthorized candidates to human approval |

Current result already hints at the theorem:

```text
CapGuard:
  legal preservation = 1.0
  laundering block   = 1.0

Strict-block:
  legal preservation = 0.0
  laundering block   = 1.0
```

Interpretation:

```text
Strict-block is sound but not transparent.
CapGuard is sound and transparent on the paired slice.
```

## 3. New Metrics

### 3.1 Authorized Field Preservation

```text
AFP(G) =
  # authorized fields unchanged by guard G
  / # authorized fields proposed by the nominal agent
```

For deterministic paired rows:

```text
authorized field = legal_consumption
unchanged = guard allows the legal field
```

### 3.2 Unauthorized Field Suppression

```text
UFS(G) =
  # unauthorized fields blocked / abstained / routed to review
  / # unauthorized fields proposed by the nominal agent
```

For paired rows:

```text
unauthorized field = laundered_consumption
suppressed = guard blocks or abstains
```

### 3.3 Minimal Field Edit Distance

For a structured action:

```text
d(a', a) =
  sum_f w_f * 1[a'.f != a.f]
```

Suggested weights:

```text
answer/body/citations: low
risk_report/risk_level: high
requires_human_approval: high
side_effect/delegation/data_write_scope: very high
```

Strict-block has high distance because it changes the whole action.
Field repair should have lower distance because it preserves safe fields.

### 3.4 Witness-Backed Transparency

```text
WBT(G) =
  # fields with covers_need=true whose values are preserved
  / # fields with covers_need=true
```

This is stronger than generic utility:

> It says the guard did not change exactly those fields for which it has a minimal authority witness.

### 3.5 Conservative Collapse Rate

```text
CCR(G) =
  # safe tasks or safe fields changed / blocked by G
  / # safe tasks or safe fields
```

This is the paper-friendly name for "agent 被防御搞得过于保守".

### 3.6 Fieldwise Maximal Permissiveness

From supervisory control theory, a good supervisor is not merely safe; it should be as permissive as possible under the safety specification.

AFW-local version:

```text
FMP(G) =
  1 iff G suppresses no field f for which ValidAuthority(s,f) holds,
  and suppresses or routes every field for which ValidAuthority(s,f) fails.
```

CapGuard should satisfy this locally under independent-field assumptions:

```text
covered field    -> preserve
uncovered field  -> suppress / repair / review-route
```

Strict-block fails because it suppresses covered fields when any field is unsafe.

### 3.7 Nonblocking Completion Distance

Also from supervisory control:

```text
safe is not enough if the supervisor blocks all paths to task completion.
```

For agent traces:

```text
NCD(G, t) =
  minimum additional safe steps needed to complete the task
  after guard G transforms trace prefix t
```

Approximate short-run metric:

```text
legal_trace_completion_rate =
  # legal tasks that still reach a safe final answer after guard
  / # legal tasks
```

Longer-run metric:

```text
mean_completion_distance_delta =
  mean_t NCD(G,t) - NCD(no_guard,t)
```

## 4. Baselines

| Baseline | Expected safety | Expected transparency | What it proves |
|---|---:|---:|---|
| no guard | low | high | utility without safety |
| strict-block | high | low | safety by conservatism |
| permission-only | low-medium | high | tool permission is insufficient |
| attribution-only | low-medium | high | influence tracking is insufficient |
| boundary-scope-only | medium | high | scope checks miss semantic role |
| CapGuard | high | high | field-level authority enables precise enforcement |
| CapGuard + field repair | high | highest task preservation | minimal intervention beyond whole-action routing |

## 5. First Experiment Table

Minimum table:

| Method | UFS ↑ | AFP ↑ | WBT ↑ | FMP ↑ | CCR ↓ | Mean edit cost ↓ |
|---|---:|---:|---:|---:|---:|---:|
| no guard | low | high | high | low | low | low |
| strict-block | high | low | low | low | high | high |
| permission-only | low | high | high | low | low | low |
| attribution-only | low | high | high | low | low | low |
| boundary-scope-only | medium | high | high | low-medium | low | low |
| CapGuard | high | high | high | high | low | medium |
| CapGuard + field repair | high | high | high | high | lowest | low-medium |

The table should not claim broad live-agent results until run on multi-step traces.

## 6. Formal Theorem Seed

If CapGuard's field decision rule is:

```text
allow(s,f) iff ValidAuthority(s,f)
block/abstain otherwise
```

and its output transformation only rewrites fields with non-allow decisions, then:

```text
Theorem 1: Field soundness.
No field without valid authority executes.

Theorem 2: Field transparency.
Every field with valid authority and no counter-authority is preserved.

Theorem 3: Strict-block is not transparent.
If a safe action has at least one authorized protected field,
strict-block changes or suppresses that field.

Theorem 4: Local fieldwise maximal permissiveness.
Under independent field effects and explicit source-to-field consumption,
CapGuard allows every authority-safe field and no authority-unsafe field.
```

This is a small but clean theoretical contribution.

## 7. Immediate Implementation Delta

No new guard is needed for the first version. Add only reporting:

1. Add `authorized_field_preservation`.
2. Add `witness_backed_transparency`.
3. Add `conservative_collapse_rate`.
4. Add `fieldwise_maximal_permissiveness`.
5. Add a simple field-edit distance for runtime candidate/final action pairs.
6. Add a short-trace proxy for `legal_trace_completion_rate`.
7. Re-render deterministic and runtime suite reports.

Second version:

1. Add `field_repair` mode.
2. Keep safe answer/citation fields when only side-effect / delegation / risk field fails.
3. Compare whole-action review routing vs field repair.

## 8. Reviewer-Safe Contribution Statement

Use:

> We connect runtime-enforcement transparency to LLM agent guardrails and instantiate it at action-field granularity through authority witnesses.

Avoid:

> We are the first to study over-refusal or safety-utility trade-offs in agents.

## 9. Decision

This direction is worth pursuing as the next paper refinement because it:

1. has a traditional formal theory anchor;
2. answers the user's concern about over-conservative agents;
3. reuses current AFW artifacts;
4. creates a sharper difference from SafeHarbor / Tri-Guard / ShieldAgent;
5. turns "minimal authority witness" into more than an explanation object: it becomes the certificate for field transparency.
