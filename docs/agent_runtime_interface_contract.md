# Agent Runtime Interface Contract

日期：2026-07-08

这份文档定义 FormalTrust 如何接入不同 Agent 的运行时元素。它不是某一个框架的适配器文档，而是平台级稳定合约。目标是让 Codex-like skills、MCP tools、LangGraph nodes、AutoGen tools、CrewAI agents、浏览器/终端工具、记忆系统、审批和子代理都能映射到同一套接口。

## 1. 设计原则

1. 不扩展 `FormalTrustState` 顶层字段。  
   Agent 对象进入 `case.metadata`、`metrics` 或 `artifacts`。

2. 少量稳定核心，避免每个名词一个类。  
   平台只定义 runtime、component、authority、action、trace event。

3. 框架差异放进 `payload` 和 `metadata`。  
   例如 MCP server 名称、LangGraph node id、Codex skill 路径、AutoGen role 都不要变成顶层字段。

4. 推荐词表不是硬枚举。  
   `kind`、`event_type`、`source_type` 都是字符串。平台提供 canonical names，但未知框架事件仍可导入。

5. 接口版本化。  
   当前版本是 `agent-runtime-interface/v1`。破坏性变更必须升版本。

## 2. 核心模型

代码入口：`formaltrust_platform.agent_interfaces`

| 模型 | 用途 | 推荐存储位置 |
|---|---|---|
| `AgentRuntimeTrace` | 一次 Agent 运行的完整 envelope | `case.metadata.agent_runtime_trace` 或 artifact |
| `AgentRuntimeDescriptor` | Agent 身份、框架、组件列表 | `runtime` |
| `AgentComponentDescriptor` | 统一描述 model、skill、tool、memory、subagent 等 | `components[]` |
| `AgentAuthorityGrant` | 来源携带的语义权限、作用域、义务、反权限 | `authorities[]` 或 event.authority |
| `AgentAction` | 候选动作或最终动作 | `metrics.candidate_action` / `metrics.final_action` |
| `AgentAuthorityConsumption` | 动作字段消费哪个来源权限 | `action.consumptions[]` |
| `AgentTraceEvent` | 规范化 trace event | `events[]` |

## 3. Component 统一描述

不要为 skill、tool、memory、planner、subagent 分别做独立平台接口。统一使用：

```json
{
  "component_id": "skill.report_formatter",
  "kind": "skill",
  "name": "Report formatter",
  "provider": "codex-like",
  "version": "1.0",
  "input_contract": {},
  "output_contract": {},
  "authority": {
    "source_id": "skill.report_formatter",
    "source_type": "skill",
    "semantic_roles": ["risk_report_formatting_authority"],
    "fields": ["risk_report"],
    "operations": ["format_report"],
    "data_scope": ["current_case"],
    "effect_scope": ["report_draft"]
  },
  "side_effects": [],
  "requires_approval": false,
  "payload": {
    "skill_path": "skills/report_formatter/SKILL.md"
  }
}
```

推荐 `kind`：

`model`, `planner`, `retriever`, `skill`, `tool`, `memory`, `approval`, `guardrail`, `evaluator`, `subagent`, `runtime`, `custom`

如果接入框架出现新 kind，先用字符串表达，不要马上改 schema。例如 `kind: "langgraph_node"` 是合法的。

## 4. Authority Grant

所有来源都用同一个权限对象表达：

```json
{
  "source_id": "approval.q3.publish",
  "source_type": "user_approval",
  "semantic_roles": ["publication_approval_authority"],
  "fields": ["side_effect", "requires_human_approval"],
  "operations": ["publish_notice"],
  "data_scope": ["q3_report"],
  "effect_scope": ["public_notice"],
  "delegation_scope": ["public_comms"],
  "time_scope": {
    "valid_until": "2026-09-30"
  },
  "obligations": ["keep_audit_log"]
}
```

同一个结构可表示：

- evidence authority
- skill output authority
- tool metadata authority
- memory authority
- user approval
- prior-step output
- delegated subagent authority

