# Agent Action Invariance Theory Scan

Date: 2026-07-01

Purpose: identify traditional offense-defense theory, mathematical modeling, and formal-methods concepts that can be fused with AFW / CapGuard. The working concern is:

> Under strict policy supervision, agent defenses may become too conservative and alter normal behavior. Can we formalize when a supervisor preserves legitimate agent actions while still blocking unsafe ones?

## 0. Current Best Name

Recommended name:

```text
Policy-Supervised Agent Action Invariance
```

AFW-specific name:

```text
Authority-Constrained Action Invariance
```

One-sentence thesis:

> A runtime guard for complex agents should be sound on unsafe actions but transparent on already-authorized action fields.

Plain version:

> 该拦的必须拦；本来合法的动作不要乱改；如果只有某个字段越权，就只干预那个字段，不要把整个 agent 打成“什么都不敢做”。

## 1. Why This Is More Interesting Than Another Guardrail

Existing AFW is already a field-level authority verifier:

```text
Cap(x) covers Need(s, f) -> field f may execute
otherwise -> block / abstain / route to review
```

The new question is orthogonal:

```text
If field f is already covered, must the guard preserve f?
If field f is not covered, what is the minimal intervention?
```

This turns the paper from "stronger blocking" into:

```text
safety + behavior preservation + minimal intervention
```

That framing directly answers the user's concern that defenses can make agents overly conservative during complex tasks.

## 2. Traditional Theory Hooks

### 2.1 Runtime Enforcement: Soundness + Transparency

Classic runtime enforcement already has the exact conceptual pair we need.

Ligatti, Bauer, and Walker's edit-automata framework defines runtime monitors as action-sequence transformers. The key bridge is:

```text
Soundness:
  transformed execution satisfies the policy.

Transparency:
  executions that already satisfy the policy are preserved.
```

For AFW:

```text
Soundness:
  no final action field executes without valid authority.

Transparency / action invariance:
  if Need(s, f) is covered by Cap(x), CapGuard must not alter f.
```

Why it helps:

- It gives a mature formal vocabulary for "防御不能乱改正常行为".
- It lets us say strict-block is conservative enforcement, not precise enforcement.
- It supports proofs over traces, not just benchmark scores.

Closest source:

- Jay Ligatti, Lujo Bauer, David Walker, "Edit Automata: Enforcement Mechanisms for Run-Time Security Policies", International Journal of Information Security, 2005. <https://users.ece.cmu.edu/~lbauer/papers/2005/ijis2005-editauto.pdf>
- Ligatti and Reddy, "A Theory of Runtime Enforcement, with Results", 2010, especially precise enforcement. <https://cse.usf.edu/~ligatti/papers/mra-tr.pdf>
- Runtime enforcement with partial control: defines transparency through semantic equivalence of valid executions. <https://arxiv.org/pdf/1508.06525>
- Cost-aware runtime enforcement: notes that soundness and transparency alone do not distinguish monitors with different output costs. <https://link.springer.com/chapter/10.1007/978-3-642-38004-4_1>

Paper angle:

> CapGuard should be evaluated as a precise field enforcer, not only as a conservative blocker.

Immediate AFW metric bridge:

```text
soundness:
  unsafe fields do not execute

transparency:
  authorized fields are unchanged

cost-aware enforcement:
  among all safe guarded traces, choose the one with lowest field-edit,
  review, latency, and task-loss cost
```

This gives a formal basis for saying strict-block is a valid but high-cost enforcer.

### 2.2 Shield Synthesis and Safe RL: Correct Only If Necessary

Shield synthesis and safe RL study controllers that sit around a system and correct unsafe actions at runtime. This maps very naturally to agent guardrails.

Traditional shield view:

```text
nominal policy pi proposes action a
shield S observes a
if a is safe, output a
if a is unsafe, output corrected action a'
```

AFW view:

```text
agent proposes structured action a = {f1, ..., fk}
CapGuard checks each field
safe fields are preserved
unsafe fields are blocked, repaired, or routed to review
```

The strong theory hook is "correct erroneous output only if necessary, and as little as possible." This is almost exactly our desired minimal field intervention.

Closest sources:

- Roderick Bloem et al., "Shield Synthesis: Runtime Enforcement for Reactive Systems", 2015. <https://arxiv.org/abs/1501.02573>
- Shield synthesis PDF / extended description, emphasizing minimum interference. <https://chaowang-vt.github.io/pubDOC/BloemKKW15.pdf>
- Minimum-cost shields for multi-agent systems. <https://figshare.le.ac.uk/articles/conference_contribution/Synthesis_of_Minimum-Cost_Shields_for_Multi-agent_Systems/10243328/files/18490232.pdf>
- Mohammed Alshiekh et al., "Safe Reinforcement Learning via Shielding", AAAI 2018. <https://arxiv.org/abs/1708.08611>
- CBF-RL and CBF safety filters are especially relevant because they formalize minimal modification of a nominal policy under safety constraints. <https://arxiv.org/html/2510.14959v1>

