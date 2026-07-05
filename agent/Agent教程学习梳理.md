# Agent 教程学习梳理

## 0. 这份文档怎么用

读者：已经把教程看过一遍，但概念、流程和组件边界还没有串起来的学习者。

读完后应该能做到：

1. 说清楚一个 Agent 系统由哪些模块组成。
2. 区分 Tool、MCP、RAG、Memory、LangGraph、DeepAgents 各自解决什么问题。
3. 看到一个 Agent 需求时，能拆出技术方案：工具、检索、状态、记忆、流式 UI、观测与部署。
4. 面试或复盘时，能用一条完整链路讲清楚“我理解的 Agent 工程化”。

这份文档不是逐页抄教程，而是把课程内容重新组织成一张知识地图。

## 1. 总体学习路线

这套教程大致可以分成 9 层：

1. **Tool 与 mini cursor**
   - 让大模型不只是聊天，而是能调用工具读文件、写文件、执行命令。
   - 这是 Agent 的最小闭环。

2. **MCP**
   - 把工具能力标准化，让不同工具以统一协议暴露给模型或 Agent。
   - 重点是 MCP Client、MCP Server、tool、stdio/http 传输。

3. **RAG 基础**
   - 解决模型不知道私有知识、长文档、业务资料的问题。
   - 重点是 loader、splitter、embedding、vector store、retriever、prompt。

4. **LangChain 基础组件**
   - Prompt Template、Output Parser、Structured Output、Runnable、LCEL。
   - 这层负责把模型调用、结构化输出和链式调用组织起来。

5. **Node/Nest 工程化**
   - 把 LangChain/Agent 能力放进后端服务里。
   - 重点是 Module、Controller、Service、DI、provider、ORM、数据库。

6. **Agent Loop 与 UI 流式协议**
   - Agent 不是一次模型调用，而是“思考 -> 调工具 -> 看结果 -> 再思考”的循环。
   - 前端需要看见 text、tool input、tool output、最终结果等事件。

7. **LangGraph 与多 Agent**
   - 用状态图显式管理复杂流程。
   - 支持 checkpoint、interrupt、条件分支、supervisor-worker、多节点协作。

8. **高级 RAG 与基础设施**
   - MySQL、Milvus、Elasticsearch、Neo4j、Redis、PostgreSQL、Docker。
   - 从简单向量检索走向混合检索、GraphRAG、Agentic RAG 和长期记忆。

9. **观测、DeepAgents 与长期记忆**
   - LangSmith 做 trace 和调试。
   - DeepAgents 把 Agent 工程化成带 middleware、todo、文件系统、子 Agent 的系统。
   - Redis、PostgreSQL、Mem0 处理会话状态和长期记忆。

## 2. Agent 的核心心智模型

Agent 可以先用一句话理解：

> Agent = LLM + Prompt + Tools + Memory/State + Loop + Observation。

更工程化一点：

```text
User Input
   |
   v
Prompt + History + Retrieved Context
   |
   v
LLM decides:
   |--------------------|
   | answer directly    |
   | call a tool        |
   | ask for more info  |
   | plan next step     |
   |--------------------|
          |
          v
Tool Call / Retrieval / State Update
          |
          v
Observation
          |
          v
LLM continues or stops
```

容易混的点：

- **LLM** 只负责生成文本或结构化决策。
- **Tool** 负责连接真实世界，比如读文件、查数据库、执行命令、调 API。
- **Memory** 负责保留上下文或长期偏好。
- **RAG** 负责把外部知识塞进上下文。
- **LangGraph** 负责把复杂 Agent 流程显式编排成状态机。
- **UI stream** 负责让用户看到 Agent 正在做什么。
- **LangSmith** 负责看清楚 Agent 为什么错、错在哪一步。

## 3. Tool：Agent 的最小行动能力

### 3.1 Tool 是什么

Tool 本质是一个被模型调用的函数，但它必须有清晰的描述和参数 schema。

模型看到工具描述后，会决定：

1. 要不要调用工具。
2. 调哪个工具。
3. 参数怎么填。

工具执行后，把结果作为 observation 返回给模型，模型再决定下一步。

典型消息流：

```text
SystemMessage
HumanMessage
AIMessage(tool_calls)
ToolMessage(tool_result)
AIMessage(final_answer or next_tool_call)
```

### 3.2 mini cursor 的关键思想

