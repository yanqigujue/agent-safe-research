# Agent Action Invariance: Control-Theory Deep Dive

Date: 2026-07-01

This note continues the theory search for AFW / CapGuard. The strongest new bridge in this round is:

```text
supervisory control theory for discrete-event systems
```

Why it matters:

> Supervisory control does not only ask whether a supervisor keeps a system safe. It also asks whether the controlled system is nonblocking and maximally permissive. That is almost exactly the "safe but not over-conservative agent" problem.

## 1. Best New Theoretical Hook

### Supervisory Control Theory

Classic supervisory control models a plant as a generator of discrete-event traces and synthesizes a supervisor that restricts the plant's behavior to satisfy a specification.

The useful triad is:

```text
safety:
  the supervised behavior stays inside the allowed language

nonblocking:
  the supervisor does not trap the system in states where task completion is impossible

maximal permissiveness / minimal restrictiveness:
  among safe supervisors, allow as much behavior as possible
```

This gives AFW a stronger vocabulary than "utility cost":

```text
strict-block may be safe but blocking.
permission-only may be permissive but unsafe.
CapGuard aims to be safe and fieldwise maximally permissive.
```

Key sources:

- Ramadge and Wonham, "Supervisory Control of a Class of Discrete Event Processes", SIAM Journal on Control and Optimization, 1987. <https://epubs.siam.org/doi/10.1137/0325013>
- Offline supervisory control synthesis taxonomy and recent results. <https://link.springer.com/article/10.1007/s10626-024-00408-z>
- Zhang et al., "Quantitatively Nonblocking Supervisory Control of Discrete-Event Systems". <https://arxiv.org/abs/2108.00721>

## 2. AFW Mapping

Map an agent run to a discrete-event system:

```text
Plant P:
  nominal LLM agent + tools + environment

Events Sigma:
  retrieval(x)
  source_lifted(Cap(x))
  propose_field(s, f, v)
  consume(x -> f, s)
  execute_field(s, f, v)
  route_to_review(s, f)
  complete_task

Supervisor S:
  CapGuard / AFW field guard

Specification K:
  authority safety + task progress + review obligations
```

Controllable vs uncontrollable:

```text
controllable events:
  execute_field
  call_tool
  write_file
  publish
  delegate
  route_to_review

uncontrollable events:
  user request
  retrieval result
  tool observation
  memory recall
  external environment update
```

Observable vs partially observable:

```text
observable:
  logged trace events, span logs, candidate actions, manifests

partially observable:
  hidden reasoning, implicit source influence, undocumented tool-side effects
```

This is useful because traditional supervisory control already has concepts for partial observation and uncontrollable events. That maps cleanly to agent traces where we cannot observe every reasoning token and cannot control every external event.

## 3. Fieldwise Maximal Permissiveness

Global maximally permissive supervision is hard for LLM agents. But AFW can claim a local fieldwise version.

Let:

```text
Auth(s, f) = ValidAuthority(s, f)
Exec(s, f) = field f executes at step s
```

Safety:

```text
forall s,f:
  Exec'(s,f) -> Auth(s,f)
```

Fieldwise maximal permissiveness:

```text
forall s,f:
  Auth(s,f) and NoConflict(s,f)
  -> Exec'(s,f) = Exec(s,f)
```

Equivalently:

```text
CapGuard suppresses no executable field that has a valid authority witness.
```

This is sharper than "high task success":

> It says exactly which parts of the agent action are guaranteed not to be unnecessarily changed.

## 4. Nonblocking Agent Guard

In supervisory control, a supervisor can be safe but bad if it blocks all paths to marked states. In agent terms:

```text
marked state = task completion / valid final answer / safe handoff
```

Strict-block can be safe but blocking:

```text
unsafe field exists
strict-block suppresses whole action
answer body and citations are also lost
task completion may become unreachable
```

Field repair can be safe and less blocking:

```text
unsafe side_effect blocked
answer body and citations preserved
task can still complete as an informational answer
```

This suggests a new metric:

```text
safe_completion_reachability =
  # states from which a safe completion remains reachable after guard
  / # states where a safe completion was reachable before guard
```

For short traces, this can be approximated by:

```text
legal_trace_completion_rate
```

For longer traces, it can be measured with a small trace automaton.

## 5. Quantitative Nonblocking

