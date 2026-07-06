# Agent Action Invariance: Evidence, Trust, and Assurance Math Deep Dive

Date: 2026-07-01

Purpose:

The previous theory passes covered runtime enforcement, supervisory control,
policy logic, formal repair, model checking, information flow, abstract
interpretation, and capability security. This note asks a different question:

```text
Can we make AFW's minimal authority witness more like a mathematical audit
object rather than only a boolean allow/block proof?
```

Short answer:

```text
Yes. The best fusion points are trust-management logic, assurance cases,
defeasible argumentation, evidence fusion, causal attribution, robust
optimization, and model-based diagnosis.
```

## 1. Why This Matters

Current AFW already has:

```text
Cap(x)        source capability
Need(s,f)     field authority requirement
Witness(s,f)  minimal source subset supporting the field
```

But reviewers may ask:

1. Why is this source trusted?
2. What if two sources conflict?
3. What if the source is relevant but low confidence?
4. What if causal attribution says the action was driven by a different
   source than the declared witness?
5. Why is the witness "minimal" and what does that buy us?
6. Can the guard choose a less conservative intervention under uncertainty?

Traditional mathematical security models give us vocabulary for these.

## 2. Trust-Management Logics: Witnesses As Certificate Chains

Trust-management systems such as SPKI/SDSI, RT, and SecPAL model authorization
through distributed credentials and delegation.

AFW mapping:

| Trust-management object | AFW object |
|---|---|
| principal | source family or source issuer |
| credential / certificate | capability manifest or approval receipt |
| role membership | authority role such as `dispatch_operation_authority` |
| delegation | source passes bounded authority to another source or step |
| attenuation | authority loses scope, effect, time, or delegation power |
| proof chain | `Witness(s,f)` |

Best transfer:

```text
Certificate-Chain Authority Witness

Allow field f only if the source-to-field path contains a credential chain
whose terminal role covers Need(s,f), and every delegation step preserves
scope, effect, time, and obligation constraints.
```

This strengthens the skill-driven-agent direction:

```text
skill manifest -> skill output capability -> downstream action field
```

The key is that skill permission is not the same as downstream authority.

Example:

```text
ReportFormattingSkill can emit formatted report sections.
It cannot delegate risk-assessment authority unless the manifest explicitly
grants that role and the delegation scope includes risk fields.
```

Candidate theorem:

```text
No Role Amplification By Delegation:
  if every delegation step is role-monotone or role-attenuating,
  then no witness chain can authorize a role absent from its credential path.
```

Useful sources:

- RFC 2693, "SPKI Certificate Theory".
  <https://www.rfc-editor.org/rfc/rfc2693>
- Li, Mitchell, and Winsborough, "Design of a Role-Based Trust-Management
  Framework". <https://doi.org/10.1109/SP.2002.1004366>
- Becker et al., "SecPAL: Design and Semantics of a Decentralized
  Authorization Language".
  <https://www.microsoft.com/en-us/research/publication/secpal-design-semantics-decentralized-authorization-language/>

## 3. Evidence Fusion: Separate Authority Validity From Confidence

Dempster-Shafer theory, subjective logic, and Bayesian attack graphs all deal
with evidence under uncertainty.

Important warning:

```text
High confidence is not authorization.
```

AFW should not allow a field just because many documents agree. A hundred
retrieved reports can support a factual claim, but still cannot authorize a
side effect if none has the required role.

Useful separation:

```text
authority_validity:
  does Cap(x) cover Need(s,f)?

evidence_confidence:
  how credible, consistent, fresh, and non-conflicting is the evidence?
```

Possible decision rule:

| Authority validity | Evidence confidence | Decision |
|---|---|---|
| valid | high | allow |
| valid | low | allow-with-review or abstain depending on risk |
| invalid | high | block; confidence does not grant authority |
| conflict | any | abstain / route |

Candidate extension:

```text
Confidence-Carrying Authority Witness

Witness(s,f) =
  minimal capability support
  + confidence score over credential freshness, issuer trust, extraction
    confidence, and conflict mass
  + explicit counter-evidence list
```

New metrics:

```text
witness_confidence_calibration =
  E[ | predicted witness confidence - empirical correctness | ]

counter_evidence_exposure_rate =
  # blocked/abstained fields reporting counter-authority / # conflict fields
```

