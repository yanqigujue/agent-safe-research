const API_BASE =
  import.meta.env.VITE_API_BASE_URL ?? (globalThis.location?.protocol === 'file:' ? 'http://127.0.0.1:8000' : '')

export type ConfigField = {
  name: string
  type: 'str' | 'int' | 'float' | 'bool' | 'list' | 'dict'
  required: boolean
  default: unknown
  description: string
  secret_env: boolean
  required_without_any?: string[]
}

export type NodeExample = {
  name: string
  config: Record<string, unknown>
  note: string
}

export type NodeDescriptor = {
  node_id: string
  category: 'attack' | 'guardrail' | 'model' | 'evaluator' | 'custom'
  summary: string
  inputs: string[]
  outputs: string[]
  metrics: string[]
  artifacts: string[]
  advanced_fields: string[]
  examples: NodeExample[]
  config_fields: ConfigField[]
}

export type GraphNode = {
  name: string
  node_id: string
  config: Record<string, unknown>
}

export type GraphEdge = {
  from: string
  to: string
  condition?: string
  else_to?: string
}

export type ExperimentConfig = {
  experiment_name: string
  dataset_path: string
  output_dir: string
  graph: {
    nodes: GraphNode[]
    edges: GraphEdge[]
  }
}

export type ConfigSummary = {
  path: string
  name: string
  experiment_name: string
  dataset_path: string
  output_dir: string
  node_count: number
  edge_count: number
  updated_at: string
}

export type ConfigDetail = {
  path: string
  name: string
  updated_at: string
  config: ExperimentConfig
  raw_text: string
}

export type DatasetSummary = {
  path: string
  name: string
  extension: string
  size_bytes: number
  updated_at: string
  case_count: number | null
  sample_case_ids: string[]
  valid: boolean
  error?: string
}

export type JobRecord = {
  id: string
  status: 'running' | 'succeeded' | 'failed'
  started_at: string
  finished_at: string | null
  config_path: string
  output_dir: string
  command: string
  stdout: string
  stderr: string
  returncode: number | null
  run_dir: string | null
  report_path: string | null
}

export type RunSummary = {
  run_id: string
  path: string
  updated_at: string
  summary: {
    total_cases?: number
    passed_cases?: number
    failed_cases?: number
    run_id?: string
  }
  report_exists: boolean
  results_size_bytes: number
}

export type CaseSummary = {
  case_id: string
  case_file: string
  input: string
  tags: string[]
  expected_behavior: string | null
  evaluation: {
    passed?: boolean
    label?: string
    score?: number
    reasons?: string[]
  }
  passed: boolean
  error_count: number
  trace_count: number
  halted: boolean
  metrics_keys: string[]
}

export type RunDetail = {
  run_id: string
  path: string
  summary: RunSummary['summary']
  cases: CaseSummary[]
  report_exists: boolean
}

export type ValidationResult = {
  valid: boolean
  issues: string[]
}

export type ModelEndpoint = {
  endpoint_id: string
  name: string
  kind: string
  provider: string
  base_url: string | null
  model: string
  api_key_env: string | null
  capabilities: string[]
  status: 'unchecked' | 'available' | 'unavailable' | 'error' | string
  last_probe_at: string | null
  last_probe_error: string | null
  metadata: Record<string, unknown>
}

export type ModelEndpointProbe = {
  endpoint_id: string
  status: string
  checked_at: string
  models: string[]
  error: string | null
}

export type QaRunResult = {
  run_id: string
  run_type: 'qa'
  input: { prompt: string; case_id?: string | null }
  answer: string
  model_snapshot: Record<string, unknown>
  latency_ms: number
  evaluation: {
    passed: boolean
    label: string
    score: number
    reasons: string[]
  }
  raw: Record<string, unknown>
}

export type QaRunSummary = {
  run_id: string
  run_type: 'qa'
  path: string
  updated_at: string
  prompt: string
  answer: string
  model_snapshot: Record<string, unknown>
  latency_ms: number | null
}

async function apiFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...init?.headers,
    },
    ...init,
  })
  if (!response.ok) {
    const body = await response.json().catch(() => ({ detail: response.statusText }))
    throw new Error(typeof body.detail === 'string' ? body.detail : JSON.stringify(body.detail))
  }
  return response.json() as Promise<T>
}

export const api = {
  catalog: () => apiFetch<{ nodes: NodeDescriptor[]; edge_conditions: string[] }>('/api/catalog'),
  modelEndpoints: () => apiFetch<{ endpoints: ModelEndpoint[] }>('/api/model-endpoints'),
  saveModelEndpoint: (endpoint: ModelEndpoint) =>
    apiFetch<{ endpoint: ModelEndpoint }>('/api/model-endpoints', {
      method: 'POST',
      body: JSON.stringify({ endpoint }),
    }),
  probeModelEndpoint: (endpointId: string) =>
    apiFetch<{ probe: ModelEndpointProbe; endpoint: ModelEndpoint }>(
      `/api/model-endpoints/${encodeURIComponent(endpointId)}/probe`,
      { method: 'POST' },
    ),
  ollamaModels: (baseUrl: string) =>
    apiFetch<{ models: string[] }>(`/api/ollama/models?base_url=${encodeURIComponent(baseUrl)}`),
  runQa: (endpointId: string, prompt: string, temperature = 0) =>
    apiFetch<QaRunResult>('/api/qa/run', {
      method: 'POST',
      body: JSON.stringify({ endpoint_id: endpointId, prompt, temperature }),
    }),
  qaRuns: () => apiFetch<{ runs: QaRunSummary[] }>('/api/qa/runs'),
  qaRun: (runId: string) => apiFetch<QaRunResult>(`/api/qa/runs/${encodeURIComponent(runId)}`),
  configs: () => apiFetch<{ configs: ConfigSummary[] }>('/api/configs'),
  config: (path: string) => apiFetch<ConfigDetail>(`/api/config?path=${encodeURIComponent(path)}`),
  saveConfig: (name: string, config: ExperimentConfig) =>
    apiFetch<ConfigDetail>('/api/configs', {
      method: 'POST',
      body: JSON.stringify({ name, config }),
    }),
  validateConfig: (config: ExperimentConfig) =>
    apiFetch<ValidationResult>('/api/configs/validate', {
      method: 'POST',
      body: JSON.stringify({ config }),
    }),
  datasets: () => apiFetch<{ datasets: DatasetSummary[] }>('/api/datasets'),
  runs: () => apiFetch<{ runs: RunSummary[] }>('/api/runs'),
  run: (runId: string) => apiFetch<RunDetail>(`/api/runs/${encodeURIComponent(runId)}`),
  report: (runId: string) => apiFetch<{ markdown: string }>(`/api/runs/${encodeURIComponent(runId)}/report`),
  case: (runId: string, caseFile: string) =>
    apiFetch<Record<string, unknown>>(`/api/runs/${encodeURIComponent(runId)}/cases/${encodeURIComponent(caseFile)}`),
  jobs: () => apiFetch<{ jobs: JobRecord[] }>('/api/jobs'),
  startRun: (configPath: string, outputDir?: string) =>
    apiFetch<JobRecord>('/api/jobs/run', {
      method: 'POST',
      body: JSON.stringify({ config_path: configPath, output_dir: outputDir || undefined }),
    }),
}
