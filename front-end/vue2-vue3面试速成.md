# Vue2 / Vue3 面试详解版

> 读者定位：你主要写 React，也写过 Vue2，但 Vue3 没怎么写过。  
> 目标：用一份文档快速建立 Vue3 心智模型，能写基础 Vue3 代码，也能回答常见 Vue / Vue3 / 后台系统面试题。  
> 复习策略：不要把 Vue 当成“另一个 React”。Vue 的核心是响应式依赖追踪 + 模板编译；React 的核心是状态变更触发组件函数重新执行。

## 0. 先建立心智模型

### 0.1 React 和 Vue 最大区别

React 的典型模型：

```text
state 更新
  -> 组件函数重新执行
  -> 得到新的 JSX
  -> React diff
  -> 更新 DOM
```

Vue 的典型模型：

```text
响应式数据被读取
  -> Vue 收集依赖
响应式数据被修改
  -> 触发依赖更新
  -> 重新渲染受影响组件
```

所以你从 React 切到 Vue3，最重要的是接受这个区别：

- React 中，组件函数每次 render 都会重新执行，依赖关系主要靠 Hooks 数组、memo、callback 管。
- Vue 中，响应式对象的读取和写入会被追踪，`computed`、`watch`、模板渲染都会自动收集依赖。

### 0.2 React Hooks 和 Vue Composition API 对照

| React | Vue3 |
| --- | --- |
| `useState` | `ref` / `reactive` |
| `useMemo` | `computed` |
| `useEffect` | `watch` / `watchEffect` / 生命周期 hook |
| `useRef` 保存 DOM | `ref` 模板引用 |
| 自定义 Hook | composable：`useXxx()` |
| Context | `provide / inject` |
| Redux / Zustand | Pinia |
| JSX | template，也可 JSX |

注意：它们不是完全等价。React Hooks 是在渲染过程中运行的函数机制；Vue Composition API 是建立响应式依赖图的组织方式。

## 1. Vue2 和 Vue3 核心差异

### 1.1 响应式原理：`Object.defineProperty` vs `Proxy`

Vue2 使用 `Object.defineProperty` 劫持对象属性的 getter / setter。

```js
function defineReactive(obj, key, value) {
  Object.defineProperty(obj, key, {
    get() {
      console.log('track', key)
      return value
    },
    set(newValue) {
      console.log('trigger', key)
      value = newValue
    },
  })
}

const state = {}
defineReactive(state, 'count', 1)
state.count
state.count = 2
```

Vue2 的限制：

- 初始化时不存在的属性，后续新增默认不是响应式。
- 删除属性无法天然触发更新。
- 数组索引赋值、直接改 `length` 有限制。

Vue2 常见补救：

```js
// 对象新增属性
this.$set(this.user, 'age', 18)

// 数组改某一项
this.list.splice(index, 1, newItem)
```

Vue3 使用 `Proxy` 代理整个对象。

```js
const state = new Proxy({ count: 1 }, {
  get(target, key) {
    console.log('track', key)
    return target[key]
  },
  set(target, key, value) {
    console.log('trigger', key)
    target[key] = value
    return true
  },
})

state.count
state.count = 2
state.name = 'Vue3'
delete state.name
```

Vue3 优势：

- 能监听新增属性。
- 能监听删除属性。
- 对数组支持更完整。
- 能拦截 `in`、遍历等操作。

面试回答：

```text
Vue2 的响应式基于 Object.defineProperty，它需要对已有属性逐个劫持，所以对象新增、删除属性以及部分数组操作需要 Vue.set 或 splice 兜底。Vue3 改成 Proxy，代理的是整个对象，可以拦截读取、写入、新增、删除、遍历等操作，响应式覆盖更完整，也让 Composition API 的组织方式更自然。
```

### 1.2 Options API vs Composition API

Vue2 常见 Options API：

```vue
<template>
  <div>
    <input v-model="keyword" />
    <p>结果：{{ filteredList.length }}</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      keyword: '',
      list: ['React', 'Vue2', 'Vue3'],
    }
  },
  computed: {
    filteredList() {
      return this.list.filter(item => item.includes(this.keyword))
    },
  },
  watch: {
    keyword(value) {
      console.log('keyword changed', value)
    },
  },
  methods: {
    reset() {
      this.keyword = ''
    },
  },
}
</script>
```

Vue3 Composition API：

```vue
<template>
  <div>
    <input v-model="keyword" />
    <p>结果：{{ filteredList.length }}</p>
    <button @click="reset">重置</button>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'

const keyword = ref('')
const list = ref(['React', 'Vue2', 'Vue3'])

const filteredList = computed(() =>
  list.value.filter(item => item.includes(keyword.value)),
)

watch(keyword, value => {
  console.log('keyword changed', value)
})

function reset() {
  keyword.value = ''
}
</script>
```

区别：

- Options API 按选项组织：`data`、`methods`、`computed`、`watch`。
- Composition API 按业务功能组织：一个功能相关的状态、计算、监听、方法可以放在一起。
- 复杂组件里 Composition API 更适合抽成 `useXxx()`。
- Vue3 仍然支持 Options API，不是强制只能写 Composition API。

面试回答：

```text
Options API 适合简单组件，因为结构固定、上手快。但复杂业务里，同一个功能的状态、方法、watch、computed 会散落在不同选项里。Composition API 更像按功能组织代码，可以把表格、权限、图表、搜索这些逻辑抽成 useTable、usePermission、useChart 等组合式函数，也更适合 TypeScript 类型推导和逻辑复用。
```

