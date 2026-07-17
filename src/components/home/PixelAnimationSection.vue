<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';

const codingHP = ref(0);
const buildingHP = ref(0);
let animationFrame: number | null = null;

function animateHP() {
  const time = Date.now() * 0.001; // 转换为秒

  // Coding HP 动画：从 0 到 100 再回到 0，循环
  codingHP.value = ((Math.sin(time * 0.5) + 1) / 2) * 100;

  // Building HP 动画：稍有延迟，从 0 到 100 再回到 0，循环
  buildingHP.value = ((Math.sin(time * 0.5 + Math.PI / 2) + 1) / 2) * 100;

  animationFrame = requestAnimationFrame(animateHP);
}

onMounted(() => {
  animateHP();
});

onUnmounted(() => {
  if (animationFrame) {
    cancelAnimationFrame(animationFrame);
  }
});
</script>

<template>
  <div class="retro-pixel-section">
    <div class="pixel-canvas">
      <!-- 左侧区域：人物像素头像 -->
      <div class="left-section">
        <!-- 背景星星 -->
        <div class="stars-background">
          <svg viewBox="0 0 100 100" class="stars-svg">
            <!-- 左上角星星 -->
            <rect x="5" y="8" width="1" height="1" fill="white" />
            <rect x="6" y="7" width="1" height="1" fill="white" />
            <rect x="7" y="6" width="1" height="1" fill="white" />
            <rect x="8" y="7" width="1" height="1" fill="white" />
            <rect x="9" y="8" width="1" height="1" fill="white" />

            <rect x="12" y="15" width="1" height="1" fill="white" />
            <rect x="13" y="14" width="1" height="1" fill="white" />
            <rect x="14" y="13" width="1" height="1" fill="white" />
            <rect x="15" y="14" width="1" height="1" fill="white" />
            <rect x="16" y="15" width="1" height="1" fill="white" />

            <!-- 右上角星星 -->
            <rect x="82" y="5" width="1" height="1" fill="white" />
            <rect x="83" y="4" width="1" height="1" fill="white" />
            <rect x="84" y="3" width="1" height="1" fill="white" />
            <rect x="85" y="4" width="1" height="1" fill="white" />
            <rect x="86" y="5" width="1" height="1" fill="white" />

            <rect x="75" y="12" width="1" height="1" fill="white" />
            <rect x="76" y="11" width="1" height="1" fill="white" />
            <rect x="77" y="10" width="1" height="1" fill="white" />
            <rect x="78" y="11" width="1" height="1" fill="white" />
            <rect x="79" y="12" width="1" height="1" fill="white" />

            <!-- 左下角星星 -->
            <rect x="8" y="85" width="1" height="1" fill="white" />
            <rect x="9" y="84" width="1" height="1" fill="white" />
            <rect x="10" y="83" width="1" height="1" fill="white" />
            <rect x="11" y="84" width="1" height="1" fill="white" />
            <rect x="12" y="85" width="1" height="1" fill="white" />

            <rect x="15" y="92" width="1" height="1" fill="white" />
            <rect x="16" y="91" width="1" height="1" fill="white" />
            <rect x="17" y="90" width="1" height="1" fill="white" />
            <rect x="18" y="91" width="1" height="1" fill="white" />
            <rect x="19" y="92" width="1" height="1" fill="white" />

            <!-- 右下角星星 -->
            <rect x="85" y="88" width="1" height="1" fill="white" />
            <rect x="86" y="87" width="1" height="1" fill="white" />
            <rect x="87" y="86" width="1" height="1" fill="white" />
            <rect x="88" y="87" width="1" height="1" fill="white" />
            <rect x="89" y="88" width="1" height="1" fill="white" />

            <rect x="92" y="82" width="1" height="1" fill="white" />
            <rect x="93" y="81" width="1" height="1" fill="white" />
            <rect x="94" y="80" width="1" height="1" fill="white" />
            <rect x="95" y="81" width="1" height="1" fill="white" />
            <rect x="96" y="82" width="1" height="1" fill="white" />
          </svg>
        </div>

        <!-- 人物像素头像 -->
        <div class="person-avatar">
          <svg viewBox="0 0 64 64" class="person-svg" style="image-rendering: pixelated;">
            <!-- 耳机头带 -->
            <rect x="20" y="8" width="24" height="2" fill="white" />
            <rect x="18" y="10" width="28" height="2" fill="white" />

            <!-- 左耳机 -->
            <rect x="14" y="12" width="4" height="2" fill="white" />
            <rect x="12" y="14" width="6" height="6" fill="white" />
            <rect x="12" y="20" width="4" height="2" fill="white" />

            <!-- 右耳机 -->
            <rect x="46" y="12" width="4" height="2" fill="white" />
            <rect x="46" y="14" width="6" height="6" fill="white" />
            <rect x="48" y="20" width="4" height="2" fill="white" />

            <!-- 右耳机上的爱心图案 -->
            <rect x="50" y="16" width="2" height="1" fill="white" />
            <rect x="48" y="17" width="4" height="1" fill="white" />
            <rect x="47" y="18" width="2" height="1" fill="white" />
            <rect x="49" y="18" width="2" height="1" fill="white" />
            <rect x="48" y="19" width="2" height="1" fill="white" />

            <!-- 头部轮廓 -->
            <rect x="22" y="14" width="20" height="2" fill="white" />
            <rect x="20" y="16" width="24" height="4" fill="white" />
            <rect x="18" y="20" width="28" height="8" fill="white" />
            <rect x="20" y="28" width="24" height="2" fill="white" />

            <!-- 头发 - 短发 -->
            <rect x="24" y="16" width="2" height="2" fill="white" />
            <rect x="26" y="14" width="4" height="2" fill="white" />
            <rect x="30" y="12" width="4" height="2" fill="white" />
            <rect x="34" y="14" width="4" height="2" fill="white" />
            <rect x="38" y="16" width="2" height="2" fill="white" />

            <!-- 眉毛 - 短像素线条 -->
            <rect x="24" y="22" width="4" height="1" fill="white" />
            <rect x="36" y="22" width="4" height="1" fill="white" />

            <!-- 眼睛 - 半耷拉的眼皮 -->
            <rect x="24" y="24" width="6" height="2" fill="white" />
            <rect x="34" y="24" width="6" height="2" fill="white" />

            <!-- 嘴巴 - 浅浅的微笑 -->
            <rect x="28" y="30" width="8" height="1" fill="white" />

            <!-- 身体轮廓 -->
            <rect x="22" y="32" width="20" height="2" fill="white" />
            <rect x="20" y="34" width="24" height="8" fill="white" />
            <rect x="18" y="42" width="28" height="4" fill="white" />

            <!-- 肩膀 -->
            <rect x="12" y="38" width="6" height="4" fill="white" />
            <rect x="46" y="38" width="6" height="4" fill="white" />
          </svg>
        </div>
      </div>

      <!-- 分隔线 -->
      <div class="divider-line"></div>

      <!-- 右侧区域：游戏UI面板 -->
      <div class="right-section">
        <!-- 上方对话框 -->
        <div class="chat-box">
          <div class="chat-content">
            <div class="chat-line sender">Yael:</div>
            <div class="chat-line message">wake up.</div>
          </div>
          <div class="dropdown-icon">
            <svg viewBox="0 0 8 8" class="dropdown-svg">
              <rect x="1" y="1" width="2" height="1" fill="white" />
              <rect x="3" y="2" width="2" height="1" fill="white" />
              <rect x="5" y="1" width="2" height="1" fill="white" />
            </svg>
          </div>
        </div>

        <!-- 下方猫咪状态栏 -->
        <div class="cats-panel">
          <div class="panel-title">cats:</div>

          <!-- 第一只猫：coding -->
          <div class="cat-row">
            <div class="cat-avatar">
              <svg viewBox="0 0 16 16" class="cat-svg">
                <!-- 开心猫猫 - 咧嘴笑、露出牙齿 -->
                <rect x="4" y="2" width="8" height="8" fill="white" />
                <rect x="3" y="3" width="1" height="2" fill="white" />
                <rect x="12" y="3" width="1" height="2" fill="white" />
                <rect x="2" y="4" width="1" height="1" fill="white" />
                <rect x="13" y="4" width="1" height="1" fill="white" />
                <!-- 眼睛 -->
                <rect x="5" y="5" width="2" height="2" fill="white" />
                <rect x="9" y="5" width="2" height="2" fill="white" />
                <!-- 咧嘴笑 -->
                <rect x="6" y="8" width="4" height="1" fill="white" />
                <rect x="7" y="9" width="2" height="1" fill="white" />
                <!-- 身体 -->
                <rect x="5" y="10" width="6" height="4" fill="white" />
              </svg>
            </div>
            <div class="cat-name">coding</div>
            <div class="hp-section">
              <div class="hp-label">HP</div>
              <div class="hp-bar">
                <div class="hp-fill" :style="{ width: codingHP + '%' }"></div>
              </div>
            </div>
          </div>

          <!-- 第二只猫：building -->
          <div class="cat-row">
            <div class="cat-avatar">
              <svg viewBox="0 0 16 16" class="cat-svg">
                <!-- 冷淡猫猫 - 眯起双眼、面无表情 -->
                <rect x="4" y="2" width="8" height="8" fill="white" />
                <rect x="3" y="3" width="1" height="2" fill="white" />
                <rect x="12" y="3" width="1" height="2" fill="white" />
                <rect x="2" y="4" width="1" height="1" fill="white" />
                <rect x="13" y="4" width="1" height="1" fill="white" />
                <!-- 眯眼 -->
                <rect x="5" y="5" width="3" height="1" fill="white" />
                <rect x="8" y="5" width="3" height="1" fill="white" />
                <!-- 面无表情 -->
                <rect x="7" y="8" width="2" height="1" fill="white" />
                <!-- 身体 -->
                <rect x="5" y="10" width="6" height="4" fill="white" />
              </svg>
            </div>
            <div class="cat-name">building</div>
            <div class="hp-section">
              <div class="hp-label">HP</div>
              <div class="hp-bar">
                <div class="hp-fill" :style="{ width: buildingHP + '%' }"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.retro-pixel-section {
  padding: 40px 0;
  background-color: #000;
}

