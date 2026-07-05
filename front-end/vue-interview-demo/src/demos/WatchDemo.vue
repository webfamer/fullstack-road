<script setup lang="ts">
import { computed, ref, watch, watchEffect } from 'vue'
import DemoCard from '../components/DemoCard.vue'
import LogPanel from '../components/LogPanel.vue'

const keyword = ref('报表')
const page = ref(1)
const logs = ref<string[]>([])

const queryText = computed(() => `${keyword.value} / 第 ${page.value} 页`)

watch(keyword, (next, prev) => {
  page.value = 1
  logs.value.unshift(`watch: keyword 从 "${prev}" 变成 "${next}"，重置页码`)
})

watchEffect(() => {
  logs.value.unshift(`watchEffect: 自动收集依赖 -> ${queryText.value}`)
})
</script>

<template>
  <DemoCard
    title="computed、watch、watchEffect 区别？"
    interview="computed 用于派生状态且有缓存；watch 适合异步请求、埋点、重置页码等副作用；watchEffect 会自动收集依赖。"
  >
    <div class="grid two">
      <section class="mini-panel">
        <label>
          搜索关键词
          <input v-model="keyword" />
        </label>
        <div class="button-row">
          <button @click="page++">下一页</button>
          <button class="ghost" @click="logs = []">清空日志</button>
        </div>
        <p><strong>computed：</strong>{{ queryText }}</p>
      </section>
      <LogPanel :logs="logs.slice(0, 8)" />
    </div>
  </DemoCard>
</template>
