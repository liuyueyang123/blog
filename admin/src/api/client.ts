/**
 * Axios 实例 — 自动携带 JWT，401 时跳转登录
 */
import axios from 'axios';
import { getToken, clearToken } from '../stores/auth';

const apiClient = axios.create({
  baseURL: '/api/v1',
  timeout: 10000,
});

// 请求拦截器：携带 token
apiClient.interceptors.request.use((config) => {
  const token = getToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// 响应拦截器：401 时清除 token 并跳转登录
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      clearToken();
      if (window.location.pathname !== '/login') {
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  },
);

export default apiClient;
