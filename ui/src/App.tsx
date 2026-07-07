import { useEffect, useMemo, useState } from 'react'
import ReactMarkdown from 'react-markdown'
import {
  ArrowDown,
  ArrowLeft,
  ArrowRight,
  ArrowUp,
  Braces,
  ChevronDown,
  ChevronRight,
  CheckCircle2,
  CircleAlert,
  Database,
  FileJson,
  FileText,
  FolderGit2,
  Gauge,
  GitBranch,
  GripVertical,
  LayoutDashboard,
  ListRestart,
  Loader2,
  MonitorCog,
  Play,
  Plus,
  RefreshCw,
  Save,
  Search,
  Terminal,
  Trash2,
} from 'lucide-react'

import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Separator } from '@/components/ui/separator'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { Textarea } from '@/components/ui/textarea'
import {
  api,
  type CaseSummary,
  type ConfigDetail,
  type ConfigField,
  type ConfigSummary,
  type DatasetSummary,
  type ExperimentConfig,
  type GraphEdge,
  type GraphNode,
  type JobRecord,
  type NodeDescriptor,
  type RunDetail,
  type RunSummary,
} from '@/lib/api'
import { cn } from '@/lib/utils'

type BusyState = 'idle' | 'boot' | 'save' | 'run' | 'load'
type MainTab = 'configure' | 'run' | 'results'
type SidebarSide = 'left' | 'right'
type NativeMenuAction =
  | 'new-config'
  | 'save-config'
  | 'run-experiment'
  | 'refresh-all'
  | 'add-node'
  | 'rebuild-edges'
  | 'view-configure'
  | 'view-run'
  | 'view-results'
  | 'refresh-runtime'
  | 'toggle-left-sidebar'
  | 'toggle-right-sidebar'
  | 'show-about'

const emptyConfig: ExperimentConfig = {
  experiment_name: 'new-formaltrust-run',
  dataset_path: 'examples/data/mock_power_cases.jsonl',
  output_dir: 'runs',
  graph: {
    nodes: [],
    edges: [],
  },
}

const selectClass =
  'h-9 w-full rounded-md border border-input bg-card px-3 text-sm shadow-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring'

const leftSidebarBounds = { min: 220, max: 520 }
const rightSidebarBounds = { min: 260, max: 560 }
const collapsedSidebarWidth = 48

const tabLabels: Record<MainTab, string> = {
  configure: '配置实验',
  run: '运行队列',
  results: '结果查看',
}

const statusLabels: Record<JobRecord['status'], string> = {
  running: '运行中',
  succeeded: '已完成',
  failed: '失败',
}

const typeLabels: Record<ConfigField['type'], string> = {
  str: '文本',
  int: '整数',
  float: '小数',
  bool: '开关',
  list: '列表 JSON',
  dict: '对象 JSON',
}

const categoryLabels: Record<NodeDescriptor['category'], string> = {
  attack: '攻击/扰动',
  custom: '自定义适配',
  evaluator: '评测',
  guardrail: '防护',
  model: '模型',
}

const nodeCopy: Record<string, { label: string; summary: string }> = {
  'attack.template': {
    label: '模板攻击',
    summary: '把原始输入套进指定模板，可用于 prompt injection 或 RAG poisoning 实验。',
  },
  'attack.eair_bench_retrieval': {
    label: 'EAIR 样本检索',
    summary: '加载一个 EAIR-Bench case，并把对应证据写入 retrieval_context。',
  },
  'attack.eair_retrieval_perturbation': {
    label: 'EAIR 检索扰动',
    summary: '对检索证据做删除、截断或乱序，用来测试防护在证据受扰时是否稳定。',
  },
  'attack.eair_claim_extraction_noise': {
    label: 'EAIR 声明噪声',
    summary: '对证据里的 claim 标注做删除或注入，用来模拟抽取错误。',
  },
  'custom.afw_trace_adapter': {
    label: 'AFW Trace 适配器',
    summary: '把原始 agent trace 转成 AFW/CapGuard 能读取的来源、权限消耗和候选动作。',
  },
  'guardrail.afw_capguard': {
    label: 'CapGuard 权限检查',
    summary: '根据 AFW 行或 trace 场景判断每个动作字段是否有足够授权，并记录阻断/放行动作。',
  },
  'guardrail.eair_hard_gate': {
    label: 'EAIR 硬规则检查',
    summary: '只检查动作策略硬约束，例如决策、工具、审批和参数是否合法。',
  },
  'guardrail.eair_evidence_sufficiency': {
    label: 'EAIR 证据充分性',
    summary: '只检查高风险、证据支持动作是否有足够证据。',
  },
  'guardrail.eair_soft_score': {
    label: 'EAIR 风险分数',
    summary: '只计算软风险分数和污染证据路径阈值。',
  },
  'guardrail.eair_full': {
    label: 'EAIR 完整防护',
    summary: '组合硬规则、证据充分性和影响分类，给出完整 EAIR 防护结果。',
  },
  'guardrail.input.noop': {
    label: '输入直通',
    summary: '不修改输入，只记录一个指标，适合作为基线节点。',
  },
  'guardrail.output.noop': {
    label: '输出直通',
    summary: '不修改输出，只记录一个指标，适合作为基线节点。',
  },
  'model.mock': {
    label: '离线 Mock 模型',
    summary: '不调用外部 API，按模板生成固定响应，适合快速调试流程。',
  },
  'model.openai_compatible': {
    label: 'OpenAI 兼容模型',
    summary: '调用兼容 /chat/completions 的模型服务，例如 OpenAI、Azure、Ollama 或 vLLM。',
  },
  'model.eair_bench_agent': {
    label: 'EAIR 确定性 Agent',
    summary: '根据检索证据确定性地产生 EAIR-Bench 候选动作。',
  },
  'model.eair_structured_action_json': {
    label: '结构化动作解析',
    summary: '从模型输出中读取动作 JSON，并转成 EAIR-Bench 的候选动作格式。',
  },
  'evaluate.rules': {
    label: '文本规则评测',
    summary: '按响应中是否包含指定文本来判断通过或失败。',
  },
  'evaluate.afw_runtime': {
    label: 'AFW 运行时评测',
    summary: '把 AFW 运行时字段决策和每个 case 的 oracle 标签进行对比。',
  },
  'evaluate.eair_bench_action': {
    label: 'EAIR 动作评测',
    summary: '根据 EAIR-Bench oracle 和动作策略判断最终动作是否正确。',
  },
  'evaluate.eair_robustness_summary': {
    label: 'EAIR 鲁棒性汇总',
    summary: '汇总检索扰动和 claim 噪声组合后的 EAIR 结果。',
  },
  'evaluate.eair_robustness_sweep': {
    label: 'EAIR 鲁棒性 Sweep',
    summary: '从当前检索状态出发，运行多组扰动配置并输出结果。',
  },
  'evaluate.eair_case_robustness_sweep': {
    label: 'EAIR 多 Case Sweep',
    summary: '跨多个 case/condition 批量运行鲁棒性 sweep。',
  },
}

