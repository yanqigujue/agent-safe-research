# 电力大模型 Action Invariance：Strict-Block vs Fieldwise-Repair 对比

## 本轮问题

用户关心的不是“防御能不能拦住危险动作”这一件事，而是：

> 在复杂 agent 任务里，严格安全监督会不会把正常行为也一起拦掉？

所以本轮把 AFW/CapGuard 从“字段级判定”推进到“最终动作级修复”：

- strict-block：只要一个字段不合法，整个 `final_action` 转人工。
- fieldwise-repair：合法字段保留，非法字段从最终动作里移除，并记录审计证据。

## 代码入口

| 组件 | 路径 | 作用 |
|---|---|---|
| CapGuard final action 模式 | `formaltrust_platform/nodes/afw.py` | 新增 `runtime_final_action_mode: fieldwise_repair` |
| Repair 配置 | `examples/power_ops_action_invariance_fieldwise_repair_validation.yaml` | 开启字段级修复 |
| 电力样本 | `examples/data/power_ops_action_invariance_cases.jsonl` | 10 个 mixed authorized/unauthorized power-op cases，其中 2 个 abstain |
| 指标生成器 | `formaltrust_platform/experiments/power_ops_action_invariance.py` | 新增最终动作级 repair 指标 |
| 回归测试 | `tests/test_power_ops_action_invariance.py` | strict-block 和 fieldwise-repair 两条路径都测 |

## 对比结果

| 指标 | Strict-block | Fieldwise-repair | 解释 |
|---|---:|---:|---|
| total_cases | 10 | 10 | 同一批电力安全样本 |
| passed_cases | 10 | 10 | 两种模式都没有 false allow |
| gate_decision_counts | block=8, abstain=2 | block=8, abstain=2 | 包含阻断和不确定/冲突授权两类场景 |
| authorized_field_preservation_rate | 1.000 | 1.000 | 字段级判定都能识别合法字段 |
| unauthorized_field_prevention_rate | 1.000 | 1.000 | 字段级判定都能阻断非法字段 |
| whole_action_block_rate | 1.000 | 0.000 | strict-block 会整体转人工，repair 不会 |
| authorized_final_field_preservation_rate | 0.000 | 1.000 | repair 模式最终动作保留了合法字段 |
| unauthorized_final_field_removal_rate | 1.000 | 1.000 | repair 模式最终动作移除了非法字段 |
| executable_fieldwise_repair_success_rate | 0.000 | 1.000 | repair 模式把“可修复”变成了真实 final action |
| repair_frame_validity_rate | 1.000 | 1.000 | repair 模式检查修复只改 invalid authority frame；strict-block 无 repair，故为 vacuous 1.000 |

## 大白话结论

以前像是：

> 这份动作里有一个危险字段，所以整份动作都别做，交给人。

现在变成：

> 这份动作里的回答、引用、格式化、调度说明这些合法部分可以保留；真正没有授权的调度、送电、越权读取、风险降级字段拿掉，并留下“为什么拿掉”的记录。

这直接回应“防御太保守”的问题。安全性没有放松，因为非法字段仍然被阻断；可用性提高了，因为合法字段不再被最终动作一起吞掉。

第四轮又补了一层检查：

> 不只要修复成功，还要证明修复没有偷偷改动合法字段、没有误删无关字段。

这个检查对应 `repair_frame_validity_rate`，当前 fieldwise-repair 的 10 个 repaired cases 全部通过。

## 当前边界

- 这是 10 个 curated power-ops regression cases，不是生产系统泛化结论。
- 当前 repair 是字段键级修复，不是完整 planner 重规划。
- `risk_level` 样本已经使用 `action_field_schema` 区分语义字段和 JSON 动作键。
- `abstain` 字段当前会被移除并列入 `human_review_fields`，但还没有完整 partial-human-review 执行协议。
- 当前已经输出 `partial_human_review_fields` 和 `auto_executable_fields`，但还没有接真实审批系统。

## 下一轮默认方向

1. 将 `action_field_schema` 和 repair validity 扩到 trace / span log / OTLP 场景。
2. 扩样本到真实 trace，避免只在手写 JSONL 上成立。
3. 接 partial-human-review 的真实审批/模拟审批协议。
4. 做文献查新和 novelty firewall。