教程里的 mini cursor 是很好的 Agent 入门项目，因为它把 Agent 的基本动作都做出来了：

- `read_file`：读取文件内容。
- `write_file`：写入文件。
- `execute_command`：执行命令。
- `list_directory`：列目录。

它的工作方式类似：

```text
用户：帮我创建一个 React todo demo
  |
  v
模型生成 tool call：执行 pnpm create vite
  |
  v
工具执行命令，返回结果
  |
  v
模型继续生成 tool call：写 App.tsx
  |
  v
工具写文件，返回结果
  |
  v
模型继续：安装依赖 / 启动 / 修复错误
```

这就是 Agent Loop 的雏形。

### 3.3 Tool 设计要点

设计工具时要注意：

1. **工具职责单一**
   - 一个工具只做一件事。
   - 读文件、写文件、执行命令不要混成一个万能工具。

2. **参数 schema 清晰**
   - 参数名要表达业务含义。
   - 必填/可选要明确。
   - 枚举值要尽量限制范围。

3. **输出可被模型理解**
   - 不要返回一大坨无结构日志。
   - 尽量返回状态、摘要、关键结果、错误信息。

4. **危险工具要加护栏**
   - 执行命令、删除文件、访问生产接口都要限制。
   - Agent 最容易出问题的地方通常不是“不会想”，而是“能乱动”。

## 4. MCP：把工具标准化

### 4.1 MCP 解决什么问题

如果每个工具都用自己的接入方式，Agent 生态会很乱。

MCP 的作用是：

> 用统一协议把外部能力暴露成 tools，让不同客户端都能使用。

可以这样理解：

```text
Agent / Cursor / LangChain
        |
        | MCP Client
        v
MCP Server
        |
        | exposes tools
        v
FileSystem / Browser / Database / Map API / DevTools
```

### 4.2 MCP 的几个关键词

- **MCP Server**
  - 提供工具的一侧。
  - 例如 filesystem server、Chrome DevTools server、高德地图 server。

- **MCP Client**
  - 使用工具的一侧。
  - 可以是 Cursor、Claude Desktop、LangChain 程序。

- **transport**
  - 常见有 stdio 和 http。
  - stdio 适合本地进程工具。
  - http 适合远程服务工具。

- **tool**
  - MCP Server 暴露的具体能力。
  - 本质仍然是“带 schema 的函数”。

### 4.3 Tool 和 MCP 的区别

| 概念 | 重点 | 类比 |
| --- | --- | --- |
| Tool | 一个可调用能力 | 函数 |
| MCP Server | 一组工具的服务端 | 插件服务 |
| MCP Client | 连接 MCP Server 并调用工具 | 工具消费者 |
| MCP | 工具接入协议 | USB/HTTP 这类统一接口 |

一句话：

> Tool 是能力，MCP 是把能力标准化暴露出去的协议。

## 5. RAG：让模型使用外部知识

### 5.1 RAG 的基础链路

RAG 是 Retrieval-Augmented Generation，核心不是“让模型记住知识”，而是在回答前把相关知识检索出来，放进 prompt。

基础流程：

```text
Documents
  |
  v
Loader
  |
  v
Splitter
  |
  v
Chunks
  |
  v
Embedding Model
  |
  v
Vector Store
  |
  v
Retriever(query)
  |
  v
Relevant Chunks
  |
  v
Prompt + LLM
  |
  v
Answer
```

### 5.2 Loader、Document、Splitter、Chunk

这几个概念特别容易混：

- **Loader**
  - 负责从 PDF、Word、网页、EPUB、YouTube、URL 等来源加载内容。

- **Document**
  - LangChain 中承载文本和 metadata 的对象。
  - 通常包含 `pageContent` 和 `metadata`。

- **Splitter**
  - 把长文档切成较小 chunk。
  - 常见有 CharacterTextSplitter、RecursiveCharacterTextSplitter、MarkdownTextSplitter。

- **Chunk**
  - 被向量化和检索的最小文本片段。

### 5.3 chunk size 和 overlap

切块不是越小越好，也不是越大越好。

- chunk 太小：
  - 上下文不完整。
  - 检索结果碎片化。

- chunk 太大：
  - 噪声多。
  - 占用 token。
  - 相似度不够精准。

- overlap：
  - 用来避免切块边界丢语义。
  - 常见经验是 chunk size 的 10% 到 20%。

