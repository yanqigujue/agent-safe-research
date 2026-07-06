# AFW 创新点核心说明

日期：2026-07-01

## 一句话

我们的创新点不是“又做一个 agent 安全框架”，而是提出并验证一个更细的安全对象：

> **动作字段级授权有效性**：同一个来源可以合法影响某个字段，但不能自动合法影响另一个字段，尤其不能被洗白成审批、风险、报告、外部副作用、委托、数据范围等非参数权限字段。

## 审稿人视角下的新问题

现有很多工作问的是：

- 这个 skill 能不能调用某个工具？
- 这个工具调用是否越权？
- 这个参数有没有来源？
- 这个输出有没有引用证据？
- 这个协议执行是否满足运行时不变量？

我们问的是另一个问题：

> **这个具体动作字段，消费的来源有没有资格管这个字段？**

例如：

- 一段检索证据可以支持“运行仿真”，但不能支持“跳过人工审批”。
- 一个 report-writing skill 可以支持“格式化报告”，但不能支持“读取密钥”或“删除日志”。
- 一段工具 schema 可以支持“填写参数”，但不能支持“批准高风险操作”。
- 用户说“可以生成草稿”，不能被洗成“可以发送/上传/发布”。
- 记忆可以支持“个性化措辞”，不能支持“修改安全策略”。

这个问题的关键是：**来源不是全局可信或全局不可信，来源的权威性是字段相关的。**

## 与已有方向的区别

| 已有方向 | 它主要保护什么 | 我们补的缺口 |
|---|---|---|
| RAG attribution / faithfulness | 输出是否被证据支持 | 证据是否有资格支配动作字段 |
| Tool permission / least privilege | 工具是否允许调用、工具是否过度授权 | 允许调用不代表来源可授权审批/风险/副作用字段 |
| Skill security | skill 是否恶意、skill 权限是否合理 | skill 后续产物是否被洗成更高语义权限 |
| Proof-carrying skill | skill 包或工具调用 envelope 是否满足证明 | 证明对象扩展到 action field 的来源-字段消费关系 |
| MCP/runtime invariant | 协议和执行过程是否违反不变量 | 运行时正确不代表字段语义授权正确 |
| AuthGraph / provenance authorization | 参数来源与授权图是否一致 | 参数来源一致不代表非参数权限字段有语义授权 |

## 可命名的核心概念

### 1. Semantic-role laundering

语义角色洗白：一个来源在原本角色下是合法的，但被 agent 消费成另一个更高权限语义角色。

```text
policy evidence -> simulation routing      legal
policy evidence -> approval waiver         laundering
```

### 2. Action-field authority warrant

对每个动作字段生成一个 warrant：

```text
Cap(x)      = 来源 x 的作用域能力
Need(s, f)  = 步骤 s 中字段 f 需要的授权条件

字段消费合法：
Consume(x -> f, s) iff Cap(x) covers Need(s, f)
```

### 3. Same-source contrast

同一来源、两种消费：

```text
source x -> legal field      allow
source x -> protected field  block, unless Cap(x) covers Need(s, f)
```

这是我们最适合写成论文主实验的地方，因为它可以排除一个常见反驳：

> “你只是把不可信来源挡掉了。”

不是。我们允许同一个来源在合法字段里使用，只阻止它被洗成不具备的权限。

### 4. Compositional warrant without role amplification

真实 agent 动作经常不是单来源授权，而是多个来源共同满足一个字段需求：

```text
Need(step, field).required_roles = [role_1, role_2, ...]
```

例如：

```text
用户同意生成本地草稿 + 策略允许本地草稿
  -> 可以授权 local_draft

用户同意生成本地草稿 + 策略允许本地草稿
  -> 不能自动放大成 external_publish
```

这给框架增加了一个更像算法突破的点：

> 多个受限授权可以组合满足字段需求，但组合不能产生任何来源都不具备的新语义角色。

## 现在已有的最小证据

文件：

- `examples/afw_same_source_paired_rows.json`
- `formaltrust_platform/experiments/afw_bench.py`
- `tests/test_afw_bench.py`
- `docs/action_field_authority_warrant_deterministic_results_2026-07-01.md`
- `examples/afw_composite_authority_rows.json`

当前 10 条 paired rows 覆盖：

- evidence
- skill
- tool metadata
- memory
- user approval
- prior-step output

当前 laundered 字段覆盖：

- approval
- risk/report
- side effect
- delegation
- data scope

组合授权样例覆盖：

- 用户批准 + 策略证据：允许本地草稿，不允许外部发布；
- skill + prior artifact：允许文档总结，不允许风险门控。

确定性结果：

| 方法 | 合法消费保留 | 洗白阻断 | 误放行 | 误阻断 |
|---|---:|---:|---:|---:|
| AFW / CapGuard | 1.0 | 1.0 | 0.0 | 0.0 |
| Permission-only | 1.0 | 0.0 | 1.0 | 0.0 |
| Attribution-only | 1.0 | 0.0 | 1.0 | 0.0 |
| Strict-block | 0.0 | 1.0 | 0.0 | 1.0 |

这个表表达的创新点是：

- permission-only 和 attribution-only 太松：它们知道来源存在或调用被允许，但不知道来源能不能管这个字段；
- strict-block 太硬：能挡风险，但会牺牲合法使用；
- AFW 的位置是中间那一层：**按字段需要的语义角色验证来源能力**。

当前测试：

```text
pytest tests\test_afw_bench.py -q
10 passed
```

## 最危险的反驳

最危险的反驳不是“这个方向没意义”，而是：

> “这只是 authorization/provenance 的另一种表述。”

防守方式：

1. 不声称我们发明 authorization。
2. 不声称 prior work 做不到工具参数授权。
3. 把论文钉在非参数保护字段上：approval、risk/report、side-effect release、delegation、data-scope。
4. 主实验必须是 same-source contrast，而不是普通 attack success rate。
5. 对 AuthGraph 类工作只说“问题不同”：它更接近参数来源和授权图一致性；我们问的是动作字段的语义授权资格。

## 推荐论文主张

保守版：

> We identify semantic-role laundering in agent actions: the same source may be valid for one action field but invalid for another. We propose action-field authority warrants, a field-level validity check that verifies whether a consumed source has the semantic role required by protected non-parameter fields.

中文表达：

> 我们发现 agent 动作中存在语义角色洗白：同一来源可合法支撑某些字段，却被错误消费为审批、风险、报告、副作用、委托或数据范围等更高权限字段的依据。为此，我们提出动作字段级授权凭证，用字段所需语义角色来验证来源能力，而不是只检查来源是否存在、工具是否允许或调用是否有出处。

## 下一步真正该突破的点

现在最需要突破的不是再换名字，而是把 “field-authority validity” 做成一个审稿人觉得不可替代的实验：

1. 增加 richer counter-authority rows：审批票据冲突、策略版本冲突、缺少回执等。
2. 增加 ambiguous rows：来源部分覆盖 Need(s,f)，迫使 verifier 给出 abstain 或 partial。
3. 增加 skill-chain rows：skill 产物跨多步传播后被洗成更高权限。
4. 做 faithful baseline：permission-only、attribution-only、AuthGraph-style parameter provenance、strict-block。
5. 把结论写成“新安全对象”，不是“全面优于所有 agent 安全方法”。
