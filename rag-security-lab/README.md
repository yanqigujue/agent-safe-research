# RAG 知识库污染与上下文污染研究框架

本项目现在使用 `rag_security_lab` 作为统一实验入口。旧的 `experiments/` 脚本和输出被保留，便于核对历史结果；新实验建议通过 YAML 配置运行，不再复制或继续扩展单体脚本。

## 统一实验链路

```text
Dataset
  -> Attack (none / targeted_static / external_jsonl)
  -> Query Selector (all / ids / attack_targets / filter)
  -> Clean Retrieval + Attacked Retrieval
  -> Retrieval Metrics
  -> Optional Generation
  -> Generation Metrics
  -> Immutable Run Directory
```

每个组件都通过注册表管理。后续增加真实 embedding、向量数据库、reranker、BIPIA 数据集或新的攻击方法时，只需新增一个组件并注册名称，不需要修改实验主流程。

## 快速开始

查看现有组件：

```powershell
python -m rag_security_lab components
```

先验证配置、数据路径和样本数量，不写任何结果：

```powershell
python -m rag_security_lab run --config configs\poisonedrag_retrieval.yaml --dry-run
```

运行统一 PoisonedRAG 检索实验：

```powershell
python -m rag_security_lab run --config configs\poisonedrag_retrieval.yaml
```

运行 Topic-FlipRAG 外部污染文本实验：

```powershell
python -m rag_security_lab run --config configs\topic_fliprag_append.yaml
```

运行本地 BGE-M3 向量检索实验：

```powershell
python -m rag_security_lab run --config configs\poisonedrag_vector_bge_m3.yaml
python -m rag_security_lab run --config configs\topic_fliprag_vector_bge_m3.yaml
```

运行测试：

```powershell
python -m unittest discover -s tests -v
```

## 配置规范

一个实验包含七个稳定部分：

| 配置段 | 作用 |
| --- | --- |
| `experiment` | 实验名、随机种子、输出根目录 |
| `dataset` | 语料来源和字段映射 |
| `queries` | 评估问题的选择与隔离 |
| `attack` | 攻击类型、append/replace、污染输入 |
| `retriever` | 检索器、top-k 和检索参数 |
| `generation` | 是否调用模型、后端、模型、prompt 和样本范围 |
| 运行清单 | 由框架自动记录，无需手写 |

内置数据集：

- `elecbench`：加载当前 Elecbench 中文版目录。
- `jsonl`：加载任意标准 JSONL 语料，可配置字段名。

内置攻击：

- `none`：干净基线。
- `targeted_static`：PoisonedRAG 风格的定向污染，支持 YAML 内联目标或现有人工 CSV。
- `external_jsonl`：加载手工构造的 Topic-FlipRAG 或其他污染文档。

内置检索器：

- `tfidf`：字符或词级稀疏检索。
- `lsa`：基于 TF-IDF + SVD 的轻量语义基线。
- `hybrid_lsa`：归一化后的 sparse/LSA 混合基线。
- `ollama_embedding`：通过 Ollama `/api/embed` 进行真实 dense embedding 检索，按模型 digest 和内容哈希使用 SQLite 缓存。

## 国内镜像与本地模型