.pixel-canvas {
  display: flex;
  max-width: 600px;
  margin: 0 auto;
  background-color: #000;
  border: 2px solid white;
  image-rendering: pixelated;
}

/* 左侧区域 */
.left-section {
  flex: 1;
  position: relative;
  background-color: #000;
  min-height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 星星背景 */
.stars-background {
  position: absolute;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.stars-svg {
  width: 100%;
  height: 100%;
  image-rendering: pixelated;
}

/* 人物头像 */
.person-avatar {
  z-index: 1;
}

.person-svg {
  width: 128px;
  height: 128px;
  image-rendering: pixelated;
  filter: none;
}

/* 分隔线 */
.divider-line {
  width: 2px;
  background-color: white;
  image-rendering: pixelated;
}

/* 右侧区域 */
.right-section {
  flex: 1;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* 聊天框 */
.chat-box {
  border: 2px solid white;
  padding: 12px;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  image-rendering: pixelated;
}

.chat-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.chat-line {
  font-family: 'Courier New', monospace;
  font-weight: bold;
  color: white;
  white-space: nowrap;
  image-rendering: pixelated;
}

.sender {
  font-size: 12px;
}

.message {
  font-size: 12px;
}

.dropdown-icon {
  margin-left: 8px;
}

.dropdown-svg {
  width: 16px;
  height: 16px;
  image-rendering: pixelated;
}

/* 猫咪面板 */
.cats-panel {
  border: 2px solid white;
  padding: 12px;
  image-rendering: pixelated;
}

.panel-title {
  font-family: 'Courier New', monospace;
  font-weight: bold;
  color: white;
  font-size: 12px;
  margin-bottom: 12px;
  white-space: nowrap;
}

.cat-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.cat-row:last-child {
  margin-bottom: 0;
}

.cat-avatar {
  width: 32px;
  height: 32px;
  flex-shrink: 0;
}

.cat-svg {
  width: 100%;
  height: 100%;
  image-rendering: pixelated;
  filter: none;
}

.cat-name {
  font-family: 'Courier New', monospace;
  font-weight: bold;
  color: white;
  font-size: 12px;
  min-width: 60px;
}

.hp-section {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 8px;
}

.hp-label {
  font-family: 'Courier New', monospace;
  font-weight: bold;
  color: white;
  font-size: 10px;
  min-width: 20px;
}

.hp-bar {
  flex: 1;
  height: 8px;
  border: 1px solid white;
  background-color: #000;
  image-rendering: pixelated;
}

.hp-fill {
  height: 100%;
  background-color: white;
  image-rendering: pixelated;
  transition: width 0.1s ease-out;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .pixel-canvas {
    flex-direction: column;
  }

  .divider-line {
    width: 100%;
    height: 2px;
  }

  .left-section {
    min-height: 200px;
  }

  .person-svg {
    width: 96px;
    height: 96px;
  }

  .right-section {
    padding: 12px;
    gap: 12px;
  }

  .chat-box,
  .cats-panel {
    padding: 8px;
  }
}

@media (prefers-reduced-motion: reduce) {
  .hp-fill {
    transition: none;
  }
}
</style>