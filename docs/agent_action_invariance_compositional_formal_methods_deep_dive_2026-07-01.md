# Agent Action Invariance: Compositional Formal Methods Deep Dive

Date: 2026-07-01

Purpose: connect AFW / CapGuard to compositional verification, contract-based
design, interface automata, temporal logic, trace refinement, and
hyperproperties.

The working question is:

```text
If every local agent component looks safe, is the composed multi-step agent
still safe, non-amplifying, and action-invariant?
```

This is the missing bridge from single-field checking to complex agent
execution:

```text
RAG -> skill -> memory -> tool -> approval -> final action
```

Each step may have a valid-looking local interface. The failure can appear only
after composition:

```text
formatting skill output + old memory + prior approval
  accidentally becomes publish authority
```

## 1. Core Thesis

The strongest compositional framing for AFW is:

> Agent components should compose without authority amplification.

In AFW terms:

```text
For every composed source y = Compose(x1, ..., xn),
Cap(y) must be no stronger than the declared composition of Cap(x1), ..., Cap(xn).
```

Then action invariance becomes a compositional property:

```text
If each component preserves valid authority boundaries,
and every composition rule is non-amplifying,
then CapGuard preserves every field whose composed witness covers Need(s,f)
and blocks/repairs fields whose composed witness does not.
```

Plain version:

```text
多个安全小步骤串起来，不能凭空变出一个更大的权限。
```

## 2. Assume-Guarantee Reasoning

Assume-guarantee reasoning proves a system by proving each component under
assumptions about its environment.

AFW mapping:

```text
Component C_i assumes:
  its inputs carry only declared Cap(x)

Component C_i guarantees:
  its outputs carry only derived/attenuated Cap(y)
  and it emits declared Consume(y -> f) edges
```

For a component:

```text
Assume_i:
  forall input source x: VerifiedCap(x) is accurate

Guarantee_i:
  forall output source y:
    Cap(y) <= Derive_i(Cap(inputs))
    no new semantic role is introduced unless explicitly authorized
```

Compositional theorem sketch:

```text
If every component's guarantee satisfies the next component's assumption,
and every derivation rule is non-amplifying,
then the composed pipeline is non-amplifying.
```

Candidate metric:

```text
assumption_discharge_rate =
  # component assumptions discharged by upstream guarantees
  / # component assumptions
```

Closest sources:

- McMillan, "A Compositional Rule for Hardware Design Refinement", CAV 1997.
  <https://link.springer.com/chapter/10.1007/3-540-63166-6_33>
- Alur and Henzinger, "Reactive Modules", Formal Methods in System Design.
  <https://link.springer.com/article/10.1023/A:1018719929481>

Safe use in AFW:

```text
Do not claim new assume-guarantee reasoning.
Use assume-guarantee contracts to state what each agent component may emit as
authority.
```

## 3. Contract-Based Design

Contract-based design packages component behavior as:

```text
assumptions A
guarantees G
```

AFW can make each source-producing component export an authority contract:

```text
Contract(skill_format_report):
  Assumes:
    input has report_body_authority
  Guarantees:
    output has report_formatting_authority
    output does not have risk_assessment_authority
    output does not have publish_approval_authority
```

Then `Cap(x)` is not just inferred from text. It is constrained by the producing
component's contract.

Candidate property:

```text
Authority Contract Refinement:
  Component C' refines component C if every authority capability C' may emit is
  covered by or weaker than C's declared guarantee under the same assumptions.
```

This matters for skill updates:

```text
new skill version is acceptable only if it refines or explicitly renegotiates
the old authority contract.
```

Candidate metrics:

```text
contract_refinement_pass_rate =
  # component updates whose authority contract refines previous version
  / # component updates

contract_violation_detection_rate =
  # authority outputs violating component contract detected
  / # injected contract-violation cases
```

Closest sources:

- Benveniste et al., "Contracts for Systems Design", Foundations and Trends in
  Electronic Design Automation, 2018.
  <https://www.nowpublishers.com/article/Details/EDA-016>
- Pacti: assume-guarantee contracts for system design.
  <https://dl.acm.org/doi/10.1145/3704736>

Safe use in AFW:

```text
Contract-based design is not new. AFW uses authority contracts to keep
source-producing agent components from emitting stronger capabilities than
their interface promises.
```

## 4. Interface Automata

Interface automata model legal component interactions:

```text
inputs
outputs
illegal interaction states
```

AFW mapping:

