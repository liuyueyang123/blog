<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from 'vue';
import { RouterLink } from 'vue-router';
import gsap from 'gsap';

const props = withDefaults(
  defineProps<{
    to?: string;
    href?: string;
    variant?: 'primary' | 'secondary' | 'ghost';
  }>(),
  { variant: 'primary' },
);

const zoneRef = ref<HTMLElement | null>(null);
const buttonRef = ref<HTMLElement | null>(null);
const labelRef = ref<HTMLElement | null>(null);
const bgRef = ref<HTMLElement | null>(null);
const shineRef = ref<HTMLElement | null>(null);

const classes = computed(() => ['magnetic-button', `magnetic-button--${props.variant}`]);

function setupMagneticMotion() {
  const zone = zoneRef.value;
  const button = buttonRef.value;
  const label = labelRef.value;
  const bg = bgRef.value;
  const shine = shineRef.value;
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  if (!zone || !button || !label || !bg || !shine || reduceMotion) {
    return undefined;
  }

  const strength = 0.36;
  const labelStrength = 0.18;
  const bgStrength = -0.12;

  const move = (event: PointerEvent) => {
    const rect = zone.getBoundingClientRect();
    const mapX = gsap.utils.mapRange(rect.left, rect.right, -rect.width / 2, rect.width / 2, event.clientX);
    const mapY = gsap.utils.mapRange(rect.top, rect.bottom, -rect.height / 2, rect.height / 2, event.clientY);

    gsap.to(button, {
      x: mapX * strength,
      y: mapY * strength,
      scale: 1.035,
      duration: 0.42,
      ease: 'power2.out',
      overwrite: 'auto',
    });

    gsap.to(label, {
      x: mapX * labelStrength,
      y: mapY * labelStrength,
      duration: 0.42,
      ease: 'power2.out',
      overwrite: true,
    });

    gsap.to(bg, {
      x: mapX * bgStrength,
      y: mapY * bgStrength,
      scale: 1.08,
      duration: 0.42,
      ease: 'power2.out',
      overwrite: true,
    });

    gsap.to(shine, {
      x: mapX * -0.22,
      y: mapY * -0.2,
      opacity: 0.42,
      duration: 0.42,
      ease: 'power2.out',
      overwrite: true,
    });
  };

  const leave = () => {
    gsap.to(button, {
      x: 0,
      y: 0,
      scale: 1,
      duration: 0.72,
      ease: 'elastic.out(1, 0.42)',
      overwrite: 'auto',
    });

    gsap.to([label, bg, shine], {
      x: 0,
      y: 0,
      scale: 1,
      duration: 0.72,
      ease: 'elastic.out(1, 0.42)',
      overwrite: true,
    });
  };

  const press = () => {
    gsap.to(button, {
      scale: 0.97,
      duration: 0.12,
      ease: 'power2.out',
      overwrite: 'auto',
    });
  };

  const release = () => {
    gsap.to(button, {
      scale: 1.035,
      duration: 0.35,
      ease: 'elastic.out(1, 0.45)',
      overwrite: 'auto',
    });
  };

  zone.addEventListener('pointermove', move);
  zone.addEventListener('pointerleave', leave);
  zone.addEventListener('pointerdown', press);
  zone.addEventListener('pointerup', release);

  return () => {
    zone.removeEventListener('pointermove', move);
    zone.removeEventListener('pointerleave', leave);
    zone.removeEventListener('pointerdown', press);
    zone.removeEventListener('pointerup', release);
    gsap.killTweensOf([button, label, bg, shine]);
  };
}

let cleanup: (() => void) | undefined;

onMounted(() => {
  cleanup = setupMagneticMotion();
});

onBeforeUnmount(() => {
  cleanup?.();
});
</script>

