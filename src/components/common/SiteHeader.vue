<script setup lang="ts">
import { Menu, X } from 'lucide-vue-next';
import { onBeforeUnmount, onMounted, ref } from 'vue';
import { RouterLink, useRoute, useRouter } from 'vue-router';
import { useProfile } from '../../composables/useProfile';

const { profile } = useProfile();
const route = useRoute();
const router = useRouter();
const open = ref(false);

const navItems = [
  { label: '首页', to: '/' },
  { label: '项目', to: '/projects' },
  { label: '技术栈', to: '/skills' },
  { label: '故障排查', to: '/troubleshooting' },
  { label: '文章', to: '/articles' },
  { label: '关于我', to: '/about' },
];

function isActive(to: string) {
  return to === '/' ? route.path === '/' : route.path.startsWith(to);
}

function handleNavCapture(event: MouseEvent) {
  const links = Array.from(document.querySelectorAll<HTMLAnchorElement>('[data-header-nav-link]'));
  const matchedLink = links.find((link) => {
    const rect = link.getBoundingClientRect();
    return (
      event.clientX >= rect.left &&
      event.clientX <= rect.right &&
      event.clientY >= rect.top &&
      event.clientY <= rect.bottom
    );
  });

  if (!matchedLink) {
    return;
  }

  event.preventDefault();
  event.stopPropagation();
  open.value = false;

  const href = matchedLink.getAttribute('href');
  if (!href) {
    return;
  }

  if (href.startsWith('/')) {
    void router.push(href);
    return;
  }

  window.open(href, matchedLink.target || '_self', 'noreferrer');
}

onMounted(() => {
  document.addEventListener('click', handleNavCapture, true);
});

onBeforeUnmount(() => {
  document.removeEventListener('click', handleNavCapture, true);
});
</script>

<template>
  <header class="site-header">
    <a class="skip-link" href="#main-content">跳到主要内容</a>
    <nav class="container nav-shell" aria-label="主导航">
      <RouterLink class="brand" to="/" @click="open = false">
        <span class="brand-mark">Y</span>
        <span>Yael</span>
      </RouterLink>
      <button class="menu-button" type="button" :aria-expanded="open" @click="open = !open">
        <Menu v-if="!open" :size="21" aria-hidden="true" />
        <X v-else :size="21" aria-hidden="true" />
        <span class="sr-only">打开或关闭导航</span>
      </button>
      <div class="nav-links" :class="{ 'nav-links--open': open }">
        <a
          v-for="item in navItems"
          :key="item.to"
          data-header-nav-link
          :href="item.to"
          :class="{ active: isActive(item.to) }"
          @click="open = false"
        >
          {{ item.label }}
        </a>
        <a data-header-nav-link :href="profile?.socialLinks.githubUrl" target="_blank" rel="noreferrer">GitHub</a>
      </div>
    </nav>
  </header>
</template>

<style scoped>
.site-header {
  position: fixed;
  z-index: 2000;
  top: 0;
  left: 0;
  width: 100%;
  pointer-events: auto;
  isolation: isolate;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  background: rgba(11, 16, 32, 0.72);
  backdrop-filter: blur(18px);
}

.skip-link {
  position: absolute;
  left: 12px;
  top: -60px;
  padding: 10px 14px;
  background: var(--color-accent);
  color: #071114;
  border-radius: var(--radius-small);
}

.skip-link:focus {
  top: 10px;
}

.nav-shell {
  position: relative;
  z-index: 2;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: clamp(42px, 18vw, 420px);
  min-height: 64px;
  pointer-events: auto;
}

.brand {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  font-weight: 800;
}

.brand-mark {
  display: grid;
  place-items: center;
  width: 34px;
  height: 34px;
  border-radius: var(--radius-small);
  background: #f7f8fc;
  color: #0b1020;
  font-size: 13px;
}

.nav-links {
  position: relative;
  z-index: 3;
  display: flex;
  align-items: center;
  gap: 4px;
  pointer-events: auto;
}

.nav-links a {
  position: relative;
  z-index: 4;
  display: inline-flex;
  align-items: center;
  padding: 10px 11px;
  border-radius: var(--radius-small);
  color: var(--color-text-secondary);
  font-size: 14px;
  pointer-events: auto;
  transition: color 160ms ease, background 160ms ease;
}

.nav-links a:hover,
.nav-links a.active {
  color: var(--color-text-primary);
  background: rgba(255, 255, 255, 0.07);
}

.menu-button {
  display: none;
  align-items: center;
  justify-content: center;
  width: 42px;
  height: 42px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-small);
  background: rgba(255, 255, 255, 0.05);
  color: var(--color-text-primary);
}

@media (max-width: 860px) {
  .nav-shell {
    justify-content: space-between;
    gap: 16px;
  }

  .menu-button {
    display: inline-flex;
  }

  .nav-links {
    position: absolute;
    top: 64px;
    left: 14px;
    right: 14px;
    display: none;
    flex-direction: column;
    align-items: stretch;
    padding: 12px;
    border: 1px solid var(--color-border);
    border-radius: var(--radius-medium);
    background: rgba(14, 20, 36, 0.98);
  }

  .nav-links--open {
    display: flex;
  }
}
</style>