const fieldCopy: Record<string, { label: string; description: string; placeholder?: string }> = {
  case_id: {
    label: 'Case ID',
    description: '指定要加载的 EAIR-Bench case；留空时从当前 case metadata 自动读取。',
  },
  condition: {
    label: '实验条件',
    description: '指定 EAIR-Bench condition；留空时使用当前 case metadata 中的条件。',
  },
  drop_claims: {
    label: '删除的 Claim',
    description: '要从匹配文档中移除的 claim id 列表，填写 JSON 数组。',
    placeholder: '["claim_1", "claim_2"]',
  },
  inject_claims: {
    label: '注入的 Claim',
    description: '要添加到匹配文档中的 claim id 列表，填写 JSON 数组。',
    placeholder: '["claim_extra"]',
  },
  drop_probability: {
    label: '删除概率',
    description: '每个 claim 被随机删除的概率，范围通常是 0 到 1。',
  },
  candidate_inject_claims: {
    label: '候选注入 Claim',
    description: '随机注入时可选的 claim id 列表，填写 JSON 数组。',
  },
  inject_probability: {
    label: '注入概率',
    description: '每个候选 claim 被随机注入的概率，范围通常是 0 到 1。',
  },
  seed: {
    label: '随机种子',
    description: '固定随机过程，便于复现实验；留空表示不指定。',
  },
  target_doc_id: {
    label: '目标文档 ID',
    description: '只扰动指定 doc_id 的文档；留空时按全部文档或目标 rank 处理。',
  },
  target_rank: {
    label: '目标排名',
    description: '只扰动指定检索排名的文档；留空时不按排名限制。',
  },
  prepend_injected: {
    label: '注入内容前置',
    description: '开启后，注入的 claim 会排在原有 claim 前面。',
  },
  drop_doc_ids: {
    label: '删除的文档 ID',
    description: '要从检索结果中移除的 doc_id 列表，填写 JSON 数组。',
  },
  drop_ranks: {
    label: '删除的排名',
    description: '要从检索结果中移除的原始排名列表，填写 JSON 数组。',
  },
  top_k: {
    label: '保留前 K 条',
    description: '过滤或乱序后只保留前 K 条证据；留空表示不截断。',
  },
  shuffle: {
    label: '打乱证据顺序',
    description: '开启后，会在截断前打乱检索文档顺序。',
  },
  attack_type: {
    label: '攻击类型',
    description: '攻击标签，例如 prompt_injection 或 rag_poisoning。',
  },
  template: {
    label: '输入模板',
    description: '包裹原始输入的模板，可使用 {input} 和 {case_id} 占位符。',
  },
  poison_document: {
    label: '污染文档',
    description: '当攻击类型为 rag_poisoning 时，用这里的文本替换污染文档内容。',
  },
  trace_key: {
    label: 'Trace 事件来源',
    description: '从 case metadata 或 metrics 中读取原始 trace 的字段名。当前示例使用 agent_trace_events。',
  },
  event_type_key: {
    label: '事件类型字段',
    description: '每条 trace 事件里表示“事件类型”的字段名。当前示例使用 event_type。',
  },
  schema_preset: {
    label: 'Trace 格式',
    description: '原始 trace 的结构预设。canonical 是标准格式，span_log_v1 用于 span 日志格式。',
  },
  source_event_type: {
    label: '来源事件类型',
    description: '哪些 trace 事件代表“权限来源”或“授权依据”。',
  },
  candidate_action_event_type: {
    label: '候选动作事件类型',
    description: '哪些 trace 事件代表 agent 准备执行的候选动作。',
  },
  consumption_event_type: {
    label: '权限消耗事件类型',
    description: '哪些 trace 事件代表动作字段消耗了某项权限。',
  },
  counter_authority_event_type: {
    label: '反向权限事件类型',
    description: '哪些 trace 事件代表禁止、撤销或反向约束。',
  },
  rows_path: {
    label: 'AFW 行文件',
    description: '可选。直接评测已有的 paired-row JSON 文件；留空时使用当前状态中的行。',
  },
  trace_scenarios_path: {
    label: 'Trace 场景文件',
    description: '可选。读取 trace scenario JSON，并由适配器转换后评测。',
  },
  include_trace_generated: {
    label: '包含 Trace 生成行',
    description: '开启后，会把 trace scenario 派生出的 authority-confusion 行一起纳入评测。',
  },
  baselines: {
    label: '对照基线',
    description: '要和 CapGuard 一起汇总的 baseline 名称列表，填写 JSON 数组。',
    placeholder: '["baseline_name"]',
  },
  runtime_enforce_obligations: {
    label: '强制履行义务',
    description: '开启后，运行时权限检查必须确认 capability obligations 已被满足。',
  },
  runtime_block_final_action: {
    label: '阻断最终动作',
    description: '开启后，block/abstain 决策会把候选动作替换成人工复核 final_action。',
  },
  runtime_final_action_mode: {
    label: '最终动作策略',
    description: 'strict_block 会整体阻断；fieldwise_repair 会按字段修复后生成最终动作。',
  },
  min_behmatch: {
    label: '最低 BehMatch',
    description: 'AFW BehMatch 达到这个分数才算通过，通常填 0 到 1。',
  },
  require_no_false_allow: {
    label: '禁止误放行',
    description: '开启后，任何应阻断字段被放行都会导致 case 失败。',
  },
  max_eair: {
    label: 'EAIR 阈值',
    description: 'EAIR 风险分数高于该值时触发防护。',
  },
  max_path_poison: {
    label: '污染路径阈值',
    description: '证据支持路径中污染比例高于该值时触发防护。',
  },
  action_json: {
    label: '动作 JSON',
    description: '模型输出的原始动作 JSON；留空时从 state.model_response.content 读取。',
  },
  model: {
    label: '模型 ID',
    description: '调用或记录的模型名称。OpenAI 兼容模型会把这个值发送给接口。',
  },
  response_template: {
    label: '响应模板',
    description: 'Mock 模型返回内容的模板，可使用 {input}、{prompt} 和 {case_id}。',
  },
  base_url: {
    label: '接口 Base URL',
    description: 'OpenAI 兼容接口地址，不要包含末尾的 /chat/completions。',
  },
  api_key_env: {
    label: 'API Key 环境变量',
    description: '保存 API key 的环境变量名称。配置文件只保存变量名，不保存密钥本身。',
  },
  temperature: {
    label: '采样温度',
    description: '控制输出随机性。0 更稳定，较高数值更发散。',
  },
  timeout_seconds: {
    label: '请求超时',
    description: '模型接口请求的超时时间，单位为秒。',
  },
  pass_if_contains: {
    label: '通过关键词',
    description: '响应包含这段文本时判为通过；留空表示不使用该规则。',
  },
  fail_if_contains: {
    label: '失败关键词',
    description: '响应包含这段文本时判为失败；留空表示不使用该规则。',
  },
  cases: {
    label: 'Case 配置',
    description: '要 sweep 的 case/condition 配置列表，填写 JSON 数组。',
  },
  case_selector: {
    label: 'Case 选择器',
    description: '从 EAIR-Bench 中筛选 case 的条件，填写 JSON 对象。',
  },
  coverage: {
    label: '覆盖要求',
    description: '最低 case 覆盖要求，填写 JSON 对象。',
  },
  sweep: {
    label: 'Sweep 配置',
    description: '共享的 evaluate.eair_robustness_sweep 配置，填写 JSON 对象。',
  },
  runs: {
    label: 'Sweep 运行列表',
    description: '必填。每次 sweep 的运行配置列表，填写 JSON 数组。',
  },
  output_dir: {
    label: '输出目录',
    description: '保存 JSON/CSV 等产物的目录；留空时使用实验默认输出目录。',
  },
  gate: {
    label: '共享防护配置',
    description: '传给 guardrail.eair_full 的共享配置，填写 JSON 对象。',
  },
  seed_grid: {
    label: '随机种子网格',
    description: '检索扰动和 claim 噪声使用的 seed 组合，填写 JSON 对象。',
  },
}

function cloneConfig(config: ExperimentConfig): ExperimentConfig {
  return JSON.parse(JSON.stringify(config)) as ExperimentConfig
}

function formatDate(value: string | null | undefined) {
  if (!value) return '等待中'
  return new Intl.DateTimeFormat('zh-CN', {
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  }).format(new Date(value))
}

function statusVariant(status: JobRecord['status']) {
  if (status === 'succeeded') return 'success'
  if (status === 'failed') return 'destructive'
  return 'warning'
}

function caseVariant(caseRow: CaseSummary) {
  if (caseRow.error_count > 0 || caseRow.halted || !caseRow.passed) return 'destructive'
  return 'success'
}

