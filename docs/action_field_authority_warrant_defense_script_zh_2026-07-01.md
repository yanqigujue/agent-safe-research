# AFW 创新点答辩稿

日期：2026-07-01

## 30 秒版本

我们的创新点不是做一个泛泛的 agent 安全框架，而是提出了一个更细的安全对象：**动作字段级授权有效性**。

同一个来源在 agent 里不是全局可信或全局不可信。它可能可以支持一个字段，但不能支持另一个字段。比如一份策略文档可以支持“先运行仿真”，但不能被 agent 洗白成“无需人工审批”或“风险很低”。我们把这种问题叫做 **semantic-role laundering**，也就是语义角色洗白。

V2 里更锋利的一点是：即使字段、操作、数据范围、副作用范围、委托范围这些边界检查都通过，来源仍然可能缺少该字段需要的语义角色。比如 report-formatting skill 可以写报告文本，但不是 risk-assessment authority。AFW / CapGuard 查的就是这个“边界正确但角色错误”的剩余漏洞。

## 2 分钟版本

现在很多 agent 把不同来源都压进一个上下文里：RAG 证据、skill、工具描述、memory、用户批准、上一步输出。现有防护通常问：

- skill 是否恶意；
- 工具是否越权；
- 参数是否有来源；
- 输出是否 faithfully grounded；
- 执行协议有没有违反 runtime invariant。

这些都重要，但它们漏了一个更细的问题：

> 对于一个具体动作字段，agent 消费的来源有没有资格支配这个字段？

比如：

- report skill 可以格式化报告，但不能因此获得读密钥、删日志或派生 delegation 的权力；
- tool metadata 可以告诉我们参数名和枚举值，但不能成为高风险操作的审批依据；
- 用户同意“生成本地草稿”，不能被洗成“发送、上传、发布”；
- memory 可以支持个性化措辞，但不能修改安全策略；
- prior step output 可以被总结，但不能扩展新的文件系统或网络权限。

所以我们的核心贡献是把 agent action 拆成多个 protected fields，对每个字段生成 action-field authority warrant。形式上就是：

```text
Cap(x)      = 来源 x 的能力和作用域
Need(s, f)  = 步骤 s 的字段 f 需要什么授权

合法消费：
Consume(x -> f, s) iff Cap(x) covers Need(s, f)
```

最关键的实验设计是 same-source contrast：同一个来源，在合法字段里应该允许，在越界字段里应该阻断。这样可以证明我们不是简单地屏蔽来源，而是在判断来源和字段之间的语义授权关系。

现在更强的实验是 boundary-preserving role mismatch：边界范围全部匹配，但 semantic role 不匹配。这样可以证明我们不是只做 scope/consent 检查。

## 5 分钟版本

### 第一层创新：新的安全对象

以前很多工作把安全对象放在 skill、tool、prompt、memory、protocol、trace 或 action 整体上。我们把对象进一步下沉到 action field。

一个 agent action 里有很多字段：

```text
tool
parameters
data_read_scope
data_write_scope
side_effect
requires_human_approval
risk_level
risk_report
delegation
```

我们的观点是：这些字段不能共享一个模糊的“上下文可信度”。每个字段需要自己的授权来源和证明。

### 第二层创新：语义角色洗白

我们要抓的不是传统 malicious input，而是一个更隐蔽的问题：

> 来源本身可能是可信的，但被 agent 用错了角色。

这就是 semantic-role laundering。

例如同一份 policy evidence：

```text
policy evidence -> route_to_simulation       合法
policy evidence -> requires_human_approval=false  非法
policy evidence -> risk_level=low            非法
```

source 是同一个，区别在于它消费到哪个 field。

### 第三层创新：字段级 authority type check

AFW 的算法核心可以理解成一个字段级类型检查：

```text
source capability type <= field requirement type
```

也就是每个来源有 `Cap(x)`，每个字段有 `Need(s,f)`，执行前检查覆盖关系。

当前实现已经支持：

- same-source legal-vs-laundered 对比；
- permission-only baseline；
- attribution-only baseline；
- strict-block baseline；
- 字段族 breakdown；
- 多来源组合授权；
- 禁止角色放大；
- counter-authority 下的 `abstain` 决策；
- scope coverage，也就是来源只能授权自己覆盖的动作操作、数据范围和委托范围。
- boundary-scope-only baseline，用来证明只查边界仍会漏掉纯语义角色洗白；
- derived-artifact attenuation，也就是 summary / skill output 不能自动继承原始来源的审批、风险或委托权威。