### 1.3 Vue2 / Vue3 生命周期对应

| Vue2 | Vue3 |
| --- | --- |
| `beforeCreate` / `created` | `setup()` |
| `beforeMount` | `onBeforeMount` |
| `mounted` | `onMounted` |
| `beforeUpdate` | `onBeforeUpdate` |
| `updated` | `onUpdated` |
| `beforeDestroy` | `onBeforeUnmount` |
| `destroyed` | `onUnmounted` |
| `activated` | `onActivated` |
| `deactivated` | `onDeactivated` |

Vue3 示例：

```vue
<script setup lang="ts">
import { onMounted, onUnmounted } from 'vue'

let timer: number | undefined

onMounted(() => {
  timer = window.setInterval(() => {
    console.log('polling')
  }, 1000)
})

onUnmounted(() => {
  if (timer) window.clearInterval(timer)
})
</script>
```

注意：

- `setup()` 执行时没有 `this`。
- 不要在 `setup()` 里写 `this.xxx`。
- 需要路由、store、props、emit，都通过函数或宏获取。

### 1.4 Vue3 的 `<script setup>`

`<script setup>` 是 Vue3 单文件组件里的编译期语法糖。它让 Composition API 更简洁。

普通 `setup`：

```vue
<script lang="ts">
import { defineComponent, ref } from 'vue'

export default defineComponent({
  setup() {
    const count = ref(0)
    const add = () => count.value++

    return {
      count,
      add,
    }
  },
})
</script>
```

`<script setup>`：

```vue
<script setup lang="ts">
import { ref } from 'vue'

const count = ref(0)
const add = () => count.value++
</script>

<template>
  <button @click="add">{{ count }}</button>
</template>
```

优势：

- 顶层变量和函数可以直接在模板里使用。
- 不需要手写 `return`。
- `defineProps`、`defineEmits`、`defineExpose` 等宏直接可用。
- TypeScript 推导更自然。

官方补充点：

- `<script setup>` 是编译期语法糖。
- `defineProps` / `defineEmits` 是编译器宏，不需要 import。
- Vue 3.5 之后，`defineProps` 解构出的变量在同一个 `<script setup>` 中仍具备响应式能力；但面试中更稳的写法仍然是不要随意解构 props，或者使用 `toRefs` / 直接 `props.xxx`。

## 2. Vue3 响应式 API

### 2.1 `ref`

`ref` 适合基础类型，也可以包对象。

```vue
<script setup lang="ts">
import { ref } from 'vue'

const count = ref(0)

function add() {
  count.value++
}
</script>

<template>
  <button @click="add">{{ count }}</button>
</template>
```

注意：

- 在 JS / TS 里访问要 `.value`。
- 在模板里会自动解包，不用写 `.value`。

React 类比：

```text
React useState:
const [count, setCount] = useState(0)
setCount(count + 1)

Vue ref:
const count = ref(0)
count.value++
```

### 2.2 `reactive`

`reactive` 适合对象和数组。

```vue
<script setup lang="ts">
import { reactive } from 'vue'

const form = reactive({
  username: '',
  password: '',
})

function submit() {
  console.log(form.username, form.password)
}
</script>

<template>
  <input v-model="form.username" />
  <input v-model="form.password" type="password" />
  <button @click="submit">提交</button>
</template>
```

常见坑：直接解构 `reactive` 会丢响应式。

```ts
const form = reactive({ username: 'xsz' })

// 不推荐：username 变成普通变量
const { username } = form
```

正确写法：

```ts
import { toRefs } from 'vue'

const form = reactive({ username: 'xsz' })
const { username } = toRefs(form)
```

面试回答：

```text
ref 更适合基础类型，reactive 更适合对象。ref 在脚本里要通过 .value 访问，模板里会自动解包。reactive 直接访问属性，但直接解构会丢响应式，需要 toRefs。实际项目里，简单独立状态我用 ref，表单或一组相关状态我用 reactive。
```

### 2.3 `computed`

`computed` 适合派生状态，有缓存。

```vue
<script setup lang="ts">
import { computed, ref } from 'vue'

const price = ref(100)
const count = ref(2)

const total = computed(() => price.value * count.value)
</script>

<template>
  <div>总价：{{ total }}</div>
</template>
```

可写 computed：

```ts
const firstName = ref('San')
const lastName = ref('Zhang')

const fullName = computed({
  get() {
    return `${firstName.value} ${lastName.value}`
  },
  set(value: string) {
    const [first, last] = value.split(' ')
    firstName.value = first
    lastName.value = last
  },
})
```

面试回答：

```text
computed 适合从已有响应式状态推导出新值，并且有缓存，依赖不变不会重新计算。比如根据表格数据计算汇总值、根据权限和状态计算按钮是否禁用，都适合 computed。
```

### 2.4 `watch`

`watch` 适合监听明确数据源，做副作用。

```vue
<script setup lang="ts">
import { ref, watch } from 'vue'

const keyword = ref('')
const loading = ref(false)
const list = ref<string[]>([])

watch(keyword, async value => {
  loading.value = true
  try {
    list.value = await searchApi(value)
  } finally {
    loading.value = false
  }
})

async function searchApi(value: string) {
  return [`result: ${value}`]
}
</script>
```

常用配置：

```ts
watch(
  () => form.status,
  (newValue, oldValue) => {
    console.log(newValue, oldValue)
  },
  {
    immediate: true,
    deep: false,
    flush: 'post',
  },
)
```

说明：

