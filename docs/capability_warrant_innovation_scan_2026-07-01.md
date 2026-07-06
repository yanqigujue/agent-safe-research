# Capability Warrant Innovation Scan

Date: 2026-07-01

Purpose: explore publishable pain points and innovation angles after expanding WarrantGuard beyond RAG into skill-driven and tool/MCP-driven agents.

## Current Project Baseline

The current WarrantGuard story is already sharp for RAG:

> Retrieved evidence is not ambient context; it is a bounded capability to govern protected action fields.

Existing formal object:

```text
Evidence Warrant:
  W_a = (F_a, C_a, S_a, T_a, X_a, H_a)

Execute(a) iff
  HardGate(a, H_a) = PASS
  and VerifyWarrant(a, W_a, K_q) = PASS
  and CounterWarrant(a, W_a, K_q) = CLEAR
```

This gives us a strong local novelty: same evidence can be valid for one action field and invalid for another. The limitation is that it is still framed as RAG-specific. Many modern agents are skill-driven, tool-driven, or MCP-driven, so the bigger question is no longer only evidence-to-action authority.

## Recent Neighbor Landscape

| Neighbor | What it already covers | Pressure on us |
|---|---|---|
| [Agent Skills for Large Language Models](https://arxiv.org/abs/2602.12430) | Frames skills as composable packages of instructions, code, and resources; highlights architecture, acquisition, and security issues. | Confirms skill-driven agents are a real frontier, not a side topic. |
| [SkillsBench](https://arxiv.org/abs/2602.12670) | Benchmarks whether curated skills improve task performance across domains. | Skill evaluation exists, but mostly capability/performance rather than authority misuse. |
| [Skill-Inject](https://arxiv.org/abs/2602.20156) | Measures agent vulnerability to skill-file attacks and prompt injection through skills. | Directly blocks a naive "skill injection benchmark" paper. |
| [Formal Analysis and Supply Chain Security for Agentic AI Skills](https://arxiv.org/abs/2603.00195) | Uses formal/static analysis for skill supply-chain security. | Directly blocks a naive "scan skill files for unsafe APIs" paper. |
| [SkillGuard](https://arxiv.org/abs/2606.03024) | Permission framework for agent skills, including what skills can inject into context and cause at runtime. | The strongest close neighbor for skill manifests and runtime permission. |
| [Methods for Formal Verification of Agent Skills](https://arxiv.org/abs/2605.23951) | Gives proof-carrying skill artifacts, capability-containment proofs, refinement types for tool-call envelopes, and bounded model checking of skill traces. | Blocks "proof-carrying skill" and "skill warrant compiler" as main novelty. We must focus on action-field authority consumption after the skill is already loaded or verified. |
| [ToolPrivBench](https://arxiv.org/abs/2606.20023) | Studies over-privileged tool selection when lower-privilege tools suffice. | Blocks a simple "least-privilege tool selection" claim. |
| [ToolSafe](https://arxiv.org/abs/2601.10156) | Step-level guardrail and feedback for tool invocation safety. | Blocks a generic "runtime tool-call guard" claim. |
| [Beyond Static Sandboxing](https://arxiv.org/abs/2604.11839) | Learned capability governance for autonomous agents and capability overprovisioning. | Blocks a broad "capability governance" claim unless we narrow the object. |
| [MCP-Style Runtime Security Invariants](https://arxiv.org/abs/2606.29073) | Makes execution-layer invariants explicit for MCP-style runtimes. | Very close for runtime invariants; we need a semantic-authority angle, not only execution control. |
| [Formal Security Analysis of Agent Protocol Composition](https://arxiv.org/abs/2606.28690) | Formalizes cross-protocol security obligations, including content-to-authority flow, semantic-to-authority isolation, authority monotonicity, bridge capability contracts, and replayable counterexamples. | The hardest close neighbor. It blocks a broad "authority flow across protocols" novelty claim. Our claim must be at agent-step/action-field warrant level, not protocol-bridge model checking. |
| [MCP Security Best Practices](https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices) | Official best practices around consent, permissions, tool safety, and confused-deputy risks. | Confirms the deployment pain, but also means "MCP needs permissions" is not novel. |

## Pain Point That Still Looks Under-Covered

Modern agents flatten many authority sources into one reasoning substrate:

- user requests
- system/developer instructions
- skill instructions
- skill scripts and resources
- tool and MCP descriptions
- retrieved evidence
- memories
- tool outputs
- approval dialogs
- prior plan steps

Existing defenses usually ask one of these:

1. Is the artifact malicious?
2. Is the skill/tool allowed?
3. Is the selected tool over-privileged?
4. Is the tool call unsafe?
5. Did a source influence the output?
6. Is the answer faithful to context?

The uncovered pain point is different:

> Which authority source was consumed to justify this step, and was that source valid for this exact field, operation, data flow, side effect, and delegation chain?

This is a semantic authority problem, not just a permission problem. An agent can pass permission checks and still be wrong because it consumes the right source in the wrong role.

## Strongest Innovation Candidate

### Name

Action-Field Authority Warrant, Semantic Capability Warrant, or Capability Warrant.

### Thesis

Agent actions should execute only when every protected step field carries a proof that the authority source consumed for that field is valid for the current role, operation, data scope, side effect, and delegation chain.

### Core Mechanism

```text
Authority source:
  x in {user, system, skill, tool, evidence, memory, approval, prior_step}

Capability:
  Cap(x) = (role, fields, operations, data_scope, effect_scope,
            time_scope, delegation_scope, provenance, obligations)

Step requirement:
  Need(s) = (role_needed, field, operation, data_access,
             side_effect, delegation, risk_level)

Valid consumption:
  Consume(x -> s) is valid iff Cap(x) covers Need(s)

Capability laundering:
  x influences or justifies s, but Cap(x) does not cover Need(s)
```

The key is that the same source may be valid in one role and invalid in another:

- A policy document may support simulation routing, but not approval waiver.
- A skill may guide report formatting, but not authorize file deletion.
- A tool description may define parameters, but not become a user approval.
- A memory item may personalize style, but not change risk policy.
- A prior successful step may justify using an output file, but not expanding filesystem scope.

## Why This Is More Novel Than "Skill Permission"

SkillGuard, SkillFortify, proof-carrying skill work, ToolPrivBench, ToolSafe, and MCP runtime work mostly focus on resource permission, unsafe invocation, privilege level, artifact inspection, capability containment, or execution invariants.

Our proposed object is narrower and different:

> Runtime field-level authority consumption: the proof that a specific step field consumed the right source in the right semantic role.

This lets us claim:

1. Not all influence is bad. Legitimate influence should pass.
2. Not all permission is sufficient. An allowed tool call can still be unjustified.
3. Not all trusted sources are universally authoritative. Trust is scoped by role.
4. The same source can be valid for one field and invalid for another.
5. Cross-step and cross-plane transformations can launder authority.

## Candidate Research Ideas

### Idea 1: Action-Field Authority Warrant

Method:

1. Label each context object with authority role and scoped capability.
2. Decompose each action/tool call into protected fields such as decision, tool, parameters, data read, data write, side effect, risk level, approval, and report.
3. Require each protected field to emit a warrant showing which capabilities it consumed.
4. Verify that consumed capabilities cover that exact field requirement.
5. Reject steps where evidence, skill text, tool metadata, memory, approval, or prior-step output is consumed outside field scope.

Novelty: high.

Reason: closest work governs tool/skill permissions or protocol bridge invariants, but not the semantic provenance of why a specific action field is authorized.

Risk: medium. Need to avoid sounding like a renamed permission system.

Best paper claim:

> We introduce action-field authority warrants, a proof-carrying representation for detecting capability laundering across evidence, skills, tools, memories, approvals, and prior steps.

### Idea 2: Same-Source Different-Consumption Benchmark

Method:

1. Build paired cases where the same artifact is used legally in one role and illegally in another.
2. Cover evidence, skill, tool description, memory, and approval sources.
3. Score whether a guard preserves legal consumption while blocking laundering.

Novelty: medium-high.

Reason: Most benchmarks compare clean vs malicious artifacts. This benchmark tests role-scoped consumption.

Risk: can look synthetic unless tied to real agent traces.

Best paper claim:

> Existing detectors overblock benign influence or underblock allowed-but-unwarranted actions; paired same-source cases expose this blind spot.

### Idea 3: Cross-Plane Capability Laundering

Method:

1. Model agent execution as authority planes: instruction, evidence, skill, tool, memory, approval.
2. Detect illegal transitions such as evidence-to-instruction, skill-to-approval, tool-metadata-to-policy, memory-to-permission.
3. Build a runtime checker that validates authority-flow transitions.

Novelty: high if framed as a type system / flow semantics.

Risk: now medium, not high, because protocol-composition work already covers content-to-authority flow and semantic-to-authority isolation at the bridge/protocol layer. This idea only remains novel if grounded in per-action-field warrants rather than protocol invariants.

Best paper claim:

> The dangerous failure is not just malicious content, but illegal promotion of data-plane authority into control-plane authority.

### Idea 4: Counterfactual Capability Auditor

Method:

1. Use perturbations or ablations to infer which source actually justified an action field.
2. Compare inferred consumed authority against declared warrants.
3. Flag hidden laundering when the declared warrant and causal source diverge.

Novelty: medium.

Reason: connects WarrantGuard with attribution, but makes attribution subordinate to warrant validity.

Risk: causal attribution may be noisy and expensive.

Best paper claim:

> Attribution is not the decision; attribution reveals consumed authority, and warrants decide whether that consumption is valid.

### Idea 5: Skill Warrant Compiler

Method:

1. Compile skill files into capability manifests.
2. Attach runtime monitors to enforce allowed tools, files, network, and side effects.
3. Extend manifests with semantic roles such as formatting, analysis, evidence interpretation, approval, execution.

Novelty: low-medium.

Reason: SkillGuard, SkillFortify, and proof-carrying skill artifacts are too close.

Risk: likely rejected as another skill permission framework unless paired with action-field authority consumption.

Status: do not use as main contribution. At most use it as a baseline or as one input source whose declared capability can be consumed or laundered by later action fields.

## Claim Firewall After Novelty Pressure

Do not claim:

- first skill security framework
- first skill permission framework
- first proof-carrying skill method
- first capability governance method
- first MCP runtime invariant system
- first content-to-authority flow formalism
- first least-privilege tool-use benchmark
- first step-level tool safety guard

Potentially safe claim:

> First, or at least sharply differentiated, action-field authority warrant for detecting whether a concrete agent step consumed the correct authority source for each protected field.

The novelty hinges on three constraints:

1. **Field-level, not artifact-level.** The question is not whether a skill/tool/evidence source is safe. It is whether a specific protected field consumed it in scope.
2. **Semantic role, not only resource permission.** The question is not whether the tool can read/write. It is whether the source can act as evidence, instruction, approval, policy, parameter support, or side-effect authorization.
3. **Same-source contrast.** The same source must pass in a legal consumption role and fail in an illegal one. This avoids binary malicious/benign framing.

If any of these three constraints are removed, the idea collapses into SkillGuard, proof-carrying skill verification, MCP runtime/protocol-composition invariants, or ToolPrivBench.

## Recommendation

The strongest paper story is not "Capability Warrant is a unified framework." That is too broad.

The strongest story is:

> Agents launder authority across sources and roles at the level of concrete action fields. Capability Warrant is a proof-carrying mechanism that verifies how each protected field consumes evidence, skill, tool, memory, approval, and prior-step authority.

Recommended title:

**Action-Field Authority Warrants: Detecting Capability Laundering in Skill- and Retrieval-Driven Agents**

Alternative title:

**Capability Warrant: Proof-Carrying Field Authority for Agentic AI**

Recommended contribution stack:

1. **Threat model: capability laundering.** Trusted or authorized sources are consumed outside their valid role, field, operation, data scope, side effect, or delegation scope.
2. **Representation: action-field authority warrant.** Each protected field emits a proof-carrying record of consumed authority sources and required capabilities.
3. **Verifier: CapGuard.** A runtime verifier checks valid consumption, preserving legitimate influence while rejecting laundering.
4. **Benchmark: same-source paired cases.** Legal and illegal consumptions share the same source artifact, forcing systems to reason about role-scoped authority rather than binary trust.

## Main Reviewer Objections and Answers

| Objection | Answer |
|---|---|
| This is just access control. | Access control asks whether the actor/tool has permission. Action-field authority warrants ask whether the consumed justification source is valid for this exact semantic role. |
| This is just SkillGuard or proof-carrying skills. | Those works govern skill permissions, skill effects, or capability containment of the skill artifact. We target how later agent action fields consume authority from skills plus evidence, memory, approvals, tool metadata, and prior steps. |
| This is just ToolPrivBench. | ToolPrivBench asks whether a lower-privilege tool suffices. We ask whether the reason for invoking even an allowed tool is authorized by the source that justified it. |
| This is just prompt injection. | Prompt injection is one way to create illegal authority flow. The broader failure includes benign or trusted sources consumed outside role. |
| This is too abstract. | Same-source paired cases make it concrete: the exact same artifact must pass in one consumption role and fail in another. |
| This is hand-designed policy. | The contribution is the action-field warrant object and proof obligation. Domain predicates instantiate scope, similar to type rules or capability systems. |

## Killer Experiment Shape

Create paired rows:

```text
same source x, two consumptions:

Case A:
  x used within Cap(x) -> should pass

Case B:
  x used outside Cap(x) -> should fail
```

Example rows:

| Source | Legal consumption | Laundered consumption |
|---|---|---|
| signed policy evidence | route to required simulation | lower risk level or waive approval |
| report-writing skill | format report sections | read secrets or delete logs |
| tool description | select valid parameter names | authorize higher-risk operation |
| memory | personalize wording | change safety policy |
| user approval | approve draft generation | send email or upload file |
| prior step output | reuse generated artifact | expand filesystem/network scope |

Metrics:

- legal-preservation rate
- laundering-block rate
- same-source contrast gap
- false block on legitimate authority flow
- false allow on out-of-scope authority flow

## Decision

Do not pitch the next paper as "RAG plus Skill plus Tool." That sounds like scope creep.

Pitch it as one new object:

> Proof-carrying action-field authority consumption.

WarrantGuard then becomes the RAG slice of a larger action-field authority framework. Skill safety is not a separate branch; it is a new authority source inside the same laundering model.
