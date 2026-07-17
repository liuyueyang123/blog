# Deployment Plan

第一版只提供前端构建和部署说明，不安装或配置 MySQL、FastAPI、Nginx。

## 未来部署链路

```text
GitHub
→ 腾讯云服务器 git pull
→ npm ci
→ npm run build
→ Nginx 托管 dist
```

## 未来 Nginx 结构

```text
Nginx
├─ 前端静态文件: dist
└─ /api 反向代理 FastAPI
```

## 本地构建

```bash
npm.cmd install
npm.cmd run build
```

## 服务器部署草案

```bash
git clone TODO_REPLACE_REPOSITORY_URL blog
cd blog
npm ci
npm run build
```

随后将 Nginx 的站点根目录指向 `dist`。后续接入 FastAPI 后，再配置 `/api` 反向代理。
