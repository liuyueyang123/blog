# 阶段 7 完成报告 — 图片上传

> 完成时间：2026-08-23
> 状态：✅ 全部验证通过
> 背景：文章正文已改为 Markdown（`![](图片URL)` 嵌图），本阶段补齐图片上传入口。

---

## 完成内容

### 1. 后端（backend/）

| 文件 | 改动 |
|------|------|
| `app/core/config.py` | 新增 `upload_dir`（默认 `uploads/`，相对 cwd 或绝对路径）、`max_upload_size_mb`（默认 5） |
| `app/api/v1/upload.py`（新增） | `POST /api/v1/admin/upload` 上传路由（JWT 认证） |
| `app/main.py` | 挂载 `StaticFiles` 到 `/uploads`，启动时自动创建上传目录 |
| `app/api/v1/router.py` | 接入 upload 路由（替换原「阶段 7」占位注释） |

**上传接口设计：**

- **路径**：`POST /api/v1/admin/upload`（需 `Authorization: Bearer <token>`）。
- **入参**：`multipart/form-data` 的 `file` 字段。
- **校验**：
  - 扩展名白名单 `{.jpg, .jpeg, .png, .gif, .webp}`，**排除 SVG**（避免潜在注入风险）。
  - 非空校验、大小上限（`max_upload_size_mb`，默认 5MB）。
- **存储**：`uuid4().hex + 原扩展名` 重命名，写入 `upload_dir` 目录，杜绝路径穿越与重名覆盖。
- **返回**：`{ "code": 0, "data": { "url": "/uploads/<filename>" } }`。

**静态文件服务：**

- 开发环境：后端 `StaticFiles` 直接 serve `/uploads/*`。
- 生产环境：Nginx 直接映射同一磁盘目录到 `/uploads/`（不经过后端）。
- 返回**相对 URL**，因此同一份 Markdown 在 dev 与线上都能直接显示，无需改内容。

---

### 2. 前端 / admin（admin/ 与根目录）

| 文件 | 改动 |
|------|------|
| `vite.config.ts`（根，主站） | 新增 `/uploads` → `localhost:8000` 代理 |
| `admin/vite.config.ts` | 新增 `/uploads` → `localhost:8000` 代理 |
| `admin/src/api/upload.ts`（新增） | `uploadImage(file): Promise<string>`，`FormData` 上传并返回 `url` |
| `admin/src/views/ArticleEditView.vue` | Markdown 编辑器上方新增「🖼 上传图片」按钮 |

**admin 编辑页交互：**

- 按钮触发隐藏 `<input type="file" accept="image/jpeg,image/png,image/gif,image/webp">`。
- 选文件 → 上传 → 成功后在**光标位置**自动插入 `![](url)`（`insertAtCursor` 处理 selectionStart/End，无焦点时追加到末尾）。
- 带「上传中...」禁用态与错误提示；上传后清空 input 以允许重复选同一文件。

---

### 3. 其它

| 文件 | 改动 |
|------|------|
| `.gitignore` | 新增 `backend/uploads/`（上传的运行时图片不提交） |

---

## 测试结果

| 测试项 | 结果 |
|--------|------|
| `POST /api/v1/admin/upload`（无 token） | ✅ 401（路由已注册） |
| 上传合法 PNG | ✅ 200，返回 `/uploads/<uuid>.png` |
| 上传 `.txt` | ✅ 400「不支持的图片格式 .txt，仅支持 .gif, .jpeg, .jpg, .png, .webp」 |
| `GET /uploads/<uuid>.png`（后端 serve） | ✅ 200 |
| 主站 `http://127.0.0.1:5173/uploads/...`（vite 代理） | ✅ 200 |
| 上传文件落盘 `backend/uploads/` | ✅ |
| admin `npm run build`（vue-tsc + vite） | ✅ 通过（1.31s） |

---

## 设计说明

1. **相对 URL**：接口返回 `/uploads/<filename>`，不写死域名。dev 走 vite 代理、线上走 Nginx，同一套内容无缝切换。
2. **只允许栅格图**：排除 SVG 与任意文件类型，配合「uuid 重命名 + 扩展名白名单」双保险，避免上传点被当作文件上传/存储型 XSS 入口。
3. **范围**：当前仅文章 Markdown 编辑器接入上传按钮（当前唯一会用图的场景）；接口本身通用，后续项目封面 / 头像等可直接复用。

---

## 下一步（阶段 8）

- [ ] 阶段 8：部署腾讯云
  - 前端接入 `VITE_API_BASE_URL`（当前仍走 dev proxy）
  - 服务器 MySQL 同结构建库 + seed
  - Nginx 反向代理 `/api/v1` → FastAPI，并映射 `/uploads/` 到上传目录
  - 后端 systemd 托管 + 前端静态构建产物托管
