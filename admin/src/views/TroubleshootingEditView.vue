<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter, RouterLink } from 'vue-router';
import { getAdminTroubleshooting, createTroubleshooting, updateTroubleshooting, type TroubleshootingPayload } from '../api/troubleshooting';

const route = useRoute();
const router = useRouter();

const caseId = computed(() => {
  const id = route.params.id;
  return id ? Number(id) : null;
});
const isEdit = computed(() => caseId.value !== null);

const form = ref({
  slug: '',
  title: '',
  symptom: '',
  process: '',
  tools: '', // comma-separated input
  root_cause: '',
  resolution: '',
  review: '',
  is_published: true,
  sort_order: 0,
});

const loading = ref(false);
const saving = ref(false);
const error = ref('');

onMounted(async () => {
  if (!isEdit.value) return;
  loading.value = true;
  try {
    const all = await getAdminTroubleshooting();
    const found = all.find((c) => c.id === caseId.value);
    if (found) {
      form.value.slug = found.slug;
      form.value.title = found.title;
      form.value.symptom = found.symptom;
      form.value.process = found.process;
      form.value.tools = found.tools.join(', ');
      form.value.root_cause = found.rootCause;
      form.value.resolution = found.resolution;
      form.value.review = found.review;
      form.value.is_published = found.isPublished ?? true;
      form.value.sort_order = found.sortOrder ?? 0;
    }
  } finally {
    loading.value = false;
  }
});

async function handleSave() {
  error.value = '';
  saving.value = true;
  const payload: TroubleshootingPayload = {
    slug: form.value.slug,
    title: form.value.title,
    symptom: form.value.symptom,
    process: form.value.process,
    tools: form.value.tools.split(',').map((t) => t.trim()).filter((t) => t !== ''),
    root_cause: form.value.root_cause,
    resolution: form.value.resolution,
    review: form.value.review,
    is_published: form.value.is_published,
    sort_order: form.value.sort_order,
  };
  try {
    if (isEdit.value) {
      await updateTroubleshooting(caseId.value!, payload);
    } else {
      await createTroubleshooting(payload);
    }
    router.push('/troubleshooting');
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
      <h1>{{ isEdit ? '编辑案例' : '新增案例' }}</h1>
      <RouterLink class="btn" to="/troubleshooting">返回列表</RouterLink>
    </header>

    <div v-if="loading" class="empty-state">加载中...</div>

    <form v-else class="card" @submit.prevent="handleSave">
      <div class="form-row">
        <div class="form-group">
          <label>Slug（URL 标识）</label>
          <input v-model="form.slug" required placeholder="prometheus-port-still-used" />
        </div>
        <div class="form-group">
          <label>标题</label>
          <input v-model="form.title" required placeholder="案例标题" />
        </div>
      </div>

      <div class="form-group">
        <label>现象</label>
        <textarea v-model="form.symptom" placeholder="问题发生时看到的现象"></textarea>
      </div>

      <div class="form-group">
        <label>排查过程</label>
        <textarea v-model="form.process" placeholder="按顺序描述排查步骤"></textarea>
      </div>

      <div class="form-group">
        <label>工具（逗号分隔）</label>
        <input v-model="form.tools" placeholder="systemctl, journalctl, ps, ss" />
      </div>

      <div class="form-group">
        <label>根因</label>
        <textarea v-model="form.root_cause" placeholder="问题根因"></textarea>
      </div>

      <div class="form-group">
        <label>解决方案</label>
        <textarea v-model="form.resolution" placeholder="解决过程"></textarea>
      </div>

      <div class="form-group">
        <label>复盘</label>
        <textarea v-model="form.review" placeholder="复盘与经验总结"></textarea>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label>排序（越小越靠前）</label>
          <input v-model.number="form.sort_order" type="number" />
        </div>
        <div class="form-group">
          <label>发布状态</label>
          <select v-model="form.is_published">
            <option :value="true">已发布</option>
            <option :value="false">草稿</option>
          </select>
        </div>
      </div>

      <div style="display: flex; gap: 12px; margin-top: 8px">
        <button class="btn btn-primary" type="submit" :disabled="saving">
          {{ saving ? '保存中...' : '保存' }}
        </button>
        <RouterLink class="btn" to="/troubleshooting">取消</RouterLink>
      </div>
      <p v-if="error" class="error-msg">{{ error }}</p>
    </form>
  </div>
</template>
