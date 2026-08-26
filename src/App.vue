<script setup lang="ts">
import { RouterView } from 'vue-router';
import SiteFooter from './components/common/SiteFooter.vue';
import SiteHeader from './components/common/SiteHeader.vue';
import CursorGlow from './components/common/CursorGlow.vue';
</script>

<template>
  <div class="global-starlight-portrait" aria-hidden="true"></div>
  <SiteHeader />
  <main id="main-content">
    <RouterView v-slot="{ Component }">
      <Transition name="page" mode="out-in">
        <component :is="Component" />
      </Transition>
    </RouterView>
  </main>
  <SiteFooter />
  <CursorGlow />
</template>

<style scoped>
.global-starlight-portrait {
  position: fixed;
  z-index: 0;
  top: 64px;
  left: 43%;
  width: min(54vw, 780px);
  height: min(92vh, 1040px);
  pointer-events: none;
  opacity: 0.24;
  background:
    radial-gradient(circle at 48% 24%, rgba(255, 207, 98, 0.16), transparent 24%),
    radial-gradient(circle at 60% 58%, rgba(84, 137, 255, 0.18), transparent 28%),
    url("/images/global-starlight-portrait-cutout.webp");
  background-repeat: no-repeat;
  background-size: contain;
  background-position: center;
  filter: saturate(112%) contrast(105%) blur(0.2px);
  mix-blend-mode: screen;
  transform: translateX(-50%);
  mask-image: linear-gradient(180deg, transparent 0%, rgba(0, 0, 0, 0.88) 12%, rgba(0, 0, 0, 0.9) 82%, transparent 100%);
}

#main-content,
:deep(.site-footer) {
  position: relative;
  z-index: 1;
}

@media (max-width: 960px) {
  .global-starlight-portrait {
    left: 48%;
    width: min(88vw, 660px);
    opacity: 0.16;
  }
}
</style>
