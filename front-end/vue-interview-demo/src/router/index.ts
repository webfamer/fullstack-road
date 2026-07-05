import { createRouter, createWebHistory } from 'vue-router'

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'home', component: () => import('../demos/RouterPermissionDemo.vue') },
    { path: '/dashboard', name: 'dashboard', component: () => import('../demos/RouterPermissionDemo.vue'), meta: { permission: 'dashboard:view' } },
    { path: '/report', name: 'report', component: () => import('../demos/RouterPermissionDemo.vue'), meta: { permission: 'report:view' } },
    { path: '/admin', name: 'admin', component: () => import('../demos/RouterPermissionDemo.vue'), meta: { permission: 'admin:view' } },
  ],
})
