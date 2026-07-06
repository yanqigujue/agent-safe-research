# 电力大模型安全 Action Invariance 连续迭代计划

## 目标

本计划把当前项目主线固定为：

```text
电力大模型 / 电力 agent 在严格策略监督下，如何尽量保持正常动作不变，同时阻断越权字段。
```

核心方法不是简单拦截整个 agent action，而是把 action 拆成字段级授权需求 `Need(s,f)`，把 RAG 文档、skill manifest、tool metadata、memory、approval、trace output 等统一提升为 capability/warrant，再做字段级 coverage check 与 fieldwise repair。

## 当前已完成的基础

| 层 | 已有成果 |
|---|---|
| 形式化建模 | `docs/power_ops_action_invariance_formal_model_2026-07-02.md`，Cap/Need/coverage/repair-frame/action-invariance 定义 |
| 运行接口 | `formaltrust_platform/experiments/power_ops_action_invariance.py`，接入现有 FormalTrust YAML/runtime |
| 测试样本 | `examples/data/power_ops_action_invariance_cases.jsonl` 及 trace、span/OTLP、AgentDojo-style、多步 trace 扩展 |
| 测试框架 | `tests/test_power_ops_action_invariance.py`，覆盖 dataset、runner、baseline、paper artifact audit |
| 实验结果 | strict-block、fieldwise-repair、baseline grid、expanded dataset、table binding、numeric audit 等 JSON/Markdown 结果 |
| 论文材料 | evidence-bound abstract/introduction/method/related work/results/limitations/evaluation/conclusion，以及 `paper/power_ops_action_invariance/main.tex` |
| 审计链 | claim ledger、readiness gate、numeric audit、paragraph map、reviewer packets、edit gate、citation scaffold |

## 每轮必须产出的硬成果

每一轮至少产出一个可检查文件，不能只停留在口头描述。

| 类型 | 例子 |
|---|---|
| 建模 | 新定义、新性质、新反例、新定理草案、新边界条件 |
| 代码 | 新 experiment 模块、新 FormalTrust node、新 CLI/runner、新 audit generator |
| 样本 | 新 JSON/JSONL/YAML case，覆盖电力工单、调度、告警、skill、tool、memory、approval、trace |
| 测试 | 新 pytest，先红后绿，覆盖正常行为保持与危险字段阻断 |
| 结果 | 新 `.md/.json/.csv` 报告，包含 baseline、ablation、failure analysis 或 readiness audit |
| 论文 | 新段落、图表、LaTeX、citation audit、claim-evidence binding |

## 固定迭代流程

1. 读 `task_plan.md`、`findings.md`、`progress.md`，确认当前轮次。
2. 为本轮写一个最小可交付目标。
3. 若涉及代码，先加失败测试，再实现最小代码，再跑测试。
4. 若涉及建模，先写形式化对象，再写例子/反例和可测试性质。
5. 若涉及样本，明确每个 case 的授权来源、目标字段、oracle 行为和期望 guard 决策。
6. 若涉及论文，所有数字、表格、段落都必须绑定已有 evidence artifact。
7. 本轮结束后更新 `task_plan.md`、`findings.md`、`progress.md`、README、必要时更新 `PAPER_PLAN.md` 和 iteration log。
8. 做 keep / revise / reject 判断，然后自动进入下一轮。

默认不停。除非用户明确说暂停/停止，或连续三轮遇到同一个无法绕开的阻塞，否则继续推进。

## 下一批连续迭代队列

| 轮次 | 目标 | 主要产物 | 验收 |
|---:|---|---|---|
| 66 / 175 | 引用元数据审计 | `formaltrust_platform/experiments/power_ops_citation_metadata_audit.py`；`docs/power_ops_action_invariance_citation_metadata_audit_2026-07-02.md/json`；`paper/power_ops_action_invariance/references_checked.bib` | 只提升 primary-source 确认的 BibTeX；不编造作者/年份 |
| 67 / 176 | 引用插入与 cite-ready gate | LaTeX 引用插入器；citation readiness audit | `main.tex` 中只使用 checked bibliography keys |
| 68 / 177 | 创新点压缩包 | `docs/power_ops_action_invariance_contribution_packet_2026-07-02.md/json` | 三个创新点都绑定代码、实验、边界 |
| 69 / 178 | Skill-driven 电力 agent 样本扩展 | skill manifest / tool metadata / approval / memory 混合样本 | 覆盖非 RAG agent 场景，证明框架不限于 RAG |
| 70 / 179 | 多步复杂任务 action invariance benchmark | 多步 planner-skill-tool-memory trace 数据集和 runner | 测试严格监督下正常字段是否保持 |
| 71 / 180 | 正常行为保持压力测试 | normal-task perturbation suite | 量化 false intervention、authorized field preservation、human-review burden |
| 72 / 181 | Authority-confusion 生成器 | trace-derived authority-confusion rows | 自动生成“边界相同但角色错误”的攻击样本 |
| 73 / 182 | 性能与开销审计 | runtime overhead benchmark | 报告每 case 检查时间、字段数扩展性、审计压缩率 |
| 74 / 183 | 更强 baseline 与 ablation | policy monitor、access-control、whole-action refusal、attribution-only、fieldwise decision-only 对照 | 比较安全性、保守性、正常动作保持 |
| 75 / 184 | 统计稳健性 | bootstrap / multi-seed summary | 给主要指标置信区间，区分 fixture 结论和统计结论 |
| 76 / 185 | 论文图表生成 | paper-ready figures/tables | 图表数字全部来自 evidence JSON |
| 77 / 186 | 外部文献与 prior-work audit | citation/novelty/readiness 更新 | 不主张 first/only/superior，明确相邻工作边界 |
| 78 / 187 | 反方审稿与杀伤点清单 | kill-argument / reviewer packet | 找出最容易被拒的点，转成修复任务 |
| 79 / 188 | 修复反方指出的问题 | 代码、样本、文本补丁 | 每条 reviewer risk 都有 response 或降级 |
| 80 / 189 | 下一循环决策 | keep/revise/reject 报告 | 决定继续扩样本、改定义、补实验或收束论文 |

