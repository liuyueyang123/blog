# Yael 的技术作品集 + 博客 + 面试展示站

这是一个面向面试展示的前端项目，用于集中展示个人技术方向、项目实践、SRE 故障排查案例、技术文章和简历入口。

## 技术栈

- Vue 3
- Vite
- TypeScript
- Vue Router
- GSAP / ScrollTrigger
- CSS Variables
- Lucide Icons

## 本地运行

```bash
npm.cmd install
npm.cmd run dev
```

## 构建

```bash
npm.cmd run build
```

## 目录结构

核心代码位于 `src`，静态内容集中在 `src/data`，文档位于 `docs`。原始参考图保留在 `images`。

## GitHub 上传步骤

```bash
git remote add origin TODO_REPLACE_REPOSITORY_URL
git branch -M main
git push -u origin main
```

## 后续部署规划

GitHub 推送后，在腾讯云服务器中通过 Git 拉取项目，执行 `npm ci` 和 `npm run build`，再由 Nginx 托管 `dist`。未来 `/api` 反向代理到 FastAPI。

## 环境变量

第一版没有真实 API 依赖。`.env.example` 仅保留站点名称和未来 API 地址占位。
