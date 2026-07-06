# AFW Production Chain Report

This report validates a manifest for the implementation-plan style multi-model RAG chain. It is a deployment-readiness artifact, not evidence that live services were launched.

## Summary

| Metric | Value |
|---|---|
| scenario | power_equipment_ops_kb_qa |
| model_roles_present | ['embedding', 'generation', 'rerank'] |
| required_model_roles_covered | True |
| rag_flow_contains_guardrail | True |
| estimated_model_memory_gb | 20.0 |
| max_total_model_memory_gb | 22.0 |
| gpu_memory_gb | 24.0 |
| memory_budget_passes | True |
| api_compatibility_passes | True |
| concurrency_target | 32 |
| production_readiness_status | manifest_validated_not_live_deployment |

## Model Chain

| Role | Model | API | Estimated memory GB | Input | Output |
|---|---|---|---:|---|---|
| embedding | bge-large-zh-v1.5 | embeddings | 2 | uploaded_manual_chunks | vector_index |
| generation | qwen2.5-7b-instruct | chat_completions | 14 | ranked_fragments | answer_or_action_field |
| rerank | bge-reranker-large | rerank | 4 | retrieved_fragments | ranked_fragments |

## Flow

document_upload -> embedding_retrieval -> rerank -> generation -> afw_capguard -> evaluate_afw_runtime

## Boundary

Use this as evidence that the production-chain assumptions are explicit and machine-checkable. Do not claim live deployment, real GPU saturation, or real concurrent-user service behavior from this report alone.
