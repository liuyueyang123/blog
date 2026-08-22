<script setup lang="ts">
import { computed } from 'vue';
import { useRoute, RouterLink } from 'vue-router';
import { useArticle } from '../composables/useArticles';
import { renderMarkdown } from '../utils/markdown';

const route = useRoute();
const slug = route.params.slug as string;
const { article } = useArticle(slug);

const rendered = computed(() => renderMarkdown(article.value?.content ?? ''));
</script>

<template>
  <article class="page">
    <div v-if="article" class="container article-detail">
      <RouterLink class="back-link" to="/articles">返回文章列表</RouterLink>
      <p class="eyebrow">{{ article.category }} · {{ article.date }} · {{ article.readTime }}</p>
      <h1 class="section-title">{{ article.title }}</h1>
      <p class="section-copy">{{ article.excerpt }}</p>

      <div class="article-layout">
        <div class="content card">
          <div class="markdown-body" v-html="rendered.html"></div>
        </div>

        <aside v-if="rendered.headings.length" class="toc card">
          <h2 class="toc-title">目录</h2>
          <nav class="toc-list">
            <a
              v-for="h in rendered.headings"
              :key="h.id"
              :href="`#${h.id}`"
              class="toc-link"
              :style="{ paddingLeft: `${(h.level - 2) * 14 + 10}px` }"
            >{{ h.text }}</a>
          </nav>
        </aside>
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

.article-layout {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 260px;
  gap: 24px;
  align-items: start;
  margin-top: 34px;
}

.content {
  max-width: 820px;
  padding: 34px;
}

/* 目录（TOC）小框框，右侧 sticky */
.toc {
  position: sticky;
  top: 104px;
  max-height: calc(100vh - 130px);
  overflow-y: auto;
  padding: 18px 16px;
}

.toc-title {
  margin: 0 0 12px;
  color: var(--color-text-primary);
  font-size: 14px;
  font-weight: 700;
  letter-spacing: 0.04em;
}

.toc-list {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.toc-link {
  display: block;
  padding: 6px 10px;
  border-radius: var(--radius-small);
  color: var(--color-text-secondary);
  font-size: 13px;
  line-height: 1.4;
  transition: background 0.15s ease, color 0.15s ease;
}

.toc-link:hover {
  color: var(--color-text-primary);
  background: rgba(120, 224, 210, 0.1);
}

@media (max-width: 900px) {
  .article-layout {
    grid-template-columns: 1fr;
  }

  .toc {
    display: none;
  }
}
</style>
