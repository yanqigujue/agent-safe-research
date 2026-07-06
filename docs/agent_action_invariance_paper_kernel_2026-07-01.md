# Paper Kernel: Authority-Constrained Agent Action Invariance

Date: 2026-07-01

This kernel turns the theory-search results into a paper-facing contribution shape. It should be read together with:

- `docs/agent_action_invariance_theory_scan_2026-07-01.md`
- `docs/agent_action_invariance_control_theory_deep_dive_2026-07-01.md`
- `docs/agent_action_invariance_experiment_seed_2026-07-01.md`
- `docs/agent_action_invariance_accountability_provenance_deep_dive_2026-07-01.md`
- `docs/agent_action_invariance_compositional_formal_methods_deep_dive_2026-07-01.md`

## 1. One-Sentence Thesis

Agent guards should not only block unauthorized actions; they should preserve every action field that already has a valid authority witness.

AFW-specific version:

> CapGuard is a fieldwise supervisor for LLM agents: it enforces authority safety while preserving every protected field whose `Need(s,f)` is covered by a consumed `Cap(x)`.

## 2. Why This Is A Better Pivot

The crowded prior-work space already covers:

- tool-call authorization,
- skill permission,
- prompt-injection defenses,
- over-refusal mitigation,
- runtime monitoring,
- probabilistic future-risk intervention,
- generic proof-carrying actions,
- capability governance.

The remaining sharp gap is not:

```text
Can we make a guard that blocks more attacks?
```

The sharper question is:

```text
Can a guard be precise enough to preserve every already-authorized action field?
```

This maps directly to traditional formal theory:

```text
runtime enforcement:
  soundness + transparency

supervisory control:
  safety + nonblocking + maximal permissiveness

runtime assurance:
  switch only the unsafe part to a backup controller

minimum-violation planning:
  satisfy hard safety constraints while minimizing soft utility violations

contract theory:
  source capability and field need are compatible contracts
```

## 3. Main Formal Objects

Use the existing AFW objects:

```text
Cap(x) = source capability
Need(s,f) = field authority requirement
Consume(x -> f, s) = source x is consumed by field f at step s
ValidAuthority(s,f) = all required roles/scopes/obligations are covered
Witness(s,f) = minimal source subset proving ValidAuthority(s,f)
```

Guard transformation:

```text
G(a_s) = a'_s
```

where `a_s` is a structured agent action with protected fields.

## 4. Core Properties

### P1. Authority Soundness

```text
forall s,f:
  Executes(a'_s.f) -> ValidAuthority(s,f)
```

No protected field executes without valid authority.

### P2. Fieldwise Transparency

```text
forall s,f:
  ValidAuthority(s,f) and NoCounterAuthority(s,f)
  -> a'_s.f = a_s.f
```

Already-authorized fields are unchanged.

### P3. Local Maximal Permissiveness

```text
AllowedFields(G, s) =
  { f | ValidAuthority(s,f) and NoCounterAuthority(s,f) }
```

Under independent-field assumptions, no authority-safe field supervisor can allow a strict superset of CapGuard's allowed fields.

### P4. Nonblocking Progress

```text
SafeCompletionReachable(a_s)
  -> SafeCompletionReachable(G(a_s))
```

This is too strong for arbitrary agents, so use it as an empirical / restricted-trace target. The practical metric is `nonblocking_completion_distance`.

## 5. Theorem Set

### Theorem 1: Field Authority Soundness

Assumptions:

1. `ValidAuthority(s,f)` is decidable from observed `Cap(x)`, `Need(s,f)`, and `Consume(x -> f,s)`.
2. The guard executes a protected field only when the field decision is `allow`.
3. `allow(s,f)` is returned only if `ValidAuthority(s,f)` holds and no required obligation is unsatisfied.

Claim:

```text
Every executed protected field has valid authority.
```

Proof sketch:

CapGuard's decision rule is by construction:

```text
allow(s,f) iff ValidAuthority(s,f) and obligations/counter-authority permit execution
```