## 当前立即执行的下一步

当前队列停在 66 / 175：引用元数据审计。优先完成：

1. 修好 arXiv/OpenReview 等 primary metadata fetch 的 fallback。
2. 跑 citation metadata audit。
3. 只把 title/authors/year/source 全部匹配的条目写入 `references_checked.bib`。
4. 如果网络或 primary source 阻塞，写成显式 blocked artifact，不造假。
5. 更新 README、PAPER_PLAN、三件套和 `refine-logs/iterations/ITERATION_175.md`。

完成后自动进入 67 / 176，不停在“计划已写完”。

## 2026-07-02 Queue Override After Iteration 71 / 180

- 71 / 180 is complete: normal-behavior stress suite, YAML, report generator, result artifacts, README/PAPER_PLAN sync, table binding, numeric audit, and readiness gates are updated.
- Current readback: 4 fully authorized cases, 16 authorized fields, 16 preserved authorized fields, false intervention field rate 0.000, whole-action intervention rate 0.000, final-action mutation cases 0.
- Current table binding: 20 fully supported rows, 0 unsupported rows.
- Current gates: unsupported numeric claims 0, residual needs_evidence 0, paper readiness PASS, claim ledger readiness PASS.
- Immediate next iteration is 72 / 181: implement a trace-derived authority-confusion generator that mutates required roles while preserving field/scope boundaries.

## 2026-07-02 Queue Override After Iteration 72 / 181

- 72 / 181 is complete: trace-derived authority-confusion generator, rows artifact, result report, README/PAPER_PLAN sync, and focused TDD regression are updated.
- Current readback: 2 source cases, 10 generated paired rows, 10 boundary-preserving semantic-role mutations, 10 rows with only `required_role` mutated.
- CapGuard contrast: legal preservation 1.000, confusion block rate 1.000, false allow rate 0.000.
- Boundary-only contrast: false allow rate 1.000, showing that boundary scope alone misses semantic role confusion.
- Immediate next iteration is 73 / 182: audit runtime overhead and audit-compression scalability across the current suite family.

## 2026-07-02 Queue Override After Iteration 73 / 182

- 73 / 182 is complete: proxy-only runtime overhead audit, result report, README/PAPER_PLAN sync, and focused TDD regression are updated.
- Current readback: 6 suites, 108 field-check proxy units, max 6 checks per case, weighted mean audit compression 0.587963.
- Boundary: wall-clock latency is not available; current performance language must remain proxy-only.
- Immediate next iteration is 74 / 183: expand the baseline/ablation grid for safety/utility comparison, especially on trace-derived authority-confusion rows.

## 2026-07-02 Queue Override After Iteration 74 / 183

- 74 / 183 is complete: authority-confusion baseline grid, result report, README/PAPER_PLAN sync, and focused TDD regression are updated.
- Current readback: 10 rows, 5 baselines, CapGuard legal preservation 1.000, CapGuard confusion block 1.000, boundary/provenance-style false allow 1.000, strict-block false block 1.000.
- Immediate next iteration is 75 / 184: add statistical robustness checks for core rates.

## 2026-07-02 Queue Override After Iteration 75 / 184

- 75 / 184 is complete: Wilson-interval statistical robustness summary, result report, README/PAPER_PLAN sync, and focused TDD regression are updated.
- Current readback: normal preservation 16/16 with lower 0.8064, CapGuard confusion block 10/10 with lower 0.7225, CapGuard false allow 0/10 with upper 0.2775.
- Boundary: intervals describe finite fixture evidence, not production population guarantees.
- Immediate next iteration is 76 / 185: generate paper-ready figures and tables with evidence binding.

## 2026-07-02 Queue Override After Iteration 76 / 185

- 76 / 185 is complete: evidence-bound figure/table package, 2 SVG figures, 2 LaTeX tables, README/PAPER_PLAN sync, and focused TDD regression are updated.
- Current readback: `docs/power_ops_paper_figure_table_package_2026-07-02.json` records 2 figures and 2 tables, each with source JSON bindings.
- Immediate next iteration is 77 / 186: refresh citation, related-work, and novelty boundaries.

## 2026-07-02 Queue Override After Iteration 77 / 186

- 77 / 186 is complete: external 50-case full-agent authority stress suite, source seed, fixture, YAML, result report, README/PAPER_PLAN sync, and TDD regression are updated.
- Current readback: 50 NERC metadata anchors, 50 full agent task cases, 350 authorized fields preserved, 50 high-impact unauthorized fields removed, whole-action block rate 0.000, blocked field family count 7.
- Boundary: this is externally seeded synthetic full-agent testing, not production telemetry.
- Immediate next iteration is 78 / 187: refresh citation, related-work, and novelty boundaries.
