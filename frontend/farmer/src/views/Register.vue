<template>
  <div class="auth-bg">
    <div class="auth-card">
      <div class="brand">
        <img class="logo" src="@/assets/logo.svg" alt="平台标识" />
        <div class="name">绿色食品交易平台</div>
        <div class="tagline">{{ roleLabel }} · 快速创建账号</div>
      </div>

      <h2>{{ roleLabel }}注册</h2>

      <form @submit.prevent="handleRegister">
        <div class="form-item">
          <label>用户名</label>
          <input v-model="form.username" type="text" placeholder="请输入用户名（不少于3位）" required />
        </div>

        <div class="form-item">
          <label>邮箱</label>
          <input v-model="form.email" type="email" placeholder="请输入邮箱" required />
        </div>

        <div class="form-item">
          <label>密码</label>
          <input v-model="form.password" type="password" placeholder="请输入密码（不少于6位）" required />
        </div>

        <button type="submit" class="primary-btn">注册</button>
      </form>

      <div class="tips">
        已有账号？
        <a href="#" @click.prevent="toLogin">返回登录</a>
      </div>

      <div class="footnote">注册后即可体验：链上溯源、批次管理、绿色认证与交易。</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import request from '@/utils/request'

const props = defineProps<{ role: string; title?: string }>()

const router = useRouter()
const form = ref({ username: '', email: '', password: '' })

const roleLabel = '农户端'

const handleRegister = async () => {
  await request.post('/api/auth/register', {
    username: form.value.username,
    email: form.value.email,
    password: form.value.password,
    role: props.role
  })
  alert('注册成功，请登录')
  router.push('/login')
}

const toLogin = () => router.push('/login')
</script>

<style scoped>
.auth-bg{
  width: 100vw;
  height: 100vh;
  display:flex;
  justify-content:center;
  align-items:center;
  padding: 18px;
}

.auth-card{
  width: min(460px, 92vw);
  padding: 26px 26px 22px;
  border-radius: 18px;
  border: 1px solid var(--border);
  background: rgba(255,255,255,.86);
  box-shadow: var(--shadow);
  backdrop-filter: blur(10px);
}

.brand{ display:flex; flex-direction:column; align-items:center; gap:6px; margin-bottom: 10px; }
.logo{ width: 46px; height: 46px; filter: drop-shadow(0 10px 18px rgba(2,6,23,.12)); }
.name{ font-weight: 900; letter-spacing:.3px; }
.tagline{ font-size: 12px; color: var(--muted); }

h2{ text-align:center; margin: 12px 0 18px; font-size: 18px; }

.form-item{ margin-bottom: 14px; }
label{ display:block; margin-bottom: 6px; color: var(--muted); font-size: 13px; }
input{
  width: 100%;
  padding: 11px 12px;
  border: 1px solid var(--border);
  border-radius: 12px;
  outline:none;
  background: rgba(255,255,255,.92);
}
input:focus{
  border-color: rgba(34,197,94,.55);
  box-shadow: 0 0 0 4px rgba(34,197,94,.14);
}

.primary-btn{
  width: 100%;
  padding: 11px 12px;
  border: none;
  border-radius: 12px;
  cursor:pointer;
  color: #fff;
  font-weight: 700;
  background: linear-gradient(135deg, var(--primary), var(--primary-2));
  box-shadow: 0 14px 22px rgba(34,197,94,.18);
  transition: transform .12s, filter .12s;
}
.primary-btn:hover{ filter: brightness(1.02); transform: translateY(-1px); }
.primary-btn:active{ transform: translateY(0); }

.tips{ margin-top: 14px; text-align:center; color: var(--muted); font-size: 13px; }
.tips a{ color: var(--primary); font-weight: 700; }
.footnote{ margin-top: 14px; font-size: 12px; color: rgba(15,23,42,.55); text-align:center; }
</style>
