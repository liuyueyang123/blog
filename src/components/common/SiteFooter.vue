<script setup lang="ts">
import { Github, Mail } from 'lucide-vue-next';
import { profile } from '../../data/profile';
</script>

<template>
  <footer class="site-footer">
    <div class="container footer-grid">
      <div>
        <p class="footer-name">{{ profile.name }}</p>
        <p class="text-muted">{{ profile.focus }}</p>
      </div>
      <div class="footer-links">
        <a :href="profile.socialLinks.githubUrl" target="_blank" rel="noreferrer">
          <Github :size="18" aria-hidden="true" /> GitHub
        </a>
        <a :href="`mailto:${profile.socialLinks.email}`">
          <Mail :size="18" aria-hidden="true" /> Email
        </a>
      </div>
    </div>
    <div class="container copyright">(c) 2026 Yael. Built for portfolio, blog and interview showcase.</div>
  </footer>
</template>

<style scoped>
.site-footer {
  border-top: 1px solid var(--color-border);
  padding: 42px 0 28px;
  background: rgba(6, 9, 18, 0.62);
}

.footer-grid {
  display: flex;
  justify-content: space-between;
  gap: 24px;
}

.footer-name {
  margin: 0 0 8px;
  font-size: 20px;
  font-weight: 800;
}

.footer-links {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: 10px;
}

.footer-links a {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  min-height: 38px;
  padding: 0 12px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-small);
  color: var(--color-text-secondary);
}

.copyright {
  margin-top: 30px;
  color: var(--color-text-secondary);
  font-size: 13px;
}

@media (max-width: 720px) {
  .footer-grid {
    flex-direction: column;
  }

  .footer-links {
    justify-content: flex-start;
  }
}
</style>
