# BACKEND_PLAN.md — 后端开发总体规划

> 生成时间：2026-07-30
> 状态：**待确认** — 请审阅后确认，确认后进入第二阶段开发
> 原则：不修改前端 UI / 动画 / 组件命名 / 目录结构，仅替换数据来源

---

## ① 当前项目结构分析

### 1.1 技术栈

| 层面 | 技术 | 版本 |
|------|------|------|
| 框架 | Vue 3 | ^3.5.0 |
| 构建 | Vite | ^7.0.0 |
| 语言 | TypeScript | ^5.5.0 |
| 路由 | Vue Router | ^4.4.0 |
| 动画 | GSAP + ScrollTrigger | ^3.13.0 |
| 图标 | lucide-vue-next | ^0.468.0 |
| 样式 | 纯 CSS（CSS Custom Properties） | — |

### 1.2 当前缺失

| 缺失项 | 说明 |
|--------|------|
| **HTTP 客户端** | 无 axios / fetch 封装，无 API 调用能力 |
| **状态管理** | 无 Pinia / Vuex，各视图直接 import 静态数据 |
| **后端 API** | `VITE_API_BASE_URL` 为空，无任何后端服务 |
| **Vite 代理** | vite.config.ts 无 server.proxy 配置 |
| **路径别名** | 无 `@/` 别名，全部使用相对路径 |
| **测试框架** | 无 Vitest / Jest |
| **代码规范** | 无 ESLint / Prettier |
| **404 路由** | 无 catch-all 路由 |
| **SEO 管理** | 无 vueuse/head 等 |

### 1.3 目录结构（现状）

```
E:\BLOG/
├── index.html                    # 入口 HTML（zh-CN, dark theme）
├── package.json                  # 6 deps + 2 devDeps
├── vite.config.ts                # 极简配置，仅 vue() 插件
├── tsconfig.json                 # strict 模式
├── .env.example                  # VITE_SITE_NAME + VITE_API_BASE_URL（空）
├── src/
│   ├── main.ts                   # createApp + router + main.css
│   ├── App.vue                   # 布局骨架：SiteHeader + RouterView + SiteFooter + CursorGlow
│   ├── router/index.ts           # 9 条路由，全部 eager import
│   ├── types/content.ts          # 7 个类型定义
│   ├── data/                     # ★ 7 个静态数据文件（全部硬编码）
│   │   ├── articles.ts           #   5 篇文章
│   │   ├── projects.ts           #   5 个项目
│   │   ├── skills.ts             #   4 组 28 项技能
│   │   ├── troubleshooting.ts    #   4 个故障案例
│   │   ├── timeline.ts           #   6 个时间线阶段
│   │   ├── profile.ts            #   1 个个人资料 + 4 张能力卡片
│   │   └── socialLinks.ts        #   1 个社交链接（多为占位符）
│   ├── composables/
│   │   └── useGsap.ts            # GSAP ScrollTrigger 封装（55 行）
│   ├── assets/styles/
│   │   └── main.css              # 全局样式（257 行，16 个 CSS 变量）
│   ├── components/
│   │   ├── common/               # 5 个通用组件
│   │   ├── home/                 # 4 个首页组件
│   │   ├── projects/             # 1 个项目卡片
│   │   ├── skills/               # 1 个技能组卡片
│   │   └── troubleshooting/      # 1 个故障卡片
│   └── views/                    # 9 个页面视图
├── docs/                         # 项目文档
└── public/                       # 静态资源
```

### 1.4 路由结构

| # | 路径 | 名称 | 组件 | 动态参数 |
|---|------|------|------|---------|
| 1 | `/` | home | HomeView | — |
| 2 | `/projects` | projects | ProjectsView | — |
| 3 | `/projects/:slug` | project-detail | ProjectDetailView | `:slug` |
| 4 | `/skills` | skills | SkillsView | — |
| 5 | `/troubleshooting` | troubleshooting | TroubleshootingView | — |
| 6 | `/articles` | articles | ArticlesView | — |
| 7 | `/articles/:slug` | article-detail | ArticleDetailView | `:slug` |
| 8 | `/about` | about | AboutView | — |
| 9 | `/resume` | resume | ResumeView | — |

---

## ② 前端已有哪些模块

### 2.1 页面模块（9 个视图）

| 视图 | 功能 | 数据来源 | 使用动画 |
|------|------|---------|---------|
| **HomeView** | 首页聚合展示 | articles, projects, skills, troubleshooting, timeline（5 个） | useRevealAnimations |
| **ProjectsView** | 项目列表 | projects | useRevealAnimations |
| **ProjectDetailView** | 项目详情 | projects（slug 查找） | 无 |
| **SkillsView** | 技能列表 | skills | useRevealAnimations |
| **TroubleshootingView** | 故障排查列表 | troubleshooting | useRevealAnimations |
| **ArticlesView** | 文章列表 | articles | 无 |
| **ArticleDetailView** | 文章详情 | articles（slug 查找） | 无 |
| **AboutView** | 关于我 | profile, timeline（2 个） | 无 |
| **ResumeView** | 简历（占位） | 无 | 无 |

### 2.2 组件模块（12 个组件）

