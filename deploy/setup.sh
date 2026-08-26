#!/usr/bin/env bash
# 一次性部署脚本（Rocky Linux 9.x，root 运行）
# 用法：DB_PASSWORD='你的MySQL密码' bash setup.sh
# 说明：密码建议只用字母数字，避免引号等特殊字符。
set -euo pipefail

DB_PASSWORD="${DB_PASSWORD:?用法: DB_PASSWORD='xxx' bash setup.sh}"

REPO_URL="https://gitee.com/lanyangyang1111234/my-blog.git"
APP_DIR="/opt/blog"
BACKEND_DIR="$APP_DIR/backend"

echo "==> [1/8] 安装系统依赖 (nginx / mysql / git / python3.11 / node22)"
dnf install -y epel-release
dnf install -y nginx mysql-server git curl python3.11 python3.11-pip policycoreutils-python-utils

# Node 22（Vite 7 需要 Node 20.19+ / 22+）
curl -fsSL https://rpm.nodesource.com/setup_22.x | bash -
dnf install -y nodejs

echo "==> [2/8] 启动 MySQL 并创建数据库/专用用户"
systemctl enable --now mysqld
mysql -uroot <<SQL
CREATE DATABASE IF NOT EXISTS portfolio_blog CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'blog'@'localhost' IDENTIFIED BY '${DB_PASSWORD}';
GRANT ALL PRIVILEGES ON portfolio_blog.* TO 'blog'@'localhost';
FLUSH PRIVILEGES;
SQL

echo "==> [3/8] 克隆代码（请确认仓库为公开，否则 clone 会失败）"
if [ -d "$APP_DIR/.git" ]; then
  echo "  已存在 $APP_DIR，跳过 clone"
else
  rm -rf "$APP_DIR"
  for i in 1 2 3 4 5; do
    echo "  第 $i 次尝试 clone（GitHub 国内偶发断连，自动重试）..."
    git clone "$REPO_URL" "$APP_DIR" && break
    echo "  clone 失败，3 秒后重试..."
    sleep 3
  done
  if [ ! -d "$APP_DIR/.git" ]; then
    echo "❌ 多次 clone 均失败，请检查网络后重跑本脚本" >&2
    exit 1
  fi
fi

echo "==> [4/8] 后端 Python 虚拟环境 + 依赖"
cd "$BACKEND_DIR"
python3.11 -m venv venv
./venv/bin/pip install --upgrade pip
./venv/bin/pip install -r requirements.txt

echo "==> [5/8] 生成生产 .env（随机 JWT 密钥）"
JWT_SECRET=$(./venv/bin/python -c "import secrets; print(secrets.token_hex(32))")
cat > "$BACKEND_DIR/.env" <<EOF
DB_HOST=localhost
DB_PORT=3306
DB_USER=blog
DB_PASSWORD=${DB_PASSWORD}
DB_NAME=portfolio_blog
JWT_SECRET_KEY=${JWT_SECRET}
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=1440
APP_ENV=production
CORS_ORIGINS=[]
EOF
chmod 600 "$BACKEND_DIR/.env"

echo "==> [6/8] 初始化数据库（建表 + 管理员 + seed）"
./venv/bin/python -m app.db.init_db
./venv/bin/python -m app.db.seed_articles
./venv/bin/python -m app.db.seed_projects
./venv/bin/python -m app.db.seed_skills
./venv/bin/python -m app.db.seed_phase6

echo "==> [7/8] 构建前端（主站 + 后台）"
# 2G 内存跑 vue-tsc 构建偏紧，先预置 2G swap 防 OOM
if ! swapon --show 2>/dev/null | grep -q /swapfile; then
  fallocate -l 2G /swapfile && chmod 600 /swapfile && mkswap /swapfile && swapon /swapfile
  grep -q '/swapfile' /etc/fstab || echo '/swapfile none swap sw 0 0' >> /etc/fstab
fi
cd "$APP_DIR"
npm ci
npm run build
cd "$APP_DIR/admin"
npm ci
npm run build

echo "==> [8/8] 部署 systemd 服务 + nginx"
id -u blog &>/dev/null || useradd -r -s /sbin/nologin blog
chown -R blog:blog "$BACKEND_DIR"

cp "$APP_DIR/deploy/blog.service" /etc/systemd/system/blog.service
systemctl daemon-reload
systemctl enable --now blog

cp "$APP_DIR/deploy/nginx.conf" /etc/nginx/conf.d/blog.conf

# SELinux：放行 nginx 反代 + 目录上下文
setsebool -P httpd_can_network_connect 1
semanage fcontext -a -t httpd_sys_content_t "$APP_DIR/dist(/.*)?" 2>/dev/null || true
semanage fcontext -a -t httpd_sys_content_t "$APP_DIR/admin/dist(/.*)?" 2>/dev/null || true
semanage fcontext -a -t httpd_sys_content_t "$BACKEND_DIR/uploads(/.*)?" 2>/dev/null || true
restorecon -Rv "$APP_DIR"

# firewalld：放行 80 / 8081
systemctl enable --now firewalld
firewall-cmd --permanent --add-service=http
firewall-cmd --permanent --add-port=8081/tcp
firewall-cmd --reload

systemctl enable --now nginx

echo ""
echo "=============================================="
echo "✅ 部署完成！"
echo "  主站:   http://124.220.201.180/"
echo "  后台:   http://124.220.201.180:8081/  (admin / admin123)"
echo "  后端健康: http://124.220.201.180/api/health"
echo "  MySQL 专用用户: blog / (你设的密码)"
echo "⚠️  登录后台后请立即修改默认密码 admin/admin123"
echo "=============================================="
