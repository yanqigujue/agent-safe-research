from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION_START
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor
from PIL import Image, ImageDraw, ImageFont


OUT_DIR = Path("outputs")
MD_PATH = OUT_DIR / "大模型安全相关技术调研报告_初稿.md"
DOCX_PATH = OUT_DIR / "大模型安全相关技术调研报告_初稿.docx"
ALT_DOCX_PATH = OUT_DIR / "大模型安全相关技术调研报告_初稿_含模型图.docx"
DIAGRAM_PATH = OUT_DIR / "agent_reasoning_state_model.png"


references = [
    ("Wei 等，Chain-of-Thought Prompting Elicits Reasoning in Large Language Models", "https://arxiv.org/abs/2201.11903"),
    ("Wang 等，Self-Consistency Improves Chain of Thought Reasoning in Language Models", "https://arxiv.org/abs/2203.11171"),
    ("Yao 等，Tree of Thoughts: Deliberate Problem Solving with Large Language Models", "https://arxiv.org/abs/2305.10601"),
    ("Besta 等，Graph of Thoughts: Solving Elaborate Problems with Large Language Models", "https://arxiv.org/abs/2308.09687"),
    ("Yao 等，ReAct: Synergizing Reasoning and Acting in Language Models", "https://arxiv.org/abs/2210.03629"),
    ("Shinn 等，Reflexion: Language Agents with Verbal Reinforcement Learning", "https://arxiv.org/abs/2303.11366"),
    ("Schick 等，Toolformer: Language Models Can Teach Themselves to Use Tools", "https://arxiv.org/abs/2302.04761"),
    ("Lewis 等，Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks", "https://arxiv.org/abs/2005.11401"),
    ("Meng 等，Locating and Editing Factual Associations in GPT", "https://rome.baulab.info/"),
    ("Wei 等，Emergent Abilities of Large Language Models", "https://arxiv.org/abs/2206.07682"),
    ("Akyurek 等，What learning algorithm is in-context learning?", "https://arxiv.org/abs/2211.15661"),
    ("Wang 等，The Rise and Potential of Large Language Model Based Agents: A Survey", "https://arxiv.org/abs/2309.07864"),
    ("Park 等，Generative Agents: Interactive Simulacra of Human Behavior", "https://arxiv.org/abs/2304.03442"),
    ("Wu 等，AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation", "https://arxiv.org/abs/2308.08155"),
    ("Shi 等，Prompt Injection attack against LLM-integrated Applications", "https://arxiv.org/abs/2306.05499"),
    ("OWASP，Top 10 for Large Language Model Applications", "https://owasp.org/www-project-top-10-for-large-language-model-applications"),
    ("Andriushchenko 等，AgentHarm: A Benchmark for Measuring Harmfulness of LLM Agents", "https://arxiv.org/abs/2410.09024"),
    ("Zhang 等，SafetyBench: Evaluating the Safety of Large Language Models", "https://arxiv.org/abs/2309.07045"),
    ("Huang 等，TrustLLM: Trustworthiness in Large Language Models", "https://arxiv.org/abs/2401.05561"),
    ("Li 等，System-Level Defense against Indirect Prompt Injection Attacks: An Information Flow Control Perspective", "https://arxiv.org/abs/2409.19091"),
]


lit_table = [
    ["LLM 推理机制", "CoT, Self-Consistency, ToT, GoT, ReAct, Reflexion, LLM planning", "LLM 的推理如何由中间步骤、分支探索、反思和行动反馈组织起来？", "为 S3 推理、S4 计划和 S5 行动之间的关系提供理论基础。"],
    ["机理解释与智能涌现", "Mechanistic Interpretability, Causal Tracing, Activation Patching, Emergent Abilities, In-context Learning", "黑盒性体现在哪里？内部表征、参数记忆、涌现能力与推理行为如何关联？", "说明本阶段不直接建模全部 Transformer 参数，而是把内部表征作为影响因素和调研支撑。"],
    ["Agent 推理机制", "LLM-based Agent, Tool use, Memory-augmented Agent, RAG Agent, Agent workflow", "Agent 相比普通 LLM 多了哪些信息源和行动环节？", "支撑 S1-S7 主链路，突出 RAG、记忆、工具和环境反馈。"],
    ["多智能体协同", "Multi-agent collaboration, AutoGen, CAMEL, agent communication, role-based agents", "多智能体消息如何改变任务分解、角色协同和错误传播路径？", "将 M_t 作为扩展变量，分析跨 Agent 污染和协同目标偏移。"],
    ["形式化建模", "State Transition System, FSM, Causal Graph, Information Flow Control, Formal Verification, Model Checking", "如何把 Agent 推理过程抽象为状态、动作、转移和安全属性？", "支撑层级化状态转移模型与贯穿式安全判定 S8。"],
    ["安全风险与可信测评", "Prompt Injection, RAG Poisoning, Tool Misuse, AgentHarm, SafetyBench, TrustLLM, OWASP LLM Top 10", "哪些风险与推理决策链路直接相关？如何形成可测指标？", "支撑 7 类关键风险、攻击测试框架和指标体系。"],
]


