<script setup lang="ts">
defineProps<{
  logs: string[]
}>()
</script>

<template>
  <section class="log-panel">
    <strong>运行日志</strong>
    <ol>
      <li v-for="(log, index) in logs" :key="`${log}-${index}`">{{ log }}</li>
    </ol>
  </section>
</template>