Paper angle:

> Agent guards should be modeled as semantic shields over structured actions. The novelty is not shielding itself, but field-level authority shielding over LLM agent traces.

Direct transfer:

```text
reactive-system shield:
  correct erroneous outputs only if necessary and as little as possible

AFW field shield:
  correct unauthorized fields only if necessary and preserve all witness-backed fields
```

### 2.3 Control Barrier Functions: Minimal Intervention Optimization

Control barrier functions often implement safety by solving:

```text
minimize distance(u, u_nominal)
subject to safety_constraint(x, u)
```

This is a clean mathematical template for agent action repair:

```text
minimize d(a', a)
subject to PolicySafe(a')
and PreserveAuthorizedFields(a', a)
```

For AFW, define distance at field level:

```text
d(a', a) =
  sum_f weight(f) * Changed(a'.f, a.f)
```

Then:

```text
authorized fields get infinite or very high preservation weight
unauthorized fields may be blocked, masked, or replaced with review action
```

This gives a bridge from "guardrail heuristic" to an optimization problem:

```text
argmin_{a'} d(a', a)
such that forall f in ProtectedFields:
  if a'.f executes then ValidAuthority(s, f)
```

Paper angle:

> We can formulate CapGuard not only as a classifier but as a minimal field-repair operator.

### 2.4 Capability Security and Confused Deputy

Capability systems address a classic problem: a program with multiple authority sources may misuse one authority on behalf of another requester.

AFW has a similar shape:

```text
agent holds multiple authority sources:
  evidence, skill, memory, approval, tool metadata, prior output

bug:
  source x is consumed under the wrong semantic role
```

Traditional confused deputy:

```text
file name does not carry the authority to access the file
program's ambient permission is silently used
```

AFW-style confused deputy:

```text
retrieved evidence / skill output does not carry authority for risk approval
agent's ambient reasoning context silently treats it as risk authority
```

Useful theory:

- explicit capability instead of ambient authority;
- least authority;
- no authority amplification;
- delegation should preserve or attenuate authority, not create it.

Closest sources:

- Norman Hardy, "The Confused Deputy", 1988. <https://www.cs.utexas.edu/~witchel/S25-380L/papers/hardy88confused.pdf>
- Miller, Yee, Shapiro, "Capability Myths Demolished". <https://classpages.cselabs.umn.edu/Fall-2021/csci5271/papers/SRL2003-02.pdf>
- Rajani, Garg, Rezk, "On access control, capabilities, their equivalence, and confused deputy attacks". <https://people.mpi-sws.org/~dg/papers/csf16-caps.pdf>

Paper angle:

> AFW is a capability-style response to semantic ambient authority inside agent context.

### 2.5 Information Flow and Robust Declassification

Information-flow security asks when information may flow from one domain to another. Robust declassification studies when intentional release is allowed without letting attackers influence what gets released.

AFW analogue:

```text
Not every influence is bad.
Some evidence should influence answers.
The question is whether the influence is authorized for this field.
```

This directly supports the "legitimate-vs-hijack influence" pair:

```text
legal evidence influence -> preserve
hijack influence -> block
```

Closest sources:

- Sabelfeld and Myers, "Language-Based Information-Flow Security". <https://cseweb.ucsd.edu/~dstefan/cse227-spring21/papers/sabelfeld%3Aifc.pdf>
- Zdancewic and Myers, "Robust Declassification". <https://www.cis.upenn.edu/~stevez/papers/Zda03.pdf>

Paper angle:

> AFW can be framed as robust authority declassification: sources may affect action fields only through declared authority channels.

### 2.6 Attack-Defense Trees and Quantitative Security

Attack-defense trees model attacker goals and defender countermeasures with quantitative attributes such as cost, probability, time, or risk reduction.

AFW can use this to organize benchmark generation:

```text
attacker goal:
  make agent execute unauthorized action field

attack refinements:
  evidence-to-approval laundering
  skill-to-delegation laundering
  memory-to-policy laundering
  tool-metadata-to-side-effect laundering

defense refinements:
  field witness
  obligation discharge
  temporal decay
  counter-authority abstain
  minimal repair
```

Metric bridge:

```text
attack success probability
defense intervention cost
false-block cost
audit cost
task-completion cost
```

Closest sources:

- Kordy, Mauw, Schweitzer, "Quantitative Questions on Attack-Defense Trees". <https://arxiv.org/abs/1210.8092>
- QuADTool, attack-defense-tree synthesis and bridge to verification. <https://arxiv.org/abs/2406.15605>