Since only `allow` fields execute, all executed fields satisfy `ValidAuthority`.

### Theorem 2: Witness-Backed Field Transparency

Assumptions:

1. `Witness(s,f).covers_need = true`.
2. No counter-authority applies to field `f`.
3. The output transformer rewrites only non-allow fields.

Claim:

```text
a'_s.f = a_s.f
```

Proof sketch:

`Witness(s,f).covers_need = true` implies `ValidAuthority(s,f)`. With no counter-authority and no unsatisfied obligation, CapGuard returns `allow`. The transformer rewrites only non-allow fields, so field `f` is preserved.

### Theorem 3: Strict-Block Is Not Transparent

Assumptions:

1. A structured action contains at least one authorized protected field.
2. The same action contains at least one unauthorized protected field.
3. Strict-block suppresses the whole action if any protected field is unauthorized.

Claim:

```text
Strict-block changes at least one authorized field.
```

Proof sketch:

Because at least one unauthorized field exists, strict-block suppresses the whole action. Because at least one authorized field exists in the action, that authorized field is also suppressed. Therefore strict-block is sound but not field-transparent.

### Theorem 4: Local Fieldwise Maximal Permissiveness

Assumptions:

1. Protected fields are independently executable or suppressible.
2. Suppressing an unauthorized field does not invalidate other fields' authority.
3. Field safety is exactly `ValidAuthority(s,f)`.

Claim:

```text
CapGuard allows every locally authority-safe field and no locally authority-unsafe field.
No other field supervisor satisfying authority soundness can allow a strict superset.
```

Proof sketch:

Any unauthorized field allowed by another supervisor violates authority soundness. Any authorized field is already allowed by CapGuard. Therefore no sound field supervisor can allow more fields than CapGuard at step `s`.

## 6. Metrics