Most useful in paper:

- Keep authority as hard logic.
- Use evidence fusion only for audit priority and abstain routing.
- Do not let probabilistic confidence override missing authority.

Useful sources:

- Shafer, "A Mathematical Theory of Evidence". Princeton University Press.
- Jøsang, "Subjective Logic: A Formalism for Reasoning Under Uncertainty".
  <https://link.springer.com/book/10.1007/978-3-319-42337-1>
- Frigault and Wang, "Measuring Network Security Using Bayesian Network-Based
  Attack Graphs". <https://doi.org/10.1109/IRI.2008.4583048>

## 4. Assurance Cases And GSN: Witness As A Mini Safety Case

Goal Structuring Notation (GSN) and assurance cases organize claims, arguments,
evidence, assumptions, and context.

AFW mapping:

| Assurance-case object | AFW object |
|---|---|
| top claim | field f is authorized |
| strategy | prove role, scope, effect, time, and obligation coverage |
| evidence | source manifest, approval receipt, trace event, discharge event |
| assumption | extraction contract, source identity, clock / epoch validity |
| defeater | counter-authority, stale approval, missing obligation |
| confidence | witness confidence / audit confidence |

This makes minimal authority witness more than an implementation detail:

```text
Minimal Authority Witness =
  smallest assurance subcase sufficient to justify a field.
```

This also explains audit compression:

```text
raw trace may contain hundreds of events;
minimal witness reduces review to the handful of evidence nodes that support
or defeat the protected field.
```

New metric:

```text
assurance_compression_ratio =
  # witness evidence nodes / # raw trace evidence nodes
```

This is close to existing `mean_compression_ratio`, but the assurance-case
language helps reviewers understand why compression matters.

Good paper sentence:

> The witness is a field-level assurance case: it records the minimal evidence,
> assumptions, and defeaters needed to justify the authority of one action
> field.

Useful sources:

- Goal Structuring Notation Community Standard.
  <https://scsc.uk/scsc-141B>
- Kelly and Weaver, "The Goal Structuring Notation - A Safety Argument
  Notation". <https://www-users.york.ac.uk/~rjc/teaching/critical/kelley.pdf>
- Bloomfield and Rushby, "Assurance 2.0".
  <https://www.csl.sri.com/users/rushby/papers/assurance2.pdf>

## 5. Abstract Argumentation And Defeasible Reasoning

Dung-style abstract argumentation models arguments and attacks between
arguments. This is a good fit for counter-authority:

```text
positive argument:
  source x has capability c covering Need(s,f)

attacking argument:
  source y has counter-authority, stale epoch, revoked approval, missing
  obligation, or conflict with x
```

Decision mapping:

| Argumentation state | AFW decision |
|---|---|
| accepted positive argument, no undefeated attacker | allow |
| no positive argument | block |
| positive and undefeated counter-argument | abstain / route |
| only attackers against invalid field | block with explanation |

Why this helps:

- It formalizes `counter_authority`.
- It explains why `abstain` is not a weak "I don't know"; it is a rational
  decision under undefeated conflict.
- It gives a clean review story for disputes between approval, policy hold,
  memory, and tool metadata.

Candidate property:

```text
Defeater Transparency:
  if CapGuard abstains due to conflict, it must expose at least one undefeated
  defeater for the field.
```

Useful sources:

- Dung, "On the Acceptability of Arguments and its Fundamental Role in
  Nonmonotonic Reasoning, Logic Programming and n-Person Games".
  <https://doi.org/10.1016/0004-3702(94)00041-X>
- Prakken and Sartor, "Argument-Based Extended Logic Programming with
  Defeasible Priorities". <https://doi.org/10.1093/logcom/7.1.25>

## 6. Causal Attribution: Influence Is Not Authority

Recent LLM-agent defenses such as CausalArmor and AttriGuard ask why a tool
call was produced: was it driven by user intent or by untrusted external
content?

This is close, but not the same as AFW.

```text
causal attribution:
  what source influenced the action?

authority warrant:
  was that source allowed to govern this field?
```

Best fusion:

```text
Authority-Causal Alignment

A field is high-risk if the declared authority witness and the causal driver
of the field disagree.
```

Example:

```text
declared witness:
  user approval authorizes publish

causal driver:
  retrieved document instruction causes publish=true

decision:
  abstain, because declared authority and causal influence diverge
```

