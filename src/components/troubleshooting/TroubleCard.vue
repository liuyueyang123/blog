<script setup lang="ts">
import type { TroubleshootingCase } from '../../types/content';

defineProps<{ item: TroubleshootingCase }>();
</script>

<template>
  <article class="trouble-card card" data-reveal>
    <h3>{{ item.title }}</h3>
    <dl>
      <div><dt>故障现象</dt><dd>{{ item.symptom }}</dd></div>
      <div><dt>排查思路</dt><dd>{{ item.process }}</dd></div>
      <div><dt>使用工具</dt><dd>{{ item.tools.join(' / ') }}</dd></div>
      <div><dt>根本原因</dt><dd>{{ item.rootCause }}</dd></div>
      <div><dt>解决结果</dt><dd>{{ item.resolution }}</dd></div>
      <div><dt>复盘总结</dt><dd>{{ item.review }}</dd></div>
    </dl>
  </article>
</template>

<style scoped>
.trouble-card {
  padding: 22px;
}

h3 {
  margin: 0 0 18px;
  font-size: 22px;
}

dl {
  display: grid;
  gap: 12px;
  margin: 0;
}

div {
  display: grid;
  grid-template-columns: 90px 1fr;
  gap: 12px;
  padding-bottom: 12px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

div:last-child {
  border-bottom: 0;
  padding-bottom: 0;
}

dt {
  color: var(--color-accent);
  font-weight: 800;
}

dd {
  margin: 0;
  color: var(--color-text-secondary);
  line-height: 1.65;
}

@media (max-width: 560px) {
  div {
    grid-template-columns: 1fr;
  }
}
</style>