- `immediate`：初始化时立即执行。
- `deep`：深度监听对象，谨慎使用，可能有性能成本。
- `flush: 'post'`：DOM 更新后再执行回调。

### 2.5 `watchEffect`

`watchEffect` 会自动收集回调里用到的响应式依赖，并立即执行。

```ts
const page = ref(1)
const pageSize = ref(20)

watchEffect(() => {
  console.log('fetch list', page.value, pageSize.value)
})
```

`watch` vs `watchEffect`：

```text
watch：明确监听谁，可以拿新旧值，适合精确控制。
watchEffect：自动收集依赖，立即执行，适合简单副作用。
```

面试回答：

```text
watch 更适合明确监听某个字段，比如筛选条件变化后请求接口，可以拿到新旧值，也能控制 immediate、deep。watchEffect 会自动收集依赖，适合依赖简单的副作用，但复杂业务里我更倾向 watch，因为可读性和可控性更强。
```

### 2.6 `nextTick`

Vue 修改响应式数据后，DOM 更新不是同步立刻完成，而是异步批处理。

```vue
<script setup lang="ts">
import { nextTick, ref } from 'vue'

const visible = ref(false)
const inputRef = ref<HTMLInputElement | null>(null)

async function open() {
  visible.value = true
  await nextTick()
  inputRef.value?.focus()
}
</script>

<template>
  <button @click="open">打开</button>
  <input v-if="visible" ref="inputRef" />
</template>
```

面试回答：

```text
nextTick 用于等待 Vue 完成 DOM 更新后再执行逻辑。比如状态改变后要读取 DOM 高度、滚动到某个位置、聚焦 input，就需要 await nextTick。它解决的是响应式数据更新和 DOM 实际更新之间的时机问题。
```

### 2.7 `shallowRef`、`markRaw`

大对象、第三方实例、图表实例不一定要深度响应式。

```ts
import { markRaw, shallowRef } from 'vue'
import * as echarts from 'echarts'

const chart = shallowRef<echarts.ECharts | null>(null)

function init(el: HTMLElement) {
  chart.value = markRaw(echarts.init(el))
}
```

适用场景：

- ECharts 实例。
- 地图实例。
- 大量原始数据。
- 第三方类实例。

面试回答：

```text
如果一个对象很大，或者是第三方库实例，我不会让 Vue 做深度响应式转换。比如 ECharts 实例可以用 markRaw，外层引用用 shallowRef，这样能减少不必要的代理和依赖收集，也避免第三方对象被 Proxy 后出现兼容问题。
```

## 3. 模板语法和常见指令

### 3.1 `v-if` 和 `v-show`

```vue
<template>
  <div v-if="hasPermission">真正创建/销毁</div>
  <div v-show="visible">只切换 display</div>
</template>
```

区别：

- `v-if` 是条件渲染，条件为 false 时 DOM 不存在。
- `v-show` 是显示隐藏，DOM 一直存在，只改 `display`。
- 频繁切换用 `v-show`。
- 条件很少变化或权限控制用 `v-if`。

面试回答：

```text
v-if 控制节点是否渲染，切换成本较高，但初始条件为 false 时不会创建 DOM。v-show 总是渲染，只切换 display，初始成本高一点，但切换成本低。频繁展开收起用 v-show，权限控制或低频条件用 v-if。
```

### 3.2 `v-for` 和 `key`

```vue
<template>
  <ul>
    <li v-for="user in users" :key="user.id">
      {{ user.name }}
    </li>
  </ul>
</template>
```

为什么不用 index：

```vue
<!-- 不推荐 -->
<li v-for="(user, index) in users" :key="index">
  <input v-model="user.name" />
</li>
```

如果列表中间插入一项，index 会变化，Vue 可能复用错误节点，导致输入框状态错乱。

面试回答：

```text
key 用来标识节点身份，帮助 diff 判断哪些节点可以复用，哪些需要移动或重新创建。列表有增删改排序时，不能用 index 作为 key，因为 index 不稳定，可能导致组件状态或表单输入被错误复用。
```

### 3.3 `v-model`

普通输入：

```vue
<input v-model="keyword" />
```

等价于：

```vue
<input :value="keyword" @input="keyword = $event.target.value" />
```

Vue2 自定义组件：

```vue
<Child v-model="title" />
<!-- 等价于 -->
<Child :value="title" @input="title = $event" />
```

Vue3 自定义组件：

```vue
<Child v-model="title" />
<!-- 等价于 -->
<Child :modelValue="title" @update:modelValue="title = $event" />
```

Vue3 子组件写法：

```vue
<script setup lang="ts">
const props = defineProps<{
  modelValue: string
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void
}>()
</script>

<template>
  <input
    :value="props.modelValue"
    @input="emit('update:modelValue', ($event.target as HTMLInputElement).value)"
  />
</template>
```

多个 `v-model`：

```vue
<UserDialog
  v-model:visible="visible"
  v-model:username="username"
/>
```

子组件：

```vue
<script setup lang="ts">
defineProps<{
  visible: boolean
  username: string
}>()

const emit = defineEmits<{
  (e: 'update:visible', value: boolean): void
  (e: 'update:username', value: string): void
}>()
</script>
```

补充：Vue 3.4+ 有 `defineModel()`，可以简化自定义组件 `v-model`，但面试里掌握 `modelValue` / `update:modelValue` 是最稳的基础。

## 4. Props、Emit、组件通信

### 4.1 `defineProps`

```vue
<script setup lang="ts">
const props = withDefaults(
  defineProps<{
    title: string
    size?: 'small' | 'middle' | 'large'
  }>(),
  {
    size: 'middle',
  },
)
</script>

<template>
  <h3>{{ props.title }}</h3>
  <span>{{ props.size }}</span>
</template>
```

