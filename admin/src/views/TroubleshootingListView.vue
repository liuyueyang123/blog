<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { RouterLink } from 'vue-router';
import AdminNav from '../components/AdminNav.vue';
import { getAdminTroubleshooting, deleteTroubleshooting, type TroubleshootingCase } from '../api/troubleshooting';

const cases = ref<TroubleshootingCase[]>([]);
const loading = ref(true);

onMounted(async () => {
  try {
    cases.value = await getAdminTroubleshooting();
  } finally {
    loading.value = false;
  }
});

async function handleDelete(item: TroubleshootingCase) {
  if (!confirm(`确定删除案例「${item.title}」吗？`)) return;
  await deleteTroubleshooting(item.id!);
  cases.value = cases.value.filter((c) => c.id !== item.id);
}
</script>

<template>
  <div class="admin-container">
    <AdminNav title="故障排查管理">
      <template #actions>
        <RouterLink class="btn btn-primary" to="/troubleshooting/new">+ 新增案例</RouterLink>
      </template>
    </AdminNav>

    <div v-if="loading" class="empty-state">加载中...</div>

    <div v-else-if="cases.length === 0" class="empty-state">暂无案例</div>

    <table v-else class="table card" style="padding: 0">
      <thead>
        <tr>
          <th>标题</th>
          <th>现象</th>
          <th>根因</th>
          <th>状态</th>
          <th style="width: 140px">操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in cases" :key="item.id">
          <td>{{ item.title }}</td>
          <td>{{ item.symptom }}</td>
          <td>{{ item.rootCause }}</td>
          <td>
            <span class="tag" :class="item.isPublished ? 'tag-published' : 'tag-draft'">
              {{ item.isPublished ? '已发布' : '草稿' }}
            </span>
          </td>
          <td>
            <RouterLink class="btn btn-sm" :to="`/troubleshooting/${item.id}/edit`">编辑</RouterLink>
            <button class="btn btn-sm btn-danger" @click="handleDelete(item)">删除</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