New metric:

```text
authority_causal_alignment =
  # fields where declared witness source matches causal driver class /
  # protected fields with causal attribution available
```

Important claim boundary:

- AttriGuard/CausalArmor are close neighbors for causal influence.
- AFW's delta is field authority, not causal attribution itself.
- The two combine well: causal attribution can audit whether the declared
  witness actually explains the action field.

Useful sources:

- CausalArmor: <https://arxiv.org/abs/2602.07918>
- AttriGuard: <https://arxiv.org/abs/2603.10749>
- Pearl, "Causal inference in statistics: An overview".
  <https://ftp.cs.ucla.edu/pub/stat_ser/r350.pdf>

## 7. Robust Optimization: Cost-Bounded Supervision

Robust optimization gives a way to choose guard decisions under uncertainty
while bounding worst-case safety loss or cost.

AFW decision variables:

```text
allow(f)
block(f)
abstain(f)
repair(f)
request_more_evidence(f)
```

Costs:

```text
false_allow_cost
false_block_cost
latency_cost
review_cost
audit_cost
task_salvage_reward
```

Constraint:

```text
never allow a field without valid authority
```

Optimization:

```text
minimize:
  false_block_cost + latency_cost + review_cost + edit_cost

subject to:
  authority soundness
  guard cost budget
  minimum authorized-field preservation
```

This gives a principled version of the user's concern:

```text
Security supervision should be strict on false allows but optimized against
unnecessary behavior changes and latency.
```

New direction:

```text
Budgeted Field Supervision

Compare:
  always-on heavy guard
  strict block
  fieldwise witness check
  fieldwise witness check + selective causal attribution
  fieldwise witness check + review budget
```

Useful sources:

- Bertsimas and Sim, "The Price of Robustness".
  <https://doi.org/10.1287/opre.1030.0065>
- Ben-Tal, El Ghaoui, and Nemirovski, "Robust Optimization".
  <https://press.princeton.edu/books/hardcover/9780691143682/robust-optimization>
- CausalArmor's selective defense motivation is a recent LLM-agent neighbor:
  <https://arxiv.org/abs/2602.07918>

## 8. Model-Based Diagnosis And Minimal Hitting Sets

Model-based diagnosis explains failures by finding minimal sets of components
whose abnormality accounts for an observation. This maps well to invalid
action fields.

AFW failure:

```text
field f is blocked or abstained
```

Possible causes:

```text
missing role
wrong source family
expired time scope
undischarged obligation
counter-authority
delegation not permitted
causal-driver mismatch
```

Minimal diagnosis:

```text
smallest set of missing or conflicting facts that explains why f cannot be
authorized.
```

Minimal repair:

```text
smallest set of extra evidence requests, field edits, or review routes needed
to make the action safe.
```

This strengthens blame localization:

```text
Blame(s,f) =
  minimal diagnosis for why ValidAuthority(s,f) failed
```

New metric:

```text
minimal_diagnosis_accuracy =
  # invalid fields whose reported cause set matches oracle / # invalid fields
```

Useful sources:

- Reiter, "A Theory of Diagnosis from First Principles".
  <https://doi.org/10.1016/0004-3702(87)90062-2>
- de Kleer and Williams, "Diagnosing Multiple Faults".
  <https://doi.org/10.1016/0004-3702(87)90063-4>

## 9. Formal Concept Analysis: Discovering The Authority Lattice

Formal Concept Analysis (FCA) builds concept lattices from objects and
attributes. It can help organize the space of roles, scopes, obligations, and
source types.

AFW mapping:

| FCA object | AFW object |
|---|---|
| object | source or trace row |
| attribute | role/scope/effect/time/obligation field |
| concept | maximal group of sources sharing capability attributes |
| implication | if a source has attributes A, it should also have B |
| concept lattice | authority role hierarchy |

Use cases:

1. discover redundant or missing capability labels;
2. generate role/scope coverage matrices;
3. detect suspicious role combinations;
4. build boundary-preserving role-mismatch rows;
5. explain why a new source type is outside current coverage.

Candidate experiment:

```text
Build an FCA lattice over all current AFW rows.
Find concepts with high support.
Generate negative cases by swapping one role attribute while preserving
scope/effect/time attributes.
```

