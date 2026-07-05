<script setup lang="ts">
defineProps<{
  title: string
  interview: string
}>()
</script>

<template>
  <article class="demo-card">
    <header>
      <span class="eyebrow">面试问法</span>
      <h3>{{ title }}</h3>
      <p>{{ interview }}</p>
    </header>
    <slot />
  </article>
</template>
