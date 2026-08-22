<script setup lang="ts">
import { useProfile } from '../composables/useProfile';
import { useTimeline } from '../composables/useTimeline';

const { profile } = useProfile();
const { timeline } = useTimeline();
</script>

<template>
  <section class="page">
    <div class="container page-header about-grid">
      <div>
        <p class="eyebrow">About</p>
        <h1 class="section-title">关于我</h1>
        <p v-if="profile" class="section-copy">
          我是{{ profile.title }}，主要学习方向是 {{ profile.focus }}。我希望把项目实践、排障复盘和技术文章组织成一个长期维护的技术档案。
        </p>
      </div>
      <aside v-if="profile" class="card about-card">
        <strong>{{ profile.name }}</strong>
        <span>{{ profile.handle }}</span>
        <p>{{ profile.intro }}</p>
      </aside>
    </div>
    <div class="container about-list">
      <article v-for="item in timeline" :key="item.title" class="card">
        <span>{{ item.time }}</span>
        <h2>{{ item.title }}</h2>
        <p>{{ item.detail }}</p>
      </article>
    </div>
  </section>
</template>

<style scoped>
.about-grid {
  display: grid;
  grid-template-columns: 1fr 340px;
  gap: 34px;
  align-items: end;
}

.about-card,
.about-list .card {
  padding: 24px;
}

.about-card strong {
  display: block;
  font-size: 26px;
}

.about-card span,
.about-list span {
  display: inline-block;
  margin: 8px 0 16px;
  color: var(--color-accent);
  font-weight: 800;
}

p {
  color: var(--color-text-secondary);
  line-height: 1.75;
}

.about-list {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 18px;
  padding-bottom: var(--section-spacing);
}

h2 {
  margin: 0;
  font-size: 21px;
}

@media (max-width: 920px) {
  .about-grid,
  .about-list {
    grid-template-columns: 1fr;
  }
}
</style>
