# Node 面试题（精简速记版）

> 版本：2026-05-11  
> 目标读者：前端转全栈  
> 使用方式：面试前快速过一遍，重点记“定义 + 原理 + 场景 + 坑点”。

---

## 1. Node.js 是什么？

**速记答案：**
Node.js 是一个 JavaScript 运行时，不是语言。它基于 V8，并提供 `fs`、`http`、`stream`、`process` 等服务端能力。

**面试展开：**
- 适合 I/O 密集型场景
- 强项是高并发请求处理，不是重 CPU 计算
- 核心是：**事件循环 + 非阻塞 I/O**

---

## 2. Node 为什么常说是“单线程”，却还能扛高并发？

**速记答案：**
Node 默认只有一个主线程执行 JS，但 I/O 不靠主线程硬等，而是交给操作系统和 libuv，结果就绪后再回到事件循环处理。

**面试展开：**
- JS 主线程负责执行回调和业务代码
- I/O 等待不阻塞主线程
- 高并发的关键是“少阻塞，不傻等”

---

## 3. 什么是事件循环？

**速记答案：**
事件循环是 Node 的任务调度机制，持续检查异步任务是否完成，并按阶段调度回调执行。

**面试展开：**
- 常见阶段：`timers`、`poll`、`check`
- `setTimeout` 不保证准点执行，只保证“最早不早于”
- 同步代码太久会拖慢整个事件循环

---

## 4. `process.nextTick()`、Promise、`setImmediate()`、`setTimeout(fn, 0)` 区别？

**速记答案：**
它们都能延后执行，但优先级不同。

**建议记忆顺序：**
1. 同步代码
2. `process.nextTick()`
3. Promise 微任务
4. `setImmediate()` / `setTimeout()` 按事件循环阶段调度

**面试展开：**
- `nextTick` 优先级很高
- 递归塞太多 `nextTick` 会造成 I/O 饥饿
- I/O 回调里经常是 `setImmediate()` 更早执行

---

## 5. Node 的异步 I/O 和线程池是什么关系？

**速记答案：**
异步不等于多线程。Node 的异步有的靠 OS 事件通知，有的靠 libuv 线程池。

**面试展开：**
- 网络 I/O 不一定走线程池
- 一些文件系统、`crypto`、`zlib`、`dns.lookup()` 会用 worker pool
- 重点：**异步是调用方式，不等于底层一定新开线程**

---

## 6. `worker_threads` 是干什么的？

**速记答案：**
`worker_threads` 用来把 CPU 密集型 JS 计算移出主线程，避免阻塞事件循环。

**适用场景：**
- 图像处理
- 压缩/加密
- 大 JSON / AST 处理
- 算法计算

**不适合：**
- 普通 HTTP 请求
- 数据库查询
- 一般文件 I/O

---

## 7. `child_process` 和 `worker_threads` 区别？

**速记答案：**
- `worker_threads`：同进程多线程，适合 CPU 密集型 JS
- `child_process`：新进程，隔离更强，适合调用系统命令或其他程序

**补充：**
- `spawn`：适合大输出、流式处理
- `exec`：适合短命令，但有 shell 注入风险
- `execFile`：不走 shell，更安全
- `fork`：拉起新 Node 进程并带 IPC

---

## 8. CommonJS 和 ESM 有什么区别？

**速记答案：**
- CommonJS：`require()` / `module.exports`
- ESM：`import` / `export`

**面试展开：**
- Node 同时支持两套模块系统
- ESM 更适合静态分析和现代工具链
- ESM 里没有 CommonJS 那些默认变量，如 `__dirname`

---

## 9. `package.json` 的 `type` 有什么作用？

**速记答案：**
它决定当前包里的 `.js` 文件按 ESM 还是 CommonJS 解释。

**速记：**
- `"type": "module"` → `.js` 按 ESM
- `"type": "commonjs"` → `.js` 按 CommonJS

**面试要点：**
很多模块报错本质都和这个字段有关。

---

## 10. `package.json` 的 `exports` 有什么用？

**速记答案：**
`exports` 用来声明包对外暴露哪些入口，限制外部随便访问内部文件。

**面试展开：**
- 收紧公共 API 边界
- 支持条件导出
- 比 `main` 更现代
- 贸然加上可能造成 breaking change

---

## 11. ESM 和 CommonJS 能混用吗？

**速记答案：**
能，但有边界，最好别乱混。

