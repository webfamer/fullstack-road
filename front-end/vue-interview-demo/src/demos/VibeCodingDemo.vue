<script setup lang="ts">
import { computed, ref } from 'vue'
import DemoCard from '../components/DemoCard.vue'

const requirement = ref('把报表字段配置生成可复用的表格 columns，并补齐类型和空值兜底')
const constraints = ref(['使用 TypeScript', '保留插槽扩展', '不能直接信任 AI 输出', '跑 lint 和自测'])

const prompt = computed(() => {
  return [
    '你是一个 Vue3 + TypeScript 前端助手。',
    `需求：${requirement.value}`,
    `约束：${constraints.value.join('；')}`,
    '请输出组件结构、类型定义、边界 case 和自测清单。',
  ].join('\n')
})
</script>

<template>
  <DemoCard
    title="Vibe Coding 面试怎么讲？"
    interview="不要说“AI 帮我写代码就完了”。要说：先拆需求和约束，再让 AI 生成，最后人工校验、重构、自测和 Review。"
  >
    <div class="grid two">
      <section class="mini-panel">
        <label>
          需求
          <textarea v-model="requirement" rows="4" />
        </label>
        <p class="notice">面试回答：AI 是提效工具，不是交付责任人；业务判断、边界校验、质量验证都要自己兜底。</p>
      </section>
      <section class="mini-panel">
        <h4>可复制 Prompt</h4>
        <pre>{{ prompt }}</pre>
      </section>
    </div>
  </DemoCard>
</template>
