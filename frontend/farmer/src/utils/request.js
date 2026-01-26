import axios from 'axios'

const request = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  timeout: 5000
})

request.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    console.error('请求出错：', error)
    return Promise.reject(error)
  }
)

request.interceptors.response.use(
  (response) => response.data,
  (error) => {
    let message = '请求失败，请稍后重试'
    if (error.response) {
      const status = error.response.status
      if (status === 401) {
        message = '登录已过期，请重新登录'
        localStorage.removeItem('isLogin')
        localStorage.removeItem('userRole')
        window.location.href = '/login'
      } else if (status === 403) {
        message = '无权限访问'
      } else if (status === 500) {
        message = '服务器内部错误'
      }
    } else if (error.request) {
      message = '网络异常，请检查网络'
    }
    alert(message)
    return Promise.reject(error)
  }
)

export default request