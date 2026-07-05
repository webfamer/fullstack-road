import { defineStore } from 'pinia'

export type Role = 'visitor' | 'operator' | 'admin'

const permissionMap: Record<Role, string[]> = {
  visitor: ['dashboard:view'],
  operator: ['dashboard:view', 'report:view'],
  admin: ['dashboard:view', 'report:view', 'admin:view'],
}

export const useUserStore = defineStore('user', {
  state: () => ({
    role: 'operator' as Role,
    token: 'mock-token',
  }),
  getters: {
    permissions: (state) => permissionMap[state.role],
    isAdmin: (state) => state.role === 'admin',
  },
  actions: {
    switchRole(role: Role) {
      this.role = role
    },
    hasPermission(code?: unknown) {
      if (typeof code !== 'string') return true
      return this.permissions.includes(code)
    },
  },
})