Paper angle:

> Use attack-defense trees not as the main novelty, but as the benchmark taxonomy and risk-cost model for authority laundering.

### 2.7 Stackelberg / Markov Security Games

Game-theoretic security models treat defender and attacker as strategic agents. This matters because a strict guard changes the attacker's incentives and the normal agent's action space.

Possible mapping:

```text
Defender chooses guard policy G:
  strict-block, field-repair, witness-only, review-route, adaptive threshold

Attacker chooses laundering strategy A:
  role mismatch, stale authority, obligation omission, counter-authority hiding

Normal agent chooses task policy pi:
  maximize task success under G
```

Payoff:

```text
U_defender = security_gain - utility_loss - audit_cost - latency_cost
U_attacker = attack_success - effort
U_agent = task_success - intervention_penalty
```

Closest sources:

- Sinha et al., "Stackelberg Security Games: Looking Beyond a Decade of Success". <https://www.ijcai.org/proceedings/2018/0775.pdf>
- Feng et al., "A Stackelberg Game and Markov Modeling of Moving Target Defense". <https://www.cs.tulane.edu/~zzheng3/publication/MTD-gamesec17.pdf>
- Survey: attacker-defender games and cyber security. <https://www.mdpi.com/2073-4336/15/4/28>

Paper angle:

> This is useful for evaluation and adaptive policy selection, but too broad for the main method. Keep as appendix/future work unless we build a concrete strategy-selection experiment.

## 3. LLM / Agent Neighbor Pressure

This action-invariance direction is related to, but not the same as, over-refusal work.

| Neighbor | What it already studies | Remaining AFW gap |
|---|---|---|
| OR-Bench | harmless prompts rejected by safety-aligned LLMs | single-turn refusal, not structured agent action fields |
| SoK jailbreak guardrails | security/efficiency/utility evaluation of guardrails | general guardrail evaluation, not field-level preservation |
| AgentDojo | attacks/defenses for tool-using agents | task utility exists, but not authority-preserving field invariance |
| Progent | privilege control and least-privilege tool calls | tool/argument policy, not semantic authority consumption per field |
| SkillGuard | permission framework for skills | skill permission and runtime effects, not downstream field-level action invariance |
| SafeHarbor | precise decision boundaries and agent over-refusal mitigation | context-aware harmful/benign boundary, not proof that authorized action fields are preserved |
| Tri-Guard / TRIAD | guardrail feedback that revises unsafe plans instead of over-refusing entire tasks | plan remediation and benign-task preservation, not field-level transparency / minimal authority witness |
| ShieldAgent | explicit safety-policy compliance over action trajectories | trajectory policy shielding, not semantic source-to-field authority invariance |

Closest sources:

- OR-Bench. <https://arxiv.org/abs/2405.20947>
- SoK: Evaluating Jailbreak Guardrails for Large Language Models. <https://arxiv.org/html/2506.10597v1>
- AgentDojo. <https://arxiv.org/abs/2406.13352>
- Progent. <https://arxiv.org/abs/2504.11703>
- SkillGuard. <https://arxiv.org/abs/2606.03024>
- SafeHarbor. <https://arxiv.org/abs/2605.05704>
- Tri-Guard / TRIAD, "From Risk Classification to Action Plan Remediation: A Guardrail Feedback Driven Framework for LLM Agents". <https://arxiv.org/abs/2606.05805>
- ShieldAgent. <https://arxiv.org/abs/2503.22738>

Safe claim:

> Prior work measures over-refusal or task utility, but AFW can define a stronger structural property: authorized action fields should be invariant under the guard.

Avoid claiming:

> First study of guardrail utility loss.

### 3.1 Direct Novelty Pressure From 2026 Agent Guardrail Papers

New search result:

```text
"defense makes agents overly conservative" is already an active agent-safety topic.
```

SafeHarbor explicitly targets over-refusal in LLM agents and claims precise decision boundaries. Tri-Guard/TRIAD directly moves from binary risk classification to action-plan remediation, routing partially unsafe plans to update rather than refusing the whole task. ShieldAgent already phrases the agent-guardrail problem as shielding action trajectories with verifiable safety-policy reasoning.

Therefore, the current direction must not be framed as:

```text
We are the first to notice guardrails hurt utility.
```

The safer, narrower delta is:

```text
Existing work preserves benign task success at the plan or trajectory level.
We define a field-level transparency property:
  if a protected field has a valid authority witness,
  the guard must preserve that field exactly.
```

This gives a different measurable object:

