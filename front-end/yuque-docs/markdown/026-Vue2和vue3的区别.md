# Vue2和vue3的区别

> 来源：https://www.yuque.com/xiumubai/doc/tydgwmg3ue2n184k

面试官：vue3有了解过吗？能说说跟vue2的区别吗？
一、Vue3介绍

关于vue3的重构背景，尤大是这样说的：

「Vue 新版本的理念成型于 2018 年末，当时 Vue 2 的代码库已经有两岁半了。比起通用软件的生命周期来这好像也没那么久，但在这段时期，前端世界已经今昔非比了

在我们更新（和重写）Vue 的主要版本时，主要考虑两点因素：首先是新的 JavaScript 语言特性在主流浏览器中的受支持水平；其次是当前代码库中随时间推移而逐渐暴露出来的一些设计和架构问题」

简要就是：

●利用新的语言特性(es6)
●解决架构问题

哪些变化

![](/api/filetransfer/images?url=https%3A%2F%2Fstatic.vue-js.com%2F9169a900-5087-11eb-85f6-6fac77c0c9b3.png&sign=4d2c115d8e479cddb1ca1fadfe07d8c4772bbdb382531b92d71af9008866cd99)

从上图中，我们可以概览Vue3的新特性，如下：

●速度更快
●体积减少
●更易维护
●更接近原生
●更易使用

速度更快

vue3相比vue2

● 重写了虚拟Dom实现
● 编译模板的优化
● 更高效的组件初始化
● undate性能提高1.3~2倍
● SSR速度提高了2~3倍

![](/api/filetransfer/images?url=https%3A%2F%2Fstatic.vue-js.com%2Fac1d23d0-5087-11eb-ab90-d9ae814b240d.png&sign=bc5418733abd9571a711b6af02507b7aad6f773b0befb150ef84ca35ec339bb1)

体积更小

通过webpack的tree-shaking功能，可以将无用模块“剪辑”，仅打包需要的

能够tree-shaking，有两大好处：

● 对开发人员，能够对vue实现更多其他的功能，而不必担忧整体体积过大
● 对使用者，打包出来的包体积变小了

vue可以开发出更多其他的功能，而不必担忧vue打包出来的整体体积过多

![](/api/filetransfer/images?url=https%3A%2F%2Fstatic.vue-js.com%2Fc01af010-5087-11eb-85f6-6fac77c0c9b3.png&sign=3f4ecee61cdabd19172da9e3fc27ae0b9fc4fb27441689622cdd1146d862c787)

更易维护

compositon Api

●可与现有的Options API一起使用
●灵活的逻辑组合与复用
●Vue3模块可以和其他框架搭配使用

![](/api/filetransfer/images?url=https%3A%2F%2Fstatic.vue-js.com%2Fc5c919b0-5087-11eb-ab90-d9ae814b240d.png&sign=96ea43cd9ede02f1ce7ed50e8e537721e26fe90420dfc8650bf1b0d24706fd62)

更好的Typescript支持

VUE3是基于typescipt编写的，可以享受到自动的类型定义提示

![](/api/filetransfer/images?url=https%3A%2F%2Fstatic.vue-js.com%2Fcc688120-5087-11eb-ab90-d9ae814b240d.png&sign=f994f1d7418756dcbb70ef324a3c0099421580e4668ea9fe6e6254f663cb860f)

编译器重写

![](/api/filetransfer/images?url=https%3A%2F%2Fstatic.vue-js.com%2Ffcd33800-5087-11eb-85f6-6fac77c0c9b3.png&sign=c8661a0fb19b781017c3846b90fbb5d549487a80cf3654485a23935a6e74e8ed)

更接近原生

可以自定义渲染 API

![](/api/filetransfer/images?url=https%3A%2F%2Fstatic.vue-js.com%2F0c7d88a0-5088-11eb-ab90-d9ae814b240d.png&sign=0f6edec4c4d880997d9e01fd8e425e35c63109455fec6d7c1ef2ed8c28c74d02)

更易使用

响应式 Api 暴露出来

![](/api/filetransfer/images?url=https%3A%2F%2Fstatic.vue-js.com%2F26070260-5088-11eb-ab90-d9ae814b240d.png&sign=43d58e10cdaa6407662db12dd37591b2a8e2856c53498931d59716c2947df0ad)

轻松识别组件重新渲染原因

![](/api/filetransfer/images?url=https%3A%2F%2Fstatic.vue-js.com%2F43b2fcb0-5088-11eb-ab90-d9ae814b240d.png&sign=0cfae4a0dbe5c16821cc09ac387f61e27bd85570ccaef2043d1f9ff305980a90)

二、Vue3新增特性

Vue 3 中需要关注的一些新功能包括：

●fragment
●Teleport
●composition Api
●createRenderer

fragment

在 Vue3.x 中，组件现在支持有多个根节点

Teleport

Teleport 是一种能够将我们的模板移动到 DOM 中 Vue app 之外的其他位置的技术，就有点像哆啦A梦的“任意门”