**面试展开：**
- ESM 可以导入 CommonJS
- CommonJS 加载 ESM 往往要用 `import()`
- 容易踩坑：默认导出、命名导出、执行时机

---

## 12. 为什么 Node 早期大量使用 error-first callback？

**速记答案：**
因为异步结果不能靠普通返回值表达，只能通过回调把“成功/失败”一起带回来。

**经典形式：**
```js
fs.readFile('a.txt', (err, data) => {
  if (err) return handle(err)
  console.log(data)
})
```

**面试展开：**
- 统一异步错误出口
- 历史价值很大
- 现代更多改用 Promise / `async-await`

---

## 13. `Promise` 和 `async/await` 解决了什么问题？

**速记答案：**
解决异步流程组合难读、错误传播混乱的问题，让异步代码更可维护。

**面试展开：**
- Promise 解决回调地狱
- `async/await` 让异步代码更接近同步写法
- 但它只是语法层优化，不会把 CPU 阻塞变没

---

## 14. `async/await` 常见误区有哪些？

**速记答案：**
最常见的误区是把能并发的任务写成串行。

**例子：**
```js
const a = await fetchA()
const b = await fetchB()
```
如果没依赖，更适合：
```js
const [a, b] = await Promise.all([fetchA(), fetchB()])
```

**面试展开：**
- `await` 不代表更快
- 要关注并发控制
- 要理解错误边界

---

## 15. `unhandledRejection` 和 `uncaughtException` 是什么？

**速记答案：**
- `unhandledRejection`：Promise reject 了，但没人接
- `uncaughtException`：异常一路冒泡，最终没人处理

**面试展开：**
- 它们适合做日志、告警、清理
- 不该作为业务层正常恢复机制
- `uncaughtException` 后通常应考虑退出进程

---

## 16. `process` 最常用来做什么？

**速记答案：**
- `process.env`：环境变量
- `process.argv`：命令行参数
- `process.cwd()`：当前工作目录
- 进程信号：`SIGINT`、`SIGTERM`

**面试展开：**
服务端里经常用于配置管理、CLI、优雅退出。

---

## 17. `EventEmitter` 的核心机制是什么？

**速记答案：**
就是发布订阅：`on` 监听，`emit` 触发。

**高频追问：监听器是同步还是异步？**
答：**同步调用。**

**面试展开：**
- 事件来源可能是异步 I/O
- 但监听器执行本身默认是同步的
- 监听器里写重 CPU 逻辑会卡当前流程

---

## 18. `Buffer` 是什么？

**速记答案：**
`Buffer` 是 Node 用来表示二进制数据的对象，本质是字节序列。

**面试展开：**
- 文件、网络、加密、流都离不开二进制
- `Buffer` 继承自 `Uint8Array`
- 字符串只是字节的一种解释方式

---

## 19. 什么是 Stream？

**速记答案：**
Stream 是 Node 处理流式数据的抽象，适合大文件、网络传输、压缩、代理转发等场景。

**四类流：**
- `Readable`
- `Writable`
- `Duplex`
- `Transform`

**面试展开：**
它的核心价值是：**边读边处理，避免一次性全量加载到内存。**

---

## 20. 什么是背压（backpressure）？

**速记答案：**
上游产出太快，下游消费不过来，数据就会不断堆积，这就是背压。

**面试展开：**
- 常见于大文件读取、上传、下载、代理转发
- 本质是生产速度和消费速度不匹配
- Stream 用 `write()` 返回值、`drain`、`pipeline()` 等机制处理背压

---

## 21. 为什么推荐 `stream.pipeline()`？

**速记答案：**
因为它比手写多个 `pipe()` 更适合生产环境，能更好处理错误传递、资源关闭和链路清理。

**面试展开：**
Demo 用 `pipe()` 可以，线上更推荐 `pipeline()`。

---

## 22. `fs.readFile()` 和 `fs.createReadStream()` 怎么选？

**速记答案：**
- 小文件、一次性读：`readFile()`
- 大文件、边读边传：`createReadStream()`

**面试展开：**
考点不在 API 名字，而在你是否理解内存占用和处理方式的差别。

---

## 23. 一个最基础的 HTTP 服务，本质上发生了什么？

**速记答案：**
`http.createServer()` 本质是在监听 socket，请求到来后 Node 把它包装成 `IncomingMessage` 和 `ServerResponse` 交给你处理。

**面试展开：**
- 请求本质是字节流
- 请求体、请求头、URL 要分别处理
- 响应最终要 `res.end()`

---

