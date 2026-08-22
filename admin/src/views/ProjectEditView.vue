<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter, RouterLink } from 'vue-router';
import { getAdminProjects, createProject, updateProject } from '../api/projects';

const route = useRoute();
const router = useRouter();

const projectId = computed(() => {
  const id = route.params.id;
  return id ? Number(id) : null;
});
const isEdit = computed(() => projectId.value !== null);

const COVER_TONES = ['vision', 'terminal', 'depth', 'sre', 'web', 'default'];

const form = ref({
  slug: '',
  title: '',
  subtitle: '',
  cover_tone: 'default',
  tags: '',       // comma-separated input
  role: '',
  result: '',
  overview: '',
  highlights: '', // newline-separated input
  github_url: '',
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
    const all = await getAdminProjects();
    const found = all.find((p) => p.id === projectId.value);
    if (found) {
      form.value.slug = found.slug;
      form.value.title = found.title;
      form.value.subtitle = found.subtitle;
      form.value.cover_tone = found.coverTone;
      form.value.tags = found.tags.join(', ');
      form.value.role = found.role;
      form.value.result = found.result;
      form.value.overview = found.overview;
      form.value.highlights = found.highlights.join('\n');
      form.value.github_url = found.githubUrl;
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
  const payload = {
    slug: form.value.slug,
    title: form.value.title,
    subtitle: form.value.subtitle,
    cover_tone: form.value.cover_tone,
    tags: form.value.tags.split(',').map((t) => t.trim()).filter((t) => t !== ''),
    role: form.value.role,
    result: form.value.result,
    overview: form.value.overview,
    highlights: form.value.highlights.split('\n').map((h) => h.trim()).filter((h) => h !== ''),
    github_url: form.value.github_url,
    is_published: form.value.is_published,
    sort_order: form.value.sort_order,
  };
  try {
    if (isEdit.value) {
      await updateProject(projectId.value!, payload);
    } else {
      await createProject(payload);
    }
    router.push('/projects');
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
      <h1>{{ isEdit ? '编辑项目' : '新增项目' }}</h1>
      <RouterLink class="btn" to="/projects">返回列表</RouterLink>
    </header>

    <div v-if="loading" class="empty-state">加载中...</div>

    <form v-else class="card" @submit.prevent="handleSave">
      <div class="form-row">
        <div class="form-group">
          <label>Slug（URL 标识）</label>
          <input v-model="form.slug" required placeholder="my-project-slug" />
        </div>
        <div class="form-group">
          <label>封面色调</label>
          <select v-model="form.cover_tone">
            <option v-for="tone in COVER_TONES" :key="tone" :value="tone">{{ tone }}</option>
          </select>
        </div>
      </div>

      <div class="form-group">
        <label>标题</label>
        <input v-model="form.title" required placeholder="项目标题" />
      </div>

      <div class="form-group">
        <label>副标题</label>
        <input v-model="form.subtitle" placeholder="一句话副标题" />
      </div>

      <div class="form-group">
        <label>标签（逗号分隔）</label>
        <input v-model="form.tags" placeholder="Python, PyTorch, Flask" />
      </div>

      <div class="form-group">
        <label>项目概述</label>
        <textarea v-model="form.overview" placeholder="项目整体介绍"></textarea>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label>我的工作</label>
          <textarea v-model="form.role" placeholder="负责的内容"></textarea>
        </div>
        <div class="form-group">
          <label>量化结果</label>
          <textarea v-model="form.result" placeholder="达成的结果"></textarea>
        </div>
      </div>

      <div class="form-group">
        <label>关键内容（每行一条）</label>
        <textarea v-model="form.highlights" rows="4" placeholder="亮点一&#10;亮点二&#10;亮点三"></textarea>
      </div>

      <div class="form-group">
        <label>GitHub 链接</label>
        <input v-model="form.github_url" placeholder="https://github.com/..." />
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
        <RouterLink class="btn" to="/projects">取消</RouterLink>
      </div>
      <p v-if="error" class="error-msg">{{ error }}</p>
    </form>
  </div>
</template>
