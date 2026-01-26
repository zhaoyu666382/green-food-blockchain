<template>
  <Layout title="农户端">
    <div class="page">
      <section class="card">
        <div class="card-title">我的产品</div>
        <div class="toolbar">
          <button class="btn" @click="loadMine">刷新</button>
        </div>

        <div v-if="loading" class="muted">正在加载...</div>
        <div v-else class="grid">
          <div v-for="p in products" :key="p.id" class="item">
            <div class="name">{{ p.name }}</div>
            <div class="meta">分类：{{ p.category || '未填写' }}</div>
            <div class="meta">产地：{{ p.origin || '未填写' }}</div>
            <div class="meta">价格：{{ p.price }} / {{ p.unit }}</div>
            <div class="meta">库存：{{ p.stock }}</div>
            <div class="actions">
              <button class="btn2" @click="selectProduct(p)">选择</button>
            </div>
          </div>
        </div>
        <div v-if="selectedProduct" class="muted" style="margin-top:10px">
          当前已选择：{{ selectedProduct.name }}（产品ID：{{ selectedProduct.id }}）
        </div>
      </section>

      <section class="card">
        <div class="card-title">新增产品</div>
        <div class="form">
          <input class="input" v-model="newP.name" placeholder="名称" />
          <input class="input" v-model="newP.category" placeholder="分类（如：叶菜类）" />
          <input class="input" v-model="newP.origin" placeholder="产地（如：江西·南昌）" />
          <div class="row2">
            <input class="input" v-model="newP.unit" placeholder="单位（默认 kg）" />
            <input class="input" v-model.number="newP.price" type="number" placeholder="价格" />
            <input class="input" v-model.number="newP.stock" type="number" placeholder="库存" />
          </div>
          <textarea class="textarea" v-model="newP.description" placeholder="简介（可选）"></textarea>
          <label class="check">
            <input type="checkbox" v-model="newP.organic_certified" />
            有机认证
          </label>
          <button class="btn" @click="createProduct">提交</button>
        </div>
      </section>

      <section class="card">
        <div class="card-title">批次与溯源事件</div>

        <div class="toolbar">
          <input class="input" v-model="batchForm.batch_number" placeholder="批次号（唯一）" />
          <input class="input" v-model.number="batchForm.quantity" type="number" placeholder="数量" />
          <button class="btn" :disabled="!selectedProduct" @click="createBatch">
            创建批次
          </button>
          <button class="btn2" @click="loadBatches">刷新批次</button>
        </div>

        <div v-if="batches.length===0" class="muted">暂无批次</div>
        <div v-else class="list">
          <div v-for="b in batches" :key="b.id" class="subcard">
            <div class="sub-title">
              批次号：{{ b.batch_number }}
              <span class="muted">｜链上哈希：{{ b.blockchain_hash || '无' }}</span>
            </div>
            <div class="meta">产品ID：{{ b.product_id }}｜数量：{{ b.quantity }}｜创建：{{ formatTime(b.created_at) }}</div>

            <div class="toolbar" style="margin-top:10px">
              <select class="select" v-model="eventForm.event_type">
                <option value="planting">种植</option>
                <option value="fertilizing">施肥</option>
                <option value="harvest">采摘</option>
                <option value="inspection">检测</option>
                <option value="transport">运输</option>
                <option value="warehouse">入库</option>
                <option value="sale">销售</option>
              </select>
              <input class="input" v-model="eventForm.location" placeholder="地点（可选）" />
              <input class="input" v-model="eventForm.description" placeholder="说明（可选）" />
              <button class="btn2" @click="addEvent(b.id)">添加事件</button>
              <button class="btn2" @click="openTimeline(b.batch_number)">查看时间线</button>
            </div>
          </div>
        </div>
      </section>

      <section class="card" v-if="timeline">
        <div class="card-title">时间线预览</div>
        <div class="muted">链完整性校验：<b>{{ timeline.chain_valid ? '通过' : '未通过' }}</b></div>

        <div class="subcard" style="margin-top:10px">
          <div class="sub-title">产品信息</div>
          <div class="meta">名称：{{ timeline.product?.name }}</div>
          <div class="meta">分类：{{ timeline.product?.category || '未填写' }}</div>
          <div class="meta">产地：{{ timeline.product?.origin || '未填写' }}</div>
        </div>

        <div class="subcard" style="margin-top:10px">
          <div class="sub-title">事件列表</div>
          <div v-if="timeline.events.length===0" class="muted">暂无事件</div>
          <div v-else class="events">
            <div v-for="e in timeline.events" :key="e.id" class="event">
              <div class="event-head">
                <span class="tag">{{ toEventText(e.event_type) }}</span>
                <span class="time">{{ formatTime(e.event_time) }}</span>
              </div>
              <div class="meta">地点：{{ e.location || '未填写' }}｜操作人：{{ e.operator || '未填写' }}</div>
              <div class="meta" v-if="e.description">说明：{{ e.description }}</div>
              <div class="muted">链上哈希：{{ e.blockchain_hash || '无' }}</div>
            </div>
          </div>
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
const products = ref<any[]>([])
const batches = ref<any[]>([])
const selectedProduct = ref<any | null>(null)
const timeline = ref<any | null>(null)

