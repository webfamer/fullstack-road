# prepme SKILL.md 双语对照

> 文件来源：`/Users/xsz/.codex/skills/prepme/SKILL.md`  
> 阅读方式：每一段先放英文原文，再放中文翻译。最后附一个很短的 skill 写作格式总结。

## Frontmatter

**Original**

```yaml
---
name: prepme
description: Generate a tailored set of likely interview questions from a candidate's resume (CV) and a job description (JD), output as an interactive HTML study sheet. Each question is clickable to copy an AI deep-dive prompt and mark itself as processed. Takes two file inputs — CV and JD; the output language is auto-detected from those documents. Trigger on "prepare interview questions", "interview prep", "mock interview questions", "prepme".
allowed-tools: Bash Read Write
---
```

**中文翻译**

```yaml
---
name: prepme
description: 根据候选人的简历（CV）和岗位描述（JD），生成一组定制化的高概率面试问题，并输出为一个交互式 HTML 学习页。每个问题都可以点击，点击后会复制一段 AI 深度解析 Prompt，并将该问题标记为已处理。该技能需要两个文件输入：CV 和 JD；输出语言会根据这两个文档自动检测。当用户提到 "prepare interview questions"、"interview prep"、"mock interview questions"、"prepme" 时触发。
allowed-tools: Bash Read Write
---
```

## Interview Preparation

**Original**

```markdown
# Interview Preparation

Turn a candidate's **resume (CV)** and a **job description (JD)** into a focused, interactive set of likely interview questions. The deliverable is a single self-contained HTML file the candidate studies from: every question is clickable to (1) copy a ready-to-paste AI prompt that requests a deep-dive analysis of that question, and (2) mark the question as processed so the candidate can track progress.

The goal is **breadth of realistic coverage**, not a domain encyclopedia. The question set is built in **two distinct halves**: one driven by the **JD** (the common technical knowledge the role requires) and one driven by the **CV** (the candidate's actual projects and the technologies they claim). Keep these two halves separate — they are generated from different sources and probe different things.
```

**中文翻译**

```markdown
# 面试准备

将候选人的**简历（CV）**和**岗位描述（JD）**转换成一组聚焦且交互式的高概率面试问题。交付物是一个自包含的 HTML 文件，候选人可以用它来学习：每个问题都可以点击，点击后会做两件事：（1）复制一段可直接粘贴给 AI 的 Prompt，用于对该问题做深度解析；（2）将该问题标记为已处理，方便候选人追踪复习进度。

目标是实现**真实且广泛的覆盖**，而不是做一个领域百科。问题集由**两个清晰分开的部分**组成：一部分由 **JD** 驱动，用来覆盖岗位要求的通用技术知识；另一部分由 **CV** 驱动，用来追问候选人的真实项目和他声称掌握的技术。必须保持这两部分分离，因为它们来自不同信息源，验证的能力也不同。
```

## Inputs

**Original**

```markdown
## Inputs

Two file inputs are required. Gather any that are missing before proceeding:

1. **CV file** — path to the candidate's resume (PDF, Markdown, txt, docx). Read it.
2. **JD file** — path to the job description (any text format). Read it.

The **output language is auto-detected** — do not ask for it. Use the JD's dominant natural language for all output (questions, follow-ups, labels, the copy prompt), falling back to the CV's language if the JD's is unclear, but always keep technology names, tools, and acronyms in their original form. An explicit language in the user's request overrides detection; only ask if no language can be determined at all. Record the resolved language in `META.language`.

If a file path is ambiguous or unreadable, ask the user for the correct path rather than guessing. PDFs can be read directly with the Read tool.
```

**中文翻译**

