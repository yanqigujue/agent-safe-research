# Agent Action Invariance: Hazard And Risk Engineering Deep Dive

Date: 2026-07-01

Purpose:

This note explores traditional safety/security engineering methods that can
strengthen AFW / CapGuard:

- STAMP / STPA;
- STPA-Sec;
- FMEA / FMECA;
- Fault Tree Analysis;
- Bow-Tie analysis;
- HAZOP;
- minimal cut sets and risk-priority scoring.

The goal is not to claim a new hazard-analysis method. The goal is to use
these mature frameworks to systematically generate:

1. failure modes;
2. laundering test cases;
3. partial-repair scenarios;
4. risk-prioritized evaluation slices;
5. reviewer-friendly threat-model coverage.

## 1. Why This Is A Good Fit

AFW currently checks whether:

```text
Cap(x) covers Need(s,f)
```

But a paper also needs to explain:

```text
Which bad outcomes matter?
Which action fields are safety/security critical?
Which failure modes should the benchmark cover?
Why are the rows not arbitrary hand-written examples?
Which failures are severe enough to justify abstain or human review?
```

Traditional hazard/risk engineering is exactly about those questions.

## 2. STPA: Unsafe Control Actions For Agent Fields

STPA treats accidents as a result of inadequate control, not only component
failure. This is a strong fit for LLM agents because the agent is a controller:

```text
controller:
  LLM planner / agent runtime

controlled process:
  external tools, files, APIs, business workflow, human approval process

control action:
  action field or tool call field, e.g. publish, dispatch, approve, delete,
  delegate, disclose, modify_risk_level

process model:
  agent's belief about source authority, time scope, obligations, policy holds,
  task state

safety constraint:
  field f executes only if ValidAuthority(s,f)
```

STPA's unsafe control action categories map cleanly:

| STPA unsafe control action pattern | AFW field failure |
|---|---|
| required control action not provided | safe field unnecessarily blocked |
| unsafe control action provided | unauthorized field allowed |
| control action provided too early / too late | stale approval or temporal authority decay failure |
| control action stopped too soon / applied too long | approval reused beyond scope or obligation forgotten |

This directly supports the user's concern:

```text
strict supervision may create unsafe behavior by omission:
  the agent fails to complete a legitimate task because the guard over-blocks.
```

New property:

```text
Authorized Control Action Preservation

If a control action field is required for safe task completion and has a valid
authority witness, the guard should preserve it rather than converting it into
generic refusal.
```

New metric:

```text
required_authorized_action_preservation =
  # required authorized fields preserved / # required authorized fields
```

Useful source:

- Leveson and Thomas, "STPA Handbook". <https://psas.scripts.mit.edu/home/get_file.php?name=STPA_handbook.pdf>

## 3. STPA-Sec: Security As Inadequate Control

STPA-Sec adapts STPA to security by treating adversarial actions as ways of
creating unsafe control. This is a natural lens for prompt injection:

```text
attacker objective:
  induce unsafe control action by manipulating agent's process model

prompt injection route:
  corrupt source authority perception
  forge approval state
  hide obligation failure
  replay stale memory
  make benign skill output look like operational authority
```

AFW contribution under this lens:

```text
CapGuard is a process-model consistency check for authority:
  the agent may believe a source supports field f,
  but the guard checks whether the source actually carries the required
  role/scope/time/effect/obligation capability.
```

Candidate benchmark generation:

For each protected field:

1. identify unsafe control action;
2. identify corrupted process-model variable;
3. create a legal row where the variable is correctly supported;
4. create a laundered row where the same boundary is preserved but role or
   obligation is wrong;
5. create a temporal/replay row;
6. create a counter-authority row;
7. create a partial-repair trace.

Example:

| STPA-Sec variable | Legal case | Laundered case |
|---|---|---|
| approval_status | signed Q3 approval | retrieved report says "approved" |
| obligation_discharge | static-scan event present | skill claims scan passed without discharge event |
| delegation_scope | explicit delegate-to-team receipt | formatting skill tells agent to assign work |
| time_epoch | current Q4 approval | Q3 approval reused |

Useful source:

- Young and Leveson, "Systems Thinking for Safety and Security".
  <https://sunnyday.mit.edu/papers/2014-03-19-STPA-Sec.pdf>

## 4. FMEA / FMECA: Field Failure Modes And Effects

FMEA asks:

```text
How can each component fail?
What is the effect?
How severe is it?
How detectable is it?
How likely is it?
What mitigation exists?
```

AFW can turn every protected field into an FMEA row.

