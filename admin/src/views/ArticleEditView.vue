<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter, RouterLink } from 'vue-router';
import { getAdminArticles, createArticle, updateArticle } from '../api/articles';
import { renderMarkdown } from '../utils/markdown';
import { uploadImage } from '../api/upload';

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
  content: '', // Markdown 原文
  is_published: true,
  sort_order: 0,
});

const loading = ref(false);
const saving = ref(false);
const error = ref('');

const previewHtml = computed(() => renderMarkdown(form.value.content));

const fileInput = ref<HTMLInputElement | null>(null);
const textareaRef = ref<HTMLTextAreaElement | null>(null);
const uploading = ref(false);

function triggerUpload() {
  fileInput.value?.click();
}

function insertAtCursor(text: string) {
  const ta = textareaRef.value;
  if (!ta) {
    form.value.content += `\n${text}`;
    return;
  }
  const start = ta.selectionStart ?? form.value.content.length;
  const end = ta.selectionEnd ?? start;
  form.value.content =
    form.value.content.slice(0, start) + text + form.value.content.slice(end);
  requestAnimationFrame(() => {
    ta.focus();
    const pos = start + text.length;
    ta.setSelectionRange(pos, pos);
  });
}

async function onFileChange(e: Event) {
  const input = e.target as HTMLInputElement;
  const file = input.files?.[0];
  if (!file) return;
  uploading.value = true;
  error.value = '';
  try {
    const url = await uploadImage(file);
    insertAtCursor(`![${file.name.replace(/[\[\]]/g, '')}](${url})`);
  } catch (e: any) {
    error.value = e.response?.data?.detail || '图片上传失败';
  } finally {
    uploading.value = false;
    input.value = '';
  }
}

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
      form.value.content = found.content;
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
    content: form.value.content,
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
        <label>正文（Markdown，左侧编写 / 右侧实时预览）</label>
        <div class="md-editor-toolbar">
          <button type="button" class="btn btn-sm" :disabled="uploading" @click="triggerUpload">
            {{ uploading ? '上传中...' : '🖼 上传图片' }}
          </button>
          <input
            ref="fileInput"
            type="file"
            accept="image/jpeg,image/png,image/gif,image/webp"
            class="hidden-file"
            @change="onFileChange"
          />
        </div>
        <div class="md-editor">
          <textarea
            ref="textareaRef"
            v-model="form.content"
            class="md-editor-input"
            placeholder="用 Markdown 编写正文，支持 ## 标题、**加粗**、- 列表、``` 代码块等"
          ></textarea>
          <div class="md-editor-preview markdown-preview" v-html="previewHtml"></div>
        </div>
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

<style scoped>
.md-editor-toolbar {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.hidden-file {
  display: none;
}

.md-editor {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  align-items: stretch;
}

.md-editor-input {
  width: 100%;
  min-height: 460px;
  padding: 12px;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  background: rgba(10, 14, 28, 0.6);
  color: var(--text-primary);
  font-family: "JetBrains Mono", "Fira Code", Consolas, monospace;
  font-size: 13px;
  line-height: 1.6;
  resize: vertical;
}

.md-editor-input:focus {
  outline: none;
  border-color: var(--accent);
}

.md-editor-preview {
  min-height: 460px;
  max-height: 660px;
  overflow-y: auto;
  padding: 14px 16px;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  background: var(--surface);
}

@media (max-width: 720px) {
  .md-editor {
    grid-template-columns: 1fr;
  }
}
</style>