### 4.2 `defineEmits`

```vue
<script setup lang="ts">
const emit = defineEmits<{
  (e: 'submit', payload: { username: string }): void
  (e: 'cancel'): void
}>()

function submit() {
  emit('submit', { username: 'xsz' })
}
</script>
```

### 4.3 `defineExpose`

父组件想调用子组件方法：

```vue
<!-- Child.vue -->
<script setup lang="ts">
function validate() {
  return true
}

defineExpose({
  validate,
})
</script>
```

```vue
<!-- Parent.vue -->
<script setup lang="ts">
import { ref } from 'vue'
import Child from './Child.vue'

const childRef = ref<InstanceType<typeof Child> | null>(null)

function submit() {
  const valid = childRef.value?.validate()
  console.log(valid)
}
</script>

<template>
  <Child ref="childRef" />
  <button @click="submit">提交</button>
</template>
```

### 4.4 组件通信方式总结

- 父传子：`props`
- 子传父：`emit`
- 双向绑定：`v-model`
- 跨层级：`provide / inject`
- 全局状态：Pinia / Vuex
- 父组件调子组件方法：`ref + defineExpose`
- 路由传参：`params` / `query`
- Vue2 事件总线：可以知道，但 Vue3 不推荐作为主方案

面试回答：

```text
组件通信我会按关系选型。父子组件用 props 和 emit；表单类组件需要双向绑定时用 v-model；跨层级但不想引入全局状态时用 provide/inject；多个页面共享用户、权限、字典等状态时用 Pinia；父组件需要触发表单校验这类命令式行为时，用 ref 配合 defineExpose。
```

## 5. Vue Router

### 5.1 hash 和 history

hash：

```text
https://example.com/#/user/1
```

- hash 变化不会请求服务端页面。
- 部署简单。
- URL 不够干净。

history：

```text
https://example.com/user/1
```

- URL 更正常。
- 依赖 HTML5 History API。
- 服务端必须配置 fallback，否则刷新深层路由会 404。

Nginx 示例：

```nginx
location / {
  try_files $uri $uri/ /index.html;
}
```

面试回答：

```text
hash 模式依赖 URL 的 #，变化不会触发服务端请求，部署简单；history 模式 URL 更干净，但刷新深层路由时服务端需要 fallback 到 index.html，否则会 404。后台系统如果部署环境不可控可以用 hash，正式产品更常用 history。
```

### 5.2 `setup` 中使用路由

```vue
<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

function goDetail(id: number) {
  router.push({
    name: 'detail',
    params: { id },
  })
}
</script>
```

### 5.3 后台权限路由

常见流程：

```text
登录
  -> 保存 token
  -> 请求用户信息
  -> 获取角色 / 权限码 / 菜单树
  -> 生成动态路由
  -> router.addRoute
  -> 渲染菜单
  -> 路由守卫校验访问权限
```

前端维护完整路由表：

```ts
const asyncRoutes = [
  {
    path: '/report',
    name: 'Report',
    meta: { permission: 'report:view' },
    component: () => import('@/views/report/index.vue'),
  },
]

function filterRoutes(routes, permissions: string[]) {
  return routes.filter(route => {
    const code = route.meta?.permission
    if (!code || permissions.includes(code)) {
      if (route.children) {
        route.children = filterRoutes(route.children, permissions)
      }
      return true
    }
    return false
  })
}
```

路由守卫：

```ts
router.beforeEach(async (to, from, next) => {
  const token = getToken()

  if (!token && to.path !== '/login') {
    return next('/login')
  }

  if (token && !userStore.loaded) {
    await userStore.fetchUserInfo()
    userStore.accessRoutes.forEach(route => router.addRoute(route))
    return next({ ...to, replace: true })
  }

  next()
})
```

面试回答：

```text
后台权限路由一般分静态路由和动态路由。登录后拿 token，再请求用户信息和权限码。如果前端维护完整路由表，就按权限码过滤路由；如果后端返回菜单树，就把菜单树转换成路由配置。最后用 addRoute 注入，菜单根据过滤后的路由或菜单树渲染。路由守卫负责 token 校验、白名单、动态路由初始化和无权限跳转。
```

## 6. Pinia / Vuex

### 6.1 Vuex 核心

Vue2 常见 Vuex：

```js
const store = new Vuex.Store({
  state: {
    userInfo: null,
  },
  getters: {
    isLogin: state => !!state.userInfo,
  },
  mutations: {
    setUserInfo(state, payload) {
      state.userInfo = payload
    },
  },
  actions: {
    async fetchUserInfo({ commit }) {
      const data = await api.getUserInfo()
      commit('setUserInfo', data)
    },
  },
})
```

特点：

- 流程严格。
- mutation 必须同步。
- 模板代码较多。
- Vue2 项目非常常见。

### 6.2 Pinia 写法

```ts
// stores/user.ts
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: '',
    userInfo: null as null | { name: string },
  }),
  getters: {
    isLogin: state => Boolean(state.token),
  },
  actions: {
    async login(params: { username: string; password: string }) {
      const res = await loginApi(params)
      this.token = res.token
      this.userInfo = res.userInfo
    },
  },
})
```

使用：

```vue
<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const { token, userInfo, isLogin } = storeToRefs(userStore)
const { login } = userStore
</script>
```

为什么 `storeToRefs`？