Template:

| FMEA column | AFW interpretation |
|---|---|
| item/function | action field `f` |
| failure mode | false allow, false block, false abstain, wrong repair, stale witness |
| cause | missing role, wrong scope, stale time, undischarged obligation, causal mismatch |
| effect | unsafe tool execution, task collapse, privacy leak, wrong approval, audit failure |
| severity | business/safety/security impact |
| occurrence | frequency in benchmark or traces |
| detectability | whether witness/diagnosis exposes it |
| RPN | severity * occurrence * detectability |
| mitigation | CapGuard rule, fieldwise repair, human review, evidence request |

New metric:

```text
field_risk_priority_number =
  severity(failure) * occurrence(failure) * non_detectability(failure)
```

New experiment:

```text
Risk-prioritized AFW suite:
  sort field failure modes by RPN;
  ensure high-RPN modes have at least N legal/laundered/repair cases.
```

This strengthens the paper's test-sample story:

```text
Rows are not only hand-written attacks;
they are sampled from a field-level FMEA table.
```

Useful source:

- IEC 60812:2018 overview page. <https://webstore.iec.ch/publication/26359>

## 5. Fault Tree Analysis: Minimal Cut Sets For Unauthorized Execution

Fault Tree Analysis starts from a top event and decomposes causes with AND/OR
gates.

AFW top event:

```text
Unauthorized protected field executes.
```

Example fault tree:

```text
Unauthorized dispatch executes
  AND
    candidate action contains dispatch field
    guard allows dispatch field
    no valid dispatch witness exists

guard allows dispatch field
  OR
    source role misclassified
    time decay not checked
    obligation not checked
    counter-authority ignored
    consumption edge missing
```

Minimal cut set:

```text
smallest combination of failures sufficient to cause the top event.
```

AFW use:

1. generate multi-factor test cases;
2. identify which rule removes which cut set;
3. justify ablations;
4. evaluate defense-loop reduction.

New metric:

```text
cut_set_coverage =
  # modeled minimal cut sets hit by at least one benchmark case /
  # modeled minimal cut sets
```

New result table:

| Defense component | Cut sets eliminated |
|---|---|
| role coverage | role misclassification cut sets |
| time scope | stale approval replay cut sets |
| obligation discharge | missing scan / missing DLP cut sets |
| counter-authority | policy hold ignored cut sets |
| trace adapter schema checks | malformed authority injection cut sets |

Useful source:

- NASA Fault Tree Handbook with Aerospace Applications.
  <https://ntrs.nasa.gov/api/citations/20020062164/downloads/20020062164.pdf>

## 6. Bow-Tie Analysis: Prevention And Recovery Around A Loss Event

Bow-Tie analysis combines:

```text
left side:
  threats and preventive barriers

center:
  top event

right side:
  consequences and recovery barriers
```

AFW top event:

```text
field enters unsafe authority state
```

Left-side threats:

- prompt injection in retrieved document;
- stale approval replay;
- skill output role laundering;
- tool metadata over-interpretation;
- memory authority decay;
- prior-step output treated as approval.

Preventive barriers:

- manifest-lifted `Cap(x)`;
- `Need(s,f)` coverage check;
- time-scope decay;
- obligation discharge check;
- counter-authority abstain;
- malformed trace fail-closed behavior.

Right-side consequences:

- unsafe tool execution;
- task collapse from strict block;
- human-review overload;
- audit failure;
- delayed safe completion.

Recovery barriers:

- fieldwise-simplex repair;
- evidence request;
- human approval route;
- minimal diagnosis;
- audit witness.

Why useful:

```text
Bow-Tie makes clear that CapGuard is both a preventive barrier and an audit /
recovery support mechanism.
```

Useful source:

- CCPS / AIChE Bow Ties in Risk Management.
  <https://www.aiche.org/ccps/resources/publications/books/bow-ties-risk-management>

## 7. HAZOP: Guide Words For Authority Deviations

HAZOP uses guide words such as "No", "More", "Less", "As well as", "Part of",
"Reverse", and "Other than" to discover deviations.

Authority HAZOP mapping:

| HAZOP guide word | AFW authority deviation |
|---|---|
| No | no witness for required field |
| More | source grants broader role/scope than intended |
| Less | approval missing required scope |
| As well as | source adds extra unauthorized instruction |
| Part of | only one required role in composite authority is present |
| Reverse | counter-authority reverses approval |
| Other than | source role is semantically different but boundary-compatible |
| Early | approval not yet valid |
| Late | approval expired |