function fieldValueToText(value: unknown, field: ConfigField) {
  if (value === undefined || value === null) {
    if (field.default === undefined || field.default === null) return ''
    return field.type === 'list' || field.type === 'dict' ? JSON.stringify(field.default, null, 2) : String(field.default)
  }
  if (field.type === 'list' || field.type === 'dict') return JSON.stringify(value, null, 2)
  return String(value)
}

function parseFieldValue(raw: string, field: ConfigField): unknown {
  if (field.type === 'int') return Number.parseInt(raw || '0', 10)
  if (field.type === 'float') return Number.parseFloat(raw || '0')
  if (field.type === 'list' || field.type === 'dict') return raw.trim() ? JSON.parse(raw) : field.type === 'list' ? [] : {}
  return raw
}

function clamp(value: number, min: number, max: number) {
  return Math.min(Math.max(value, min), max)
}

function fallbackLabel(identifier: string) {
  return identifier
    .split(/[._-]/)
    .filter(Boolean)
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(' ')
}

function getNodeCopy(descriptor: NodeDescriptor) {
  return nodeCopy[descriptor.node_id] ?? { label: fallbackLabel(descriptor.node_id), summary: descriptor.summary }
}

function getFieldCopy(descriptor: NodeDescriptor, field: ConfigField) {
  return fieldCopy[`${descriptor.node_id}.${field.name}`] ?? fieldCopy[field.name] ?? {
    label: fallbackLabel(field.name),
    description: field.description,
  }
}

function getCategoryLabel(category: string) {
  return categoryLabels[category as NodeDescriptor['category']] ?? category
}

function getNodeOptionText(descriptor: NodeDescriptor) {
  const copy = getNodeCopy(descriptor)
  return `${copy.label} - ${descriptor.node_id}`
}