```ts
const userStore = useUserStore()

// 不推荐：直接解构 state/getter 可能丢响应式
const { userInfo } = userStore

// 推荐
const { userInfo } = storeToRefs(userStore)

// action 可以直接解构
const { login } = userStore
```

面试回答：

```text
Vuex 更像传统集中式状态管理，state、getter、mutation、action 分层明确，但写法偏重。Pinia 是 Vue3 官方推荐生态里更常用的状态管理方案，去掉 mutations，可以直接在 action 或组件里修改 state，TypeScript 推导更友好，也更贴合 Composition API。使用 Pinia 时，解构 state 和 getter 推荐 storeToRefs，避免丢响应式；action 可以直接解构。
```

## 7. 后台系统高频场景

### 7.1 登录鉴权

典型链路：

```text
登录表单
  -> login API
  -> 保存 token
  -> axios 请求拦截器加 token
  -> 响应拦截器处理 401
  -> 路由守卫控制页面访问
```

axios 示例：

```ts
import axios from 'axios'

const request = axios.create({
  baseURL: '/api',
  timeout: 10000,
})

request.interceptors.request.use(config => {
  const token = getToken()
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

request.interceptors.response.use(
  response => response.data,
  error => {
    if (error.response?.status === 401) {
      removeToken()
      router.push('/login')
    }
    return Promise.reject(error)
  },
)
```

面试回答：

```text
登录鉴权我一般分三层：接口层、路由层、UI 层。接口层通过请求拦截器统一带 token，响应拦截器处理 401 和过期；路由层通过 beforeEach 判断白名单、登录态和页面权限；UI 层根据权限码控制菜单和按钮展示。但真正的数据权限和接口权限必须后端兜底，前端隐藏按钮不等于安全。
```

### 7.2 动态菜单和按钮权限

菜单权限：

```ts
type MenuItem = {
  title: string
  path: string
  permission?: string
  children?: MenuItem[]
}
```

按钮权限：

```vue
<template>
  <button v-if="hasPermission('user:create')">新增用户</button>
  <button v-if="hasPermission('user:delete')">删除用户</button>
</template>
```

封装指令：

```ts
app.directive('permission', {
  mounted(el, binding) {
    const code = binding.value
    if (!permissionStore.codes.includes(code)) {
      el.parentNode?.removeChild(el)
    }
  },
})
```

使用：

```vue
<button v-permission="'user:create'">新增</button>
```

注意：

- 菜单权限：控制能看到哪些页面入口。
- 路由权限：控制能不能访问页面。
- 按钮权限：控制页面内操作。
- 接口权限：必须后端校验。

### 7.3 表格组件封装

思路：配置 + 插槽 + 事件。

```vue
<BaseTable
  :columns="columns"
  :data="list"
  :loading="loading"
  :pagination="pagination"
  @page-change="fetchList"
>
  <template #status="{ row }">
    <StatusTag :value="row.status" />
  </template>

  <template #actions="{ row }">
    <button @click="edit(row)">编辑</button>
  </template>
</BaseTable>
```

columns：

```ts
const columns = [
  { title: '用户名', key: 'username', width: 160 },
  { title: '状态', key: 'status', slot: 'status' },
  { title: '操作', key: 'actions', slot: 'actions', fixed: 'right' },
]
```

面试回答：

```text
后台表格我一般会按配置 + 插槽 + 事件封装。通用能力如 loading、分页、排序、筛选、空状态放在 BaseTable 里；列定义通过 columns 配置；复杂单元格通过 slot 或 render 暴露扩展点。这样简单表格可以配置生成，复杂业务又不会被 schema 限死。
```

### 7.4 表单组件封装

```vue
<BaseForm
  v-model="form"
  :schema="schema"
  @submit="handleSubmit"
/>
```

schema：

```ts
const schema = [
  {
    field: 'username',
    label: '用户名',
    component: 'Input',
    rules: [{ required: true, message: '请输入用户名' }],
  },
  {
    field: 'role',
    label: '角色',
    component: 'Select',
    options: roleOptions,
  },
]
```

面试回答：

```text
表单封装我会把字段、组件类型、校验规则、默认值、联动逻辑抽象成 schema。通用场景用 schema 提效，复杂场景保留 slot 或自定义 render。核心是不要为了配置化牺牲可维护性，复杂业务仍然允许局部手写。
```

## 8. 可视化和大屏

### 8.1 ECharts 组件封装

```vue
<template>
  <div ref="chartRef" class="chart"></div>
</template>

<script setup lang="ts">
import { markRaw, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import * as echarts from 'echarts'

const props = defineProps<{
  option: echarts.EChartsOption
}>()

const chartRef = ref<HTMLDivElement | null>(null)
let chart: echarts.ECharts | null = null

onMounted(async () => {
  await nextTick()
  if (chartRef.value) {
    chart = markRaw(echarts.init(chartRef.value))
    chart.setOption(props.option)
  }
})

watch(
  () => props.option,
  option => {
    chart?.setOption(option)
  },
  { deep: true },
)

onBeforeUnmount(() => {
  chart?.dispose()
  chart = null
})
</script>
```

注意点：

- 容器不可见时初始化可能拿不到宽高。
- tab / modal 展示后要调用 `resize`。
- 组件卸载时必须 `dispose`，否则内存泄漏。
- ECharts 实例不要深度 reactive。

### 8.2 WebSocket 高频数据

不要每条消息都直接更新图表。

```ts
const queue: Message[] = []
let timer: number | undefined

socket.onmessage = event => {
  queue.push(JSON.parse(event.data))

  if (!timer) {
    timer = window.setTimeout(() => {
      const batch = queue.splice(0)
      updateChart(batch)
      timer = undefined
    }, 200)
  }
}
```

