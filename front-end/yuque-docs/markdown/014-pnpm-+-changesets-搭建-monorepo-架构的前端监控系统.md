# pnpm + changesets 搭建 monorepo 架构的前端监控系统

> 来源：https://www.yuque.com/xiumubai/doc/be13gi863o79w8g9

现在越来越多的前端工程都选择 monorepo 的架构进行开发，比如 Vue、React、Babel 等项目都采用 monorepo 的方式进行管理
monorepo 的组织结构如下：
​9123456├── packages|   ├── pkg1|   |   ├── package.json|   ├── pkg2|   |   ├── package.json├── package.json如 [vuejs](https://link.juejin.cn/?target=https%3A%2F%2Fgithub.com%2Fvuejs%2Fcore) 所示，所有子项目都在 packages 目录中
![8bc1ee98-37cb-44d8-a7e3-54b286bca9c8.webp](https://cdn.nlark.com/yuque/0/2025/webp/338969/1750756857585-8bc1ee98-37cb-44d8-a7e3-54b286bca9c8.webp)
本篇作为 [web-see](https://link.juejin.cn/?target=https%3A%2F%2Fgithub.com%2Fxy-sea%2Fweb-see) 前端监控的架构篇，主要聊聊如何使用 monorepo，以及带来的好处有哪些？
关于前端监控系统的知识点，这里推荐笔者的 [如何从0到1搭建前端监控平台](https://juejin.cn/post/7172072612430872584)，文中有详细的介绍
下面先聊聊 monorepo 架构的优势以及如何搭建、如何发布
monorepo 的简单介绍
简单来说，monorepo 就是把多个子工程放到一个 git 仓库中进行管理，各工程之间共用同一套构建流程、代码规范，各工程可以使用link软链接的方式实现相互引用，方便版本的统一管理
monorepo 架构的优势：
1、可以将一个大型项目，拆分成多个子项目，更容易维护和管理代码
2、提高代码共享和重用性，这些子项目可以共享代码和库，可以减少代码重复，降低维护成本
3、由于所有代码都在同一个代码库中，可以更容易地对代码进行构建和测试，有利于持续集成和持续交付
4、更方便的进行版本控制和管理，可以结合 changesets 类似的发布工具，跟踪代码的变更历史和版本变更
pnpm + workspace 搭建 monorepo 项目
pnpm 提出了 workspace 的概念，内置了对 monorepo 的支持，可以用来快速搭建项目
以下 [pnpm-monorepo-changesets](https://link.juejin.cn/?target=https%3A%2F%2Fgithub.com%2Fxy-sea%2Fblog%2Ftree%2Fmain%2Fpnpm-monorepo-changesets) 示例的仓库地址，感兴趣的小伙伴可以动手试试
1、安装 pnpm
​91npm install -g pnpm2、初始化项目
​91pnpm init在根目录下存在 pnpm-workspace.yaml 文件，用来指定工作空间的目录
​912packages:  - 'packages/*'3、创建 packages 目录
在 packages 目录下创建 pkg1 和 pkg2 两个文件（代表两个子工程），分别执行 pnpm init 命令，初始化工程
在 pkg1 和 pkg2 的 src 目录下创建 index.ts 文件，作为项目的入口文件
![1750756857507-134a7e4e-c76b-4b75-9991-4c56ade24b9a.webp](https://cdn.nlark.com/yuque/0/2025/webp/338969/1750756857507-134a7e4e-c76b-4b75-9991-4c56ade24b9a.webp)
4、修改 pkg1 和 pkg2 中 package.json 的 name 属性
分别将 name 修改为 @websee/pk1 、 @websee/pk2，这里的 @websee 是在 npm 官网上创建的组件名
注意: 这个组织名一定要提前创建好，否则各工程相互引用时会报错
![1750756857550-783a8678-44fc-455e-ba07-01a8d77a879c.webp](https://cdn.nlark.com/yuque/0/2025/webp/338969/1750756857550-783a8678-44fc-455e-ba07-01a8d77a879c.webp)
5、修改 pkg1 和 pkg2 package.json 中的 main 属性
main 属性为该工程的入口文件，默认为 "main": "index.js"， 修改为 "main": "src/index.ts"，并添加 publishConfig 属性
最终 package.json 如下
5、各工程间相互引用
要在 pk2 中使用 pk1 的代码，传统的写法如下
这种相对路径的写法很繁琐且不易维护，如果当某一工程的目录结构发生变化时，其他所有引用该工程的文件都要修改
pnpm 通过 workspace 的实现，可以通过直接引用子工程的 name 名称，就可以实现各工程的相互引用，代码如下
pnpm 提供了 [--filter](https://link.juejin.cn/?target=https%3A%2F%2Fpnpm.io%2Fzh%2Ffiltering) 参数，可以用来对特定的 package 进行操作
pkg1 中将 pkg2 作为依赖进行安装，在根目录下执行
此时查看 pkg2 的 package.json，可以看到 dependencies 字段自动添加了 pk1 的引用，证明相互引用添加成功
6、打包验证
这里使用 rollup 打包，安装依赖，pnpm 提供了 [-w](https://link.juejin.cn/?target=https%3A%2F%2Fpnpm.io%2Fzh%2Fpnpm-cli%23-w---workspace-root) 参数，可以将依赖包安装到工程的根目录下，作为所有 package 的公共依赖
创建rollup.config.js
rollup.config.js 会读取 packages 文件中各子目录的名称，并将每一个目录设置成打包的入口文件，并配置对应的出口路径
在根目录 package.json 中配置打包命令
执行 pnpm run build，会在 packages 各目录下生成对应的 dist 文件
changesets
changesets 用来进行版本控制和管理
1、安装依赖
2、初始化
执行完初始化命令后，会在工程的根目录下生成 .changeset 目录
3、在根目录 package.json 中配置对应的命令
下面用两个具体的例子，来演示下 changeset 的发包流程
注意：npm 包一般的版本结构为：1.0.0，类似这样的三位数版本号，分别是对应的 changeset version 里面的：major、minor、patch
npm包版本 1.0.0 更新为 1.1.0
这里 @websee/pk1 和 @websee/pk2 的初始版本都为 1.0.0
执行 pnpm run changeset
1、选择要发布的包
![1750756857555-5c8c5946-557c-43ea-bda5-6ffa9c4da4da.webp](https://cdn.nlark.com/yuque/0/2025/webp/338969/1750756857555-5c8c5946-557c-43ea-bda5-6ffa9c4da4da.webp)
2、发布 minor，选择对应的包
现在是 1.0.0 更新为 1.1.0，这里选择 minor
![1750756857544-71f0d436-9006-4ff0-812f-49c85d5dd381.webp](https://cdn.nlark.com/yuque/0/2025/webp/338969/1750756857544-71f0d436-9006-4ff0-812f-49c85d5dd381.webp)
3、填写 changelog
![1750756858045-663c7955-a35f-4601-a838-381f0ad073d9.webp](https://cdn.nlark.com/yuque/0/2025/webp/338969/1750756858045-663c7955-a35f-4601-a838-381f0ad073d9.webp)
4、Is this your desired changeset 选择true
![1750756858057-3aa68750-29d6-411c-8e48-ddf0074efa9a.webp](https://cdn.nlark.com/yuque/0/2025/webp/338969/1750756858057-3aa68750-29d6-411c-8e48-ddf0074efa9a.webp)
执行 pnpm run packages-version
![1750756858093-1a58bcc1-7eda-4ccd-abad-3a8a9acbcedb.webp](https://cdn.nlark.com/yuque/0/2025/webp/338969/1750756858093-1a58bcc1-7eda-4ccd-abad-3a8a9acbcedb.webp)
提示 All files have been updated
打开 pk1 和 pk2 下的 package.json，发现版本号已修改完成
![1750756858085-eb566536-17fd-403f-87dc-5e4b865654f3.webp](https://cdn.nlark.com/yuque/0/2025/webp/338969/1750756858085-eb566536-17fd-403f-87dc-5e4b865654f3.webp)
同时各目录下会自动生成 CHANGELOG.md 文件，记录版本号的变化
执行 pnpm run publish
发布 1.1.0 版本
![95e49a82-b801-45cf-b28f-46fe064b06f2.webp](https://cdn.nlark.com/yuque/0/2025/webp/338969/1750756858071-95e49a82-b801-45cf-b28f-46fe064b06f2.webp)
在 npm 官网上搜索 @websee/pk1，证明发布成功
![41b0cb59-7923-4cb0-a95e-707d39c87511.webp](https://cdn.nlark.com/yuque/0/2025/webp/338969/1750756858568-41b0cb59-7923-4cb0-a95e-707d39c87511.webp)
npm包 1.1.0 更新为 2.1.0
继续发布 2.1.0 版本，
执行 pnpm run changeset
不同点在于选择发布 major，剩余的流程和上面的都一样
![1750756858573-a525d2cb-aae8-4912-993d-17869dc73e55.webp](https://cdn.nlark.com/yuque/0/2025/webp/338969/1750756858573-a525d2cb-aae8-4912-993d-17869dc73e55.webp)
为何要使用 monorepo 架构搭建前端监控
目前 [web-see](https://link.juejin.cn/?target=https%3A%2F%2Fgithub.com%2Fxy-sea%2Fweb-see) 前端监控 SDK，主要功能有代码报错、性能检测、页面录屏、记录用户行为、白屏检测等功能
老版本存在的主要问题有：[test 分支](https://link.juejin.cn/?target=https%3A%2F%2Fgithub.com%2Fxy-sea%2Fweb-see%2Ftree%2Ftest)
1、这些功能的代码全部耦合在一起，随着SDK功能的增多，体积越来越大，打包后的体积为 147K
![1750756858545-6e45b15f-b2d0-4a90-92a4-56395d05e805.webp](https://cdn.nlark.com/yuque/0/2025/webp/338969/1750756858545-6e45b15f-b2d0-4a90-92a4-56395d05e805.webp)
2、有些用户用不到某些功能，不希望加载该插件，以减少SDK体积
3、用户想要自定义扩展非常不方便
使用 monorepo 架构改造后的结果：[main 分支](https://link.juejin.cn/?target=https%3A%2F%2Fgithub.com%2Fxy-sea%2Fweb-see%2Ftree%2Ftest)
1、将 SDK 主要拆分为3个项目
●@websee/core 核心模块：包含代码报错、记录用户行为、白屏检测等功能，体积为 41K
●@websee/performance 性能检测模块，体积为 26K
●@websee/recordscreen 页面录屏模块，体积为 116K
2、用户可以根据自己的需求，选择项的安装性能检测与页面录屏模块
3、用户想要自定义扩展其他功能，可以继续在 packages 添加新的模块，并且模块间相互引用更加方便快捷
![1750756858592-2aadc0b6-91f1-4ecf-8729-73cc0e4f2329.webp](https://cdn.nlark.com/yuque/0/2025/webp/338969/1750756858592-2aadc0b6-91f1-4ecf-8729-73cc0e4f2329.webp)
当前的 packages 目录
​991234567891011121314├── packages|   ├── common // 公共变量|   |   ├── package.json|   ├── core // 核心模块|   |   ├── package.json|   ├── performance // 性能检测|   |   ├── package.json|   ├── recordscreen // 页面录屏|   |   ├── package.json|   |── types // ts类型|   |   ├── package.json|   |── utils // 公共方法|   |   ├── package.json├── package.jsonSDK 架构设计
SDK 为支持插件 可拓展、可插拔的特点，整体架构是 内核 + 插件 + 发布订阅模式 的设计
1、@websee/core 核心模块主要是内核 + 发布订阅模式
​99123456789101112131415161718192021222324// handlers 存储所有的事件和对应的回调函数const handlers: { [key in EVENTTYPES]?: ReplaceCallback[] } = {};// subscribeEvent 设置标识，并将处理的方法放置到handlers中，如{ xhr: [ funtion ] }export function subscribeEvent(handler: ReplaceHandler): boolean {  if (!handler || getFlag(handler.type)) return false;  setFlag(handler.type, true);  handlers[handler.type] = handlers[handler.type] || [];  handlers[handler.type]?.push(handler.callback);  return true;}export function notify(type: EVENTTYPES, data?: any): void {  if (!type || !handlers[type]) return;  // 获取对应事件的回调函数并执行，回调函数为addReplaceHandler事件中定义的事件  handlers[type]?.forEach(callback => {    nativeTryCatch(      () => {        callback(data);      },      (e: any) => {        console.error(`web-see 重写事件notify的回调函数发生错误，Type:${type} ${e}`);      }    );  });}2、@websee/performance 和 @websee/recordscreen 插件都继承于BasePlugin
​9123456789export abstract class BasePlugin {  public type: string; // 插件类型  constructor(type: string) {    this.type = type;  }  abstract bindOptions(options: object): void; // 校验参数  abstract core(sdkBase: SdkBase): void; // 核心方法  abstract transform(data: any): void; // 数据转化}3、通过调用 @websee/core的use方法来注册插件
​Plain TextCopy99123456789101112131415function use(plugin: any, option: any) {  const instance = new plugin(option);  if (    !subscribeEvent({      callback: data => {        instance.transform(data);      },      type: instance.type,    })  ) return;  nativeTryCatch(() => {    // 执行插件的core方法    instance.core({ transportData, breadcrumb, options, notify });  });}SDK 安装说明
以下为 vue2 的安装说明
​Plain TextCopy991234567891011121314151617181920212223242526import webSee from '@websee/core';import performance from '@websee/performance';import recordscreen from '@websee/recordscreen';
Vue.use(webSee, {  dsn: 'http://test.com/reportData',  apikey: 'abcd',  silentWhiteScreen: true, // 开启白屏检测  skeletonProject: true, // 页面包含骨架屏  repeatCodeError: true, // 开启错误上报去重，重复的代码错误只上报一次  userId: '123',  handleHttpStatus(data) { // (自定义 hook) 根据接口返回的 response 判断请求是否正确    let { url, response } = data;    let { code } = typeof response === 'string' ? JSON.parse(response) : response;    if (url.includes('/getErrorList')) {      return code === 200 ? true : false;    } else {      return true;    }  }});
// 注册性能检测插件webSee.use(performance);// 注册页面录屏插件webSee.use(recordscreen);最后通过 changesets 来管理各个模块的版本，统一发布
总结
本文通过 [web-see](https://link.juejin.cn/?target=https%3A%2F%2Fgithub.com%2Fxy-sea%2Fweb-see) 前端监控实际的案例，来讲解采用 monorepo 架构的好处以及它解决的实际问题
有兴趣的小伙伴可以结合git仓库的源码和本文一起阅读，帮助加深理解
后续
下一篇会继续讨论前端监控，聊一聊前端监控的报警机制
参考文章：
[pnpm + workspace + changesets 构建你的 monorepo 工程](https://juejin.cn/post/7098609682519949325)
[腾讯三面：说说前端监控平台/监控SDK的架构设计和难点亮点？](https://juejin.cn/post/7108660942686126093)
