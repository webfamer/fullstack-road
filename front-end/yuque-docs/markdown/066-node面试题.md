# node面试题

> 来源：https://www.yuque.com/xiumubai/doc/pm2t4s0rvzr2l5v4

01：如何监控文件的变动

1在 node 中调用 API fs.watch
2在 linux 中原理是 inotify，macos 中原理是 FSEvents，windows 中原理是 ReadDirectoryChangesW
3由于内核对文件监控更加细粒度，更加敏感，当每次修改文件时可能触发内核多次调用，需要防抖
4注意软链接，读写权限等文件系统属性

可参考文章 [How to Watch for Files Changes in Node.js(opens in a new tab)](https://thisdavej.com/how-to-watch-for-files-changes-in-node-js/) 及 [精读《如何利用 Nodejs 监听文件夹》](https://github.com/dt-fe/weekly/blob/v2/059.精读《如何利用 Nodejs 监听文件夹》.md)

02：在 Node 应用中如何利用多核心 CPU 的优势

使用 cluster 模块

[Node 中 cluster 的原理是什么](https://github.com/shfshanyue/Daily-Question/issues/141)

03：Node 中 cluster 的原理是什么

1fork 子进程
2Load Balance
3多进程共享端口

04：Node 中如何判断一个路径是文件还是文件夹

●isFile()：检测是否为常规文件
●isDirectory()：检测是否为文件夹

05：以下代码，koa 会返回什么数据

​99123456789101112const Koa = require("koa");const app = new Koa(); app.use(async (ctx, next) => {  ctx.body = "hello, 1";}); app.use((ctx) => {  ctx.body = "hello, 2";}); app.listen(3000);

​9912345678910111213const Koa = require("koa");const app = new Koa(); app.use(async (ctx, next) => {  ctx.body = "hello, 1";  await next();}); app.use((ctx) => {  ctx.body = "hello, 2";}); app.listen(3000);

根据 koa 的洋葱模型，返回结果是：

06：什么是 koa 的洋葱模型

Koa 的洋葱模型指的是以 next() 函数为分割点，先由外到内执行 Request 的逻辑，再由内到外执行 Response 的逻辑。

通过洋葱模型，将多个中间件之间通信等变得更加可行和简单。 其实现的原理并不是很复杂，主要是 compose 方法。

07：Node 如何进行进程间通信

对于 spawn/fork 出来的父子进程来说，可以通过 pipe 的方式

●process.on('message')/process.send
●stdin.on/stdout.write

对于并无相关的进程

●socket
●message queue

08：Node 应用中如何查看 gc 的日志

通过开启参数 --trace-gc 与 --trace-gc-verbose

09：Node 中循环引用会发生什么

在 CommonJS 规范中，当遇到require()语句时，会执行require模块中的代码，并缓存执行的结果，当下次再次加载时不会重复执行，而是直接取缓存的结果。正因为此，出现循环依赖时才不会出现无限循环调用的情况。

当执行node a.js时：

10：简述 node/v8 中的垃圾回收机制

v8 中的垃圾回收机制分为三种

1Scavenge，工作在新生代，把 from space 中的存活对象移至 to space
2Mark-Sweep，标记清除。新生代的某些对象由于过度活跃会被移至老生代，此时对老生代中活对象进行标记，并清理死对象
3Mark-Compact，标记整理。

相关链接

1[主流的垃圾回收机制都有哪些?(opens in a new tab)](https://www.zhihu.com/question/32373436)
2[各种编程语言的实现都采用了哪些垃圾回收算法](https://www.zhihu.com/question/20018826)

11：node 中 dns.resolve 及 dns.lookup 有什么区别

dns.resolve 返回指定类型或全部类型的 dns 解析记录，如A记录, CNAME记录, MX记录 dns.lookup返回A记录(IPv4)或AAAA记录(IPv6)

12：Node 中 require json 文件数据时，如何当文件更新时，重新 require

13：有没有接触过 fs-extra，它是解决什么问题的

fs-extra 是 fs 的一个扩展，提供了非常多的便利 API，并且继承了 fs 所有方法和为 fs 方法添加了 promise 的支持。

14：在 node 中如何开启 https

在 express 中开启 https，如下代码所示：

15：node 中 module.exports 与 exports 有什么区别

一句话：exports 是 module.exports 的引用，如果 exports 没有重赋值，则二者没有任何区别，原理就在于 CommonJS 的 module_wrapper，compiledWrapper.call(thisValue, module.exports, require, module)。

类似如下所示

那以下代码结果会如何导出？

很显然会导出 100，毕竟 exports 进行了重赋值。

那在 node 源码中如何实现的呢？ 从源码里可以看出 exports 的实质
![](https://cdn.nlark.com/yuque/0/2023/png/1461594/1691487177753-776ccbd3-17ba-4a54-9b86-e4b9690940cc.png?x-oss-process=image%2Fwatermark%2Ctype_d3F5LW1pY3JvaGVp%2Csize_36%2Ctext_56iL5bqP5ZGYU3VuZGF5%2Ccolor_FFFFFF%2Cshadow_50%2Ct_80%2Cg_se%2Cx_10%2Cy_10)

详见源码: [https://github.com/nodejs/node/blob/master/lib/internal/modules/cjs/loader.js#L1252(opens in a new tab)](https://github.com/nodejs/node/blob/master/lib/internal/modules/cjs/loader.js#L1252)，可以看出符合猜想

众所周知，node 中所有的模块代码都被包裹在这个函数中

而以下源码指出，exports 是如何得来

我们再对示例代码放在包裹函数中，最终导出结果如何一目了然

16：如何得知目前 node 版本的 v8 版本号

在 process.versions 中可以查看 node 及相关依赖的版本号

17：在 node 中如何判断一个对象是 stream

stream 可以通过缓冲区来高效利用内存，从而提高性能。常用场景如读写大文件、http-server 中的大静态文件渲染。

每一个 stream 都有 pipe 函数，可以用来判断一个对象是否 stream。

代码如下，摘自 [is-stream(opens in a new tab)](https://github.com/sindresorhus/is-stream/blob/master/index.js): 一个周下载量两千万的 npm package。

18：node 中 nextTick 与 setTimeout 有什么区别

nextTick属于微任务，setTimeout属于宏任务，在事件循环中执行的优先级不一样

19：请简述重新登录 refresh token 的原理

Refresh Token，将会话管理流程改进如下。

●客户端使用用户名密码进行认证
●服务端生成有效时间较短的 Access Token（例如 10 分钟），和有效时间较长的 Refresh Token（例如 7 天）
●客户端访问需要认证的接口时，携带 Access Token
●如果 Access Token 没有过期，服务端鉴权后返回给客户端需要的数据
●如果携带 Access Token 访问需要认证的接口时鉴权失败（例如返回 401 错误），则客户端使用 Refresh Token 向刷新接口申请新的 Access Token
●如果 Refresh Token 没有过期，服务端向客户端下发新的 Access Token
●客户端使用新的 Access Token 访问需要认证的接口

Refresh Token 提供了服务端禁用用户 Token 的方式，当用户需要登出或禁用用户时，只需要将服务端的 Refresh Token 禁用或删除，用户就会在 Access Token 过期后，由于无法获取到新的 Access Token 而再也无法访问需要认证的接口。这样的方式虽然会有一定的窗口期（取决于 Access Token 的失效时间），但是结合用户登出时客户端删除 Access Token 的操作，基本上可以适应常规情况下对用户认证鉴权的精度要求。

20：简述 koa 的中间件原理，手写 koa-compose 代码

21：在 Node 中如何发送请求

如果使用原生 API，可使用 http/https 核心模块：

如果使用第三方库的话，可使用 axios 等。

目前，Node 团队抛弃了核心模块 http/https 从头开发了一个新的 http client，名为 [undeci(opens in a new tab)](https://github.com/nodejs/undici)，将有可能成为以后默认的 http client

22：Node 中服务端框架如何解析 http 的请求体 body

在 Node 服务中，通过 http.createServer 接收到的 req 为可读流，对流进行读取数据

23：在 Node 中流 (stream) 分为几类，有哪些应用场景

Node.js 中有四种基本的流类型：

●Writable: 可以写入数据的流（例如，fs.createWriteStream()）。
●Readable: 可以从中读取数据的流（例如，fs.createReadStream()）。
●Duplex: Readable 和 Writable 的流（例如，net.Socket）。
●Transform: 可以在写入和读取数据时修改或转换数据的 Duplex 流（例如，zlib.createDeflate()）

24：请简述下 Node 与浏览器环境中的事件循环

众所周知，js 是单线程的语言，同一时间只做一件事，单线程也就导致一个任务执行完才能执行下一个任务，一旦某个任务执行时间太长就容易造成阻塞，为了解决这一问题，js 引入了事件循环机制

js 单线程任务分为同步任务和异步任务

同步任务：立即执行的任务，直接在主线程上排队执行 异步任务：不进入主线程，而是在异步任务有了结果之后将回调函数放入到任务队列中等待主线程空闲时调用执行

主线程任务执行完毕后从任务队列中不断读取任务，放入到主线程去执行，这个过程是循环不停的

而异步任务又可以分为宏任务和微任务

微任务和宏任务 常见微任务：Promise.then，Object.observe，MutationObserver，process.nextTick(Node 环境) 常见宏任务：setTimeout，ajax，dom 事件，setImmediate(Node 环境)，requestAnimationFrame

同步任务执行完毕后会开始从调用栈中去执行异步任务，优先执行的是微任务，当微任务队列清空后才会去执行宏任务，每次单个宏任务执行完毕后会去检查微任务队列是否为空，如果不为空会按照先入先出的原则执行微任务，待微任务队列清空后再执行下一个宏任务，如此循环往复，这种运行机制就叫做事件循环

25：有没有使用过 Node 的 inspect 这个核心模块

inspector 模块提供了与 V8 检查器交互的 API。

​JavaScriptRun CodeCopy912345const session = new inspector.Session();session.connect();session.post("Profiler.enable", () => {  session.post("Profiler.start", start);});