state_table = [
    ["S0", "用户输入接收", "X_t", "记录用户任务、问题、约束或攻击输入", "直接提示注入、越狱诱导、恶意任务伪装"],
    ["S1", "任务理解与上下文构造", "X_t, C_t, H_t", "形成当前任务目标、指令优先级和上下文窗口", "上下文污染、系统指令覆盖、目标偏移"],
    ["S2", "外部知识检索 / 记忆读取", "K_t, R_t, H_t", "调用 RAG、知识库、短期/长期记忆", "RAG 投毒、检索劫持、记忆污染、记忆泄露"],
    ["S3", "大模型推理与中间决策", "X_t, C_t, K_t, R_t, H_t, E_t, M_t", "形成中间判断、归因、候选答案或候选动作", "幻觉、错误归因、证据不一致、目标劫持"],
    ["S4", "计划生成", "C_t, K_t, R_t, H_t", "拆分任务步骤、确定行动顺序和工具策略", "危险计划、错误任务分解、高风险操作路径"],
    ["S5", "工具调用 / 行动执行", "A_t, E_t", "选择工具、传入参数、接收工具结果", "越权调用、参数注入、工具误用、外部副作用"],
    ["S6", "输出生成", "O_t, C_t, K_t, R_t", "生成用户可见文本、建议、报告或解释", "敏感泄露、危险建议、系统提示泄露、幻觉输出"],
    ["S7", "反馈更新 / 记忆写入", "H_t, R_t, E_t", "根据反馈更新历史轨迹或记忆", "错误记忆写入、自我强化、跨会话污染"],
    ["S8", "贯穿式安全判定与约束", "Phi, S_t, A_t, O_t", "在上下文、检索、计划、工具、输出、记忆写入等关键点执行安全判定", "漏报、误报、风险等级错误、策略绕过"],
]


risk_table = [
    ["提示注入", "S0/S1/S6", "攻击者通过用户输入或外部文本混入冲突指令", "改变任务目标、覆盖安全约束、诱导泄露或违规输出", "攻击成功率 ASR、目标偏移率、拒答正确率"],
    ["RAG 投毒", "S2/S3/S6", "污染检索语料或诱导检索命中低可信内容", "错误证据进入上下文，导致幻觉或错误建议被包装为有依据", "投毒命中率、证据一致率、风险发现数量"],
    ["记忆污染", "S2/S7", "将错误事实、偏置指令或敏感信息写入短期/长期记忆", "污染后续推理，形成跨轮次或跨会话风险", "记忆污染触发率、跨轮风险复现率"],
    ["幻觉与错误归因", "S3/S6", "模型在证据不足、证据冲突或上下文噪声下生成确定性判断", "输出不可靠结论，影响电力知识问答和运维辅助判断", "幻觉率、证据溯源失败率、事实一致率"],
    ["工具误调用", "S4/S5", "错误选择工具、越权传参或把不可信内容转化为工具参数", "产生外部副作用、访问越权资源或执行不应执行的动作", "工具误调用率、权限检查覆盖率、参数异常率"],
    ["敏感信息泄露", "S2/S6/S7", "诱导模型泄露系统提示、内部策略、检索内容或记忆中的敏感信息", "暴露内部规则、业务数据或用户隐私", "泄露率、敏感片段命中率、脱敏失败率"],
    ["多智能体错误传播/感染", "S1/S3/S4/S7", "一个 Agent 的错误消息、污染记忆或不当计划被其他 Agent 接收并放大", "形成群体性错误归因、协同目标偏移或跨角色风险传播", "跨 Agent 传播率、协同一致性错误率、风险节点定位准确率"],
]


