<script setup lang="ts">
import ProjectCard from '../components/projects/ProjectCard.vue';
import { useRevealAnimations } from '../composables/useGsap';
import { projects } from '../data/projects';

useRevealAnimations();
</script>

<template>
  <section class="page">
    <div class="container page-header">
      <p class="eyebrow">Projects</p>
      <h1 class="section-title">真实项目与工程实践</h1>
      <p class="section-copy">覆盖 AI 模型训练、Web 推理、SRE 可观测性和个人站点部署规划。</p>
    </div>
    <div class="container project-page-grid">
      <ProjectCard v-for="project in projects" :key="project.slug" :project="project" />
    </div>
  </section>
</template>

<style scoped>
.project-page-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 18px;
  padding-bottom: var(--section-spacing);
}

@media (max-width: 860px) {
  .project-page-grid {
    grid-template-columns: 1fr;
  }
}
</style>
