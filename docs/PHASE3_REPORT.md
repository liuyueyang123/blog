# 阶段 3 完成报告 — 文章 CRUD + 前端对接 + 后台管理

> 完成时间：2026-08-04
> 状态：✅ 全部测试通过

---

## 完成内容

### 1. 后端（backend/）

**新增文件：**

| 文件 | 说明 |
|------|------|
| `app/models/article.py` | Article ORM 模型（JSON 列存 content 段落数组） |
| `app/schemas/article.py` | Pydantic v2 schemas，`alias_generator=to_camel` 自动输出 camelCase |
| `app/services/article.py` | 文章 CRUD 业务逻辑 |
| `app/api/v1/articles.py` | 公开路由：GET /articles, GET /articles/{slug} |
| `app/api/v1/admin_articles.py` | 管理路由：GET/POST/PUT/DELETE /admin/articles |
| `app/db/seed_articles.py` | Seed 脚本：导入前端现有 5 篇文章 |

**数据库：**
- MySQL `portfolio_blog.articles` 表已创建并导入 5 条数据
- 字段与前端 `Article` 接口完全对齐（camelCase 响应）

### 2. 前端（src/）

**新增文件：**

| 文件 | 说明 |
|------|------|
| `src/api/client.ts` | axios 实例 + 响应拦截器 |
| `src/api/articles.ts` | getArticles() / getArticleBySlug() |
| `src/composables/useArticles.ts` | useArticles() / useArticle(slug)，封装 loading/error |

**修改文件（最小改动）：**

| 文件 | 改动 |
|------|------|
| `vite.config.ts` | +7 行：server.proxy `/api` → localhost:8000 |
| `src/views/ArticlesView.vue` | 改 1 行 import → useArticles() |
| `src/views/ArticleDetailView.vue` | 改 import + find → useArticle(slug) |
| `src/views/HomeView.vue` | 改 1 行 import → useArticles()（其余 4 个 data 暂未迁移） |

**清理：**
- 删除 `vite.config.js` / `vite.config.d.ts`（vue-tsc 编译产物，会覆盖 vite.config.ts 的 proxy 配置）
- `.gitignore` 新增忽略这两个编译产物

> ⚠️ 组件模板、GSAP 动画、CSS 全部未动。

### 3. 后台（admin/）— 全新 Vue3 项目

```
admin/
├── package.json          # vue3 + vite + axios + vue-router
├── vite.config.ts        # port 5174, proxy /api → 8000
├── index.html
├── tsconfig.json
└── src/
    ├── main.ts
    ├── App.vue
    ├── styles/admin.css   # 暗色管理后台样式
    ├── router/index.ts    # 路由 + 登录守卫
    ├── stores/auth.ts     # token 存取（localStorage）
    ├── api/client.ts      # axios + JWT 拦截器 + 401 跳转
    ├── api/articles.ts    # login + 文章 CRUD API
    └── views/
        ├── LoginView.vue       # 登录页
        ├── ArticleListView.vue # 文章列表 + 删除
        └── ArticleEditView.vue # 新增/编辑表单
```

---

## 测试结果

### 后端 API

| 测试项 | 结果 |
|--------|------|
| GET /api/v1/articles（列表，camelCase） | ✅ total: 5 |
| GET /api/v1/articles/{slug}（详情） | ✅ readTime 字段正确 |
| GET /api/v1/articles/nonexistent | ✅ 404 |
| POST /admin/articles（创建） | ✅ |
| PUT /admin/articles/{id}（更新） | ✅ |
| DELETE /admin/articles/{id}（删除） | ✅ |
| 无 token 访问 /admin/* | ✅ 401 |

### 前端集成

| 测试项 | 结果 |
|--------|------|
| Vite proxy /api → 8000 | ✅ |
| 文章列表经 proxy 返回 camelCase | ✅ |
| 文章详情 readTime 字段对齐 | ✅ |
| `vite build` 成功 | ✅ |

### 后台集成

| 测试项 | 结果 |
|--------|------|
| admin 构建成功（代码分割） | ✅ |
| 登录 → 返回 JWT | ✅ |
| 文章列表（带 token） | ✅ 5 条 |

---

## 本地运行方式

```bash
# 1. 后端
cd backend
source venv/Scripts/activate
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

# 2. 前端主站
cd ..
npm run dev          # http://localhost:5173

# 3. 后台管理
cd admin
npm run dev          # http://localhost:5174
```

后台登录：`admin / admin123`

---

## 下一步（阶段 4：项目管理）

- [ ] Project 模型 + schema + service
- [ ] 公开 API：GET /projects, GET /projects/{slug}
- [ ] 管理 API：CRUD /admin/projects
- [ ] Seed：导入现有 5 个项目
- [ ] 前端：src/api/projects.ts + useProjects() + 视图改 import
- [ ] 后台：项目管理页面
