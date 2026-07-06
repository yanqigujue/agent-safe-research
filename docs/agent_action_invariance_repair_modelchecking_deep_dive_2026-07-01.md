# Agent Action Invariance: Repair, Revision, and Model-Checking Deep Dive

Date: 2026-07-01

This note continues the theory search for AFW / CapGuard. The previous notes found:

- runtime enforcement: soundness + transparency;
- supervisory control: safety + nonblocking + maximal permissiveness;
- runtime assurance: switching to a trusted backup;
- policy logic: allow/block/abstain, obligations, and conflicts.

This round focuses on another question:

> If an agent action is unsafe, what is the principled minimal way to repair it while preserving legitimate behavior?

The strongest new bridges are:

```text
belief revision:
  minimal change under new information

formal repair:
  minimal patch satisfying tests/specifications

model checking:
  counterexample-guided repair of traces/specs

process algebra/session types:
  interaction-preserving repair for multi-agent protocols

gradual typing/blame:
  dynamic checks with accountable boundary failures
```

## 1. Belief Revision: Minimal Change As A Normative Principle

Belief revision asks how a knowledge base should change when new information arrives while preserving consistency.

The core principle that matters for AFW is:

```text
minimal change:
  preserve as much of the old belief state as possible while incorporating the new constraint
```

Useful sources:

- Stanford Encyclopedia of Philosophy, "Logic of Belief Revision". <https://plato.stanford.edu/entries/logic-belief-revision/>
- Huber, "Belief Revision I: The AGM Theory". <https://huber.artsci.utoronto.ca/wp-content/uploads/2013/07/Belief-Revision-I-The-AGM-Theory.pdf>
- Boutilier, "Iterated Revision and Minimal Change of Conditional Beliefs". <https://www.cs.toronto.edu/~cebly/Papers/jpl95.pdf>
- SEP / standard AGM background distinguishes expansion, contraction, revision, and update.

AFW mapping:

```text
current action proposal:
  a = {answer, citations, risk_level, side_effect, delegation, ...}

new safety information:
  field f lacks ValidAuthority

repair objective:
  revise a into a' so that authority safety holds,
  while preserving every field not implicated by the violation
```

Belief revision view:

```text
unsafe action repair = action-state revision under authority constraints
```

This is useful because it gives a mature reason for "minimal field edit":

> The guard should not erase the entire action when the inconsistency is localized to one field.

## 2. Belief Update vs Belief Revision

Belief revision and belief update are different:

```text
revision:
  new information corrects or conflicts with current beliefs about the same world

update:
  the world has changed, so the belief state must track a changed environment
```

AFW can use this distinction:

```text
revision case:
  discover that a field lacks authority
  -> repair the proposed action

update case:
  policy epoch changes, approval expires, counter-authority arrives
  -> update available Cap(x) before checking action fields
```

This helps temporal authority decay:

```text
Q3 approval reused for Q4 is not only missing a role;
the authority world has changed, so the capability state must be updated.
```

Paper use:

```text
Use belief revision/update as a theory lens for temporal decay and minimal action repair.
Do not claim a new belief-revision theory.
```

## 3. Formal Repair And Automated Program Repair

Automated program repair (APR) often frames repair as:

```text
find a minimal change to the program so that tests or formal specifications pass
```

Useful sources:

- Le Goues, Pradel, Roychoudhury, "Automated Program Repair". <https://cacm.acm.org/research/automated-program-repair/>
- CACM PDF version. <https://abhikrc.com/pdf/cacm19.pdf>
- "Automated Program Repair: Emerging trends pose and expose problems for benchmarks". <https://arxiv.org/abs/2405.05455>
- Syntax-guided repair for HyperLTL, which explicitly discusses transparent repairs. <https://link.springer.com/chapter/10.1007/978-3-031-65633-0_1>
- Runtime-safety-guided policy repair, phrased as minimally deviating policy repair. <https://eskang.github.io/assets/papers/rv20a.pdf>

AFW mapping:

```text
program:
  structured agent action or trace

specification:
  authority safety + task-preservation constraints

patch:
  field replacement / field deletion / review-route insertion

minimality:
  weighted field edit distance
```

Formal repair gives the right language for `fieldwise-simplex`:

```text
repair(a) =
  argmin_a' edit_cost(a', a)
  subject to authority_safe(a')
```

The key AFW claim:

> CapGuard whole-action review is a safe repair; fieldwise-simplex is a lower-edit repair when unsafe fields are localized.

## 4. Model Checking And Counterexample-Guided Repair

