<script setup lang="ts">
import type { SkillGroup } from '../../types/content';

defineProps<{ group: SkillGroup }>();
</script>

<template>
  <article class="skill-group card" data-reveal>
    <div class="skill-heading">
      <h3>{{ group.title }}</h3>
      <p>{{ group.summary }}</p>
    </div>
    <div class="skill-items">
      <div v-for="item in group.items" :key="`${group.title}-${item.name}`" class="skill-item">
        <div>
          <strong>{{ item.name }}</strong>
          <span>{{ item.direction }}</span>
        </div>
        <p>{{ item.scenario }}</p>
        <em>{{ item.status }}</em>
      </div>
    </div>
  </article>
</template>

<style scoped>
.skill-group {
  padding: 24px;
}

.skill-heading {
  display: flex;
  justify-content: space-between;
  gap: 24px;
  margin-bottom: 20px;
}

h3 {
  margin: 0;
  font-size: 24px;
}

.skill-heading p,
.skill-item p {
  margin: 0;
  color: var(--color-text-secondary);
  line-height: 1.65;
}

.skill-items {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}

.skill-item {
  padding: 16px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-small);
  background: rgba(255, 255, 255, 0.035);
}

.skill-item div {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 10px;
}

.skill-item span {
  color: var(--color-accent);
  font-size: 13px;
}

.skill-item em {
  display: inline-block;
  margin-top: 12px;
  color: #ffdce6;
  font-style: normal;
  font-size: 13px;
}

@media (max-width: 760px) {
  .skill-heading,
  .skill-item div {
    flex-direction: column;
  }

  .skill-items {
    grid-template-columns: 1fr;
  }
}
</style>
