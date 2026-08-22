# 阶段 5 完成报告 — 技能管理（技能组 + 技能项双层结构）

> 完成时间：2026-08-05
> 状态：✅ 全部测试通过

---

## 完成内容

### 1. 后端（backend/）

**新增文件：**

| 文件 | 说明 |
|------|------|
| `app/models/skill.py` | SkillGroup（1）→ SkillItem（N），relationship + 级联删除 |
| `app/schemas/skill.py` | 嵌套 schemas，`SkillStatus` Literal 校验 4 级状态 |
| `app/services/skill.py` | 组/项 CRUD，selectinload 预加载避免 N+1 |
| `app/api/v1/skills.py` | 公开路由：GET /skills（嵌套返回） |
| `app/api/v1/admin_skills.py` | 管理路由：组 CRUD + 项 CRUD |
| `app/db/seed_skills.py` | Seed：导入 4 组 28 项 |

**数据库：**
- `skill_groups` + `skill_items` 表（外键 ON DELETE CASCADE）
- status 用 VARCHAR(50) + Pydantic Literal 校验（避免 MySQL ENUM 迁移麻烦）

**管理 API 端点：**

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /admin/skills | 全部技能组（含项） |
| POST | /admin/skill-groups | 新增组 |
| PUT | /admin/skill-groups/{id} | 更新组 |
| DELETE | /admin/skill-groups/{id} | 删除组（级联删除项） |
| POST | /admin/skill-groups/{id}/items | 新增项 |
| PUT | /admin/skill-items/{id} | 更新项 |
| DELETE | /admin/skill-items/{id} | 删除项 |

### 2. 前端（src/）

**新增文件：**
- `src/api/skills.ts` — getSkillGroups()
- `src/composables/useSkills.ts` — useSkills()

**修改文件：**

| 文件 | 改动 |
|------|------|
| `src/views/SkillsView.vue` | 改 import → useSkills() |
| `src/views/HomeView.vue` | 改 import → useSkills()，传入合并 loading |
| `src/views/ProjectsView.vue` | 补传 loading（动画修复） |
| `src/composables/useGsap.ts` | ⚠️ 见下方「动画兼容修复」 |

### 3. ⚠️ 动画兼容修复（重要说明）

**问题**：数据改为 API 异步加载后，`useRevealAnimations()` 在 `onMounted` 时扫描 `[data-reveal]` 元素，此时 v-for 卡片尚未渲染，导致 ScrollTrigger 入场动画失效。

**修复**：`useRevealAnimations` 新增可选参数 `loading?: Ref<boolean>`：
- 数据加载完成后自动补扫新渲染的元素
- 用 WeakSet 记录已动画元素，防止重复动画
- **动画参数完全未变**（y/opacity/duration/ease/stagger 全部保持原值）
- 向后兼容：不传参数时行为与原版一致

### 4. 后台（admin/）

**新增文件：**

| 文件 | 说明 |
|------|------|
| `src/api/skills.ts` | 组/项 CRUD API + SKILL_STATUS_OPTIONS |
| `src/views/SkillListView.vue` | 双层管理页：组卡片内嵌项表格，行内编辑 |

**功能：**
- 新增/编辑/删除技能组（行内表单）
- 新增/编辑/删除技能项（行内表单，状态下拉选择）
- AdminNav 导航新增「技能」入口

---

## 测试结果

| 测试项 | 结果 |
|--------|------|
| GET /api/v1/skills（嵌套，4 组 28 项） | ✅ |
| 响应字段与前端 SkillGroup/SkillItem 类型对齐 | ✅ |
| UTF-8 中文内容完整性（断言验证） | ✅ |
| POST /admin/skill-groups（创建组） | ✅ |
| POST /admin/skill-groups/{id}/items（创建项） | ✅ |
| PUT /admin/skill-items/{id}（更新状态） | ✅ |
| PUT /admin/skill-groups/{id}（更新组） | ✅ |
| DELETE /admin/skill-items/{id}（删除项） | ✅ |
| DELETE /admin/skill-groups/{id}（级联删除） | ✅ |
| 前端 vite build | ✅（bundle 减小 4KB，静态数据移除） |
| admin vite build | ✅ |

---

## 前端数据迁移进度

| 数据 | API 迁移 | 状态 |
|------|---------|------|
| articles | ✅ | 阶段 3 |
| projects | ✅ | 阶段 4 |
| skills | ✅ | 阶段 5 |
| troubleshooting | 🔲 | 阶段 6 |
| timeline | 🔲 | 阶段 6 |
| profile + socialLinks + capabilityCards | 🔲 | 阶段 6 |

---

## 下一步（阶段 6：故障排查 + 时间线 + 个人资料）

- [ ] TroubleshootingCase 模型 + CRUD + seed（4 条）
- [ ] TimelineItem 模型 + CRUD + seed（6 条）
- [ ] Profile 模型（合并 socialLinks + capabilityCards）+ seed
- [ ] 公开 API：/troubleshooting, /timeline, /profile
- [ ] 管理 API：对应 CRUD
- [ ] 前端：useTroubleshooting / useTimeline / useProfile + 视图对接
  - TroubleshootingView, HomeView, AboutView, SiteFooter, SiteHeader, CapabilityOverview
- [ ] 后台：故障排查/时间线/个人资料管理页
