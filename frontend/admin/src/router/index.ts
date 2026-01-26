import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Home from '../views/Home.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/login'
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/register',
      name: 'register',
      component: Register,
      props: { role: 'admin', title: '管理端注册' }
    },
    {
      path: '/home',
      name: 'home',
      component: Home,
      meta: { requiresAuth: true, role: 'admin' }
    }
  ]
})

router.beforeEach((to, from, next) => {
  const isLogin = localStorage.getItem('isLogin')
  const userRole = localStorage.getItem('userRole')

  if (to.meta.requiresAuth) {
    if (!isLogin) {
      next('/login')
    } else if (userRole !== to.meta.role) {
      next('/login')
    } else {
      next()
    }
  } else {
    next()
  }
})

export default router