Model checking verifies a finite-state model against a formal property and returns counterexamples when the property fails.

Recent agent-specific work is close:

- AgentVerify uses LTL model checking for agent safety. <https://www.preprints.org/manuscript/202604.1029>
- TraceFix uses TLA+ counterexamples to repair LLM multi-agent coordination protocols. <https://arxiv.org/abs/2605.07935>
- PAT-Agent uses model checker feedback to repair formal models. <https://arxiv.org/abs/2509.23675>
- AgentGuard builds an MDP-style runtime verification layer. <https://arxiv.org/abs/2509.23864>
- ProbGuard performs proactive probabilistic runtime monitoring. <https://arxiv.org/abs/2508.00500>
- C-Trace checks compliance predicates over agent execution traces. <https://arxiv.org/abs/2606.19242>

Pressure on us:

```text
Do not claim first formal verification, model checking, runtime verification,
counterexample-guided repair, or TLA+ workflow for agents.
```

Safe delta:

```text
Model checking finds a bad trace or bad protocol.
AFW identifies the exact action field whose consumed authority is invalid,
then repairs only that field when possible.
```

AFW can use counterexamples as input:

```text
model checker counterexample:
  trace violates "no unauthorized side effect"

AFW localization:
  side_effect field consumed x where Cap(x) does not cover Need(s, side_effect)

field repair:
  replace side_effect with review-route while preserving answer/citations
```

This gives a clean future integration:

```text
counterexample-guided field repair
```

## 5. Runtime Model Checking vs Field Authority Checking

Runtime verification often abstracts raw I/O into formal events and verifies temporal properties:

```text
G(no_secret_exfiltration)
G(tool_call -> prior_approval)
F(task_complete)
```

AFW's property is more local:

```text
for each protected field f:
  Execute(f) -> ValidAuthority(s,f)
```

The two are complementary:

```text
runtime model checking:
  detects temporal/global property violations

AFW:
  provides field-level cause and repair target
```

Possible hybrid:

```text
LTL monitor detects violation pattern
AFW witness explains which field/source failed
fieldwise-simplex repairs the action
```

## 6. Process Algebra And Refinement

Process algebra models interacting systems as processes and communications. It is mature in security-protocol verification.

Useful sources:

- CyBOK Formal Methods for Security knowledge area. <https://www.cybok.org/wp-content/uploads/Formal_Methods_for_Security_v1.0.0.pdf>
- Blanchet et al., "Modeling and Verifying Security Protocols with the Applied Pi Calculus and ProVerif". <https://bblanche.gitlabpages.inria.fr/publications/BlanchetFnTPS16.pdf>
- Ryan and Smyth, "Applied pi calculus" tutorial. <https://markryan.eu/research/papers/pdf/11-applied-pi.extended.pdf>
- FDR3 / CSP refinement checking. <https://www.cs.ox.ac.uk/files/6001/Document.pdf>
- Process Algebra and Model Checking. <https://link.springer.com/chapter/10.1007/978-3-319-10575-8_32>

AFW mapping:

```text
Agent = process
Tool = process
Skill = process
Memory = process
UserApproval = process
CapGuard = supervisor / mediator process

Events:
  propose(field)
  consume(source, field)
  allow(field)
  block(field)
  route_review(field)
  execute(field)
```

Refinement view:

```text
GuardedAgent refines SafeAgentSpec
```

Behavior preservation view:

```text
For authorized-field events, GuardedAgent should be trace-equivalent
to NominalAgent.
```

Why useful:

- Gives a compositional way to model skill/tool/memory/user-approval as separate communicating processes.
- Refinement can express that guarded behavior is a safe subset of nominal behavior.
- Trace equivalence/bisimulation can express preservation of authorized events.

Risk:

```text
Process algebra may be too heavy for the main paper.
Use it as appendix/formalization option, not headline novelty.
```

## 7. Session Types, Linearity, And Delegation

Session types specify structured communication protocols, often with linearity: resources/channels are used in disciplined ways.

Useful sources:

- Gradual Session Types. <https://arxiv.org/abs/1809.05649>
- Session types and linear logic background. <https://homepages.inf.ed.ac.uk/wadler/topics/linear-logic.html>
- Session types for access and information flow control. <https://www-sop.inria.fr/indes/MATYSS/Documents_files/concur10-final.pdf>

AFW mapping:

```text
delegation field:
  can be treated as passing an authority channel

no role amplification:
  linear/capability discipline prevents duplicating or upgrading the channel

obligation carrying:
  obligations are protocol obligations that travel with the channel
```

