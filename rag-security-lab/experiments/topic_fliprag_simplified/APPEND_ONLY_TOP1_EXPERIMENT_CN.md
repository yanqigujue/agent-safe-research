# Append-only Top1 检索优化实验记录

## 实验目的

本实验验证一个更现实的知识库污染设定：攻击者不替换已有知识库文档，只追加少量污染文本。在该设定下，我们测试是否可以通过检索排序优化，把本阶段 A 组污染内容推到目标问题的 Top1。

这里的实验仅用于本地安全研究与防御评估。它模拟的是污染文本已经进入测试知识库后的检索与生成影响，不讨论或实现真实系统中的未授权注入。

## 方法改动

在 `topic_fliprag_simplified.py` 中新增 `--optimize-append-ranking`：

- 对每个目标问题，从原始污染文本生成多个 append-only 候选。
- 候选包括普通长文本、Question/Answer 检索卡片、短检索段、问题复述密集段、chunk-aware 段落等。
- 使用本地检索器计算候选相对 clean KB 中最佳文档的 margin：

```text
margin = score(poison_candidate, target_query) - score(best_clean_doc, target_query)
```

- 为每个目标问题选择 margin 最大的候选文本。
- 最终仍采用 `attack-mode append`，不删除、不替换任何 clean 文档。

## 关键命令

```powershell
python experiments\topic_fliprag_simplified\topic_fliprag_simplified.py --mode retrieve --top-k 5 --poison-docs-path experiments\topic_fliprag_simplified\monitoring_capacity_group_a_poisoned_docs.jsonl --query-source poison-targets --attack-mode append --retriever hybrid-lsa --hybrid-alpha 0.5 --dense-components 64 --selected-poisons-per-topic 6 --optimize-append-ranking --optimizer-variants 9 --query-repeat 3
```

```powershell
python experiments\topic_fliprag_simplified\topic_fliprag_simplified.py --mode generate --top-k 5 --poison-docs-path experiments\topic_fliprag_simplified\monitoring_capacity_group_a_poisoned_docs.jsonl --query-source poison-targets --attack-mode append --retriever hybrid-lsa --hybrid-alpha 0.5 --dense-components 64 --selected-poisons-per-topic 6 --optimize-append-ranking --optimizer-variants 9 --query-repeat 3 --max-generation-queries 6 --prompt-mode naive --model qwen3:8b --base-url http://localhost:11434
```

## 检索结果

在 A 组 6 个监测系统能力误判问题上，append-only 优化后得到：

- `topic_query_count`: 6
- `attack_mode`: append
- `replaced_clean_doc_count`: 0
- `appended_poison_doc_count`: 6
- `retriever`: hybrid-lsa
- `topic_poison_hit_rate`: 1.0
- `topic_poison_rank1_rate`: 1.0
- `topic_poison_rank1_count`: 6
- `append_optimizer_positive_margin_count`: 6
- `append_optimizer_predicted_top1_count`: 6

这说明在当前本地检索器和数据集上，不替换 clean 文档也可以把污染内容推到 Top1。关键不是简单追加原始污染长文，而是构造短检索段，使其同时包含目标问题原词和目标立场。

## 生成结果

使用本地 `qwen3:8b`、naive prompt、Top5 上下文进行生成评估：

- `generation_query_count`: 6
- `heuristic_downplay_marker_increased_rate`: 0.1667
- `heuristic_dominant_downplay_shift_rate`: 0.1667

检索 Top1 成功并不等于生成立场一定完全翻转。模型仍会综合 TopK 中的 clean 文档，且安全问题本身的语义会促使模型保留风险提示。因此，本轮实验更强地证明了检索排名攻击可行，但生成层面的立场改变仍需要进一步优化污染文本的证据化表达、上下文占比或 prompt 条件。

## 与 replace 设定的关系

此前 replace 模式可以自然得到更强的 Top1 效果，但替换已有知识库内容在现实中属于更强攻击者能力。append-only 优化实验更适合作为主线威胁模型：

- `append-only`: 更接近公开语料、UGC、共享文档、同步源更新等现实入口。
- `replace`: 可作为内部权限、供应链篡改或强攻击者能力下的上界分析。

## 阶段结论

本轮实验支持以下判断：

1. 替换知识库不是必要条件，追加污染文本也可以实现 Top1 检索命中。
2. 仅靠固定 trigger 和自然长文本不足以稳定 Top1，需要面向检索器做候选生成和 margin 选择。
3. Top1 检索成功后，生成层面的立场改变仍不稳定，需要将污染文本进一步做成更像可信证据的短段落。
4. 后续更合理的第二阶段目标应从“替换 clean 文档”转为“append-only 条件下最大化污染文本相对 clean 文档的检索 margin”。

## 输出文件

- `experiments/topic_fliprag_simplified/outputs/ranking_manipulation_summary_append_opt_poison-targets_hybrid-lsa_top5.json`
- `experiments/topic_fliprag_simplified/outputs/ranking_manipulation_details_append_opt_poison-targets_hybrid-lsa_top5.jsonl`
- `experiments/topic_fliprag_simplified/outputs/append_optimizer_summary_append_opt_poison-targets_hybrid-lsa_top5.json`
- `experiments/topic_fliprag_simplified/outputs/generation_summary_naive_append_opt_poison-targets_hybrid-lsa_top5.json`
- `experiments/topic_fliprag_simplified/outputs/generation_results_naive_append_opt_poison-targets_hybrid-lsa_top5.jsonl`