metric_table = [
    ["形式化一致率", "模型判定的安全相关行为与被测 Agent 实际输出/轨迹的一致程度", "一致样本数 / 有效测试样本数", "提示注入、幻觉、工具误调用、泄露", "直接对齐 80% 建模一致率"],
    ["风险发现数量", "模型化测试框架发现的有效风险点数量", "去重后的有效风险点计数", "全部 7 类风险", "支撑风险发现能力评估"],
    ["风险发现提升率", "相对传统基准新增或提升的风险发现能力", "(本方法风险数 - 基准风险数) / 基准风险数", "RAG 投毒、记忆污染、多智能体传播等传统基准覆盖不足风险", "对齐风险数量提升 10%"],
    ["攻击成功率 ASR", "攻击样本导致目标安全属性被破坏的比例", "成功攻击样本数 / 攻击样本总数", "提示注入、RAG 投毒、工具误调用", "用于衡量攻击测试框架有效性"],
    ["风险节点定位准确率", "测试框架定位的风险状态与人工标注状态一致的比例", "定位正确样本数 / 已定位风险样本数", "全部状态相关风险", "说明模型能支持风险溯源"],
    ["证据一致率", "输出结论与可信检索证据一致的比例", "证据一致输出数 / 需证据支撑输出数", "幻觉、RAG 投毒、电力知识问答风险", "落实电力场景证据溯源要求"],
    ["敏感信息泄露率", "输出或记忆写入中出现敏感信息的比例", "泄露样本数 / 含敏感信息风险样本数", "敏感泄露、系统提示泄露、记忆泄露", "用于安全行为一致率和后续防护验证"],
    ["工具误调用率", "工具选择、权限、参数或调用时机错误的比例", "误调用次数 / 工具调用总次数", "工具误调用、越权调用", "为后续权限控制和外置防护提供依据"],
    ["通用能力下降率", "安全约束或防护引入后正常任务能力下降比例", "(基准能力分 - 防护后能力分) / 基准能力分", "防护副作用", "本阶段预留，后续对齐下降不多于 10%"],
    ["防护后风险下降率", "防护策略部署后风险问题下降比例", "(防护前风险数 - 防护后风险数) / 防护前风险数", "全部可防护风险", "本阶段预留，后续对齐下降至少 20%"],
]


