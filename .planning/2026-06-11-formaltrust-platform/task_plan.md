# FormalTrust Modular Validation Platform MVP

## Goal
Build a lightweight, easy-to-integrate validation platform foundation for LLM trustworthiness testing. The MVP must run a complete local loop: JSONL test cases -> attack node -> guardrail hooks -> model node -> evaluator node -> local artifacts -> Markdown report.

## Phases
| Phase | Status | Content |
|---|---|---|
| Phase 1 | complete | Create tests and package skeleton for config, state, registry, graph runner, nodes, artifacts, CLI, and examples |
| Phase 2 | complete | Implement MVP platform modules with LangGraph orchestration and Pydantic state contracts |
| Phase 3 | complete | Add examples, templates, and developer documentation for easy module integration |
| Phase 4 | complete | Run verification commands and update this plan with final status |

## Decisions
- Do not overwrite root `task_plan.md`, `findings.md`, or `progress.md`; those belong to the earlier RAG poisoning research task.
- Package name: `formaltrust_platform`.
- CLI target: `formaltrust run --config examples/mock_validation.yaml`.
- MVP validation must pass without API keys by using a Mock model.
- Real model integration is provided via an OpenAI-compatible adapter using `base_url`, `model`, and an API key read from an environment variable.
- Data format: JSONL.
- Graph config: YAML-defined nodes and edges.
- Execution: serial batch; one LangGraph run per case; no automatic retry.
- Plugin approach: Python LangGraph node functions registered by node id, with clear templates for model, attack, and evaluator nodes.
- RAG poisoning is a mock contract test: no real RAG implementation in MVP.
- Guardrail hooks are input and output only, default no-op.

## Errors Encountered
| Error | Attempt | Resolution |
|---|---|---|
| Report read failed because cleanup ran first | Tried reading generated CLI report and deleting `.tmp_cli_runs` in parallel | Re-ran CLI/read/cleanup sequentially |
