# PoisonedRAG 完整版实验框架

本目录用于基于本地 `Elecbench中文版` 数据库实现更接近 PoisonedRAG 的批量实验。

默认生成模型：

```text
qianwen3:8b
```

如果你的 Ollama 中模型实际名称不同，可以运行时通过 `--model` 修改。

## 实验覆盖

当前 full 版支持：

- 从 Elecbench 中文数据中批量选择目标问题。
- 每个目标问题生成多条 poisoned docs。
- 对 `top-k=1/3/5/10` 批量评估检索命中率。
- 统计目标问题命中率和非目标溢出率。
- 可选调用本地 Ollama 模型做 clean / poisoned 生成对比。
- 对检索溢出的非目标问题做最终回答污染评估。
- 输出 poisoned docs、target specs、retrieval metrics 和 generation results。

## 快速运行

只跑检索侧批量评估：

```powershell
python experiments\poisonedrag_full\poisonedrag_full.py --mode retrieve --target-count 24 --poisons-per-target 3 --top-ks 1,3,5,10
```

调用本地 `qianwen3:8b` 做生成评估：

```powershell
python experiments\poisonedrag_full\poisonedrag_full.py --mode generate --target-count 12 --poisons-per-target 3 --top-ks 1,3,5 --model qianwen3:8b --base-url http://localhost:11434
```

生成评估会比较：

```text
clean KB 检索 + qianwen3:8b 回答
poisoned KB 检索 + qianwen3:8b 回答
```

## 使用 DeepSeek API

如果不下载本地模型，可以使用 DeepSeek 的 OpenAI-compatible API。先在当前 PowerShell 会话中设置：

```powershell
$env:DEEPSEEK_API_KEY="你的 API Key"
```

然后运行：

```powershell
python experiments\poisonedrag_full\poisonedrag_full.py --mode generate --backend deepseek --model deepseek-v4-flash --target-count 12 --poisons-per-target 3 --top-ks 5 --eval-non-target --max-non-target 10
```

如果 API 实际模型名不是 `deepseek-v4-flash`，将 `--model` 改成 DeepSeek 控制台里显示的可用模型名。

也可以从本地文件读取 API key，例如工作区根目录的 `deepseek-api.txt`：

```powershell
python experiments\poisonedrag_full\poisonedrag_full.py --mode generate --backend deepseek --model deepseek-v4-flash --api-key-file deepseek-api.txt --manual-attack-csv experiments\poisonedrag_full\manual_review_poisonedrag_10_attacks.csv --poison-style paper_lm_targeted --poisons-per-target 5 --top-ks 5 --eval-non-target --max-non-target 10
```

如果要使用人工精细化的 PoisonedRAG 攻击文本：

```powershell
python experiments\poisonedrag_full\poisonedrag_full.py --mode generate --backend deepseek --model deepseek-v4-flash --manual-attack-csv experiments\poisonedrag_full\manual_review_poisonedrag_10_attacks.csv --top-ks 5 --eval-non-target --max-non-target 10
```

如果要按原文黑盒 `LM_targeted` 风格，把每条人工样本扩展为每题 5 条：

```powershell
python experiments\poisonedrag_full\poisonedrag_full.py --mode generate --backend ollama --model qwen3:8b --base-url http://localhost:11434 --manual-attack-csv experiments\poisonedrag_full\manual_review_poisonedrag_10_attacks.csv --poison-style paper_lm_targeted --poisons-per-target 5 --top-ks 5 --eval-non-target --max-non-target 10
```

如果要评估“非目标问题最终答案是否被污染带偏”，加入：

```powershell
python experiments\poisonedrag_full\poisonedrag_full.py --mode generate --target-count 12 --poisons-per-target 3 --top-ks 5 --model qianwen3:8b --eval-non-target --max-non-target 20
```

如果只想评估非目标最终回答污染，不跑目标问题生成，可以加：

```powershell
python experiments\poisonedrag_full\poisonedrag_full.py --mode generate --skip-target-generation --target-count 12 --poisons-per-target 3 --top-ks 5 --model qianwen3:8b --eval-non-target --max-non-target 10
```

## 输出文件

输出目录：

```text
experiments/poisonedrag_full/outputs/
```

主要文件：

- `target_specs.jsonl`：目标问题和攻击目标答案。
- `poisoned_docs.jsonl`：构造出的污染文档。
- `retrieval_summary.json`：不同 top-k 下的检索攻击指标。
- `retrieval_details_top{k}.jsonl`：每个问题的检索明细。
- `generation_results_top{k}.jsonl`：可选生成结果。
- `non_target_generation_spillover_top{k}_{prompt_mode}.jsonl`：非目标最终回答污染评估结果。

## 指标

核心指标：

| 指标 | 含义 |
| --- | --- |
| Target Poison Hit Rate | 目标问题 top-k 是否检索到对应污染文档 |
| Target Poison Rank1 Rate | 目标问题 rank-1 是否为对应污染文档 |
| Non-target Spillover Rate | 非目标问题 top-k 是否误检索到任意污染文档 |
| Non-target Generation Spillover Rate | 非目标问题最终回答是否被污染文档带偏 |
| Generation Attack Success | poisoned answer 是否更接近攻击答案而非 clean answer |

当前生成攻击成功使用关键词/相似度启发式做粗评估，后续可以替换为 LLM-as-judge。
