# AFW V3：创新点与统一框架叙事

日期：2026-07-01

## 一句话

我们的创新点不是“再做一个 Agent 安全 guard”，而是提出一个更细的安全对象：

> **动作字段级语义授权凭证**：每个受保护 action field 都必须证明，它消费的来源具备该字段所需的语义授权角色。

更短的论文口号：

> Agents need warrants, not just permissions.

## 真正痛点

现代 Agent 会把很多异质来源压进同一个上下文：

- RAG 文档；
- skill 输出；
- tool / MCP schema；
- memory；
- user approval；
- prior-step output；
- system / developer / user instruction。

现有很多方法会检查来源、权限、工具、参数、协议或引用是否正确。但它们常常没有单独检查：

> 这个来源是否有资格支撑这个具体字段？

所以会出现一种更隐蔽的问题：

```text
来源是可信的；
边界也是正确的；
permission / attribution / scope 都可能通过；
但来源被消费成了错误的语义角色。
```

这就是 **semantic-role laundering**，也就是语义角色洗白。

## 最强创新点

### 1. Boundary-Preserving Role Mismatch

最关键的创新不是“越权访问”，而是：

> 边界没错，角色错了。

例子：

```text
report-formatting skill
  -> 可以写 risk report 的格式化文本
  -> 不能变成 risk-assessment authority
```

这使 AFW 和普通 scope / consent / permission guard 区分开来。即使 field、operation、data scope、effect scope、delegation scope 都匹配，来源仍然可能缺少字段要求的 semantic role。

### 2. Trace-Derived Authority Confusion

为了避免“你只是手写攻击样例”的质疑，现在我们有一个 seed generator：

```text
legal trace event + role_confusion spec
  -> boundary-preserving semantic-role mutation
```

当前生成样例：

```text
TRACE-SKILL-REPORT-RISK-LAUNDER::risk_assessment_from_formatting
```

它保持这些边界不变：

- field；
- operation；
- attributed source；
- data scope；
- effect scope。

只改变：

```text
required_role: report_formatting_skill -> risk_assessment_authority
```

结果是：

- CapGuard / AFW 阻断；
- boundary-scope-only 误放行；
- field-attribution-only 误放行；
- skill-permission-style 误放行。

这让 benchmark 从纯手写行集，开始变成 trace-derived 对照生成。

### 3. Minimal Authority Witness

AFW 现在不只输出 allow / block，还可以输出最小授权见证：

```text
min X_f such that X_f covers Need(s, f)
```

也就是说，对于一个字段，我们给出：

- 最小需要哪些 capability；
- 每个 capability 覆盖哪个 required role；
- 哪些 role 缺失；
- 从见证 capability 继承了哪些 obligations。

这让 AFW 从“分类器”变成一个可审计的 proof object。

现在这个 witness 还可以量化审计压缩：

```text
full_context_capability_count
witness_capability_count
irrelevant_capability_count
compression_ratio
```

一个回归样例中，完整上下文有 3 个 capability，但最小 witness 只需要 2 个 capability，因此压缩率是 `1/3`。这让 “minimal witness” 不只是解释输出，而是可以进入实验表的审计成本指标。

例子：

```text
user approval + policy evidence
  -> 可以共同授权 local draft
  -> 不能自动推出 external publish
```

legal field 的 witness 是两个 capability；laundered field 的 witness 是空，并明确报告缺失 external publish approval 和 external publish policy。

### 4. Authority Type Inference Seed

AFW 最大的部署假设是：

> `Cap(x)` 从哪里来？

现在我们有一个最小可运行答案：从 skill manifest 和 trace metadata 中 lift 出 source capability。

```text
skill_manifest.output_semantic_roles
skill_manifest.allowed_fields
skill_manifest.allowed_operations
skill_manifest.allowed_data_scope
skill_manifest.allowed_effect_scope
skill_manifest.allowed_delegation_scope
skill_manifest.output_obligations
  -> Cap(skill_output)
```

这不是声称“自动理解所有权限”，而是一个保守的 manifest-lift：

- manifest 明确声明 output semantic roles 才推断；
- 没有声明就不猜；
- trace adapter 在缺少显式 `capability` 时可以自动 fallback 到这个推断。

