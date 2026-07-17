<script setup lang="ts">
import { computed } from 'vue';
import { useRoute, RouterLink } from 'vue-router';
import { articles } from '../data/articles';

const route = useRoute();
const article = computed(() => articles.find((item) => item.slug === route.params.slug));
</script>

<template>
  <article class="page">
    <div v-if="article" class="container article-detail">
      <RouterLink class="back-link" to="/articles">返回文章列表</RouterLink>
      <p class="eyebrow">{{ article.category }} · {{ article.date }} · {{ article.readTime }}</p>
      <h1 class="section-title">{{ article.title }}</h1>
      <p class="section-copy">{{ article.excerpt }}</p>
      <div class="content card">
        <p v-for="paragraph in article.content" :key="paragraph">{{ paragraph }}</p>
      </div>
    </div>
    <div v-else class="container page-header">
      <h1 class="section-title">没有找到这篇文章</h1>
      <RouterLink class="back-link" to="/articles">返回文章列表</RouterLink>
    </div>
  </article>
</template>

<style scoped>
.article-detail {
  padding: 124px 0 var(--section-spacing);
}

.back-link {
  display: inline-block;
  margin-bottom: 22px;
  color: var(--color-accent);
  font-weight: 800;
}

.content {
  max-width: 820px;
  margin-top: 34px;
  padding: 30px;
}

.content p {
  color: var(--color-text-secondary);
  font-size: 18px;
  line-height: 1.9;
}
</style>
