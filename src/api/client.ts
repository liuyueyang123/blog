/**
 * Axios 实例 — 统一 HTTP 客户端
 * 开发环境通过 Vite proxy 转发 /api → http://localhost:8000
 */
import axios from 'axios'

const apiClient = axios.create({
  baseURL: '/api/v1',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 响应拦截器：统一处理错误
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    const message =
      error.response?.data?.detail ||
      error.response?.data?.message ||
      'Network error'
    console.error('[API Error]', message)
    return Promise.reject(error)
  },
)

export default apiClient