sections = [
    ("研究摘要", [
        "本报告初稿围绕项目研究点 1.1.1“大模型推理决策机制的形式化建模技术研究”展开。当前阶段的核心任务不是开发完整软件系统，也不是立即构建沙盒或 LangGraph 工程，而是先建立能够支撑后续可信性测评、攻击测试和安全防护的理论与模型框架。",
        "报告以大模型推理机制和 Agent 推理机制为起点，结合机理解释、智能涌现、状态空间建模、因果信息流和安全属性定义，提出“面向智能体场景的大模型推理决策机制层级化状态转移模型”。该模型以 S0-S7 表示 Agent 推理决策主链路，以 S8 表示贯穿式安全判定与约束节点，用于解释外部知识、记忆、工具、环境反馈和多智能体消息如何共同影响大模型决策行为。"
    ]),
    ("1. 研究背景与问题定位", [
        "大模型在电力知识问答、运维辅助分析、规程检索和文档生成等场景中具有较强应用潜力，但其黑盒特性、上下文敏感性和生成式输出机制使决策过程难以解释。尤其在 Agent 场景中，大模型不再只是接收输入并生成文本，而是可能读取外部知识、调用工具、写入记忆、接收环境反馈，并与其他智能体交换消息。这使推理决策过程从单轮文本生成转变为多源信息驱动的动态状态演化过程。",
        "因此，本阶段需要解决的核心问题是：如何在不直接建模全部 Transformer 参数的前提下，抽象出大模型及 Agent 的推理决策链路；如何定义状态、变量、动作、转移和安全属性；如何基于该模型定位提示注入、RAG 投毒、记忆污染、工具误调用、幻觉和敏感泄露等关键风险。"
    ]),
    ("2. LLM 推理机制与机理解释调研", [
        "学术界通常通过提示方法和推理轨迹来描述 LLM 的推理行为。CoT 将复杂任务拆解为中间推理步骤，Self-Consistency 通过多条推理路径投票提升稳定性，ToT 和 GoT 将推理从单链扩展为树状或图状搜索，ReAct 将推理与行动交替组织，Reflexion 则强调模型可利用反馈进行反思和改进。这些研究说明，大模型的“推理”并不只是最终输出，而包括中间表示、候选路径、行动反馈和自我修正等过程。",
        "机理解释研究从另一个角度揭示大模型的不可解释性。因果追踪、激活修补和表征分析尝试定位模型内部哪些激活或模块影响事实回忆和输出行为；智能涌现和上下文学习研究则说明，模型能力可能随规模、训练数据和提示形式发生非线性变化。对本项目而言，这些研究的启发是：第一节点不宜承诺精确解释全部参数和层间表征，而应把内部表征、参数记忆和注意力机制作为影响推理决策的底层因素，在 Agent 层面优先建立可观察、可验证的状态转移模型。"
    ]),
    ("3. Agent 场景下推理机制变化", [
        "普通 LLM 的典型输入是用户问题和上下文，输出是文本结果。Agent 场景则增加了外部知识、记忆、工具、环境反馈和多智能体消息等影响因素。RAG 将外部知识 K_t 引入上下文，提升知识覆盖，但也引入检索污染和证据可信性问题；短期与长期记忆 R_t 使 Agent 能跨轮次保持信息，但也可能形成记忆污染和敏感信息泄露；工具调用 A_t 使模型从“说”变成“做”，带来越权、参数注入和外部副作用风险；环境反馈 E_t 会改变后续推理路径，使决策过程具有闭环性。",
        "多智能体协同进一步改变推理机制。多个 Agent 可能承担规划、检索、执行、审查等不同角色，消息 M_t 在智能体之间传播。协同可以提高复杂任务处理能力，但也可能放大错误：一个 Agent 的错误归因、污染记忆或不安全建议可能被其他 Agent 接收、复述、强化，并在协同链路中形成跨 Agent 风险传播。因此，多智能体不宜只作为系统架构问题，而应被纳入推理决策机制模型。"
    ]),
    ("4. 层级化状态转移模型", [
        "本报告建议采用“面向智能体场景的大模型推理决策机制层级化状态转移模型”。模型不把大模型视为单一黑箱输出器，而是将 Agent 执行链路抽象为状态集合 S、输入变量集合 X/C/K/R/H/E/M、动作集合 A、输出 O、转移函数 T 和安全属性集合 Phi。",
        "核心决策函数可写为：O_t, A_t = F_theta(X_t, C_t, K_t, R_t, H_t, E_t, M_t)。其中 F_theta 表示大模型与 Agent 决策策略的组合，X_t 为当前用户输入，C_t 为上下文，K_t 为外部知识或检索内容，R_t 为记忆，H_t 为历史交互轨迹，E_t 为环境或工具反馈，M_t 为多智能体消息，O_t 为文本输出，A_t 为动作或工具调用。",
        "S0-S7 表示主决策链路，S8 不是单独的末端节点，而是贯穿上下文构造、外部知识接入、计划生成、工具调用、输出生成和记忆写入等关键位置的安全判定机制。这样的设计能够避免把安全检查简化为最终输出过滤，并为后续风险定位和可信性测评提供状态依据。"
    ]),
    ("5. 安全属性与电力场景边界", [
        "安全属性 Phi 用于描述模型在不同状态下必须满足的安全行为边界。通用属性包括：不得输出危险或违规建议；不得泄露敏感信息、系统提示词或内部策略；外部检索内容不得覆盖系统安全指令；被污染记忆不得影响高风险决策；高风险工具调用前必须经过权限检查；攻击输入不应导致模型偏离原始任务目标；输出应与可信证据保持一致；安全约束不应显著损伤正常任务能力。",
        "结合电力场景，本阶段增加“证据溯源要求”：电力知识问答和运维辅助建议必须能够关联可信资料、规程或检索证据；当证据不足、证据冲突或来源可信度不足时，模型不得给出确定性处置结论。第一节点以电力知识问答和运维辅助决策为应用示例，不研究实时调度、控制指令生成或自动化执行。"
    ]),
    ("6. 攻击测试与可信性测评框架", [
        "攻击测试框架应从模型状态出发，而不是只从攻击名称出发。测试样本库记录场景、输入、攻击类型、目标状态、预期安全行为、预期风险、风险等级和判定标准；被测对象执行后记录上下文构造、检索内容、记忆读取、推理轨迹摘要、计划、工具调用、输出和记忆写入等关键字段；随后由 S8 安全判定机制判断是否违反安全属性，并计算指标。",
        "本阶段指标体系重点服务两项项目考核目标：其一，安全攸关建模结果与模型实际输出在安全相关行为上的一致率达到 80% 以上；其二，潜在风险发现数量相比传统基准提高 10%。防护后风险下降至少 20% 和通用能力下降不多于 10% 属于后续防护验证指标，本阶段只保留口径，不展开具体防护算法。"
    ]),
    ("7. 后续工作边界", [
        "本阶段不开展完整软件系统设计，不构建沙盒，不编写 LangGraph 工程方案，不设计数据库、API 或前端界面，也不展开具体安全防护算法。后续可基于本阶段模型和风险定位结果，进一步研究安全提示优化、外置防护模块、权限控制、记忆清洗、检索可信性过滤和防护效果验证。",
        "当前阶段的完成标准是形成一份能够向老师说明研究逻辑的报告初稿：为什么要从推理机制出发，为什么 Agent 场景需要状态转移模型，模型如何定义状态和变量，安全风险如何从模型推出，可信测评指标如何对齐项目考核目标。"
    ]),
]


def markdown_table(headers, rows):
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(cell.replace("\n", " ") for cell in row) + " |")
    return "\n".join(lines)