这让统一框架更像可部署系统：`Cap(x)` 不必永远手写，至少可以从 skill-driven agent 的 manifest 和执行 trace 中产生。

进一步地，adapter 现在也支持通用 `authority_manifest`：

```text
authority_manifest.semantic_roles
authority_manifest.fields
authority_manifest.operations
authority_manifest.data_scope
authority_manifest.effect_scope
authority_manifest.delegation_scope
authority_manifest.obligations
  -> Cap(source)
```

这让 user approval、tool metadata、memory、prior-step output 等来源可以共享同一个 manifest-lift 接口。当前 seed 已经包含一个 user approval trace：用户只批准 local draft，不能被洗成 external publish。

### 5. Obligation-Carrying Warrants

另一个可以支撑 skill 安全方向的创新点是：

> 来源不只携带 role 和 scope，还携带 obligations。

比如一个 repository-writing skill output 可能有：

```text
semantic_role = repository_write_authority
obligation = requires_static_scan
```

这意味着即使 role、field、operation、data scope、effect scope 全都匹配，如果下游字段没有声明这个 obligation 已经被 carried 或 discharged，CapGuard 仍然应该阻断。

当前规则：

```text
if row.enforce_obligations
and inherited obligation o is not satisfied under its mode
then block
```

现在支持两类 mode：

```text
must_discharge:
  必须出现在 discharged_obligations

may_carry_forward:
  可以出现在 carried_obligations 或 discharged_obligations
```

这让 AFW 比普通 permission / scope guard 更进一步：不只是“能不能做”，还要看“带着什么条件做”，以及这个条件是必须当前完成，还是可以传给下游继续检查。

### 6. Temporal Authority Decay

这一轮补上的机制是：授权不只要 role / scope 匹配，还要在有效时间或策略 epoch 内有效。

```text
Cap(x).time_scope must cover Need(s, f).time_scope
```

当前两个最小样例是：

```text
TEMPORAL-APPROVAL-EXPIRED:
  Q3 publish approval -> 不能复用成 Q4 publish authority

TEMPORAL-MEMORY-PREFERENCE-STALE:
  epoch-7 memory preference -> 不能静默复用到 epoch 8
```

这个点不要单独拔高成主创新。更稳的说法是：它是 AFW coverage 维度之一，用来封住“旧 approval / 旧 memory / 旧 policy 仍被当成当前授权”的漏洞。

## 统一框架

AFW 的统一性来自一个共同接口：

```text
Cap(x)      = 来源 x 的语义角色与作用域能力
Need(s, f)  = 步骤 s 中字段 f 的授权需求

Valid consumption:
  Consume(x -> f, s) iff Cap(x) covers Need(s, f)
```

不同 Agent 范式都可以接入：

| 来源 | AFW 中的角色 |
|---|---|
| RAG 文档 | evidence capability |
| skill 输出 | skill-output capability |
| tool metadata | schema / parameter capability |
| memory | preference / history capability |
| user approval | effect-scoped approval capability |
| prior-step output | derived artifact capability |

所以这个框架不限于 RAG。对 skill-driven agent 也成立，因为 skill 输出本身会成为后续 action fields 的来源。

## 和近邻工作的边界

| 近邻 | 它主要管什么 | AFW 的差异 |
|---|---|---|
| SkillGuard | skill 能做什么、能注入什么 | AFW 管 skill 输出后来被哪个字段消费 |
| AuthGraph | 参数来源和授权图是否一致 | AFW 聚焦非参数 protected fields 的 semantic-role validity |
| PCAA | action certificate / runtime governance | AFW 可作为 certificate 内部的 field-level payload semantics |
| IGAC | intent certificate 和 tool authorization | AFW 不证明 intent 一致，而是证明字段消费的来源有对应语义角色 |
| Cordon | side effect transaction lifecycle | AFW 问哪个来源授权了 side-effect field |
| RAG attribution | 输出是否引用了来源 | AFW 问来源有没有资格管这个字段 |

安全表述：

> AFW 不是更通用的 authorization framework，而是 protected action fields 上的 semantic-role witness layer。

## 当前证据

已实现：

