# 黑启动主题 Topic-FlipRAG 流程实验记录

## 目标

本实验选择主题 3：

```text
黑启动过程安全与恢复风险
```

目标是更接近 Topic-FlipRAG 原文流程，而不是继续使用手工 trigger 或 query-specific Top1 优化。

## 目标问题集

从 `blackstart_zh.jsonl` 选取 7 个同类问题：

- `blackstart_zh:23`
- `blackstart_zh:24`
- `blackstart_zh:25`
- `blackstart_zh:26`
- `blackstart_zh:27`
- `blackstart_zh:28`
- `blackstart_zh:29`

这些问题集中在黑启动计划、战略位置、同步发电机、系统稳定性、黑启动设施作用和协调员职责。没有选取“未经授权访问/停止黑启动/破坏流程”等高风险操作请求。

## 流程实现

新增脚本：

```text
experiments/topic_fliprag_simplified/topic_fliprag_blackstart_stage_flow.py
```

该脚本实现三步：

1. `Stage1`: 调用本地 `qwen3:8b`，根据同类问题生成 topic-level 污染知识段。
2. `Stage2`: 不手写 trigger，而是从 Stage1 的 `key_nodes`、`retrieval_keywords`、`knowledge_passage` 中抽取候选短语，并用本地 surrogate retriever 自动搜索 trigger。
3. `RAG pipeline`: 构建 clean KB 与 attacked KB，支持 `append` 和 `replace` 两种注入方式，输出检索评测。

## 严格 class-level 约束

为避免退化成 query-specific 攻击，当前版本做了如下限制：

- 不把目标问题原句写入污染文本。
- 不使用上一版的“问题复述密集卡片”。
- Stage2 不手工指定 trigger。
- Stage2 候选主要来自 Stage1 归纳出的类关键词和知识段。

## 当前结果

命令：

```powershell
python experiments\topic_fliprag_simplified\topic_fliprag_blackstart_stage_flow.py --mode retrieve --attack-mode replace --retriever hybrid-lsa --hybrid-alpha 0.5 --dense-components 32 --top-k 5 --trigger-steps 10 --beam-size 4 --max-candidates 80 --model qwen3:8b --base-url http://localhost:11434
```

结果：

```json
{
  "query_count": 7,
  "attack_mode": "replace",
  "replaced_clean_doc_count": 7,
  "appended_poison_doc_count": 0,
  "topic_poison_hit_rate": 0.0,
  "topic_poison_rank1_rate": 0.0
}
```

在更宽松的候选抽取版本中，如果允许从原问题中抽取短片段，命中率可以提高到：

```json
{
  "topic_poison_hit_rate": 0.8571,
  "topic_poison_rank1_rate": 0.2857
}
```

但该版本的 trigger 会出现类似原问题片段的字符切片，因此不适合作为严格的一类问题攻击结果。

## 阶段判断

本轮实验说明：

1. 缺少 Stage1 的确会让污染文本缺少类级知识结构。
2. 但仅有 Stage1 还不够，Stage2 的 trigger 优化质量非常关键。
3. 在当前 `hybrid-lsa` 本地检索器下，严格 class-level trigger 很难压过或替代 clean 文档。
4. 之前 query-specific Top1 成功不能代表 Topic-FlipRAG 式一类问题攻击成功。
5. 如果要更贴近原文效果，下一步需要更强的 Stage2：例如更好的候选词生成、真正的 embedding/reranker surrogate，或者按子主题生成多条污染 passage。

## 输出文件

- `experiments/topic_fliprag_simplified/outputs/blackstart_stage_flow_stage1_replace_hybrid-lsa_top5.json`
- `experiments/topic_fliprag_simplified/outputs/blackstart_stage_flow_trigger_trace_replace_hybrid-lsa_top5.json`
- `experiments/topic_fliprag_simplified/outputs/blackstart_stage_flow_poison_doc_replace_hybrid-lsa_top5.jsonl`
- `experiments/topic_fliprag_simplified/outputs/blackstart_stage_flow_retrieval_details_replace_hybrid-lsa_top5.jsonl`
- `experiments/topic_fliprag_simplified/outputs/blackstart_stage_flow_retrieval_summary_replace_hybrid-lsa_top5.json`