<template>
  <span ref="zoneRef" class="magnetic-zone">
    <RouterLink v-if="to" v-slot="{ href, navigate }" :to="to" custom>
      <a ref="buttonRef" :href="href" :class="classes" @click="navigate">
        <span ref="bgRef" class="magnetic-bg" aria-hidden="true"></span>
        <span ref="shineRef" class="magnetic-shine" aria-hidden="true"></span>
        <span class="magnetic-depth" aria-hidden="true"></span>
        <span ref="labelRef" class="magnetic-label"><slot /></span>
      </a>
    </RouterLink>
    <a v-else-if="href" ref="buttonRef" :href="href" :class="classes" target="_blank" rel="noreferrer">
      <span ref="bgRef" class="magnetic-bg" aria-hidden="true"></span>
      <span ref="shineRef" class="magnetic-shine" aria-hidden="true"></span>
      <span class="magnetic-depth" aria-hidden="true"></span>
      <span ref="labelRef" class="magnetic-label"><slot /></span>
    </a>
    <button v-else ref="buttonRef" :class="classes" type="button">
      <span ref="bgRef" class="magnetic-bg" aria-hidden="true"></span>
      <span ref="shineRef" class="magnetic-shine" aria-hidden="true"></span>
      <span class="magnetic-depth" aria-hidden="true"></span>
      <span ref="labelRef" class="magnetic-label"><slot /></span>
    </button>
  </span>
</template>

<style scoped>
.magnetic-zone {
  display: inline-flex;
  padding: 14px;
  margin: -14px;
  border-radius: 999px;
}

.magnetic-button {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 58px;
  padding: 0 28px;
  border: 1px solid rgba(195, 255, 219, 0.38);
  border-radius: 999px;
  overflow: hidden;
  color: #071114;
  font-weight: 900;
  cursor: pointer;
  will-change: transform;
  text-shadow: 0 1px 0 rgba(255, 255, 255, 0.24);
  box-shadow:
    0 14px 26px rgba(0, 0, 0, 0.28),
    0 0 0 1px rgba(42, 255, 100, 0.12),
    inset 0 1px 1px rgba(255, 255, 255, 0.22),
    inset 0 -5px 10px rgba(0, 92, 42, 0.12);
}

.magnetic-bg {
  position: absolute;
  inset: -18%;
  z-index: 0;
  border-radius: inherit;
  background:
    radial-gradient(ellipse at 76% 38%, rgba(202, 255, 137, 0.88), transparent 42%),
    linear-gradient(105deg, #04d84d 0%, #2bea63 50%, #b8fb78 100%);
  will-change: transform;
}

.magnetic-shine {
  position: absolute;
  left: 9%;
  right: 12%;
  top: 10%;
  z-index: 1;
  height: 50%;
  border-radius: 999px;
  background: radial-gradient(ellipse at 64% 30%, rgba(255, 255, 255, 0.22), transparent 58%);
  opacity: 0.34;
  filter: blur(6px);
  pointer-events: none;
  will-change: transform, opacity;
}

.magnetic-depth {
  position: absolute;
  left: 7%;
  right: 7%;
  bottom: 4%;
  z-index: 1;
  height: 34%;
  border-radius: 999px;
  background: linear-gradient(180deg, transparent, rgba(0, 82, 44, 0.1));
  pointer-events: none;
}

.magnetic-label {
  position: relative;
  z-index: 2;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  pointer-events: none;
  will-change: transform;
}

.magnetic-button--secondary .magnetic-bg {
  background:
    radial-gradient(ellipse at 76% 38%, rgba(255, 206, 230, 0.36), transparent 42%),
    linear-gradient(135deg, rgba(241, 168, 189, 0.42), rgba(157, 134, 255, 0.18));
}

.magnetic-button--secondary {
  border-color: rgba(241, 168, 189, 0.36);
  color: #ffdce6;
}

.magnetic-button--ghost {
  border-color: var(--color-border);
  color: #78e0d2;
  text-shadow: none;
  box-shadow:
    0 18px 34px rgba(0, 0, 0, 0.24),
    inset 0 1px 0 rgba(255, 255, 255, 0.18),
    inset 0 -10px 18px rgba(0, 0, 0, 0.18);
}

.magnetic-button--ghost .magnetic-bg {
  background:
    radial-gradient(ellipse at 76% 38%, rgba(255, 255, 255, 0.13), transparent 42%),
    linear-gradient(135deg, rgba(255, 255, 255, 0.18), rgba(255, 255, 255, 0.06));
}

.magnetic-button--ghost .magnetic-shine {
  opacity: 0.18;
}

.magnetic-button--ghost .magnetic-depth {
  background: linear-gradient(180deg, transparent, rgba(0, 0, 0, 0.22));
}

@media (prefers-reduced-motion: reduce) {
  .magnetic-button,
  .magnetic-label,
  .magnetic-bg,
  .magnetic-shine {
    transform: none !important;
  }
}
</style>
