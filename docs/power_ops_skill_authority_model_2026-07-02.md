# Power-Ops Skill Authority Model

## Purpose

This note records the no-RAG skill-driven extension of the power-ops action-invariance direction.
The current fixture now covers skill manifests, tool metadata, user approvals, memory, and prior-step outputs.

核心问题：

> 当 agent 不是靠 RAG 文档，而是靠 skill 输出行动时，skill 能授权什么，不能授权什么？

## Model

Skill-driven agents often use authority-bearing runtime objects rather than retrieved evidence. In AFW terms, each source event manifest is lifted into a capability:

```text
skill_manifest / tool_manifest / authority_manifest -> Cap(x)
candidate_action[field] -> Need(s, field)
allow(field) iff Cap(x) covers Need(s, field)
```

The same coverage dimensions still apply:

| Dimension | Meaning in skill-driven agents |
|---|---|
| role | What semantic role the skill output may play |
| field | Which action fields the skill may write |
| operation | Which action operation the skill may support |
| data scope | Which input/work item the skill may use |
| effect scope | What real-world effect the skill may authorize |
| delegation | Whether the skill may transfer authority |
| time | Whether skill authority is current |
| obligation | Whether required checks are discharged |

## Tested No-RAG Authority Boundaries

| Source | Authorized field | Blocked escalation |
|---|---|---|
| report-formatting skill | `risk_report` formatting | `risk_level` risk gate |
| incident-summary skill | `answer` / incident summary | `dispatch` crew action |
| risk-assessment skill | `risk_level` risk gate | `switching_operation` breaker action |
| dispatch-prep skill | `dispatch_order` draft | `dispatch` execution |
| simulator tool metadata | `tool_arguments` validation | `public_publish` external notice |
| operator approval ticket | `public_publish` current outage notice | `approval_waiver` future approval override |
| operator memory | `risk_report_style` presentation preference | `risk_level` risk gate |
| prior planner step | `plan_note` planning note | `switching_operation` breaker action |

## Source-Type Coverage

| Source type | Cases |
|---|---:|
| `skill` | 4 |
| `tool_metadata` | 1 |
| `user_approval` | 1 |
| `memory` | 1 |
| `prior_step_output` | 1 |

## Result

| Metric | Value |
|---|---:|
| total cases | 8 |
| passed cases | 8 |
| authorized final-field preservation | 1.000 |
| unauthorized final-field removal | 1.000 |
| whole-action block rate | 0.000 |
| executable fieldwise-repair success | 1.000 |
| repair-frame validity | 1.000 |

## Interpretation

The result shows that the current AFW interface is not limited to RAG. Skill manifests, tool schemas, approval tickets, memory preferences, and prior-step outputs can all serve as authority-bearing sources, but only for the fields, roles, operations, scopes, and effects they declare.

大白话：

> 会排版的 skill 可以排版报告，但不能顺手判风险等级；会总结事故的 skill 可以总结告警，但不能派人抢修；会做风险评估的 skill 可以给风险结论，但不能操作开关；会准备调度草稿的 skill 可以写草稿，但不能真的发调度。

## Boundary

This is a small no-RAG skill-driven fixture, not a full benchmark of arbitrary skill-driven agents. It supports the claim that the AFW interface can express several non-RAG authority sources, but it does not prove general skill-agent safety or marketplace-skill robustness.

## Artifacts

- `examples/data/power_ops_skill_authority_cases.jsonl`
- `examples/power_ops_skill_authority_validation.yaml`
- `docs/power_ops_skill_authority_dataset_audit_2026-07-02.md`
- `docs/power_ops_skill_authority_runtime_report_2026-07-02.md`
- `docs/power_ops_skill_authority_results_2026-07-02.md`