在vue2中，像 modals,toast 等这样的元素，如果我们嵌套在 Vue 的某个组件内部，那么处理嵌套组件的定位、z-index 和样式就会变得很困难

通过Teleport，我们可以在组件的逻辑位置写模板代码，然后在 Vue 应用范围之外渲染它

createRenderer

通过createRenderer，我们能够构建自定义渲染器，我们能够将 vue 的开发模型扩展到其他平台

我们可以将其生成在canvas画布上

![](https://www.yuque.com/api/filetransfer/images?url=https%3A%2F%2Fp1-juejin.byteimg.com%2Ftos-cn-i-k3u1fbpfcp%2Fda4437845ec54eb3829313c92fc81afe%7Etplv-k3u1fbpfcp-watermark.image&sign=d97b0d38df438788f70ecb955f9b3cb543b31aa6b5483de2e509608321b4af74&date=1780734146957)![](data:image/svg+xml;utf8,%3C%3Fxml%20version%3D%221.0%22%20encoding%3D%22UTF-8%22%3F%3E%0A%3Csvg%20width%3D%2218px%22%20height%3D%2216px%22%20viewBox%3D%220%200%2018%2016%22%20version%3D%221.1%22%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20xmlns%3Axlink%3D%22http%3A%2F%2Fwww.w3.org%2F1999%2Fxlink%22%3E%0A%20%20%20%20%3Cg%20id%3D%22%E9%A1%B5%E9%9D%A2-2%22%20stroke%3D%22none%22%20stroke-width%3D%221%22%20fill%3D%22none%22%20fill-rule%3D%22evenodd%22%3E%0A%20%20%20%20%20%20%20%20%3Cg%20id%3D%22%E5%85%B6%E4%BB%96%E5%8D%A1%E7%89%87%22%20transform%3D%22translate(-831.000000%2C%20-7078.000000)%22%3E%0A%20%20%20%20%20%20%20%20%20%20%20%20%3Cg%20id%3D%22%E7%BC%96%E7%BB%84-10%22%20transform%3D%22translate(729.000000%2C%207032.000000)%22%3E%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%3Cg%20id%3D%22%E7%BC%96%E7%BB%84-15%22%20transform%3D%22translate(102.000000%2C%2046.000000)%22%3E%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%3Cg%20id%3D%22image%E5%A4%87%E4%BB%BD%22%3E%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%3Crect%20id%3D%22%E7%9F%A9%E5%BD%A2%22%20fill%3D%22%23000000%22%20fill-rule%3D%22nonzero%22%20opacity%3D%220%22%20x%3D%220%22%20y%3D%220%22%20width%3D%2216%22%20height%3D%2216%22%3E%3C%2Frect%3E%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%3Cpath%20d%3D%22M2.125%2C12.375%20L2.125%2C10.4960156%20L4.194125%2C8.042375%20C4.24407812%2C7.98315625%204.33529688%2C7.98315625%204.38525%2C8.042375%20L6.63471875%2C10.7098437%20L10.1869531%2C6.49754687%20C10.2369063%2C6.43832812%2010.328125%2C6.43832812%2010.3780781%2C6.49754687%20L13.875%2C10.64425%20L13.875%2C12.375%20L13.875%2C3.625%20L2.125%2C3.625%20L2.125%2C12.375%20Z%20M1.5%2C2.5%20L14.5%2C2.5%20C14.7761406%2C2.5%2015%2C2.72385937%2015%2C3%20L15%2C13%20C15%2C13.2761406%2014.7761406%2C13.5%2014.5%2C13.5%20L1.5%2C13.5%20C1.22385937%2C13.5%201%2C13.2761406%201%2C13%20L1%2C3%20C1%2C2.72385937%201.22385937%2C2.5%201.5%2C2.5%20Z%20M4.75%2C7%20C4.05964063%2C7%203.5%2C6.44035937%203.5%2C5.75%20C3.5%2C5.05964063%204.05964063%2C4.5%204.75%2C4.5%20C5.44035937%2C4.5%206%2C5.05964063%206%2C5.75%20C6%2C6.44035937%205.44035937%2C7%204.75%2C7%20Z%22%20id%3D%22%E5%BD%A2%E7%8A%B6%22%20fill%3D%22%238C8C8C%22%3E%3C%2Fpath%3E%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%3C%2Fg%3E%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%3Cg%20id%3D%22alert-fill%22%20transform%3D%22translate(9.000000%2C%207.000000)%22%3E%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%3Cpath%20d%3D%22M4.870227%2C0.216197695%20L8.94272401%2C7.35134981%20C9.01909103%2C7.48514349%209.01909206%2C7.64998385%208.94272672%2C7.78377851%20C8.86636138%2C7.91757317%208.72523106%2C8%208.57249701%2C8%20L0.427502991%2C8%20C0.274768942%2C8%200.133638625%2C7.91757317%200.0572732809%2C7.78377851%20C-0.0190920629%2C7.64998385%20-0.0190910287%2C7.48514349%200.0572759941%2C7.35134981%20L4.129773%2C0.216197695%20C4.20614384%2C0.0824130438%204.34727177%2C0%204.5%2C0%20C4.65272823%2C0%204.79385616%2C0.0824130438%204.870227%2C0.216197695%20Z%22%20id%3D%22%E5%BD%A2%E7%8A%B6%22%20fill%3D%22%23F7D844%22%3E%3C%2Fpath%3E%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%3Cpolygon%20id%3D%22%E8%B7%AF%E5%BE%84%22%20fill%3D%22%23FFFFFF%22%20points%3D%224.07248614%205.8378327%204.07248614%206.70269962%204.92751386%206.70269962%204.92751386%205.8378327%22%3E%3C%2Fpolygon%3E%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%3Cpolygon%20id%3D%22%E8%B7%AF%E5%BE%84%22%20fill%3D%22%23FFFFFF%22%20points%3D%224.07248614%202.81079846%204.07248614%204.97296577%204.92751386%204.97296577%204.92751386%202.81079846%204.07248614%202.81079846%22%3E%3C%2Fpolygon%3E%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%3C%2Fg%3E%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%3C%2Fg%3E%0A%20%20%20%20%20%20%20%20%20%20%20%20%3C%2Fg%3E%0A%20%20%20%20%20%20%20%20%3C%2Fg%3E%0A%20%20%20%20%3C%2Fg%3E%0A%3C%2Fsvg%3E%0A)Network error, can't display image

关于createRenderer，我们了解下基本使用，就不展开讲述了

composition Api

composition Api，也就是组合式api，通过这种形式，我们能够更加容易维护我们的代码，将相同功能的变量进行一个集中式的管理

![](/api/filetransfer/images?url=https%3A%2F%2Fstatic.vue-js.com%2F5e0bfb70-5088-11eb-ab90-d9ae814b240d.png&sign=85468f2d10c2be3d14f48c281944e44c1da1ca254819888248dd9a7e29657e01)

关于compositon api的使用，这里以下图展开

![](/api/filetransfer/images?url=https%3A%2F%2Fstatic.vue-js.com%2F6f67a590-5088-11eb-85f6-6fac77c0c9b3.png&sign=beccecbfb8f5359bc5d637d75212dc0ed1c1b49a4e37a64c5e40eb29018d6210)

简单使用:

三、非兼容变更

Global API

●全局 Vue API 已更改为使用应用程序实例
●全局和内部 API 已经被重构为可 tree-shakable

模板指令

●组件上 v-model 用法已更改
●<template v-for>和 非 v-for节点上key用法已更改
●在同一元素上使用的 v-if 和 v-for 优先级已更改
●v-bind="object" 现在排序敏感
●v-for 中的 ref 不再注册 ref 数组

组件

●只能使用普通函数创建功能组件
●functional 属性在单文件组件 (SFC)
●异步组件现在需要 defineAsyncComponent 方法来创建

渲染函数

●渲染函数API改变
●$scopedSlots property 已删除，所有插槽都通过 $slots 作为函数暴露
●自定义指令 API 已更改为与组件生命周期一致
●一些转换 class 被重命名了：
○v-enter -> v-enter-from
○v-leave -> v-leave-from
●组件 watch 选项和实例方法 $watch不再支持点分隔字符串路径，请改用计算函数作为参数
●在 Vue 2.x 中，应用根容器的 outerHTML 将替换为根组件模板 (如果根组件没有模板/渲染选项，则最终编译为模板)。VUE3.x 现在使用应用程序容器的 innerHTML。

其他小改变

●destroyed 生命周期选项被重命名为 unmounted
●beforeDestroy 生命周期选项被重命名为 beforeUnmount
●[prop default工厂函数不再有权访问 this 是上下文
●自定义指令 API 已更改为与组件生命周期一致
●data 应始终声明为函数
●来自 mixin 的 data 选项现在可简单地合并
●attribute 强制策略已更改
●一些过渡 class 被重命名
●组建 watch 选项和实例方法 $watch不再支持以点分隔的字符串路径。请改用计算属性函数作为参数。
●<template> 没有特殊指令的标记 (v-if/else-if/else、v-for 或 v-slot) 现在被视为普通元素，并将生成原生的 <template> 元素，而不是渲染其内部内容。
●在Vue 2.x 中，应用根容器的 outerHTML 将替换为根组件模板 (如果根组件没有模板/渲染选项，则最终编译为模板)。Vue 3.x 现在使用应用容器的 innerHTML，这意味着容器本身不再被视为模板的一部分。

移除 API

●keyCode 支持作为 v-on 的修饰符
●$on，$off和$once 实例方法
●过滤filter
●内联模板 attribute
●$destroy 实例方法。用户不应再手动管理单个Vue 组件的生命周期。

参考文献

●[https://vue3js.cn/docs/zh/guide/migration/introduction.html#模板指令](https://vue3js.cn/docs/zh/guide/migration/introduction.html#%E6%A8%A1%E6%9D%BF%E6%8C%87%E4%BB%A4)
●[https://composition-api.vuejs.org/zh/#api-介绍](https://composition-api.vuejs.org/zh/#api-%E4%BB%8B%E7%BB%8D)
