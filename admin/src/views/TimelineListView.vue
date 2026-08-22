<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { RouterLink } from 'vue-router';
import AdminNav from '../components/AdminNav.vue';
import { getAdminTimeline, deleteTimelineItem, type TimelineItem } from '../api/timeline';

const items = ref<TimelineItem[]>([]);
const loading = ref(true);

onMounted(async () => {
  try {
    items.value = await getAdminTimeline();
  } finally {
    loading.value = false;
  }
});

async function handleDelete(item: TimelineItem) {
  if (!confirm(`确定删除时间线「${item.title}」吗？`)) return;
  await deleteTimelineItem(item.id!);
  items.value = items.value.filter((i) => i.id !== item.id);
}
</script>

<template>
  <div class="admin-container">
    <AdminNav title="时间线管理">
      <template #actions>
        <RouterLink class="btn btn-primary" to="/timeline/new">+ 新增时间线</RouterLink>
      </template>
    </AdminNav>

    <div v-if="loading" class="empty-state">加载中...</div>

    <div v-else-if="items.length === 0" class="empty-state">暂无时间线</div>

    <table v-else class="table card" style="padding: 0">
      <thead>
        <tr>
          <th style="width: 120px">阶段</th>
          <th>标题</th>
          <th>详情</th>
          <th style="width: 80px">排序</th>
          <th style="width: 140px">操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in items" :key="item.id">
          <td>{{ item.time }}</td>
          <td>{{ item.title }}</td>
          <td>{{ item.detail }}</td>
          <td>{{ item.sortOrder }}</td>
          <td>
            <RouterLink class="btn btn-sm" :to="`/timeline/${item.id}/edit`">编辑</RouterLink>
            <button class="btn btn-sm btn-danger" @click="handleDelete(item)">删除</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
