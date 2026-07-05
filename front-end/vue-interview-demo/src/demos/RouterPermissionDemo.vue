<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore, type Role } from '../stores/user'
import DemoCard from '../components/DemoCard.vue'

const router = useRouter()
const route = useRoute()
const user = useUserStore()

const menus = [
  { label: '驾驶舱', path: '/dashboard', permission: 'dashboard:view' },
  { label: '报表中心', path: '/report', permission: 'report:view' },
  { label: '系统管理', path: '/admin', permission: 'admin:view' },
]

const visibleMenus = computed(() => menus.filter((menu) => user.hasPermission(menu.permission)))
const currentPermission = computed(() => route.meta.permission)
const canOpenCurrent = computed(() => user.hasPermission(currentPermission.value))

function switchRole(role: Role) {
  user.switchRole(role)
  if (!user.hasPermission(currentPermission.value)) {
    router.push('/dashboard')
  }
}
</script>

<template>
  <DemoCard
    title="后台权限路由怎么设计？"
    interview="常见流程：登录拿 token -> 获取用户权限 -> 过滤菜单/动态路由 -> addRoute -> 路由守卫校验。这个 demo 用 Pinia 模拟角色权限。"
  >
    <div class="grid two">
      <section class="mini-panel">
        <h4>切换角色</h4>
        <div class="button-row">
          <button @click="switchRole('visitor')">visitor</button>
          <button @click="switchRole('operator')">operator</button>
          <button @click="switchRole('admin')">admin</button>
        </div>
        <p>当前角色：<strong>{{ user.role }}</strong></p>
        <p>权限码：{{ user.permissions.join(' / ') }}</p>
      </section>

      <section class="mini-panel">
        <h4>动态菜单</h4>
        <div class="menu-row">
          <button v-for="menu in visibleMenus" :key="menu.path" @click="router.push(menu.path)">
            {{ menu.label }}
          </button>
        </div>
        <p>当前路由：{{ route.path }}</p>
        <p :class="canOpenCurrent ? 'ok' : 'danger'">当前页面权限：{{ canOpenCurrent ? '允许访问' : '无权限' }}</p>
      </section>
    </div>
  </DemoCard>
</template>
