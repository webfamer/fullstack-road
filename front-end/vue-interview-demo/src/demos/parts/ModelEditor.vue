<script setup lang="ts">
defineProps<{
  title: string
  visible: boolean
}>()

const emit = defineEmits<{
  (event: 'update:title', value: string): void
  (event: 'update:visible', value: boolean): void
}>()
</script>

<template>
  <div class="form-stack">
    <label>
      子组件修改 title
      <input :value="title" @input="emit('update:title', ($event.target as HTMLInputElement).value)" />
    </label>
    <label class="checkline">
      <input :checked="visible" type="checkbox" @change="emit('update:visible', ($event.target as HTMLInputElement).checked)" />
      visible
    </label>
  </div>
</template>