function App() {
  const [catalog, setCatalog] = useState<NodeDescriptor[]>([])
  const [edgeConditions, setEdgeConditions] = useState<string[]>([])
  const [configs, setConfigs] = useState<ConfigSummary[]>([])
  const [datasets, setDatasets] = useState<DatasetSummary[]>([])
  const [runs, setRuns] = useState<RunSummary[]>([])
  const [jobs, setJobs] = useState<JobRecord[]>([])
  const [selectedConfig, setSelectedConfig] = useState<ConfigDetail | null>(null)
  const [draft, setDraft] = useState<ExperimentConfig>(emptyConfig)
  const [saveName, setSaveName] = useState('new-formaltrust-run')
  const [dirty, setDirty] = useState(false)
  const [busy, setBusy] = useState<BusyState>('boot')
  const [notice, setNotice] = useState<string | null>(null)
  const [tab, setTab] = useState<MainTab>('configure')
  const [selectedRun, setSelectedRun] = useState<RunDetail | null>(null)
  const [selectedReport, setSelectedReport] = useState('')
  const [selectedCase, setSelectedCase] = useState<Record<string, unknown> | null>(null)
  const [caseFilter, setCaseFilter] = useState('')
  const [leftSidebarOpen, setLeftSidebarOpen] = useState(true)
  const [rightSidebarOpen, setRightSidebarOpen] = useState(true)
  const [leftSidebarWidth, setLeftSidebarWidth] = useState(300)
  const [rightSidebarWidth, setRightSidebarWidth] = useState(360)
  const [mainPanelResizeEdge, setMainPanelResizeEdge] = useState<SidebarSide | null>(null)

  const nodeById = useMemo(() => new Map(catalog.map((node) => [node.node_id, node])), [catalog])
  const groupedCatalog = useMemo(() => {
    return catalog.reduce<Record<string, NodeDescriptor[]>>((groups, node) => {
      groups[node.category] = groups[node.category] ? [...groups[node.category], node] : [node]
      return groups
    }, {})
  }, [catalog])
  const latestJob = jobs[0]
  const latestRun = runs[0]
  const workbenchColumns = `${leftSidebarOpen ? leftSidebarWidth : collapsedSidebarWidth}px 14px minmax(0, 1fr) 14px ${
    rightSidebarOpen ? rightSidebarWidth : collapsedSidebarWidth
  }px`
  const filteredCases = useMemo(() => {
    if (!selectedRun) return []
    const query = caseFilter.trim().toLowerCase()
    if (!query) return selectedRun.cases
    return selectedRun.cases.filter((caseRow) => {
      return (
        caseRow.case_id.toLowerCase().includes(query) ||
        caseRow.tags.some((tag) => tag.toLowerCase().includes(query)) ||
        (caseRow.evaluation.label || '').toLowerCase().includes(query)
      )
    })
  }, [caseFilter, selectedRun])

  useEffect(() => {
    void bootstrap()
  }, [])

  useEffect(() => {
    if (!jobs.some((job) => job.status === 'running')) return
    const timer = window.setInterval(() => {
      void refreshRuntime()
    }, 2000)
    return () => window.clearInterval(timer)
  }, [jobs])

  async function bootstrap() {
    setBusy('boot')
    setNotice(null)
    try {
      const [catalogResponse, configResponse, datasetResponse, runResponse, jobResponse] = await Promise.all([
        api.catalog(),
        api.configs(),
        api.datasets(),
        api.runs(),
        api.jobs(),
      ])
      setCatalog(catalogResponse.nodes)
      setEdgeConditions(catalogResponse.edge_conditions)
      setConfigs(configResponse.configs)
      setDatasets(datasetResponse.datasets)
      setRuns(runResponse.runs)
      setJobs(jobResponse.jobs)
      if (configResponse.configs[0]) {
        await loadConfig(configResponse.configs[0].path)
      }
      if (runResponse.runs[0]) {
        await loadRun(runResponse.runs[0].run_id)
      }
    } catch (error) {
      setNotice(error instanceof Error ? error.message : String(error))
    } finally {
      setBusy('idle')
    }
  }

  async function refreshRuntime() {
    const [jobResponse, runResponse] = await Promise.all([api.jobs(), api.runs()])
    setJobs(jobResponse.jobs)
    setRuns(runResponse.runs)
  }

  async function refreshConfigs() {
    const configResponse = await api.configs()
    setConfigs(configResponse.configs)
  }

  function createNewConfig() {
    setSelectedConfig(null)
    setDraft(cloneConfig(emptyConfig))
    setSaveName(emptyConfig.experiment_name)
    setDirty(true)
    setTab('configure')
  }

  async function loadConfig(path: string) {
    setBusy('load')
    setNotice(null)
    try {
      const detail = await api.config(path)
      setSelectedConfig(detail)
      setDraft(cloneConfig(detail.config))
      setSaveName(detail.config.experiment_name)
      setDirty(false)
    } catch (error) {
      setNotice(error instanceof Error ? error.message : String(error))
    } finally {
      setBusy('idle')
    }
  }

  function editDraft(mutator: (next: ExperimentConfig) => void) {
    setDraft((current) => {
      const next = cloneConfig(current)
      mutator(next)
      return next
    })
    setDirty(true)
  }

  function updateNode(index: number, patch: Partial<GraphNode>) {
    editDraft((next) => {
      next.graph.nodes[index] = { ...next.graph.nodes[index], ...patch }
    })
  }

  function updateNodeConfig(index: number, field: ConfigField, rawValue: string | boolean) {
    try {
      editDraft((next) => {
        const node = next.graph.nodes[index]
        const nextConfig = { ...node.config }
        if (typeof rawValue === 'boolean') {
          nextConfig[field.name] = rawValue
        } else if (rawValue.trim() === '' && !field.required) {
          delete nextConfig[field.name]
        } else {
          nextConfig[field.name] = parseFieldValue(rawValue, field)
        }
        node.config = nextConfig
      })
      setNotice(null)
    } catch (error) {
      setNotice(error instanceof Error ? `${field.name} 不是合法值：${error.message}` : String(error))
    }
  }

  function addNode() {
    const firstNode = catalog[0]
    if (!firstNode) return
    editDraft((next) => {
      const name = `${firstNode.category}_${next.graph.nodes.length + 1}`
      next.graph.nodes.push({ name, node_id: firstNode.node_id, config: {} })
      next.graph.edges = linearEdges(next.graph.nodes)
    })
  }

  function removeNode(index: number) {
    editDraft((next) => {
      next.graph.nodes.splice(index, 1)
      next.graph.edges = linearEdges(next.graph.nodes)
    })
  }

  function moveNode(index: number, direction: -1 | 1) {
    editDraft((next) => {
      const target = index + direction
      if (target < 0 || target >= next.graph.nodes.length) return
      const [node] = next.graph.nodes.splice(index, 1)
      next.graph.nodes.splice(target, 0, node)
      next.graph.edges = linearEdges(next.graph.nodes)
    })
  }

  function rebuildEdges() {
    editDraft((next) => {
      next.graph.edges = linearEdges(next.graph.nodes)
    })
  }

  function updateEdge(index: number, patch: Partial<GraphEdge>) {
    editDraft((next) => {
      next.graph.edges[index] = { ...next.graph.edges[index], ...patch }
    })
  }

  function startSidebarResize(side: SidebarSide, startX: number) {
    const startWidth = side === 'left' ? leftSidebarWidth : rightSidebarWidth
    const bounds = side === 'left' ? leftSidebarBounds : rightSidebarBounds

    function handlePointerMove(moveEvent: PointerEvent) {
      const delta = moveEvent.clientX - startX
      const nextWidth = side === 'left' ? startWidth + delta : startWidth - delta
      const clampedWidth = clamp(nextWidth, bounds.min, bounds.max)
      if (side === 'left') {
        setLeftSidebarWidth(clampedWidth)
      } else {
        setRightSidebarWidth(clampedWidth)
      }
    }

    function handlePointerUp() {
      document.body.classList.remove('is-resizing-sidebar')
      window.removeEventListener('pointermove', handlePointerMove)
      window.removeEventListener('pointerup', handlePointerUp)
    }

    document.body.classList.add('is-resizing-sidebar')
    window.addEventListener('pointermove', handlePointerMove)
    window.addEventListener('pointerup', handlePointerUp, { once: true })
  }

  function beginSidebarResize(side: SidebarSide, event: React.PointerEvent<HTMLButtonElement>) {
    event.preventDefault()
    startSidebarResize(side, event.clientX)
  }

  function beginMainPanelEdgeResize(event: React.PointerEvent<HTMLDivElement>) {
    const rect = event.currentTarget.getBoundingClientRect()
    const edgeSize = 12
    if (leftSidebarOpen && event.clientX - rect.left <= edgeSize) {
      event.preventDefault()
      startSidebarResize('left', event.clientX)
    } else if (rightSidebarOpen && rect.right - event.clientX <= edgeSize) {
      event.preventDefault()
      startSidebarResize('right', event.clientX)
    }
  }

  function updateMainPanelResizeEdge(event: React.PointerEvent<HTMLDivElement>) {
    const rect = event.currentTarget.getBoundingClientRect()
    const edgeSize = 12
    const nextEdge =
      leftSidebarOpen && event.clientX - rect.left <= edgeSize
        ? 'left'
        : rightSidebarOpen && rect.right - event.clientX <= edgeSize
          ? 'right'
          : null
    setMainPanelResizeEdge((current) => (current === nextEdge ? current : nextEdge))
  }

  async function saveCurrentConfig() {
    setBusy('save')
    setNotice(null)
    try {
      const detail = await api.saveConfig(saveName, draft)
      setSelectedConfig(detail)
      setDraft(cloneConfig(detail.config))
      setSaveName(detail.config.experiment_name)
      setDirty(false)
      await refreshConfigs()
      setNotice(`已保存：${detail.path}`)
      return detail
    } catch (error) {
      setNotice(error instanceof Error ? error.message : String(error))
      return null
    } finally {
      setBusy('idle')
    }
  }

  async function startRun() {
    setBusy('run')
    setNotice(null)
    try {
      let detail = selectedConfig
      if (dirty || !detail) {
        detail = await api.saveConfig(saveName, draft)
        setSelectedConfig(detail)
        setDraft(cloneConfig(detail.config))
        setDirty(false)
        await refreshConfigs()
      }
      const job = await api.startRun(detail.path, detail.config.output_dir)
      setJobs((current) => [job, ...current.filter((item) => item.id !== job.id)])
      setTab('run')
      setNotice(`已启动任务：${job.id}`)
    } catch (error) {
      setNotice(error instanceof Error ? error.message : String(error))
    } finally {
      setBusy('idle')
    }
  }

  async function loadRun(runId: string) {
    setBusy('load')
    setNotice(null)
    try {
      const [runDetail, report] = await Promise.all([
        api.run(runId),
        api.report(runId).catch(() => ({ markdown: '' })),
      ])
      setSelectedRun(runDetail)
      setSelectedReport(report.markdown)
      setSelectedCase(null)
    } catch (error) {
      setNotice(error instanceof Error ? error.message : String(error))
    } finally {
      setBusy('idle')
    }
  }

  async function loadCase(caseRow: CaseSummary) {
    if (!selectedRun) return
    setNotice(null)
    try {
      const payload = await api.case(selectedRun.run_id, caseRow.case_file)
      setSelectedCase(payload)
    } catch (error) {
      setNotice(error instanceof Error ? error.message : String(error))
    }
  }

  useEffect(() => {
    function handleNativeMenu(event: Event) {
      const action = (event as CustomEvent<NativeMenuAction>).detail
      if (!action) return

      switch (action) {
        case 'new-config':
          createNewConfig()
          break
        case 'save-config':
          void saveCurrentConfig()
          break
        case 'run-experiment':
          void startRun()
          break
        case 'refresh-all':
          void bootstrap()
          break
        case 'add-node':
          addNode()
          break
        case 'rebuild-edges':
          rebuildEdges()
          break
        case 'view-configure':
          setTab('configure')
          break
        case 'view-run':
          setTab('run')
          break
        case 'view-results':
          setTab('results')
          break
        case 'refresh-runtime':
          void refreshRuntime()
          break
        case 'toggle-left-sidebar':
          setLeftSidebarOpen((open) => !open)
          break
        case 'toggle-right-sidebar':
          setRightSidebarOpen((open) => !open)
          break
        case 'show-about':
          setNotice('FormalTrust 本地控制台：用于配置实验、启动运行、查看证据与结果。')
          break
      }
    }

    window.addEventListener('formaltrust:native-menu', handleNativeMenu)
    return () => window.removeEventListener('formaltrust:native-menu', handleNativeMenu)
  })

  return (
    <main className="desktop-shell">
      <div className="workbench-grid" style={{ gridTemplateColumns: workbenchColumns }}>
        <aside className="sidebar-column">
          {leftSidebarOpen ? (
            <ResourcePanel
              configs={configs}
              datasets={datasets}
              selectedConfigPath={selectedConfig?.path}
              onNew={createNewConfig}
              onSelectConfig={(path) => void loadConfig(path)}
              onCollapse={() => setLeftSidebarOpen(false)}
            />
          ) : (
            <SidebarRail
              side="left"
              icon={<FolderGit2 className="size-4" />}
              label="资源"
              onExpand={() => setLeftSidebarOpen(true)}
            />
          )}
        </aside>

        <ResizeHandle
          side="left"
          disabled={!leftSidebarOpen}
          onPointerDown={(event) => beginSidebarResize('left', event)}
        />

        <section className="flex min-h-0 min-w-0 flex-col gap-3 px-2">
          <div className="shrink-0 space-y-2">
            <WorkspaceBar
              activeTab={tab}
              busy={busy}
              dirty={dirty}
              nodeCount={draft.graph.nodes.length}
              selectedConfigPath={selectedConfig?.path}
              onSaveConfig={() => void saveCurrentConfig()}
              onStartRun={() => void startRun()}
            />
            {notice && (
              <div className="rounded-md border border-amber-200 bg-amber-50 px-3 py-2 text-sm text-amber-900">
                {notice}
              </div>
            )}
          </div>

          <div
            className={cn(
              'main-work-panel min-h-0 flex-1 overflow-auto rounded-lg border bg-card/70 p-3',
              mainPanelResizeEdge && 'cursor-col-resize',
            )}
            onPointerDown={beginMainPanelEdgeResize}
            onPointerMove={updateMainPanelResizeEdge}
            onPointerLeave={() => setMainPanelResizeEdge(null)}
          >
            {tab === 'configure' && (
              <ConfigPanel
                draft={draft}
                saveName={saveName}
                selectedConfig={selectedConfig}
                datasets={datasets}
                groupedCatalog={groupedCatalog}
                nodeById={nodeById}
                edgeConditions={edgeConditions}
                onSaveNameChange={setSaveName}
                onDraftChange={editDraft}
                onUpdateNode={updateNode}
                onUpdateNodeConfig={updateNodeConfig}
                onAddNode={addNode}
                onRemoveNode={removeNode}
                onMoveNode={moveNode}
                onRebuildEdges={rebuildEdges}
                onUpdateEdge={updateEdge}
              />
            )}
            {tab === 'run' && <RunPanel jobs={jobs} latestJob={latestJob} onRefresh={() => void refreshRuntime()} />}
            {tab === 'results' && (
              <ResultsPanel
                runs={runs}
                selectedRun={selectedRun}
                selectedReport={selectedReport}
                selectedCase={selectedCase}
                filteredCases={filteredCases}
                caseFilter={caseFilter}
                onCaseFilterChange={setCaseFilter}
                onRunSelect={(runId) => void loadRun(runId)}
                onCaseSelect={(caseRow) => void loadCase(caseRow)}
              />
            )}
          </div>
        </section>

        <ResizeHandle
          side="right"
          disabled={!rightSidebarOpen}
          onPointerDown={(event) => beginSidebarResize('right', event)}
        />

        <aside className="sidebar-column">
          {rightSidebarOpen ? (
            <StatusPanel
              latestJob={latestJob}
              latestRun={latestRun}
              runs={runs}
              onCollapse={() => setRightSidebarOpen(false)}
              onRunSelect={(runId) => {
                setTab('results')
                void loadRun(runId)
              }}
            />
          ) : (
            <SidebarRail
              side="right"
              icon={<Gauge className="size-4" />}
              label="状态"
              onExpand={() => setRightSidebarOpen(true)}
            />
          )}
        </aside>
      </div>
    </main>
  )
}

