# 阶段 6 完成报告 — 故障排查 + 时间线 + 个人资料

> 完成时间：2026-08-22
> 状态：✅ 全部验证通过

---

## 完成内容

### 1. 后端（backend/）

> 阶段 6 的 Python 代码（模型/schema/service/路由/seed）在此前已写好，本阶段主要是**接线 + 一处字段统一修复 + 本地 MySQL 落库**。

**阶段 6 后端文件（已存在，本阶段未改业务逻辑）：**

| 文件 | 说明 |
|------|------|
| `app/models/troubleshooting.py` | TroubleshootingCase 模型 |
| `app/models/timeline.py` | TimelineItem 模型 |
| `app/models/profile.py` | Profile 模型（合并 socialLinks + capabilityCards） |
| `app/schemas/troubleshooting.py` | 排障 schemas（已配 `alias_generator=to_camel`） |
| `app/schemas/timeline.py` | 时间线 schemas（**本阶段加 camelCase 修复，见下**） |
| `app/schemas/profile.py` | 资料 schemas（嵌套 socialLinks / capabilityCards） |
| `app/services/troubleshooting.py` | 排障 CRUD |
| `app/services/timeline.py` | 时间线 CRUD |
| `app/services/profile.py` | 资料读取/更新 |
| `app/api/v1/troubleshooting.py` | 公开路由 GET /troubleshooting |
| `app/api/v1/timeline.py` | 公开路由 GET /timeline |
| `app/api/v1/profile.py` | 公开路由 GET /profile |
| `app/api/v1/admin_troubleshooting.py` | 管理路由 CRUD |
| `app/api/v1/admin_timeline.py` | 管理路由 CRUD |
| `app/api/v1/admin_profile.py` | 管理路由 GET/PUT /admin/profile |
| `app/db/seed_phase6.py` | Seed：排障 4 条 + 时间线 6 条 + 资料 1 条 |

**本阶段后端改动（1 处）：**

- `app/schemas/timeline.py`：`TimelineItemResponse.model_config` 增加 `alias_generator=to_camel`。
  - 作用：时间线响应此前是唯一一个输出 `sort_order`（snake_case）的模块，与其它模块的 camelCase 约定不一致；统一后输出 `sortOrder` / `createdAt` / `updatedAt`。
  - `time` 字段的 `validation_alias="time_label"` 保留（只影响输入解析，不影响输出）。

**数据库表（本地 MySQL `portfolio_blog`）：**

- `troubleshooting_cases`、`timeline_items`、`profile` 三张表已存在（阶段 6 数据已 seed，seed 幂等，0 新增记录）。

---

### 2. 前端（src/）

**新增文件：**

| 文件 | 说明 |
|------|------|
| `src/api/troubleshooting.ts` | `getTroubleshootingCases()` |
| `src/api/timeline.ts` | `getTimeline()` |
| `src/api/profile.ts` | `getProfile()`（单对象） |
| `src/composables/useTroubleshooting.ts` | `useTroubleshooting()` → `{ troubleshootingCases, loading, error }` |
| `src/composables/useTimeline.ts` | `useTimeline()` → `{ timeline, loading, error }` |
| `src/composables/useProfile.ts` | `useProfile()` → `{ profile: Ref<Profile\|null>, loading, error }` |

**修改文件：**

| 文件 | 改动 |
|------|------|
| `src/views/TroubleshootingView.vue` | 静态数据 → `useTroubleshooting()`，`useRevealAnimations(loading)` |
| `src/views/HomeView.vue` | 增加 `useTroubleshooting()` + `useTimeline()`，loading 并入 `asyncLoading` |
| `src/views/AboutView.vue` | `useProfile()` + `useTimeline()`，加 `v-if="profile"` 守卫 |
| `src/components/common/SiteHeader.vue` | `socialLinks` → `useProfile()`，用 `profile?.socialLinks.githubUrl` |
| `src/components/common/SiteFooter.vue` | `profile` → `useProfile()`，加 `v-if="profile"` 守卫 |
| `src/components/home/CapabilityOverview.vue` | `capabilityCards` → `useProfile()`，`profile?.capabilityCards ?? []` |

> 关键点：profile 是单对象，首屏为 null，上述 4 处均加了 `v-if` / `?.` 空值守卫。

