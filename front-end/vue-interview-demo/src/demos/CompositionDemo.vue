<script setup lang="ts">
import { computed, reactive, ref, toRefs } from 'vue'
import DemoCard from '../components/DemoCard.vue'

const count = ref(1)
const profile = reactive({
  name: 'Vue3',
  role: 'frontend',
})
const { name, role } = toRefs(profile)

const summary = computed(() => `${name.value} / ${role.value} / count=${count.value}`)

function switchRole() {
  role.value = role.value === 'frontend' ? 'fullstack-front' : 'frontend'
  count.value++
}
</script>

<template>
  <DemoCard
    title="ref、reactive、toRefs 怎么用？"
    interview="ref 适合基础类型，reactive 适合对象。reactive 直接解构会丢响应式，要用 toRefs 或 storeToRefs。"
  >
    <div class="mini-panel">
      <p><strong>响应式摘要：</strong>{{ summary }}</p>
      <p>模板里 ref 会自动解包；脚本里访问 ref 要用 `.value`。</p>
      <button @click="switchRole">切换角色并增加 count</button>
    </div>
  </DemoCard>
</template>
