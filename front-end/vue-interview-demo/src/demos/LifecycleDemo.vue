<script setup lang="ts">
import { ref } from 'vue'
import DemoCard from '../components/DemoCard.vue'
import LogPanel from '../components/LogPanel.vue'
import LifecycleChild from './parts/LifecycleChild.vue'

const visible = ref(true)
const cached = ref(true)
const logs = ref<string[]>([])

function addLog(message: string) {
  logs.value.unshift(message)
}
</script>

<template>
  <DemoCard
    title="生命周期和 KeepAlive 怎么讲？"
    interview="Vue3 用 onMounted/onUpdated/onUnmounted 等钩子；KeepAlive 缓存组件时会触发 activated/deactivated。"
  >
    <div class="grid two">
      <section class="mini-panel">
        <div class="button-row">
          <button @click="visible = !visible">{{ visible ? '卸载组件' : '挂载组件' }}</button>
          <button class="ghost" @click="cached = !cached">{{ cached ? '关闭缓存' : '开启缓存' }}</button>
        </div>

        <KeepAlive v-if="cached">
          <LifecycleChild v-if="visible" mode="KeepAlive" @log="addLog" />
        </KeepAlive>
        <LifecycleChild v-else-if="visible" mode="普通组件" @log="addLog" />
      </section>
      <LogPanel :logs="logs.slice(0, 10)" />
    </div>
  </DemoCard>
</template>