**通用组件（common/）：**

| 组件 | 功能 | 数据依赖 | 动画 |
|------|------|---------|------|
| SiteHeader | 固定导航栏 + 移动端菜单 | socialLinks（GitHub 链接）+ 硬编码 navItems | 无 |
| SiteFooter | 页脚 | profile（name, focus, socialLinks） | 无 |
| CursorGlow | 鼠标跟随光效 + 粒子 | 无 | CSS keyframes |
| MagneticButton | 磁吸按钮 | 无 | GSAP（重度） |
| SectionHeader | 章节标题 | 无（纯 props） | 无 |

**首页组件（home/）：**

| 组件 | 功能 | 数据依赖 | 动画 |
|------|------|---------|------|
| HeroSection | 首屏（标题 + 终端卡片 + 照片墙） | 硬编码标题/终端文本，80帧 PNG 序列 | CSS bounce + rAF 帧动画 |
| CapabilityOverview | 技术方向概览（4 张卡片） | capabilityCards（来自 profile.ts） | data-stagger |
| EngineeringMap | 工程流程图 | 无（全部硬编码在模板中） | data-reveal |
| PixelAnimationSection | 像素风装饰动画 | 无（手绘 SVG） | rAF 正弦波 |

**业务组件：**

| 组件 | 功能 | Props 类型 | 数据依赖 |
|------|------|-----------|---------|
| ProjectCard | 项目卡片 | `Project` | 无（纯 props 驱动）✅ |
| SkillGroupCard | 技能组卡片 | `SkillGroup` | 无（纯 props 驱动）✅ |
| TroubleCard | 故障案例卡片 | `TroubleshootingCase` | 无（纯 props 驱动）✅ |

### 2.3 动画系统

| 机制 | 实现 | 使用位置 |
|------|------|---------|
| `useRevealAnimations()` | GSAP ScrollTrigger 封装 | HomeView, ProjectsView, SkillsView, TroubleshootingView |
| `data-hero-reveal` | 首屏入场动画 | HeroSection（5 个元素） |
| `data-reveal` | 滚动淡入 | SectionHeader, ProjectCard, SkillGroupCard, TroubleCard, EngineeringMap |
| `data-stagger` | 子元素交错动画 | HomeView 文章/时间线列表, CapabilityOverview |
| MagneticButton | GSAP 磁吸效果 | HeroSection CTA 按钮 |
| CursorGlow | CSS 粒子 + 鼠标跟随 | App.vue 全局 |
| 页面过渡 | Vue Transition（180ms） | App.vue RouterView |
| prefers-reduced-motion | CSS + JS 双重支持 | 全局 |

### 2.4 类型系统（src/types/content.ts）

| 类型 | 字段数 | 使用位置 |
|------|--------|---------|
| `Status` | 4 个联合值 | SkillItem.status |
| `SkillItem` | 4 字段 | skills 数据 |
| `SkillGroup` | 3 字段 | skills 数据, SkillGroupCard |
| `Project` | 10 字段 | projects 数据, ProjectCard |
| `TroubleshootingCase` | 8 字段 | troubleshooting 数据, TroubleCard |
| `Article` | 7 字段 | articles 数据, ArticleDetailView |
| `TimelineItem` | 3 字段 | timeline 数据 |

> ⚠️ **类型缺失**：`profile.ts` 和 `socialLinks.ts` 的数据没有定义 TypeScript 接口，使用类型推断。后续应在 `content.ts` 中补充 `Profile`、`CapabilityCard`、`SocialLinks` 类型。

---

## ③ 哪些地方已经写死

### 3.1 静态数据文件（src/data/）— 53 条记录

| 文件 | 导出 | 记录数 | 状态 |
|------|------|--------|------|
| `articles.ts` | `articles` | 5 篇文章 | 模拟数据，内容为 2 段式占位 |
| `projects.ts` | `projects` | 5 个项目 | 半真实数据，githubUrl 全为占位符 |
| `skills.ts` | `skillGroups` | 4 组 28 项 | 真实数据 |
| `troubleshooting.ts` | `troubleshootingCases` | 4 个案例 | 半真实数据 |
| `timeline.ts` | `timeline` | 6 个阶段 | 真实数据 |
| `profile.ts` | `profile`, `capabilityCards` | 1 + 4 | 真实数据，socialLinks 为占位 |
| `socialLinks.ts` | `socialLinks` | 1 个对象 6 字段 | 5/6 为 `TODO_REPLACE` 占位符 |

### 3.2 组件内硬编码内容

| 组件 | 硬编码内容 |
|------|-----------|
| **SiteHeader** | 6 个导航项（首页/项目/技术栈/故障排查/文章/关于我）|
| **HeroSection** | 标题 `"Hello, I'm Yael."`、终端 whoami/focus/status 内容、CTA 目标路径、帧动画配置（80帧/12fps） |
| **EngineeringMap** | 6 个流程节点标签（Code/Build/Deploy/Observe/Debug/Review）、全部描述文本 |
| **CapabilityOverview** | SectionHeader 的 eyebrow/title 文本 |
| **ProjectDetailView** | 卡片标题（我的工作/量化结果/关键内容）、GitHub 占位链接文本 |
| **ArticleDetailView** | 回退文本（没有找到这篇文章/返回文章列表） |
| **AboutView** | 页面介绍文本（部分混合静态+数据） |
| **ResumeView** | 整页内容 100% 硬编码 |
| **SiteFooter** | 版权声明 |
| 各列表页 | SectionHeader 的 eyebrow/title/copy（共约 18 个中文字符串） |

