import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import ProjectsView from '../views/ProjectsView.vue';
import ProjectDetailView from '../views/ProjectDetailView.vue';
import SkillsView from '../views/SkillsView.vue';
import TroubleshootingView from '../views/TroubleshootingView.vue';
import ArticlesView from '../views/ArticlesView.vue';
import ArticleDetailView from '../views/ArticleDetailView.vue';
import AboutView from '../views/AboutView.vue';
import ResumeView from '../views/ResumeView.vue';

const router = createRouter({
  history: createWebHistory(),
  scrollBehavior() {
    return { top: 0 };
  },
  routes: [
    { path: '/', name: 'home', component: HomeView, meta: { title: '首页' } },
    { path: '/projects', name: 'projects', component: ProjectsView, meta: { title: '项目' } },
    { path: '/projects/:slug', name: 'project-detail', component: ProjectDetailView, meta: { title: '项目详情' } },
    { path: '/skills', name: 'skills', component: SkillsView, meta: { title: '技术方向' } },
    { path: '/troubleshooting', name: 'troubleshooting', component: TroubleshootingView, meta: { title: '故障排查' } },
    { path: '/articles', name: 'articles', component: ArticlesView, meta: { title: '文章' } },
    { path: '/articles/:slug', name: 'article-detail', component: ArticleDetailView, meta: { title: '文章详情' } },
    { path: '/about', name: 'about', component: AboutView, meta: { title: '关于我' } },
    { path: '/resume', name: 'resume', component: ResumeView, meta: { title: '简历' } },
  ],
});

router.afterEach((to) => {
  const pageTitle = typeof to.meta.title === 'string' ? to.meta.title : '作品集';
  document.title = `${pageTitle} | Yael`;
});

export default router;