| Existing utility metric | AFW invariance metric |
|---|---|
| benign task success rate | authorized-field preservation rate |
| helpfulness-safety score | soundness-transparency pair |
| over-refusal rate | false intervention on valid fields |
| plan update success | minimal field edit distance |
| rule recall | witness-backed field preservation |

Reviewer-safe positioning:

> We do not compete with SafeHarbor or Tri-Guard on general over-refusal mitigation. We use classic runtime-enforcement transparency to define a stronger structural guarantee for guarded agent actions: valid fields should be unchanged, invalid fields should be minimally repaired or routed to review.

## 4. Formal Problem Draft

Let:

```text
pi       = nominal agent policy
G        = guard / supervisor
tau      = original action trace: a1, ..., an
tau'     = guarded trace: G(tau)
a_s      = structured action at step s
F_s      = protected fields in a_s
Auth(s,f)= ValidAuthority(s,f)
```

### 4.1 Safety

```text
forall s,f:
  Executes(tau', s, f) -> Auth(s, f)
```

No protected field executes without authority.

### 4.2 Field Transparency / Invariance

```text
forall s,f:
  Auth(s, f) and NoConflict(s, f)
  -> tau'.a_s.f = tau.a_s.f
```

Authorized, conflict-free fields should not be changed.

### 4.3 Minimal Intervention

```text
tau' = argmin_z d(z, tau)
       subject to Safety(z)
```

Distance can be field-weighted:

```text
d(z, tau) =
  changed_authorized_fields * high_weight
  + changed_unauthorized_fields * low_weight
  + inserted_review_steps * review_cost
  + deleted_task_steps * task_cost
```

### 4.4 Task Preservation

```text
TaskGoal(tau) and SafeRepairExists(tau)
  -> TaskGoal(tau')
```

This is harder than field invariance and may need empirical evaluation rather than proof.

### 4.5 Conservative Collapse

Define:

```text
ConservativeCollapse(G, D) =
  P_{tau in D}[safe_fields_changed or safe_task_fails]
```

Field version:

```text
FalseBlockRate =
  # authorized fields changed or blocked
  / # authorized fields
```

Trace version:

```text
LegalTracePreservation =
  # safe traces where tau' semantically equals tau
  / # safe traces
```

This gives a clean metric for "agent becomes too conservative."

## 5. Candidate Research Directions

### Direction A: Precise Field Enforcement for LLM Agents

Build a formal bridge from runtime-enforcement transparency to AFW:

```text
CapGuard is sound if it blocks unauthorized fields.
CapGuard is transparent if it preserves authorized fields.
CapGuard is precise if both hold.
```

Why promising:

- Directly grounded in classic theory.
- Extends current AFW with a sharper theorem/metric.
- Easy to test using existing legal-vs-laundered paired rows.

Main experiment:

Compare:

```text
strict-block
tool-permission
attribution-only
boundary-scope-only
CapGuard
CapGuard + field repair
```

Metrics:

```text
soundness / laundering block
field transparency
legal trace preservation
false block
minimal-edit distance
task completion
```

Verdict: strongest near-term direction.

### Direction B: Minimal Field Repair as Agent Shielding

Convert CapGuard from allow/block into a repair operator:

```text
unsafe field -> remove / mask / route-to-review
safe fields -> preserve
```

Example:

```json
{
  "answer": "manual explanation",
  "citations": ["manual-7"],
  "side_effect": "dispatch_work_order"
}
```

Repair:

```json
{
  "answer": "manual explanation",
  "citations": ["manual-7"],
  "side_effect": "require_human_approval"
}
```

Why promising:

- More useful than whole-action blocking.
- Fits CBF/shielding "minimal intervention".
- Can produce better task utility than strict-block.

Risk:

- Need define when partial action execution is semantically safe.

Verdict: strong method extension after Direction A.

### Direction C: Robust Authority Declassification

Use information-flow / declassification theory:

```text
source influence is allowed only through declared authority channels
```

AFW analogue:

```text
evidence may flow into answer.body
evidence may not flow into approval waiver
skill output may flow into report_format
skill output may not flow into risk conclusion
```

Why promising:

- Gives deeper theory language for legitimate-vs-hijack influence.
- Helps answer "not all influence is bad."

Risk:

- Information-flow framing can get heavy and may distract from agent action fields.

Verdict: good theory section, not main algorithm yet.

### Direction D: Attack-Defense Tree for Authority Laundering

Use ADTrees to systematically generate benchmark families:

```text
Goal: unauthorized field executes
  OR evidence laundering
  OR skill laundering
  OR memory laundering
  OR stale approval reuse
  OR obligation omission
```

Each defense has cost:

```text
witness cost
latency cost
false-block cost
human-review cost
```

Why promising:

- Good for benchmark design and visual explanation.
- Makes attack/defense coverage more systematic.

Risk:

- ADTree itself is old; must remain a tool, not novelty claim.

Verdict: useful evaluation scaffolding.

### Direction E: Game-Theoretic Guard Policy Selection

Model the defender's guard policy as a strategic choice:

```text
strict mode: high security, high false block
field mode: high security, low false block, more modeling cost
witness-only mode: low disruption, lower security
adaptive mode: changes by task risk
```

Why promising:

- Good long-term research direction.
- Can explain policy trade-offs under attacker adaptation.

Risk:

- Too big for current paper unless we implement a concrete small game.

Verdict: keep as future direction or appendix.

## 6. Recommended Pivot

Do not pivot to:

```text
"another unified agent security framework"
```

Pivot to:

```text
"precise field-level runtime enforcement for agents"
```

Core sentence:

> Existing defenses often optimize for blocking unsafe behavior; we study whether a guard preserves authorized behavior under strict supervision.

AFW sentence:

> CapGuard checks source-to-field authority and enforces a transparency property: covered fields are preserved, uncovered fields are minimally repaired or routed to review.

## 7. Immediate Integration With Current Project

Current artifacts already support the first version:

| Needed for new direction | Existing artifact |
|---|---|
| Legal vs laundered pairs | `examples/afw_*_rows.json` |
| Strict-block baseline | implemented in AFW bench |
| Legal preservation metric | current deterministic result table |
| False block metric | current baseline summaries |
| Runtime traces | `examples/data/afw_trace_adapter_*_cases.jsonl` |
| Minimal witness | current witness object |
| Partial block route | `final_action=require_human_approval` |

Missing artifacts:

1. `field_transparency_rate`
2. `minimal_edit_distance`
3. `legal_trace_preservation`
4. partial-repair output beyond whole-action `require_human_approval`
5. task-level utility preservation on multi-step traces

## 8. Next Search Seeds

Search and verify these next:

1. "precise enforcement" and "transparency" in runtime enforcement.
2. "minimum-cost shields" and "least restrictive shields" in reactive systems.
3. CBF-QP "minimum intervention" safety filters.
4. "robust declassification" and "selective dependency" in information flow.
5. "over-refusal" benchmarks beyond single-turn LLMs.
6. "agent utility preservation" in prompt-injection defenses.
7. "formal repair" or "program repair" with minimum edit distance.
8. "runtime assurance" conservative switching and utilization of untrusted controller.

## 9. Current Ranking

| Rank | Direction | Novelty potential | Fit with AFW | Risk |
|---:|---|---:|---:|---|
| 1 | Precise field enforcement / action invariance | high | very high | medium |
| 2 | Minimal field repair / semantic shield | high | high | medium |
| 3 | Robust authority declassification | medium-high | high | high theory overhead |
| 4 | ADTree benchmark generator | medium | medium-high | low novelty if standalone |
| 5 | Game-theoretic guard policy selection | medium | medium | too broad |

## 10. Working Abstract Seed

Runtime defenses for LLM agents are usually evaluated by whether they block unsafe tool calls or attacks. However, in complex tasks, strict supervision can also change legitimate behavior, causing agents to become overly conservative. We formulate this as policy-supervised agent action invariance: a guard should be sound on unauthorized action fields while transparent on fields that already satisfy the policy. Building on runtime-enforcement transparency and safe-control shielding, we instantiate this property for action-field authority warrants. Each source is lifted into a scoped capability, each protected action field declares a need, and the guard preserves fields whose needs are covered while minimally repairing or routing uncovered fields. This reframes agent safety evaluation from attack blocking alone to precise field enforcement, measured by laundering block rate, field transparency, minimal edit distance, and task preservation.

## 11. Control-Theory Deepening

The next theory pass adds a stronger formal vocabulary:

```text
supervisory control theory:
  safety + nonblocking + maximal permissiveness
```

This is a better fit than generic utility trade-off. In AFW terms:

```text
safety:
  no unauthorized protected field executes

nonblocking:
  the guard should not eliminate all paths to safe task completion

fieldwise maximal permissiveness:
  every protected field with a valid authority witness is preserved,
  and every protected field without one is suppressed, repaired, or routed to review
```

This lets us say:

```text
strict-block is safe but not maximally permissive and may be blocking.
CapGuard is locally maximally permissive under independent-field assumptions.
fieldwise-simplex repair can be safer than no guard and less blocking than whole-action review.
```

New supporting document:

- `docs/agent_action_invariance_control_theory_deep_dive_2026-07-01.md`

## 12. Policy-Logic Deepening

Another useful but non-central theory line is policy logic:

```text
deontic logic:
  permission / prohibition / obligation

XACML-style decisions:
  Permit / Deny / NotApplicable / Indeterminate

Belnap-style policy composition:
  grant / deny / conflict / unspecified
```