def load_font(size, bold=False):
    candidates = [
        r"C:\Windows\Fonts\msyhbd.ttc" if bold else r"C:\Windows\Fonts\msyh.ttc",
        r"C:\Windows\Fonts\simhei.ttf",
        r"C:\Windows\Fonts\simsun.ttc",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def wrap_text(draw, text, font, max_width):
    lines = []
    current = ""
    for char in text:
        candidate = current + char
        bbox = draw.textbbox((0, 0), candidate, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = char
    if current:
        lines.append(current)
    return lines


def draw_centered_text(draw, box, text, font, fill="#1F2937", line_gap=6):
    x1, y1, x2, y2 = box
    max_width = x2 - x1 - 28
    lines = []
    for raw in text.split("\n"):
        lines.extend(wrap_text(draw, raw, font, max_width))
    heights = [draw.textbbox((0, 0), line, font=font)[3] - draw.textbbox((0, 0), line, font=font)[1] for line in lines]
    total_h = sum(heights) + line_gap * (len(lines) - 1)
    y = y1 + ((y2 - y1) - total_h) / 2
    for line, height in zip(lines, heights):
        bbox = draw.textbbox((0, 0), line, font=font)
        line_w = bbox[2] - bbox[0]
        draw.text((x1 + ((x2 - x1) - line_w) / 2, y), line, font=font, fill=fill)
        y += height + line_gap


def arrow(draw, start, end, fill="#334155", width=4, dashed=False):
    x1, y1 = start
    x2, y2 = end
    if dashed:
        segments = 18
        for i in range(segments):
            if i % 2 == 0:
                sx = x1 + (x2 - x1) * i / segments
                sy = y1 + (y2 - y1) * i / segments
                ex = x1 + (x2 - x1) * (i + 1) / segments
                ey = y1 + (y2 - y1) * (i + 1) / segments
                draw.line((sx, sy, ex, ey), fill=fill, width=width)
    else:
        draw.line((x1, y1, x2, y2), fill=fill, width=width)

    import math

    angle = math.atan2(y2 - y1, x2 - x1)
    head_len = 16
    head_angle = math.pi / 7
    p1 = (
        x2 - head_len * math.cos(angle - head_angle),
        y2 - head_len * math.sin(angle - head_angle),
    )
    p2 = (
        x2 - head_len * math.cos(angle + head_angle),
        y2 - head_len * math.sin(angle + head_angle),
    )
    draw.polygon([end, p1, p2], fill=fill)


def create_model_diagram():
    width, height = 1800, 1180
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)

    title_font = load_font(38, bold=True)
    subtitle_font = load_font(24)
    node_font = load_font(24, bold=True)
    center_font = load_font(34, bold=True)
    small_font = load_font(21)
    tiny_font = load_font(19)

    draw.rectangle((0, 0, width, 112), fill="#F8FAFC")
    draw.text((70, 34), "面向智能体场景的大模型推理决策机制层级化状态转移模型", font=title_font, fill="#0F172A")
    draw.text((72, 82), "S8 置于模型中心，表示其贯穿并约束 Agent 推理决策链路的关键状态", font=subtitle_font, fill="#475569")

    nodes = {
        "S0": (90, 210, 310, 330, "S0\n用户输入接收\nX_t"),
        "S1": (470, 170, 735, 300, "S1\n任务理解与\n上下文构造\nC_t, H_t"),
        "S2": (980, 170, 1255, 300, "S2\n外部知识检索 /\n记忆读取\nK_t, R_t"),
        "S3": (1370, 365, 1645, 500, "S3\n大模型推理与\n中间决策\nFθ(...)"),
        "S4": (1280, 690, 1535, 820, "S4\n计划生成\n任务分解"),
        "S5": (880, 820, 1135, 950, "S5\n工具调用 /\n行动执行\nA_t"),
        "S6": (480, 690, 735, 820, "S6\n输出生成\nO_t"),
        "S7": (165, 440, 430, 570, "S7\n反馈更新 /\n记忆写入\nR_{t+1}, H_{t+1}"),
    }

    node_fill = "#E8F1FB"
    node_border = "#2E74B5"
    for key, (x1, y1, x2, y2, label) in nodes.items():
        draw.rounded_rectangle((x1, y1, x2, y2), radius=18, fill=node_fill, outline=node_border, width=3)
        draw_centered_text(draw, (x1, y1, x2, y2), label, node_font)

    # Main reasoning-decision chain.
    arrow(draw, (310, 270), (470, 240))
    arrow(draw, (735, 235), (980, 235))
    arrow(draw, (1255, 250), (1370, 405))
    arrow(draw, (1510, 500), (1435, 690))
    arrow(draw, (1280, 755), (1135, 870))
    arrow(draw, (880, 875), (735, 755))
    arrow(draw, (480, 740), (430, 545))
    arrow(draw, (300, 440), (540, 300), fill="#64748B", dashed=True)
    draw.text((372, 365), "反馈闭环", font=tiny_font, fill="#64748B")

    # Central security hub.
    s8_box = (735, 420, 1080, 650)
    draw.rounded_rectangle(s8_box, radius=28, fill="#FEE2E2", outline="#B91C1C", width=5)
    draw_centered_text(
        draw,
        (755, 430, 1060, 540),
        "S8\n贯穿式安全判定\n与约束 Φ",
        center_font,
        fill="#7F1D1D",
    )
    draw_centered_text(
        draw,
        (765, 545, 1050, 640),
        "对上下文、检索、推理、计划、工具、输出、记忆写入执行安全属性检查",
        tiny_font,
        fill="#7F1D1D",
    )

    s8_center = (908, 535)
    for target in [
        (600, 300),   # S1
        (1120, 300),  # S2
        (1370, 432),  # S3
        (1280, 740),  # S4
        (1005, 820),  # S5
        (735, 740),   # S6
        (430, 505),   # S7
    ]:
        arrow(draw, s8_center, target, fill="#B91C1C", width=3, dashed=True)

    # Redraw the central node after constraint arrows so S8 remains the visual hub.
    draw.rounded_rectangle(s8_box, radius=28, fill="#FEE2E2", outline="#B91C1C", width=5)
    draw_centered_text(
        draw,
        (755, 430, 1060, 540),
        "S8\n贯穿式安全判定\n与约束 Φ",
        center_font,
        fill="#7F1D1D",
    )
    draw_centered_text(
        draw,
        (765, 545, 1050, 640),
        "对上下文、检索、推理、计划、工具、输出、记忆写入执行安全属性检查",
        tiny_font,
        fill="#7F1D1D",
    )

    # External influences.
    draw.rounded_rectangle((1285, 170, 1690, 305), radius=18, fill="#FFF7ED", outline="#D97706", width=3)
    draw_centered_text(draw, (1285, 170, 1690, 305), "外部影响因素\nE_t：环境/工具反馈\nM_t：多智能体消息", small_font, fill="#7C2D12")
    arrow(draw, (1285, 235), (1255, 235), fill="#D97706", dashed=True)
    arrow(draw, (1490, 305), (1490, 365), fill="#D97706", dashed=True)
    arrow(draw, (1410, 305), (1410, 690), fill="#D97706", dashed=True)

    legend_box = (120, 940, 620, 1080)
    draw.rounded_rectangle(legend_box, radius=16, fill="#F8FAFC", outline="#CBD5E1", width=2)
    draw_centered_text(
        draw,
        legend_box,
        "图示说明\n黑色实线：推理决策状态转移\n红色虚线：S8 安全约束作用\n橙色虚线：外部影响输入",
        tiny_font,
        fill="#334155",
    )

    formula_box = (690, 970, 1600, 1065)
    draw.rounded_rectangle(formula_box, radius=16, fill="#F8FAFC", outline="#CBD5E1", width=2)
    draw_centered_text(
        draw,
        formula_box,
        "形式化表达：O_t, A_t = Fθ(X_t, C_t, K_t, R_t, H_t, E_t, M_t)",
        subtitle_font,
        fill="#0F172A",
    )

    img.save(DIAGRAM_PATH)


def build_markdown():
    parts = [
        "# 大模型安全相关技术调研报告（初稿）",
        "",
        "聚焦研究点：1.1.1 大模型推理决策机制的形式化建模技术研究",
        "",
    ]
    for title, paras in sections:
        parts.append(f"## {title}")
        for para in paras:
            parts.append(para)
            parts.append("")
        if title.startswith("4."):
            parts.append("![图 1 面向智能体场景的大模型推理决策机制层级化状态转移模型](agent_reasoning_state_model.png)")
            parts.append("")
            parts.append("图 1 将 Agent 推理决策过程建模为 S0-S7 主链路，并将 S8 设计为贯穿式安全判定与约束节点，用于表达安全属性 Phi 对上下文、检索、计划、工具、输出和记忆写入等关键环节的约束。")
            parts.append("")
    parts.extend([
        "## 8. 四张核心表",
        "",
        "### 表 1 文献调研任务表",
        markdown_table(["调研方向", "检索关键词", "需回答问题", "研究启发"], lit_table),
        "",
        "### 表 2 状态变量定义表",
        markdown_table(["状态节点", "状态含义", "输入变量", "动作/输出", "安全关注点"], state_table),
        "",
        "### 表 3 关键风险映射表",
        markdown_table(["风险类型", "对应状态", "攻击方式", "影响后果", "可测指标"], risk_table),
        "",
        "### 表 4 测评指标体系表",
        markdown_table(["指标名称", "定义", "计算口径", "对应风险", "项目指标关系"], metric_table),
        "",
        "## 9. 需要老师确认的问题",
        "1. 第一节点模型是否采用 Agent 推理决策状态模型为主，内部表征和参数机制作为调研支撑而不深入建模。",
        "2. “传统基准”具体采用通用 LLM safety benchmark、项目自建基准，还是二者结合。",
        "3. 电力场景是否以电力知识问答和运维辅助决策为主要示例，暂不进入调度/控制类场景。",
        "",
        "## 参考文献与资料来源",
    ])
    for idx, (name, url) in enumerate(references, 1):
        parts.append(f"[{idx}] {name}. {url}")
    parts.append("")
    return "\n".join(parts)


def set_run_font(run, name="Calibri", east_asia="Microsoft YaHei", size=None, color=None, bold=None, italic=None):
    run.font.name = name
    run._element.rPr.rFonts.set(qn("w:ascii"), name)
    run._element.rPr.rFonts.set(qn("w:hAnsi"), name)
    run._element.rPr.rFonts.set(qn("w:eastAsia"), east_asia)
    if size is not None:
        run.font.size = Pt(size)
    if color is not None:
        run.font.color.rgb = RGBColor.from_string(color)
    if bold is not None:
        run.bold = bold
    if italic is not None:
        run.italic = italic


def set_paragraph_spacing(paragraph, before=0, after=6, line=1.10):
    paragraph.paragraph_format.space_before = Pt(before)
    paragraph.paragraph_format.space_after = Pt(after)
    paragraph.paragraph_format.line_spacing = line


def shade_cell(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), fill)
    tc_pr.append(shd)