面试回答：

```text
高频 WebSocket 数据不能每条都触发响应式更新或 setOption。我的处理方式是先进入队列，再按固定频率批处理，比如 100ms 或 200ms 合并一次，图表用增量数据更新。同时要控制数据窗口大小，避免数组无限增长；组件卸载时清理 socket、定时器和图表实例。
```

### 8.3 大屏卡顿排查

排查顺序：

1. Chrome Performance 看长任务、FPS。
2. Memory 看内存是否持续增长。
3. Network / WebSocket 看消息频率和数据量。
4. 检查图表是否重复初始化。
5. 检查是否全量 setOption。
6. 检查是否大量深度响应式数据。

面试回答：

```text
大屏卡顿我会先用 Performance 看主线程长任务和 FPS，再用 Memory 看内存是否持续上涨。然后检查 WebSocket 消息频率、图表 setOption 策略、是否重复初始化 ECharts、组件卸载是否 dispose。优化上会做消息节流批处理、图表增量更新、限制数据窗口、清理资源，必要时把大数据用 shallowRef 或普通变量承载，避免进入深度响应式。
```

## 9. 性能优化

### 9.1 首屏加载

常见手段：

- 路由懒加载。
- 组件异步加载。
- 图片 CDN、压缩、懒加载。
- 第三方库按需引入。
- 打包拆分，分析 bundle。
- 骨架屏。
- 静态资源缓存。

路由懒加载：

```ts
const routes = [
  {
    path: '/report',
    component: () => import('@/views/report/index.vue'),
  },
]
```

异步组件：

```ts
import { defineAsyncComponent } from 'vue'

const HeavyChart = defineAsyncComponent(() => import('./HeavyChart.vue'))
```

### 9.2 Vue 组件渲染优化

- 合理拆组件，减少无关更新。
- 用 `computed` 缓存派生数据。
- 大列表用虚拟滚动。
- 巨大对象用 `shallowRef` / `markRaw`。
- 不频繁创建新对象传给子组件。
- 用稳定 `key`。
- Vue3 可提 `v-memo` / `v-once`。

`v-once`：

```vue
<div v-once>{{ staticTitle }}</div>
```

`v-memo`：

```vue
<div v-for="item in list" :key="item.id" v-memo="[item.id, item.selected]">
  {{ item.name }}
</div>
```

面试回答：

```text
Vue 性能优化我会先区分是加载慢还是渲染慢。加载慢看资源体积、懒加载、缓存；渲染慢看组件更新范围、大列表、图表、深度响应式对象。Vue3 里可以用 computed 缓存派生数据，KeepAlive 缓存页面，v-memo/v-once 跳过稳定内容，大数据用 shallowRef 或 markRaw 避免不必要代理。
```

### 9.3 KeepAlive

```vue
<router-view v-slot="{ Component }">
  <KeepAlive include="UserList">
    <component :is="Component" />
  </KeepAlive>
</router-view>
```

生命周期：

```ts
onActivated(() => {
  console.log('页面被激活')
})

onDeactivated(() => {
  console.log('页面被缓存')
})
```

后台场景：

- 列表页进入详情页后返回，保留筛选条件。
- tab 页切换保留组件状态。
- 表单草稿保留。

注意：

- 缓存太多会占内存。
- 需要设计 include / exclude / max。
- 不是所有页面都应该缓存。

## 10. Vue2 经典八股

### 10.1 为什么组件 `data` 是函数

回答：

```text
组件可能被复用多次。如果 data 是一个对象，多个组件实例会共享同一个对象引用，导致状态互相污染。写成函数，每次创建组件实例都会执行 data 函数并返回一个新的对象，保证每个实例拥有独立状态。
```

代码：

```js
export default {
  data() {
    return {
      count: 0,
    }
  },
}
```

### 10.2 Vue2 父子生命周期顺序

加载：

```text
父 beforeCreate
父 created
父 beforeMount
子 beforeCreate
子 created
子 beforeMount
子 mounted
父 mounted
```

更新：

```text
父 beforeUpdate
子 beforeUpdate
子 updated
父 updated
```

销毁：

```text
父 beforeDestroy
子 beforeDestroy
子 destroyed
父 destroyed
```

### 10.3 `computed` 和 `watch`

回答：

```text
computed 用来声明派生状态，有缓存，依赖不变不会重新计算；watch 用来监听数据变化并执行副作用，比如请求接口、埋点、手动操作 DOM。简单来说，能用 computed 表达的派生数据不要用 watch；需要异步或副作用时用 watch。
```

### 10.4 `nextTick` 原理

回答：

```text
Vue 更新 DOM 是异步批处理的。数据变化后，Vue 会把 watcher 更新放进队列，同一轮事件循环里多次数据变化会合并，等同步代码执行完后再统一刷新 DOM。nextTick 就是在 DOM 更新完成后执行回调，底层优先使用微任务，比如 Promise.then，兼容场景下会降级。
```

### 10.5 Vue diff 简述

Vue2 双端 diff 常见说法：

```text
Vue diff 是同层比较，不跨层级比较。Vue2 对子节点采用双端比较，用 oldStart、oldEnd、newStart、newEnd 四个指针从两端向中间移动，尽量复用已有节点，减少 DOM 操作。key 的作用就是帮助 diff 更准确地识别节点身份。
```

Vue3 加分点：

```text
Vue3 在编译阶段增加了 patch flag、静态提升、block tree 等优化，能更精准地知道哪些节点是动态的，运行时 diff 的范围更小。
```

