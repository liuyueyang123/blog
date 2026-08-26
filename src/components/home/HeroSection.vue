<script setup lang="ts">
import { ArrowRight } from 'lucide-vue-next';
import { onBeforeUnmount, onMounted, ref } from 'vue';
import MagneticButton from '../common/MagneticButton.vue';

const heroTitle = "Hello, I'm Yael.";
const frameCount = 80;
const frameRate = 12;
const isPhotoWallPaused = ref(false);
const canvasRef = ref<HTMLCanvasElement | null>(null);

const FRAME_DIR = '/video/photo-wall-frames-webp';
const frameSrcs: string[] = Array.from(
  { length: frameCount },
  (_, i) => `${FRAME_DIR}/frame-${String(i).padStart(3, '0')}.webp`,
);

const frames: HTMLImageElement[] = new Array(frameCount);
let currentFrameIndex = 0;
let animationId = 0;
let lastFrameTime = 0;

function loadFrame(i: number): Promise<void> {
  return new Promise((resolve) => {
    const img = new Image();
    img.decoding = 'sync';
    img.onload = () => resolve();
    img.onerror = () => resolve();
    img.src = frameSrcs[i];
    frames[i] = img;
  });
}

function draw() {
  const canvas = canvasRef.value;
  const ctx = canvas?.getContext('2d');
  if (!canvas || !ctx) return;
  const img = frames[currentFrameIndex];
  if (img && img.naturalWidth > 0) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
  }
}

function animatePhotoWall(timestamp: number) {
  if (!lastFrameTime) {
    lastFrameTime = timestamp;
  }

  const frameDuration = 1000 / frameRate;
  if (!isPhotoWallPaused.value && timestamp - lastFrameTime >= frameDuration) {
    currentFrameIndex = (currentFrameIndex + 1) % frameCount;
    draw();
    lastFrameTime = timestamp;
  }

  animationId = window.requestAnimationFrame(animatePhotoWall);
}

function togglePhotoWall() {
  isPhotoWallPaused.value = !isPhotoWallPaused.value;
}

onMounted(async () => {
  // 先加载第一帧立即绘制，让主图快速出现
  await loadFrame(0);
  draw();

  // 其余帧并行加载，全部就绪后再启动动画，杜绝逐帧现取的闪烁
  await Promise.all(Array.from({ length: frameCount - 1 }, (_, i) => loadFrame(i + 1)));

  animationId = window.requestAnimationFrame(animatePhotoWall);
});

onBeforeUnmount(() => {
  window.cancelAnimationFrame(animationId);
});
</script>

<template>
  <section class="hero">
    <div class="flower-field" aria-hidden="true"></div>
    <div class="container hero-grid">
      <div class="hero-copy">
        <div class="hero-main">
          <p class="eyebrow" data-hero-reveal>Portfolio / Blog / Interview</p>
          <h1 class="bounce-title" aria-label="Hello, I'm Yael." data-hero-reveal>
            <span
              v-for="(char, index) in heroTitle"
              :key="`${char}-${index}`"
              class="bounce-letter"
              :style="{ animationDelay: `${index * 0.045}s` }"
              aria-hidden="true"
            >
              {{ char === ' ' ? '\u00A0' : char }}
            </span>
          </h1>
          <div class="hero-actions" data-hero-reveal>
            <MagneticButton to="/projects">
              查看项目 <ArrowRight :size="18" aria-hidden="true" />
            </MagneticButton>
            <MagneticButton to="/skills" variant="ghost">查看技术方向</MagneticButton>
          </div>
        </div>

        <aside class="terminal-card" data-hero-reveal aria-label="终端风格简介">
          <div class="terminal-bar">
            <span></span><span></span><span></span>
          </div>
          <div class="terminal-body">
            <p><strong>$ whoami</strong><br />Yael</p>
            <p><strong>$ focus</strong><br />Linux · Cloud · SRE · AI</p>
            <p><strong>$ status</strong><br />Building, learning and troubleshooting</p>
          </div>
        </aside>
      </div>

      <aside
        class="photo-wall-shell"
        data-hero-reveal
        role="button"
        tabindex="0"
        :aria-pressed="isPhotoWallPaused"
        aria-label="点击暂停或继续 3D 滚动照片墙"
        @click="togglePhotoWall"
        @keydown.enter.prevent="togglePhotoWall"
        @keydown.space.prevent="togglePhotoWall"
      >
        <div class="photo-wall-depth" aria-hidden="true"></div>
        <canvas ref="canvasRef" class="photo-wall-animation" width="420" height="747" aria-hidden="true"></canvas>
      </aside>
    </div>
  </section>
</template>

<style scoped>
.hero {
  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: center;
  overflow: hidden;
  padding: 112px 0 72px;
}

.flower-field {
  position: absolute;
  left: -4vw;
  right: -4vw;
  bottom: 0;
  height: 46vh;
  pointer-events: none;
  opacity: 0.5;
  background:
    linear-gradient(180deg, rgba(13, 20, 37, 0.82), rgba(13, 20, 37, 0.34) 36%, rgba(13, 20, 37, 0.72) 100%),
    url("/images/hero-flower-field.png");
  background-size: cover;
  background-position: center bottom;
  filter: blur(2px) saturate(110%);
  transform: scale(1.04);
  mask-image: linear-gradient(180deg, transparent 0%, rgba(0, 0, 0, 0.34) 15%, rgba(0, 0, 0, 0.82) 54%, rgba(0, 0, 0, 0.62) 100%);
}