- 40 行 V2 deterministic seed benchmark；
- 22 个 trace scenario seeds，其中 20 个来自电力运维 RAG 场景；
- 41 个 trace-derived authority-confusion generated rows；
- skill-manifest 和 generic authority-manifest inference seeds；
- 2 个 obligation-discharge rows；
- 2 个 temporal authority-decay rows；
- 32 个电力设备运维 RAG paired rows；
- 40 个电力设备运维 trace-derived authority-confusion rows；
- faithful-style baselines：
  - permission-only；
  - attribution-only；
  - boundary-scope-only；
  - field-attribution-only；
  - AuthGraph-style parameter provenance；
  - skill-permission-style；
  - strict-block；
- minimal authority witness extraction；
- FormalTrust built-in guardrail node wrapper：`guardrail.afw_capguard`；
- power-ops Markdown/JSON result report helper；
- power-ops plausibility audit sheet：40 条 generated rows 已完成自动结构预检，等待人工填写；
- manifest-lifted `Cap(x)` inference；
- obligation discharge enforcement；
- time-scope coverage；
- counter-authority abstain；
- derived-artifact attenuation；
- composite non-amplification。

验证：

```text
pytest tests\test_afw_bench.py -q
38 passed
```

接口注册验证：

```text
pytest tests\test_interfaces.py tests\test_afw_bench.py -q
53 passed
```

## 现在论文最稳的贡献写法

1. **Problem**：Agent action 中存在 semantic-role laundering；它不是普通 hallucination、prompt injection、tool over-privilege 或 RAG attribution failure。
2. **Representation**：Action-field authority warrants，用统一的 `Cap(x)` / `Need(s,f)` 描述 RAG、skill、tool、memory、approval、prior output。
3. **Algorithm**：CapGuard 做字段级 coverage check，并输出 minimal authority witness。
4. **Benchmark**：same-source paired rows + trace-derived authority-confusion rows，专门测试“合法消费保留、语义角色洗白阻断”。
5. **Practical layer**：manifest-lifted authority type inference，回答 `Cap(x)` 如何从 skill-driven agent traces 和通用 source manifests 中产生。
6. **Obligation layer**：obligation-carrying warrants，检查来源约束是否被 carried 或 discharged。
7. **Temporal layer**：time-scope authority decay，检查旧 approval、旧 memory 或旧 policy epoch 是否被复用成当前授权。
8. **Audit metric**：minimal witness compression，量化审计上下文减少比例。

## 下一步真正该突破的地方

最重要的不是继续改名字，而是扩大证据强度：

1. 对当前 40 个电力运维 generated rows 做 human audit，证明 mutation 是 plausible agent errors，不是任意标签翻转。
2. 让人工 reviewer 填写 40 条 generated rows 的 plausibility audit，并开始接入真实或半真实 RAG trace。
3. 测 minimal witness 是否减少审计成本，比如 token 数、人工定位时间、误判率。
4. 把 authority type inference 从通用 manifest 扩展成 tool metadata、memory 和 prior-step output 的具体 adapter。
5. 扩展更丰富的 obligation policy，例如 receipt-bound obligation，以及把 time-scope 接入更多真实 trace adapter。
6. 只在这些都站住后再跑 live model pilot。

## 给你汇报时可以直接说

我们的新角度是：Agent 安全不能只看工具有没有权限、来源有没有引用、scope 有没有匹配，还要看**字段消费的语义角色是否匹配**。同一个来源在一个字段里合法，在另一个字段里可能就是洗白。AFW 把 RAG、skill、tool、memory、approval 都统一成 `Cap(x)`，把 action fields 统一成 `Need(s,f)`，并用 CapGuard 检查覆盖关系。现在进一步有六个算法化支撑：一是从 trace 生成 boundary-preserving role confusion，二是输出 minimal authority witness 并量化 audit compression，三是从 manifest 推断 `Cap(x)`，四是检查 inherited obligations 是否被 carried 或 discharged，五是区分 obligation mode，六是检查 time-scope，避免旧 approval、旧 memory、旧 policy epoch 被复用成当前授权。所以它不是单纯的 guard，而是一个可生成 benchmark、可解释决策、能从 agent trace 产生授权对象、还能携带下游约束和时间有效性的字段级凭证框架。