本项目当前使用从 [ModelScope 的 Xorbits/bge-m3-gguf](https://www.modelscope.cn/models/Xorbits/bge-m3-gguf) 获取的 `bge-m3-Q4_K_M.gguf`，再按 [Ollama 官方 GGUF 导入方式](https://docs.ollama.com/import)创建本地模型 `bge-m3-ms-q4`。这不是替换 Ollama Registry 的代理，而是“国内镜像下载 GGUF + Ollama 本地导入”的稳定路径。

当前工作区已包含导入描述文件，GGUF 大文件和嵌入缓存均被 Git 忽略：

```powershell
& "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe" create bge-m3-ms-q4 -f local_models\bge-m3\Modelfile
```

模型为 BERT 架构、Q4_K_M 量化、1024 维嵌入。框架会记录实际模型 digest，模型被替换后不会错误复用旧缓存。

内置生成后端：

- `ollama`
- `openai_compatible`

API 密钥只能通过 `generation.api_key_env` 指定的环境变量读取，不支持从明文文件读取。

## 运行产物

每次实验会创建独立目录：

```text
runs/YYYYMMDD_HHMMSS_<experiment>_<config-hash>/
```

目录内包括：

| 文件 | 内容 |
| --- | --- |
| `manifest.json` | 状态、时间、Python、依赖版本、Git revision、异常信息 |
| `config.resolved.json` | 完整配置快照和配置哈希 |
| `preview.json` | 文档、污染、查询和目标数量 |
| `queries.jsonl` | 本次实际评估的查询集 |
| `poison_documents.jsonl` | 本次实际注入的污染文档 |
| `retrieval_results.jsonl` | 每个查询的 clean/attacked 双路排名 |
| `metrics.retrieval.json` | 每个 top-k 的 clean/attacked 原文档效用、目标命中、rank-1、MRR 和非目标溢出 |
| `generation_results.jsonl` | 可选的模型、后端、prompt 模式和回答 |
| `metrics.generation.json` | 明确标注为 heuristic 的生成指标 |

目录不会覆盖旧实验。即使运行失败，`manifest.json` 也会记录失败类型和原因。

## 首轮同口径结果

以下为 `retrieval_v2` 的首轮结果；PoisonedRAG 使用 288 个查询（10 个攻击目标），Topic-FlipRAG 为 6 个攻击目标的探索性小样本。

| 攻击 | 检索器 | Clean Gold R@1 | Attacked Gold R@1 | Target ASR@1 | Target ASR@5 | 非目标污染暴露@5 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| PoisonedRAG | TF-IDF | 99.3% | 96.9% | 70.0% | 100.0% | 4.7% |
| PoisonedRAG | BGE-M3 Q4 | 99.3% | 97.2% | 60.0% | 100.0% | 7.9% |
| Topic-FlipRAG | Hybrid LSA | 100.0% | 100.0% | 0.0% | 100.0% | N/A |
| Topic-FlipRAG | BGE-M3 Q4 | 100.0% | 100.0% | 0.0% | 100.0% | N/A |

这轮结果说明 BGE-M3 已经可实际执行和复现，但不能仅凭这组小样本宣称优于或弱于词法检索。当前 Gold 指标使用与查询同 ID 的原文档，存在原问题文本自匹配，数值偏乐观；正式实验需要加入未见改写查询、更多随机种子和置信区间。

## 添加新组件

组件类接收对应配置段，并注册到统一注册表。例如新增检索器：

```python
from rag_security_lab.registry import RETRIEVERS

@RETRIEVERS.register("my_dense_retriever")
class MyDenseRetriever:
    def __init__(self, config):
        self.config = config

    def retrieve(self, docs, queries, top_k):
        # 返回 list[list[RetrievalHit]]
        ...
```

当前内置组件集中在 `rag_security_lab/components/`。成熟后的真实 embedding、BIPIA、LLM judge、provenance defense 都应沿这一接口添加。

## 推荐的系统性研究顺序

1. 固定 clean baseline、查询划分和运行清单。
2. 先比较同一攻击在 `tfidf / lsa / hybrid_lsa` 下的检索表现。
3. 加入真实 embedding retriever，并保留现有检索器作为可解释 baseline。
4. 将目标问题划分为攻击构造集和未见改写测试集，避免逐字问题泄漏。
5. 在检索命中指标稳定后再运行生成层。
6. 用盲评人工标注或校准后的语义 judge 替代关键词启发式。
7. 最后接入防御组件和 BIPIA 上下文污染任务，统一报告安全性与原任务能力。

## 历史实验

`experiments/` 中的旧脚本仍可单独运行，但它们不具备统一运行清单和防覆盖机制。建议只用于历史结果核对，不再作为新增实验的入口。
