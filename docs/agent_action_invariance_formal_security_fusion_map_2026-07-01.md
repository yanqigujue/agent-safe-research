# Agent Action Invariance: Formal Security Fusion Map

Date: 2026-07-01

Purpose:

This note asks which traditional attack-defense theories, mathematical
models, and formal-methods tools can be fused into AFW / CapGuard without
turning the paper into a generic formal-methods survey.

The target problem remains:

```text
Under strict policy supervision, preserve authorized agent behavior
while blocking, repairing, or routing unauthorized behavior.
```

Current AFW objects:

```text
Cap(x)       source capability lifted from evidence / skill / tool metadata /
             memory / approval / prior output

Need(s,f)    authority requirement of action field f at step s

Consume(x,s,f)
             source x is used to justify field f

ValidAuthority(s,f)
             consumed capabilities cover the field need

Witness(s,f)
             minimal capability subset proving ValidAuthority(s,f)
```

## 1. Ranking: Which Theory Is Most Useful?

| Rank | Theory family | Best use in AFW | Main risk |
|---:|---|---|---|
| 1 | Information-flow control and robust declassification | formalize authority flow from sources to action fields | theory overhead if we overclaim noninterference |
| 2 | Abstract interpretation / static analysis | explain CapGuard as a sound, imprecise-but-cheap abstract interpreter over traces | needs a precise abstraction relation |
| 3 | Capability security / confused deputy / effect types | strengthen the "wrong source role" story and skill-driven-agent setting | old theory; do not claim capability novelty |
| 4 | Protocol verification: Dolev-Yao, ProVerif, Tamarin | model multi-agent/tool/skill delegation as an authority protocol | heavy tooling; likely appendix/future work |
| 5 | Attack-defense trees / attack graphs | generate structured laundering and defense benchmark cases | weak as a main algorithmic novelty |
| 6 | Security games / MDP/POMDP cyber defense | choose guard intensity under cost, latency, and attacker adaptation | too broad for the current paper |
| 7 | Petri nets / colored Petri nets | model concurrent event traces and race conditions | useful for trace semantics, not core contribution |

Recommended main fusion:

```text
Information-flow control + abstract interpretation + capability security.
```

Recommended appendix / future-work fusion:

```text
Protocol verification + attack-defense trees + security games.
```

## 2. Information-Flow Control: Authority Flow, Not Just Data Flow

Classic information-flow control asks whether secret or untrusted data can
influence public outputs. AFW can adapt this to authority:

```text
data-flow question:
  may value v influence output y?

authority-flow question:
  may source x authorize action field f?
```

Mapping:

| IFC object | AFW object |
|---|---|
| security label | capability label: role, field, operation, scope, time, obligation |
| source variable | evidence / skill output / memory / approval / tool metadata |
| sink/output | protected action field |
| flow policy | `Cap(x) covers Need(s,f)` |
| declassification | deliberate use of a source to authorize a lower / external action |
| robust declassification | untrusted content cannot influence what authority is released |

Candidate property:

```text
Authority Noninterference

For any two traces T1 and T2 that differ only in sources whose capabilities
do not cover Need(s,f), the guarded value of field f is unchanged.
```

Plain meaning:

```text
If a document has no dispatch authority, changing that document should not
change whether the agent dispatches a work order.
```

Why this is strong:

- It turns prompt injection into an unauthorized influence problem.
- It explains why attribution alone is insufficient: a source may influence a
  field, but that influence is legal only through an allowed authority channel.
- It naturally supports memory, skill output, approval, and prior-step output,
  not just RAG documents.

Refinement for our paper:

```text
Robust Authority Declassification

A source may intentionally authorize an action field only if the decision to
release that authority is itself backed by high-integrity capability evidence.
```

Example:

```text
approval text may authorize publish_action
retrieved report text may be quoted in report_body
retrieved report text may not decide approval_status
```

This is a good theory layer for the paper, but we should not claim first
information-flow model or first declassification theory.

Useful sources:

- Sabelfeld and Myers, "Language-Based Information-Flow Security".
  <https://www.cs.cornell.edu/andru/papers/jsac/sm-jsac03.pdf>
- Zdancewic and Myers, "Robust Declassification".
  <https://www.cis.upenn.edu/~stevez/papers/Zda03.pdf>
- Myers and Liskov, "A Decentralized Model for Information Flow Control".
  <https://www.cs.cornell.edu/andru/papers/iflow-sosp97/paper.html>

## 3. Abstract Interpretation: CapGuard As A Trace Analyzer

Abstract interpretation studies sound approximation of program semantics.
That lens fits CapGuard surprisingly well.

Concrete semantics:

```text
Trace T =
  all retrieved documents,
  raw skill outputs,
  memory recalls,
  approval messages,
  tool metadata,
  intermediate action proposals,
  final tool calls / side effects
```

Abstract semantics:

```text
Abs(T) =
  capability facts,
  consumption edges,
  field needs,
  missing roles,
  conflict / counter-authority facts,
  discharged / undischarged obligations
```

CapGuard then runs over `Abs(T)`, not the whole natural-language trace.

Possible formal statement:

```text
alpha(T) = abstract authority state
gamma(A) = set of concrete traces represented by abstract state A

Soundness:
  if CapGuard(alpha(T)) allows field f,
  then every concrete trace represented by alpha(T) contains enough authority
  evidence for f under the AFW extraction contract.

Precision:
  false blocks arise when alpha forgets distinctions needed to prove authority.
```

This gives a clean answer to "will the guard hurt agent performance?":

```text
Performance loss is precision loss.
```

If the abstraction is too coarse, valid fields become `abstain` or `block`.
If the abstraction is precise enough, valid fields are preserved.

New metric:

```text
authority_abstraction_precision =
  # authorized fields with enough abstract evidence / # authorized fields
```

New experiment:

| Abstraction | Expected safety | Expected preservation | Cost |
|---|---:|---:|---:|
| text-only classifier | medium | unstable | high |
| source-family only | medium | low-medium | low |
| role + scope | high | medium-high | low |
| role + scope + time + obligation | high | high | medium |
| full witness graph | high | highest | medium-high |

Good paper sentence:

> CapGuard can be viewed as an abstract interpreter over agent traces: it
> discards most natural-language content and retains only authority-relevant
> capability, need, consumption, and obligation facts.

Useful sources:

- Cousot, "A Personal Historical Perspective on Abstract Interpretation".
  <https://cs.nyu.edu/~pcousot/publications.www/Cousot-FSP-2024.pdf>
- MIT Press, "Principles of Abstract Interpretation".
  <https://mitpress.ublish.com/book/principles-of-abstract-interpretation>
- Rival and Yi, "Static Analysis and Verification of Aerospace Software by
  Abstract Interpretation". <https://www.di.ens.fr/~rival/papers/fnt15.pdf>

## 4. Capability Security And Confused Deputy: The Cleanest Security Story

The confused-deputy problem is:

```text
A less-authorized party tricks a more-authorized deputy into using authority
that the requester did not possess.
```

This is almost exactly what semantic-role laundering does:

```text
retrieved document has report-formatting authority
agent has dispatch capability
document tricks agent into using dispatch field
```

AFW difference:

```text
The source must carry the capability for the field it governs.
Ambient agent ability is not enough.
```

Mapping:

| Capability-security object | AFW object |
|---|---|
| capability token | `Cap(x)` |
| designation + authority | source id + role/scope/effect labels |
| ambient authority | agent/tool has ability but source lacks field authority |
| confused deputy | wrong source governs a protected field |
| attenuation | capability loses role/scope/time/effect power |
| delegation | source passes limited authority to later source/action |

Best claim:

```text
AFW is a capability-style discipline for source-to-field authority consumption.
It prevents an agent from laundering ambient tool power through an
unauthorized source.
```

Possible extension:

```text
Linear / affine authority receipts

A high-risk approval capability can be:
  single-use,
  time-bounded,
  non-delegable,
  effect-bounded,
  obligation-carrying.
```

This gives a strong bridge to skill-driven agents:

```text
skill permission says what a skill may do directly;
AFW says what the skill output may later authorize.
```

Useful sources:

- Drossopoulou et al., "On Access Control, Capabilities, their Equivalence,
  and Confused Deputy Attacks". <https://people.mpi-sws.org/~dg/papers/csf16-caps.pdf>
- "Capability Myths Demolished". <https://classpages.cselabs.umn.edu/Fall-2021/csci5271/papers/SRL2003-02.pdf>
- Wadler / Findler blame resources. <https://homepages.inf.ed.ac.uk/wadler/topics/blame.html>

## 5. Protocol Verification: Agent Authority As A Security Protocol

Traditional protocol verification assumes an adversary controls the network.
For agents, a useful analogy is:

```text
Dolev-Yao attacker:
  can intercept, replay, synthesize, and reorder protocol messages

Prompt-injection attacker:
  can inject, replay, synthesize, and reorder natural-language instructions
  through retrieved content, memory, tool output, or prior steps
```

AFW protocol roles:

```text
User
Retriever
Skill
Tool
Memory
Approval source
Agent planner
CapGuard
Executor
```

Messages:

```text
source_event(capability_manifest)
candidate_action(field_values)
authority_use(source_id, field)
guard_decision(field, allow/block/abstain)
execution_event(tool/effect)
```

Security goals:

```text
No Forge:
  attacker-controlled content cannot create Cap(x) for roles it lacks.

No Role Amplification:
  combining two weak sources cannot create a role absent from both unless a
  declared composition rule exists.

No Unauthorized Execute:
  an execution event for field f implies a prior authority witness for f.

No Replay Across Epoch:
  stale approval from epoch t cannot authorize field f in epoch t+1.
```

This could be encoded in Tamarin-style trace properties or ProVerif-style
correspondence assertions.

Example correspondence:

```text
Exec(s,f,effect) ==> exists x. AuthorityUse(x,s,f) && Covers(Cap(x),Need(s,f))
```

Why not make this the main paper?

- Tooling overhead is high.
- Natural-language extraction still has to be trusted or bounded.
- It is an excellent appendix / future-work validator for the trace adapter.

Useful sources:

- Dolev-Yao model overview.
  <https://cseweb.ucsd.edu/classes/sp05/cse208/lec-dolevyao.html>
- Blanchet, "Modeling and Verifying Security Protocols with the Applied Pi
  Calculus and ProVerif".
  <https://bblanche.gitlabpages.inria.fr/publications/BlanchetFnTPS16.pdf>
- Tamarin Prover Manual.
  <https://tamarin-prover.com/manual/master/book/001_introduction.html>

## 6. Attack-Defense Trees And Attack Graphs: Benchmark Generator

Attack trees decompose a malicious objective into subgoals. Attack-defense
trees add countermeasures at arbitrary levels. For AFW, their strongest use is
not the core algorithm; it is systematic dataset construction.

AFW attack tree root:

```text
Unauthorized high-impact agent action executes
```

Example decomposition:

```text
execute unauthorized dispatch
  OR
    forge approval source
    replay stale approval
    launder formatting skill into dispatch authority
    exploit tool metadata as policy approval
    combine memory + retrieved document into fake composite authority
```

Defense nodes:

```text
manifest-lifted capability check
time-scope decay
obligation discharge check
counter-authority abstain
minimal witness audit
fieldwise-simplex repair
```

Quantitative attributes:

```text
attack_success_probability
defense_cost
false_block_cost
guard_latency_cost
audit_cost
```

Useful benchmark idea:

```text
ADTree-derived authority-confusion dataset

For each attack-tree leaf:
  generate legal row
  generate same-boundary role-laundered row
  generate stale/replay variant
  generate counter-authority variant
  generate partial-repair trace
```

This gives a principled answer to "where do test samples come from?"

Useful sources:

- NCSC, "Using attack trees to understand cyber security risk".
  <https://www.ncsc.gov.uk/collection/risk-management/using-attack-trees-to-understand-cyber-security-risk>
- Kordy, Mauw, Schweitzer, "Quantitative Questions on Attack-Defense Trees".
  <https://arxiv.org/abs/1210.8092>
- "Formal Methods for Attack Tree-based Security Modeling".
  <https://dl.acm.org/doi/fullHtml/10.1145/3331524>
- Jha, Sheyner, Wing, "Two Formal Analyses of Attack Graphs".
  <https://www.cs.cmu.edu/~scenariograph/jha-wing.pdf>

## 7. Security Games And MDPs: Guard Policy Selection

Security games and MDP/POMDP cyber-defense models are useful when the guard
must trade off:

```text
safety risk
false-block cost
latency cost
human-review cost
attacker adaptation
```

AFW mapping:

| Game / MDP object | AFW object |
|---|---|
| state | current trace authority state |
| defender action | allow, block, abstain, request evidence, route review, repair |
| attacker action | inject, replay, forge manifest, exploit memory, confuse skill role |
| reward / cost | safety loss, utility loss, latency, review burden |
| policy | guard intensity schedule |

Candidate direction:

```text
Cost-Bounded Field Supervision

Choose the cheapest guard decision that preserves authority soundness and
minimizes conservative collapse.
```

This is attractive, especially after Guardrail DoS, but it is a second paper
unless we keep it very small.

Minimal version for current paper:

```text
Measure guard_cost_bound_violation and conservative collapse.
Do not optimize a full security game yet.
```

Useful sources:

- Sinha et al., "Stackelberg Security Games: Looking Beyond a Decade of
  Success". <https://www.ijcai.org/proceedings/2018/0775.pdf>
- "Game-Theoretic Cybersecurity: the Good, the Bad and the Ugly".
  <https://arxiv.org/html/2401.13815v2>
- Zhou et al., "Markov Decision Process For Automatic Cyber Defense".
  <https://arxiv.org/abs/2207.05436>

## 8. Petri Nets: Concurrent Trace Semantics

Petri nets help model concurrent events:

```text
retrieval returns
memory recalls
skill emits output
approval changes epoch
tool metadata updates
planner proposes action
guard checks fields
executor runs side effect
```

Why this matters:

- Multi-agent systems may race: one subagent receives approval while another
  uses stale memory.
- Authority may decay while an action is being planned.
- Obligations may be discharged by one event and consumed by another.

AFW mapping:

| Petri-net object | AFW object |
|---|---|
| place | authority state / pending obligation / candidate action |
| token | source capability / obligation receipt / approval epoch |
| transition | retrieve, lift capability, consume, discharge, execute |
| reachability | can an unauthorized execution state be reached? |

Candidate property:

```text
No reachable marking contains Exec(f) without a covering authority token.
```

This is useful for future multi-agent / asynchronous traces, but too heavy for
the main paper right now.

Useful sources:

- "Detection and Modeling of Cyber Attacks with Petri Nets".
  <https://www.mdpi.com/1099-4300/16/12/6602>
- "A Survey of Practical Formal Methods for Security".
  <https://arxiv.org/pdf/2109.1362>

## 9. New Candidate Research Directions

### Direction A: Authority-Flow Control For Agent Actions

Method:

```text
Treat every source as carrying an authority label.
Treat every protected field as an authority sink.
Define authority noninterference and robust authority declassification.
Measure whether prompt-injected sources can influence fields they cannot
authorize.
```

Why it may publish:

- Strong theoretical bridge to information-flow security.
- Cleanly generalizes beyond RAG to skills, memory, approvals, and tools.
- Explains semantic-role laundering in a known formal vocabulary.

Minimum experiment:

```text
Generate source-pair traces where unauthorized source content changes.
Check whether guarded protected fields remain invariant.
```

### Direction B: Abstract Interpretation Of Agent Authority Traces

Method:

```text
Define concrete trace semantics and an abstract authority domain.
Implement several abstractions of increasing precision.
Show the safety / preservation / cost frontier.
```

Why it may publish:

- Gives a principled explanation for conservative collapse.
- Turns "guard is too strict" into "abstraction is too imprecise".
- Produces a natural ablation table.

Minimum experiment:

```text
Compare source-family-only, role-only, role+scope, role+scope+time+obligation,
and full-witness abstractions.
```

### Direction C: Protocol-Verified Authority Delegation

Method:

```text
Encode source events, capability manifests, delegation, time decay, and
execution as a symbolic protocol.
Prove no forge / no amplification / no replay properties on bounded trace
families.
```

Why it may publish:

- Strong formal-methods story for multi-agent and skill-driven agents.
- Turns prompt injection into an adversarial message model.

Risk:

- Might become a formal-verification paper rather than an agent-safety paper.

### Direction D: ADTree-Derived Authority-Confusion Benchmark

Method:

```text
Use attack-defense trees to systematically enumerate laundering paths and
defenses, then generate paired legal/laundered rows from each leaf.
```

Why it may publish:

- Helps justify test sample coverage.
- Good companion artifact, weaker as main contribution.

### Direction E: Cost-Bounded Authority Supervision

Method:

```text
Model guard decisions as a small MDP:
  allow / block / abstain / request evidence / repair.
Optimize for safety subject to false-block and latency budgets.
```

Why it may publish:

- Directly responds to Guardrail DoS and over-conservative supervision.
- Good second-stage direction after CapGuard metrics are stable.

## 10. Updated Recommendation

Best immediate paper spine:

```text
Authority-Constrained Action Invariance
  = runtime-enforcement transparency
  + supervisory-control permissiveness
  + information-flow authority noninterference
  + abstract-interpretation precision
  + capability-security confused-deputy prevention
```

Best short claim:

> CapGuard is a fieldwise authority-flow checker: it abstracts an agent trace
> into capability facts and preserves exactly those protected action fields
> whose required authority is witnessed by the sources they consume.

Best next implementation / experiment:

```text
Add an abstraction ablation:
  source-family-only
  role-only
  role+scope
  role+scope+time
  role+scope+time+obligation
  full minimal witness

Report:
  unauthorized field suppression
  authorized field preservation
  conservative collapse rate
  authority_abstraction_precision
  guard cost
```

## 11. Claim Firewall Additions

Do not claim:

- first information-flow control for agents;
- first noninterference / declassification formulation;
- first abstract interpreter or static analyzer for LLM agents;
- first capability-security solution or confused-deputy defense;
- first security protocol verification for agents;
- first attack-tree / attack-graph benchmark generator;
- first game-theoretic guard policy.

Safe claim:

```text
We instantiate these classical theories at a new object boundary:
source-to-action-field authority consumption in LLM agents.
```

This is narrower and stronger than:

```text
we make agents secure
we solve over-refusal
we create a universal formal model
```

