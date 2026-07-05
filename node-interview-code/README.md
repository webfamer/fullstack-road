# Node 面试题代码版

这套代码把 `Nodejs面试题-重构版.md` 里保留下来的“建议手写题”实现成了可运行 demo。

目标不是做生产框架，而是让你把这些面试题真正跑起来：

1. 简单静态文件服务器
2. `readFile` vs Stream 大文件下载对比
3. `pipeline()` 文件压缩
4. BFF 聚合接口 + 超时控制
5. 故意阻塞事件循环，再改成 `worker_threads`
6. CommonJS / ESM 互操作 demo
7. 优雅退出（`SIGTERM`）

## 目录

```txt
node-interview-code/
├── 01-static-file-server/
├── 02-download-compare/
├── 03-pipeline-gzip/
├── 04-bff-timeout/
├── 05-event-loop-blocking/
├── 06-cjs-esm-interop/
├── 07-graceful-shutdown/
├── shared/
└── scripts/
```

## 运行环境

- Node.js 18+ 更稳妥
- 无第三方依赖

## 先准备大文件样本

```bash
cd node-interview-code
npm run prepare:sample
```

会生成：

- `shared/public/hello.txt`
- `shared/public/index.html`
- `shared/sample-large.txt`（约 20MB）

---

## 1) 静态文件服务器

```bash
npm run server:static
```

打开：

- http://127.0.0.1:3001/
- http://127.0.0.1:3001/hello.txt

考点：

- `http.createServer`
- 路径解析与简单安全控制
- `createReadStream`
- 基础 MIME type

---

## 2) 大文件下载：`readFile` vs Stream

```bash
npm run server:download
```

打开：

- http://127.0.0.1:3002/readFile
- http://127.0.0.1:3002/stream
- http://127.0.0.1:3002/metrics

考点：

- 为什么大文件更适合 Stream
- `pipeline()` 的错误传递和资源清理
- 内存占用差异

---

## 3) `pipeline()` 压缩脚本

```bash
npm run gzip
```

它会把 `shared/sample-large.txt` 压缩成：

- `shared/sample-large.txt.gz`

考点：

- `pipeline()` 比裸 `pipe()` 更适合生产环境
- 出错时自动清理链路

---

## 4) BFF 聚合接口 + 超时控制

```bash
npm run bff
```

打开：

- http://127.0.0.1:3003/api/profile
- http://127.0.0.1:3003/api/orders
- http://127.0.0.1:3003/bff/dashboard
- http://127.0.0.1:3003/bff/dashboard?ordersDelay=1200

考点：

- `Promise.allSettled`
- `AbortController`
- 聚合接口的部分失败处理

---

## 5) 阻塞事件循环 vs Worker 版本

先看阻塞版：

```bash
npm run block
```

再看 Worker 版：

```bash
npm run worker
```

考点：

- 主线程被 CPU 任务卡住时，timer 会明显延迟
- `worker_threads` 如何把 CPU 密集任务移走

---

## 6) CommonJS / ESM 互操作

先跑 CommonJS 入口：

```bash
npm run interop:cjs
```

再跑 ESM 入口：

```bash
npm run interop:esm
```

考点：

- ESM 如何导入 CommonJS
- CommonJS 如何通过 `import()` 加载 ESM

---

## 7) 优雅退出

```bash
npm run graceful
```

另开一个终端：

```bash
curl http://127.0.0.1:3004/slow
```

然后回到服务终端按 `Ctrl+C`，或：

```bash
kill -TERM <pid>
```

考点：

- `SIGINT` / `SIGTERM`
- `server.close()`
- 拒绝新请求、等待旧请求完成、超时强退

---

## 建议你怎么学

建议顺序：

1. 先跑 01、02、03，理解 `http`、Stream、`pipeline`
2. 再跑 04，理解 BFF 聚合和超时控制
3. 再跑 05，体会“不要阻塞事件循环”
4. 最后跑 06、07，补模块系统和进程管理

## 对照面试题

- 事件循环 / 阻塞主线程 → `05-event-loop-blocking`
- Stream / 背压 / `pipeline` → `02-download-compare`, `03-pipeline-gzip`
- CommonJS / ESM → `06-cjs-esm-interop`
- `process` / 优雅退出 → `07-graceful-shutdown`
- BFF / I/O 密集型 → `04-bff-timeout`
