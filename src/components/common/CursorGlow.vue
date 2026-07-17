<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';

interface FlairParticle {
  id: number;
  x: number;
  y: number;
  dx: number;
  fall: number;
  rotation: number;
  type: number;
}

const route = useRoute();
const active = computed(() => route.path === '/');
const visible = ref(false);
const cursorX = ref(0);
const cursorY = ref(0);
const particles = ref<FlairParticle[]>([]);

let lastEmit = { x: 0, y: 0 };
let particleId = 0;
let cleanup: (() => void) | undefined;
const listenerOptions = { capture: true, passive: true } as const;

function emitFlair(x: number, y: number) {
  const id = particleId;
  particleId += 1;

  const particle: FlairParticle = {
    id,
    x,
    y,
    dx: Math.round(Math.random() * 68 - 34),
    fall: Math.round(Math.random() * 78 + 78),
    rotation: Math.round(Math.random() * 520 - 260),
    type: (id % 4) + 1,
  };

  particles.value.push(particle);
  window.setTimeout(() => {
    particles.value = particles.value.filter((item) => item.id !== id);
  }, 980);
}

function trackPointer(event: MouseEvent | PointerEvent) {
  if (!active.value) {
    return;
  }

  visible.value = true;
  cursorX.value = event.clientX;
  cursorY.value = event.clientY;

  const distance = Math.hypot(lastEmit.x - event.clientX, lastEmit.y - event.clientY);
  if (distance > 8) {
    emitFlair(event.clientX, event.clientY);
    lastEmit = { x: event.clientX, y: event.clientY };
  }
}

onMounted(() => {
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduceMotion) {
    return;
  }

  document.addEventListener('pointermove', trackPointer, listenerOptions);
  document.addEventListener('pointerrawupdate', trackPointer, listenerOptions);
  document.addEventListener('mousemove', trackPointer, listenerOptions);
  window.addEventListener('pointermove', trackPointer, listenerOptions);
  window.addEventListener('mousemove', trackPointer, listenerOptions);
  cleanup = () => {
    document.removeEventListener('pointermove', trackPointer, listenerOptions);
    document.removeEventListener('pointerrawupdate', trackPointer, listenerOptions);
    document.removeEventListener('mousemove', trackPointer, listenerOptions);
    window.removeEventListener('pointermove', trackPointer, listenerOptions);
    window.removeEventListener('mousemove', trackPointer, listenerOptions);
  };
});

onBeforeUnmount(() => {
  cleanup?.();
});
</script>

<template>
  <Teleport to="body">
    <div v-if="active" class="cursor-flair-layer" aria-hidden="true">
      <span
        v-if="visible"
        class="cursor-orb"
        :style="{ transform: `translate3d(${cursorX - 10}px, ${cursorY - 10}px, 0)` }"
      ></span>
      <span
        v-for="particle in particles"
        :key="particle.id"
        class="cursor-flair"
        :class="`cursor-flair--${particle.type}`"
        :style="{
          left: `${particle.x}px`,
          top: `${particle.y}px`,
          '--dx': `${particle.dx}px`,
          '--fall': `${particle.fall}px`,
          '--rotate': `${particle.rotation}deg`,
        }"
      ></span>
    </div>
  </Teleport>
</template>

<style scoped>
.cursor-flair-layer {
  position: fixed;
  left: 0;
  top: 0;
  width: 100vw;
  height: 100vh;
  z-index: 3000;
  pointer-events: none !important;
  overflow: visible;
}

.cursor-flair-layer *,
.cursor-orb,
.cursor-flair {
  pointer-events: none !important;
}

.cursor-orb {
  position: fixed;
  left: 0;
  top: 0;
  width: 20px;
  height: 20px;
  border-radius: 999px;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.68) 0 8%, rgba(120, 224, 210, 0.58) 22%, rgba(120, 224, 210, 0.2) 52%, transparent 74%);
  box-shadow: 0 0 18px rgba(120, 224, 210, 0.58), 0 0 52px rgba(120, 224, 210, 0.22);
  will-change: transform;
}

.cursor-flair {
  position: fixed;
  left: 0;
  top: 0;
  width: 32px;
  height: 32px;
  opacity: 0;
  border-radius: 999px;
  background:
    radial-gradient(circle at 32% 28%, rgba(255, 255, 255, 0.96), transparent 28%),
    linear-gradient(135deg, rgba(120, 224, 210, 0.98), rgba(184, 251, 120, 0.92));
  box-shadow: 0 0 30px rgba(120, 224, 210, 0.62);
  animation: flair-fall 1180ms cubic-bezier(0.2, 0.85, 0.24, 1) forwards;
  transform: translate(-50%, -50%) scale(0);
  will-change: transform, opacity;
}

.cursor-flair--2 {
  width: 20px;
  height: 34px;
  border-radius: 999px 999px 999px 5px;
  background: linear-gradient(135deg, rgba(241, 168, 189, 0.92), rgba(120, 224, 210, 0.78));
}

.cursor-flair--3 {
  width: 26px;
  height: 26px;
  border-radius: 4px;
  background: linear-gradient(135deg, rgba(255, 220, 130, 0.96), rgba(120, 224, 210, 0.84));
}

.cursor-flair--4 {
  width: 38px;
  height: 16px;
  border-radius: 999px;
  background: linear-gradient(90deg, rgba(120, 224, 210, 0.98), rgba(255, 255, 255, 0.52));
}

@keyframes flair-fall {
  0% {
    opacity: 0;
    transform: translate(-50%, -50%) scale(0) rotate(0deg);
  }
  18% {
    opacity: 1;
    transform: translate(-50%, -50%) scale(1.08) rotate(calc(var(--rotate) * 0.18));
  }
  100% {
    opacity: 0;
    transform: translate(calc(-50% + var(--dx, 0px)), calc(-50% + var(--fall, 120px))) scale(0.62) rotate(var(--rotate, 180deg));
  }
}
</style>
