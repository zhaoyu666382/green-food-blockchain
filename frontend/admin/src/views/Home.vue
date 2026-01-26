<template>
  <Layout title="管理端">
    <div class="page">
      <section class="card">
        <div class="card-title">系统概览</div>
        <div class="toolbar">
          <button class="btn" @click="loadStats">刷新</button>
        </div>

        <div v-if="loading" class="muted">正在加载...</div>
        <div v-else class="stats">
          <div class="stat">
            <div class="num">{{ stats.users }}</div>
            <div class="label">用户数</div>
          </div>
          <div class="stat">
            <div class="num">{{ stats.products }}</div>
            <div class="label">产品数</div>
          </div>
          <div class="stat">
            <div class="num">{{ stats.batches }}</div>
            <div class="label">批次数</div>
          </div>
          <div class="stat">
            <div class="num">{{ stats.events }}</div>
            <div class="label">事件数</div>
          </div>
        </div>
      </section>

      <section class="card">
        <div class="card-title">用户列表（只读）</div>
        <div class="toolbar">
          <input class="input" v-model="q" placeholder="按用户名/邮箱搜索" @keyup.enter="loadUsers" />
          <button class="btn" @click="loadUsers">查询</button>
        </div>

        <div v-if="usersLoading" class="muted">正在加载...</div>
        <div v-else class="table">
          <div class="thead">
            <div>用户名</div><div>邮箱</div><div>角色</div><div>状态</div><div>创建时间</div>
          </div>
          <div v-for="u in users" :key="u.id" class="tr">
            <div>{{ u.username }}</div>
            <div>{{ u.email }}</div>
            <div>{{ toRoleText(u.role) }}</div>
            <div>{{ u.is_active ? '启用' : '停用' }}</div>
            <div>{{ formatTime(u.created_at) }}</div>
          </div>
          <div v-if="users.length===0" class="muted" style="margin-top:10px">暂无数据</div>
        </div>
      </section>
    </div>
  </Layout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import Layout from '@/components/Layout.vue'
import request from '@/utils/request'

const loading = ref(false)
const usersLoading = ref(false)
const stats = ref<any>({ users: 0, products: 0, batches: 0, events: 0 })

const q = ref('')
const users = ref<any[]>([])

const loadStats = async () => {
  loading.value = true
  try {
    const res = await request.get('/api/admin/stats')
    stats.value = res
  } finally {
    loading.value = false
  }
}

const loadUsers = async () => {
  usersLoading.value = true
  try {
    const res = await request.get('/api/admin/users', { params: { q: q.value || undefined } })
    users.value = res
  } finally {
    usersLoading.value = false
  }
}

const formatTime = (t: string) => {
  try { return new Date(t).toLocaleString() } catch { return t }
}

const toRoleText = (role: string) => {
  const map: Record<string, string> = { admin: '管理员', farmer: '农户', consumer: '消费者' }
  return map[role] || role
}

onMounted(async () => {
  await loadStats()
  await loadUsers()
})
</script>

<style scoped>
.page { display:flex; flex-direction:column; gap:16px; }
.card{ background: rgba(255,255,255,.86); border:1px solid var(--border); border-radius: var(--radius2); padding:16px; box-shadow: var(--shadow2); backdrop-filter: blur(6px); }
.card-title{ font-size:16px; font-weight:800; margin-bottom:12px; display:flex; align-items:center; gap:10px; }
.toolbar{ display:flex; gap:10px; margin-bottom:12px; flex-wrap:wrap; align-items:center; }
.input{ flex:1; min-width:220px; padding:10px 12px; border:1px solid var(--border); border-radius:12px; background: rgba(255,255,255,.9); outline:none; }
.btn{ padding:10px 14px; border:none; border-radius:12px; background: linear-gradient(135deg, var(--primary), var(--primary-2)); color:#fff; cursor:pointer; font-weight:700; box-shadow: 0 10px 18px rgba(34,197,94,.20); transition: transform .12s, filter .12s; }
.btn:hover{ filter: brightness(1.02); transform: translateY(-1px); }
.btn:active{ transform: translateY(0); }
.muted{ color: var(--muted); font-size: 13px; }
.stats { display:grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap:12px; }
.stat { border:1px solid #eee; border-radius:8px; padding:14px; text-align:center; }
.num { font-size:28px; font-weight:700; color:#333; }
.label { margin-top:6px; color:#666; font-size:13px; }
.table { border:1px solid #eee; border-radius:8px; overflow:hidden; }
.thead, .tr { display:grid; grid-template-columns: 1.2fr 2fr 1fr 1fr 1.5fr; gap: 10px; padding:10px 12px; }
.thead { background:#f5f7fa; font-weight:600; color:#333; }
.tr { border-top:1px solid #eee; color:#444; font-size:13px; }
</style>