```markdown
## 输入

必须提供两个文件输入。开始执行前，如果缺少任何一个，都要先收集齐：

1. **CV 文件**：候选人简历的路径（PDF、Markdown、txt、docx）。读取它。
2. **JD 文件**：岗位描述的路径（任意文本格式）。读取它。

**输出语言会自动检测**，不要主动询问。所有输出内容（问题、追问、标签、复制用 Prompt）都使用 JD 中占主导的自然语言；如果 JD 语言不明确，则回退到 CV 的语言。但技术名称、工具名和缩写始终保持原文。如果用户请求中明确指定了语言，则以用户指定语言为准；只有在完全无法判断语言时才询问。将最终确定的语言记录到 `META.language`。

如果文件路径有歧义或无法读取，要向用户询问正确路径，不要猜测。PDF 可以直接用 Read 工具读取。
```

## Principles

**Original**

```markdown
## Principles

These shape *which* questions you generate. Read them before drafting.
```

**中文翻译**

```markdown
## 原则

这些原则决定你应该生成*哪些*问题。在开始草拟之前先阅读它们。
```

### 1. Two sources, two halves

**Original**

```markdown
1. **Two sources, two halves.**
   - **JD half — common required knowledge.** From the JD, extract the underlying tech, skills, and concepts the role requires, then ask questions about *that knowledge in general*. Do **not** weld the company's specific domain or product onto each question — a "real-time payments platform using Kafka" JD should yield a clean question about Kafka delivery semantics or event-driven design, not "how would you build our payments pipeline with Kafka." Test whether the candidate owns the transferable fundamentals the role depends on.
   - **CV half — experience & claimed tech.** From the CV, ask about the candidate's actual projects, decisions, and the specific technologies they list. These questions *are* grounded in the candidate's own work: probe what they built, why, the tradeoffs they made, and whether their claimed depth in each listed tech is real.
```

**中文翻译**

```markdown
1. **两个来源，两个部分。**
   - **JD 部分：岗位要求的通用知识。** 从 JD 中提取该岗位需要的底层技术、技能和概念，然后针对这些*通用知识*提问。不要把公司的具体业务领域或产品强行绑定到每个问题上。例如，一个写着“使用 Kafka 的实时支付平台”的 JD，应该生成关于 Kafka 投递语义或事件驱动设计的清晰问题，而不是“你会如何用 Kafka 构建我们的支付管道”。这里要测试的是候选人是否掌握该岗位依赖的可迁移基础能力。
   - **CV 部分：真实经历和声称掌握的技术。** 从 CV 中围绕候选人的真实项目、决策和列出的具体技术提问。这些问题必须基于候选人自己的经历：追问他构建了什么、为什么这么做、做了哪些取舍，以及他在简历中声称掌握的技术深度是否真实。
```

### 2. General over hyper-specific

**Original**

```markdown
2. **General over hyper-specific (JD half especially).** Favor widely transferable technical and conceptual knowledge — fundamentals, design tradeoffs, debugging approach, system thinking. Avoid obscure, company-internal, or narrow domain trivia. A good question is one a competent practitioner *should* be able to answer and that reveals real understanding.
```

**中文翻译**

```markdown
2. **通用优先于过度具体，尤其是 JD 部分。** 优先选择具有广泛迁移性的技术和概念知识，例如基础原理、设计取舍、调试方法、系统思维。避免晦涩、公司内部化或狭窄领域的小知识点。一个好问题应该是合格从业者*应该*能回答的问题，同时能暴露出他是否真正理解。
```

### 3. Full coverage, no padding

**Original**

```markdown
3. **Full coverage, no padding.** Every meaningful JD knowledge area and every substantial CV project/technology should map to at least one question. Track this explicitly (see Coverage Map). Do not invent questions for things absent from both documents.
```

**中文翻译**

```markdown
3. **完整覆盖，不灌水。** 每个有意义的 JD 知识领域，以及每个重要的 CV 项目/技术，都应该至少映射到一个问题。要显式追踪这一点（见 Coverage Map）。不要为两个文档中都不存在的内容编造问题。
```

### 4. Anticipate the follow-up

**Original**

```markdown
4. **Anticipate the follow-up.** Real interviews drill down. Each question carries 2–4 likely follow-ups the interviewer would ask next — these reward depth and expose hand-waving.
```

**中文翻译**

```markdown
4. **预判追问。** 真实面试会继续深挖。每个问题都要带 2 到 4 个面试官可能接着问的追问。这些追问用来奖励深度，也能暴露空泛回答。
```

