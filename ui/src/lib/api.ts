const API_BASE =
  import.meta.env.VITE_API_BASE_URL ?? (globalThis.location?.protocol === 'file:' ? 'http://127.0.0.1:8000' : '')

export type ConfigField = {
  name: string
  type: 'str' | 'int' | 'float' | 'bool' | 'list' | 'dict'
  required: boolean
  default: unknown
  description: string
  secret_env: boolean
}

export type NodeDescriptor = {
  node_id: string
  category: 'attack' | 'guardrail' | 'model' | 'evaluator' | 'custom'
  summary: string
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
  configs: () => apiFetch<{ configs: ConfigSummary[] }>('/api/configs'),
  config: (path: string) => apiFetch<ConfigDetail>(`/api/config?path=${encodeURIComponent(path)}`),
  saveConfig: (name: string, config: ExperimentConfig) =>
    apiFetch<ConfigDetail>('/api/configs', {
      method: 'POST',
      body: JSON.stringify({ name, config }),
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
