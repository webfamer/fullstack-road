<script setup lang="ts">
import { computed, ref } from 'vue'
import ReactivityDemo from './demos/ReactivityDemo.vue'
import CompositionDemo from './demos/CompositionDemo.vue'
import WatchDemo from './demos/WatchDemo.vue'
import ConditionalDemo from './demos/ConditionalDemo.vue'
import VModelDemo from './demos/VModelDemo.vue'
import LifecycleDemo from './demos/LifecycleDemo.vue'
import RouterPermissionDemo from './demos/RouterPermissionDemo.vue'
import PiniaDemo from './demos/PiniaDemo.vue'
import PerformanceDemo from './demos/PerformanceDemo.vue'
import VibeCodingDemo from './demos/VibeCodingDemo.vue'

const demos = [
  { id: 'reactivity', title: 'Vue2 / Vue3 响应式', tag: 'Proxy', component: ReactivityDemo },
  { id: 'composition', title: 'Composition API', tag: 'ref/reactive', component: CompositionDemo },
  { id: 'watch', title: 'computed / watch', tag: '副作用', component: WatchDemo },
  { id: 'conditional', title: 'v-if / v-show', tag: '渲染', component: ConditionalDemo },
  { id: 'vmodel', title: 'Vue3 v-model', tag: '组件通信', component: VModelDemo },
  { id: 'lifecycle', title: '生命周期 / KeepAlive', tag: '缓存', component: LifecycleDemo },
  { id: 'router', title: '路由权限', tag: '后台系统', component: RouterPermissionDemo },
  { id: 'pinia', title: 'Pinia 状态管理', tag: 'store', component: PiniaDemo },
  { id: 'performance', title: '大屏性能优化', tag: 'WebSocket', component: PerformanceDemo },
  { id: 'vibe', title: 'Vibe Coding 工作流', tag: 'AI 提效', component: VibeCodingDemo },
]

const activeId = ref(demos[0].id)
const activeDemo = computed(() => demos.find((demo) => demo.id === activeId.value) ?? demos[0])
</script>

<template>
  <main class="shell">
    <aside class="sidebar">
      <div class="brand">
        <span class="eyebrow">Vue 面试实验台</span>
        <h1>把题背成能跑的代码</h1>
        <p>Vue2 / Vue3 高频题、后台权限、可视化性能和 Vibe Coding，都放在一个可操作项目里。</p>
      </div>

      <nav class="nav-list" aria-label="Vue demo list">
        <button
          v-for="demo in demos"
          :key="demo.id"
          class="nav-item"
          :class="{ active: demo.id === activeId }"
          type="button"
          @click="activeId = demo.id"
        >
          <span>{{ demo.title }}</span>
          <small>{{ demo.tag }}</small>
        </button>
      </nav>
    </aside>

    <section class="stage">
      <header class="stage-header">
        <div>
          <span class="eyebrow">当前知识点</span>
          <h2>{{ activeDemo.title }}</h2>
        </div>
        <span class="pill">{{ activeDemo.tag }}</span>
      </header>

      <component :is="activeDemo.component" />
    </section>
  </main>
</template>