## 11. Vue2 -> Vue3 迁移常考

重点变化：

- `new Vue()` 改为 `createApp()`。
- Vue3 自定义组件 `v-model` 使用 `modelValue` / `update:modelValue`。
- `.sync` 移除，使用 `v-model:xxx`。
- filter 移除，改用 computed / methods。
- 事件总线不再推荐。
- Vuex 可迁移到 Pinia。
- Vue Router 在 `setup` 中用 `useRouter` / `useRoute`。
- 插件注册方式变化。
- Vue3 支持 Fragment，即多个根节点。

入口对比：

```js
// Vue2
new Vue({
  router,
  store,
  render: h => h(App),
}).$mount('#app')
```

```ts
// Vue3
import { createApp } from 'vue'
import App from './App.vue'

createApp(App)
  .use(router)
  .use(pinia)
  .mount('#app')
```

面试回答：

```text
Vue2 到 Vue3 迁移主要关注响应式、入口 API、v-model、filter、事件总线、路由和状态管理。createApp 替代 new Vue；自定义组件 v-model 从 value/input 变为 modelValue/update:modelValue，并支持多个 v-model；filter 被移除，建议用 computed 或 methods；复杂项目里 Vuex 可以逐步迁移到 Pinia。迁移时我会先跑 migration build 或梳理破坏性变更，再按模块逐步改造和回归测试。
```

## 12. TypeScript 在 Vue3 中怎么用

### 12.1 props 和 emits 类型

```vue
<script setup lang="ts">
type User = {
  id: number
  name: string
}

const props = defineProps<{
  user: User
  mode?: 'view' | 'edit'
}>()

const emit = defineEmits<{
  (e: 'save', user: User): void
  (e: 'cancel'): void
}>()
</script>
```

### 12.2 ref DOM 类型

```ts
const inputRef = ref<HTMLInputElement | null>(null)

function focus() {
  inputRef.value?.focus()
}
```

### 12.3 API 类型

```ts
type PageResult<T> = {
  list: T[]
  total: number
}

type User = {
  id: number
  name: string
}

async function fetchUsers(): Promise<PageResult<User>> {
  return request.get('/users')
}
```

面试回答：

```text
Vue3 比 Vue2 更适合 TypeScript，因为 Composition API 直接用函数和变量组织逻辑，类型推导更自然。defineProps、defineEmits 可以用泛型声明 props 和事件类型，Pinia 对 state、getter、action 的类型支持也更好。实际项目里我会重点给组件入参、emit、接口响应、表单模型和 store 状态补类型。
```

## 13. Vite / Webpack

### 13.1 Vite 为什么快

回答：

```text
Vite 开发环境利用浏览器原生 ESM，启动时不需要把整个项目先打包，而是按需转换当前请求的源码。依赖预构建通常使用 esbuild，把 CommonJS 或多文件依赖转成 ESM 并合并请求，所以冷启动和热更新更快。生产环境 Vite 通常使用 Rollup 打包。
```

### 13.2 Webpack 和 Vite 区别

```text
Webpack 是传统打包器，会从入口构建完整依赖图，生态成熟，适合复杂定制。Vite 开发环境基于原生 ESM 和按需编译，启动和 HMR 更快，生产构建用 Rollup。Vue3 新项目一般优先 Vite，但老项目、复杂插件体系或历史工程仍可能继续使用 Webpack。
```

## 14. AI 辅助开发 / Vibe Coding 怎么讲

这个问题现在很常见，尤其 AI 应用岗位。

推荐回答：

```text
我会把 AI 当成提效工具，不当成最终交付者。一般我会先自己拆需求、确定边界和数据结构，再让 Cursor / Copilot 辅助生成组件模板、类型定义、表格 columns、表单 schema、单测草稿或重构建议。生成后我会重点检查业务逻辑、类型、异常处理、权限边界和是否引入不必要复杂度，最后通过 lint、类型检查、自测和真实数据验证。架构取舍和关键业务判断仍然由我自己负责。
```

可以举的例子：

- 根据字段配置生成表单 schema。
- 根据接口类型生成表格 columns。
- 让 AI 辅助补 TypeScript 类型。
- 把重复逻辑抽成 composable。
- 贴错误日志让 AI 给排查方向，但最终自己验证。

面试官追问：怎么避免 AI 写垃圾代码？

```text
我会先给 AI 明确上下文、约束、代码风格和不能做的事情，避免它自由发挥。生成后重点看三类问题：业务规则是否符合需求，类型和边界是否完整，代码是否过度设计或不可维护。最后必须跑 lint、类型检查和关键流程自测，涉及公共逻辑时还要补测试或让同事 review。
```

## 15. 高频八股问答

### 15.1 Vue 的响应式原理是什么？

回答：

```text
Vue 的响应式核心是依赖收集和派发更新。数据被读取时收集当前使用它的副作用，比如组件渲染、computed、watch；数据被修改时通知这些依赖重新执行。Vue2 用 Object.defineProperty 劫持属性，Vue3 用 Proxy 代理对象，并用 getter/setter 处理 ref。
```

### 15.2 Vue3 为什么用 Proxy？

回答：

```text
Proxy 可以代理整个对象，不需要像 Object.defineProperty 那样逐个属性劫持。它可以监听新增、删除、in、遍历、数组变化等操作，解决 Vue2 中对象新增属性和部分数组操作不响应的问题。但 Proxy 也有兼容性要求，不支持 IE。
```

### 15.3 `ref` 和 `reactive` 区别？