### 5.4 Milvus、MySQL、Elasticsearch 的分工

教程里反复出现 MySQL + Milvus + Elasticsearch，是因为它们解决的问题不同：

| 系统 | 擅长 | 在 RAG 中的角色 |
| --- | --- | --- |
| MySQL | 结构化数据、事务、业务表 | 存业务实体、文档信息、chunk 元数据 |
| Milvus | 向量相似度检索 | 按语义找相似 chunk |
| Elasticsearch | 全文检索、关键词、分词、过滤 | 按关键词、标签、字段做精确或近似匹配 |
| Neo4j | 图关系 | 做 GraphRAG，表达实体关系 |
| Redis | 缓存、短期状态、TTL | 会话状态、任务状态、临时记忆 |
| PostgreSQL | 关系数据，也可配合向量扩展 | 存对话、消息、用户数据、长期状态 |

### 5.5 Naive RAG、Hybrid RAG、Agentic RAG、GraphRAG

#### Naive RAG

最基础：

```text
query -> vector search -> topK chunks -> prompt -> answer
```

适合简单文档问答。

#### Hybrid RAG

结合向量检索和关键词检索：

```text
query
  |----------------|
  v                v
Milvus         Elasticsearch
  |                |
  |---- merge/rerank
          |
          v
       prompt
```

适合既要语义相似，又要关键词精确命中的场景。

#### Agentic RAG

让 Agent 决定怎么检索、是否改写 query、是否多轮检索、是否验证答案。

典型流程：

```text
question
  |
  v
analyze question
  |
  v
choose retrieval strategy
  |
  v
retrieve / rerank / verify
  |
  v
answer or retry
```

#### GraphRAG

把知识组织成实体和关系。

适合：

- 人物、组织、事件之间关系复杂。
- 单个 chunk 无法表达完整上下文。
- 需要沿关系路径推理。

## 6. Prompt Template 与 Output Parser

### 6.1 Prompt Template

Prompt Template 不是简单字符串拼接，而是让 prompt 可维护、可复用、可测试。

常见组成：

- 任务说明。
- 输入变量。
- 输出格式要求。
- 示例。
- 约束条件。

例子：

```text
你是一个数据分析助手。
请根据用户问题和字段说明生成 SQL。

用户问题：{question}
字段说明：{schema}

要求：
1. 只输出 SQL。
2. 不要解释。
3. 表名必须来自字段说明。
```

### 6.2 Output Parser

Output Parser 解决的问题是：

> 模型输出不稳定，程序需要稳定的数据结构。

没有 parser：

```text
模型可能输出：
名字：张三
年龄：18
```

有 parser：

```json
{
  "name": "张三",
  "age": 18
}
```

### 6.3 Structured Output 和 Tool Calling 的关系

很多框架的 structured output 底层会用 tool/function calling。

区别可以这样理解：

| 能力 | 目标 |
| --- | --- |
| Structured Output | 让模型按 schema 输出结构化数据 |
| Tool Calling | 让模型决定调用哪个工具以及参数 |

如果只是要稳定 JSON，用 structured output。

如果要让模型调用真实函数，用 tool calling。

## 7. Runnable 与 LCEL

### 7.1 Runnable 是什么

LangChain 里很多东西都可以被看成 Runnable：

- PromptTemplate
- ChatModel
- OutputParser
- Retriever
- RunnableLambda
- RunnableBranch
- RunnableSequence

Runnable 统一了调用方式：

- `invoke`：单次调用。
- `batch`：批量调用。
- `stream`：流式调用。

### 7.2 LCEL 的意义

LCEL 可以把多个 Runnable 串起来：

```text
input
  |
  v
PromptTemplate
  |
  v
ChatModel
  |
  v
OutputParser
  |
  v
structured result
```

代码上就是类似：

```text
prompt | model | parser
```

### 7.3 RunnableBranch / RunnableLambda / RunnablePassthrough

- **RunnableLambda**
  - 把普通函数包装成链的一部分。

- **RunnableBranch**
  - 做 if/else 分支。
  - 例如根据输入类型选择不同 prompt。

- **RunnablePassthrough**
  - 原样透传输入，常用于并行拼装字段。

LCEL 适合中等复杂度链路。

如果流程变成多节点、多循环、多条件、多状态，就应该考虑 LangGraph。

## 8. LangChain 与不同模型 API

教程里对比了 OpenAI、Anthropic、Gemini 等模型 API。