| Metric | Formula | Purpose |
|---|---|---|
| Unauthorized Field Suppression | `# unsafe fields blocked_or_reviewed / # unsafe fields` | Safety |
| Authorized Field Preservation | `# authorized fields unchanged / # authorized fields` | Transparency |
| Witness-Backed Transparency | `# witness-covered fields unchanged / # witness-covered fields` | Links witness to invariance |
| Fieldwise Maximal Permissiveness | `1` iff all valid fields preserved and all invalid fields suppressed/reviewed | Supervisory-control analogue |
| Conservative Collapse Rate | `# safe fields/tasks unnecessarily changed / # safe fields/tasks` | Measures over-conservatism |
| Mean Field Edit Cost | weighted edit distance between candidate and guarded action | Minimal intervention |
| Nonblocking Completion Distance | extra safe steps needed to reach completion after guarding | Progress preservation |
| Partial Task Salvage Rate | `# mixed tasks with at least one valid field preserved / # mixed tasks` | Avoids whole-task collapse |
| Guard Cost Bound Violation | `# guard calls over token/time budget / # guard calls` | Checks whether supervision itself harms performance |
| Blame Localization Accuracy | `# failures whose reported missing/counter authority matches oracle / # failures` | Measures whether repair has the right target |
| Authority Abstraction Precision | `# authorized fields provable in the abstract authority state / # authorized fields` | Explains false blocks as precision loss |
| Assurance Compression Ratio | `# witness evidence nodes / # raw trace evidence nodes` | Measures audit-context reduction |
| Counter-Evidence Exposure Rate | `# conflict decisions exposing a defeater / # conflict decisions` | Tests whether abstain is explainable |
| Authority-Causal Alignment | `# fields whose causal driver matches declared witness class / # attributed protected fields` | Detects hidden laundering |
| Required Authorized Action Preservation | `# required authorized fields preserved / # required authorized fields` | Captures unsafe omission from over-conservative guarding |
| High-RPN Failure Coverage | `# high-risk failure modes represented in tests / # high-risk failure modes` | Risk-prioritized benchmark coverage |
| Cut-Set Coverage | `# modeled minimal cut sets hit by tests / # modeled minimal cut sets` | Checks systematic threat coverage |
| Ongoing Authorization Preservation | `# fields still valid at execution after valid proposal / # fields valid at proposal` | Captures UCON-style continuous authority |
| Revocation Response Rate | `# revoked/expired fields blocked or routed / # revoked/expired fields` | Tests temporal decay and policy mutation |
| Source SoD Violation Detection | `# toxic source-role combinations blocked/routed / # toxic-combination cases` | Tests separation-of-duty constraints |
| Quorum Authority Coverage | `# threshold fields with enough independent valid issuers / # threshold fields` | Tests k-of-n composite authority |
| Source Independence Violation Rate | `# dependent-issuer quorum failures detected / # quorum cases` | Detects fake multi-source authority |
| Witness Log Completeness | `# executed protected fields with logged witness events / # executed protected fields` | Tests audit completeness |
| Witness Log Tamper Detection Rate | `# detected log rewrite/delete/fork attacks / # injected log tamper attacks` | Tests tamper-evident audit trail |
| Provenance Witness Minimality | `# witnesses where every selected source is necessary / # emitted witnesses` | Tests minimal provenance-backed witness |
| Signed Manifest Verification Rate | `# consumed capability manifests with valid issuer signatures / # consumed manifests` | Tests verifiable capability inputs |
| Skill Provenance Verification Rate | `# consumed skill outputs with verified artifact provenance / # consumed skill outputs` | Tests skill supply-chain authority |
| Assumption Discharge Rate | `# component assumptions discharged by upstream guarantees / # component assumptions` | Tests assume-guarantee closure |
| Contract Refinement Pass Rate | `# component updates whose authority contract refines prior contract / # component updates` | Tests safe component evolution |
| Contract Violation Detection Rate | `# detected authority-contract violations / # injected contract violations` | Tests component contract enforcement |
| Interface Compatibility Rate | `# compatible source-component consumptions / # source-component consumptions` | Tests declared authority interfaces |
| Hyper-Authority Noninterference Pass Rate | `# paired traces where unauthorized-source changes do not affect guarded field / # paired traces` | Tests hyperproperty view |
| Authority Refinement Pass Rate | `# guarded traces satisfying selective authority refinement / # guarded traces` | Tests trace-level preservation |
| Frame Preservation Rate | `# repairs preserving all out-of-frame authorized fields / # repairs` | Tests precise field repair |

## 7. Experiment Table Shape

| Method | UFS up | AFP up | WBT up | FMP up | CCR down | Edit Cost down | NCD down |
|---|---:|---:|---:|---:|---:|---:|---:|
| No guard | low | high | high | low | low | low | low |
| Strict-block | high | low | low | low | high | high | high |
| Permission-only | low | high | high | low | low | low | low |
| Attribution-only | low | high | high | low | low | low | low |
| Boundary-scope-only | medium | high | high | medium | low | low | low |
| CapGuard whole-action review | high | high | high | high on field decisions, medium on final action | low-medium | medium | medium |
| CapGuard fieldwise-simplex | high | high | high | high | low | low-medium | low |

Interpretation:

- `No guard` preserves behavior but is unsafe.
- `Strict-block` is safe but over-conservative.
- Weak baselines preserve behavior but miss laundering.
- CapGuard is the first candidate that should satisfy both field soundness and field transparency on the AFW benchmark.
- Fieldwise-simplex is the system extension that should reduce edit cost and nonblocking distance.

## 8. Closest-Neighbor Firewall

