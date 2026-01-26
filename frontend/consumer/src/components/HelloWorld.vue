<script setup lang="ts">
defineProps<{ msg: string }>()
</script>

<template>
  <div class="greetings">
    <h1 class="green">{{ msg }}</h1>
    <h3>
      你已成功创建前端页面 🎉
      现在可以继续完善“区块链可信溯源 + 绿色食品交易”的业务功能。
    </h3>
  </div>
</template>

<style scoped>
h1 { font-weight: 800; font-size: 2.2rem; top: -10px; }
h3 { font-size: 1.1rem; color: var(--muted); line-height: 1.6; }
.greetings h1, .greetings h3 { text-align: center; }
@media (min-width: 1024px) {
  .greetings h1, .greetings h3 { text-align: left; }
}
</style>