核心点：

> 不同模型厂商 API 格式不同，LangChain 做了一层统一抽象。

例如：

- OpenAI 常见是 `messages`。
- Anthropic 把 system 单独放。
- Gemini 是 contents/parts 风格。

LangChain 的价值：

- 统一 ChatModel 调用。
- 统一消息对象。
- 统一 tool calling。
- 统一 prompt、parser、runnable。

但要注意：

- 统一抽象不代表不同模型行为完全一致。
- Tool calling、structured output、streaming 的兼容度仍然要实测。
- 模型能力差异会直接影响 Agent 稳定性。

## 9. Memory：上下文、短期记忆、长期记忆

### 9.1 Memory 不等于 RAG

这是一个非常重要的区分：

| 概念 | 回答的问题 |
| --- | --- |
| Chat History | 这轮对话前面说了什么 |
| Memory | 用户/任务/偏好/状态需要被记住什么 |
| RAG | 外部知识库里有什么相关资料 |

### 9.2 短期记忆

短期记忆通常就是 messages：

```text
SystemMessage
HumanMessage
AIMessage
ToolMessage
HumanMessage
...
```

问题：

- token 有上限。
- 长对话会越来越贵。
- 无关历史会干扰模型。

处理方式：

- 截断。
- 摘要。
- 只保留关键状态。
- 把长期信息写入数据库或 memory 服务。

### 9.3 Redis / PostgreSQL / Mem0

教程后面进入 Redis、PostgreSQL、Mem0，重点是记忆持久化。

- Redis：
  - 适合短期状态、TTL、会话缓存。
  - 例如 CLI Agent 的当前任务状态、临时上下文。

- PostgreSQL：
  - 适合长期结构化存储。
  - 例如 conversations、messages、users。

- Mem0：
  - 更像开箱即用的 Agent Memory 服务。
  - 可以 add conversation，再 search 用户相关记忆。

长期记忆常见模式：

```text
new message
  |
  v
extract memory candidates
  |
  v
store user facts/preferences/task history
  |
  v
future query searches memory
  |
  v
inject relevant memories into prompt
```

## 10. NestJS：把 Agent 能力服务化

教程中多次用 NestJS 承载 Agent。

### 10.1 Nest 的基本结构

```text
Module
  |
  |-- Controller
  |      |-- 接收 HTTP 请求
  |
  |-- Service
  |      |-- 业务逻辑
  |
  |-- Provider
         |-- 可注入依赖，如 ChatModel、数据库连接、工具服务
```

关键词：

- MVC
- DI / IoC
- Controller
- Service
- Module
- Provider
- `@Injectable`
- `useFactory`

### 10.2 为什么 Agent 适合放进后端服务

因为 Agent 通常需要：

- 管理 API key。
- 调工具和数据库。
- 持久化会话。
- 记录 trace。
- 控制权限。
- 对前端提供 SSE/WebSocket 流。

这些都不适合完全放在浏览器端。

### 10.3 TypeORM 与数据库

TypeORM 把数据库表映射成实体类。

常见结构：

```text
Entity -> Repository -> Service -> Controller
```

在 Agent 系统里，数据库常用于：

- 用户。
- 会话。
- 消息。
- 工具调用记录。
- 文档元数据。
- 任务状态。

## 11. Agent Loop：从聊天到自动执行

### 11.1 最小 Agent Loop

```text
while not done:
    send messages to model
    if model returns final answer:
        stop
    if model returns tool call:
        execute tool
        append ToolMessage
        continue
```

### 11.2 Agent Loop 的关键风险

1. **无限循环**
   - 工具结果不满足模型预期，模型反复调用。
   - 需要 max steps。

2. **错误工具参数**
   - schema 不清晰或模型理解错。
   - 需要参数校验。

3. **工具执行失败**
   - 命令失败、API 超时、权限不足。
   - 需要把错误结构化返回给模型。

4. **危险动作**
   - 删除文件、改配置、访问生产环境。
   - 需要确认和权限边界。

5. **上下文污染**
   - 工具输出太大或太乱。
   - 需要摘要和裁剪。

## 12. AGUI 与流式 UI

### 12.1 为什么 Agent 需要流式 UI

Agent 经常不是一次回答结束，而是会：

- 生成文本。
- 调工具。
- 等工具输出。
- 再生成。
- 再调用。

