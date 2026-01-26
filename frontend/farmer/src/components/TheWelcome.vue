<script setup lang="ts">
import WelcomeItem from './WelcomeItem.vue'
import DocumentationIcon from './icons/IconDocumentation.vue'
import ToolingIcon from './icons/IconTooling.vue'
import EcosystemIcon from './icons/IconEcosystem.vue'
import CommunityIcon from './icons/IconCommunity.vue'
import SupportIcon from './icons/IconSupport.vue'
</script>

<template>
  <WelcomeItem>
    <template #icon><DocumentationIcon /></template>
    <template #heading>平台定位</template>
    面向“绿色食品交易 + 区块链可信溯源”的一体化平台：把<strong>批次</strong>和<strong>关键事件</strong>写入链上，
    让数据可验证、可追溯、难篡改。
  </WelcomeItem>

  <WelcomeItem>
    <template #icon><EcosystemIcon /></template>
    <template #heading>核心流程</template>
    农户创建产品 → 创建批次 → 记录种植/采摘/检测/运输等事件 → 用户按批次查询溯源 → 完成交易与评价。
  </WelcomeItem>

  <WelcomeItem>
    <template #icon><ToolingIcon /></template>
    <template #heading>快速开始</template>
    先启动后端服务，再分别运行管理端、农户端、用户端前端项目。进入登录页后按角色注册账号即可体验完整流程。
  </WelcomeItem>

  <WelcomeItem>
    <template #icon><CommunityIcon /></template>
    <template #heading>绿色与可信</template>
    支持有机认证标记、产地信息、检测记录与链上哈希展示，帮助建立品牌信任、提升复购与溢价能力。
  </WelcomeItem>

  <WelcomeItem>
    <template #icon><SupportIcon /></template>
    <template #heading>提示</template>
    演示时可先用农户端创建“白菜/菠菜”等样例产品与批次，再到用户端输入批次号查看时间线与链上校验结果。
  </WelcomeItem>
</template>
