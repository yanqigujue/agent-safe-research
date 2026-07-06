# Agent Action Invariance: Access-Control And Zero-Trust Deep Dive

Date: 2026-07-01

Purpose:

This note explores whether traditional access-control and zero-trust models can
be fused with AFW / CapGuard:

- RBAC;
- ABAC;
- UCON / usage control;
- ReBAC / relationship-based access control;
- NGAC / policy machine;
- Zero Trust Architecture;
- policy-as-code / OPA / Rego;
- separation of duty and least privilege.

The main conclusion:

```text
Traditional access control asks whether a subject may perform an action on an
object.

AFW asks whether a source consumed by an action field has authority to govern
that field.
```

So the best use is not to claim a new access-control model. The best use is to
adapt mature authorization vocabulary to a new boundary:

```text
source -> protected action field
```

## 1. Access Control Is Necessary But Not Sufficient

Standard access control:

```text
Can agent A call tool T with operation op on object o?
```

AFW:

```text
Can source x authorize field f inside the proposed action?
```

Example:

```text
The agent may have permission to call dispatch_work_order.
But the retrieved report may not have authority to set side_effect=dispatch.
```

This gives the key firewall sentence:

> Tool permission is a precondition. Field authority is a separate source-to-field check.

## 2. RBAC: Roles Are Useful, But The Subject Is Wrong

RBAC assigns permissions to roles and users to roles.

AFW can reuse the role vocabulary:

```text
dispatch_operation_authority
risk_assessment_authority
publish_approval_authority
report_formatting_authority
data_scope_authority
```

But the subject is not only the agent:

```text
RBAC subject:
  user / process / service account

AFW authority subject:
  source consumed by a field
```

This prevents a common mistake:

```text
Agent has DispatchRole, therefore any retrieved text can trigger dispatch.
```

AFW says:

```text
Agent may execute dispatch only if the dispatch field is backed by a source
whose role covers dispatch_operation_authority.
```

Best use:

- role taxonomy;
- role hierarchy;
- separation of duty;
- no role amplification.

Candidate property:

```text
Source-Role Separation:
  execution role of the agent does not imply authority role of the source.
```

Useful source:

- NIST RBAC Library. <https://csrc.nist.gov/projects/role-based-access-control>

## 3. ABAC: Cap(x) Is Attribute-Based Authority

ABAC decides access from attributes of:

```text
subject, object, action, environment.
```

AFW can be seen as ABAC over:

```text
source attributes:
  source_type, issuer, role, trust_level, freshness, manifest, delegation flag

field attributes:
  field_name, operation, effect_scope, data_scope, risk_level

environment attributes:
  time_epoch, policy_epoch, active counter-authority, obligation status

consumption attributes:
  source_id, field_id, use_type, trace edge, causal driver if available
```

ABAC mapping:

| ABAC component | AFW component |
|---|---|
| subject attributes | source capability attributes |
| object attributes | action-field attributes |
| action attributes | operation/effect requested by the field |
| environment attributes | time scope, policy epoch, obligations, counter-authority |
| policy | `Cap(x) covers Need(s,f)` |

This supports a paper claim:

```text
AFW is an ABAC-style policy over source-to-field consumption, not only over
agent-to-tool execution.
```

New metric:

```text
attribute_coverage_rate =
  # required Need attributes present in source capabilities / # required Need attributes
```

Useful source:

- NIST SP 800-162, "Guide to Attribute Based Access Control".
  <https://csrc.nist.gov/pubs/sp/800/162/upd2/final>

## 4. UCON: The Strongest Fit

Usage control (UCON) extends access control with:

- authorizations;
- obligations;
- conditions;
- continuity;
- mutability of attributes during use.

This is extremely close to CapGuard's new direction.

AFW mapping:

| UCON idea | AFW use |
|---|---|
| authorization | `Cap(x)` covers `Need(s,f)` |
| obligation | `requires_static_scan`, `requires_dlp_scan`, approval receipts |
| condition | time scope, policy epoch, active hold, environment state |
| ongoing control | re-check authority across multi-step traces |
| mutability | memory/approval/policy state changes after initial proposal |
| usage session | agent task or tool-call lifecycle |

UCON is the best theory for:

```text
temporal authority decay
obligation-carrying warrants
continuous field supervision
policy epoch changes
approval revocation
```

Candidate property:

```text
Continuous Field Authorization:
  for any protected field f whose execution spans multiple steps,
  ValidAuthority(s,f) must hold at proposal, repair, and execution time,
  unless the field is routed to human review.
```

New metrics:

```text
pre_authorization_pass_rate
ongoing_authorization_preservation
revocation_response_rate
obligation_mutation_detection_rate
```

Best paper sentence:

> CapGuard can be interpreted as usage control for agent action fields: authority is checked not only before an action is proposed, but across the source, obligation, and policy state that the field consumes.

Useful source:

- Park and Sandhu, "The UCONABC Usage Control Model".
  <https://doi.org/10.1145/775412.775414>

## 5. ReBAC: Relationship Authority In Multi-Agent And Skill Systems

Relationship-Based Access Control (ReBAC) grants access based on graph
relationships.

Agent systems naturally form graphs:

```text
user -> approval -> task
skill -> output -> field
memory -> prior step -> action
tool metadata -> tool call -> effect
subagent -> delegated task -> final action
```

AFW relationship examples:

```text
issued_by(approval, manager)
delegated_to(skill_output, agent)
derived_from(prior_output, approval)
revoked_by(policy_hold, policy_engine)
discharges(scan_event, obligation)
```

Candidate property:

```text
Relationship-Bounded Delegation:
  a source may authorize field f only if there exists an allowed relationship
  path from an authority issuer to the consumed source, and every edge preserves
  role/scope/time/obligation constraints.
```

This is a good fit for multi-agent and skill-driven agents.

Useful source:

- Fong, "Relationship-Based Access Control: Protection Model and Policy
  Language". <https://doi.org/10.1145/2046707.2046771>

## 6. NGAC / Policy Machine: Source-Field Policy Graphs

NIST's Next Generation Access Control / Policy Machine represents access
decisions through a graph of users, objects, attributes, operations, and policy
classes.

AFW can borrow the graph idea:

```text
source nodes
source attribute nodes
field nodes
field attribute nodes
operation/effect nodes
obligation nodes
policy epoch nodes
counter-authority nodes
```

Decision:

```text
field f is allowed if graph reachability from source x to f satisfies all
required policy paths and no counter-authority path defeats it.
```

Potential system direction:

```text
Authority Policy Graph

Compile manifests and trace events into a small policy graph.
Answer each Need(s,f) by graph reachability + obligation checks.
```

Why useful:

- natural explanation for witness extraction;
- supports graph compression;
- supports counter-authority as negative paths;
- supports audit visualization.

Risk:

- May look like generic policy graph unless tied tightly to source-to-field
  consumption and action invariance.

Useful source:

- NIST SP 800-178, "A Comparison of Attribute Based Access Control Standards
  for Data Service Applications". <https://csrc.nist.gov/pubs/sp/800/178/final>
- NIST NGAC project. <https://csrc.nist.gov/projects/next-generation-access-control>

## 7. Zero Trust: Never Trust Source Context By Default

Zero Trust Architecture (ZTA) says access decisions should be dynamic,
contextual, and continuously evaluated.

AFW maps very naturally:

```text
never trust retrieved content, memory, skill output, or prior-step output as
authority by default
```

Zero-trust principles for AFW:

1. Every protected field must have explicit authority.
2. Authority is scoped to role, field, operation, data, effect, delegation,
   time, and obligations.
3. Authority is continuously rechecked when policy, memory, approval, or
   obligation state changes.
4. Least privilege applies to sources, not only tools.
5. Decisions produce audit evidence.

Candidate property:

```text
Source Zero Trust:
  absent a manifest-lifted or explicitly declared capability, no source is
  trusted to authorize protected fields.
```

Useful source:

- NIST SP 800-207, "Zero Trust Architecture".
  <https://csrc.nist.gov/pubs/sp/800/207/final>

## 8. Policy-As-Code / OPA / Rego: Executable Need-Coverage Rules

OPA/Rego and policy-as-code systems are practical rather than primarily
theoretical, but they are useful for a reviewer-facing implementation story.

AFW policy can be expressed as:

```text
allow[field] if
  source.capabilities[_].role covers field.need.role
  source.capabilities[_].scope covers field.need.scope
  source.capabilities[_].time covers current_epoch
  all obligations are discharged
  no counter-authority applies
```

Potential contribution:

```text
AFW policy compilation:
  Cap(x), Need(s,f), obligations, and counter-authority facts can be compiled
  into a policy-as-code rule set.
```

