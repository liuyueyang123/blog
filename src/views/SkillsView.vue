<script setup lang="ts">
import SkillGroupCard from '../components/skills/SkillGroupCard.vue';
import { useRevealAnimations } from '../composables/useGsap';
import { useSkills } from '../composables/useSkills';

const { skillGroups, loading } = useSkills();
useRevealAnimations(loading);
</script>

<template>
  <section class="page">
    <div class="container page-header">
      <p class="eyebrow">Skills</p>
      <h1 class="section-title">技术方向</h1>
      <p class="section-copy">每项技术都对应方向、使用场景和当前状态。</p>
    </div>
    <div class="container skill-page-list">
      <SkillGroupCard v-for="group in skillGroups" :key="group.title" :group="group" />
    </div>
  </section>
</template>

<style scoped>
.skill-page-list {
  display: grid;
  gap: 18px;
  padding-bottom: var(--section-spacing);
}
</style>