如果前端只等最终结果，用户会觉得“卡死”。

所以需要把中间过程流式展示出来。

### 12.2 AGUI / Vercel AI SDK 数据流事件

教程中提到的事件类似：

- `text-start`
- `text-delta`
- `text-end`
- `tool-input-start`
- `tool-input-delta`
- `tool-input-available`
- `tool-output-available`

可以理解成：

```text
AI 开始说话
  -> 文本增量输出
  -> 文本结束
  -> 工具输入开始
  -> 工具参数逐步可见
  -> 工具开始执行
  -> 工具输出可见
  -> AI 继续回答
```

### 12.3 SSE 和前端渲染

SSE 很适合 Agent UI：

- 服务端单向推送。
- 浏览器支持简单。
- 适合文本流、步骤流、工具调用流。

前端要处理：

- 消息追加。
- 步骤状态。
- 工具调用卡片。
- 错误状态。
- 中断和重试。
- 连接断开。

## 13. LangGraph：把 Agent 做成状态机

### 13.1 为什么需要 LangGraph

LCEL 适合线性链路。

但复杂 Agent 需要：

- 多节点。
- 条件分支。
- 循环。
- 状态保存。
- 人工中断。
- 多 Agent 协作。

这就是 LangGraph 的场景。

### 13.2 LangGraph 基本模型

```text
State
  |
  v
START -> nodeA -> nodeB -> condition
                         |       |
                         v       v
                       nodeC    END
```

核心概念：

- **State**
  - 整个图共享的状态。
  - 例如 question、messages、retrievedDocs、toolResults、answer。

- **Node**
  - 一个处理步骤。
  - 可以是 LLM 调用、检索、工具执行、校验、总结。

- **Edge**
  - 节点之间的连接。

- **Conditional Edge**
  - 根据状态决定下一步。

- **Checkpoint**
  - 保存状态，支持恢复。

- **Interrupt**
  - 中断流程，让人类确认或输入。

### 13.3 LangGraph 适合哪些 Agent

适合：

- 多步 RAG。
- SQL Agent。
- 多工具 Agent。
- 需要人工确认的 Agent。
- 长任务 Agent。
- 多 Agent 协作。

不适合：

- 只有一次 prompt -> answer。
- 线性 prompt -> model -> parser。

## 14. 多 Agent：Supervisor - Worker

### 14.1 多 Agent 解决什么问题

一个 Agent 什么都做，容易：

- prompt 太长。
- 工具太多。
- 角色不清。
- 决策不稳定。

多 Agent 把任务拆给不同角色：

```text
Supervisor
  |
  |-- Researcher
  |-- Analyst
  |-- Coder
  |-- Editor
```

### 14.2 Supervisor 的职责

Supervisor 不应该亲自做所有事，而是：

- 理解目标。
- 拆任务。
- 分配给合适 worker。
- 整合结果。
- 判断是否继续。

### 14.3 Worker 的职责

Worker 应该：

- 专注一个子任务。
- 使用有限工具。
- 输出结构化结果。
- 不擅自扩大范围。

多 Agent 的风险：

- 成本上升。
- 延迟变长。
- 互相传递错误。
- 最终整合质量不稳定。

## 15. DeepAgents：更工程化的 Agent 框架

DeepAgents 可以理解为在 LangGraph 基础上做了一层更“产品化”的 Agent 抽象。

教程里出现的关键词：

- `createDeepAgent`
- middleware
- tool
- prompt
- todo
- file system
- subagents
- researcher
- analyst
- editor
- QuickJS REPL

### 15.1 DeepAgents 的价值

它把常见 Agent 工程能力打包：

- 任务规划。
- 子 Agent。
- 文件读写。
- todo 管理。
- 中间件扩展。
- LangSmith 观测。
- 更接近真实可用的研究/分析/编辑助手。

### 15.2 middleware 的作用

middleware 可以在 Agent 执行前后插入逻辑：

- 修改输入。
- 注入上下文。
- 记录日志。
- 限制工具。
- 拦截危险操作。
- 做 trace。

这类似后端框架里的中间件思想。

## 16. LangSmith：Agent 调试与观测

Agent 很难调试，因为错误可能来自：

- prompt。
- 模型能力。
- 检索结果。
- 工具输出。
- 状态传递。
- 分支判断。
- token 截断。

LangSmith 的价值是 trace：