function SidebarRail({
  side,
  icon,
  label,
  onExpand,
}: {
  side: SidebarSide
  icon: React.ReactNode
  label: string
  onExpand: () => void
}) {
  const arrow = side === 'left' ? <ArrowRight className="size-4" /> : <ArrowLeft className="size-4" />

  return (
    <button
      type="button"
      className="sidebar-rail"
      onClick={onExpand}
      aria-label={`展开${label}栏`}
      title={`展开${label}栏`}
    >
      {icon}
      {arrow}
      <span className="sidebar-rail-label">{label}</span>
    </button>
  )
}

function ResizeHandle({
  side,
  disabled,
  onPointerDown,
}: {
  side: SidebarSide
  disabled?: boolean
  onPointerDown: (event: React.PointerEvent<HTMLButtonElement>) => void
}) {
  return (
    <button
      type="button"
      className={cn('resize-handle', disabled && 'resize-handle-disabled')}
      disabled={disabled}
      onPointerDown={onPointerDown}
      aria-label={side === 'left' ? '拖拽调整左侧栏宽度' : '拖拽调整右侧栏宽度'}
      title={side === 'left' ? '拖拽调整左侧栏宽度' : '拖拽调整右侧栏宽度'}
    >
      <GripVertical className="size-3" />
    </button>
  )
}

function WorkspaceBar({
  activeTab,
  busy,
  dirty,
  nodeCount,
  selectedConfigPath,
  onSaveConfig,
  onStartRun,
}: {
  activeTab: MainTab
  busy: BusyState
  dirty: boolean
  nodeCount: number
  selectedConfigPath: string | undefined
  onSaveConfig: () => void
  onStartRun: () => void
}) {
  const isBusy = busy !== 'idle'
  const icon =
    activeTab === 'configure' ? (
      <LayoutDashboard className="size-4" />
    ) : activeTab === 'run' ? (
      <Terminal className="size-4" />
    ) : (
      <GitBranch className="size-4" />
    )

  return (
    <div className="workspace-bar">
      <div className="min-w-0">
        <div className="flex items-center gap-2 text-sm font-semibold">
          {icon}
          <span>{tabLabels[activeTab]}</span>
        </div>
        <div className="mt-0.5 truncate font-mono text-xs text-muted-foreground">{selectedConfigPath ?? '新配置'}</div>
      </div>
      <div className="flex shrink-0 items-center gap-1.5">
        {dirty && <Badge variant="warning">未保存</Badge>}
        <Button variant="outline" size="icon" onClick={onSaveConfig} disabled={isBusy} aria-label="保存配置" title="保存配置">
          <Save className="size-4" />
        </Button>
        <Button size="icon" onClick={onStartRun} disabled={isBusy || nodeCount === 0} aria-label="运行实验" title="运行实验">
          {busy === 'run' ? <Loader2 className="size-4 animate-spin" /> : <Play className="size-4" />}
        </Button>
      </div>
    </div>
  )
}

function ResourcePanel({
  configs,
  datasets,
  selectedConfigPath,
  onNew,
  onSelectConfig,
  onCollapse,
}: {
  configs: ConfigSummary[]
  datasets: DatasetSummary[]
  selectedConfigPath: string | undefined
  onNew: () => void
  onSelectConfig: (path: string) => void
  onCollapse: () => void
}) {
  const [configsOpen, setConfigsOpen] = useState(true)
  const [datasetsOpen, setDatasetsOpen] = useState(true)

  return (
    <>
      <Card className={cn('flex min-h-0 flex-col', configsOpen ? 'flex-1' : 'shrink-0')}>
        <CardHeader className="shrink-0 pb-3">
          <div className="flex items-start justify-between gap-2">
            <button
              type="button"
              className="section-toggle"
              onClick={() => setConfigsOpen((open) => !open)}
              aria-expanded={configsOpen}
            >
              {configsOpen ? <ChevronDown className="size-4" /> : <ChevronRight className="size-4" />}
              <FolderGit2 className="size-4" />
              <span>实验配置</span>
            </button>
            <Button variant="ghost" size="icon" onClick={onCollapse} aria-label="收起资源栏" title="收起资源栏">
              <ArrowLeft className="size-4" />
            </Button>
          </div>
          <CardDescription>{configs.length} 个可运行 YAML</CardDescription>
        </CardHeader>
        {configsOpen && (
          <CardContent className="flex min-h-0 flex-1 flex-col gap-2">
            <Button variant="outline" className="shrink-0 justify-start" onClick={onNew}>
              <Plus className="size-4" />
              新建配置
            </Button>
            <div className="min-h-0 flex-1 space-y-2 overflow-auto pr-1">
              {configs.map((config) => (
                <button
                  key={config.path}
                  className={cn(
                    'w-full rounded-md border bg-card p-3 text-left text-sm transition-colors hover:bg-muted',
                    selectedConfigPath === config.path && 'border-primary bg-accent',
                  )}
                  onClick={() => onSelectConfig(config.path)}
                >
                  <div className="flex items-center justify-between gap-2">
                    <span className="truncate font-medium">{config.experiment_name}</span>
                    <Badge variant="outline" className="shrink-0 whitespace-nowrap">{config.node_count} 节点</Badge>
                  </div>
                  <div className="mt-1 truncate font-mono text-xs text-muted-foreground">{config.path}</div>
                  <div className="mt-2 truncate text-xs text-muted-foreground">{config.dataset_path}</div>
                </button>
              ))}
            </div>
          </CardContent>
        )}
      </Card>

      <Card className="shrink-0">
        <CardHeader className="pb-3">
          <button
            type="button"
            className="section-toggle"
            onClick={() => setDatasetsOpen((open) => !open)}
            aria-expanded={datasetsOpen}
          >
            {datasetsOpen ? <ChevronDown className="size-4" /> : <ChevronRight className="size-4" />}
            <Database className="size-4" />
            <span>数据集</span>
          </button>
          <CardDescription>{datasets.filter((item) => item.valid).length} 个有效 fixture</CardDescription>
        </CardHeader>
        {datasetsOpen && (
          <CardContent>
            <div className="max-h-56 space-y-2 overflow-auto pr-1">
              {datasets.slice(0, 12).map((dataset) => (
                <div key={dataset.path} className="rounded-md border px-3 py-2 text-xs">
                  <div className="flex items-center justify-between gap-2">
                    <span className="truncate font-medium">{dataset.name}</span>
                    <Badge variant={dataset.valid ? 'success' : 'destructive'}>{dataset.case_count ?? '异常'}</Badge>
                  </div>
                  <div className="mt-1 truncate font-mono text-muted-foreground">{dataset.path}</div>
                </div>
              ))}
            </div>
          </CardContent>
        )}
      </Card>
    </>
  )
}

