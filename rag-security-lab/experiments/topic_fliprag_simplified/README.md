# Topic-FlipRAG 简化 Demo

这个目录实现一个轻量版 Topic-FlipRAG 思路验证，用于本项目的电力安全知识库污染调研。

参考 GitHub 源码仓库 `LauJames/Topic-FlipRAG` 的三段结构：

1. `Stage1_knowledge_guided_attack.ipynb`：生成 topic-aware 的 `doc_know`。
2. `Stage2_adversarial_trigger_generation.ipynb`：为 `doc_know` 添加 trigger，提高检索排名。
3. `RAG_pipeline.ipynb`：构建 RAG，比较污染前后输出，并评估 stance 变化。

本 demo 不复现 GPU/梯度 trigger 优化，而是做一个可本地运行、可解释的最小版本：

- 从 `知识库污染数据集/Elecbench中文版` 读取 clean KB。
- 按 `blackstart`、`monitoring`、`dispatch` 三个主题选择风险/影响/保护相关问题。
- 为每个主题生成少量“风险淡化立场”的 topic poisoned docs。
- 使用自然语言 trigger 和主题节点覆盖，模拟 Topic-FlipRAG 的 topic-oriented poisoned passages。
- 用 TF-IDF 字符 n-gram 检索先评估污染文档是否进入 top-k。
- 可选调用本地 Ollama `qwen3:8b`，比较 clean RAG 与 poisoned RAG 的回答是否更倾向风险淡化。

## 快速运行

只跑检索侧 demo：

```powershell
python experiments\topic_fliprag_simplified\topic_fliprag_simplified.py --mode retrieve --top-k 5
```

调用本地 qwen3:8b 做生成对比：

```powershell
python experiments\topic_fliprag_simplified\topic_fliprag_simplified.py --mode generate --model qwen3:8b --base-url http://localhost:11434 --top-k 5 --prompt-mode naive --max-generation-queries 6
```

防御提示词对照：

```powershell
python experiments\topic_fliprag_simplified\topic_fliprag_simplified.py --mode generate --model qwen3:8b --base-url http://localhost:11434 --top-k 5 --prompt-mode guarded --max-generation-queries 6
```

## 输出文件

输出目录：

```text
experiments/topic_fliprag_simplified/outputs/
```

主要文件：

- `poisoned_topic_docs.jsonl`：构造的主题污染文档。
- `retrieval_summary_top{k}.json`：主题污染检索命中率。
- `retrieval_details_top{k}.jsonl`：每个主题问题的 top-k 检索明细。
- `generation_results_{prompt_mode}_top{k}.jsonl`：clean/poisoned 生成对比。
- `generation_summary_{prompt_mode}_top{k}.json`：启发式风险淡化偏移统计。

## 指标

| 指标 | 含义 |
| --- | --- |
| `topic_poison_hit_rate` | 同主题污染文档是否进入目标主题问题的 top-k |
| `topic_poison_rank1_rate` | 同主题污染文档是否排在 rank-1 |
| `cross_topic_poison_hit_rate` | 其他主题污染文档是否误命中 |
| `heuristic_downplay_marker_increased_rate` | poisoned answer 中风险淡化标记是否比 clean answer 增加 |
| `heuristic_dominant_downplay_shift_rate` | 更严格的主导淡化偏移：淡化标记增加且审慎标记没有增加 |

## 与原论文的差异

这是调研 demo，不是完整复现：

- 没有使用 LLM 自动提取 key nodes，而是使用人工主题节点。
- 没有实现 lexical substitutions / sentential rewrites / phrase insertions 的迭代候选搜索。
- 没有实现 reverse-gradient 或 beam search trigger 优化。
- stance 评估暂用关键词启发式，后续可替换为 LLM-as-judge。

它适合先验证本项目中的核心问题：

```text
少量主题级风险淡化文档，是否会在电力安全 RAG 问答中被检索出来，
并让同一主题下多个问题的回答整体偏向淡化风险？
```