This is especially relevant for:

```text
delegation_scope
prior-step output authority
skill-to-agent authority passing
tool/MCP handoff
```

Potential future angle:

```text
Authority sessions:
  a lightweight session-type discipline for authority-bearing agent interactions
```

But current recommendation:

```text
Keep session types as a future direction, not main contribution.
```

## 8. Gradual Typing And Blame

Gradual typing mixes statically typed and dynamically checked components. When a dynamic check fails, blame identifies which boundary is responsible.

Useful sources:

- Gradual Information Flow Typing. <https://users.soe.ucsc.edu/~cormac/papers/stop11.pdf>
- Gradual session types. <https://arxiv.org/abs/1809.05649>
- Blame tracking in gradual types. <https://www2.ccs.neu.edu/racket/pubs/icfp21-lgfd.pdf>

AFW mapping:

```text
static authority:
  manifest-lifted Cap(x) known before execution

dynamic authority:
  source-to-field consumption extracted from runtime traces

dynamic check:
  Cap(x) covers Need(s,f)?

blame:
  the source/field pair responsible for failed coverage
```

This strengthens the witness story:

```text
minimal witness explains success
missing-role witness assigns blame for failure
```

Possible metric:

```text
blame_localization_accuracy =
  # cases where AFW identifies the expected missing source/role
  / # unsafe cases
```

This could be useful for reviewer objections that AFW is just a blocker:

> It also localizes the authority boundary that failed.

## 9. New Candidate Directions

### Direction A: Minimal Authority Revision

View guarded action repair as AGM-style minimal revision:

```text
input:
  proposed action a
  authority constraints K

output:
  revised action a'
  such that K holds and distance(a,a') is minimized
```

Novelty fit:

```text
medium-high as a theory lens;
high if implemented as fieldwise-simplex repair with metrics.
```

### Direction B: Counterexample-Guided Field Repair

Use model-checker counterexamples to locate unsafe traces, then use AFW witnesses to repair the minimal fields.

```text
TLA+/LTL counterexample -> AFW field blame -> fieldwise repair
```

Novelty fit:

```text
medium;
close neighbors TraceFix and AgentVerify are strong,
but field-level authority repair remains different.
```

### Direction C: Authority Process Algebra

Model agent components as processes and prove guarded-agent refinement:

```text
GuardedAgent <= SafeAgentSpec
and
AuthorizedProjection(GuardedAgent) ~= AuthorizedProjection(NominalAgent)
```

Novelty fit:

```text
medium;
very formal, possibly too heavy for the current paper.
```

### Direction D: Blame-Carrying Authority Checks

Extend minimal witnesses so failures produce blame:

```text
missing role
missing operation
expired time_scope
unsatisfied obligation
counter-authority conflict
```

Novelty fit:

```text
high practical value;
small implementation delta from current witness output.
```

## 10. Updated Ranking

| Rank | Direction | Why |
|---:|---|---|
| 1 | Fieldwise maximally permissive CapGuard | Still the main theory angle. |
| 2 | Fieldwise-simplex / minimal authority repair | Strengthened by belief revision and formal repair. |
| 3 | Blame-carrying authority witnesses | Natural extension of minimal witness; useful for audits. |
| 4 | Counterexample-guided field repair | Good bridge to TLA+/LTL tools but close prior work exists. |
| 5 | Nonblocking completion distance | Still strong evaluation angle. |
| 6 | Authority process algebra/session types | Deep but likely appendix/future work. |

## 11. Claim Firewall Additions

Do not claim:

- first belief-revision or minimal-change repair theory;
- first automated program repair / formal repair method;
- first model-checking or runtime-verification framework for agents;
- first TLA+ / LTL / PAT repair loop for LLM systems;
- first process algebra / session-type model for security protocols;
- first gradual typing / blame-tracking mechanism.

Safe claim:

> AFW borrows minimal-change and repair principles to define fieldwise action repair: preserve authority-witnessed fields and revise only fields that lack valid authority or carry unresolved conflict.

## 12. How This Changes The Paper Kernel

Add one sentence to the paper:

> We view guarded action repair as a minimal-change revision problem over structured action fields, where authority witnesses determine which fields are protected from repair.

Add one metric:

```text
blame_localization_accuracy
```

Add one future-work bridge:

```text
counterexample-guided field repair:
  temporal monitor finds bad trace,
  AFW localizes invalid authority consumption,
  fieldwise-simplex repairs only implicated fields.
```

