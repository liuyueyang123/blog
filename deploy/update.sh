#!/usr/bin/env bash
# 更新部署：拉最新代码 → 重建前端 → 重启后端（root 运行）
set -euo pipefail

APP_DIR="/opt/blog"
BACKEND_DIR="$APP_DIR/backend"

cd "$APP_DIR"

echo "==> 拉取最新代码（GitHub 国内偶发断连，自动重试）"
for i in 1 2 3 4 5; do
  git pull origin main && break
  echo "  拉取失败，3 秒后重试..."
  sleep 3
done

echo "==> 更新后端依赖（如有变化）"
cd "$BACKEND_DIR"
./venv/bin/pip install -r requirements.txt

echo "==> 重建主站前端"
cd "$APP_DIR"
npm ci
npm run build

echo "==> 重建后台前端"
cd "$APP_DIR/admin"
npm ci
npm run build

echo "==> 修正目录归属与 SELinux 上下文"
chown -R blog:blog "$BACKEND_DIR"
restorecon -RF "$APP_DIR/dist" "$APP_DIR/admin/dist" "$BACKEND_DIR/uploads"

echo "==> 重启后端"
systemctl restart blog

echo "✅ 更新完成。主站 http://124.220.201.180/  后台 http://124.220.201.180:8081/"