This is weaker as a main theorem, but useful for dataset growth and coverage
audits.

Useful sources:

- Ganter and Wille, "Formal Concept Analysis: Mathematical Foundations".
  <https://link.springer.com/book/10.1007/978-3-642-59830-2>
- Priss, "Formal Concept Analysis in Information Science".
  <https://doi.org/10.1002/aris.1440400120>

## 10. New Candidate Directions

### Direction A: Assurance-Carrying Authority Witnesses

Method:

```text
Extend minimal witnesses into mini assurance cases:
  claim, evidence, assumptions, defeaters, confidence, and compression.
```

Why strong:

- Directly upgrades an existing AFW artifact.
- Helps paper storytelling: "we do not just block; we produce auditable
  justification".
- Integrates obligations, counter-authority, temporal decay, and audit
  compression.

Minimum experiment:

```text
For each allow/block/abstain, output a GSN-like witness tree and score:
  witness size
  raw trace size
  compression ratio
  defeater exposure
  diagnosis accuracy
```

### Direction B: Trust-Chain Authority Delegation

Method:

```text
Treat capability manifests as trust-management credentials.
Prove no role amplification along source -> skill -> output -> action chains.
```

Why strong:

- Best fit for skill-driven agents.
- Differentiates direct skill permission from downstream action authority.

Minimum experiment:

```text
Build paired traces where the skill is allowed to run but its output is
laundered into a role the skill never possessed.
```

### Direction C: Defeasible Counter-Authority Semantics

Method:

```text
Model authority and counter-authority as arguments.
Use accepted / attacked / undecided states to define allow / block / abstain.
```

Why strong:

- Makes `abstain` mathematically clean.
- Fits policy holds, revoked approvals, stale memory, and conflict cases.

Minimum experiment:

```text
Counter-authority rows with oracle defeaters and measured
counter_evidence_exposure_rate.
```

### Direction D: Authority-Causal Alignment

Method:

```text
Run a causal-attribution module on protected fields.
Check whether causal driver and declared authority witness agree.
```

Why strong:

- Bridges AFW with AttriGuard/CausalArmor without pretending to replace them.
- Catches hidden laundering when the declared witness is clean but the actual
  influence path is not.

Minimum experiment:

```text
Create traces where declared authority is valid but injected content causally
drives one protected field.
```

### Direction E: Budgeted Field Supervision

Method:

```text
Optimize guard routing under costs:
  allow, block, abstain, request evidence, repair.
```

Why strong:

- Directly answers whether guardrails make agents too conservative or too slow.
- Natural response to Guardrail DoS and over-defense.

Minimum experiment:

```text
Compare always-on heavy defense, strict block, CapGuard, and CapGuard +
selective causal attribution under latency / token budgets.
```

## 11. Updated Ranking

| Rank | Direction | Why |
|---:|---|---|
| 1 | Assurance-carrying authority witnesses | Most directly extends current AFW artifacts and audit story |
| 2 | Trust-chain authority delegation | Best fit for skill-driven agents and no-role-amplification theorem |
| 3 | Defeasible counter-authority semantics | Makes abstain/conflict rigorous |
| 4 | Authority-causal alignment | Strong bridge to recent causal defenses |
| 5 | Budgeted field supervision | Strong systems angle, probably second paper |
| 6 | Evidence-fusion confidence scoring | Useful but dangerous if it blurs authority vs confidence |
| 7 | FCA authority lattice mining | Good dataset/coverage tool, weak as main contribution |

## 12. Claim Firewall

Do not claim:

- first trust-management logic for agents;
- first evidence-fusion or Dempster-Shafer use in security;
- first subjective-logic trust model;
- first Bayesian attack graph or probabilistic risk model;
- first assurance case for AI or security;
- first argumentation-based security policy;
- first causal-attribution defense for LLM agents;
- first robust-optimization guard policy;
- first model-based diagnosis explanation;
- first formal concept analysis for access control.

Safe claim:

```text
AFW instantiates these traditions at a narrow object boundary:
minimal source-to-action-field authority witnesses for LLM agents.
```

Best current paper addition:

```text
The witness is not only a pass/fail artifact. It is an auditable, compressed
assurance case that records the minimal authority chain, assumptions, defeaters,
and missing facts for each protected field.
```