const newP = ref<any>({
  name: '',
  category: '',
  origin: '',
  unit: 'kg',
  price: 0,
  stock: 0,
  description: '',
  organic_certified: false
})

const batchForm = ref({ batch_number: '', quantity: 0 })

const eventForm = ref<any>({
  event_type: 'inspection',
  location: '',
  description: ''
})

const loadMine = async () => {
  loading.value = true
  try {
    const res = await request.get('/api/products/mine')
    products.value = res
  } finally {
    loading.value = false
  }
}

const selectProduct = (p: any) => {
  selectedProduct.value = p
}

const createProduct = async () => {
  if (!newP.value.name) return alert('请填写产品名称')
  await request.post('/api/products', newP.value)
  alert('创建成功')
  newP.value = { name: '', category: '', origin: '', unit: 'kg', price: 0, stock: 0, description: '', organic_certified: false }
  await loadMine()
}

const createBatch = async () => {
  if (!selectedProduct.value) return alert('请先选择产品')
  if (!batchForm.value.batch_number) return alert('请填写批次号')
  await request.post('/api/batches', {
    product_id: selectedProduct.value.id,
    batch_number: batchForm.value.batch_number,
    quantity: batchForm.value.quantity || 0
  })
  alert('批次创建成功')
  batchForm.value = { batch_number: '', quantity: 0 }
  await loadBatches()
}

const loadBatches = async () => {
  const res = await request.get('/api/batches', { params: { mine: true } })
  batches.value = res
}

const addEvent = async (batch_id: number) => {
  await request.post('/api/trace/events', {
    batch_id,
    event_type: eventForm.value.event_type,
    event_time: new Date().toISOString(),
    location: eventForm.value.location || null,
    description: eventForm.value.description || null
  })
  alert('事件已添加')
  eventForm.value.location = ''
  eventForm.value.description = ''
}

const openTimeline = async (batchNumber: string) => {
  const res = await request.get(`/api/trace/timeline/${encodeURIComponent(batchNumber)}`)
  timeline.value = res
}

const formatTime = (t: string) => {
  try { return new Date(t).toLocaleString() } catch { return t }
}

const toEventText = (type: string) => {
  const map: Record<string, string> = {
    planting: '种植', fertilizing: '施肥', harvest: '采摘', inspection: '检测', transport: '运输', warehouse: '入库', sale: '销售'
  }
  return map[type] || type
}

onMounted(async () => {
  await loadMine()
  await loadBatches()
})
</script>

<style scoped>
.page { display:flex; flex-direction:column; gap:16px; }
.card{ background: rgba(255,255,255,.86); border:1px solid var(--border); border-radius: var(--radius2); padding:16px; box-shadow: var(--shadow2); backdrop-filter: blur(6px); }
.card-title{ font-size:16px; font-weight:800; margin-bottom:12px; display:flex; align-items:center; gap:10px; }
.toolbar{ display:flex; gap:10px; margin-bottom:12px; flex-wrap:wrap; align-items:center; }
.input{ flex:1; min-width:220px; padding:10px 12px; border:1px solid var(--border); border-radius:12px; background: rgba(255,255,255,.9); outline:none; }
.select{ padding:10px 12px; border:1px solid var(--border); border-radius:12px; background: rgba(255,255,255,.9); outline:none; }
.textarea{ width:100%; padding:10px 12px; border:1px solid var(--border); border-radius:12px; background: rgba(255,255,255,.9); outline:none; min-height:92px; resize: vertical; }
.btn{ padding:10px 14px; border:none; border-radius:12px; background: linear-gradient(135deg, var(--primary), var(--primary-2)); color:#fff; cursor:pointer; font-weight:700; box-shadow: 0 10px 18px rgba(34,197,94,.20); transition: transform .12s, filter .12s; }
.btn:hover{ filter: brightness(1.02); transform: translateY(-1px); }
.btn:active{ transform: translateY(0); }
.btn2{ padding:10px 14px; border-radius:12px; cursor:pointer; border:1px solid var(--border); background: rgba(15,23,42,.04); color: var(--text); font-weight:700; transition: transform .12s; }
.btn2:hover{ background: rgba(15,23,42,.06); transform: translateY(-1px); }
.muted{ color: var(--muted); font-size: 13px; }
.grid { display:grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap:12px; }
.item { border:1px solid #eee; border-radius:8px; padding:12px; }
.name { font-weight:600; margin-bottom:8px; }
.meta { color:#666; font-size:13px; line-height:1.6; }
.actions { margin-top:10px; }
.list { display:flex; flex-direction:column; gap:12px; }
.subcard { border:1px solid #eee; border-radius:8px; padding:12px; }
.sub-title { font-weight:600; margin-bottom:6px; }
.events { display:flex; flex-direction:column; gap:10px; margin-top:10px; }
.event { border-top:1px dashed #eee; padding-top:10px; }
.event:first-child { border-top:none; padding-top:0; }
.event-head { display:flex; justify-content:space-between; margin-bottom:6px; }
.tag { background: rgba(34,197,94,.10); color: var(--primary); padding:2px 8px; border-radius:999px; font-size:12px; }
.time { color:#666; font-size:12px; }
.form { display:flex; flex-direction:column; gap:10px; }
.row2 { display:flex; gap:8px; flex-wrap:wrap; }
.check { color:#444; font-size:14px; }
</style>
