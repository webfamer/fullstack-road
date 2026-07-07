# 项目源文件迁移指南

> 最后更新：2026-07-08
> 说明：标记项目中每个源文件的处理状态 — 已迁移到 docs / 包含可提取内容 / 已过时

---

## ✅ 已迁移（内容已整合到 docs/）

| 源文件 | 迁移到 | 备注 |
|--------|--------|------|
| `node/Nodejs面试题.md` | `docs/guide/node-*` 系列 7 篇 | 全部覆盖 |
| `node/Nodejs面试题-重构版.md` | `docs/guide/node-*` 系列 | 同上 |
| `node/Nodejs面试题-精简速记版.md` | `docs/guide/node-*` 系列 | 精简版，内容一致 |
| `Python_FastAPI知识与实战用法手册.md` | `docs/guide/fastapi-*` + `python-*` | 已拆分到 6 篇 |
| `MySQL表结构设计与SQL场景练习手册.md` | `docs/guide/mysql-table-design` + `sql-basics` | 已整合 |
| `全栈开发中的并发事务与数据一致性实战.md` | `docs/guide/concurrency-transaction` | 已整合 |
| `架构设计知识点速记.md` | `docs/guide/backend-thinking.md` | 部分整合 |
| `index.txt` | `docs/guide/backend-thinking.md` | 提取了 REST、微服务、消息队列等 |

---

## 🔄 已补充（从源文件提取到 docs 的新内容）

| 源文件来源 | 补充到 | 补充了什么 |
|-----------|--------|-----------|
| `nestjs-cn.md` | `docs/guide/nestjs-advanced.md` | 文件上传、WebSocket Gateway、循环依赖、软删除、微服务基础 |
| `Python快速入门教程.md` | `docs/guide/python-intro.md` | asyncio 异步编程、虚拟环境、类型标注深入 |
| `index.txt` | `docs/guide/backend-thinking.md` | REST API 设计规范、单体 vs 微服务、架构五原则 |
| 新撰写 | `docs/guide/docker-deployment.md` | 全新模块：Dockerfile、docker-compose、nginx、PM2、CI/CD |
| 新撰写 | `docs/guide/redis-deep.md` | 全新模块：5 种数据结构、缓存策略、分布式锁、实战场景 |
| 新撰写 | `docs/guide/message-queue.md` | 全新模块：RabbitMQ vs Kafka、生产消费、幂等、场景实战 |
| 新撰写 | `docs/guide/fastapi-advanced.md` | 增强：测试深度、中间件、WebSocket、面试话术 |

---

## 📌 个人材料（保留原样，不纳入 docs）

| 文件 | 说明 |
|------|------|
| `项思哲_AI应用_AI全栈_简历局部改写稿.md` | 简历材料 |
| `项思哲_AI应用开发_Agent开发_简历改写稿.md` | 简历材料 |
| `项思哲_AI应用开发_投递优化稿.md` | 简历材料 |
| `项思哲_前端岗位面试复习资料.md` | 面试材料 |
| `Sizhe_Xiang_English_Resume.md` | 英文简历 |
| `简历.md` | 简历 |
| `jd.txt` | 岗位描述 |
| `interview-prep.md` | 面试准备材料 |
| `interview-prep-*.html` / `interview-prep-*.md` | 公司定制面试材料 |
| `本智激活_高级Agent开发工程师_面试背诵手册.md` | 面试材料 |
| `初面高频问题答案版.html` | 面试材料 |

---

## 📚 学习笔记（独立的，不纳入 docs 但保留）

| 文件 | 说明 |
|------|------|
| `agent/Agent教程学习梳理.md` / `.html` | Agent/AI 学习笔记 |
| `agent/LangChain-LangGraph-DeepAgents面试手册.md` | Agent 面试手册 |
| `agent/电商问数agent.md` | Agent 项目笔记 |
| `front-end/prepme-skill双语学习笔记.md` | 英语学习 |
| `front-end/vue2-vue3面试速成.md` | Vue 面试（Vue2 部分过时） |
| `front-end/前端八股必备版.md` | 前端面试八股（JS/浏览器基础仍有效） |
| `python/  .md` | 空文件名（可清理） |

---

## ❌ 过时内容（不建议继续使用）

| 文件 / 内容 | 过时原因 |
|------------|---------|
| `vue2面试题.md` | Vue2 已不再主流，且不是全栈方向 |
| `index.txt` 中的 `.NET / Java EJB / WebX` 部分 | 技术方向不匹配（Java 企业生态，非 Node/Python 全栈） |
| `index.txt` 中的 `Hibernate / MyBatis / SOAP` 对比 | ORM 对比和协议对比已有更现代的替代内容 |
| `nestjs.md`（英文版） | 内容已被 `nestjs-cn.md` 和 docs 覆盖 |
| `front-end/vue2面试题.md` | 同上 |
| `python/  .md`（空文件, 文件名是空格） | 无内容，可直接删除 |

---

## 建议的后续处理

### 可删除
```bash
# 空文件
rm "python/  .md"

# 已完全被 docs 覆盖的 node 源文件（保留一份即可）
# rm node/Nodejs面试题.md node/Nodejs面试题-重构版.md node/Nodejs面试题-精简速记版.md
```

### 建议重命名明确状态
- `index.txt` → `archived/架构旧笔记.txt`（仅保留有用部分后归档）
- `nestjs.md` → `archived/nestjs-english-问答合集.md`（保留英文版参考）

### 其他
- `front-end/前端八股必备版.md` 中 JS/浏览器/HTTP 部分仍有效，可作为前端基础补充参考
- `front-end/vue2-vue3面试速成.md` 如果不再面 Vue 岗位可以考虑归档
