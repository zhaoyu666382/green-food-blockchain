<template>
  <div class="auth-bg">
    <div class="auth-card">
      <div class="brand">
        <img class="logo" src="@/assets/logo.svg" alt="平台标识" />
        <div class="name">绿色食品交易平台</div>
        <div class="tagline">{{ roleLabel }} · 区块链可信溯源</div>
      </div>

      <h2>{{ roleLabel }}登录</h2>

      <form @submit.prevent="handleLogin">
        <div class="form-item">
          <label>用户名</label>
          <input v-model="form.username" type="text" placeholder="请输入用户名" required />
        </div>

        <div class="form-item">
          <label>密码</label>
          <input v-model="form.password" type="password" placeholder="请输入密码" required />
        </div>

        <button type="submit" class="primary-btn">登录</button>
      </form>

      <div class="tips">
        还没有账号？
        <a href="#" @click.prevent="toRegister">立即注册</a>
      </div>

      <div class="footnote">提示：平台将关键溯源信息上链存证，保障透明可信。</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import request from '@/utils/request'

const router = useRouter()
const form = ref({ username: '', password: '' })

const role = 'admin'
const roleLabel = '管理端'

const handleLogin = async () => {
  const body = new URLSearchParams()
  body.append('username', form.value.username)
  body.append('password', form.value.password)

  const res = await request.post('/api/auth/login', body, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
  })

  localStorage.setItem('token', res.access_token)
  localStorage.setItem('isLogin', 'true')
  localStorage.setItem('userRole', role)
  localStorage.setItem('username', form.value.username)

  router.push('/home')
}

const toRegister = () => router.push('/register')
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
  width: min(440px, 92vw);
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

@media (prefers-reduced-motion: reduce){
  .primary-btn{ transition:none; }
}
</style>