### 3.3 配置层硬编码

| 位置 | 硬编码 |
|------|--------|
| `index.html` | 站点标题 `Yael \| Linux Cloud SRE AI Portfolio`、meta description、theme-color `#0b1020` |
| `.env.example` | `VITE_API_BASE_URL` 为空 |
| `main.css` | 16 个 CSS 变量值（颜色/圆角/阴影/间距） |
| `App.vue` | 全局背景图路径 `/images/global-starlight-portrait-cutout.png` |

---

## ④ 哪些地方需要 API

### 4.1 需要 API 的视图（8/9）

按迁移优先级排序：

| 优先级 | 视图 | 当前数据源 | 需要的 API |
|--------|------|-----------|-----------|
| 🔴 P0 | HomeView | 5 个 data 文件 | 多个列表 API（articles, projects, skills, troubleshooting, timeline） |
| 🔴 P0 | ArticlesView | articles | `GET /api/articles` |
| 🔴 P0 | ArticleDetailView | articles + slug | `GET /api/articles/{slug}` |
| 🔴 P0 | ProjectsView | projects | `GET /api/projects` |
| 🔴 P0 | ProjectDetailView | projects + slug | `GET /api/projects/{slug}` |
| 🟡 P1 | SkillsView | skills | `GET /api/skills` |
| 🟡 P1 | TroubleshootingView | troubleshooting | `GET /api/troubleshooting` |
| 🟡 P1 | AboutView | profile + timeline | `GET /api/profile` + `GET /api/timeline` |
| ⚪ 不需要 | ResumeView | 无 | 纯占位页 |

### 4.2 需要 API 的组件（3 个高优先级）

| 优先级 | 组件 | 当前数据源 | 改造方案 |
|--------|------|-----------|---------|
| 🔴 高 | SiteFooter | `import profile from data/profile` | 改为从 Pinia store 或 composable 获取 |
| 🔴 高 | CapabilityOverview | `import capabilityCards from data/profile` | 同上 |
| 🟡 中 | SiteHeader | `import socialLinks from data/socialLinks` | 同上 |

### 4.3 不需要 API 的组件（9 个）

CursorGlow、MagneticButton、SectionHeader、PixelAnimationSection、EngineeringMap（模板内硬编码文本，非数据驱动）、HeroSection（品牌内容，非数据库内容）、ProjectCard、SkillGroupCard、TroubleCard（已为 props 驱动）。

### 4.4 前端需要新增的基础设施

| 需要新增 | 说明 |
|---------|------|
| **HTTP 客户端** | 推荐 axios，封装统一请求/响应拦截器 |
| **Pinia 状态管理** | 管理 profile、socialLinks 等全局共享数据 |
| **API composables** | `useArticles()`, `useProjects()` 等，封装加载状态和错误处理 |
| **Vite 代理** | 开发环境 `server.proxy` 转发 `/api` → `http://localhost:8000` |
| **环境变量** | 填充 `VITE_API_BASE_URL` |

---

## ⑤ 哪些地方需要数据库

### 5.1 需要入库的数据

| 数据 | 当前来源 | 记录数 | 入库原因 |
|------|---------|--------|---------|
| 文章 | articles.ts | 5 | 需要后台 CRUD，内容会持续增长 |
| 项目 | projects.ts | 5 | 需要后台 CRUD，含详情/标签/高亮 |
| 技能 | skills.ts | 4 组 28 项 | 需要后台管理技能列表和状态 |
| 故障案例 | troubleshooting.ts | 4 | 需要后台 CRUD，案例库会增长 |
| 时间线 | timeline.ts | 6 | 需要后台管理成长路径 |
| 个人资料 | profile.ts | 1 | 需要后台编辑个人信息 |
| 能力卡片 | profile.ts | 4 | 需要后台管理首页展示 |
| 社交链接 | socialLinks.ts | 1 | 需要后台配置，当前全为占位符 |
| 管理员 | 无 | 0 | 后台登录认证 |

### 5.2 不需要入库的数据

| 数据 | 原因 |
|------|------|
| navItems（导航菜单） | 固定 6 项，与路由绑定，不需动态管理 |
| HeroSection 标题/终端文本 | 品牌内容，极少变化，保持硬编码 |
| EngineeringMap 节点 | 装饰性内容，非数据驱动 |
| PixelAnimationSection | 纯艺术装饰 |
| CSS 变量/主题 | 前端设计系统，不属于内容管理 |
| 帧动画配置 | 静态资源配置 |

---

## ⑥ 哪些地方需要后台

### 6.1 后台管理功能清单