### 5. Honest difficulty

**Original**

```markdown
5. **Honest difficulty.** Tag each question's level (Foundational / Core / Advanced) so the candidate budgets study time well.
```

**中文翻译**

```markdown
5. **真实标注难度。** 为每个问题标注难度等级（Foundational / Core / Advanced），让候选人能合理分配学习时间。
```

## Workflow

### Step 1 — Read and extract

**Original**

```markdown
### Step 1 — Read and extract

Read both files fully. Produce two internal lists (you don't have to show them, but reason through them):

- **JD knowledge set**: the underlying technologies, skills, and concepts the role requires — distilled into *general knowledge areas*, deliberately stripped of the company's specific product/domain framing.
- **CV claims**: each project, role, achievement, technical decision, and specific technology the candidate asserts.

Also note the **role level** (junior / mid / senior / lead) since it sets question difficulty, and **resolve the output language** per the Inputs rules. Use that language for everything that follows.
```

**中文翻译**

```markdown
### 第 1 步：读取并提取

完整读取两个文件。生成两个内部列表（不一定展示给用户，但你需要据此推理）：

- **JD 知识集合**：该岗位要求的底层技术、技能和概念，并将其提炼成*通用知识领域*，刻意去掉公司的具体产品/业务语境。
- **CV 声明项**：候选人在简历中声明的每个项目、角色、成果、技术决策和具体技术。

同时记录**岗位级别**（初级 / 中级 / 高级 / 负责人），因为它会决定问题难度；并根据 Inputs 规则确定**输出语言**。后续所有输出都使用该语言。
```

### Step 2 — Design the two question sets

**Original**

```markdown
### Step 2 — Design the two question sets

Generate **20–35 questions total**, split into the two halves below, each organized into **2–4 categories**. Order the JD categories first, then the CV categories, so the HTML reads as two clear sections.

**Set A — JD-driven (common required knowledge).** Cover the knowledge areas the role depends on, as *general* questions per Principle 1. Typical categories (adapt — don't force-fit):
- Core technical fundamentals (language / runtime / CS basics the role implies)
- Tools, frameworks & paradigms named in the JD (asked generically, not bolted to the company's product)
- System / architecture / design thinking
- Practices the role demands (testing, debugging, collaboration, process)

**Set B — CV-driven (experience & claimed tech).** Ground every question in the candidate's own résumé:
- Project deep-dives (one or more per substantial project — what, why, tradeoffs, outcomes, what they'd change)
- Depth probes on specific technologies the CV lists (confirm real mastery vs. buzzword)
- Role/impact & ownership (scope, decisions, collaboration on their stated work)
```

**中文翻译**

```markdown
### 第 2 步：设计两组问题

总共生成 **20 到 35 个问题**，并拆成下面两个部分，每个部分组织成 **2 到 4 个分类**。先放 JD 分类，再放 CV 分类，这样 HTML 读起来就是两个清晰板块。

**A 组：JD 驱动，岗位要求的通用知识。** 按照原则 1，以*通用问题*覆盖该岗位依赖的知识领域。典型分类包括，但不要硬套：
- 核心技术基础，例如语言、运行时、岗位隐含的计算机基础。
- JD 中点名的工具、框架和范式，以通用方式提问，不绑定公司产品。
- 系统、架构和设计思维。
- 岗位要求的实践能力，例如测试、调试、协作、流程。

**B 组：CV 驱动，真实经验和声称掌握的技术。** 每个问题都要基于候选人自己的简历：
- 项目深挖，每个重要项目至少一个问题，关注做了什么、为什么做、取舍、结果、如果重来会怎么改。
- 对 CV 中列出的具体技术做深度追问，确认是真掌握还是关键词堆砌。
- 角色、影响力和 ownership，例如范围、决策、协作和他声称负责的工作。
```

### Question fields

**Original**

