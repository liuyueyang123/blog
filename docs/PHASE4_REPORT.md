# 阶段 4 完成报告 — 项目管理

> 完成时间：2026-08-04
> 状态：✅ 全部测试通过

---

## 完成内容

### 1. 后端（backend/）

**新增文件：**

| 文件 | 说明 |
|------|------|
| `app/models/project.py` | Project ORM 模型（tags/highlights 用 JSON 列） |
| `app/schemas/project.py` | Pydantic v2 schemas，camelCase 输出 |
| `app/services/project.py` | 项目 CRUD 业务逻辑 |
| `app/api/v1/projects.py` | 公开路由：GET /projects, GET /projects/{slug} |
| `app/api/v1/admin_projects.py` | 管理路由：CRUD /admin/projects |
| `app/db/seed_projects.py` | Seed 脚本：导入前端现有 5 个项目 |

**数据库：**
- MySQL `portfolio_blog.projects` 表已创建并导入 5 条数据
- 字段与前端 `Project` 接口完全对齐（coverTone, githubUrl 等 camelCase）

### 2. 前端（src/）

**新增文件：**

| 文件 | 说明 |
|------|------|
| `src/api/projects.ts` | getProjects() / getProjectBySlug() |
| `src/composables/useProjects.ts` | useProjects() / useProject(slug) |

**修改文件（最小改动）：**

| 文件 | 改动 |
|------|------|
| `src/views/ProjectsView.vue` | 改 1 行 import → useProjects() |
| `src/views/ProjectDetailView.vue` | 改 import + find → useProject(slug) |
| `src/views/HomeView.vue` | 改 1 行 import → useProjects() |

> ⚠️ 组件模板、GSAP 动画、CSS 全部未动。ProjectCard 本就是 props 驱动，无需改动。

### 3. 后台（admin/）

**新增文件：**

| 文件 | 说明 |
|------|------|
| `src/api/projects.ts` | 项目 CRUD API |
| `src/components/AdminNav.vue` | 共享导航头（文章/项目切换 + 退出） |
| `src/views/ProjectListView.vue` | 项目列表 + 删除 |
| `src/views/ProjectEditView.vue` | 新增/编辑表单（标签逗号分隔、亮点换行分隔、封面色调下拉） |

**修改文件：**

| 文件 | 改动 |
|------|------|
| `src/router/index.ts` | +3 条项目路由 |
| `src/views/ArticleListView.vue` | 改用 AdminNav 共享导航 |

---

## 测试结果

| 测试项 | 结果 |
|--------|------|
| GET /api/v1/projects（列表，camelCase） | ✅ total: 5 |
| GET /api/v1/projects/{slug}（详情） | ✅ coverTone/githubUrl/highlights 正确 |
| POST /admin/projects（创建） | ✅ |
| DELETE /admin/projects/{id}（删除） | ✅ |
| 前端 `vite build` | ✅ |
| admin `vite build`（代码分割） | ✅ |
| admin 项目列表（带 token） | ✅ 5 条 |

---

## 当前前端数据迁移进度

| 数据 | API 迁移 | 视图 |
|------|---------|------|
| articles | ✅ | ArticlesView, ArticleDetailView, HomeView |
| projects | ✅ | ProjectsView, ProjectDetailView, HomeView |
| skills | 🔲 阶段 5 | SkillsView, HomeView |
| troubleshooting | 🔲 阶段 6 | TroubleshootingView, HomeView |
| timeline | 🔲 阶段 6 | HomeView, AboutView |
| profile | 🔲 阶段 6 | AboutView, SiteFooter, SiteHeader, CapabilityOverview |

---

## 下一步（阶段 5：技能管理）

- [ ] SkillGroup + SkillItem 模型（1:N 关系）
- [ ] 公开 API：GET /skills（返回嵌套的组+项）
- [ ] 管理 API：技能组 CRUD + 技能项 CRUD
- [ ] Seed：导入现有 4 组 28 项技能
- [ ] 前端：src/api/skills.ts + useSkills() + 视图改 import
- [ ] 后台：技能管理页面（组+项双层编辑）
