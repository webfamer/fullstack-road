<script setup lang="ts">
import { storeToRefs } from 'pinia'
import DemoCard from '../components/DemoCard.vue'
import { useUserStore } from '../stores/user'

const user = useUserStore()
const { role, permissions, isAdmin } = storeToRefs(user)
</script>

<template>
  <DemoCard
    title="Pinia 和 Vuex 有什么区别？"
    interview="Pinia 写法更轻，没有 mutations，TypeScript 支持更自然。解构 state/getters 要用 storeToRefs，避免丢响应式。"
  >
    <div class="mini-panel">
      <p>role：{{ role }}</p>
      <p>isAdmin：{{ isAdmin }}</p>
      <p>permissions：{{ permissions.join(' / ') }}</p>
      <div class="button-row">
        <button @click="user.switchRole('operator')">切到 operator</button>
        <button @click="user.switchRole('admin')">切到 admin</button>
      </div>
    </div>
  </DemoCard>
</template>