```markdown
For **each question**, decide:

| Field | What goes in it |
|-------|-----------------|
| `q` | The question, phrased exactly as an interviewer would say it, in the target language. |
| `level` | `Foundational` \| `Core` \| `Advanced` |
| `source` | One short clause: which set it belongs to and what it maps to — e.g. "JD: requires Kafka → event-delivery fundamentals" or "CV: owned the billing-service rewrite". This is the coverage justification. |
| `followups` | 2–4 likely interviewer follow-ups, in the target language. |

Spread across difficulty levels appropriate to the role level.
```

**中文翻译**

```markdown
对**每个问题**，确定以下字段：

| 字段 | 内容 |
|-------|-----------------|
| `q` | 问题本身，要用目标语言写成面试官真实提问的语气。 |
| `level` | `Foundational` \| `Core` \| `Advanced` |
| `source` | 一个简短说明：它属于哪一组，映射到什么内容。例如：“JD: requires Kafka → event-delivery fundamentals” 或 “CV: owned the billing-service rewrite”。这是覆盖依据。 |
| `followups` | 2 到 4 个面试官可能继续问的追问，使用目标语言。 |

根据岗位级别合理分布不同难度的问题。
```

### Step 3 — Build the coverage map

**Original**

```markdown
### Step 3 — Build the coverage map

Before generating, confirm in your own reasoning that every JD knowledge area is covered by a Set A question and every substantial CV project/technology is covered by a Set B question. The HTML's coverage summary has two columns — `coverage.jd` (the general knowledge areas from the JD) and `coverage.cv` (the projects/tech from the résumé) — fill each from the matching set. If a JD area can't be covered with a *general* question, note it briefly rather than inventing trivia.
```

**中文翻译**

```markdown
### 第 3 步：构建覆盖图

在生成之前，先在自己的推理中确认：每个 JD 知识领域都被 A 组问题覆盖，每个重要 CV 项目/技术都被 B 组问题覆盖。HTML 的覆盖摘要有两列：`coverage.jd` 表示来自 JD 的通用知识领域，`coverage.cv` 表示来自简历的项目/技术。分别用对应问题集中的内容填充。如果某个 JD 领域无法用*通用*问题覆盖，简单说明，而不是编造冷门知识点。
```

### Step 4 — Generate the HTML

**Original**

```markdown
### Step 4 — Generate the HTML

1. Read the template at `assets/template.html` (in this skill's directory).
2. Replace the placeholders:
   - `__TITLE__` — e.g. "Interview Prep — <Role> — <Company>" in the target language. Use the company name and/or job title from the JD; **never** put the candidate's name in the title. If the company isn't stated in the JD, use just the role (e.g. "Interview Prep — <Role>").
   - `__META__` — a JSON object: `{ "role": "...", "candidate": "...", "language": "...", "generated": "YYYY-MM-DD", "coverage": { "jd": ["req 1", "req 2", ...], "cv": ["area 1", ...] } }`. Strings in target language; use today's date.
   - `__PROMPT_TEMPLATE__` — the deep-dive prompt **in the target language**, containing the literal tokens `{{QUESTION}}` and `{{FOLLOWUPS}}` where the question text and its follow-up list will be substituted at click time. See "The copy prompt" below for required content.
   - `__DATA__` — a JSON array of category objects:
     ```json
     [
       { "category": "Category name in target language",
         "questions": [
           { "q": "...", "level": "Core", "source": "...", "followups": ["...", "..."] }
         ]
       }
     ]
     ```
   - `__UI__` — a JSON object of UI label strings in the target language (keys listed in the template's comment, e.g. progress/filter/copied labels). Translate each value.
3. Write the result to the user's working directory as `interview-prep.html` (or a name the user requested). Use the Write tool.
4. Validate the JSON you inject is well-formed (no trailing commas, properly escaped quotes). Then tell the user the file path and a one-line summary (N questions across M categories).
```

**中文翻译**

