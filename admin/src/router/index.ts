import { createRouter, createWebHistory } from 'vue-router';
import { isAuthenticated } from '../stores/auth';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
    },
    {
      path: '/',
      name: 'articles',
      component: () => import('../views/ArticleListView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/articles/new',
      name: 'article-new',
      component: () => import('../views/ArticleEditView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/articles/:id/edit',
      name: 'article-edit',
      component: () => import('../views/ArticleEditView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/projects',
      name: 'projects',
      component: () => import('../views/ProjectListView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/projects/new',
      name: 'project-new',
      component: () => import('../views/ProjectEditView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/projects/:id/edit',
      name: 'project-edit',
      component: () => import('../views/ProjectEditView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/skills',
      name: 'skills',
      component: () => import('../views/SkillListView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/troubleshooting',
      name: 'troubleshooting',
      component: () => import('../views/TroubleshootingListView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/troubleshooting/new',
      name: 'troubleshooting-new',
      component: () => import('../views/TroubleshootingEditView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/troubleshooting/:id/edit',
      name: 'troubleshooting-edit',
      component: () => import('../views/TroubleshootingEditView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/timeline',
      name: 'timeline',
      component: () => import('../views/TimelineListView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/timeline/new',
      name: 'timeline-new',
      component: () => import('../views/TimelineEditView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/timeline/:id/edit',
      name: 'timeline-edit',
      component: () => import('../views/TimelineEditView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('../views/ProfileView.vue'),
      meta: { requiresAuth: true },
    },
  ],
});

// 路由守卫：未登录跳转到 /login
router.beforeEach((to) => {
  if (to.meta.requiresAuth && !isAuthenticated()) {
    return { name: 'login' };
  }
});

export default router;
