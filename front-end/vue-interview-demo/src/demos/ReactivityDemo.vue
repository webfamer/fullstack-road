<script setup lang="ts">
import { computed, reactive, ref } from 'vue'
import DemoCard from '../components/DemoCard.vue'

const defineCount = ref(0)
const proxyState = reactive({
  user: { name: '项思哲', level: 7 },
  list: ['Vue2', 'Vue3'],
})

const vue2Like: Record<string, unknown> = {}
let internalValue = 'old'
Object.defineProperty(vue2Like, 'known', {
  get() {
    return internalValue
  },
  set(value) {
    internalValue = String(value)
    defineCount.value++
  },
})

function addVue2LikeProp() {
  vue2Like.newProp = `新增属性 ${Date.now().toString().slice(-4)}`
}

function updateProxy() {
  proxyState.user.name = proxyState.user.name === '项思哲' ? 'Vue 候选人' : '项思哲'
  proxyState.list[1] = proxyState.list[1] === 'Vue3' ? 'Proxy 响应式' : 'Vue3'
}

const proxySnapshot = computed(() => JSON.stringify(proxyState, null, 2))
</script>

<template>
  <DemoCard
    title="Vue2 和 Vue3 响应式有什么区别？"
    interview="Vue2 基于 Object.defineProperty，只能劫持已有属性；Vue3 使用 Proxy 代理整个对象，新增、删除、数组索引等场景覆盖更完整。"
  >
    <div class="grid two">
      <section class="mini-panel">
        <h4>Vue2 类比：Object.defineProperty</h4>
        <p>修改已劫持属性会触发 setter，新增属性不会被这个 setter 捕获。</p>
        <div class="button-row">
          <button @click="vue2Like.known = `更新 ${Date.now().toString().slice(-4)}`">修改 known</button>
          <button class="ghost" @click="addVue2LikeProp">新增 newProp</button>
        </div>
        <pre>{{ vue2Like }}</pre>
        <span class="metric">setter 触发次数：{{ defineCount }}</span>
      </section>

      <section class="mini-panel">
        <h4>Vue3：Proxy + reactive</h4>
        <p>对象属性和数组索引变化都能被响应式系统追踪。</p>
        <button @click="updateProxy">修改对象和数组</button>
        <pre>{{ proxySnapshot }}</pre>
      </section>
    </div>
  </DemoCard>
</template>