| Neighbor | What it already covers | Do not claim | Safe delta |
|---|---|---|---|
| Runtime enforcement / edit automata | Soundness and transparency for runtime policies | First transparency notion | We instantiate transparency at LLM-agent action-field authority granularity. |
| Supervisory control | Nonblocking and maximally permissive supervisors | First maximal-permissiveness theory | We define a local fieldwise analogue for structured agent actions. |
| Shield synthesis / safe RL | Correct unsafe outputs while minimizing interference | First shield / first minimal intervention | We shield semantic authority consumption, not physical control actions. |
| Runtime assurance / Simplex | Switch unsafe controllers to backup controllers | First runtime assurance architecture | We propose fieldwise switching instead of whole-agent backup. |
| Minimum-violation planning | Least-violating trajectories under conflicting specs | First minimal-repair method | We use it as the optimization view for field repair. |
| Information-flow control / declassification | Noninterference and controlled release | First IFC or declassification model for agents | We instantiate authority flow from sources to protected action fields. |
| Abstract interpretation / static analysis | Sound approximation of program behavior | First abstract interpreter or static analyzer for agents | We analyze an abstract authority state over trace-derived capabilities and needs. |
| Capability security / confused deputy | Prevent ambient authority misuse | First capability-security defense | AFW prevents wrong-source semantic-role laundering into protected fields. |
| Protocol verification | Prove trace correspondence properties under Dolev-Yao attackers | First formal verification of agent protocols | We keep protocol encodings as appendix/future-work support for source-to-field authority. |
| Attack-defense trees / attack graphs | Structured attack and defense enumeration | First attack-tree benchmark for agents | Use them to generate laundering cases, not as the core method. |
| Trust-management logic | Credential chains, delegation, and distributed authorization | First trust-management model for agents | We treat capability manifests and approvals as witness-chain inputs. |
| Assurance cases / GSN | Claim-evidence safety and security arguments | First assurance case for AI/agent safety | We compress each field decision into a minimal authority assurance case. |
| Abstract argumentation / defeasible logic | Attacks, defeaters, accepted arguments | First argumentation-based security policy | We use defeaters to formalize counter-authority and abstain. |
| Evidence fusion / subjective logic | Confidence, uncertainty, and conflict mass | First probabilistic/evidential trust model | Confidence can prioritize review, but missing authority still blocks. |
| Causal attribution defenses | Identify what source drove an action | First causal defense for LLM agents | We compare causal driver with declared authority witness. |
| STPA / STPA-Sec | Unsafe control actions and security control flaws | First STPA method for agents | We derive authority-specific unsafe control actions and benchmark cases. |
| FMEA / FMECA | Failure modes, severity, occurrence, detectability | First FMEA for AI/agent systems | We prioritize field-level false allow/block/abstain/repair failures. |
| Fault trees / Bow-Tie / HAZOP | Minimal cut sets, barriers, and guide-word deviations | First risk-engineering benchmark generator | We use them to systematize authority-laundering rows and ablations. |
| RBAC / ABAC | role and attribute based access decisions | First access-control model for agents | AFW applies role/attribute checks to source-to-field consumption, not only agent-to-tool execution. |
| UCON / usage control | ongoing authorization, obligations, conditions, mutable attributes | First usage-control model for agents | CapGuard's temporal decay and obligation warrants instantiate continuous field authority. |
| ReBAC / NGAC / policy graphs | relationship paths and graph-based policy decisions | First relationship or policy-graph authorization model | We use relationship paths to bound skill/source delegation into action fields. |
| Zero Trust / policy-as-code | dynamic contextual policy enforcement | First zero-trust or policy-as-code agent guard | AFW's zero-trust boundary is source authority over protected fields. |
| XACML / access-control combining | permit/deny/not-applicable/indeterminate and policy combining | First multi-valued access decision | AFW's `abstain` is tied to counter-authority and missing runtime warrant, not generic policy algebra. |
| Byzantine quorum / BFT | tolerate faulty or malicious participants through quorum agreement | First BFT or consensus protocol for agents | We use quorum as a field-authority threshold lens, not as a replicated-state-machine protocol. |
| Threshold signatures / multi-approval | distributed signing and k-of-n authorization | First threshold authorization mechanism | We instantiate threshold requirements as field-level authority witnesses. |
| Certificate Transparency / Merkle logs | tamper-evident append-only logs with inclusion and consistency proofs | First transparency log or audit log | We log action-field witness events for audit completeness and replay detection. |
| Provenance semirings | compact formal provenance expressions over query inputs | First provenance theory | We model minimal source-to-field authority witnesses as provenance expressions. |
| Verifiable Credentials | issuer-holder-verifier credential claims | First signed capability credential system | We use signed capability claims as inputs to `Cap(x)` verification. |
| in-toto / SLSA / Sigstore | signed software supply-chain provenance and transparency | First supply-chain security framework for agents | We bind skill/tool authority to artifact provenance before it can support a protected field. |
| Assume-guarantee reasoning | compositional proofs from component assumptions and guarantees | First compositional verification for agents | We use it to state source-producing component authority contracts. |
| Contract-based design | assumption/guarantee interfaces and refinement | First contract framework for agents | We define authority contracts for capabilities emitted by skills/tools/memory. |
| Interface automata / I/O automata | compatible component interaction and trace behavior | First automata model for agents | We model illegal interaction as consuming authority outside a component interface. |
| TLA+ / LTL / model checking | temporal state-machine specs and trace checking | First temporal-logic agent verifier | We express AFW lifecycle properties such as execution, obligation discharge, revocation, and repair. |
| Alloy / relational modeling | lightweight relational counterexample generation | First relational model of agent security | We generate small authority-laundering counterexamples and benchmark rows. |
| Hyperproperties / HyperLTL | security properties over multiple traces | First hyperproperty model for agents | We state same-source legal-vs-laundered contrast as authority noninterference. |
| Trace refinement / process algebra | implementation traces refine specification traces | First refinement checker for agents | Guarded traces selectively refine nominal traces: preserve authorized fields, suppress unsafe fields. |
| Rely-guarantee / separation logic | concurrent interference and frame preservation | First concurrency or frame logic for agents | We use them as lenses for source mutation and fieldwise repair scope. |
| AgentSpec / symbolic guardrails | Customizable runtime enforcement rules for LLM agents | First DSL or symbolic runtime enforcement for agents | AFW's object is authority-witness-backed field preservation, not general trigger-check-enforce policy rules. |
| SafeHarbor / TRIAD | Agent over-refusal and plan remediation | First guardrail utility-preservation study | We measure exact authorized-field preservation, not only benign task success. |
| PolicyGuard | dialogue-level policy verification and remediation | First policy-adherence verifier or remediation guard | AFW uses source-to-field capability coverage to decide which action fields must remain invariant. |
| Guardrail DoS | guardrails themselves can become denial-of-service targets and degrade availability | First availability/latency critique of guardrails | We add bounded field checks and conservative-collapse metrics as part of action-invariance evaluation. |
| ShieldAgent | Policy shielding for action trajectories | First action shielding for agents | We focus on source-to-field authority witnesses and local maximal permissiveness. |
| ProbGuard | Probabilistic runtime monitoring and proactive intervention | First runtime monitor for LLM agents | ProbGuard predicts when to intervene; AFW decides which fields to preserve or repair. |
| SkillGuard / skill verification | Skill permission and verifiable skill artifacts | First skill security framework | We study downstream consumption of skill authority by action fields. |

