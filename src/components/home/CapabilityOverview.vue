<script setup lang="ts">
import { ArrowRight } from 'lucide-vue-next';
import { useProfile } from '../../composables/useProfile';
import SectionHeader from '../common/SectionHeader.vue';

const { profile } = useProfile();

function visualClass(index: number) {
  return ['visual-rings', 'visual-bars', 'visual-wave', 'visual-grid'][index % 4];
}
</script>

<template>
  <section class="section direction-section">
    <div class="container">
      <SectionHeader
        eyebrow="Core Focus"
        title="我的技术方向"
        copy="用部署、观测、排障和模型实践把技术学习连接成一条可以持续迭代的工程路径。"
      />
      <div class="capability-grid" data-stagger>
        <RouterLink
          v-for="(card, index) in profile?.capabilityCards ?? []"
          :key="card.title"
          class="capability-card card"
          to="/skills"
        >
          <div class="card-visual" :class="visualClass(index)" aria-hidden="true">
            <span></span><span></span><span></span><span></span>
          </div>
          <div class="card-copy">
            <h3>{{ card.title }}</h3>
            <p class="tech">{{ card.tech }}</p>
            <p>{{ card.practice }}</p>
            <span class="detail-link">查看详情 <ArrowRight :size="16" aria-hidden="true" /></span>
          </div>
        </RouterLink>
      </div>
    </div>
  </section>
</template>

<style scoped>
.direction-section {
  position: relative;
}

.direction-section::before {
  content: "";
  position: absolute;
  inset: 10% 0 auto;
  height: 360px;
  pointer-events: none;
  opacity: 0.18;
  background:
    repeating-radial-gradient(ellipse at 20% 40%, transparent 0 18px, rgba(120, 224, 210, 0.48) 19px 20px, transparent 21px 34px),
    repeating-radial-gradient(ellipse at 80% 38%, transparent 0 16px, rgba(241, 168, 189, 0.38) 17px 18px, transparent 19px 32px);
}

.capability-grid {
  position: relative;
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 16px;
}

.capability-card {
  display: grid;
  grid-template-rows: 150px 1fr;
  min-height: 390px;
  overflow: hidden;
  transition: transform 180ms ease, border-color 180ms ease;
}

.capability-card:hover {
  transform: translateY(-4px);
  border-color: rgba(120, 224, 210, 0.45);
}

.card-visual {
  position: relative;
  overflow: hidden;
  border-bottom: 1px solid var(--color-border);
  background: rgba(255, 255, 255, 0.035);
}

.visual-rings {
  background:
    repeating-radial-gradient(circle at 48% 55%, transparent 0 15px, rgba(120, 224, 210, 0.62) 16px 17px, transparent 18px 30px),
    linear-gradient(135deg, rgba(120, 224, 210, 0.12), rgba(255, 255, 255, 0.03));
}

.visual-rings span {
  position: absolute;
  width: 10px;
  height: 10px;
  border-radius: 999px;
  background: var(--color-accent);
}

.visual-rings span:nth-child(1) { left: 22%; top: 28%; }
.visual-rings span:nth-child(2) { right: 28%; top: 22%; }
.visual-rings span:nth-child(3) { left: 36%; bottom: 24%; }
.visual-rings span:nth-child(4) { right: 18%; bottom: 30%; }

.visual-bars {
  display: flex;
  align-items: end;
  gap: 10px;
  padding: 24px;
  background: linear-gradient(145deg, rgba(241, 168, 189, 0.16), rgba(255, 255, 255, 0.03));
}

.visual-bars span {
  flex: 1;
  border-radius: 999px 999px 0 0;
  background: linear-gradient(180deg, var(--color-accent-secondary), rgba(241, 168, 189, 0.2));
}

.visual-bars span:nth-child(1) { height: 42%; }
.visual-bars span:nth-child(2) { height: 72%; }
.visual-bars span:nth-child(3) { height: 56%; }
.visual-bars span:nth-child(4) { height: 88%; }

.visual-wave {
  background:
    linear-gradient(90deg, rgba(120, 224, 210, 0.1) 1px, transparent 1px),
    linear-gradient(rgba(120, 224, 210, 0.1) 1px, transparent 1px);
  background-size: 28px 28px;
}

.visual-wave span {
  position: absolute;
  left: 12%;
  width: 76%;
  height: 2px;
  background: linear-gradient(90deg, transparent, var(--color-accent), transparent);
  transform-origin: left;
}

.visual-wave span:nth-child(1) { top: 30%; transform: rotate(8deg); }
.visual-wave span:nth-child(2) { top: 45%; transform: rotate(-5deg); }
.visual-wave span:nth-child(3) { top: 60%; transform: rotate(7deg); }
.visual-wave span:nth-child(4) { top: 75%; transform: rotate(-4deg); }

.visual-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
  padding: 24px;
  background:
    radial-gradient(circle at 70% 30%, rgba(120, 224, 210, 0.18), transparent 38%),
    rgba(255, 255, 255, 0.035);
}

.visual-grid span {
  border: 1px solid rgba(120, 224, 210, 0.34);
  border-radius: var(--radius-small);
  background: rgba(120, 224, 210, 0.07);
}

.card-copy {
  padding: 22px;
}

h3 {
  margin: 0;
  font-size: 20px;
}

p {
  color: var(--color-text-secondary);
  line-height: 1.7;
}

.tech {
  color: var(--color-accent);
  font-weight: 700;
}

.detail-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  margin-top: 10px;
  color: var(--color-text-primary);
  font-weight: 700;
}

@media (max-width: 1020px) {
  .capability-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 620px) {
  .capability-grid {
    grid-template-columns: 1fr;
  }

  .capability-card {
    min-height: auto;
  }
}
</style>
