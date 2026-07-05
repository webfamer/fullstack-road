<script setup lang="ts">
import { ref } from 'vue'
import DemoCard from '../components/DemoCard.vue'
import ModelEditor from './parts/ModelEditor.vue'

const title = ref('Vue3 v-model')
const visible = ref(true)
</script>

<template>
  <DemoCard
    title="Vue3 自定义组件 v-model 有什么变化？"
    interview="Vue3 默认使用 modelValue / update:modelValue，并支持多个 v-model，例如 v-model:title 和 v-model:visible。"
  >
    <div class="mini-panel">
      <ModelEditor v-model:title="title" v-model:visible="visible" />
      <p><strong>父组件 title：</strong>{{ title }}</p>
      <p><strong>父组件 visible：</strong>{{ visible }}</p>
    </div>
  </DemoCard>
</template>