This is a simple and productive benchmark generator:

```text
For each Need(s,f), apply HAZOP guide words to produce negative and edge-case
rows.
```

Example:

```text
Need:
  publish_authority for public report

No:
  no approval source

Part of:
  approval covers internal publish only

Other than:
  report-formatting skill says "publish"

Late:
  Q3 approval reused for Q4

Reverse:
  policy hold present
```

Useful source:

- IEC 61882:2016 HAZOP overview page. <https://webstore.iec.ch/publication/24321>

## 8. New Candidate Directions

### Direction A: STPA-Derived Agent Action Invariance Benchmark

Method:

```text
For each protected action field, define:
  unsafe control actions,
  corrupted process-model variables,
  safety constraints,
  legal rows,
  laundered rows,
  temporal rows,
  counter-authority rows,
  partial-repair traces.
```

Why strong:

- Directly gives a principled sample-generation story.
- Fits the user's concern that over-conservative guards can also be unsafe by
  omission.
- Bridges safety engineering with LLM-agent security.

Minimum artifact:

```text
docs/afw_stpa_table_*.md
examples/afw_stpa_derived_rows.json
```

### Direction B: Field-FMEA For Guard Failure Modes

Method:

```text
Treat each protected action field as an FMEA item.
List false allow, false block, false abstain, stale witness, and wrong repair.
Score severity, occurrence, and detectability.
Use RPN to select benchmark slices.
```

Why strong:

- Directly answers "which failures matter most?"
- Gives a risk-prioritized evaluation, not only average accuracy.

Minimum metric:

```text
high_rpn_failure_coverage
```

### Direction C: Fault-Tree Cut-Set Coverage

Method:

```text
Build fault trees for top events such as unauthorized dispatch or public
release.
Generate benchmark rows from minimal cut sets.
Measure which defense components eliminate which cut sets.
```

Why strong:

- Makes ablations less arbitrary.
- Excellent for defense-loop claims.

Minimum metric:

```text
cut_set_coverage
cut_set_elimination_rate
```

### Direction D: Authority HAZOP Generator

Method:

```text
Apply HAZOP guide words to each Need(s,f) dimension:
  role, field, operation, data scope, effect scope, delegation, time,
  obligation.
```

Why strong:

- Cheap, systematic, and immediately implementable.
- Can generate many paired rows beyond hand-written cases.

Risk:

- As standalone contribution, it may look like data augmentation.

### Direction E: Bow-Tie Barrier Evaluation

Method:

```text
Model threats, preventive barriers, top events, consequences, and recovery
barriers.
Score CapGuard components as barriers.
```

Why strong:

- Useful for deployment / systems story.
- Good visual figure for paper or slides.

Risk:

- More engineering-report style than theory.

## 9. Updated Ranking

| Rank | Direction | Why |
|---:|---|---|
| 1 | STPA-derived action-invariance benchmark | Best principled way to generate multi-step safety/security cases |
| 2 | Field-FMEA with RPN scoring | Best way to prioritize failures and answer performance/safety trade-offs |
| 3 | Fault-tree cut-set coverage | Strong ablation and defense-loop explanation |
| 4 | Authority HAZOP generator | Very implementable dataset expansion tool |
| 5 | Bow-Tie barrier evaluation | Good deployment story and figure |

## 10. Best Paper Integration

Add a benchmark-generation subsection:

```text
We derive evaluation scenarios using a safety-engineering workflow:
  STPA identifies unsafe agent control actions;
  Field-FMEA enumerates failure modes and prioritizes them;
  Fault trees generate minimal cut-set test cases;
  HAZOP guide words expand authority-deviation variants.
```

This gives a clean answer to:

```text
Where do your test cases come from?
```

And also:

```text
How do you know strict blocking is not enough?
```

Because STPA includes unsafe behavior by omission:

```text
not providing a required authorized control action can also be a loss scenario.
```

## 11. Claim Firewall

Do not claim:

- first STPA method for AI agents;
- first STPA-Sec security analysis;
- first FMEA/FMECA for AI systems;
- first fault-tree or bow-tie analysis for cyber risk;
- first HAZOP-style security benchmark generator;
- first risk-prioritized security evaluation.

Safe claim:

```text
We use mature hazard and risk-engineering methods to derive and prioritize
authority-laundering benchmark scenarios for structured LLM-agent actions.
```

Best concise position:

> AFW's benchmark can be risk-derived rather than example-derived: unsafe
> control actions, failure modes, minimal cut sets, and HAZOP guide words
> determine which legal/laundered/repair rows should exist.