AFW mapping:

```text
allow:
  positive authority witness exists

block:
  missing role/scope/time/obligation or hard denial

abstain:
  conflict, counter-authority, missing receipt, or indeterminate policy state
```

This helps formalize `abstain`, obligation-carrying warrants, and counter-authority, but it should remain background/appendix material.

New supporting document:

- `docs/agent_action_invariance_policy_logic_deep_dive_2026-07-01.md`

## 13. 2026 Frontier Reality Check: The User's Pivot Is Real

The sharper problem statement is:

```text
Strict policy supervision can make complex agents too conservative.
How can a guard preserve authorized behavior while still blocking unauthorized behavior?
```

This direction is already pressured by very recent agent-guardrail work:

| Neighbor | What it shows | What it does not settle for AFW |
|---|---|---|
| SafeHarbor | agent defenses must balance safety and benign utility / over-refusal | exact source-to-field authority preservation |
| TRIAD / Tri-Guard | guardrail feedback can update an unsafe plan instead of refusing the whole task | formal field-level invariance under authority witnesses |
| PolicyGuard | policy adherence needs dialogue-level remediation and can block less than argument-level guards | capability-to-need coverage and minimal authority witness |
| Symbolic Guardrails | symbolic policies can improve safety/security without sacrificing agent utility | semantic-role laundering and fieldwise maximal permissiveness |
| Guardrail DoS | the guardrail itself can become an availability bottleneck under attack | bounded-cost authority checking and conservative-collapse metrics |

So the safe novelty claim is not:

```text
first to notice guardrails hurt utility
first to reduce over-refusal
first to remediate unsafe plans
```

The safer claim is:

```text
We formulate strict agent supervision as an action-invariance problem:
authorized fields should be preserved, unauthorized fields should be blocked,
repaired, or routed, and this judgment is backed by minimal authority witnesses.
```

This converts a vague utility trade-off into three testable objects:

1. `ValidAuthority(s,f)`: is this field authorized by the sources it consumes?
2. `Preserve(a.f)`: if authorized, did the guard leave it unchanged?
3. `Repair(a.f)`: if unauthorized, did the guard change only the necessary fields?

The next empirical section should therefore include a "strict-supervision collapse"
slice:

| Case type | Expected strict-block behavior | Expected CapGuard behavior |
|---|---|---|
| benign action with complete authority | unnecessary refusal | preserve all fields |
| mixed action with one laundered field | reject whole task | preserve valid fields and route invalid field |
| dialogue-level missing prerequisite | block or generic refusal | abstain with missing prerequisite witness |
| expensive guardrail reasoning case | high latency / conservative timeout | bounded field check or bounded abstain |

Useful added metrics:

```text
authorized_action_invariance =
  # authorized actions whose protected fields are unchanged / # authorized actions

partial_task_salvage =
  # mixed tasks with at least one preserved valid field / # mixed tasks

guard_cost_bound_violation =
  # cases exceeding guard token/time budget / # guarded cases
```

New pressure points to cite:

- PolicyGuard: <https://arxiv.org/abs/2606.29225>
- Guardrail DoS: <https://arxiv.org/abs/2606.14517>

## 14. Formal-Security Fusion Update

The next theory pass broadens the foundation from runtime/control theory to
traditional formal security:

```text
information-flow control:
  unauthorized sources should not influence protected fields

abstract interpretation:
  CapGuard analyzes an abstract authority state, not raw natural language

capability security / confused deputy:
  ambient agent ability is not enough; the source must carry field authority

protocol verification:
  delegation, replay, and role-amplification can be modeled as trace properties

attack-defense trees:
  structured way to generate laundering benchmark cases
```

Most useful near-term fusion:

```text
Authority-flow control for agent actions
  = information-flow labels over Cap(x)
  + field sinks defined by Need(s,f)
  + declassification only through valid authority witnesses
```

New candidate property:

```text
Authority Noninterference:
  changing sources that lack authority for field f must not change the guarded
  value or execution status of f.
```

New candidate metric:

```text
authority_abstraction_precision =
  # authorized fields with enough abstract evidence / # authorized fields
```

This also gives a cleaner explanation of conservative collapse:

```text
Some guards over-block because their authority abstraction is too coarse.
CapGuard should reduce false blocking by retaining the precise role/scope/time/
obligation facts needed to prove authority.
```

New supporting document:

- `docs/agent_action_invariance_formal_security_fusion_map_2026-07-01.md`

## 15. Evidence, Trust, And Assurance Update

The next mathematical-modeling pass focuses on `Witness(s,f)` itself.

Existing AFW view:

```text
Witness(s,f) =
  minimal set of capabilities that proves field f is authorized
```

