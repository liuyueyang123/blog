<script setup lang="ts">
import TroubleCard from '../components/troubleshooting/TroubleCard.vue';
import { useRevealAnimations } from '../composables/useGsap';
import { troubleshootingCases } from '../data/troubleshooting';

useRevealAnimations();
</script>

<template>
  <section class="page">
    <div class="container page-header">
      <p class="eyebrow">SRE Cases</p>
      <h1 class="section-title">故障排查案例</h1>
      <p class="section-copy">按现象、排查、工具、根因、解决和复盘组织，突出可迁移的排障思维。</p>
    </div>
    <div class="container trouble-page-grid">
      <TroubleCard v-for="item in troubleshootingCases" :key="item.slug" :item="item" />
    </div>
  </section>
</template>

<style scoped>
.trouble-page-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 18px;
  padding-bottom: var(--section-spacing);
}

@media (max-width: 900px) {
  .trouble-page-grid {
    grid-template-columns: 1fr;
  }
}
</style>