function ConfigPanel({
  draft,
  saveName,
  selectedConfig,
  datasets,
  groupedCatalog,
  nodeById,
  edgeConditions,
  onSaveNameChange,
  onDraftChange,
  onUpdateNode,
  onUpdateNodeConfig,
  onAddNode,
  onRemoveNode,
  onMoveNode,
  onRebuildEdges,
  onUpdateEdge,
}: {
  draft: ExperimentConfig
  saveName: string
  selectedConfig: ConfigDetail | null
  datasets: DatasetSummary[]
  groupedCatalog: Record<string, NodeDescriptor[]>
  nodeById: Map<string, NodeDescriptor>
  edgeConditions: string[]
  onSaveNameChange: (value: string) => void
  onDraftChange: (mutator: (next: ExperimentConfig) => void) => void
  onUpdateNode: (index: number, patch: Partial<GraphNode>) => void
  onUpdateNodeConfig: (index: number, field: ConfigField, rawValue: string | boolean) => void
  onAddNode: () => void
  onRemoveNode: (index: number) => void
  onMoveNode: (index: number, direction: -1 | 1) => void
  onRebuildEdges: () => void
  onUpdateEdge: (index: number, patch: Partial<GraphEdge>) => void
}) {
  return (
    <div className="space-y-3">
      <Card>
        <CardHeader className="pb-3">
          <CardTitle className="flex items-center gap-2">
            <LayoutDashboard className="size-4" />
            基本信息
          </CardTitle>
          <CardDescription className="font-mono">{selectedConfig?.path ?? '新配置，保存后会写入 examples/ui_configs/'}</CardDescription>
        </CardHeader>
        <CardContent className="grid gap-3 md:grid-cols-2">
          <Field label="实验名称">
            <Input
              value={draft.experiment_name}
              onChange={(event) => {
                onSaveNameChange(event.target.value)
                onDraftChange((next) => {
                  next.experiment_name = event.target.value
                })
              }}
            />
          </Field>
          <Field label="保存文件名">
            <Input value={saveName} onChange={(event) => onSaveNameChange(event.target.value)} />
          </Field>
          <Field label="数据集">
            <select
              className={selectClass}
              value={draft.dataset_path}
              onChange={(event) =>
                onDraftChange((next) => {
                  next.dataset_path = event.target.value
                })
              }
            >
              {datasets.map((dataset) => (
                <option key={dataset.path} value={dataset.path}>
                  {dataset.path}
                </option>
              ))}
            </select>
          </Field>
          <Field label="输出目录">
            <Input
              value={draft.output_dir}
              onChange={(event) =>
                onDraftChange((next) => {
                  next.output_dir = event.target.value
                })
              }
            />
          </Field>
        </CardContent>
      </Card>

      <Card>
        <CardHeader className="flex-row items-center justify-between gap-3 pb-3">
          <div>
            <CardTitle className="flex items-center gap-2">
              <Braces className="size-4" />
              节点流程
            </CardTitle>
            <CardDescription>{draft.graph.nodes.length} 个节点，按顺序执行</CardDescription>
          </div>
          <Button variant="outline" size="sm" onClick={onAddNode}>
            <Plus className="size-4" />
            添加节点
          </Button>
        </CardHeader>
        <CardContent className="space-y-3">
          {draft.graph.nodes.map((node, index) => (
            <div key={`${node.name}-${index}`} className="rounded-lg border bg-background p-3">
              <div className="grid gap-3 lg:grid-cols-[1fr_1.5fr_auto]">
                <Field label="节点名称">
                  <Input value={node.name} onChange={(event) => onUpdateNode(index, { name: event.target.value })} />
                </Field>
                <Field label="节点类型">
                  <select
                    className={selectClass}
                    value={node.node_id}
                    onChange={(event) => onUpdateNode(index, { node_id: event.target.value, config: {} })}
                  >
                    {Object.entries(groupedCatalog).map(([category, nodes]) => (
                      <optgroup key={category} label={getCategoryLabel(category)}>
                        {nodes.map((descriptor) => (
                          <option key={descriptor.node_id} value={descriptor.node_id}>
                            {getNodeOptionText(descriptor)}
                          </option>
                        ))}
                      </optgroup>
                    ))}
                  </select>
                </Field>
                <div className="flex items-end gap-1">
                  <Button variant="outline" size="icon" onClick={() => onMoveNode(index, -1)} disabled={index === 0}>
                    <ArrowUp className="size-4" />
                  </Button>
                  <Button
                    variant="outline"
                    size="icon"
                    onClick={() => onMoveNode(index, 1)}
                    disabled={index === draft.graph.nodes.length - 1}
                  >
                    <ArrowDown className="size-4" />
                  </Button>
                  <Button variant="outline" size="icon" onClick={() => onRemoveNode(index)}>
                    <Trash2 className="size-4" />
                  </Button>
                </div>
              </div>
              <NodeConfigEditor
                descriptor={nodeById.get(node.node_id)}
                node={node}
                onFieldChange={(field, value) => onUpdateNodeConfig(index, field, value)}
              />
            </div>
          ))}
        </CardContent>
      </Card>

      <Card>
        <CardHeader className="flex-row items-center justify-between gap-3 pb-3">
          <div>
            <CardTitle>连线</CardTitle>
            <CardDescription>{draft.graph.edges.length} 条边，支持条件分支</CardDescription>
          </div>
          <Button variant="outline" size="sm" onClick={onRebuildEdges}>
            <ListRestart className="size-4" />
            重建线性流程
          </Button>
        </CardHeader>
        <CardContent className="overflow-auto">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>从</TableHead>
                <TableHead>到</TableHead>
                <TableHead>条件</TableHead>
                <TableHead>否则到</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {draft.graph.edges.map((edge, index) => (
                <TableRow key={`${edge.from}-${edge.to}-${index}`}>
                  <TableCell>
                    <EndpointSelect
                      value={edge.from}
                      nodes={draft.graph.nodes}
                      includeStart
                      onChange={(value) => onUpdateEdge(index, { from: value })}
                    />
                  </TableCell>
                  <TableCell>
                    <EndpointSelect
                      value={edge.to}
                      nodes={draft.graph.nodes}
                      includeEnd
                      onChange={(value) => onUpdateEdge(index, { to: value })}
                    />
                  </TableCell>
                  <TableCell>
                    <select
                      className={selectClass}
                      value={edge.condition ?? ''}
                      onChange={(event) => onUpdateEdge(index, { condition: event.target.value || undefined })}
                    >
                      <option value="">无</option>
                      {edgeConditions.map((condition) => (
                        <option key={condition} value={condition}>
                          {condition}
                        </option>
                      ))}
                    </select>
                  </TableCell>
                  <TableCell>
                    <EndpointSelect
                      value={edge.else_to ?? ''}
                      nodes={draft.graph.nodes}
                      includeEnd
                      includeBlank
                      onChange={(value) => onUpdateEdge(index, { else_to: value || undefined })}
                    />
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  )
}

function NodeConfigEditor({
  descriptor,
  node,
  onFieldChange,
}: {
  descriptor: NodeDescriptor | undefined
  node: GraphNode
  onFieldChange: (field: ConfigField, value: string | boolean) => void
}) {
  if (!descriptor) {
    return <div className="mt-3 rounded-md border border-red-200 bg-red-50 p-3 text-sm text-red-700">未知节点类型。</div>
  }
  const nodeInfo = getNodeCopy(descriptor)
  if (descriptor.config_fields.length === 0) {
    return (
      <div className="mt-3 rounded-md border bg-card px-3 py-2 text-sm">
        <div className="font-medium">{nodeInfo.label}</div>
        <div className="mt-1 text-xs leading-relaxed text-muted-foreground">
          {nodeInfo.summary || '这个节点没有额外参数。'}
        </div>
      </div>
    )
  }
  return (
    <div className="mt-3 space-y-3">
      <div className="rounded-md border bg-card px-3 py-2 text-sm">
        <div className="flex flex-wrap items-center gap-2">
          <span className="font-medium">{nodeInfo.label}</span>
          <Badge variant="outline">{getCategoryLabel(descriptor.category)}</Badge>
          <span className="font-mono text-xs text-muted-foreground">{descriptor.node_id}</span>
        </div>
        <div className="mt-1 text-xs leading-relaxed text-muted-foreground">{nodeInfo.summary}</div>
      </div>

      <div className="grid gap-3 md:grid-cols-2">
        {descriptor.config_fields.map((field) => {
          const value = node.config[field.name] ?? field.default
          const copy = getFieldCopy(descriptor, field)
          return (
            <div key={field.name} className="space-y-1.5">
              <div className="flex min-w-0 flex-wrap items-center gap-2">
                <Label className="text-sm font-medium">{copy.label}</Label>
                {field.required && <Badge variant="warning">必填</Badge>}
                {field.secret_env && <Badge variant="muted">环境变量</Badge>}
                <Badge variant="outline" className="whitespace-nowrap">{typeLabels[field.type]}</Badge>
                <span className="font-mono text-xs text-muted-foreground">{field.name}</span>
              </div>
              {field.type === 'bool' ? (
                <label className="flex h-9 items-center gap-2 rounded-md border bg-card px-3 text-sm">
                  <input
                    type="checkbox"
                    checked={Boolean(value)}
                    onChange={(event) => onFieldChange(field, event.target.checked)}
                  />
                  <span>{value ? '开启' : '关闭'}</span>
                  <span className="font-mono text-xs text-muted-foreground">{value ? 'true' : 'false'}</span>
                </label>
              ) : field.type === 'list' || field.type === 'dict' ? (
                <Textarea
                  className="min-h-20 font-mono text-xs"
                  defaultValue={fieldValueToText(value, field)}
                  placeholder={copy.placeholder}
                  onBlur={(event) => onFieldChange(field, event.target.value)}
                />
              ) : (
                <Input
                  type={field.type === 'int' || field.type === 'float' ? 'number' : 'text'}
                  value={fieldValueToText(value, field)}
                  placeholder={copy.placeholder}
                  onChange={(event) => onFieldChange(field, event.target.value)}
                />
              )}
              <div className="text-xs leading-relaxed text-muted-foreground">{copy.description}</div>
            </div>
          )
        })}
      </div>
    </div>
  )
}

function EndpointSelect({
  value,
  nodes,
  includeStart,
  includeEnd,
  includeBlank,
  onChange,
}: {
  value: string
  nodes: GraphNode[]
  includeStart?: boolean
  includeEnd?: boolean
  includeBlank?: boolean
  onChange: (value: string) => void
}) {
  return (
    <select className={selectClass} value={value} onChange={(event) => onChange(event.target.value)}>
      {includeBlank && <option value="">默认</option>}
      {includeStart && <option value="START">START</option>}
      {nodes.map((node) => (
        <option key={node.name} value={node.name}>
          {node.name}
        </option>
      ))}
      {includeEnd && <option value="END">END</option>}
    </select>
  )
}

function RunPanel({
  jobs,
  latestJob,
  onRefresh,
}: {
  jobs: JobRecord[]
  latestJob: JobRecord | undefined
  onRefresh: () => void
}) {
  return (
    <div className="space-y-3">
      <Card>
        <CardHeader className="flex-row items-center justify-between gap-3 pb-3">
          <div>
            <CardTitle className="flex items-center gap-2">
              <Terminal className="size-4" />
              运行队列
            </CardTitle>
            <CardDescription>当前 API 会话中的 {jobs.length} 个任务</CardDescription>
          </div>
          <Button variant="outline" size="sm" onClick={onRefresh}>
            <RefreshCw className="size-4" />
            刷新运行状态
          </Button>
        </CardHeader>
        <CardContent className="overflow-auto">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>状态</TableHead>
                <TableHead>配置</TableHead>
                <TableHead>开始时间</TableHead>
                <TableHead>输出目录</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {jobs.map((job) => (
                <TableRow key={job.id}>
                  <TableCell>
                    <Badge variant={statusVariant(job.status)}>{statusLabels[job.status]}</Badge>
                  </TableCell>
                  <TableCell className="max-w-[260px] truncate font-mono text-xs">{job.config_path}</TableCell>
                  <TableCell>{formatDate(job.started_at)}</TableCell>
                  <TableCell className="max-w-[260px] truncate font-mono text-xs">{job.run_dir ?? '等待输出'}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>

      <Card>
        <CardHeader className="pb-3">
          <CardTitle>命令输出</CardTitle>
          <CardDescription className="font-mono">{latestJob?.command ?? '还没有选择任务'}</CardDescription>
        </CardHeader>
        <CardContent>
          <pre className="min-h-80 overflow-auto rounded-md bg-slate-950 p-4 text-xs leading-relaxed text-slate-100">
            {latestJob ? `${latestJob.stdout}\n${latestJob.stderr}`.trim() || '等待输出' : '还没有运行任务'}
          </pre>
        </CardContent>
      </Card>
    </div>
  )
}

function ResultsPanel({
  runs,
  selectedRun,
  selectedReport,
  selectedCase,
  filteredCases,
  caseFilter,
  onCaseFilterChange,
  onRunSelect,
  onCaseSelect,
}: {
  runs: RunSummary[]
  selectedRun: RunDetail | null
  selectedReport: string
  selectedCase: Record<string, unknown> | null
  filteredCases: CaseSummary[]
  caseFilter: string
  onCaseFilterChange: (value: string) => void
  onRunSelect: (runId: string) => void
  onCaseSelect: (caseRow: CaseSummary) => void
}) {
  return (
    <div className="grid gap-3 2xl:grid-cols-[300px_minmax(0,1fr)]">
      <Card className="2xl:sticky 2xl:top-0">
        <CardHeader className="pb-3">
          <CardTitle className="flex items-center gap-2">
            <GitBranch className="size-4" />
            运行结果
          </CardTitle>
          <CardDescription>{runs.length} 个 run 文件夹</CardDescription>
        </CardHeader>
        <CardContent className="max-h-[680px] space-y-2 overflow-auto pr-1">
          {runs.map((run) => (
            <button
              key={run.run_id}
              className={cn(
                'w-full rounded-md border bg-card p-3 text-left text-sm hover:bg-muted',
                selectedRun?.run_id === run.run_id && 'border-primary bg-accent',
              )}
              onClick={() => onRunSelect(run.run_id)}
            >
              <div className="truncate font-mono text-xs font-medium">{run.run_id}</div>
              <div className="mt-2 flex flex-wrap gap-2">
                <Badge variant="success">{run.summary.passed_cases ?? 0} 通过</Badge>
                <Badge variant={(run.summary.failed_cases ?? 0) > 0 ? 'destructive' : 'muted'}>
                  {run.summary.failed_cases ?? 0} 失败
                </Badge>
              </div>
            </button>
          ))}
        </CardContent>
      </Card>

      <div className="min-w-0 space-y-3">
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="font-mono text-sm">{selectedRun?.run_id ?? '还没有选择 run'}</CardTitle>
            <CardDescription>
              {selectedRun
                ? `${selectedRun.summary.total_cases ?? 0} 个 case，${selectedRun.summary.failed_cases ?? 0} 个失败`
                : '从左侧选择一次运行结果。'}
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="relative">
              <Search className="pointer-events-none absolute left-3 top-2.5 size-4 text-muted-foreground" />
              <Input
                className="pl-9"
                placeholder="按 case id、tag、label 搜索"
                value={caseFilter}
                onChange={(event) => onCaseFilterChange(event.target.value)}
              />
            </div>
            <div className="mt-3 max-h-80 overflow-auto rounded-md border bg-card">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>状态</TableHead>
                    <TableHead>Case</TableHead>
                    <TableHead>Label</TableHead>
                    <TableHead>Tags</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {filteredCases.map((caseRow) => (
                    <TableRow key={caseRow.case_id} className="cursor-pointer" onClick={() => onCaseSelect(caseRow)}>
                      <TableCell>
                        <Badge variant={caseVariant(caseRow)}>
                          {caseRow.passed && caseRow.error_count === 0 ? '通过' : '检查'}
                        </Badge>
                      </TableCell>
                      <TableCell className="max-w-[280px] truncate font-mono text-xs font-medium">{caseRow.case_id}</TableCell>
                      <TableCell>{caseRow.evaluation.label ?? '未评估'}</TableCell>
                      <TableCell className="max-w-[260px] truncate">{caseRow.tags.join(', ') || '无'}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          </CardContent>
        </Card>

        <div className="grid gap-3 xl:grid-cols-2">
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="flex items-center gap-2">
                <FileText className="size-4" />
                报告
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="prose prose-sm max-h-[520px] max-w-none overflow-auto rounded-md border bg-background p-4">
                {selectedReport ? <ReactMarkdown>{selectedReport}</ReactMarkdown> : <span className="text-muted-foreground">还没有加载报告。</span>}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="flex items-center gap-2">
                <FileJson className="size-4" />
                Case 明细
              </CardTitle>
            </CardHeader>
            <CardContent>
              <Separator className="mb-3" />
              <pre className="max-h-[520px] overflow-auto rounded-md bg-slate-950 p-4 text-xs leading-relaxed text-slate-100">
                {selectedCase ? JSON.stringify(selectedCase, null, 2) : '点击上方 case 行查看 JSON。'}
              </pre>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}

function StatusPanel({
  latestJob,
  latestRun,
  runs,
  onCollapse,
  onRunSelect,
}: {
  latestJob: JobRecord | undefined
  latestRun: RunSummary | undefined
  runs: RunSummary[]
  onCollapse: () => void
  onRunSelect: (runId: string) => void
}) {
  return (
    <>
      <Card className="shrink-0">
        <CardHeader className="pb-3">
          <div className="flex items-start justify-between gap-2">
            <CardTitle className="flex items-center gap-2">
              <Gauge className="size-4" />
              当前状态
            </CardTitle>
            <Button variant="ghost" size="icon" onClick={onCollapse} aria-label="收起状态栏" title="收起状态栏">
              <ArrowRight className="size-4" />
            </Button>
          </div>
          <CardDescription>本地 API 会话</CardDescription>
        </CardHeader>
        <CardContent className="grid gap-2">
          <MiniMetric
            icon={<MonitorCog className="size-4" />}
            label="最新任务"
            value={latestJob ? statusLabels[latestJob.status] : '无任务'}
            tone={latestJob?.status === 'failed' ? 'bad' : latestJob?.status === 'running' ? 'warn' : 'good'}
          />
          <MiniMetric
            icon={<CheckCircle2 className="size-4" />}
            label="最近通过"
            value={`${latestRun?.summary.passed_cases ?? 0}`}
            tone="good"
          />
          <MiniMetric
            icon={<CircleAlert className="size-4" />}
            label="最近失败"
            value={`${latestRun?.summary.failed_cases ?? 0}`}
            tone={(latestRun?.summary.failed_cases ?? 0) > 0 ? 'bad' : 'muted'}
          />
        </CardContent>
      </Card>

      <Card className="flex min-h-0 flex-1 flex-col">
        <CardHeader className="shrink-0 pb-3">
          <CardTitle className="flex items-center gap-2">
            <Terminal className="size-4" />
            任务日志
          </CardTitle>
          <CardDescription className="font-mono">{latestJob ? latestJob.id : '暂无任务'}</CardDescription>
        </CardHeader>
        <CardContent className="flex min-h-0 flex-1 flex-col gap-3">
          {latestJob ? (
            <>
              <div className="flex items-center justify-between">
                <Badge variant={statusVariant(latestJob.status)}>{statusLabels[latestJob.status]}</Badge>
                <span className="text-xs text-muted-foreground">{formatDate(latestJob.started_at)}</span>
              </div>
              <pre className="max-h-28 overflow-auto rounded-md bg-slate-950 p-3 text-xs text-slate-100">
                {latestJob.command}
              </pre>
              <pre className="min-h-0 flex-1 overflow-auto rounded-md border bg-background p-3 text-xs">
                {(latestJob.stdout || latestJob.stderr || '等待输出').trim()}
              </pre>
            </>
          ) : (
            <div className="text-sm text-muted-foreground">还没有通过界面启动任务。</div>
          )}
        </CardContent>
      </Card>

      <Card className="shrink-0">
        <CardHeader className="pb-3">
          <CardTitle>最近结果</CardTitle>
          <CardDescription>{runs.length} 个 run</CardDescription>
        </CardHeader>
        <CardContent className="max-h-52 space-y-2 overflow-auto pr-1">
          {runs.slice(0, 6).map((run) => (
            <button
              key={run.run_id}
              className="w-full rounded-md border px-3 py-2 text-left text-xs hover:bg-muted"
              onClick={() => onRunSelect(run.run_id)}
            >
              <div className="truncate font-mono font-medium">{run.run_id}</div>
              <div className="mt-1 flex items-center gap-2 text-muted-foreground">
                <span>{run.summary.passed_cases ?? 0} 通过</span>
                <span>{run.summary.failed_cases ?? 0} 失败</span>
              </div>
            </button>
          ))}
        </CardContent>
      </Card>
    </>
  )
}

function Field({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div className="space-y-1.5">
      <Label>{label}</Label>
      {children}
    </div>
  )
}

function MiniMetric({
  icon,
  label,
  value,
  tone,
}: {
  icon: React.ReactNode
  label: string
  value: string
  tone: 'good' | 'warn' | 'bad' | 'muted'
}) {
  const toneClass = {
    good: 'bg-emerald-50 text-emerald-700 border-emerald-200',
    warn: 'bg-amber-50 text-amber-800 border-amber-200',
    bad: 'bg-red-50 text-red-700 border-red-200',
    muted: 'bg-muted text-muted-foreground border-border',
  }[tone]
  return (
    <div className={cn('flex items-center justify-between rounded-md border px-3 py-2', toneClass)}>
      <div className="flex items-center gap-2 text-xs">
        {icon}
        {label}
      </div>
      <div className="text-sm font-semibold">{value}</div>
    </div>
  )
}

function linearEdges(nodes: GraphNode[]): GraphEdge[] {
  if (nodes.length === 0) return []
  const edges: GraphEdge[] = [{ from: 'START', to: nodes[0].name }]
  for (let index = 0; index < nodes.length - 1; index += 1) {
    edges.push({ from: nodes[index].name, to: nodes[index + 1].name })
  }
  edges.push({ from: nodes[nodes.length - 1].name, to: 'END' })
  return edges
}

export default App