Stronger audit view:

```text
Witness(s,f) =
  compressed field-level assurance case:
    claim
    evidence
    trust chain
    assumptions
    defeaters
    confidence notes
    missing facts / diagnosis
```

Most useful theory fusions:

| Theory | AFW use |
|---|---|
| trust-management logic | treat manifests and approvals as credential chains |
| assurance cases / GSN | make minimal witness an auditable claim-evidence structure |
| abstract argumentation | define counter-authority and `abstain` via defeaters |
| evidence fusion / subjective logic | attach confidence and conflict mass without letting confidence grant authority |
| causal attribution | compare declared witness with actual causal driver |
| robust optimization | choose less conservative guard routing under cost budgets |
| model-based diagnosis | explain why a field failed and what minimal repair is needed |
| formal concept analysis | mine capability lattices and coverage gaps |

Key warning:

```text
High confidence is not authorization.
```

This matters because a source can be factually reliable yet lack the semantic
role needed for a protected action field.

New candidate metrics:

```text
witness_confidence_calibration
counter_evidence_exposure_rate
assurance_compression_ratio
authority_causal_alignment
minimal_diagnosis_accuracy
```

Best new direction:

```text
Assurance-carrying authority witnesses:
  CapGuard outputs not only allow/block/abstain, but also the minimal
  trust-chain evidence, assumptions, defeaters, and missing facts behind the
  decision.
```

New supporting document:

- `docs/agent_action_invariance_evidence_trust_math_deep_dive_2026-07-01.md`

## 16. Hazard And Risk Engineering Update

Traditional safety/security engineering gives a systematic answer to:

```text
Where do the benchmark scenarios come from?
Which failures matter most?
Why is strict blocking not enough?
```

Most useful fusions:

| Method | AFW use |
|---|---|
| STPA / STAMP | model agent fields as control actions and derive unsafe control actions |
| STPA-Sec | model prompt injection as corrupted authority process-model variables |
| FMEA / FMECA | enumerate field failure modes and prioritize by severity/occurrence/detectability |
| Fault Tree Analysis | derive minimal cut sets for unauthorized field execution |
| Bow-Tie analysis | separate preventive barriers from recovery/audit barriers |
| HAZOP | generate authority-deviation rows using guide words |

Key insight:

```text
Over-conservative guarding can be unsafe by omission:
  failing to provide a required authorized control action can also be a loss
  scenario.
```

New candidate metrics:

```text
required_authorized_action_preservation =
  # required authorized fields preserved / # required authorized fields

field_risk_priority_number =
  severity * occurrence * non_detectability

cut_set_coverage =
  # modeled minimal cut sets hit by benchmark cases / # modeled minimal cut sets

high_rpn_failure_coverage =
  # high-risk failure modes represented in tests / # high-risk failure modes
```

Best new direction:

```text
STPA-derived action-invariance benchmark:
  unsafe control actions -> failure modes -> minimal cut sets -> HAZOP variants
  -> legal/laundered/temporal/counter-authority/repair traces.
```

New supporting document:

- `docs/agent_action_invariance_hazard_risk_engineering_deep_dive_2026-07-01.md`

## 17. Access-Control And Zero-Trust Update

Traditional access control asks:

```text
Can subject S perform action A on object O?
```

AFW asks a different question:

```text
Can source x authorize protected action field f?
```

Most useful fusions:

| Model | AFW use |
|---|---|
| RBAC | authority role taxonomy and source-role separation |
| ABAC | `Cap(x)` / `Need(s,f)` as source, field, action, environment attributes |
| UCON | continuous authority, obligations, mutable policy state, temporal decay |
| ReBAC | delegation and skill-output authority as relationship paths |
| NGAC / policy graph | witness extraction as minimal satisfying policy paths |
| Zero Trust | no source is trusted by default without explicit capability |
| policy-as-code | export field authority rules to deployment engines |
| separation of duty | block toxic source-role combinations and self-approval |

Key insight:

```text
Tool permission is a precondition.
Field authority is a separate source-to-field usage-control check.
```

Best new direction:

```text
UCON-style continuous authority for agent fields:
  ValidAuthority(s,f) must hold not only at proposal time, but across repair,
  obligation discharge, policy epoch changes, revocation, and execution.
```

New candidate metrics:

```text
attribute_coverage_rate
pre_authorization_pass_rate
ongoing_authorization_preservation
revocation_response_rate
obligation_mutation_detection_rate
sod_violation_detection_rate
```

New supporting document:

- `docs/agent_action_invariance_access_control_deep_dive_2026-07-01.md`

## 18. Accountability, Provenance, And Threshold Authority Update

The next traditional-security pass strengthens the audit object behind
`Witness(s,f)`.

