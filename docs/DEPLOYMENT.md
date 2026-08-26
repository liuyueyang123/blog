# 部署文档 — 腾讯云 Rocky Linux 9.x

> 目标：把本博客（Vue3 前端 + FastAPI 后端 + MySQL）部署到腾讯云服务器，Nginx 反代，systemd 托管后端。
> 现状：无域名，通过公网 IP 访问，纯 HTTP（不申请证书）。
> 未来：购买域名后，用 certbot 自动配置 + 自动续签 HTTPS（见文末「SSL」）。

---

## 架构

```
浏览器
  ├─ http://<IP>/          →  Nginx :80   → /opt/blog/dist（主站）
  │                             ├─ /api/     → 反代 127.0.0.1:8000 (FastAPI)
  │                             └─ /uploads/ → /opt/blog/backend/uploads
  ├─ http://<IP>:8081/     →  Nginx :8081 → /opt/blog/admin/dist（后台）
  │                             └─ /api/     → 反代 127.0.0.1:8000
  └─ FastAPI(uvicorn, 8000) → MySQL :3306 (库 portfolio_blog)
```

关键点：
- 前端 `baseURL` 是相对路径 `/api/v1`，所以靠 Nginx 反代即可，**无需改代码、无需 CORS**。
- 后端只监听 `127.0.0.1:8000`（不对外），由 Nginx 转发。
- 仓库是单仓库：主站源码（根目录）、后台（`admin/`）、后端（`backend/`）都在同一个 git 仓库，一次 clone 全下来。

---

## 本地前置步骤（一次性）

部署脚本在仓库的 `deploy/` 目录，需要先提交并推送，服务器才能 clone 到。

```bash
# 1. 确认仓库是公开的（私有仓库需要额外配 deploy key，见文末）
#    GitHub → 仓库 Settings → 底部 Danger Zone → Change visibility → Public

# 2. 提交所有改动并推送
git add -A
git commit -m "feat: 图片上传 + 部署脚本"
git push origin main
```

---

## 服务器一次性部署（root 执行）

> 前提：腾讯云安全组已放行 **80、8081、22** 端口（SSH 22 默认已放行）。

SSH 登录服务器后，执行：

```bash
# 设一个 MySQL 专用密码（只用字母数字），例如 MyBlog2026
DB_PASSWORD='你的密码' bash <(curl -fsSL https://raw.githubusercontent.com/liuyueyang123/blog/main/deploy/setup.sh)
```

> 上面的「curl | bash」会在线拉取脚本执行。如果不放心，也可以：
> `git clone https://github.com/liuyueyang123/blog.git /opt/blog && DB_PASSWORD='密码' bash /opt/blog/deploy/setup.sh`
> （但 clone 到 /opt/blog 后 setup.sh 会检测到已存在而跳过 clone，行为一致。）

脚本会自动完成：
1. 安装 nginx / MySQL / git / Python3.11 / Node22（NodeSource 源）。
2. 初始化 MySQL：建库 `portfolio_blog` + 专用用户 `blog`。
3. `git clone` 代码到 `/opt/blog`。
4. 后端建 venv、装依赖、生成生产 `.env`（随机 JWT 密钥）。
5. 建表 + 管理员 + seed（5 篇文章 / 3 项目 / 4 技能组 / 排障 / 时间线 / 资料）。
6. 构建主站 + 后台前端（`npm ci && npm run build`）。
7. 部署 systemd 服务 `blog` + nginx 配置 + SELinux 放行 + firewalld 放行。

完成后访问：
- 主站：`http://124.220.201.180/`
- 后台：`http://124.220.201.180:8081/`（默认 `admin / admin123`，**登录后立即改密码**）
- 健康检查：`http://124.220.201.180/api/health`

---

## 日常更新（代码改动后）

本地 push 后，SSH 上服务器执行：

```bash
bash /opt/blog/deploy/update.sh
```

它会：`git pull` → 后端依赖更新 → 重建主站/后台前端 → 修正 SELinux 上下文 → 重启后端。

> 只改文章内容（不是代码）不需要这个，直接登录后台编辑即可，数据在 MySQL 里。

---

## 常见问题排查

| 现象 | 原因 / 处理 |
|------|------------|
| 访问站点 502 | 后端没起来：`systemctl status blog` 看日志，`journalctl -u blog -f` |
| 静态页正常但接口 502 | SELinux 拦截反代：`setsebool -P httpd_can_network_connect 1` |
| 上传的图片 403 | SELinux 上下文：`restorecon -RF /opt/blog/backend/uploads` |
| 页面 403 | 目录上下文：`restorecon -RF /opt/blog/dist /opt/blog/admin/dist` |
| 构建时 OOM | 2G 内存跑 `vue-tsc` 偏紧，加 2G swap：`fallocate -l 2G /swapfile && chmod 600 /swapfile && mkswap /swapfile && swapon /swapfile` |
| `mysql -uroot` 连不上 | MySQL 8 默认 socket 认证，root 下直接 `mysql` 即可；要密码登录用 `mysql -ublog -p` |
| 端口不通 | 腾讯云**安全组**和服务器 firewalld 都要放行 80 / 8081 |

---

## SSL（未来购买域名后）

自动续签可用 **Let's Encrypt + certbot**，certbot 自带 systemd 定时器，**到期前自动续签、无需人工**。步骤（购买域名后执行）：

```bash
# 1. 域名 A 记录指向服务器 IP
# 2. 把域名写进 nginx 的 server_name
# 3. 安装并申请证书（自动改 nginx 配置）
dnf install -y certbot python3-certbot-nginx
certbot --nginx -d 你的域名
# 4. 验证自动续签（dry-run）
certbot renew --dry-run
```

certbot 会自动加 `certbot-renew.timer` 每日检查，到期自动续签。如果之后不需要自动续签（例如不想暴露域名），就保持纯 HTTP，符合「做不到自动续签就不申请」的原则。

---

## 附录：私有仓库方案（可选）

若坚持私有仓库，服务器需要免密拉取，二选一：
1. **SSH deploy key**：服务器生成密钥 `ssh-keygen`，把公钥加到 GitHub 仓库的 Deploy keys，clone 用 `git@github.com:...`。
2. **Personal Access Token**：`git clone https://<token>@github.com/liuyueyang123/blog.git`（token 会出现在 shell 历史，注意清理）。