| 模块 | 功能 | 对应前端页面 |
|------|------|-------------|
| **登录认证** | 管理员账号密码登录、JWT token、登出 | 后台登录页 |
| **文章管理** | 列表 / 新增 / 编辑 / 删除 / 发布切换 | ArticlesView, ArticleDetailView |
| **项目管理** | 列表 / 新增 / 编辑 / 删除 / 标签管理 | ProjectsView, ProjectDetailView |
| **技能管理** | 技能组 CRUD / 技能项 CRUD / 排序 | SkillsView |
| **故障排查管理** | 列表 / 新增 / 编辑 / 删除 | TroubleshootingView |
| **时间线管理** | 列表 / 新增 / 编辑 / 删除 / 排序 | HomeView 时间线, AboutView |
| **个人资料管理** | 编辑姓名/头衔/介绍/位置 | AboutView, SiteFooter |
| **能力卡片管理** | 编辑首页 4 张方向卡片 | CapabilityOverview |
| **社交链接管理** | 编辑 GitHub/邮箱/B站/抖音/小红书链接 | SiteHeader, SiteFooter |
| **图片上传** | 上传项目封面/文章配图/头像 | 各模块 |
| **网站设置** | 站点名称、SEO 描述（远期） | index.html meta |

### 6.2 后台技术栈

| 技术 | 说明 |
|------|------|
| Vue 3 + Vite + TypeScript | 与主站技术栈一致 |
| 独立目录 `admin/` | 独立构建，独立部署 |
| 使用主站 API | 通过 `/api/admin/*` 端点操作数据 |
| JWT 认证 | 登录后获取 token，存 localStorage，请求头携带 |

---

## ⑦ 前后端如何解耦

### 7.1 解耦原则

> **核心原则：只替换数据来源，不动 UI 层。**

```
当前架构：
  View → import data/*.ts → 渲染

目标架构：
  View → composable/store → HTTP Client → FastAPI → MySQL
                                    ↕
                              admin/ (后台管理)
```

### 7.2 解耦策略（按层说明）

#### 第一层：类型定义保持不变

`src/types/content.ts` 中的 7 个接口 **完全保留**，作为前后端数据契约。
后端 Pydantic schemas 的字段名和类型 **必须与这些接口一一对应**。

需要补充 3 个缺失类型：
```typescript
// 新增到 src/types/content.ts
interface Profile {
  name: string
  handle: string
  title: string
  focus: string
  intro: string
  location: string
}

interface CapabilityCard {
  title: string
  tech: string
  practice: string
}

interface SocialLinks {
  githubUrl: string
  email: string
  bilibiliUrl: string
  douyinUrl: string
  xiaohongshuUrl: string
  resumeUrl: string
}
```

#### 第二层：新增 API 层（src/api/）

```
src/api/
├── client.ts          # axios 实例 + 拦截器
├── articles.ts        # getArticles(), getArticleBySlug()
├── projects.ts        # getProjects(), getProjectBySlug()
├── skills.ts          # getSkillGroups()
├── troubleshooting.ts # getCases(), getCaseBySlug()
├── timeline.ts        # getTimeline()
└── profile.ts         # getProfile(), getSocialLinks(), getCapabilityCards()
```

#### 第三层：新增 Composables（src/composables/）

```
src/composables/
├── useGsap.ts          # 已有，不动
├── useArticles.ts      # 新增：封装文章列表/详情获取 + loading/error
├── useProjects.ts      # 新增
├── useSkills.ts        # 新增
├── useTroubleshooting.ts # 新增
├── useTimeline.ts      # 新增
└── useProfile.ts       # 新增
```

每个 composable 返回 `{ data, loading, error }`，视图组件使用方式：

```typescript
// 改造前（当前）
import { articles } from '../data/articles'

// 改造后（目标）
const { data: articles, loading, error } = useArticles()
```

#### 第四层：视图层改造（最小化）

每个视图只需改 **1-2 行 import**，模板和动画完全不动。

```diff
// HomeView.vue
- import { articles } from '../data/articles'
- import { projects } from '../data/projects'
- import { skillGroups } from '../data/skills'
- import { troubleshootingCases } from '../data/troubleshooting'
- import { timeline } from '../data/timeline'
+ const { data: articles } = useArticles()
+ const { data: projects } = useProjects()
+ const { data: skillGroups } = useSkills()
+ const { data: troubleshootingCases } = useTroubleshooting()
+ const { data: timeline } = useTimeline()
```

模板中的 `v-for`、GSAP 动画、组件 props 传递 **全部不变**。

#### 第五层：Vite 配置

```typescript
// vite.config.ts 新增
export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      }
    }
  }
})
```

#### 第六层：data/ 文件的过渡处理

**不立即删除** `src/data/*.ts`，而是：
1. 开发期间作为 API 未就绪时的降级数据
2. 可在 composable 中实现 fallback：API 失败时使用本地数据
3. 所有 API 对接完成并测试通过后，再删除 data/ 目录

### 7.3 不受影响的部分（明确不动）

| 不动的部分 | 原因 |
|-----------|------|
| 所有 `.vue` 组件的模板 | UI 不变 |
| 所有 GSAP 动画 | 动画与数据无关 |
| CSS / 设计系统 | 样式不变 |
| 路由定义 | 路由结构不变 |
| 组件命名 / 目录结构 | 不重构 |
| types/content.ts 现有类型 | 作为前后端契约 |
| useGsap.ts | 动画封装不变 |
| public/ 静态资源 | 不变 |