```text
component input:
  source with Cap(x)

component output:
  derived source y with Cap(y)

illegal interaction:
  component emits or consumes authority outside its declared interface
```

Example:

```text
report-formatting skill interface:
  input: draft report
  output: formatted report
  illegal: external publish approval
```

This is useful because an agent component can be "safe" only under a compatible
environment:

```text
The skill is safe when consumed as formatting output.
The same skill output is unsafe when consumed as risk authority.
```

Candidate metric:

```text
interface_compatibility_rate =
  # source-to-component consumptions satisfying declared authority interfaces
  / # source-to-component consumptions
```

Closest source:

- de Alfaro and Henzinger, "Interface Automata", ESEC/FSE 2001.
  <https://dl.acm.org/doi/10.1145/503209.503226>

Safe use in AFW:

```text
Use interface automata to explain compatible authority consumption, not as a new
automata theory contribution.
```

## 5. Temporal Logic And TLA+

Temporal logic lets us state trace properties:

```text
always:
  no protected field executes without valid authority

eventually:
  every review-routed field is either approved, rejected, or expired

until:
  a field requiring an obligation cannot execute until the obligation is
  discharged
```

TLA+ is useful for modeling multi-step agent workflows:

```text
state variables:
  sources
  capabilities
  consumptions
  policy_epoch
  obligations
  pending_reviews
  action_fields

next relation:
  retrieve / call_skill / update_memory / request_approval / propose_action /
  guard / execute / revoke / repair
```

Candidate temporal properties:

```text
[] (Exec(s,f) => ValidAuthority(s,f))

[] (ValidAuthority(s,f) /\ NoCounterAuthority(s,f) /\ GuardRuns(s)
    => Preserved(s,f))

[] (ObligationRequired(s,f,o) /\ ~Discharged(o)
    => ~Exec(s,f))

[] (Revoked(x) /\ Consumes(s,f,x)
    => ~Exec(s,f))

[] (ReviewRoute(s,f) => <> (Approved(s,f) \/ Rejected(s,f) \/ Expired(s,f)))
```

Candidate metric:

```text
temporal_property_coverage =
  # modeled AFW temporal properties with at least one positive and negative test
  / # modeled AFW temporal properties
```

Closest sources:

- Lamport, "Specifying Systems: The TLA+ Language and Tools for Hardware and
  Software Engineers". <https://lamport.azurewebsites.net/tla/book.html>
- Lamport, "The Temporal Logic of Actions", ACM TOPLAS 1994.
  <https://dl.acm.org/doi/10.1145/177492.177726>

Safe use in AFW:

```text
Do not claim first TLA+ model of agents.
Use temporal logic as the precise property language for multi-step authority
lifecycle and action invariance.
```

## 6. Alloy And Lightweight Relational Modeling

Alloy is useful when the object is a relation:

```text
Source x has Cap c
Field f requires Need n
Source x consumed by field f
Capability c covers need n
```

AFW is heavily relational, so Alloy-style modeling is a natural fit:

```text
sig Source {}
sig Field {}
sig Role {}
sig Cap { roles: set Role }
sig Need { required: set Role }
sig Consume { src: Source, field: Field }

fact NoRoleAmplification {
  all y: Source |
    roles(y) in declaredDerivedRoles(y)
}
```

Possible use:

1. Generate small counterexamples where composition creates authority.
2. Check whether a witness is minimal.
3. Search for source-family combinations that break no-amplification.
4. Generate benchmark rows from counterexamples.

Candidate metric:

```text
relational_counterexample_yield =
  # useful AFW benchmark rows generated from relational counterexamples
  / # generated counterexamples
```

Closest source:

- Jackson, "Software Abstractions: Logic, Language, and Analysis".
  <https://mitpress.mit.edu/9780262528907/software-abstractions/>
- Alloy Analyzer project. <https://alloytools.org/>

Safe use in AFW:

```text
Do not claim new relational modeling.
Use Alloy-style counterexamples to generate authority-laundering test cases.
```

## 7. Hyperproperties And HyperLTL

Some security properties relate multiple traces, not one trace.

AFW already has paired-trace ideas:

```text
legal trace:
  same source used within its authority

laundered trace:
  same source used outside its authority
```

Action invariance is also hyperproperty-shaped:

```text
If two traces differ only in a source that lacks authority for field f,
then the guarded value/execution status of f should be the same.
```

Candidate property:

```text
Authority Noninterference As A Hyperproperty:
  For traces tau1 and tau2, if tau1 and tau2 are identical on all sources
  authorized for field f, then guarded field f is identical in tau1 and tau2.
```