## 9. Reviewer Objections And Answers

### Objection: This is just over-refusal mitigation.

Answer:

> Over-refusal work measures whether benign tasks are refused. We define a structural field-level property: if a field has an authority witness, the guard must preserve that exact field.

### Objection: This is just runtime enforcement transparency.

Answer:

> The theory is inherited, but the agent-specific contribution is the protected action-field object, the source-to-field authority witness, and the semantic-role laundering benchmark where strict-block is sound but not transparent.

### Objection: AgentSpec or symbolic guardrails already enforce runtime policies.

Answer:

> They provide general rule languages and enforcement mechanisms. AFW asks a narrower question inside a structured action: which fields have an authority witness and therefore must be preserved by any precise guard?

### Objection: This is just access control.

Answer:

> Access control asks whether an action is permitted. AFW asks whether the source consumed by each field carries the semantic role required by that field. The same source may be valid for one field and invalid for another.

### Objection: Maximal permissiveness is impossible for LLM agents.

Answer:

> We do not claim global maximal permissiveness. We claim local fieldwise maximal permissiveness under explicit consumption edges, decidable field needs, and independent field effects.

### Objection: The theorem is too narrow.

Answer:

> It is intentionally narrow: it converts a guardrail design problem into a precise field-level invariant that can be tested on agent traces. The empirical sections then measure where assumptions fail.

