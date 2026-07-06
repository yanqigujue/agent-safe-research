# Fieldwise Repair Validity 与 Partial Human Review

## 本轮目标

前几轮已经证明：

```text
fieldwise repair 可以保留合法字段、移除危险字段。
```

但还需要证明一件更细的事：

```text
repair 没有偷偷改掉合法字段，也没有删错字段。
```

因此本轮新增一个可运行的 repair validity verifier，并把 partial-human-review 语义写进 `final_action`。

## 形式化对象

设原始动作是：

```text
a
```

修复后的最终动作是：

```text
a'
```

字段级授权结果给出：

```text
AllowFields(a) = { f | Cap(x) covers Need(a,f) }
InvalidFields(a) = { f | decision(f) in {block, abstain} }
```

`action_field_schema` 给出语义字段到动作 JSON key 的映射：

```text
Keys(f) = action_field_schema.fields[f].action_keys
```

没有 schema 时默认：

```text
Keys(f) = {f}
```

## Repair Validity 条件

一个 fieldwise repair 合法，当且仅当：

1. **授权字段不变：**

```text
forall f in AllowFields(a), forall k in Keys(f):
  a'[k] = a[k]
```

2. **无效字段被移除：**

```text
forall f in InvalidFields(a), forall k in Keys(f):
  k notin dom(a')
```

3. **不删无关字段：**

```text
removed_keys(a,a') subseteq union(Keys(f) for f in InvalidFields(a))
```

4. **不改无关业务字段：**

除 `decision`、`tool`、`requires_human_approval`、`rationale` 等 repair control keys 外，非 invalid frame 内的原始字段不能被改写。

5. **局部人工复核字段一致：**

```text
partial_human_review_fields = InvalidFields(a)
auto_executable_fields = AllowFields(a)
```

## 代码接口

新增 verifier：

```python
validate_fieldwise_repair_frame(metadata, metrics) -> dict
```

输出字段：

| 字段 | 含义 |
|---|---|
| `checked` | 当前 case 是否产生了 `fieldwise_repaired` final action |
| `valid` | repair 是否满足 frame validity |
| `authorized_field_mutations` | 被错误改写的授权语义字段 |
| `unexpected_removed_action_keys` | 不该删却被删的动作键 |
| `missing_removed_action_keys` | 应该删但仍保留的动作键 |
| `out_of_frame_mutations` | repair frame 外被改写的动作键 |
| `partial_human_review_fields_match` | 局部人工复核字段是否等于 invalid fields |

新增 summary 指标：

```text
repair_frame_validity_rate
```

定义：

```text
repair_frame_validity_rate =
  valid_repaired_cases / checked_repaired_cases
```

若当前模式没有产生 repair，例如 strict-block，则该指标为 vacuous 1.0，并在 `case_counts.repair_frame_checked_cases` 中显示 checked=0。

## Partial Human Review final_action

`fieldwise_repair` 现在会写：

```json
{
  "decision": "fieldwise_repaired",
  "tool": "fieldwise_repair",
  "partial_human_review_required": true,
  "partial_human_review_fields": ["public_publish"],
  "auto_executable_fields": ["answer"],
  "removed_fields": ["public_publish"],
  "removed_action_keys": ["public_publish"]
}
```

大白话：

> `answer` 可以继续自动执行，`public_publish` 不自动执行，交给人看。

这不是完整生产执行协议，但已经把“局部转人工”从一句话变成了可检查的结构化对象。

## 当前结果

在 10 个 curated power-ops cases 上：

| 模式 | checked repairs | valid repairs | repair_frame_validity_rate |
|---|---:|---:|---:|
| strict-block | 0 | 0 | 1.000 |
| fieldwise-repair | 10 | 10 | 1.000 |

同时 fieldwise-repair 保持：

```text
whole_action_block_rate = 0.000
executable_fieldwise_repair_success_rate = 1.000
```

## 当前边界

- verifier 依赖 `original_action`，真实 agent trace 中也必须保留原始动作。
- 当前 `partial_human_review_fields` 只标识字段，不负责调用真实审批系统。
- 当前 theorem 是 frame-level safety property，不证明修复后的动作在任意业务系统中都可执行。
- 后续要把 verifier 接到 trace/span/OTLP 派生的动作上，并检查 schema 自动生成质量。