This is stronger than normal attribution:

```text
Attribution says which source influenced f.
Hyperproperty says unauthorized source changes must not change guarded f.
```

Candidate metrics:

```text
hyper_authority_noninterference_pass_rate =
  # paired traces where unauthorized-source perturbation leaves guarded field unchanged
  / # paired traces

same_source_contrast_coverage =
  # source families with legal-vs-laundered paired traces
  / # source families
```

Closest sources:

- Clarkson and Schneider, "Hyperproperties", Journal of Computer Security,
  2010. <https://doi.org/10.3233/JCS-2009-0393>
- Clarkson et al., "Temporal Logics for Hyperproperties", POST 2014.
  <https://link.springer.com/chapter/10.1007/978-3-642-54792-8_15>

Safe use in AFW:

```text
Do not claim first hyperproperty model.
Use hyperproperties to state same-source legal-vs-laundered contrast and
authority noninterference.
```

## 8. Trace Refinement, Simulation, And Bisimulation

Refinement checks whether an implementation preserves a specification.

AFW mapping:

```text
untrusted nominal agent trace:
  tau

guarded trace:
  G(tau)

spec:
  authority-safe trace that preserves all authorized fields
```

Candidate relation:

```text
G(tau) refines tau with respect to authority:
  - unauthorized field executions may be removed, repaired, or routed
  - authorized field values must be preserved
  - new field authority cannot appear without a witness
```

This is not ordinary trace equivalence because unsafe events may be removed.
It is a selective refinement:

```text
equivalent on authorized fields
stricter on unauthorized fields
```

Candidate metric:

```text
authority_refinement_pass_rate =
  # guarded traces satisfying selective authority refinement
  / # guarded traces
```

Closest sources:

- CSP/FDR refinement checking. <https://cocotec.io/fdr/manual/>
- Lynch and Tuttle, "An Introduction to Input/Output Automata".
  <https://groups.csail.mit.edu/tds/papers/Lynch/jacm89.pdf>

Safe use in AFW:

```text
Use refinement as a property of guarded traces.
Do not claim a new process-algebra checker.
```

## 9. Rely-Guarantee And Concurrent Agent Components

Rely-guarantee reasoning is a classic method for concurrent programs:

```text
rely:
  what interference from the environment is allowed

guarantee:
  what interference this component may cause
```

Agent systems often have concurrent or interleaved components:

- planner;
- retriever;
- memory updater;
- skill executor;
- tool runner;
- approval requester;
- guard;
- observer.

AFW mapping:

```text
memory updater guarantee:
  does not create approval authority from conversational preference

tool runner guarantee:
  does not treat schema metadata as side-effect approval

skill executor guarantee:
  derived output roles are attenuated by manifest

guard rely:
  upstream components report source identity and declared capability
```

Candidate metric:

```text
interference_violation_detection_rate =
  # concurrent/interleaved traces where invalid authority interference is detected
  / # injected interference traces
```

Closest source:

- Jones, "Tentative Steps Toward a Development Method for Interfering
  Programs", ACM TOPLAS 1983.
  <https://dl.acm.org/doi/10.1145/357980.358001>

Safe use in AFW:

```text
Use rely-guarantee to reason about concurrent source mutation and policy epoch
changes, not as a new concurrency logic.
```

## 10. Separation Logic And Frame Conditions

Separation logic's frame idea is useful:

```text
if a command modifies only region R, the rest of the state is preserved
```

AFW analogue:

```text
If guard repairs only unauthorized field f_bad, then all authorized fields
outside f_bad's authority frame should be unchanged.
```

Candidate property:

```text
Authority Frame Preservation:
  A field repair may alter only fields in the invalid authority frame and
  required routing/audit fields; it must not alter unrelated authorized fields.
```

Candidate metric:

```text
frame_preservation_rate =
  # repairs that leave all out-of-frame authorized fields unchanged
  / # repairs
```

Closest source:

- Reynolds, "Separation Logic: A Logic for Shared Mutable Data Structures",
  LICS 2002. <https://dl.acm.org/doi/10.1109/LICS.2002.1029817>

Safe use in AFW:

```text
Use frame conditions to define precise field repair.
Do not claim separation logic for agents.
```

## 11. Best Research Directions From This Pass

### Direction A: Compositional Non-Amplification Contracts

Method:

1. Give every source-producing component an authority contract.
2. Define composition rules that can attenuate or combine roles but cannot
   create undeclared semantic roles.
3. Prove a local theorem: if component contracts compose, final action fields
   cannot gain authority absent from upstream contracts.

Why strong:

- Directly answers skill-driven and multi-tool agents.
- Fits our existing "composition must not create roles" story.
- Testable with synthetic and trace-derived authority-confusion rows.

Risk:

- Must distinguish from broad protocol-composition prior work.

Verdict:

```text
Very strong theory extension.
```

### Direction B: Hyperproperty Benchmark For Same-Source Legal/Laundered Contrast

Method:

1. Construct paired traces differing only by field `Need(s,f)` or source role.
2. Require guarded outputs to diverge only when authority differs.
3. Measure authority noninterference under unauthorized-source perturbations.

Why strong:

- Converts our paired-row intuition into a formal hyperproperty.
- Excellent reviewer explanation for "not all influence is bad."

Risk:

- HyperLTL formalism may be too heavy for main text.

Verdict:

```text
Good formal appendix and benchmark-generation principle.
```

### Direction C: Alloy-Generated Authority Counterexamples

Method:

1. Encode sources, roles, needs, derivations, and composition rules relationally.
2. Ask the solver for smallest cases violating no-amplification or minimality.
3. Convert counterexamples into benchmark rows.

Why strong:

- Gives systematic sample generation.
- Cheap to implement.
- Looks more rigorous than hand-written attack cases.

Risk:

- Need avoid spending the paper on the solver.

Verdict:

```text
Excellent benchmark generator / appendix artifact.
```

### Direction D: TLA+ Authority Lifecycle Spec

Method:

1. Model retrieval, skill calls, memory update, approval, guard, execution,
   revocation, and repair as state transitions.
2. State safety, transparency, obligation, and liveness properties.
3. Use counterexamples to refine runtime rows.

Why strong:

- Good for multi-step workflows.
- Captures temporal decay and review liveness cleanly.

Risk:

- Existing TraceFix / AgentVerify style work already pressures this.

Verdict:

```text
Useful validation artifact, not core novelty.
```

### Direction E: Authority Frame Repair

Method:

1. Define an authority frame for each invalid field.
2. Fieldwise repair is allowed to change only fields in the invalid frame plus
   explicit audit/review fields.
3. Measure frame preservation.

Why strong:

- Directly addresses over-conservative guard behavior.
- Ties to minimal intervention in a precise way.

Risk:

- Needs careful semantics for coupled fields.

Verdict:

```text
Strong system metric and repair theorem.
```

## 12. Ranking

| Rank | Direction | Novelty fit | Implementation cost | Main use |
|---:|---|---:|---:|---|
| 1 | Compositional non-amplification contracts | high | medium | formal core |
| 2 | Authority frame repair | high | medium | action-invariance repair |
| 3 | Hyperproperty benchmark | medium-high | low-medium | formal evaluation |
| 4 | Alloy-generated counterexamples | medium-high | medium | benchmark generation |
| 5 | TLA+ authority lifecycle spec | medium | medium-high | validation appendix |

## 13. Claim Firewall

Do not claim:

- first assume-guarantee reasoning for agents;
- first contract-based design for agents;
- first interface-automata model of tools or skills;
- first TLA+, Alloy, LTL, HyperLTL, or model-checking framework for agents;
- first trace-refinement, process-algebra, or I/O automata model for agents;
- first rely-guarantee or separation-logic treatment of agent systems;
- first formal verification of agent skills or protocol-composition invariants;
- fully verified production agent behavior unless a complete model and proof
  artifact exists.

Safe claim:

> AFW uses compositional formal methods to state a narrow authority invariant:
> component composition may attenuate, preserve, or explicitly combine declared
> capabilities, but it must not create a semantic role absent from upstream
> contracts. CapGuard then enforces action-field invariance over the resulting
> composed witnesses.

## 14. Plain Version

This direction says:

```text
单个 skill、memory、tool 看起来都没问题，不代表串起来以后没问题。

我们要防的是：
  A 只会格式化，
  B 只会总结，
  C 只是旧审批，
  但 agent 把 A+B+C 合起来当成了“可以发布/可以执行/可以免审”。

组合形式化方法给我们的抓手是：
  每个组件说清楚自己假设什么、保证什么；
  组件输出的权限不能比输入和合同更大；
  guard 修复一个坏字段时，不能误改其他好字段。
```

Best short name:

```text
Compositional Authority Non-Amplification
```

