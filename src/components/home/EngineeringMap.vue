<template>
  <section class="section map-section">
    <div class="container map-layout">
      <div class="map-copy" data-reveal>
        <p class="eyebrow">System Map</p>
        <h2 class="section-title">从代码到服务现场</h2>
        <p class="section-copy">
          我更希望首页能像一张工程地图：能看到技术方向，也能看到它们如何流向部署、观测、排障和复盘。
        </p>
      </div>
      <div class="flow-board card" data-reveal aria-label="工程流程图">
        <div class="flow-node node-code">Code</div>
        <div class="flow-node node-build">Build</div>
        <div class="flow-node node-deploy">Deploy</div>
        <div class="flow-node node-observe">Observe</div>
        <div class="flow-node node-debug">Debug</div>
        <div class="flow-node node-review">Review</div>
        <div class="flow-track track-a"></div>
        <div class="flow-track track-b"></div>
        <div class="flow-track track-c"></div>
        <div class="contour-overlay" aria-hidden="true"></div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.map-section {
  padding-top: 24px;
}

.map-layout {
  display: grid;
  grid-template-columns: 0.76fr 1.24fr;
  gap: 34px;
  align-items: center;
}

.flow-board {
  position: relative;
  min-height: 420px;
  overflow: hidden;
  background:
    linear-gradient(135deg, rgba(120, 224, 210, 0.08), transparent 44%),
    linear-gradient(315deg, rgba(241, 168, 189, 0.11), transparent 46%),
    rgba(255, 255, 255, 0.035);
}

.contour-overlay {
  position: absolute;
  inset: -12%;
  opacity: 0.24;
  background:
    repeating-radial-gradient(ellipse at 28% 72%, transparent 0 20px, rgba(120, 224, 210, 0.48) 21px 22px, transparent 23px 38px),
    repeating-radial-gradient(ellipse at 82% 20%, transparent 0 16px, rgba(241, 168, 189, 0.42) 17px 18px, transparent 19px 34px);
}

.flow-node {
  position: absolute;
  z-index: 2;
  display: grid;
  place-items: center;
  width: 112px;
  height: 58px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-small);
  background: rgba(9, 14, 28, 0.8);
  color: var(--color-text-primary);
  font-family: "Cascadia Code", Consolas, monospace;
  font-weight: 800;
  backdrop-filter: blur(10px);
}

.node-code { left: 8%; top: 18%; }
.node-build { left: 36%; top: 14%; }
.node-deploy { right: 10%; top: 24%; }
.node-observe { right: 12%; bottom: 22%; }
.node-debug { left: 39%; bottom: 14%; }
.node-review { left: 9%; bottom: 26%; }

.flow-track {
  position: absolute;
  z-index: 1;
  height: 2px;
  background: linear-gradient(90deg, transparent, rgba(120, 224, 210, 0.72), transparent);
}

.track-a {
  left: 18%;
  top: 29%;
  width: 62%;
  transform: rotate(8deg);
}

.track-b {
  right: 17%;
  top: 52%;
  width: 46%;
  transform: rotate(82deg);
}

.track-c {
  left: 18%;
  bottom: 29%;
  width: 60%;
  transform: rotate(-9deg);
}

@media (max-width: 900px) {
  .map-layout {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 560px) {
  .flow-board {
    min-height: 360px;
  }

  .flow-node {
    width: 92px;
    height: 50px;
    font-size: 13px;
  }
}
</style>