```text
Run
  |
  |-- Prompt input
  |-- Model output
  |-- Tool call
  |-- Tool result
  |-- Retriever result
  |-- Error stack
  |-- Token / latency
```

有了 trace，才能回答：

- 模型到底看到了什么？
- 它为什么调这个工具？
- 检索结果是不是错的？
- 哪个节点耗时最长？
- 哪一步 token 爆了？

## 17. STT / TTS：语音 Agent

教程中还有 STT 和 TTS。

- STT：Speech To Text，把语音转文字。
- TTS：Text To Speech，把文本转语音。

语音 Agent 链路：

```text
microphone audio
  |
  v
STT
  |
  v
Agent / LLM
  |
  v
TTS
  |
  v
audio output
```

和文本 Agent 相比，语音 Agent 还要关注：

- 延迟。
- 打断。
- 语音分段。
- 噪音。
- 播放状态。
- 用户说话和模型说话的轮转。

## 18. 常见概念对照表

| 容易混的概念 | 怎么区分 |
| --- | --- |
| Tool vs MCP | Tool 是能力；MCP 是暴露和连接工具的协议 |
| Tool Calling vs Structured Output | 前者调用函数；后者稳定输出结构化数据 |
| Prompt Template vs System Prompt | Template 是可复用模板；System Prompt 是对模型角色和规则的最高优先级指令 |
| RAG vs Memory | RAG 查外部知识；Memory 记用户/会话/任务历史 |
| Milvus vs Elasticsearch | Milvus 做语义向量检索；ES 做关键词/全文/过滤 |
| LCEL vs LangGraph | LCEL 适合线性链；LangGraph 适合状态机和复杂流程 |
| Agent vs Workflow | Agent 更自主决策；Workflow 更固定流程 |
| SSE vs WebSocket | SSE 适合服务端单向流；WebSocket 适合双向实时通信 |
| Checkpoint vs Memory | Checkpoint 保存流程状态；Memory 保存对话或用户长期信息 |
| DeepAgents vs LangGraph | DeepAgents 是更上层的 Agent 工程框架，底层可基于 LangGraph |

## 19. 从零做一个 Agent 应用的步骤

可以按这个清单设计：

### Step 1：定义任务边界

先回答：

- 用户要完成什么任务？
- Agent 能自主到什么程度？
- 哪些动作需要用户确认？
- 最终输出是什么格式？

### Step 2：选择模型

考虑：

- 是否支持 tool calling。
- 是否支持 structured output。
- 上下文窗口大小。
- 成本。
- 延迟。
- 中文能力。

### Step 3：设计 Prompt

Prompt 至少包含：

- 角色。
- 任务目标。
- 输入说明。
- 工具使用规则。
- 输出格式。
- 禁止行为。
- 错误处理方式。

### Step 4：设计 Tools

每个工具要明确：

- 名字。
- 描述。
- 参数 schema。
- 返回结构。
- 错误结构。
- 权限边界。

### Step 5：决定是否需要 RAG

如果需要外部知识：

- 用什么 loader。
- 如何 split。
- 用什么 embedding。
- 存在哪个 vector store。
- 是否需要 ES 混合检索。
- 是否需要 rerank。

### Step 6：决定是否需要状态图

如果只是线性链路，用 LCEL。

如果需要循环、分支、恢复、人工确认，用 LangGraph。

### Step 7：决定记忆策略

- 当前对话：messages。
- 临时状态：Redis。
- 长期会话：PostgreSQL。
- 语义记忆：Mem0 或向量库。

### Step 8：设计 UI 流

前端需要展示：

- 用户消息。
- AI 文本流。
- 工具调用中。
- 工具输出。
- 错误。
- 中断/重试。
- 最终结果。

### Step 9：加观测

至少记录：

- 用户输入。
- prompt 关键变量。
- 检索结果。
- tool call。
- tool result。
- 模型输出。
- token。
- 耗时。
- 错误。

### Step 10：加护栏

包括：

- max steps。
- tool allowlist。
- 参数校验。
- 敏感操作确认。
- 输出格式校验。
- 超时。
- 重试。
- 失败兜底。

## 20. Debug Checklist

Agent 出问题时，不要只改 prompt。按链路排：

1. **用户问题是否清楚**
   - 输入是否缺关键信息。

2. **Prompt 是否清楚**
   - 角色、目标、工具规则、输出格式是否明确。

