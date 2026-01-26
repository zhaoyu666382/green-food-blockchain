<template>
  <Layout title="用户端">
    <div class="page">
      <section class="card">
        <div class="card-title">商品列表</div>
        <div class="toolbar">
          <input v-model="keyword" class="input" placeholder="按名称/分类搜索" @keyup.enter="loadProducts" />
          <button class="btn" @click="loadProducts">查询</button>
        </div>

        <div v-if="loading" class="muted">正在加载...</div>
        <div v-else class="grid">
          <div v-for="p in products" :key="p.id" class="item">
            <div class="name">{{ p.name }}</div>
            <div class="meta">分类：{{ p.category || '未填写' }}</div>
            <div class="meta">产地：{{ p.origin || '未填写' }}</div>
            <div class="meta">价格：{{ p.price }} / {{ p.unit }}</div>
            <div class="meta">库存：{{ p.stock }}</div>
          </div>
        </div>
      </section>

      <section class="card">
        <div class="card-title">溯源查询</div>
        <div class="toolbar">
          <input v-model="batchNumber" class="input" placeholder="请输入批次号（batch_number）" @keyup.enter="queryTrace" />
          <button class="btn" @click="queryTrace">查询</button>
        </div>

        <div v-if="traceLoading" class="muted">正在查询...</div>
        <div v-else-if="timeline" class="timeline">
          <div class="muted">
            链完整性校验：<b>{{ timeline.chain_valid ? '通过' : '未通过' }}</b>
          </div>

          <div class="subcard">
            <div class="sub-title">产品信息</div>
            <div class="row">名称：{{ timeline.product?.name }}</div>
            <div class="row">分类：{{ timeline.product?.category || '未填写' }}</div>
            <div class="row">产地：{{ timeline.product?.origin || '未填写' }}</div>
            <div class="row">批次号：{{ timeline.batch?.batch_number }}</div>
            <div class="row">链上哈希：{{ timeline.batch?.blockchain_hash || '无' }}</div>
          </div>

          <div class="subcard">
            <div class="sub-title">溯源事件（按时间排序）</div>
            <div v-if="timeline.events.length === 0" class="muted">暂无事件记录</div>
            <div v-else class="events">
              <div v-for="e in timeline.events" :key="e.id" class="event">
                <div class="event-head">
                  <span class="tag">{{ toEventText(e.event_type) }}</span>
                  <span class="time">{{ formatTime(e.event_time) }}</span>
                </div>
                <div class="row">地点：{{ e.location || '未填写' }}</div>
                <div class="row">操作人：{{ e.operator || '未填写' }}</div>
                <div class="row" v-if="e.temperature !== null && e.temperature !== undefined">温度：{{ e.temperature }}℃</div>
                <div class="row" v-if="e.humidity !== null && e.humidity !== undefined">湿度：{{ e.humidity }}%</div>
                <div class="row" v-if="e.description">说明：{{ e.description }}</div>
                <div class="row muted">链上哈希：{{ e.blockchain_hash || '无' }}</div>
              </div>
            </div>
          </div>
        </div>

        <div v-else class="muted">请输入批次号进行查询</div>
      </section>
    </div>
  </Layout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import Layout from '@/components/Layout.vue'
import request from '@/utils/request'

const products = ref<any[]>([])
const loading = ref(false)
const keyword = ref('')

const batchNumber = ref('')
const traceLoading = ref(false)
const timeline = ref<any | null>(null)

const loadProducts = async () => {
  loading.value = true
  try {
    const res = await request.get('/api/products', { params: { q: keyword.value || undefined } })
    products.value = res
  } finally {
    loading.value = false
  }
}

const queryTrace = async () => {
  if (!batchNumber.value) return
  traceLoading.value = true
  timeline.value = null
  try {
    const res = await request.get(`/api/trace/timeline/${encodeURIComponent(batchNumber.value)}`)
    timeline.value = res
  } finally {
    traceLoading.value = false
  }
}

const formatTime = (t: string) => {
  try {
    return new Date(t).toLocaleString()
  } catch {
    return t
  }
}

const toEventText = (type: string) => {
  const map: Record<string, string> = {
    planting: '种植',
    fertilizing: '施肥',
    harvest: '采摘',
    inspection: '检测',
    transport: '运输',
    warehouse: '入库',
    sale: '销售'
  }
  return map[type] || type
}

onMounted(loadProducts)
</script>

<style scoped>
.page { display: flex; flex-direction: column; gap: 16px; }
.card{ background: rgba(255,255,255,.86); border:1px solid var(--border); border-radius: var(--radius2); padding:16px; box-shadow: var(--shadow2); backdrop-filter: blur(6px); }
.card-title{ font-size:16px; font-weight:800; margin-bottom:12px; display:flex; align-items:center; gap:10px; }
.toolbar{ display:flex; gap:10px; margin-bottom:12px; flex-wrap:wrap; align-items:center; }
.input{ flex:1; min-width:220px; padding:10px 12px; border:1px solid var(--border); border-radius:12px; background: rgba(255,255,255,.9); outline:none; }
.btn{ padding:10px 14px; border:none; border-radius:12px; background: linear-gradient(135deg, var(--primary), var(--primary-2)); color:#fff; cursor:pointer; font-weight:700; box-shadow: 0 10px 18px rgba(34,197,94,.20); transition: transform .12s, filter .12s; }
.btn:hover{ filter: brightness(1.02); transform: translateY(-1px); }
.btn:active{ transform: translateY(0); }
.muted{ color: var(--muted); font-size: 13px; }
.grid { display:grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 12px; }
.item { border: 1px solid #eee; border-radius: 8px; padding: 12px; }
.name { font-weight: 600; margin-bottom: 8px; }
.meta { color:#666; font-size: 13px; line-height: 1.6; }
.timeline { display:flex; flex-direction: column; gap: 12px; }
.subcard { border: 1px solid #eee; border-radius: 8px; padding: 12px; }
.sub-title { font-weight: 600; margin-bottom: 8px; }
.row { color:#444; font-size: 13px; line-height: 1.7; }
.events { display:flex; flex-direction: column; gap: 10px; }
.event { border-top: 1px dashed #eee; padding-top: 10px; }
.event:first-child { border-top: none; padding-top: 0; }
.event-head { display:flex; justify-content: space-between; align-items:center; margin-bottom: 6px; }
.tag { background: rgba(34,197,94,.10); color: var(--primary); padding: 2px 8px; border-radius: 999px; font-size: 12px; }
.time { color:#666; font-size: 12px; }
</style>
