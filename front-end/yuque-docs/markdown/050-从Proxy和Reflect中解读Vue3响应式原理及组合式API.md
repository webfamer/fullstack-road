# 从Proxy和Reflect中解读Vue3响应式原理及组合式API

> 来源：https://www.yuque.com/xiumubai/doc/xzbropamg5rrgvoo

数据响应式
数据响应式是什么？
通过数据的改变去驱动 DOM 视图的变化。
Vue2与Vue3实现数据响应式有何区别？
Vue2响应式：通过Object.defineProperty来实现。对data对象的每个属性都劫持监听。
​99123456789101112131415161718192021222324252627282930313233343536data = {  name: '李四',  car: '路虎',  work: {    a: '1'  }}
observer(data);
function observer(data) {  if (typeof data !== 'object' || data == null) {    return;  }  // 如果是对象，则需要递归调用响应式函数  const keys = Object.keys(data);
  for (let i = 0; i < keys.length; i++) {    let key = keys[i];    let value = obj[key];    reactive(obj, key, value);  }}
// `Object.defineProperty()` 是 Vue2 的核心// Vue2 在初始化时会对数据进行劫持，如果劫持的属性还是对象的话需要递归劫持。// 响应式函数function reactive(obj, key, value) {  observer(value);
  Object.defineProperty(obj, key, {    get() {      return value;    },    set(newValue) {      if (newValue === value) return;💥通过Object.defineProperty来实现响应式有何缺点？
1从上面的代码中我们发现 Object.defineProperty() 是有缺陷的，当观察的数据嵌套非常深时，这样是非常耗费性能的。
2只对初始对象里的属性有劫持，当此对象新增某个属性或者移除某属性时，都是无响应式。故可通过Vue.set()或Vue.delete()解决此类问题。
3无法监听数组索引的直接赋值，无法监听修改数组的长度，故Vue2中通过修改数组的继承关系，重写数组方法的方式进行拦截调用。例如这些数组的方法push,pop,shift,unshift,splice,sort,reverse。
在Vue2中，通过arr[0]='newVal'这种根据数组索引值直接赋值的操作不会触发页面更新。这也并不是Object.defineProperty无法做到，而是因为考虑性能问题没有这么做。因为不确定数组的长度，对数组遍历进行劫持性能会损失很大。
Vue3响应式：使用ES6新增的Proxy(代理)实现。先看看使用Proxy代理的例子。
​9912345678910111213141516171819202122232425262728293031// 定义处理函数const handler = {  // get捕捉器-获取属性值  get (target, prop) {    console.log(`拦截了读取数据: 属性${prop}`)    return target  },  //  set捕捉器-修改属性值或者是添加属性  set (target, prop, value) {    target[prop] = value    console.log(`拦截了修改数据或者是添加属性: 属性${prop},属性值${value}`)    return target  },  //  deleteProperty捕捉器-删除某个属性  deleteProperty (target, prop) {    delete target[prop]    console.log(`拦截了删除数据: 属性${prop}`)    return target  }  //...一共13个配置项（捕捉器）}
// 使用Proxy,此时p就是代理后的对象了const p = new Proxy({}, handler);
// 验证修改/添加属性（会走到handler的set捕捉器方法）p.name = '李梅'// 验证读取属性（会走到handler的set捕捉器方法）p.name// 验证删除属性（会走到handler的deleteProperty捕捉器方法）delete p.name💥从上面例子可以看出Vue3使用Proxy代理实现响应式的优势：
1可以劫持整个对象（而不是仅对属性劫持），并返回一个新对象。Proxy在代码量上远远优于Object.defineProperty()的数据劫持操作。
2Proxy提供了13种劫持捕捉操作，可以更加精细化劫持捕捉操作，这是Object.defineProperty无法做到的。
Vue2与Vue3的兼容
因为Object.defineProperty兼容到IE8，所以Vue2一般可以兼容到IE8。而Proxy对IE11是不兼容的，故Vue3目前来看是不对IE11兼容的。
详解Proxy和Reflect
Proxy定义?
刚刚已经知道了Vue3是通过Proxy来实现数据响应式的，现在我们来看看它是如何使用的。
ES6新增的最明显的元编程特性之一就是Proxy(代理)特性。
简单来说，代理可以看作是对目标对象的“包装”，为目标对象架设一层拦截，外界对该对象的访问，都必须通过这层拦截。提供了像get,set,deleteProperty等13种捕捉器。
![](https://cdn.nlark.com/yuque/0/2024/webp/338969/1704288403334-4222072a-638b-42fe-84e9-29341f7e2508.webp)
Proxy使用?
语法：
参数：
●target
●要使用 Proxy 包装的目标对象（可以是任何类型的对象，包括原生数组，函数，甚至另一个代理）。
●handler
●代理配置：带有“捕捉器”（“traps”，即拦截操作的方法）的对象。比如 get 捕捉器方法用于读取 target 的属性，set 捕捉器方法用于写入 target 的属性，等等。
上面例子🌰由于没有捕捉器(空的 handler 对象)，所有对 proxy 的操作都直接转发给了 target。
1写入操作 proxy.test 会将值写入 target。
2读取操作 proxy.test 会从 target 返回对应的值。
3迭代 proxy 会从 target 返回对应的值。
我们可以看到，没有任何捕捉器，proxy 是一个 target 的透明包装器（wrapper）。
![](https://cdn.nlark.com/yuque/0/2024/webp/338969/1704288403282-fbe9ede3-ce55-481f-97a2-cb053d1a9397.webp)
当然可以添加捕捉器（13个）以此进行拦截，扩展激活出proxy更多的功能。
首先，对于对象的大多数操作，JavaScript 规范中有一个所谓的“内部方法”，它描述了最底层的工作方式。例如 [[Get]]，用于读取属性的内部方法，[[Set]]，用于写入属性的内部方法，等等。这些方法仅在规范中使用，我们不能直接通过方法名调用它们。
Proxy 捕捉器会拦截这些方法的调用。对于每个内部方法，表中都有一个捕捉器：捕捉器可用于添加到 new Proxy 的 handler 参数中以拦截对象内部方法的使用：
![](https://cdn.nlark.com/yuque/0/2024/webp/338969/1704288403282-a5c04acc-9882-4611-9406-5553ec47c99e.webp)
[可以点击MDN看看这13种捕捉器它们如何/何时触发。](https://link.juejin.cn/?target=https%3A%2F%2Fdeveloper.mozilla.org%2Fzh-CN%2Fdocs%2FWeb%2FJavaScript%2FReference%2FGlobal_Objects%2FProxy)
💥为什么要使用Proxy?
1代理成为了代码交互的主要对象，而实际目标对象保持隐藏/被保护的状态。
2可以拦截（并覆盖）对象的几乎所有行为，这意味着可以以强有力的方式扩展对象特性超出JavaScript内容。
3降低函数或类的复杂度
![](https://cdn.nlark.com/yuque/0/2024/webp/338969/1704288403502-bae72d5a-1eb8-45c2-bd79-79ef98a89c9b.webp)
Reflect的定义
Reflect称为反射。它也是ES6中为了操作对象而提供的新的API，用来替代直接调用Object的方法。
Reflect是一个内置的对象，它提供拦截 JavaScript 操作的方法。
前面所讲过对象的一些内部方法，例如 [[Get]] 和 [[Set]] 等，都只是规范性的，不能直接调用。
Reflect 对象使调用这些内部方法成为了可能。它的方法是内部方法的最小包装。
以下是执行相同操作和 Reflect 调用的示例：
![](https://cdn.nlark.com/yuque/0/2024/webp/338969/1704288403324-70c6c6b2-3bfe-47e1-965c-7aadedd1dbc0.webp)
例如，我们可以通过Reflect.set代替obj[prop] = value的操作：
所以，我们可以更方便使用 Reflect 来将操作转发给原始对象。这也是Reflect 的出现的原因之一：操作对象更为方便和语义化。
[可以点击去MDN看看Object和Reflect两者的对比](https://link.juejin.cn/?target=https%3A%2F%2Fdeveloper.mozilla.org%2Fen-US%2Fdocs%2FWeb%2FJavaScript%2FReference%2FGlobal_Objects%2FReflect%2FComparing_Reflect_and_Object_methods)
而Reflect使用在Proxy中的转发对象上也十分典型。对于每个可被 Proxy 捕获的内部方法，在 Reflect 中都有一个对应的方法，其名称和参数与 Proxy 捕捉器相同。 这一点很关键，13种捕获器可以与Reflect方法一一对应，简化 Proxy 的创建。这也是Reflect 的出现的原因之一：完美的与Proxy搭配使用。 看下面这个例子🌰：
💥总结Reflect的一些特点:
1不可构造，不能使用 new 进行调用
2所有方法和 Proxy handlers中的捕捉器相同(13个一一对应)
3提供的API比Object更为丰富且使用起来更为语义化
4所有的方法都是静态方法，类似于 Math。（静态方法是可以直接用类名.方法名去调用的；而实例方法是不可以的，必须要用实例才可以去调用）
5部分方法和 Object.* 相同，但行为略微有所区别。譬如 Object.defineProperty(obj, name, desc) 在无法定义属性时，会抛出一个错误，而 Reflect.defineProperty(obj, name, desc) 则会返回false。(见下例子🌰)
receiver参数具有不可替代性
让我们看一个例子🌰，来说明为什么 Reflect.get 更好。此外，我们还将看到为什么 get/set 有第三个参数 receiver，如何使用它。
读取 cat.name 应该返回 "猫"，而不是 "动物"！
发生了什么？或许我们在继承方面做错了什么？
但是，如果我们移除代理，那么一切都会按预期进行。
问题实际上出在代理中，在 (*) 行。
1当我们读取 cat.name 时，由于 cat 对象自身没有对应的的属性，搜索将转到其原型。
2原型是 animalProxy。
3从代理读取 name 属性时，get 捕捉器会被触发，并从原始对象返回 target[prop] 属性，在 (*) 行。
当调用 target[prop] 时，若 prop 是一个 getter，它将在 this=target 上下文中运行其代码。因此，结果是来自原始对象 target 的 this._name，即来自 animal。
为了解决这种情况，我们需要 get 捕捉器的第三个参数 receiver。它保证将正确的 this 传递给 getter。在我们的例子中是 cat。
如何把上下文传递给 getter？对于一个常规函数，我们可以使用 call/apply，但这是一个 getter，它不能“被调用”，只能被访问。
Reflect.get 可以做到。如果我们使用它，一切都会正常运行。
这是更正后的变体：
现在 receiver 保留了对正确 this 的引用（即 cat），该引用是在 (*) 行中被通过 Reflect.get 传递给 getter 的。
可以看出捕捉器的第三个参数 receiver具有不可替代性。
我们可以把捕捉器重写得更短：
Reflect 调用的命名与捕捉器的命名完全相同，并且接受相同的参数。它们是以这种方式专门设计的。
因此，return Reflect... 提供了一个安全的方式，可以轻松地转发操作，并确保我们不会忘记与此相关的任何内容。
Proxy和Reflect总是协同工作的
从上一节的最后一个例子🌰也可以看出Proxy和Reflect从设计之初就是完美搭配使用的。
💥现在总结下两者协同工作的原因：
1Reflect Api有13个静态函数，这与Proxy设计是一一对应的。如果Proxy一个捕捉器想要将调用转发给对象，则只需使用相同的参数调用 Reflect.<method> 就足够了。这种映射在设计之初就是有意对称的。
2Proxy get/set()方法需要的返回值正是Reflect的get/set方法的返回值，可以天然配合使用，比直接对象赋值/获取值要更方便和准确。
3receiver参数具有不可替代性。
Reflect和Proxy搭配使用实现响应式
现在将用Proxy + Reflect 搭配改造一下，实现数据响应式效果。
从上面的例子可以看出，如果我们不使用Reflect也可以达到相同的效果。但是考虑到以下几点，我们通常选择了Proxy + Reflect API搭配使用:
1只要是Proxy对象具有的代理方法，Reflect对象全部都与之对应，。故无论Proxy怎么修改默认行为，总是可以通过Reflect对应的方法获取默认行为。
2使用Reflect API修改行为不会报错，使用起来更为合理。例如上面所提到的Object.defineProperty(obj, name, desc)和Reflect.defineProperty(obj, name, desc)。
3Reflect提供这种静态方法调用，更加的具有语义化。
Vue3组合式API实现原理
前言
Vue3引入了新特性——组合式API。其中一些响应性的API就是通过Proxy+Reflect实现的。列出一部分的响应性的API看看具体是如何实现的。
[API的具体作用和功能可以去官网看看，这里不再叙述，只针对其内部的实现进行说明。](https://link.juejin.cn/?target=https%3A%2F%2Fv3.cn.vuejs.org%2Fapi%2Fbasic-reactivity.html)
![](https://cdn.nlark.com/yuque/0/2024/webp/338969/1704288403731-218e31f2-7823-43ad-b22a-88e6f24e6246.webp)
原理
响应性API的实现原理
●通过Proxy（代理）：拦截对象中任意属性的变化，包括：属性值的读写、属性的添加、属性的删除等。
●通过Reflect（反射）：对被代理对象的属性进行操作。
实现
我们这里只是实现数据响应式简单的逻辑编排，并没有实现其中DOM变化。
1. shallowReactive和reactive
首先看第一对shallowReactive和reactive。
需要说明的就是两点：
1调用shallowReactive(obj)会返回一个代理后的对象，所以shallowReactive函数应该返回一个proxy：new Proxy(target, reactiveHandler)。
2调用reactive(obj)会返回一个深层次的代理对象，所以在shallowReactive函数实现的基础上递归去判断其值是否是对象类型，如果是，就需要递归执行new Proxy(target, reactiveHandler)这一操作。让对象的每一层都返回一个响应式的代理对象，这样自然就会返回一个深层次的代理对象。
这样就简单实现了shallowReactive和reactive函数对读/写/删除操作的响应式了。其中可以单独抽取reactiveHandler处理函数，供shallowReactive和reactive函数使用。
✅现在使用下自己写的shallowReactive和reactive函数，看是否是预期效果。
[你也可以点击去codepen工作台去验证下shallowReactive和reactive函数实现](https://link.juejin.cn/?target=https%3A%2F%2Fcodepen.io%2FFengmaybe%2Fpen%2FgOXqGPQ)
2. shallowReadonly和readonly
再来看看shallowReadonly和readonly实现
shallowReadonly和readonly这两个函数的几乎与shallowReactive和reactive函数实现一致。
只有在处理函数(handler)中有点区别。readonly代表只读，故只会在get中执行Reflect.get(target, prop)，在其他的地方并不操作对象的行为，只返回一个Boolean值。这便实现了对代理对象中的属性只可读，不能进行修改/添加/删除等操作。
✅小小验证下shallowReadonly和readonly函数是否达到了预期效果。
[你也可以点击去codepen工作台去验证下shallowReadonly和readonly函数实现](https://link.juejin.cn/?target=https%3A%2F%2Fcodepen.io%2FFengmaybe%2Fpen%2FBamMxZr)
3. shallowRef和ref
再来看看shallowRef和ref实现
shallowRef和ref和上面两个例子又有所不同，它返回的响应式代理对象仅有一个 .value property，指向赋值进来的目标对象。
故shallowRef函数和ref函数设计时是需要返回一个对象，这个对象有get/set的访问器属性，当读取对象属性时会走到get方法中，当修改属性时会走到set方法中。
✅验证一下shallowRef和ref响应式的实现。
[你也可以点击去codepen工作台去验证下shallowRef和ref函数实现](https://link.juejin.cn/?target=https%3A%2F%2Fcodepen.io%2FFengmaybe%2Fpen%2FBamMVav)
4. isRef/isReactive/isReadonly/isProxy
看看isRef/isReactive/isReadonly/isProxy函数如何设计
其实很简单，这几个函数返回一个Boolean值，这时只需要设计一个属性，这个属性挂在生成其代理对象的处理函数中即可。
📍新增_is_ref属性要挂载到ref函数中的返回对象里
📍新增_is_reactive属性要挂载到reactive函数中的处理函数
📍新增_is_readonly属性要挂载到readonly函数中的处理函数
✅简单验证下
[你也可以点击去codepen工作台去验证下isRef/isReactive/isReadonly/isProxy函数实现](https://link.juejin.cn/?target=https%3A%2F%2Fcodepen.io%2FFengmaybe%2Fpen%2FLYOqBxa)
Composition API VS Option API
上一节我们梳理了Vue3中通过Proxy来实现组合式API（Composition API）的实现原理。那么我们来看看为何选择抛弃Vue2的选项API（Option API）。
Option API的问题
在传统的Vue Options API中，新增或者修改一个需求，就需要分别在data，methods，computed里修改 ，滚动条反复上下移动。
![](https://cdn.nlark.com/yuque/0/2024/gif/338969/1704288403770-5a9fe96b-7ee0-4492-8622-128857671642.gif)![](https://cdn.nlark.com/yuque/0/2024/webp/338969/1704288403790-228090a1-0dbd-4719-b544-8088125bdf3d.webp)
使用Compisition API
我们可以更加优雅的组织我们的代码，函数。让相关功能的代码更加有序的组织在一起。
当我们需要在原有页面新增一个功能时，Compisition API可以让我们的新增功能这块代码尽可能不分散，有序在一块上，从而更好实现“功能代码块”的概念，方便维护。
![](https://cdn.nlark.com/yuque/0/2024/webp/338969/1704288403893-de241cc0-4761-4e28-81a9-7d683624e241.webp)![](https://cdn.nlark.com/yuque/0/2024/webp/338969/1704288403872-65a87750-86b0-47aa-8ff3-f9e64918c17c.webp)![](https://cdn.nlark.com/yuque/0/2024/webp/338969/1704288404127-4de082ea-607c-4abc-ace7-c5a825519758.webp)