## 10. Paper Contribution Stack

Recommended contribution list:

1. **Problem:** Conservative collapse under strict agent supervision.
2. **Formalism:** Authority-constrained action invariance over protected fields.
3. **Theory:** Field soundness, witness-backed transparency, local fieldwise maximal permissiveness, and authority-flow noninterference.
4. **Method:** CapGuard as a fieldwise authority supervisor.
5. **System extension:** Fieldwise-simplex repair for partial action preservation.
6. **Audit artifact:** assurance-carrying minimal authority witnesses with evidence, assumptions, defeaters, and missing facts.
7. **Accountability extension:** threshold, logged, provenance-backed, and signed-manifest witnesses for high-risk fields.
8. **Compositional extension:** component authority contracts, non-amplifying composition, hyperproperty contrast, and authority-frame repair.
9. **Benchmark:** same-source legal-vs-laundered rows plus STPA/FMEA/FTA-derived multi-step traces.
10. **Metrics:** UFS, AFP, WBT, FMP, CCR, edit cost, nonblocking completion distance, partial task salvage, guard cost bound violation, blame localization, authority abstraction precision, assurance compression, counter-evidence exposure, authority-causal alignment, required authorized action preservation, high-RPN failure coverage, cut-set coverage, ongoing authorization preservation, revocation response, source-SoD detection, quorum coverage, witness-log completeness, provenance witness minimality, signed-manifest verification, skill-provenance verification, contract refinement, hyper-authority noninterference, authority refinement, and frame preservation.

## 11. Minimal Implementation Roadmap

Stage 1: no new guard behavior.

```text
Add reporting only:
  authorized_field_preservation
  witness_backed_transparency
  fieldwise_maximal_permissiveness
  conservative_collapse_rate
  field_edit_cost
  authority_abstraction_precision
  assurance_compression_ratio
  counter_evidence_exposure_rate
  required_authorized_action_preservation
  high_rpn_failure_coverage
  cut_set_coverage
  ongoing_authorization_preservation
  revocation_response_rate
  sod_violation_detection_rate
  quorum_authority_coverage
  source_independence_violation_rate
  witness_log_completeness
  witness_log_tamper_detection_rate
  provenance_witness_minimality
  signed_manifest_verification_rate
  skill_provenance_verification_rate
  assumption_discharge_rate
  contract_refinement_pass_rate
  contract_violation_detection_rate
  interface_compatibility_rate
  hyper_authority_noninterference_pass_rate
  authority_refinement_pass_rate
  frame_preservation_rate
```

Stage 2: fieldwise-simplex output mode.

```text
If some fields allow and some block:
  preserve allow fields
  replace blocked side-effect/risk/delegation fields with review-route
  keep task-informational fields when safe
```

Stage 3: multi-step nonblocking traces.

```text
Build traces where:
  strict-block prevents final safe answer
  whole-action review reaches completion with extra review
  fieldwise-simplex reaches completion with fewer edits
```

## 12. Recommended Title Options

1. **Authority-Constrained Action Invariance for LLM Agents**
2. **Fieldwise Maximally Permissive Guarding for Agent Actions**
3. **CapGuard: Preserving Authorized Agent Actions Under Strict Supervision**
4. **From Blocking to Supervising: Fieldwise Action Invariance for Secure Agents**

Best current title:

> **Authority-Constrained Action Invariance for LLM Agents**
