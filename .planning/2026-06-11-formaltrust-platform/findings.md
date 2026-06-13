# FormalTrust Platform Findings

## Repository Context
- Current workspace is an initial Git repository with no commits.
- Existing root planning files are for a prior RAG poisoning research task and show encoding corruption in terminal output; they should be left untouched.
- The implementation should be added as a new package beside existing report-generation artifacts.

## Dependency Check
- Local Python already has `pydantic`, `yaml`, `typer`, `httpx`, `langgraph`, and `pytest` available.
- LangGraph official docs describe `StateGraph` as a graph where nodes read/write shared state and return partial state updates.

## Implementation Priorities
- Easy integration beats feature breadth.
- Friendly diagnostics are required when a plugin node returns invalid fields or a config references unknown nodes.
- The first acceptance demo must not depend on external API keys or network calls.

## Final Implementation Notes
- `formaltrust_platform` now exposes config loading, a node registry, LangGraph graph building, serial experiment running, JSONL data loading, JSON artifacts, and Markdown reports.
- Built-in nodes cover template attacks, input/output no-op guardrails, mock model calls, OpenAI-compatible model calls, and rule-based evaluation.
- Example node templates are provided for model, attack, and evaluator extension.
- Verification passed with `pytest -q` and `python -m formaltrust_platform run --config examples/mock_validation.yaml --output-dir .tmp_cli_runs`.