---

## ⑧ 推荐的数据库设计

### 8.1 设计原则

- **逐步演进**：第一阶段只建 6 张表，后续按需扩展
- **与前端类型对齐**：字段名与 `types/content.ts` 接口一致（snake_case 转换）
- **slug 为业务主键**：前端路由已使用 slug，保持一致
- **JSON 字段适度使用**：数组类字段（tags, highlights, tools, content）第一阶段用 JSON，避免过多关联表

### 8.2 第一阶段表结构（6 张表）

#### `admins` — 管理员

```sql
CREATE TABLE admins (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    username      VARCHAR(50)  NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,          -- bcrypt
    display_name  VARCHAR(100) NOT NULL,
    is_active     BOOLEAN      NOT NULL DEFAULT TRUE,
    created_at    DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at    DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

#### `articles` — 文章

```sql
CREATE TABLE articles (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    slug       VARCHAR(200) NOT NULL UNIQUE,
    title      VARCHAR(300) NOT NULL,
    category   VARCHAR(100) NOT NULL,             -- 'SRE', 'AI', 'Linux' 等
    excerpt    TEXT         NOT NULL,
    date       DATE         NOT NULL,              -- 前端 string → 数据库 DATE
    read_time  VARCHAR(50)  NOT NULL DEFAULT '5 min',
    content    JSON         NOT NULL,              -- string[] 段落数组
    is_published BOOLEAN    NOT NULL DEFAULT TRUE,
    sort_order INT          NOT NULL DEFAULT 0,
    created_at DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

> `content` 使用 JSON 列存储 `["段落1", "段落2", ...]`，与前端 `Article.content: string[]` 完全对应。

#### `projects` — 项目

```sql
CREATE TABLE projects (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    slug        VARCHAR(200) NOT NULL UNIQUE,
    title       VARCHAR(300) NOT NULL,
    subtitle    VARCHAR(500) NOT NULL,
    cover_tone  VARCHAR(50)  NOT NULL DEFAULT 'default',  -- 'vision','terminal','depth','sre','web'
    tags        JSON         NOT NULL,                     -- string[]
    role        TEXT         NOT NULL,
    result      TEXT         NOT NULL,
    overview    TEXT         NOT NULL,
    highlights  JSON         NOT NULL,                     -- string[]
    github_url  VARCHAR(500) NOT NULL DEFAULT '',
    is_published BOOLEAN     NOT NULL DEFAULT TRUE,
    sort_order  INT          NOT NULL DEFAULT 0,
    created_at  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

#### `skill_groups` — 技能组

```sql
CREATE TABLE skill_groups (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    title      VARCHAR(200) NOT NULL,
    summary    VARCHAR(500) NOT NULL DEFAULT '',
    sort_order INT          NOT NULL DEFAULT 0,
    created_at DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

#### `skill_items` — 技能项

```sql
CREATE TABLE skill_items (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    group_id   INT          NOT NULL,
    name       VARCHAR(100) NOT NULL,
    direction  VARCHAR(200) NOT NULL DEFAULT '',
    scenario   TEXT         NOT NULL,
    status     ENUM('有项目实践','能够独立完成基础操作','能够排查常见问题','正在系统学习') NOT NULL,
    sort_order INT          NOT NULL DEFAULT 0,
    created_at DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (group_id) REFERENCES skill_groups(id) ON DELETE CASCADE
);
```

#### `profile` — 个人资料（单行配置表）

```sql
CREATE TABLE profile (
    id               INT AUTO_INCREMENT PRIMARY KEY,
    name             VARCHAR(100) NOT NULL DEFAULT 'Yael',
    handle           VARCHAR(100) NOT NULL DEFAULT 'yael',
    title            VARCHAR(300) NOT NULL DEFAULT '',
    focus            VARCHAR(500) NOT NULL DEFAULT '',
    intro            TEXT,
    location         VARCHAR(100) NOT NULL DEFAULT 'China',
    github_url       VARCHAR(500) NOT NULL DEFAULT '',
    email            VARCHAR(300) NOT NULL DEFAULT '',
    bilibili_url     VARCHAR(500) NOT NULL DEFAULT '',
    douyin_url       VARCHAR(500) NOT NULL DEFAULT '',
    xiaohongshu_url  VARCHAR(500) NOT NULL DEFAULT '',
    resume_url       VARCHAR(500) NOT NULL DEFAULT '',
    capability_cards JSON,               -- [{title, tech, practice}, ...]
    updated_at       DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

> 将 `profile` + `socialLinks` + `capabilityCards` 合并为一张表。`capability_cards` 用 JSON 存储 4 张卡片。第一阶段足够用，后续如需单独管理可拆表。

### 8.3 后续阶段扩展表

| 阶段 | 新增表 | 说明 |
|------|--------|------|
| 第四阶段 | `troubleshooting_cases` | slug, title, symptom, process, tools(JSON), root_cause, resolution, review |
| 第五阶段 | `timeline_items` | time_label, title, detail, sort_order |
| 第七阶段 | `images` | filename, path, mime_type, size, uploaded_by, created_at |
| 远期 | `categories` | 文章分类独立表（当前 category 为自由文本） |
| 远期 | `tags` + `project_tags` | 标签规范化（当前 tags 为 JSON 数组） |

### 8.4 ER 关系图（第一阶段）

```
admins ────────────── (独立，无外键关联)

articles ──────────── (独立)

projects ──────────── (独立)

skill_groups ──┐
               ├── 1:N ── skill_items
               │
profile ─────────────── (独立，单行)
```

> 第一阶段表之间 **几乎无关联**（仅 skill_groups ↔ skill_items），这是有意为之。
> 前端数据文件之间也只有 socialLinks → profile/projects 的引用关系。
> 文章↔故障案例、项目↔技能之间的关联是语义上的，暂不做外键。

---

## ⑨ 推荐 API 设计

### 9.1 API 设计原则

- RESTful 风格
- 前缀 `/api/v1/`（版本化，便于后续演进）
- 公开接口无需认证（前端展示用）
- 管理接口需 JWT Bearer Token
- 响应格式统一
- 字段名使用 **camelCase**（与前端 TypeScript 接口直接对应，避免转换）

### 9.2 统一响应格式

```json
// 成功 - 单条
{
  "code": 0,
  "message": "ok",
  "data": { ... }
}

// 成功 - 列表
{
  "code": 0,
  "message": "ok",
  "data": [ ... ],
  "total": 5
}

// 错误
{
  "code": 40001,
  "message": "Article not found",
  "data": null
}
```

### 9.3 公开 API（前端展示用，无需认证）

| 方法 | 路径 | 说明 | 对应前端 |
|------|------|------|---------|
| GET | `/api/v1/articles` | 文章列表（已发布） | ArticlesView, HomeView |
| GET | `/api/v1/articles/{slug}` | 文章详情 | ArticleDetailView |
| GET | `/api/v1/projects` | 项目列表（已发布） | ProjectsView, HomeView |
| GET | `/api/v1/projects/{slug}` | 项目详情 | ProjectDetailView |
| GET | `/api/v1/skills` | 技能组列表（含技能项） | SkillsView, HomeView |
| GET | `/api/v1/troubleshooting` | 故障案例列表 | TroubleshootingView, HomeView |
| GET | `/api/v1/troubleshooting/{slug}` | 故障案例详情 | （远期详情页） |
| GET | `/api/v1/timeline` | 时间线列表 | HomeView, AboutView |
| GET | `/api/v1/profile` | 个人资料 + 社交链接 + 能力卡片 | AboutView, SiteFooter, SiteHeader, CapabilityOverview |

### 9.4 认证 API

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/v1/auth/login` | 管理员登录，返回 JWT |
| GET | `/api/v1/auth/me` | 获取当前管理员信息 |
| POST | `/api/v1/auth/refresh` | 刷新 token（远期） |

### 9.5 管理 API（需 JWT 认证）

所有管理接口前缀：`/api/v1/admin/`

**文章管理：**

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/admin/articles` | 全部文章（含未发布） |
| POST | `/api/v1/admin/articles` | 新增文章 |
| PUT | `/api/v1/admin/articles/{id}` | 更新文章 |
| DELETE | `/api/v1/admin/articles/{id}` | 删除文章 |

**项目管理：**

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/admin/projects` | 全部项目 |
| POST | `/api/v1/admin/projects` | 新增项目 |
| PUT | `/api/v1/admin/projects/{id}` | 更新项目 |
| DELETE | `/api/v1/admin/projects/{id}` | 删除项目 |

**技能管理：**

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/admin/skills` | 全部技能组 + 项 |
| POST | `/api/v1/admin/skill-groups` | 新增技能组 |
| PUT | `/api/v1/admin/skill-groups/{id}` | 更新技能组 |
| DELETE | `/api/v1/admin/skill-groups/{id}` | 删除技能组（级联删除项） |
| POST | `/api/v1/admin/skill-groups/{id}/items` | 新增技能项 |
| PUT | `/api/v1/admin/skill-items/{id}` | 更新技能项 |
| DELETE | `/api/v1/admin/skill-items/{id}` | 删除技能项 |

**故障排查管理（第四阶段）：**

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/admin/troubleshooting` | 全部案例 |
| POST | `/api/v1/admin/troubleshooting` | 新增案例 |
| PUT | `/api/v1/admin/troubleshooting/{id}` | 更新案例 |
| DELETE | `/api/v1/admin/troubleshooting/{id}` | 删除案例 |

**时间线管理（第五阶段）：**

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/admin/timeline` | 全部时间线 |
| POST | `/api/v1/admin/timeline` | 新增 |
| PUT | `/api/v1/admin/timeline/{id}` | 更新 |
| DELETE | `/api/v1/admin/timeline/{id}` | 删除 |

**个人资料管理：**

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/admin/profile` | 获取资料 |
| PUT | `/api/v1/admin/profile` | 更新资料（含社交链接、能力卡片） |

**图片上传（第七阶段）：**

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/v1/admin/upload` | 上传图片，返回 URL |
| GET | `/api/v1/admin/images` | 图片列表 |
| DELETE | `/api/v1/admin/images/{id}` | 删除图片 |

### 9.6 API 与前端类型映射

| 前端类型 | API 端点 | 响应字段（camelCase） |
|---------|---------|---------------------|
| `Article` | `/articles/{slug}` | slug, title, category, excerpt, date, readTime, content |
| `Project` | `/projects/{slug}` | slug, title, subtitle, coverTone, tags, role, result, overview, highlights, githubUrl |
| `SkillGroup` | `/skills` | title, summary, items[{name, direction, scenario, status}] |
| `TroubleshootingCase` | `/troubleshooting/{slug}` | slug, title, symptom, process, tools, rootCause, resolution, review |
| `TimelineItem` | `/timeline` | time, title, detail |
| `Profile` + `SocialLinks` + `CapabilityCard[]` | `/profile` | name, handle, title, focus, intro, location, socialLinks{...}, capabilityCards[...] |

> **关键**：API 响应的 JSON 字段名必须与前端 TypeScript 接口 **完全一致**（camelCase），前端无需做任何字段映射。

---

## ⑩ 后端开发顺序

### 阶段总览

```
阶段 1  ✅  阅读项目 → 生成本文档（当前）
阶段 2  🔲  搭建 FastAPI 骨架 + 数据库连接 + 管理员登录
阶段 3  🔲  文章 CRUD（后端 API + 后台管理页面）
阶段 4  🔲  项目管理
阶段 5  🔲  技能管理
阶段 6  🔲  故障排查管理
阶段 7  🔲  图片上传
阶段 8  🔲  部署（Nginx + 腾讯云）
```

### 阶段 2：FastAPI 骨架 + 数据库 + 认证

**目标**：后端能跑起来，数据库能连上，管理员能登录。

**后端目录结构**：
```
backend/
├── app/
│   ├── main.py              # FastAPI app 入口
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py           # 依赖注入（get_db, get_current_admin）
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py     # v1 总路由
│   │       ├── auth.py       # 登录/认证
│   │       ├── articles.py   # 文章（阶段 3）
│   │       ├── projects.py   # 项目（阶段 4）
│   │       ├── skills.py     # 技能（阶段 5）
│   │       ├── troubleshooting.py  # 故障排查（阶段 6）
│   │       ├── timeline.py   # 时间线
│   │       └── profile.py    # 个人资料
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py         # Settings（pydantic-settings）
│   │   └── security.py       # JWT 生成/验证 + bcrypt
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py           # SQLAlchemy Base + engine + SessionLocal
│   │   └── init_db.py        # 初始化：创建管理员
│   ├── models/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── article.py
│   │   ├── project.py
│   │   ├── skill.py
│   │   └── profile.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── article.py
│   │   ├── project.py
│   │   ├── skill.py
│   │   └── profile.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── article.py
│   │   ├── project.py
│   │   ├── skill.py
│   │   └── profile.py
│   └── utils/
│       ├── __init__.py
│       └── response.py       # 统一响应格式
├── alembic/
│   ├── env.py
│   └── versions/
├── alembic.ini
├── requirements.txt
└── .env
```

**具体任务**：
1. 创建 `backend/` 目录 + `requirements.txt`
2. 配置 `app/core/config.py`（MySQL 连接、JWT 密钥、token 过期时间）
3. 配置 `app/db/base.py`（SQLAlchemy 2.0 engine + async/sync session）
4. 创建 `admins` 表 model + migration
5. 实现 `POST /api/v1/auth/login`（bcrypt 验证 + JWT 签发）
6. 实现 `GET /api/v1/auth/me`（JWT 验证 + 返回管理员信息）
7. 实现 `app/api/deps.py`（`get_current_admin` 依赖）
8. 配置 CORS（允许前端 dev server 跨域）
9. 初始化脚本：创建默认管理员账号
10. 测试：登录 → 获取 token → 访问 /auth/me

**验证标准**：
- `uvicorn app.main:app --reload` 能启动
- 登录返回 JWT token
- 用 token 访问 /auth/me 返回管理员信息
- 无 token 访问管理接口返回 401

### 阶段 3：文章 CRUD

**后端任务**：
1. 创建 `articles` 表 model + Alembic migration
2. 实现 Pydantic schemas（ArticleCreate, ArticleUpdate, ArticleResponse）
3. 实现 service 层 CRUD
4. 实现公开 API：`GET /articles`, `GET /articles/{slug}`
5. 实现管理 API：`POST/PUT/DELETE /admin/articles`
6. 编写 seed 脚本：将现有 5 篇文章数据导入数据库

**前端任务**（最小改动）：
1. 新增 `src/api/client.ts`（axios 实例）
2. 新增 `src/api/articles.ts`
3. 新增 `src/composables/useArticles.ts`
4. 修改 `ArticlesView.vue`、`ArticleDetailView.vue`、`HomeView.vue` 的 import（各改 1 行）
5. 修改 `vite.config.ts` 添加 proxy

**后台任务**：
1. 创建 `admin/` Vue3 项目
2. 实现登录页
3. 实现文章列表页 + 编辑表单

**验证标准**：
- 前端文章列表从 API 加载
- 后台可新增/编辑/删除文章
- 前端实时反映后台修改

### 阶段 4-8 概要

| 阶段 | 核心内容 | 模式 |
|------|---------|------|
| 4 | 项目 CRUD | 与阶段 3 相同模式：model → schema → service → API → 前端改 import → 后台页面 |
| 5 | 技能组 + 技能项 CRUD（双层嵌套） | 同上，但 API 需处理 group/items 嵌套关系 |
| 6 | 故障排查 CRUD + 时间线 CRUD + 个人资料编辑 | 同上 |
| 7 | 图片上传（本地存储 → 返回 URL） | FastAPI UploadFile + 静态文件服务 |
| 8 | 部署：Nginx 反代 + 前端构建 + 后端 systemd + MySQL | 按 DEPLOYMENT.md 规划执行 |

### 每个阶段的固定流程

```
1. 设计 → 确认表结构 + API 端点
2. 后端 → model → migration → schema → service → API
3. 测试 → 用 curl/httpie 测试所有端点
4. 前端 → api 层 → composable → 视图改 import（最小改动）
5. 后台 → 管理页面（如该阶段需要）
6. 集成测试 → 前端 + 后台 + API 联调
7. 文档 → 更新 BACKEND_PLAN.md 进度
8. 确认 → 等待你确认后再进入下一阶段
```

---

## 附录 A：现有数据 → 数据库迁移对照

| 前端数据文件 | 记录数 | 目标表 | 迁移方式 |
|-------------|--------|--------|---------|
| articles.ts | 5 | articles | seed 脚本 |
| projects.ts | 5 | projects | seed 脚本 |
| skills.ts | 4 组 28 项 | skill_groups + skill_items | seed 脚本 |
| troubleshooting.ts | 4 | troubleshooting_cases（阶段 4） | seed 脚本 |
| timeline.ts | 6 | timeline_items（阶段 5） | seed 脚本 |
| profile.ts | 1 + 4 | profile（含 capability_cards JSON） | seed 脚本 |
| socialLinks.ts | 1 | profile（合并字段） | seed 脚本 |

## 附录 B：前端改造影响评估

| 文件 | 改动类型 | 改动量 | 风险 |
|------|---------|--------|------|
| `vite.config.ts` | 新增 proxy 配置 | +6 行 | 无 |
| `src/types/content.ts` | 新增 3 个接口 | +20 行 | 无 |
| `src/api/client.ts` | 新增文件 | ~40 行 | 无 |
| `src/api/*.ts` | 新增 6 个文件 | 各 ~15 行 | 无 |
| `src/composables/use*.ts` | 新增 6 个文件 | 各 ~25 行 | 无 |
| `HomeView.vue` | 改 5 行 import | 5 行 | ⚠️ 低（需确保 loading 态不破坏动画） |
| `ArticlesView.vue` | 改 1 行 import | 1 行 | 无 |
| `ArticleDetailView.vue` | 改 import + find→API | ~3 行 | 无 |
| `ProjectsView.vue` | 改 1 行 import | 1 行 | 无 |
| `ProjectDetailView.vue` | 改 import + find→API | ~3 行 | 无 |
| `SkillsView.vue` | 改 1 行 import | 1 行 | 无 |
| `TroubleshootingView.vue` | 改 1 行 import | 1 行 | 无 |
| `AboutView.vue` | 改 2 行 import | 2 行 | 无 |
| `SiteFooter.vue` | 改 1 行 import | 1 行 | 无 |
| `SiteHeader.vue` | 改 1 行 import | 1 行 | 无 |
| `CapabilityOverview.vue` | 改 1 行 import | 1 行 | 无 |

**总计**：新增约 13 个文件，修改约 12 个现有文件（每个改 1-5 行 import）。
**不动**：所有组件模板、所有 CSS、所有 GSAP 动画、路由定义、组件命名。

## 附录 C：已知问题与改进建议

| # | 问题 | 建议 | 紧急度 |
|---|------|------|--------|
| 1 | `githubUrl` 全部指向 `https://github.com/`（占位） | 后台管理中为每个项目配置真实 URL | 中 |
| 2 | socialLinks 5/6 为 `TODO_REPLACE` | 后台管理中配置真实链接 | 中 |
| 3 | `profile.ts` 和 `socialLinks.ts` 无 TypeScript 接口 | 补充到 content.ts | 低 |
| 4 | `@vitejs/plugin-vue` 和 `vite` 在 dependencies 而非 devDependencies | 移到 devDependencies | 低 |
| 5 | 无 404 catch-all 路由 | 添加 NotFoundView | 低 |
| 6 | 无 favicon | 添加到 public/ | 低 |
| 7 | 路由全部 eager import，无代码分割 | 远期改为 lazy import | 低 |
| 8 | Article.content 为 string[]，不支持 Markdown | 远期考虑 Markdown 渲染 | 低 |
| 9 | troubleshooting 无分类字段 | 建表时可加 category | 低 |
| 10 | timeline.time 为标签而非日期 | 建表时用 sort_order 排序 | 低 |

---

> **下一步**：请审阅本文档。确认后我将从 **阶段 2（搭建 FastAPI 骨架 + 数据库连接 + 管理员登录）** 开始开发。