Existing AFW:

```text
Cap(x) covers Need(s,f)
```

Accountable AFW:

```text
VerifiedCap(x) =
  Cap(x)
  + issuer identity
  + signature / attestation
  + policy epoch
  + artifact provenance
  + revocation state
  + log inclusion proof

VerifiedCap(x) covers Need(s,f)
```

Most useful fusions:

| Theory | AFW use |
|---|---|
| Byzantine quorum / BFT | require independent k-of-n authority for high-risk fields |
| threshold cryptography | model multi-approval and no-single-authorizer fields |
| Certificate Transparency / Merkle logs | make field witness events tamper-evident |
| provenance semirings | model minimal authority witnesses as compact source-to-field provenance expressions |
| verifiable credentials | encode skill/tool/approval capabilities as signed issuer claims |
| in-toto / SLSA / Sigstore | bind skill and tool authority to artifact provenance and signing events |
| non-repudiation | make both capability issuance and field consumption auditable |

Key insight:

```text
Accountability does not grant authority.
A signed report-formatting skill manifest still cannot authorize risk
assessment or external publication unless its Cap(x) covers that Need(s,f).
```

New candidate properties:

```text
Quorum-Sound Composite Authority:
  threshold-protected fields execute only with enough independent valid issuers.

Witness Log Inclusion:
  every executed protected field has a logged witness event.

Provenance-Minimal Authority Witness:
  removing any selected source from Witness(s,f) breaks Need(s,f) coverage.

Supply-Chain-Bound Skill Authority:
  a skill output contributes to Witness(s,f) only if the skill artifact,
  manifest, signer, and build provenance satisfy the field policy.
```

New candidate metrics:

```text
quorum_authority_coverage
source_independence_violation_rate
witness_log_completeness
witness_log_tamper_detection_rate
replay_epoch_mismatch_rate
provenance_witness_minimality
signed_manifest_verification_rate
skill_provenance_verification_rate
```

Best new direction:

```text
Threshold and tamper-evident authority witnesses:
  CapGuard outputs a minimal field witness whose sources are verified,
  logged, non-revoked, fresh for the current policy epoch, and sufficient for
  any k-of-n independence requirements on the field.
```

New supporting document:

- `docs/agent_action_invariance_accountability_provenance_deep_dive_2026-07-01.md`

## 19. Compositional Formal Methods Update

The next formal-methods pass asks whether local authority checks survive
composition across RAG, skills, memory, tools, approval, and prior-step output.

Key problem:

```text
Each component can be locally safe, but the composed agent trace can still
launder authority by combining weak sources into a stronger semantic role.
```

Best formal slogan:

```text
Compositional Authority Non-Amplification
```

Most useful fusions:

| Theory | AFW use |
|---|---|
| assume-guarantee reasoning | each agent component assumes input authority bounds and guarantees output authority bounds |
| contract-based design | source-producing components export authority contracts |
| interface automata | illegal interaction is consuming or emitting authority outside declared interface |
| temporal logic / TLA+ | specify multi-step authority lifecycle, obligation, revocation, and review liveness |
| Alloy / relational modeling | generate small counterexamples for role amplification and non-minimal witnesses |
| hyperproperties / HyperLTL | express same-source legal-vs-laundered contrast and authority noninterference |
| trace refinement / I/O automata | guarded trace equals original trace on authorized fields and is stricter on unauthorized fields |
| rely-guarantee | reason about concurrent memory/policy/source mutation |
| separation-logic frame conditions | field repair may modify only invalid authority frames plus routing/audit fields |

New candidate properties:

```text
Compositional Non-Amplification:
  derived or composed sources may attenuate or explicitly combine authority, but
  must not create a semantic role absent from upstream contracts.

Authority Contract Refinement:
  a component update is acceptable only if its emitted capabilities are no
  stronger than the previous contract, unless policy explicitly renegotiates it.

Authority Noninterference Hyperproperty:
  changing sources that lack authority for field f must not change the guarded
  value or execution status of f.

Authority Frame Preservation:
  repair of an invalid field may not alter unrelated authorized fields.
```

New candidate metrics:

```text
assumption_discharge_rate
contract_refinement_pass_rate
contract_violation_detection_rate
interface_compatibility_rate
temporal_property_coverage
relational_counterexample_yield
hyper_authority_noninterference_pass_rate
authority_refinement_pass_rate
interference_violation_detection_rate
frame_preservation_rate
```

Best new direction:

```text
Compositional non-amplification contracts:
  every source-producing component declares an authority contract, and CapGuard
  checks final action fields against composed witnesses that cannot invent new
  semantic roles.
```

New supporting document:

- `docs/agent_action_invariance_compositional_formal_methods_deep_dive_2026-07-01.md`