组合授权这一点比较重要。比如：

```text
用户同意生成本地草稿 + 策略允许本地草稿
  -> 可以授权 local_draft

用户同意生成本地草稿 + 策略允许本地草稿
  -> 不能自动推出 external_publish
```

这说明我们不是只做单来源规则，而是能表达多来源共同满足一个字段需求，同时不允许组合产生任何来源都没有的新语义角色。

另外，真实系统里不一定只有 allow/block。有些字段虽然正向授权看起来满足，但还存在反向约束，比如缺少 DLP 扫描、审批票据冲突、策略要求复核。我们现在也支持 `abstain`：

```text
positive authority covered + counter-authority present
  -> abstain / route to review
```

### 第四层创新：实验记忆点

主实验不是普通 attack success rate，而是 same-source paired benchmark：

```text
source x -> legal field      allow
source x -> protected field  block
```

当前最小结果：

| 方法 | 合法消费保留 | 洗白阻断 | 误放行 | 误阻断 |
|---|---:|---:|---:|---:|
| AFW / CapGuard | 1.0 | 1.0 | 0.0 | 0.0 |
| Permission-only | 1.0 | 0.0 | 1.0 | 0.0 |
| Attribution-only | 1.0 | 0.0 | 1.0 | 0.0 |
| Strict-block | 0.0 | 1.0 | 0.0 | 1.0 |

这个结果的含义是：

- permission-only 太松；
- attribution-only 太松；
- strict-block 太硬；
- AFW 在中间：保留合法消费，同时阻断越界字段消费。

### 第五层创新边界

我们不能说自己是第一个 agent authorization，也不能说是第一个 proof-carrying action，更不能说比 AuthGraph、SkillGuard、PCAA 全面更强。

我们应该说：

> 这些工作保护的是 skill、工具、参数来源、执行协议、动作证书等对象；我们补的是 protected action field 这一层，尤其是 approval、risk/report、side-effect、delegation、data-scope 这些非参数字段的语义授权有效性。

这就是比较稳的创新边界。

## 被追问时的回答

### Q1：这不就是访问控制吗？

不是传统访问控制。传统访问控制通常问这个主体能不能访问这个资源；我们问的是一个 agent 动作字段消费的来源有没有资格支配这个字段。同一来源在一个字段里允许，在另一个字段里阻断，这是字段级语义授权问题。

### Q2：这不就是 provenance / attribution 吗？

不是。Attribution 只能说明字段受哪个来源影响；AFW 进一步问这个来源有没有资格管这个字段。我们已经有 attribution-only baseline，它能追到来源，但会误放行全部洗白字段。

### Q3：这不就是 tool permission 吗？

不是。工具允许调用不代表该工具描述、检索证据或 skill 输出可以授权审批、风险降级、副作用释放或 delegation。AFW 查的是字段被什么来源授权，而不是工具本身是否在权限列表里。

### Q4：这和 AuthGraph 怎么区分？

AuthGraph 很接近，所以不能硬说它做不到授权来源。我们的安全边界应该放在非参数字段：approval、risk/report、side-effect、delegation、data-scope。我们不抢普通参数 provenance，而是问这些动作语义字段是否被有效来源授权。

### Q5：这和 proof-carrying agent actions 怎么区分？

Proof-carrying action 更像证书框架；AFW 可以作为证书里的字段级 payload semantics。我们的贡献不是“第一个动作证书”，而是定义 protected action fields 消费来源时需要检查什么语义授权。

## 最推荐的最终表述

中文：

> 我们提出动作字段级授权凭证，用来检测 agent 动作中的语义角色洗白。核心发现是：同一来源可以合法支撑某个字段，但不能自动支撑审批、风险、报告、副作用、委托或数据范围等更高权限字段。AFW / CapGuard 对每个受保护字段检查其消费来源是否具备所需语义角色，从而在保留合法来源使用的同时阻断越界消费。

英文：

> We study semantic-role laundering in agent actions: the same source may be valid for one action field but invalid for another. Action-field authority warrants check whether each protected field consumes sources that cover the field's required semantic roles and scopes, preserving legal same-source use while blocking out-of-scope authority consumption.
