<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { login } from '../api/articles';
import { setToken } from '../stores/auth';

const router = useRouter();
const username = ref('');
const password = ref('');
const error = ref('');
const loading = ref(false);

async function handleLogin() {
  error.value = '';
  loading.value = true;
  try {
    const token = await login(username.value, password.value);
    setToken(token);
    router.push('/');
  } catch (e: any) {
    error.value = e.response?.data?.detail || '登录失败，请检查用户名和密码';
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <div class="login-wrap">
    <div class="login-card card">
      <h1>Yael Admin</h1>
      <p class="subtitle">后台管理系统</p>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="username">用户名</label>
          <input id="username" v-model="username" type="text" autocomplete="username" required />
        </div>
        <div class="form-group">
          <label for="password">密码</label>
          <input id="password" v-model="password" type="password" autocomplete="current-password" required />
        </div>
        <button class="btn btn-primary" type="submit" :disabled="loading" style="width: 100%; justify-content: center">
          {{ loading ? '登录中...' : '登录' }}
        </button>
        <p v-if="error" class="error-msg">{{ error }}</p>
      </form>
    </div>
  </div>
</template>
