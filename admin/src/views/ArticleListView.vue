<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { RouterLink } from 'vue-router';
import AdminNav from '../components/AdminNav.vue';
import { getAdminArticles, deleteArticle, type Article } from '../api/articles';

const articles = ref<Article[]>([]);
const loading = ref(true);

onMounted(async () => {
  try {
    articles.value = await getAdminArticles();
  } finally {
    loading.value = false;
  }
});

async function handleDelete(article: Article) {
  if (!confirm(`确定删除文章「${article.title}」吗？`)) return;
  await deleteArticle(article.id!);
  articles.value = articles.value.filter((a) => a.id !== article.id);
}
</script>

<template>
  <div class="admin-container">
    <AdminNav title="文章管理">
      <template #actions>
        <RouterLink class="btn btn-primary" to="/articles/new">+ 新增文章</RouterLink>
      </template>
    </AdminNav>

    <div v-if="loading" class="empty-state">加载中...</div>

    <div v-else-if="articles.length === 0" class="empty-state">暂无文章</div>

    <table v-else class="table card" style="padding: 0">
      <thead>
        <tr>
          <th>标题</th>
          <th>分类</th>
          <th>日期</th>
          <th>状态</th>
          <th style="width: 140px">操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="article in articles" :key="article.id">
          <td>{{ article.title }}</td>
          <td>{{ article.category }}</td>
          <td>{{ article.date }}</td>
          <td>
            <span class="tag" :class="article.isPublished ? 'tag-published' : 'tag-draft'">
              {{ article.isPublished ? '已发布' : '草稿' }}
            </span>
          </td>
          <td>
            <RouterLink class="btn btn-sm" :to="`/articles/${article.id}/edit`">编辑</RouterLink>
            <button class="btn btn-sm btn-danger" @click="handleDelete(article)">删除</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
