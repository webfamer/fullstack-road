<script setup lang="ts">
import { onActivated, onBeforeUnmount, onDeactivated, onMounted, onUnmounted, ref } from 'vue'

const props = defineProps<{
  mode: string
}>()

const emit = defineEmits<{
  (event: 'log', value: string): void
}>()

const count = ref(0)

onMounted(() => emit('log', `${props.mode}: mounted`))
onBeforeUnmount(() => emit('log', `${props.mode}: beforeUnmount`))
onUnmounted(() => emit('log', `${props.mode}: unmounted`))
onActivated(() => emit('log', `${props.mode}: activated`))
onDeactivated(() => emit('log', `${props.mode}: deactivated`))
</script>

<template>
  <div class="notice">
    <strong>{{ mode }}</strong>
    <p>内部状态 count：{{ count }}</p>
    <button @click="count++">增加内部状态</button>
  </div>
</template>