**⚠️ 修复的既有类型错误（非本阶段引入，阻断构建）：**

- `src/components/common/CursorGlow.vue`：`pointerrawupdate` 事件监听器与 `trackPointer(event: MouseEvent | PointerEvent)` 签名不匹配（TS2769）。改为 `trackPointer(event: Event)` + 内部类型收窄，运行时行为不变。

---

### 3. 后台（admin/）

**新增文件：**

| 文件 | 说明 |
|------|------|
| `src/api/troubleshooting.ts` | 排障 CRUD + `TroubleshootingCase` / `TroubleshootingPayload` 类型 |
| `src/api/timeline.ts` | 时间线 CRUD + `TimelineItem` / `TimelinePayload` 类型 |
| `src/api/profile.ts` | 资料 GET/PUT + `Profile` / `ProfilePayload` 类型 |
| `src/views/TroubleshootingListView.vue` | 排障列表页（标题/现象/根因/状态/操作） |
| `src/views/TroubleshootingEditView.vue` | 排障编辑页（tools 逗号分隔） |
| `src/views/TimelineListView.vue` | 时间线列表页（阶段/标题/详情/排序/操作） |
| `src/views/TimelineEditView.vue` | 时间线编辑页 |
| `src/views/ProfileView.vue` | 资料单记录页（整表表单 + capability_cards 内联增删） |

**修改文件：**

| 文件 | 改动 |
|------|------|
| `src/router/index.ts` | 新增 6 条路由（排障/时间线/资料的 list+new+edit，及 /profile） |
| `src/components/AdminNav.vue` | 新增「排障 / 时间线 / 资料」3 个导航入口 |

**⚠️ 修复的既有类型错误：**

- `src/api/articles.ts` / `src/api/projects.ts`：新增 `ArticlePayload` / `ProjectPayload`（snake_case）接口，`create/update` 签名由 camelCase `Omit<Article,'id'>` 改为 payload 类型（TS2345），与后端 Pydantic 字段名一致。

---

## 测试结果

| 测试项 | 结果 |
|--------|------|
| GET /api/v1/troubleshooting（rootCause 等 camelCase） | ✅ |
| GET /api/v1/timeline（sortOrder/createdAt/updatedAt 已 camelCase） | ✅ |
| GET /api/v1/profile（socialLinks/githubUrl 嵌套 camelCase） | ✅ |
| GET /api/v1/admin/troubleshooting（无 token） | ✅ 401 |
| POST /api/v1/auth/login（admin/admin123） | ✅ 返回 token |
| GET /api/v1/admin/troubleshooting（带 token） | ✅ 200 |
| GET /api/v1/admin/timeline（带 token） | ✅ 200 |
| GET /api/v1/admin/profile（带 token） | ✅ 200 |
| 前端 `npm run build`（vue-tsc + vite） | ✅ |
| admin `npm run build`（vue-tsc + vite） | ✅ |
| `src/` 不再 import 静态数据（`src/data/*.ts` 成为无引用遗留） | ✅ |

---

## 前端数据迁移进度

| 数据 | API 迁移 | 状态 |
|------|---------|------|
| articles | ✅ | 阶段 3 |
| projects | ✅ | 阶段 4 |
| skills | ✅ | 阶段 5 |
| troubleshooting | ✅ | 阶段 6 |
| timeline | ✅ | 阶段 6 |
| profile + socialLinks + capabilityCards | ✅ | 阶段 6 |

---

## MySQL 切换说明

- 后端 `backend/.env` 已切换为本地 MySQL（`root/123456@localhost:3306/portfolio_blog`）。
- 本地「库已存在」，`Base.metadata.create_all` 只建缺失表，不删除已有数据；默认管理员 `admin` 已存在。
- 阶段 6 三张表（`troubleshooting_cases` / `timeline_items` / `profile`）及 seed 数据均已落库。

---

## 下一步（阶段 7 / 8）

- [ ] 阶段 7：图片上传（文章/项目封面、头像）
- [ ] 阶段 8：部署腾讯云
  - 前端接入 `VITE_API_BASE_URL`（当前仍走 dev proxy）
  - 服务器 MySQL 同结构建库 + seed
  - Nginx 反向代理 `/api/v1` → FastAPI
