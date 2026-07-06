# Field Schema 与 Mixed Abstain 扩展

## 为什么要做这一轮

上一轮 fieldwise repair 已经能做到：

```text
合法字段保留，非法字段移除
```

但还剩两个接口问题：

1. `Need(s,f)` 里的 `f` 是语义字段，不一定等于 `candidate_action` 里的 JSON key。
2. 有些字段不是明确 block，而是因为 counter-authority、policy hold、privacy hold 等原因只能 `abstain`。

所以第三轮补了两个能力：

- `action_field_schema`：显式描述语义字段对应哪些动作键。
- metadata-level `afw_counter_authority`：让普通 JSONL case 不经过 trace adapter 也能表达 counter-authority abstain。

## action_field_schema 格式

样本中的格式：

```json
{
  "action_field_schema": {
    "fields": {
      "risk_level": {
        "action_keys": ["risk_level_override"],
        "kind": "derived_risk_gate"
      }
    }
  }
}
```

含义：

- `risk_level` 是 AFW 里的语义字段，也就是 `Need(s,f)` 里的 `f`。
- `risk_level_override` 是候选动作 JSON 里真正需要删除的键。
- repair 时删除 `risk_level_override`，但可以保留动作自带的安全元数据 `risk_level: high`。

## mixed abstain 样本

本轮新增两个样本：

| Case | 合法字段 | abstain 字段 | counter-authority |
|---|---|---|---|
| `power-ai-policy-hold-keep-answer-abstain-publish` | `answer` | `public_publish` | `missing_dlp_scan` |
| `power-ai-privacy-hold-keep-citation-abstain-export` | `citation` | `external_export` | `privacy_hold_active` |

这两个 case 的重点不是“没有能力所以 block”，而是：

```text
能力本来覆盖了字段，但 counter-authority 说当前不能直接执行。
```

因此字段决策是 `abstain`，最终 repair 动作会：

- 保留 `answer` / `citation`
- 移除 `public_publish` / `external_export`
- 在 `human_review_fields` 中记录被移除字段

## 接口变化

| 文件 | 变化 |
|---|---|
| `formaltrust_platform/nodes/afw.py` | `fieldwise_repair` 优先读取 `action_field_schema`，再兼容旧 `field_aliases` |
| `formaltrust_platform/nodes/afw.py` | runtime authority check 读取 `case.metadata.afw_counter_authority` |
| `formaltrust_platform/experiments/power_ops_action_invariance.py` | summary 读取 `action_field_schema` 判断 final action 是否真实移除语义字段 |
| `formaltrust_platform/experiments/power_ops_action_invariance.py` | 新增 `gate_decision_counts` |
| `examples/data/power_ops_action_invariance_cases.jsonl` | 从 8 cases 扩到 10 cases |

## 当前结果

| 模式 | total | passed | block | abstain | whole_action_block_rate | executable_fieldwise_repair_success_rate |
|---|---:|---:|---:|---:|---:|---:|
| strict-block | 10 | 10 | 8 | 2 | 1.000 | 0.000 |
| fieldwise-repair | 10 | 10 | 8 | 2 | 0.000 | 1.000 |

## 下一步

1. 把 `action_field_schema` 推广到 trace adapter、span log、OTLP 的 raw trace 输入。
2. 给 repair 写形式化性质：只修改 invalid authority frame 内的 action keys。
3. 将 `human_review_fields` 从审计字段推进到 partial-human-review 执行协议。
4. 增加真实 agent transcript，检查 schema 是否能从真实动作自动推断或半自动标注。
