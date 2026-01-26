<template>
  <div class="layout">
    <header class="topbar">
      <div class="brand">
        <img class="logo" src="@/assets/logo.svg" alt="平台标识" />
        <div class="brand-text">
          <div class="title">{{ titleText }}</div>
          <div class="subtitle">区块链可信溯源 · 绿色食品交易</div>
        </div>
      </div>

      <div class="actions">
        <div class="user" title="当前登录用户">{{ username || '已登录' }}</div>
        <button class="logout" @click="handleLogout">退出</button>
      </div>
    </header>

    <div class="layout-main">
      <main class="content">
        <slot />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps<{ title?: string }>()
const router = useRouter()

const titleText = computed(() => props.title || '绿色食品交易平台')
const username = ref(localStorage.getItem('username') || '')

const handleLogout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('isLogin')
  localStorage.removeItem('userRole')
  localStorage.removeItem('username')
  router.push('/login')
}
</script>

<style scoped>
.layout{ min-height:100vh; display:flex; flex-direction:column; }
.topbar{
  position: sticky;
  top: 0;
  z-index: 10;
  display:flex;
  align-items:center;
  justify-content:space-between;
  padding: 14px 18px;
  border-bottom: 1px solid var(--border);
  background: rgba(255,255,255,.74);
  backdrop-filter: blur(10px);
}

.brand{ display:flex; align-items:center; gap:12px; }
.logo{ width:34px; height:34px; filter: drop-shadow(0 6px 14px rgba(2,6,23,.10)); }
.brand-text .title{ font-weight:800; letter-spacing:.2px; }
.brand-text .subtitle{ font-size:12px; color: var(--muted); margin-top:2px; }

.actions{ display:flex; align-items:center; gap:10px; }
.user{
  max-width: 180px;
  padding: 8px 10px;
  border: 1px solid var(--border);
  border-radius: 12px;
  background: rgba(255,255,255,.76);
  color: var(--text);
  font-size: 13px;
  overflow:hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.logout{
  padding: 9px 12px;
  border-radius: 12px;
  border: 1px solid var(--border);
  background: rgba(15,23,42,.04);
  cursor:pointer;
  font-weight: 600;
}
.logout:hover{ background: rgba(15,23,42,.06); transform: translateY(-1px); }
.layout-main{ flex:1; padding: 18px; }
.content{ max-width: 1200px; margin: 0 auto; }
@media (max-width: 720px){
  .layout-main{ padding: 12px; }
  .content{ max-width: 100%; }
  .user{ display:none; }
}
</style>
