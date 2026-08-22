# 阶段 2 完成报告 — FastAPI 骨架 + 数据库 + 管理员登录

> 完成时间：2026-08-03
> 状态：✅ 全部测试通过

---

## 完成内容

### 1. 后端目录结构

```
backend/
├── app/
│   ├── main.py                 # FastAPI 入口（CORS + 路由 + 健康检查）
│   ├── api/
│   │   ├── deps.py             # 依赖注入（get_current_admin）
│   │   └── v1/
│   │       ├── router.py       # v1 总路由
│   │       └── auth.py         # 登录 / 获取当前管理员
│   ├── core/
│   │   ├── config.py           # pydantic-settings 配置
│   │   └── security.py         # JWT + bcrypt（直接使用 bcrypt 库）
│   ├── db/
│   │   ├── base.py             # SQLAlchemy 2.0 engine + session
│   │   └── init_db.py          # 建表 + 默认管理员
│   ├── models/
│   │   └── admin.py            # Admin ORM 模型
│   ├── schemas/
│   │   └── admin.py            # Pydantic v2 请求/响应模型
│   ├── services/
│   │   └── auth.py             # 认证业务逻辑
│   └── utils/
│       └── response.py         # 统一响应格式
├── alembic/                    # 数据库迁移（已配置，待生成首次 migration）
├── requirements.txt
├── .env                        # 本地配置（当前使用 SQLite）
└── .env.example
```

### 2. 技术选型说明

| 项目 | 选择 | 原因 |
|------|------|------|
| Python | 3.12.7（Anaconda） | 3.14/3.13 包兼容性不足 |
| 密码哈希 | bcrypt 直接使用 | passlib 与 bcrypt>=4.1 不兼容 |
| 本地数据库 | SQLite（dev.db） | MySQL 密码待配置，先用 SQLite 验证 |
| 生产数据库 | MySQL 8（PyMySQL） | .env 中切换 DATABASE_URL 即可 |

### 3. 已实现的 API

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| GET | `/api/health` | 健康检查 | 无 |
| POST | `/api/v1/auth/login` | 管理员登录 | 无 |
| GET | `/api/v1/auth/me` | 当前管理员信息 | JWT |
| GET | `/api/docs` | Swagger 文档 | 无 |

### 4. 默认管理员

- 用户名：`admin`
- 密码：`admin123`
- ⚠️ 首次使用后必须修改

---

## 测试结果

| 测试项 | 结果 |
|--------|------|
| `GET /api/health` | ✅ `{"code":0,"message":"ok"}` |
| `POST /auth/login`（正确密码） | ✅ 返回 JWT token |
| `GET /auth/me`（有效 token） | ✅ 返回管理员信息 |
| `POST /auth/login`（错误密码） | ✅ 401 "用户名或密码错误" |
| `GET /auth/me`（无 token） | ✅ 401 "Not authenticated" |
| `GET /auth/me`（无效 token） | ✅ 401 "无效或已过期的 token" |
| `GET /api/docs` | ✅ 200 Swagger UI |

---

## 本地运行方式

```bash
cd backend
source venv/Scripts/activate    # Windows Git Bash
# 或 venv\Scripts\activate.bat  # Windows CMD

# 初始化数据库（首次运行）
python -m app.db.init_db

# 启动服务
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

访问 http://127.0.0.1:8000/api/docs 查看交互式 API 文档。

---

## 切换到 MySQL

编辑 `backend/.env`：

```env
# 注释掉 SQLite 行
# DATABASE_URL=sqlite:///./dev.db

# 启用 MySQL 配置
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=你的密码
DB_NAME=portfolio_blog
```

然后重新运行 `python -m app.db.init_db` 建表。

---

## 下一步（阶段 3）

- [ ] 创建 `articles` 表 + Alembic migration
- [ ] 实现文章公开 API（GET /articles, GET /articles/{slug}）
- [ ] 实现文章管理 API（POST/PUT/DELETE /admin/articles）
- [ ] 前端新增 axios + API 层 + composable
- [ ] 前端视图改 import（最小改动）
- [ ] 创建 admin/ 后台项目 + 登录页 + 文章管理页