Zhang et al. define quantitative nonblocking in terms of bounded distance to marker states. This gives an even better metric for complex agent tasks.

AFW analogue:

```text
completion_distance_G(t) =
  minimum number of additional safe steps to complete the task
  after guard G transforms trace prefix t
```

Then:

```text
quantitative_nonblocking_score(G) =
  average or max completion_distance_G(t)
```

A guard is less conservative if it keeps this distance low.

This can distinguish:

```text
strict-block:
  safe but may increase completion distance sharply

CapGuard review-route:
  safe but may insert human-review steps

CapGuard field-repair:
  safe and may keep task completion distance small
```

## 6. Runtime Assurance and Simplex Architecture

Runtime assurance (RTA) / Simplex architectures let an unverified high-performance controller operate until it risks violating a safety property, then switch to a trusted backup controller.

Agent mapping:

```text
advanced controller:
  nominal LLM agent

monitor:
  CapGuard / temporal monitor / probabilistic risk monitor

backup controller:
  human approval, safe template, restricted tool mode, no-side-effect answer
```

Key sources:

- Hobbs et al., "Runtime Assurance for Safety-Critical Systems". <https://coogan.ece.gatech.edu/papers/pdf/hobbs2022csm.pdf>
- NASA formal verification framework for runtime assurance. <https://shemesh.larc.nasa.gov/fm/papers/NFM2024-draft.pdf>
- Mehmood et al., "The Black-Box Simplex Architecture for Runtime Assurance of Autonomous CPS". <https://arxiv.org/pdf/2102.12981>
- Optimal RTA via RL, noting that existing RTA can be overly conservative. <https://arxiv.org/abs/2310.04288>

The AFW twist:

```text
Instead of switching the whole agent to a backup controller,
switch only the unauthorized field to a backup behavior.
```

Call this:

```text
Fieldwise Simplex
```

Example:

```text
answer.body          -> nominal LLM preserved
answer.citations     -> nominal LLM preserved
side_effect          -> backup review-route
risk_level           -> backup conservative default or review
```

This is likely more publishable than whole-action blocking because it directly attacks over-conservatism.

## 7. Minimum-Violation Planning

Minimum-violation planning handles cases where all rules cannot be satisfied simultaneously. It assigns priority/weight to specifications and computes the least-violating trajectory.

Key sources:

- Tumova et al., "Minimum-violation LTL Planning with Conflicting Specifications". <https://arxiv.org/abs/1303.3679>
- Wongpiromsarn et al., "Minimum-Violation Planning for Autonomous Systems". <https://arxiv.org/abs/2009.11954>

AFW mapping:

```text
hard constraints:
  no unauthorized side effect
  no approval waiver without authority
  no data write outside scope

soft constraints:
  preserve answer detail
  minimize review steps
  minimize latency
  preserve user-requested formatting
```

Then field repair becomes:

```text
choose a' minimizing weighted violation / edit cost
subject to hard authority constraints
```

This gives a more nuanced alternative to:

```text
allow / block everything
```

## 8. Assume-Guarantee Contracts and Interface Automata

Assume-guarantee contracts specify what a component assumes from its environment and guarantees in return.

This maps to capability manifests:

```text
skill manifest:
  assumption: input is supplied report text
  guarantee: output is formatting-only

tool metadata:
  assumption: arguments fit schema
  guarantee: returns observation, not approval

approval source:
  assumption: effect_scope matches requested effect
  guarantee: approval_for_exact_effect
```

Key sources:

- de Alfaro and Henzinger, "Interface Automata". <https://luca.dealfaro.com/papers/01/FSE01.pdf>
- Contract-based assume-guarantee reasoning with scheduled components. <https://loonwerks.com/publications/liu2022nfm.html>
- Pacti assume-guarantee contracts. <https://dl.acm.org/doi/10.1145/3704736>

AFW insight:

```text
Cap(x) is a contract guarantee.
Need(s,f) is a field-side assumption/requirement.
Coverage is contract compatibility.
No role amplification is contract refinement safety.
```

This can help formalize manifest-lifted capability:

```text
skill manifest -> source contract -> Cap(x)
field need -> consumer contract -> Need(s,f)
Cap covers Need iff contracts are compatible
```

## 9. Current Agent-Safety Neighbor Pressure

This round also found several direct 2025-2026 neighbors:

```text
ProbGuard / Pro2Guard
AgentSpec
Symbolic guardrails
```

ProbGuard models LLM agent traces as a DTMC and intervenes before predicted unsafe states. AgentSpec and symbolic guardrail work pressure any broad claim about customizable runtime policy enforcement or trigger-check-enforce frameworks.

Source:

- Wang et al., "ProbGuard: Probabilistic Runtime Monitoring for LLM Agent Safety". <https://arxiv.org/abs/2508.00500>
- "AgentSpec: Customizable Runtime Enforcement for Safe and Reliable LLM Agents". <https://arxiv.org/abs/2503.18666>
- "Symbolic Guardrails for Domain-Specific Agents". <https://arxiv.org/abs/2604.15579>

Pressure on us:

```text
Do not claim first proactive runtime monitor for LLM agents.
Do not claim first probabilistic model-checking guard.
Do not claim first symbolic guardrail, runtime policy DSL, or trigger-check-enforce framework.
```

Safe delta:

```text
ProbGuard decides when future risk is high.
AgentSpec/symbolic guardrails define general policy enforcement mechanisms.
AFW decides which concrete action fields have authority witnesses
and should therefore be preserved or repaired.
```

Potential combination:

```text
ProbGuard chooses when to activate stronger supervision.
AFW decides the minimal field-level intervention once supervision is active.
```

## 10. Updated Direction Ranking

| Rank | Direction | What changes after this deep dive | Verdict |
|---:|---|---|---|
| 1 | Fieldwise maximally permissive CapGuard | Stronger than previous "transparency"; directly backed by supervisory control | Best main theory angle |
| 2 | Fieldwise Simplex / RTA for agents | Strong practical architecture: switch only unsafe fields to backup | Best system angle |
| 3 | Quantitative nonblocking metric | Measures whether guard keeps safe completion reachable | Best evaluation angle |
| 4 | Minimum-violation field repair | Converts repair into weighted optimization | Best extension angle |
| 5 | Contract-lifted capability manifests | Gives manifest inference a formal contract semantics | Best formalization appendix |
| 6 | Probabilistic supervisor + AFW | Hybrid with ProbGuard-like future-risk monitor | Future work / neighbor-aware extension |

## 11. Proposed New Paper Thesis

Old thesis:

```text
CapGuard checks whether each action field has authority.
```

Stronger thesis:

```text
CapGuard is a fieldwise supervisor for LLM agents:
it enforces authority safety while preserving every field that has a valid authority witness.
```

Even stronger but still safe:

```text
Under independent field effects and explicit source-to-field consumptions,
CapGuard is the locally maximally permissive supervisor for authority safety:
it suppresses exactly the unauthorized fields and no authorized fields.
```

## 12. Theorem Sketch

Assume:

1. Each protected field can be executed or suppressed independently.
2. `ValidAuthority(s,f)` is decidable from `Cap(x)` and `Need(s,f)`.
3. Suppressing an unauthorized field does not invalidate the authority of other fields.
4. No counter-authority applies to the authorized field.

Define CapGuard:

```text
S_CG(s,f) =
  allow if ValidAuthority(s,f)
  suppress_or_review otherwise
```

Then:

```text
Theorem A: Authority safety.
Every executed protected field is authorized.

Theorem B: Fieldwise transparency.
Every authorized protected field is preserved.

Theorem C: Local maximal permissiveness.
No other authority-safe field supervisor can allow a strict superset
of fields at step s.
```

Proof idea:

```text
The safety theorem follows because CapGuard only executes fields satisfying ValidAuthority.
Transparency follows by construction: authorized fields are not rewritten.
Maximal permissiveness follows because every unauthorized field would violate safety if executed,
and every authorized field is already allowed by CapGuard.
```

This theorem is narrow but clean. It does not claim global optimality over arbitrary multi-step agents.

## 13. Immediate Next Work

1. Add `fieldwise_maximal_permissiveness` to the experiment seed.
2. Add `nonblocking_completion_distance` for multi-step traces.
3. Design `fieldwise_simplex` output mode:
   - preserve safe informational fields;
   - replace unsafe side-effect/risk/delegation fields with review-route fields.
4. Compare:
   - strict-block;
   - whole-action review-route;
   - fieldwise-simplex repair.
5. Keep ProbGuard / AgentSpec / SafeHarbor / TRIAD as close neighbors in the claim firewall.