```markdown
### 第 4 步：生成 HTML

1. 读取该 skill 目录下的 `assets/template.html` 模板。
2. 替换以下占位符：
   - `__TITLE__`：例如用目标语言写成 “Interview Prep — <Role> — <Company>”。使用 JD 中的公司名和/或岗位名；**绝不要**把候选人姓名放进标题。如果 JD 没有公司名，就只使用岗位名，例如 “Interview Prep — <Role>”。
   - `__META__`：一个 JSON 对象：`{ "role": "...", "candidate": "...", "language": "...", "generated": "YYYY-MM-DD", "coverage": { "jd": ["req 1", "req 2", ...], "cv": ["area 1", ...] } }`。字符串使用目标语言；日期使用今天日期。
   - `__PROMPT_TEMPLATE__`：目标语言写成的深度解析 Prompt，必须包含字面 token `{{QUESTION}}` 和 `{{FOLLOWUPS}}`，点击时页面会将问题文本和追问列表替换进去。具体要求见下面的 “The copy prompt”。
   - `__DATA__`：一个分类对象组成的 JSON 数组：
     ```json
     [
       { "category": "目标语言中的分类名",
         "questions": [
           { "q": "...", "level": "Core", "source": "...", "followups": ["...", "..."] }
         ]
       }
     ]
     ```
   - `__UI__`：一个 UI 文案 JSON 对象，使用目标语言填写模板注释中列出的 key，例如 progress、filter、copied 等标签。
3. 将结果写入用户工作目录，文件名为 `interview-prep.html`，或者使用用户指定的名称。使用 Write 工具。
4. 校验注入的 JSON 格式正确，例如没有尾随逗号、引号正确转义。然后告诉用户文件路径，并用一句话总结：共 N 个问题，分布在 M 个分类中。
```

## The copy prompt

**Original**

```markdown
### The copy prompt (`__PROMPT_TEMPLATE__`)

This is what gets copied to the clipboard when a question is clicked. Written in the target language, it must instruct an AI to deliver a **detailed analysis** of the question and must request all of:

- **Best answer** — what a strong, structured answer looks like.
- **Bonus points** — what would impress the interviewer / signal seniority.
- **Anticipated follow-ups + how to answer them** — pre-empt where the interviewer drills next. Seed these with the question's own `{{FOLLOWUPS}}`.
- **ASCII diagrams** — instruct the AI to include ASCII diagrams to explain architecture, flow, or data structures *where it aids understanding*.

It must include the tokens `{{QUESTION}}` (the question text) and `{{FOLLOWUPS}}` (its follow-up list) so the page can fill them in per question. Keep it copy-paste ready for any chat AI.
```

**中文翻译**

```markdown
### 复制用 Prompt（`__PROMPT_TEMPLATE__`）

这是用户点击某个问题时复制到剪贴板的内容。它必须使用目标语言编写，并指示 AI 对该问题进行**详细分析**，同时必须要求包含以下所有内容：

- **最佳回答**：一个强、有结构的回答应该是什么样。
- **加分点**：哪些内容会让面试官印象更好，或者体现高级工程师能力。
- **预判追问 + 如何回答**：提前覆盖面试官下一步可能深挖的方向。这里要使用该问题自带的 `{{FOLLOWUPS}}` 作为输入。
- **ASCII 图**：在有助于理解时，要求 AI 用 ASCII 图解释架构、流程或数据结构。

它必须包含 token `{{QUESTION}}`，也就是问题文本；以及 `{{FOLLOWUPS}}`，也就是追问列表。这样页面才能针对每个问题填充具体内容。Prompt 要保持为可直接复制粘贴到任意聊天 AI 的格式。
```

## HTML behavior

**Original**

```markdown
## HTML behavior (provided by the template — don't reimplement)

The template already implements all interactivity; you only inject data. It provides:

- **Clickable question cards.** Clicking a card copies the filled-in deep-dive prompt to the clipboard **and** toggles the card to a "processed" state (greyed/checked) so the candidate tracks what they've drilled. A small toast confirms "copied". A separate small control lets the user un-mark if they misclicked.
- **Progress tracking.** A progress bar / counter shows processed vs total. State persists in `localStorage` (keyed per file) so progress survives reloads.
- **Filters.** By category, by level, and a "hide processed" toggle.
- **Self-contained.** No external network calls, no CDN, inline CSS+JS. Works by opening the file directly in a browser. Clipboard uses the async Clipboard API with a `document.execCommand('copy')` fallback for `file://`.

