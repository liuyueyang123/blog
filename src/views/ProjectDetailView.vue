<script setup lang="ts">
import { computed } from 'vue';
import { useRoute, RouterLink } from 'vue-router';
import { Github } from 'lucide-vue-next';
import { projects } from '../data/projects';

const route = useRoute();
const project = computed(() => projects.find((item) => item.slug === route.params.slug));
</script>

<template>
  <section class="page">
    <div v-if="project" class="container detail">
      <RouterLink class="back-link" to="/projects">返回项目列表</RouterLink>
      <p class="eyebrow">Project Detail</p>
      <h1 class="section-title">{{ project.title }}</h1>
      <p class="section-copy">{{ project.overview }}</p>
      <ul class="tag-list">
        <li v-for="tag in project.tags" :key="tag" class="tag">{{ tag }}</li>
      </ul>
      <div class="detail-grid">
        <article class="card">
          <h2>我的工作</h2>
          <p>{{ project.role }}</p>
        </article>
        <article class="card">
          <h2>量化结果</h2>
          <p>{{ project.result }}</p>
        </article>
      </div>
      <article class="card highlight-card">
        <h2>关键内容</h2>
        <ul>
          <li v-for="item in project.highlights" :key="item">{{ item }}</li>
        </ul>
        <a :href="project.githubUrl" target="_blank" rel="noreferrer">
          <Github :size="17" aria-hidden="true" /> GitHub 占位链接
        </a>
      </article>
    </div>
    <div v-else class="container page-header">
      <h1 class="section-title">没有找到这个项目</h1>
      <RouterLink class="back-link" to="/projects">返回项目列表</RouterLink>
    </div>
  </section>
</template>

<style scoped>
.detail {
  padding: 124px 0 var(--section-spacing);
}

.back-link {
  display: inline-block;
  margin-bottom: 22px;
  color: var(--color-accent);
  font-weight: 800;
}

.tag-list {
  margin-top: 26px;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 18px;
  margin-top: 30px;
}

.card {
  padding: 24px;
}

h2 {
  margin: 0 0 12px;
  font-size: 22px;
}

p,
li {
  color: var(--color-text-secondary);
  line-height: 1.75;
}

.highlight-card {
  margin-top: 18px;
}

.highlight-card a {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  margin-top: 16px;
  color: var(--color-accent);
  font-weight: 800;
}

@media (max-width: 760px) {
  .detail-grid {
    grid-template-columns: 1fr;
  }
}
</style>
