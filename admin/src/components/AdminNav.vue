<script setup lang="ts">
import { RouterLink, useRouter } from 'vue-router';
import { clearToken } from '../stores/auth';

defineProps<{ title: string }>();

const router = useRouter();

function handleLogout() {
  clearToken();
  router.push('/login');
}
</script>

<template>
  <header class="admin-header">
    <div style="display: flex; align-items: center; gap: 22px">
      <h1>{{ title }}</h1>
      <nav class="admin-nav">
        <RouterLink to="/">文章</RouterLink>
        <RouterLink to="/projects">项目</RouterLink>
        <RouterLink to="/skills">技能</RouterLink>
        <RouterLink to="/troubleshooting">排障</RouterLink>
        <RouterLink to="/timeline">时间线</RouterLink>
        <RouterLink to="/profile">资料</RouterLink>
      </nav>
    </div>
    <div style="display: flex; gap: 10px">
      <slot name="actions" />
      <button class="btn" @click="handleLogout">退出</button>
    </div>
  </header>
</template>

<style scoped>
.admin-nav {
  display: flex;
  gap: 4px;
}

.admin-nav a {
  padding: 6px 14px;
  border-radius: var(--radius);
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 14px;
  font-weight: 600;
  transition: background 0.15s ease, color 0.15s ease;
}

.admin-nav a:hover {
  color: var(--text-primary);
  background: rgba(255, 255, 255, 0.05);
}

.admin-nav a.router-link-exact-active {
  color: var(--accent);
  background: rgba(120, 224, 210, 0.1);
}
</style>
