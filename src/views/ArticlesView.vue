<script setup lang="ts">
import { useArticles } from '../composables/useArticles';

const { articles } = useArticles();
</script>

<template>
  <section class="page">
    <div class="container page-header">
      <p class="eyebrow">Articles</p>
      <h1 class="section-title">技术文章</h1>
      <p class="section-copy">第一版为静态模拟文章，主题覆盖 Linux、SRE、容器和 AI。</p>
    </div>
    <div class="container article-grid">
      <RouterLink
        v-for="article in articles"
        :key="article.slug"
        :to="`/articles/${article.slug}`"
        class="article-card card"
      >
        <span>{{ article.category }} · {{ article.date }}</span>
        <h2>{{ article.title }}</h2>
        <p>{{ article.excerpt }}</p>
        <em>{{ article.readTime }}</em>
      </RouterLink>
    </div>
  </section>
</template>

<style scoped>
.article-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 18px;
  padding-bottom: var(--section-spacing);
  perspective: 1200px;
}

.article-card {
  padding: 24px;
  transition:
    transform 190ms cubic-bezier(0.2, 0.9, 0.24, 1.25),
    border-color 190ms ease,
    box-shadow 190ms ease;
  will-change: transform;
}

.article-card:hover {
  transform: translateY(-5px) scale(1.018);
  border-color: rgba(120, 224, 210, 0.45);
}

.article-card:active {
  animation: article-pop 360ms cubic-bezier(0.2, 0.95, 0.24, 1.28);
}

.article-card span,
.article-card em {
  color: var(--color-accent);
  font-style: normal;
  font-size: 13px;
  font-weight: 800;
}

h2 {
  margin: 12px 0;
  font-size: 24px;
}

p {
  color: var(--color-text-secondary);
  line-height: 1.7;
}

@media (max-width: 760px) {
  .article-grid {
    grid-template-columns: 1fr;
  }
}

@media (prefers-reduced-motion: reduce) {
  .article-card,
  .article-card:hover {
    transform: none;
    animation: none;
  }
}
</style>
