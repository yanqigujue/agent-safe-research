# PoisonedRAG 简化复现实验

这个目录用于先做一个小规模、可解释的 PoisonedRAG 复现：

1. 使用 `知识库污染数据集/Elecbench中文版` 中的 JSONL 作为 clean KB。
2. 对少量目标问题注入“精确问题诱饵 + 错误证据”的 poisoned docs。
3. 用向量检索检查污染是否主要命中目标问题，而不是泛化影响其他问题。
4. 可选调用本地 Qwen3:8b 进行 clean / poisoned RAG 答案对比。

## 快速运行

先只跑检索侧评估：

```powershell
python experiments\poisonedrag_simplified\simplified_poisonedrag.py --mode retrieve
```

输出会写入：

```text
experiments/poisonedrag_simplified/outputs/
```

主要看两个文件：

- `retrieval_summary.json`：目标问题和非目标问题的污染命中率。
- `retrieval_details.jsonl`：每个问题 top-k 检索结果明细。

## 调用本地模型

如果本地 Qwen3:8b 是 Ollama 服务：

```powershell
python experiments\poisonedrag_simplified\simplified_poisonedrag.py --mode generate --backend ollama --model qwen3:8b --base-url http://localhost:11434 --top-k 1 --prompt-mode naive
```

如果本地模型是 OpenAI-compatible 服务，例如 LM Studio、vLLM、Ollama OpenAI 兼容接口：

```powershell
python experiments\poisonedrag_simplified\simplified_poisonedrag.py --mode generate --backend openai-compatible --model qwen3:8b --base-url http://localhost:1234/v1 --top-k 1 --prompt-mode naive
```

如果你的模型名实际是 `qainwen3:8b` 或其他名字，把 `--model` 改成对应名称即可。

`--prompt-mode naive` 用于复现裸 RAG 攻击；`--prompt-mode guarded` 用于后续防御对照，会显式要求模型识别资料冲突。

生成结果会按 top-k 保存，例如：

- `generation_results_naive_top1.jsonl`
- `generation_results_naive_top5.jsonl`
- `retrieval_summary_top1.json`
- `retrieval_summary_top5.json`

## 为什么这样污染

为了尽可能只污染具体问题，默认污染文档遵循：

- 只复述目标问题，不写宽泛主题词。
- 使用目标问题中的稀有实体、数值、选项或专有短语。
- 不加入“黑启动安全”“电网风险”等泛化关键词堆砌。
- 每条污染文档只服务一个目标问题。

检索评估里会专门统计：

- `target_poison_hit_rate`：目标问题 top-k 是否命中对应污染文档。
- `non_target_poison_hit_rate`：非目标问题 top-k 是否误命中任何污染文档。

理想状态是前者高、后者低。
