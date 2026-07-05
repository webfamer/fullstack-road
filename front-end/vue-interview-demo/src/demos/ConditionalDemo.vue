<script setup lang="ts">
import { ref } from 'vue'
import DemoCard from '../components/DemoCard.vue'

const showIf = ref(true)
const showDisplay = ref(true)
</script>

<template>
  <DemoCard
    title="v-if 和 v-show 怎么选？"
    interview="v-if 会创建/销毁节点，适合低频切换；v-show 只改 display，适合高频切换。"
  >
    <div class="grid two">
      <section class="mini-panel">
        <h4>v-if</h4>
        <button @click="showIf = !showIf">切换 v-if</button>
        <p v-if="showIf" class="notice">我会被创建或销毁。</p>
      </section>
      <section class="mini-panel">
        <h4>v-show</h4>
        <button @click="showDisplay = !showDisplay">切换 v-show</button>
        <p v-show="showDisplay" class="notice">我一直在 DOM 里，只切换 display。</p>
      </section>
    </div>
  </DemoCard>
</template>
