<script setup lang="ts">
defineProps<{
  eyebrow: string;
  title: string;
  copy?: string;
}>();
</script>

<template>
  <div class="section-heading" data-reveal>
    <p class="eyebrow">{{ eyebrow }}</p>
    <h2 class="section-title">{{ title }}</h2>
    <p v-if="copy" class="section-copy">{{ copy }}</p>
  </div>
</template>

<style scoped>
.section-heading {
  margin-bottom: 34px;
}
</style>
