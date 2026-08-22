<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter, RouterLink } from 'vue-router';
import { getAdminArticles, createArticle, updateArticle } from '../api/articles';

const route = useRoute();
const router = useRouter();

const articleId = computed(() => {
  const id = route.params.id;
  return id ? Number(id) : null;
});
const isEdit = computed(() => articleId.value !== null);

const form = ref({
  slug: '',
  title: '',
  category: '',
  excerpt: '',
  date: new Date().toISOString().slice(0, 10),
  read_time: '5 min',
  content: '' as string, // textarea, split by newline into paragraphs
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
    // 从列表中找到对应文章（简单实现，后续可加 GET /admin/articles/{id}）
    const all = await getAdminArticles();
    const found = all.find((a) => a.id === articleId.value);
    if (found) {
      form.value.slug = found.slug;
      form.value.title = found.title;
      form.value.category = found.category;
      form.value.excerpt = found.excerpt;
      form.value.date = found.date;
      form.value.read_time = found.readTime;
      form.value.content = found.content.join('\n');
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
    category: form.value.category,
    excerpt: form.value.excerpt,
    date: form.value.date,
    read_time: form.value.read_time,
    content: form.value.content.split('\n').filter((p) => p.trim() !== ''),
    is_published: form.value.is_published,
    sort_order: form.value.sort_order,
  };
  try {
    if (isEdit.value) {
      await updateArticle(articleId.value!, payload);
    } else {
      await createArticle(payload);
    }
    router.push('/');
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
      <h1>{{ isEdit ? '编辑文章' : '新增文章' }}</h1>
      <RouterLink class="btn" to="/">返回列表</RouterLink>
    </header>

    <div v-if="loading" class="empty-state">加载中...</div>

    <form v-else class="card" @submit.prevent="handleSave">
      <div class="form-row">
        <div class="form-group">
          <label>Slug（URL 标识）</label>
          <input v-model="form.slug" required placeholder="my-article-slug" />
        </div>
        <div class="form-group">
          <label>分类</label>
          <input v-model="form.category" placeholder="SRE / AI / Linux ..." />
        </div>
      </div>

      <div class="form-group">
        <label>标题</label>
        <input v-model="form.title" required placeholder="文章标题" />
      </div>

      <div class="form-group">
        <label>摘要</label>
        <textarea v-model="form.excerpt" placeholder="一句话摘要"></textarea>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label>日期</label>
          <input v-model="form.date" type="date" required />
        </div>
        <div class="form-group">
          <label>阅读时长</label>
          <input v-model="form.read_time" placeholder="5 min" />
        </div>
      </div>

      <div class="form-group">
        <label>正文（每行一个段落）</label>
        <textarea v-model="form.content" rows="8" placeholder="第一段&#10;第二段&#10;第三段"></textarea>
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
        <RouterLink class="btn" to="/">取消</RouterLink>
      </div>
      <p v-if="error" class="error-msg">{{ error }}</p>
    </form>
  </div>
</template>
