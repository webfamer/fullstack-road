<script setup lang="ts">
import { computed, onBeforeUnmount, ref, shallowRef } from 'vue'
import DemoCard from '../components/DemoCard.vue'

type Point = { id: number; value: number }

const running = ref(false)
const rawMessages = ref(0)
const chartData = shallowRef<Point[]>([])
let timer: number | undefined
let buffer: Point[] = []

const maxValue = computed(() => Math.max(10, ...chartData.value.map((item) => item.value)))

function flushBuffer() {
  if (!buffer.length) return
  chartData.value = [...chartData.value, ...buffer].slice(-24)
  buffer = []
}

function startStream() {
  if (running.value) return
  running.value = true
  timer = window.setInterval(() => {
    rawMessages.value++
    buffer.push({ id: rawMessages.value, value: Math.round(Math.random() * 100) })
    if (rawMessages.value % 5 === 0) {
      flushBuffer()
    }
  }, 120)
}

function stopStream() {
  running.value = false
  if (timer) window.clearInterval(timer)
  flushBuffer()
}

function reset() {
  stopStream()
  rawMessages.value = 0
  chartData.value = []
  buffer = []
}

onBeforeUnmount(stopStream)
</script>

<template>
  <DemoCard
    title="WebSocket 高频数据和大屏怎么优化？"
    interview="不要每条消息都触发渲染。常用队列、节流、批处理、增量更新；大数组可用 shallowRef，长时间运行要清理定时器、图表实例和连接。"
  >
    <div class="mini-panel">
      <div class="button-row">
        <button @click="startStream">模拟 WebSocket</button>
        <button class="ghost" @click="stopStream">暂停</button>
        <button class="ghost" @click="reset">重置</button>
      </div>
      <p>收到消息：{{ rawMessages }}；实际渲染点数：{{ chartData.length }}</p>
      <div class="bars" aria-label="mock chart">
        <span
          v-for="point in chartData"
          :key="point.id"
          :style="{ height: `${(point.value / maxValue) * 140 + 8}px` }"
          :title="String(point.value)"
        />
      </div>
    </div>
  </DemoCard>
</template>