3. **模型是否支持需要的能力**
   - tool calling 是否稳定。
   - structured output 是否可用。

4. **工具 schema 是否清楚**
   - 参数是否歧义。
   - 返回是否太乱。

5. **工具结果是否正确**
   - API 是否失败。
   - 命令是否报错。
   - 数据库是否返回空。

6. **RAG 检索是否命中**
   - chunk 是否合理。
   - query 是否需要改写。
   - topK 是否太少或太多。
   - 是否需要关键词检索补充。

7. **状态是否传错**
   - LangGraph state 字段是否更新。
   - checkpoint 是否恢复了旧状态。

8. **上下文是否污染**
   - history 是否太长。
   - tool output 是否太大。
   - 无关资料是否塞进 prompt。

9. **是否缺观测**
   - 没有 trace 就很难定位。
   - 优先接入 LangSmith 或自建日志。

## 21. 面试/项目表达模板

如果面试官问“你理解 Agent 吗”，可以这样答：

> 我理解 Agent 不是简单的一次大模型调用，而是模型在 prompt、工具、记忆和状态管理约束下，围绕目标进行多步执行的系统。最小闭环是模型根据消息决定 tool call，工具执行后把结果作为 ToolMessage 返回，模型继续判断直到完成。工程上还要解决 RAG 知识增强、LangGraph 状态编排、SSE 流式 UI、长期记忆、trace 观测和工具安全边界。

如果问“RAG 怎么做”，可以这样答：

> 我会先用 loader 把文档转成 Document，再用 splitter 按合适的 chunk size 和 overlap 切块，用 embedding 模型向量化后写入 Milvus。查询时先做 query 改写或直接检索，取 topK chunk 组装进 prompt。如果业务有大量关键词、标签和字段过滤，我会结合 Elasticsearch 做混合检索；如果知识关系很强，再考虑 Neo4j 做 GraphRAG。

如果问“LangGraph 有什么用”，可以这样答：

> LCEL 更适合线性链路，比如 prompt -> model -> parser。LangGraph 适合复杂 Agent，它把流程显式建成状态图，节点之间通过 state 传递数据，可以做条件分支、循环、checkpoint、interrupt 和多 Agent 协作。比如 SQL Agent 可以拆成理解问题、检索元数据、生成 SQL、校验 SQL、执行 SQL、修正错误、总结结果这些节点。

如果问“怎么做一个 AI 应用的前端交互”，可以这样答：

> Agent 不应该只等最终结果，前端最好通过 SSE 展示中间过程。服务端可以按事件推送 text-start、text-delta、tool-input、tool-output、error、done 等事件。前端把 AI 文本、工具调用卡片、执行状态、错误和最终结果分开展示，让用户知道 Agent 正在做什么，也方便中断和重试。

## 22. 推荐复习顺序

如果你现在“都看过但细节乱”，建议按这个顺序重新过一遍：

1. **Tool / mini cursor**
   - 目标：搞懂 tool_calls、ToolMessage、Agent Loop。

2. **MCP**
   - 目标：搞懂 MCP Server/Client 与普通 tool 的关系。

3. **RAG 基础**
   - 目标：背熟 loader -> splitter -> embedding -> vector store -> retriever -> prompt。

4. **Prompt / Output Parser / Runnable / LCEL**
   - 目标：知道 LangChain 怎么把模型调用组织成链。

5. **NestJS + Agent 服务化**
   - 目标：知道 Agent 如何变成后端接口。

6. **AGUI / SSE**
   - 目标：知道 Agent 中间过程如何展示到前端。

7. **LangGraph**
   - 目标：掌握 state、node、edge、checkpoint、interrupt。

8. **Advanced RAG**
   - 目标：区分 Milvus、ES、Neo4j、Agentic RAG、GraphRAG。

9. **LangSmith / DeepAgents / Memory**
   - 目标：理解真实项目里的调试、子 Agent 和长期记忆。

## 23. 一句话总览

这套教程的主线可以压缩成一句话：

> 先让模型能调工具，再用 MCP 标准化工具，用 RAG 补知识，用 LangChain 组织调用，用 NestJS 服务化，用 SSE/AGUI 展示过程，用 LangGraph 管复杂状态，用 ES/Milvus/Neo4j/Redis/Postgres/Mem0 管知识和记忆，用 LangSmith/DeepAgents 把 Agent 做到可调试、可扩展、可落地。

