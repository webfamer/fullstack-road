# Vue中的keep-alive

> 来源：https://www.yuque.com/xiumubai/doc/ginywdgnco26y61n

面试官：说说你对keep-alive的理解是什么？
一、Keep-alive 是什么

keep-alive是vue中的内置组件，能在组件切换过程中将状态保留在内存中，防止重复渲染DOM

keep-alive 包裹动态组件时，会缓存不活动的组件实例，而不是销毁它们

keep-alive可以设置以下props属性：

● include - 字符串或正则表达式。只有名称匹配的组件会被缓存
● exclude - 字符串或正则表达式。任何名称匹配的组件都不会被缓存
● max - 数字。最多可以缓存多少组件实例

关于keep-alive的基本用法：

​9123<keep-alive>  <component :is="view"></component></keep-alive>
使用includes和exclude：

​9912345678910111213<keep-alive include="a,b">  <component :is="view"></component></keep-alive>
<!-- 正则表达式 (使用 `v-bind`) --><keep-alive :include="/a|b/">  <component :is="view"></component></keep-alive>
<!-- 数组 (使用 `v-bind`) --><keep-alive :include="['a', 'b']">  <component :is="view"></component></keep-alive>
匹配首先检查组件自身的 name 选项，如果 name 选项不可用，则匹配它的局部注册名称 (父组件 components 选项的键值)，匿名组件不能被匹配

设置了 keep-alive 缓存的组件，会多出两个生命周期钩子（activated与deactivated）：

● 首次进入组件时：beforeRouteEnter > beforeCreate > created> mounted > activated > ... ... > beforeRouteLeave > deactivated
● 再次进入组件时：beforeRouteEnter >activated > ... ... > beforeRouteLeave > deactivated

二、使用场景

使用原则：当我们在某些场景下不需要让页面重新加载时我们可以使用keepalive

举个栗子:

当我们从首页–>列表页–>商详页–>再返回，这时候列表页应该是需要keep-alive

从首页–>列表页–>商详页–>返回到列表页(需要缓存)–>返回到首页(需要缓存)–>再次进入列表页(不需要缓存)，这时候可以按需来控制页面的keep-alive

在路由中设置keepAlive属性判断是否需要缓存

​991234567891011{  path: 'list',  name: 'itemList', // 列表页  component (resolve) {    require(['@/pages/item/list'], resolve) }, meta: {  keepAlive: true,  title: '列表页' }}
使用<keep-alive>

三、原理分析

keep-alive是vue中内置的一个组件

源码位置：src/core/components/keep-alive.js

可以看到该组件没有template，而是用了render，在组件渲染的时候会自动执行render函数

this.cache是一个对象，用来存储需要缓存的组件，它将以如下形式存储：

在组件销毁的时候执行pruneCacheEntry函数

在mounted钩子函数中观测 include 和 exclude 的变化，如下：

如果include 或exclude 发生了变化，即表示定义需要缓存的组件的规则或者不需要缓存的组件的规则发生了变化，那么就执行pruneCache函数，函数如下：

在该函数内对this.cache对象进行遍历，取出每一项的name值，用其与新的缓存规则进行匹配，如果匹配不上，则表示在新的缓存规则下该组件已经不需要被缓存，则调用pruneCacheEntry函数将其从this.cache对象剔除即可

关于keep-alive的最强大缓存功能是在render函数中实现

首先获取组件的key值：

拿到key值后去this.cache对象中去寻找是否有该值，如果有则表示该组件有缓存，即命中缓存，如下：

直接从缓存中拿 vnode 的组件实例，此时重新调整该组件key的顺序，将其从原来的地方删掉并重新放在this.keys中最后一个

this.cache对象中没有该key值的情况，如下：

表明该组件还没有被缓存过，则以该组件的key为键，组件vnode为值，将其存入this.cache中，并且把key存入this.keys中

此时再判断this.keys中缓存组件的数量是否超过了设置的最大缓存数量值this.max，如果超过了，则把第一个缓存组件删掉

四、思考题：缓存后如何获取数据

解决方案可以有以下两种：

● beforeRouteEnter
● actived

beforeRouteEnter

每次组件渲染的时候，都会执行beforeRouteEnter

​GoRun CodeCopy91234567beforeRouteEnter(to, from, next){    next(vm=>{        console.log(vm)        // 每次进入路由执行        vm.getData()  // 获取数据    })},
actived

在keep-alive缓存的组件被激活的时候，都会执行actived钩子

​GoRun CodeCopy9123activated(){   this.getData() // 获取数据},
注意：服务器端渲染期间avtived不被调用

参考文献

●[https://www.cnblogs.com/dhui/p/13589401.html](https://www.cnblogs.com/dhui/p/13589401.html)
●[https://www.cnblogs.com/wangjiachen666/p/11497200.html](https://www.cnblogs.com/wangjiachen666/p/11497200.html)
●[https://vue3js.cn/docs/zh](https://vue3js.cn/docs/zh)