## 24. 为什么上传/下载/代理场景里流式处理几乎是必选项？

**速记答案：**
因为数据量大、持续时间长，如果总是全量读进内存，容易导致内存暴涨和响应变慢。

**面试展开：**
- 边到边处理更符合磁盘和网络的工作方式
- 这类题很适合顺带讲背压

---

## 25. 为什么不能在 Node 主线程里做重 CPU 计算？

**速记答案：**
因为主线程既要跑业务逻辑，又要推进事件循环。重 CPU 会把其他请求一起卡住。

**面试展开：**
- 所有请求延迟一起上升
- timer 和 I/O 回调被拖延
- 解决思路通常是 `worker_threads` 或拆到独立服务

---

## 26. 为什么同步 API 在线上服务里要慎用？

**速记答案：**
因为同步 API 会阻塞事件循环，影响整个服务的吞吐和响应时间。

**典型例子：**
- `readFileSync`
- `execSync`
- 超大 JSON 的同步解析/序列化

**面试展开：**
CLI、小工具、启动阶段可以用；在线请求链路里要慎用。

---

## 27. Node 服务常见内存问题从哪里来？

**速记答案：**
- 全局引用不释放
- 缓存无上限
- 事件监听器泄漏
- 流/连接没关
- 超大对象长期滞留

**面试展开：**
JS 有 GC，不代表不会泄漏；只要对象还可达，GC 就不会回收。

---

## 28. 如何理解“不要阻塞事件循环”？

**速记答案：**
这不是口号，而是 Node 服务设计的核心约束。

**面试展开：**
- 不要写超长同步回调
- 不要滥用同步 API
- 不要把重 CPU 逻辑塞进主线程
- 阻塞严重时还可能被恶意请求放大成 DoS

---

## 29. Node 服务常见安全问题有哪些？

**速记答案：**
- 输入校验不足
- 命令注入
- 路径穿越
- 敏感信息泄露
- 供应链风险

**面试展开：**
前端转全栈的人容易只盯 XSS/CSRF，但 Node 服务端还要关注文件系统、进程和依赖边界。

---

## 30. 为什么 `exec()` 比 `spawn()` / `execFile()` 更危险？

**速记答案：**
因为 `exec()` 通常通过 shell 执行命令，只要用户输入拼进命令字符串，就容易出现命令注入。

**面试展开：**
- 优先用 `spawn()` / `execFile()`
- 传参数数组
- 输入做白名单校验

---

## 31. 综合题：如果让你用 Node 做一个大文件上传服务，你会关注什么？

**速记答案：**
至少答这 5 点：

1. 流式处理
2. 背压控制
3. 异常清理
4. 安全校验
5. 分片上传 / 断点续传 / 对象存储扩展

**面试展开：**
这题能同时考出你对 Stream、背压、错误处理、安全性的理解。

---

## 32. 综合题：如果一个 Node 接口越来越慢，你怎么排查？

**速记答案：**
先分层判断：

1. 是主线程阻塞？
2. 是下游服务慢？
3. 是文件 I/O 慢？
4. 是同步 API 或重 CPU？
5. 是内存 / GC 抖动？

**面试展开：**
重点不在工具名，而在有没有“先判断瓶颈属于哪一层”的意识。

---

# 最后速记：面试前最该讲顺的 8 个题

如果时间真的很少，至少把这 8 个题讲顺：

1. Node 是什么，适合什么场景
2. 事件循环和非阻塞 I/O
3. `nextTick` / Promise / `setImmediate` / `setTimeout`
4. CommonJS / ESM / `type` / `exports`
5. `async/await` 的并发与错误边界
6. `Buffer` / Stream / 背压
7. 为什么不要阻塞事件循环
8. 大文件上传 / BFF / 网关类综合场景

---

# 官方参考资料

- Event Loop  
  https://nodejs.org/en/learn/asynchronous-work/event-loop-timers-and-nexttick
- `process.nextTick()`  
  https://nodejs.org/en/learn/asynchronous-work/understanding-processnexttick
- Don’t Block the Event Loop  
  https://nodejs.org/en/learn/asynchronous-work/dont-block-the-event-loop
- Streams Backpressure  
  https://nodejs.org/en/learn/modules/backpressuring-in-streams
- `worker_threads`  
  https://nodejs.org/api/worker_threads.html
- CommonJS  
  https://nodejs.org/api/modules.html
- ESM  
  https://nodejs.org/api/esm.html
- Packages / `type` / `exports`  
  https://nodejs.org/api/packages.html