## 5. Action 和字段消费

Agent 动作保持和现有 EAIR/AFW 兼容：

```json
{
  "action_id": "action-1",
  "decision": "direct_execute",
  "tool": "dispatch_console",
  "risk_level": "high",
  "requires_human_approval": false,
  "supporting_claims": ["skill.report_formatter"],
  "rationale": "The report formatter was incorrectly treated as dispatch approval.",
  "consumptions": [
    {
      "field": "side_effect",
      "operation": "dispatch_work_order",
      "attributed_source_id": "skill.report_formatter",
      "required_role": "dispatch_operation_authority",
      "effect_scope": "maintenance_dispatch"
    }
  ]
}
```

推荐受保护字段：

`decision`, `tool`, `tool_arguments`, `parameters`, `requires_human_approval`, `risk_level`, `risk_report`, `data_scope`, `side_effect`, `delegation`, `rationale`

## 6. Trace Event

所有框架日志先映射到 `AgentTraceEvent`：

```json
{
  "event_id": "evt-2",
  "event_type": "action.candidate",
  "agent_id": "codex-like-power-agent",
  "span_id": "span-action-1",
  "parent_span_id": "span-skill-1",
  "component_id": "tool.dispatch_console",
  "action": {
    "decision": "direct_execute",
    "tool": "dispatch_console",
    "requires_human_approval": false
  },
  "payload": {
    "raw_event_name": "agent.action.proposed"
  }
}
```

推荐事件名：

`agent.started`, `agent.finished`, `model.called`, `plan.created`, `plan.step.selected`, `retrieval.performed`, `skill.discovered`, `skill.selected`, `skill.invoked`, `skill.output`, `tool.selected`, `tool.called`, `tool.result`, `memory.read`, `memory.write`, `approval.requested`, `approval.granted`, `approval.denied`, `delegation.created`, `subagent.spawned`, `action.candidate`, `action.final`, `authority.granted`, `authority.consumed`, `authority.counter`, `error`, `custom`

未知事件名允许导入。适配器应保留原始事件到 `payload.raw` 或 artifact。

## 7. 与现有 AFW 的兼容

当前 `custom.afw_trace_adapter` 已经使用：

- `case.metadata.agent_trace_events`
- `metrics.agent_trace_events`
- `metrics.candidate_action`
- `metrics.afw_source_events`
- `metrics.afw_consumptions`

新接口不替换这些字段，而是给它们一个稳定上层合约：

| 新接口对象 | 现有 AFW 字段 |
|---|---|
| `AgentTraceEvent` | `agent_trace_events` |
| `AgentAction` | `candidate_action` / `final_action` |
| `AgentAuthorityGrant` | `authority_manifest`, `skill_manifest`, `tool_manifest` 归一后的能力 |
| `AgentAuthorityConsumption` | `afw_consumptions` |

因此现有 YAML、测试和运行报告不需要迁移。

## 8. 新 Agent 框架接入流程

1. 写一个 adapter，把原始日志转换为 `AgentRuntimeTrace`。
2. 把框架对象映射为 `AgentComponentDescriptor`。
3. 把权限、审批、工具 schema、memory scope 映射为 `AgentAuthorityGrant`。
4. 把候选动作映射为 `AgentAction`。
5. 把字段级来源消费映射为 `AgentAuthorityConsumption`。
6. 将大体量原始日志写入 artifact，只在 event `payload` 里保留摘要和引用。
7. 通过 `/api/agent-interfaces` 读取当前 schema，避免 adapter 和平台字段漂移。

## 9. 稳定性规则

- 可以增加 canonical 推荐词，但不能让旧字符串非法。
- 可以给模型新增可选字段，但不要改已有字段语义。
- 框架专有字段优先进 `payload`，不要新增顶层字段。
- 只有当某类对象不能被 component、event、action、authority 表达时，才考虑新增核心模型。
- `agent-runtime-interface/v1` 的破坏性变更必须新开版本。