def set_cell_margins(cell, top=80, bottom=80, start=120, end=120):
    tc = cell._tc
    tc_pr = tc.get_or_add_tcPr()
    tc_mar = tc_pr.first_child_found_in("w:tcMar")
    if tc_mar is None:
        tc_mar = OxmlElement("w:tcMar")
        tc_pr.append(tc_mar)
    for m, v in [("top", top), ("bottom", bottom), ("start", start), ("end", end)]:
        node = tc_mar.find(qn(f"w:{m}"))
        if node is None:
            node = OxmlElement(f"w:{m}")
            tc_mar.append(node)
        node.set(qn("w:w"), str(v))
        node.set(qn("w:type"), "dxa")


def set_table_width(table, widths):
    table.alignment = WD_TABLE_ALIGNMENT.LEFT
    table.autofit = False
    tbl = table._tbl
    tbl_pr = tbl.tblPr
    tbl_w = tbl_pr.first_child_found_in("w:tblW")
    if tbl_w is None:
        tbl_w = OxmlElement("w:tblW")
        tbl_pr.append(tbl_w)
    tbl_w.set(qn("w:w"), "9360")
    tbl_w.set(qn("w:type"), "dxa")
    tbl_ind = tbl_pr.first_child_found_in("w:tblInd")
    if tbl_ind is None:
        tbl_ind = OxmlElement("w:tblInd")
        tbl_pr.append(tbl_ind)
    tbl_ind.set(qn("w:w"), "120")
    tbl_ind.set(qn("w:type"), "dxa")
    for row in table.rows:
        for idx, cell in enumerate(row.cells):
            cell.width = Inches(widths[idx])
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            set_cell_margins(cell)