回答：

```text
ref 返回一个带 value 的响应式引用，适合基础类型，也能包对象；reactive 返回响应式代理对象，适合对象和数组。ref 在脚本里要用 .value，模板中自动解包。reactive 不能直接解构，否则会丢响应式，需要 toRefs。
```

### 15.4 `computed` 和 `watch` 区别？

回答：

```text
computed 用于声明派生状态，有缓存，依赖不变不会重新计算；watch 用于监听数据变化执行副作用，适合请求接口、埋点、操作 DOM 等。能用 computed 表达的数据推导，不要用 watch。
```

### 15.5 Vue3 的 `v-model` 有什么变化？

回答：

```text
Vue2 自定义组件 v-model 默认是 value + input。Vue3 改成 modelValue + update:modelValue，并支持多个 v-model，比如 v-model:title、v-model:visible。这样自定义组件的双向绑定语义更清晰，也替代了 Vue2 的 .sync。
```

### 15.6 Pinia 和 Vuex 区别？

回答：

```text
Vuex 流程更严格，有 state、getters、mutations、actions、modules，但写法偏重。Pinia 更轻，没有 mutations，可以直接改 state，action 同时支持同步和异步，TypeScript 支持更好，也更适合 Vue3 的 Composition API。
```

### 15.7 Vue Router 权限怎么做？

回答：

```text
后台系统一般登录后获取 token，再请求用户信息和权限码。路由分静态路由和动态路由，动态路由根据权限码过滤或由后端菜单树生成，然后通过 addRoute 注入。路由守卫负责白名单、登录态、动态路由初始化和页面权限校验。按钮权限用权限码控制展示，但接口权限必须后端兜底。
```

### 15.8 Vue3 怎么做逻辑复用？

回答：

```text
Vue3 推荐用 composable，也就是 useXxx 函数，把某个业务功能相关的响应式状态、计算属性、watch 和方法封装在一起。比如 useTable、usePermission、useChart。相比 mixin，composable 来源清晰，命名冲突少，类型推导更好，也更容易测试。
```

### 15.9 为什么不推荐 mixin？

回答：

```text
mixin 会把 data、methods、生命周期等合并进组件，来源不清晰，容易命名冲突，也不利于 TypeScript 推导。复杂项目里多个 mixin 叠加后，很难判断某个变量或方法来自哪里。Vue3 更推荐 composable 做逻辑复用。
```

### 15.10 Vue 如何做性能优化？

回答：

```text
我会先区分加载性能和渲染性能。加载性能看路由懒加载、组件异步加载、图片优化、CDN、打包拆分和缓存。渲染性能看组件拆分、computed 缓存、大列表虚拟滚动、稳定 key、KeepAlive、v-memo/v-once，以及避免巨大对象进入深度响应式系统。可视化场景还要注意图表销毁、高频数据节流和增量更新。
```

## 16. 7 天快速上手计划

### Day 1：Vue2 基础回忆

- 响应式限制。
- `data` 为什么是函数。
- 生命周期。
- `computed` / `watch`。
- 组件通信。

### Day 2：Vue3 Composition API

- `ref`、`reactive`、`computed`。
- `watch`、`watchEffect`。
- `<script setup>`。
- 写一个搜索列表组件。

### Day 3：组件通信和 TypeScript

- `defineProps`。
- `defineEmits`。
- `v-model`。
- `defineExpose`。
- 写一个弹窗或表单组件。

### Day 4：Router + Pinia

- 登录态。
- 动态路由。
- 菜单权限。
- Pinia 用户 store。

### Day 5：后台系统组件

- 表格封装。
- 表单封装。
- axios 拦截器。
- KeepAlive。

### Day 6：可视化和性能

- ECharts 组件封装。
- WebSocket 批处理。
- 大屏适配。
- 内存泄漏排查。

### Day 7：面试表达

- 准备 10 道八股。
- 把自己的 BI 报表、驾驶舱、权限、表格组件用 Vue3 口径讲一遍。
- 准备 AI 辅助开发回答。

## 17. 面试前 10 分钟速背

```text
Vue2 用 Object.defineProperty，Vue3 用 Proxy。
Vue3 响应式核心仍是依赖收集和派发更新。
ref 包基础类型，脚本里用 .value；reactive 包对象，解构要 toRefs。
computed 有缓存，适合派生状态；watch 适合副作用和异步。
watchEffect 自动收集依赖，但复杂业务 watch 更可控。
Vue3 v-model 默认 modelValue / update:modelValue，支持多个 v-model。
<script setup> 是编译期语法糖，顶层变量可直接用于模板。
Pinia 比 Vuex 更轻，没有 mutations，TS 更友好。
Router setup 里用 useRouter / useRoute。
权限路由：token -> 用户信息 -> 权限码/菜单 -> addRoute -> 路由守卫。
大屏优化：节流、批处理、增量更新、dispose 图表、清理 WebSocket。
AI 辅助开发：先拆需求和约束，再生成，最后人工校验、自测、lint。
```

## 18. 参考资料

- Vue 官方文档：`https://vuejs.org/`
- Vue Reactivity API：`https://vuejs.org/api/reactivity-core.html`
- Vue Reactivity in Depth：`https://vuejs.org/guide/extras/reactivity-in-depth.html`
- Vue `<script setup>`：`https://vuejs.org/api/sfc-script-setup.html`
- Vue 3 Migration Guide：`https://v3-migration.vuejs.org/`
- Vue Router：`https://router.vuejs.org/`
- Pinia：`https://pinia.vuejs.org/`