If the template file is missing, recreate an equivalent self-contained HTML using the same placeholder contract.
```

**中文翻译**

```markdown
## HTML 行为，由模板提供，不要重新实现

模板已经实现了所有交互功能；你只需要注入数据。它提供：

- **可点击的问题卡片。** 点击卡片会把填充后的深度解析 Prompt 复制到剪贴板，**并且**将该卡片切换为“已处理”状态，也就是变灰/打勾，方便候选人追踪自己练习过哪些题。一个小 toast 会提示“已复制”。如果用户误点，还有一个小控件可以取消标记。
- **进度追踪。** 进度条/计数器展示已处理数量和总数。状态会持久化到 `localStorage`，并按文件区分，所以刷新后进度仍然保留。
- **过滤器。** 可以按分类、难度过滤，也可以开启“隐藏已处理”开关。
- **自包含。** 没有外部网络请求，没有 CDN，CSS 和 JS 都内联。直接用浏览器打开文件即可使用。剪贴板优先使用异步 Clipboard API，并为 `file://` 场景提供 `document.execCommand('copy')` 降级方案。

如果模板文件缺失，就使用相同的占位符契约重新创建一个等价的自包含 HTML。
```

## Quality bar

**Original**

```markdown
## Quality bar

- The set is clearly split: Set A (JD) questions are general/knowledge-revealing and free of the company's specific domain framing; Set B (CV) questions are grounded in the candidate's actual projects and listed tech.
- Every JD knowledge area and substantial CV item is traceable to a question via its `source` field.
- JD-half questions are general, not obscure or company-internal trivia (Principle 1–2).
- Difficulty matches the role level.
- Follow-ups are realistic next-drill questions, not restatements.
- The HTML opens and works offline; clicking copies a correct, language-correct prompt and marks processed.
- All visible text (questions, labels, prompt) is in the requested language.
```

**中文翻译**

```markdown
## 质量标准

- 问题集清晰分成两部分：A 组（JD）问题是通用的、能揭示知识掌握程度的问题，并且不绑定公司的具体业务语境；B 组（CV）问题基于候选人的真实项目和列出的技术。
- 每个 JD 知识领域和重要 CV 项目，都能通过 `source` 字段追踪到对应问题。
- JD 部分的问题是通用问题，不是晦涩问题，也不是公司内部知识点，符合原则 1 和原则 2。
- 难度与岗位级别匹配。
- 追问是真实的下一步深挖问题，而不是对主问题的重复表述。
- HTML 可以打开并离线工作；点击问题能复制正确且语言正确的 Prompt，并将问题标记为已处理。
- 所有可见文本，包括问题、标签、Prompt，都使用用户要求的语言。
```

## 写 Skill 的简短格式总结

一个实用的 `SKILL.md` 通常可以按这个结构写：

```markdown
---
name: skill-name
description: 说明这个 skill 做什么、输入是什么、输出是什么、什么时候触发。
allowed-tools: Bash Read Write
---

# Skill Title

一句话说明目标和最终交付物。

## Inputs

列出必须输入和可选输入。
说明缺失、歧义、不可读取时怎么办。

## Principles

写清楚什么是好结果，什么不要做。

## Workflow

Step 1: 读取/分析输入。
Step 2: 抽取结构化信息。
Step 3: 生成内容或执行任务。
Step 4: 输出文件或结果。
Step 5: 验证。

## Output Schema / Template

如果有固定格式，明确 JSON / Markdown / HTML 的字段。
如果有模板，说明读取哪个 `assets/template`，替换哪些占位符。

## Quality bar

列出完成前必须满足的验收标准。
```

最重要的写法原则：

- `description` 要写清楚触发场景。
- `Inputs` 要让 Agent 不乱猜。
- `Principles` 要约束输出质量。
- `Workflow` 要把任务拆成可执行步骤。
- `Output Schema` 要让结果稳定。
- `Quality bar` 要让 Agent 完成前自检。