def add_docx_table(doc, title, headers, rows, widths):
    p = doc.add_paragraph()
    set_paragraph_spacing(p, before=8, after=4, line=1.10)
    run = p.add_run(title)
    set_run_font(run, size=11, bold=True, color="1F4D78")

    table = doc.add_table(rows=1, cols=len(headers))
    table.style = "Table Grid"
    set_table_width(table, widths)
    for i, header in enumerate(headers):
        cell = table.rows[0].cells[i]
        shade_cell(cell, "F2F4F7")
        para = cell.paragraphs[0]
        set_paragraph_spacing(para, after=0, line=1.10)
        run = para.add_run(header)
        set_run_font(run, size=9, bold=True)
    for row in rows:
        cells = table.add_row().cells
        for i, text in enumerate(row):
            para = cells[i].paragraphs[0]
            set_paragraph_spacing(para, after=0, line=1.10)
            run = para.add_run(text)
            set_run_font(run, size=8.5)
    return table


def build_docx():
    doc = Document()
    section = doc.sections[0]
    section.page_width = Inches(8.5)
    section.page_height = Inches(11)
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)
    section.header_distance = Inches(0.492)
    section.footer_distance = Inches(0.492)

    styles = doc.styles
    normal = styles["Normal"]
    normal.font.name = "Calibri"
    normal._element.rPr.rFonts.set(qn("w:eastAsia"), "Microsoft YaHei")
    normal.font.size = Pt(11)
    normal.paragraph_format.space_after = Pt(6)
    normal.paragraph_format.line_spacing = 1.10

    for style_name, size, color, before, after in [
        ("Heading 1", 16, "2E74B5", 16, 8),
        ("Heading 2", 13, "2E74B5", 12, 6),
        ("Heading 3", 12, "1F4D78", 8, 4),
    ]:
        style = styles[style_name]
        style.font.name = "Calibri"
        style._element.rPr.rFonts.set(qn("w:eastAsia"), "Microsoft YaHei")
        style.font.size = Pt(size)
        style.font.color.rgb = RGBColor.from_string(color)
        style.paragraph_format.space_before = Pt(before)
        style.paragraph_format.space_after = Pt(after)

    header_p = section.header.paragraphs[0]
    header_p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    header_run = header_p.add_run("大模型安全相关技术调研报告")
    set_run_font(header_run, size=9, color="666666")

    footer_p = section.footer.paragraphs[0]
    footer_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    footer_run = footer_p.add_run("初稿")
    set_run_font(footer_run, size=9, color="666666")

    title = doc.add_paragraph()
    set_paragraph_spacing(title, before=10, after=4, line=1.10)
    run = title.add_run("大模型安全相关技术调研报告")
    set_run_font(run, size=23, color="000000", bold=True)

    subtitle = doc.add_paragraph()
    set_paragraph_spacing(subtitle, before=0, after=14, line=1.10)
    run = subtitle.add_run("聚焦 1.1.1 大模型推理决策机制的形式化建模技术研究")
    set_run_font(run, size=12, color="555555")

    meta = doc.add_paragraph()
    set_paragraph_spacing(meta, before=0, after=14, line=1.10)
    run = meta.add_run("版本：初稿 | 定位：研究思路说明与阶段产出草稿 | 边界：不展开系统开发、沙盒或具体防护算法")
    set_run_font(run, size=10.5, color="555555")

    for title_text, paras in sections:
        doc.add_heading(title_text, level=1)
        for para in paras:
            p = doc.add_paragraph()
            set_paragraph_spacing(p, before=0, after=6, line=1.10)
            r = p.add_run(para)
            set_run_font(r, size=11)
        if title_text.startswith("4.") and DIAGRAM_PATH.exists():
            pic_p = doc.add_paragraph()
            pic_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            pic_p.paragraph_format.space_before = Pt(6)
            pic_p.paragraph_format.space_after = Pt(4)
            pic_p.add_run().add_picture(str(DIAGRAM_PATH), width=Inches(6.25))

            cap = doc.add_paragraph()
            cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            set_paragraph_spacing(cap, before=0, after=8, line=1.10)
            cap_run = cap.add_run("图 1 面向智能体场景的大模型推理决策机制层级化状态转移模型")
            set_run_font(cap_run, size=9.5, color="555555")

    doc.add_heading("8. 四张核心表", level=1)
    add_docx_table(doc, "表 1 文献调研任务表", ["调研方向", "检索关键词", "需回答问题", "研究启发"], lit_table, [1.05, 1.85, 2.0, 2.6])
    add_docx_table(doc, "表 2 状态变量定义表", ["状态节点", "状态含义", "输入变量", "动作/输出", "安全关注点"], state_table, [0.65, 1.25, 1.35, 2.2, 2.1])
    add_docx_table(doc, "表 3 关键风险映射表", ["风险类型", "对应状态", "攻击方式", "影响后果", "可测指标"], risk_table, [1.05, 0.85, 2.0, 2.05, 1.6])
    add_docx_table(doc, "表 4 测评指标体系表", ["指标名称", "定义", "计算口径", "对应风险", "项目指标关系"], metric_table, [1.1, 1.85, 1.7, 1.55, 1.8])

    doc.add_heading("9. 需要老师确认的问题", level=1)
    questions = [
        "第一节点模型是否采用 Agent 推理决策状态模型为主，内部表征和参数机制作为调研支撑而不深入建模。",
        "“传统基准”具体采用通用 LLM safety benchmark、项目自建基准，还是二者结合。",
        "电力场景是否以电力知识问答和运维辅助决策为主要示例，暂不进入调度/控制类场景。",
    ]
    for idx, text in enumerate(questions, 1):
        p = doc.add_paragraph()
        set_paragraph_spacing(p, before=0, after=6, line=1.10)
        r = p.add_run(f"{idx}. {text}")
        set_run_font(r, size=11)

    doc.add_heading("参考文献与资料来源", level=1)
    for idx, (name, url) in enumerate(references, 1):
        p = doc.add_paragraph()
        set_paragraph_spacing(p, before=0, after=4, line=1.10)
        r = p.add_run(f"[{idx}] {name}. {url}")
        set_run_font(r, size=9.5)

    try:
        doc.save(DOCX_PATH)
        return DOCX_PATH
    except PermissionError:
        doc.save(ALT_DOCX_PATH)
        return ALT_DOCX_PATH


def main():
    OUT_DIR.mkdir(exist_ok=True)
    create_model_diagram()
    MD_PATH.write_text(build_markdown(), encoding="utf-8")
    saved_docx = build_docx()
    print(MD_PATH.resolve())
    print(saved_docx.resolve())
    print(DIAGRAM_PATH.resolve())


if __name__ == "__main__":
    main()
