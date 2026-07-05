# Vue3如何做treeshaking的

> 来源：https://www.yuque.com/xiumubai/doc/md7m9lzentntafox

面试官：说说Vue 3.0中Treeshaking特性？举例说明一下？
一、是什么

Tree shaking 是一种通过清除多余代码方式来优化项目打包体积的技术，专业术语叫 Dead code elimination

简单来讲，就是在保持代码运行结果不变的前提下，去除无用的代码

如果把代码打包比作制作蛋糕，传统的方式是把鸡蛋（带壳）全部丢进去搅拌，然后放入烤箱，最后把（没有用的）蛋壳全部挑选并剔除出去

而treeshaking则是一开始就把有用的蛋白蛋黄（import）放入搅拌，最后直接作出蛋糕

也就是说 ，tree shaking 其实是找出使用的代码

在Vue2中，无论我们使用什么功能，它们最终都会出现在生产代码中。主要原因是Vue实例在项目中是单例的，捆绑程序无法检测到该对象的哪些属性在代码中被使用到

​9123import Vue from 'vue' Vue.nextTick(() => {})
而Vue3源码引入tree shaking特性，将全局 API 进行分块。如果您不使用其某些功能，它们将不会包含在您的基础包中

​9123import { nextTick, observable } from 'vue' nextTick(() => {})
二、如何做

Tree shaking是基于ES6模板语法（import与exports），主要是借助ES6模块的静态编译思想，在编译时就能确定模块的依赖关系，以及输入和输出的变量

Tree shaking无非就是做了两件事：

●编译阶段利用ES6 Module判断哪些模块已经加载
●判断那些模块和变量未被使用或者引用，进而删除对应代码

下面就来举个例子：

通过脚手架vue-cli安装Vue2与Vue3项目

​91vue create vue-demo
Vue2 项目

组件中使用data属性

对项目进行打包，体积如下图

![](/api/filetransfer/images?url=https%3A%2F%2Fstatic.vue-js.com%2F6bd2aff0-6097-11eb-85f6-6fac77c0c9b3.png&sign=314014da6d0ad64e95a4b84a7859b102aa00e49fcae258163ed5503e7f8924e2)

为组件设置其他属性（compted、watch）

再一次打包，发现打包出来的体积并没有变化

![](/api/filetransfer/images?url=https%3A%2F%2Fstatic.vue-js.com%2F7c29e260-6097-11eb-ab90-d9ae814b240d.png&sign=7431a5d0f94c19efdf4dfe93410cf8543df7f98342409600d4cbce39ee2ea62a)

Vue3 项目

组件中简单使用

​991234567891011import { reactive, defineComponent } from "vue";export default defineComponent({  setup() {    const state = reactive({      count: 1,    });    return {      state,    };  },});
将项目进行打包

![](/api/filetransfer/images?url=https%3A%2F%2Fstatic.vue-js.com%2F95df0000-6097-11eb-85f6-6fac77c0c9b3.png&sign=819a54080b2bbf01ba64254b87da865a46711eaeea96a27568cc25ac5e7c3c32)

在组件中引入computed和watch

​JavaScriptRun CodeCopy991234567891011121314151617181920212223import { reactive, defineComponent, computed, watch } from "vue";export default defineComponent({  setup() {    const state = reactive({      count: 1,    });    const double = computed(() => {      return state.count * 2;    });
    watch(      () => state.count,      (count, preCount) => {        console.log(count);        console.log(preCount);      }    );    return {      state,      double,    };  },});
再次对项目进行打包，可以看到在引入computer和watch之后，项目整体体积变大了

![](/api/filetransfer/images?url=https%3A%2F%2Fstatic.vue-js.com%2Fb36a7a00-6097-11eb-85f6-6fac77c0c9b3.png&sign=319f99e16eaf8f68d5bc625dc62ef4012c94cd9fda77431342baa718b4e5c458)

三、作用

通过Tree shaking，Vue3给我们带来的好处是：

●减少程序体积（更小）
●减少程序执行时间（更快）
●便于将来对程序架构进行优化（更友好）

参考文献

●[https://segmentfault.com/a/1190000038962700](https://segmentfault.com/a/1190000038962700)
