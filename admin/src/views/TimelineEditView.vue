<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter, RouterLink } from 'vue-router';
import { getAdminTimeline, createTimelineItem, updateTimelineItem, type TimelinePayload } from '../api/timeline';

const route = useRoute();
const router = useRouter();

const itemId = computed(() => {
  const id = route.params.id;
  return id ? Number(id) : null;
});
const isEdit = computed(() => itemId.value !== null);

const form = ref({
  time: '',
  title: '',
  detail: '',
  sort_order: 0,
});

const loading = ref(false);
const saving = ref(false);
const error = ref('');

onMounted(async () => {
  if (!isEdit.value) return;
  loading.value = true;
  try {
    const all = await getAdminTimeline();
    const found = all.find((i) => i.id === itemId.value);
    if (found) {
      form.value.time = found.time;
      form.value.title = found.title;
      form.value.detail = found.detail;
      form.value.sort_order = found.sortOrder ?? 0;
    }
  } finally {
    loading.value = false;
  }
});

async function handleSave() {
  error.value = '';
  saving.value = true;
  const payload: TimelinePayload = {
    time: form.value.time,
    title: form.value.title,
    detail: form.value.detail,
    sort_order: form.value.sort_order,
  };
  try {
    if (isEdit.value) {
      await updateTimelineItem(itemId.value!, payload);
    } else {
      await createTimelineItem(payload);
    }
    router.push('/timeline');
  } catch (e: any) {
    error.value = e.response?.data?.detail || '保存失败';
  } finally {
    saving.value = false;
  }
}
</script>

<template>
  <div class="admin-container">
    <header class="admin-header">
      <h1>{{ isEdit ? '编辑时间线' : '新增时间线' }}</h1>
      <RouterLink class="btn" to="/timeline">返回列表</RouterLink>
    </header>

    <div v-if="loading" class="empty-state">加载中...</div>

    <form v-else class="card" @submit.prevent="handleSave">
      <div class="form-row">
        <div class="form-group">
          <label>阶段标签</label>
          <input v-model="form.time" placeholder="阶段 01" />
        </div>
        <div class="form-group">
          <label>排序（越小越靠前）</label>
          <input v-model.number="form.sort_order" type="number" />
        </div>
      </div>

      <div class="form-group">
        <label>标题</label>
        <input v-model="form.title" required placeholder="时间线标题" />
      </div>

      <div class="form-group">
        <label>详情</label>
        <textarea v-model="form.detail" placeholder="一句话描述这一阶段"></textarea>
      </div>

      <div style="display: flex; gap: 12px; margin-top: 8px">
        <button class="btn btn-primary" type="submit" :disabled="saving">
          {{ saving ? '保存中...' : '保存' }}
        </button>
        <RouterLink class="btn" to="/timeline">取消</RouterLink>
      </div>
      <p v-if="error" class="error-msg">{{ error }}</p>
    </form>
  </div>
</template>
