<script setup lang="ts">
import { Github } from 'lucide-vue-next';
import type { Project } from '../../types/content';

defineProps<{ project: Project }>();
</script>

<template>
  <article class="project-card card" :class="`tone-${project.coverTone}`" data-reveal>
    <RouterLink class="project-visual" :to="`/projects/${project.slug}`" :aria-label="`查看${project.title}`">
      <span>{{ project.coverTone }}</span>
    </RouterLink>
    <div class="project-body">
      <h3>{{ project.title }}</h3>
      <p class="subtitle">{{ project.subtitle }}</p>
      <ul class="tag-list" aria-label="技术栈">
        <li v-for="tag in project.tags" :key="tag" class="tag">{{ tag }}</li>
      </ul>
      <p><strong>我的工作：</strong>{{ project.role }}</p>
      <p><strong>结果：</strong>{{ project.result }}</p>
      <div class="project-actions">
        <RouterLink :to="`/projects/${project.slug}`">项目详情</RouterLink>
        <a :href="project.githubUrl" target="_blank" rel="noreferrer">
          <Github :size="16" aria-hidden="true" /> GitHub
        </a>
      </div>
    </div>
  </article>
</template>

<style scoped>
.project-card {
  overflow: hidden;
  transition: transform 180ms ease, border-color 180ms ease;
}

.project-card:hover {
  transform: translateY(-4px);
  border-color: rgba(120, 224, 210, 0.42);
}

.project-visual {
  display: grid;
  place-items: end start;
  min-height: 168px;
  padding: 18px;
  background:
    linear-gradient(135deg, rgba(255, 255, 255, 0.16), transparent 42%),
    linear-gradient(160deg, #1e293b, #0f172a);
}

.tone-vision .project-visual {
  background: linear-gradient(135deg, #164e63, #0f172a 62%, #f1a8bd);
}

.tone-terminal .project-visual {
  background: linear-gradient(135deg, #111827, #020617);
}

.tone-depth .project-visual {
  background: linear-gradient(135deg, #1d4ed8, #111827 58%, #78e0d2);
}

.tone-sre .project-visual {
  background: linear-gradient(135deg, #064e3b, #111827 58%, #f59e0b);
}

.tone-web .project-visual {
  background: linear-gradient(135deg, #312e81, #111827 58%, #f1a8bd);
}

.project-visual span {
  color: rgba(255, 255, 255, 0.78);
  font-family: "Cascadia Code", Consolas, monospace;
  font-size: 13px;
}

.project-body {
  padding: 22px;
}

h3 {
  margin: 0;
  font-size: 22px;
}

.subtitle,
p {
  color: var(--color-text-secondary);
  line-height: 1.65;
}

.project-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 18px;
}

.project-actions a {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  min-height: 38px;
  padding: 0 12px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-small);
  font-weight: 700;
}
</style>
