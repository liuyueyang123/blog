<script setup lang="ts">
import HeroSection from '../components/home/HeroSection.vue';
import CapabilityOverview from '../components/home/CapabilityOverview.vue';
import EngineeringMap from '../components/home/EngineeringMap.vue';
import SectionHeader from '../components/common/SectionHeader.vue';
import SkillGroupCard from '../components/skills/SkillGroupCard.vue';
import ProjectCard from '../components/projects/ProjectCard.vue';
import TroubleCard from '../components/troubleshooting/TroubleCard.vue';
import { useRevealAnimations } from '../composables/useGsap';
import { skillGroups } from '../data/skills';
import { projects } from '../data/projects';
import { troubleshootingCases } from '../data/troubleshooting';
import { articles } from '../data/articles';
import { timeline } from '../data/timeline';

useRevealAnimations();
</script>

<template>
  <div>
    <HeroSection />
    <CapabilityOverview />
    <EngineeringMap />

    <section class="section">
      <div class="container">
        <SectionHeader
          eyebrow="Skills"
          title="技术栈与使用场景"
          copy="不做百分比熟练度，也不堆图标。这里更像一份工程索引：技术、方向、用法和当前状态。"
        />
        <div class="home-skill-list">
          <SkillGroupCard v-for="group in skillGroups.slice(0, 2)" :key="group.title" :group="group" />
        </div>
      </div>
    </section>

    <section class="section visual-projects">
      <div class="container">
        <SectionHeader
          eyebrow="Projects"
          title="项目切片"
          copy="每张卡片都保留项目目标、我的工作和结果，同时加入更明确的视觉封面，避免变成纯文字列表。"
        />
        <div class="project-grid">
          <ProjectCard v-for="project in projects" :key="project.slug" :project="project" />
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <SectionHeader
          eyebrow="Troubleshooting"
          title="排障现场"
          copy="用真实问题展示 SRE 思维：看现象、分层验证、找根因、做复盘。"
        />
        <div class="trouble-grid">
          <TroubleCard v-for="item in troubleshootingCases" :key="item.slug" :item="item" />
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container article-timeline">
        <div>
          <SectionHeader
            eyebrow="Articles"
            title="技术文章"
            copy="第一版使用模拟文章，后续可以替换为 FastAPI 返回的数据。"
          />
          <div class="article-list" data-stagger>
            <RouterLink v-for="article in articles" :key="article.slug" :to="`/articles/${article.slug}`" class="article-row">
              <span>{{ article.category }}</span>
              <strong>{{ article.title }}</strong>
              <em>{{ article.readTime }}</em>
            </RouterLink>
          </div>
        </div>
        <div>
          <SectionHeader eyebrow="Timeline" title="成长路径" />
          <ol class="timeline" data-stagger>
            <li v-for="item in timeline" :key="item.title">
              <span>{{ item.time }}</span>
              <strong>{{ item.title }}</strong>
              <p>{{ item.detail }}</p>
            </li>
          </ol>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.home-skill-list {
  display: grid;
  gap: 18px;
}

.visual-projects {
  position: relative;
}

.visual-projects::before {
  content: "";
  position: absolute;
  inset: 5% 0 auto;
  height: 420px;
  opacity: 0.16;
  pointer-events: none;
  background:
    linear-gradient(90deg, rgba(120, 224, 210, 0.22) 1px, transparent 1px),
    linear-gradient(rgba(120, 224, 210, 0.16) 1px, transparent 1px);
  background-size: 54px 54px;
}

.project-grid,
.trouble-grid {
  position: relative;
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 18px;
}

.article-timeline {
  display: grid;
  grid-template-columns: 1fr 0.9fr;
  gap: 42px;
}

.article-list {
  display: grid;
  gap: 10px;
  perspective: 1000px;
}

.article-row {
  display: grid;
  grid-template-columns: 120px 1fr 70px;
  gap: 12px;
  align-items: center;
  min-height: 58px;
  padding: 0 16px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-small);
  background:
    linear-gradient(135deg, rgba(255, 255, 255, 0.12), rgba(255, 255, 255, 0.035)),
    rgba(14, 21, 39, 0.46);
  box-shadow: var(--shadow-glass);
  backdrop-filter: blur(16px) saturate(135%);
  -webkit-backdrop-filter: blur(16px) saturate(135%);
  transition:
    transform 190ms cubic-bezier(0.2, 0.9, 0.24, 1.25),
    border-color 190ms ease,
    box-shadow 190ms ease;
  will-change: transform;
}

.article-row:hover {
  transform: translateY(-3px) scale(1.014);
  border-color: rgba(120, 224, 210, 0.42);
}

.article-row:active {
  animation: article-pop 360ms cubic-bezier(0.2, 0.95, 0.24, 1.28);
}

.article-row span,
.article-row em {
  color: var(--color-text-secondary);
  font-style: normal;
  font-size: 13px;
}

.timeline {
  display: grid;
  gap: 14px;
  margin: 0;
  padding: 0;
  list-style: none;
}

.timeline li {
  position: relative;
  padding: 18px 18px 18px 22px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-small);
  background: rgba(255, 255, 255, 0.04);
}

.timeline span {
  color: var(--color-accent);
  font-size: 13px;
  font-weight: 800;
}

.timeline strong {
  display: block;
  margin-top: 6px;
}

.timeline p {
  margin: 8px 0 0;
  color: var(--color-text-secondary);
  line-height: 1.65;
}

@media (max-width: 920px) {
  .project-grid,
  .trouble-grid,
  .article-timeline {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 620px) {
  .article-row {
    grid-template-columns: 1fr;
    padding: 14px;
  }
}

@media (prefers-reduced-motion: reduce) {
  .article-row,
  .article-row:hover {
    transform: none;
    animation: none;
  }
}
</style>