Claim boundary:

- Do not claim first policy-as-code for agents.
- Safe claim: field-level authority witnesses can be exported to policy-as-code
  facts/rules for deployment.

Useful source:

- Open Policy Agent documentation. <https://www.openpolicyagent.org/docs/latest/>

## 9. Separation Of Duty And Toxic Combinations

Separation of duty prevents one actor or role from completing conflicting
steps.

AFW analogue:

```text
same source should not both create a high-risk recommendation and approve it
unless policy explicitly allows self-approval.
```

Examples:

```text
recommend_patch and approve_patch must be separate roles
generate_report and publish_report may require different authority
detect_risk and suppress_risk_report is a toxic combination
```

New property:

```text
Source Separation Of Duty:
  a witness for field f is invalid if it contains a toxic combination of source
  roles or if the same source appears in mutually exclusive authority positions.
```

New metric:

```text
sod_violation_detection_rate =
  # toxic-combination fields blocked/abstained / # toxic-combination fields
```

This is especially useful for multi-agent workflows where one subagent writes
and approves its own output.

## 10. New Candidate Directions

### Direction A: UCON-Style Continuous Authority For Agent Fields

Method:

```text
Model each protected field as a usage session.
Check authority before proposal, during repair, and at execution.
Track obligation discharge, policy epoch, revocation, and mutable memory state.
```

Why strong:

- Directly extends current temporal decay and obligation-carrying warrants.
- Strong formal vocabulary from UCON.
- Fits long-horizon agents better than one-shot access control.

Minimum experiment:

```text
Multi-step traces where approval is valid at proposal time but revoked,
expired, or countered before execution.
```

### Direction B: Source ABAC For Protected Action Fields

Method:

```text
Define source, field, operation, effect, data, environment, and consumption
attributes.
Run ablations over which attribute families are checked.
```

Why strong:

- Very clean mapping to `Cap(x)` / `Need(s,f)`.
- Gives interpretable ablation table.

Minimum experiment:

```text
source-family-only vs role-only vs role+scope vs role+scope+time+obligation.
```

### Direction C: Relationship-Bounded Delegation For Skill Agents

Method:

```text
Represent user -> skill -> output -> action as a relationship graph.
Allow downstream field authority only along declared delegation paths.
```

Why strong:

- Best fit for skill-driven agents.
- Distinguishes direct skill permission from downstream authority.

Minimum experiment:

```text
Allowed skill execution but blocked downstream laundering into approval,
delegation, risk, or side-effect fields.
```

### Direction D: Source Separation Of Duty

Method:

```text
Define toxic source-role combinations and self-approval patterns.
Extend witness validation to reject toxic combinations.
```

Why strong:

- New failure family not fully covered by role mismatch.
- Very relevant for multi-agent workflows.

Minimum experiment:

```text
Rows where one source both recommends and approves a high-impact action.
```

### Direction E: Authority Policy Graph / NGAC Compilation

Method:

```text
Compile Cap(x), Need(s,f), obligations, counter-authority, and trace edges into
a policy graph.
Extract witnesses as minimal satisfying paths.
```

Why strong:

- Gives a clean implementation and audit visualization story.
- Could support larger-scale policy management.

Risk:

- Graph policy systems are old; novelty must remain source-to-field action
  invariance.

## 11. Updated Ranking

| Rank | Direction | Why |
|---:|---|---|
| 1 | UCON-style continuous authority | Strongest fit with temporal decay, obligations, long-horizon agents |
| 2 | Source ABAC for fields | Cleanest formalization and ablation path |
| 3 | Relationship-bounded delegation | Best skill-driven-agent extension |
| 4 | Source separation of duty | Important new failure family for multi-agent workflows |
| 5 | Authority policy graph / NGAC compilation | Good system/audit direction, more implementation-heavy |
| 6 | OPA/Rego policy export | Useful deployment story, weak novelty by itself |

## 12. Claim Firewall

Do not claim:

- first RBAC / ABAC / ReBAC / UCON / NGAC model;
- first zero-trust architecture for LLM agents;
- first policy-as-code guardrail;
- first separation-of-duty model for agents;
- first least-privilege authorization method.

Safe claim:

```text
AFW adapts mature access-control ideas to a different authorization boundary:
source-to-action-field authority consumption.
```

Best concise positioning:

> CapGuard is not a replacement for tool access control. It is a usage-control
> layer over the sources that protected action fields consume.