.flower-field::before,
.flower-field::after {
  content: "";
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse at 18% 72%, rgba(123, 210, 184, 0.22), transparent 24%),
    radial-gradient(ellipse at 72% 64%, rgba(233, 243, 220, 0.18), transparent 28%),
    linear-gradient(180deg, transparent, rgba(84, 142, 134, 0.16));
}

.flower-field::after {
  opacity: 0.35;
  transform: translateY(18px) scale(1.06);
  filter: blur(8px);
}

.hero-grid {
  position: relative;
  z-index: 2;
  display: grid;
  grid-template-columns: minmax(0, 0.92fr) minmax(340px, 1.08fr);
  gap: clamp(34px, 5vw, 72px);
  align-items: center;
}

.hero-copy {
  display: grid;
  align-content: center;
  min-height: 560px;
}

.hero-main {
  transform: translateY(-34px);
}

h1 {
  margin: 0;
  max-width: 760px;
  font-size: clamp(42px, 5.6vw, 72px);
  line-height: 1.02;
}

.bounce-title {
  display: inline-flex;
  flex-wrap: nowrap;
  white-space: nowrap;
}

.bounce-letter {
  display: inline-block;
  animation: title-bounce 1.85s cubic-bezier(0.2, 0.9, 0.25, 1.4) both;
}

.hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 30px;
}

.hero-actions :deep(.magnetic-button) {
  gap: 8px;
}

.terminal-card {
  width: min(100%, 430px);
  margin-top: 42px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-large);
  overflow: hidden;
  background:
    linear-gradient(135deg, rgba(255, 255, 255, 0.12), rgba(255, 255, 255, 0.035)),
    rgba(8, 13, 26, 0.66);
  box-shadow: var(--shadow-glass);
  backdrop-filter: blur(18px) saturate(138%);
  -webkit-backdrop-filter: blur(18px) saturate(138%);
}

.terminal-bar {
  display: flex;
  gap: 8px;
  padding: 14px 16px;
  border-bottom: 1px solid var(--color-border);
}

.terminal-bar span {
  width: 10px;
  height: 10px;
  border-radius: 999px;
  background: var(--color-accent-secondary);
}

.terminal-bar span:nth-child(2) {
  background: #ffd166;
}

.terminal-bar span:nth-child(3) {
  background: var(--color-accent);
}

.terminal-body {
  padding: 24px;
  color: #d8fff9;
  font-family: "Cascadia Code", "Fira Code", Consolas, monospace;
  font-size: 14px;
  line-height: 1.65;
}

.terminal-body p {
  margin: 0 0 18px;
}

.terminal-body p:last-child {
  margin-bottom: 0;
}

.photo-wall-shell {
  position: relative;
  width: min(100%, 560px);
  justify-self: end;
  margin-right: clamp(10px, 2vw, 28px);
  padding: clamp(6px, 1vw, 12px);
  background: transparent;
  border: 0;
  perspective: 1100px;
  cursor: pointer;
  -webkit-tap-highlight-color: transparent;
}

.photo-wall-depth {
  position: absolute;
  inset: 16% 2% 4% 18%;
  z-index: 0;
  border-radius: 32px;
  background: linear-gradient(135deg, rgba(120, 224, 210, 0.2), rgba(241, 168, 189, 0.12));
  filter: blur(24px);
  opacity: 0.62;
  transform: rotateX(8deg) rotateY(-10deg) translateZ(-30px);
}

.photo-wall-animation {
  position: relative;
  z-index: 1;
  display: block;
  width: 100%;
  max-width: calc(min(70vh, 710px) * 420 / 747);
  height: auto;
  background: transparent;
  filter: drop-shadow(0 30px 58px rgba(0, 0, 0, 0.42));
  transform: rotateX(4deg) rotateY(-9deg) rotateZ(0.8deg);
  transform-origin: center;
}

@keyframes title-bounce {
  0% {
    opacity: 0;
    transform: translateY(18px) scale(0.96);
  }
  56% {
    opacity: 1;
    transform: translateY(-8px) scale(1.025);
  }
  74% {
    transform: translateY(3px) scale(0.995);
  }
  100% {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

@media (max-width: 960px) {
  .hero {
    min-height: auto;
  }

  .hero-grid {
    grid-template-columns: 1fr;
  }

  .hero-copy {
    min-height: auto;
  }

  .hero-main {
    transform: none;
  }

  .photo-wall-shell {
    justify-self: center;
    margin-right: 0;
    width: min(100%, 500px);
  }

}

@media (max-width: 720px) {
  h1 {
    font-size: clamp(32px, 9.2vw, 52px);
  }
}

@media (max-width: 520px) {
  h1 {
    font-size: clamp(28px, 8.8vw, 42px);
  }

  .hero-actions {
    flex-direction: column;
  }

  .hero-actions :deep(.magnetic-button) {
    width: 100%;
  }

  .terminal-card {
    margin-top: 32px;
  }

  .photo-wall-animation {
    transform: rotateX(2deg) rotateY(-4deg);
  }
}

@media (prefers-reduced-motion: reduce) {
  .bounce-letter {
    animation: none;
  }
}
</style>
