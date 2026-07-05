# Vue虚拟dom

> 来源：https://www.yuque.com/xiumubai/doc/pzc3z0svwccfblls

面试官：什么是虚拟DOM？如何实现一个虚拟DOM？说说你的思路
一、什么是虚拟DOM

虚拟 DOM （Virtual DOM ）这个概念相信大家都不陌生，从 React 到 Vue ，虚拟 DOM 为这两个框架都带来了跨平台的能力（React-Native 和 Weex）

实际上它只是一层对真实DOM的抽象，以JavaScript 对象 (VNode 节点) 作为基础的树，用对象的属性来描述节点，最终可以通过一系列操作使这棵树映射到真实环境上

在Javascript对象中，虚拟DOM 表现为一个 Object对象。并且最少包含标签名 (tag)、属性 (attrs) 和子元素对象 (children) 三个属性，不同框架对这三个属性的名命可能会有差别

创建虚拟DOM就是为了更好将虚拟的节点渲染到页面视图中，所以虚拟DOM对象的节点与真实DOM的属性一一照应

在vue中同样使用到了虚拟DOM技术

定义真实DOM

​91234<div id="app">    <p class="p">节点内容</p>    <h3>{{ foo }}</h3></div>
实例化vue

​9123456const app = new Vue({    el:"#app",    data:{        foo:"foo"    }})
观察render的render，我们能得到虚拟DOM

​91234(function anonymous() {	with(this){return _c('div',{attrs:{"id":"app"}},[_c('p',{staticClass:"p"},					  [_v("节点内容")]),_v(" "),_c('h3',[_v(_s(foo))])])}})
通过VNode，vue可以对这颗抽象树进行创建节点,删除节点以及修改节点的操作， 经过diff算法得出一些需要修改的最小单位,再更新视图，减少了dom操作，提高了性能

二、为什么需要虚拟DOM

DOM是很慢的，其元素非常庞大，页面的性能问题，大部分都是由DOM操作引起的

真实的DOM节点，哪怕一个最简单的div也包含着很多属性，可以打印出来直观感受一下：
![](/api/filetransfer/images?url=https%3A%2F%2Fstatic.vue-js.com%2Fcc95c7f0-442c-11eb-ab90-d9ae814b240d.png&sign=12e3a6ac695aee120627e18213a339f5d0ba6dd2e8b785143a1098bb0e026fef)

由此可见，操作DOM的代价仍旧是昂贵的，频繁操作还是会出现页面卡顿，影响用户的体验

举个例子：

你用传统的原生api或jQuery去操作DOM时，浏览器会从构建DOM树开始从头到尾执行一遍流程

当你在一次操作时，需要更新10个DOM节点，浏览器没这么智能，收到第一个更新DOM请求后，并不知道后续还有9次更新操作，因此会马上执行流程，最终执行10次流程

而通过VNode，同样更新10个DOM节点，虚拟DOM不会立即操作DOM，而是将这10次更新的diff内容保存到本地的一个js对象中，最终将这个js对象一次性attach到DOM树上，避免大量的无谓计算

很多人认为虚拟 DOM 最大的优势是 diff 算法，减少 JavaScript 操作真实 DOM 的带来的性能消耗。虽然这一个虚拟 DOM 带来的一个优势，但并不是全部。虚拟 DOM 最大的优势在于抽象了原本的渲染过程，实现了跨平台的能力，而不仅仅局限于浏览器的 DOM，可以是安卓和 IOS 的原生组件，可以是近期很火热的小程序，也可以是各种GUI

三、如何实现虚拟DOM

首先可以看看vue中VNode的结构

源码位置：src/core/vdom/vnode.js

这里对VNode进行稍微的说明：

●所有对象的 context 选项都指向了 Vue 实例
●elm 属性则指向了其相对应的真实 DOM 节点

vue是通过createElement生成VNode

源码位置：src/core/vdom/create-element.js

上面可以看到createElement 方法实际上是对 _createElement 方法的封装，对参数的传入进行了判断

可以看到_createElement接收5个参数：

● context 表示 VNode 的上下文环境，是 Component 类型
● tag 表示标签，它可以是一个字符串，也可以是一个 Component
● data 表示 VNode 的数据，它是一个 VNodeData 类型
● children 表示当前 VNode的子节点，它是任意类型的
● normalizationType 表示子节点规范的类型，类型不同规范的方法也就不一样，主要是参考 render 函数是编译生成的还是用户手写的

根据normalizationType 的类型，children会有不同的定义

simpleNormalizeChildren方法调用场景是 render 函数是编译生成的

normalizeChildren方法调用场景分为下面两种：

●render 函数是用户手写的
●编译 slot、v-for 的时候会产生嵌套数组

无论是simpleNormalizeChildren还是normalizeChildren都是对children进行规范（使children 变成了一个类型为 VNode 的 Array），这里就不展开说了

规范化children的源码位置在：src/core/vdom/helpers/normalzie-children.js

在规范化children后，就去创建VNode

​9912345678910111213141516171819202122232425let vnode, ns// 对tag进行判断if (typeof tag === 'string') {  let Ctor  ns = (context.$vnode && context.$vnode.ns) || config.getTagNamespace(tag)  if (config.isReservedTag(tag)) {    // 如果是内置的节点，则直接创建一个普通VNode    vnode = new VNode(      config.parsePlatformTagName(tag), data, children,      undefined, undefined, context    )  } else if (isDef(Ctor = resolveAsset(context.$options, 'components', tag))) {    // component    // 如果是component类型，则会通过createComponent创建VNode节点    vnode = createComponent(Ctor, data, context, children, tag)  } else {    vnode = new VNode(      tag, data, children,      undefined, undefined, context    )  }} else {  // direct component options / constructor  vnode = createComponent(tag, data, context, children)}
createComponent同样是创建VNode

源码位置：src/core/vdom/create-component.js

​JavaScriptRun CodeCopy99123456789101112131415161718192021222324252627282930313233343536export function createComponent (  Ctor: Class<Component> | Function | Object | void,  data: ?VNodeData,  context: Component,  children: ?Array<VNode>,  tag?: string): VNode | Array<VNode> | void {  if (isUndef(Ctor)) {    return  } // 构建子类构造函数   const baseCtor = context.$options._base
  // plain options object: turn it into a constructor  if (isObject(Ctor)) {    Ctor = baseCtor.extend(Ctor)  }
  // if at this stage it's not a constructor or an async component factory,  // reject.  if (typeof Ctor !== 'function') {    if (process.env.NODE_ENV !== 'production') {      warn(`Invalid Component definition: ${String(Ctor)}`, context)    }    return  }
  // async component  let asyncFactory  if (isUndef(Ctor.cid)) {    asyncFactory = Ctor    Ctor = resolveAsyncComponent(asyncFactory, baseCtor, context)    if (Ctor === undefined) {      return createAsyncPlaceholder(        asyncFactory,        data,
稍微提下createComponent生成VNode的三个关键流程：

●构造子类构造函数Ctor
●installComponentHooks安装组件钩子函数
●实例化 vnode

小结

createElement 创建 VNode 的过程，每个 VNode 有 children，children 每个元素也是一个VNode，这样就形成了一个虚拟树结构，用于描述真实的DOM树结构

参考文献

●[https://ustbhuangyi.github.io/vue-analysis/v2/data-driven/create-element.html#children-的规范化](https://ustbhuangyi.github.io/vue-analysis/v2/data-driven/create-element.html#children-%E7%9A%84%E8%A7%84%E8%8C%83%E5%8C%96)
●[https://juejin.cn/post/6876711874050818061](https://juejin.cn/post/6876711874050818061)
