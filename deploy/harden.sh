#!/usr/bin/env bash
# 安全加固脚本：拉最新代码 → 生成后台 Basic Auth → 部署 nginx 加固配置 → 重启后端
#
# 用法（root 执行）：
#   ADMIN_BA_USER='门卫用户名' ADMIN_BA_PASS='门卫密码' bash /opt/blog/deploy/harden.sh
#
# 说明：
#   - ADMIN_BA_USER / ADMIN_BA_PASS 是后台 8081 的第一道门（HTTP Basic Auth），
#     与后台登录的用户名密码（lyy / ...）是两套，请分开设置、不要相同。
#   - 脚本自带 git pull，所以本地 push 后直接跑这一条即可（首次若服务器还没本脚本，先跑一次 update.sh 拉代码）。
set -euo pipefail

if [[ $EUID -ne 0 ]]; then
  echo "❌ 请用 root 运行：sudo bash /opt/blog/deploy/harden.sh" >&2
  exit 1
fi

ADMIN_BA_USER="${ADMIN_BA_USER:?用法: ADMIN_BA_USER='xxx' ADMIN_BA_PASS='yyy' bash /opt/blog/deploy/harden.sh}"
ADMIN_BA_PASS="${ADMIN_BA_PASS:?用法: ADMIN_BA_USER='xxx' ADMIN_BA_PASS='yyy' bash /opt/blog/deploy/harden.sh}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "==> [1/5] 拉取最新代码（GitHub 国内偶发断连，自动重试）"
cd "$APP_DIR"
for i in 1 2 3 4 5; do
  git pull origin main && break
  echo "  拉取失败，3 秒后重试..."
  sleep 3
done

echo "==> [2/5] 安装 httpd-tools（htpasswd）"
dnf install -y httpd-tools

echo "==> [3/5] 生成后台 Basic Auth 密码文件 /etc/nginx/.htpasswd_admin"
printf '%s\n' "$ADMIN_BA_PASS" | htpasswd -c -i -B /etc/nginx/.htpasswd_admin "$ADMIN_BA_USER"
chown root:nginx /etc/nginx/.htpasswd_admin
chmod 640 /etc/nginx/.htpasswd_admin

echo "==> [4/5] 部署加固后的 nginx 配置"
cp "$SCRIPT_DIR/nginx.conf" /etc/nginx/conf.d/blog.conf

echo "==> [5/5] 校验并重载 nginx + 重启后端"
nginx -t
systemctl reload nginx
systemctl restart blog

echo ""
echo "✅ 加固完成："
echo "  - 后台 8081 增加 Basic Auth（用户名：$ADMIN_BA_USER）"
echo "  - 登录接口限流 + 安全响应头"
echo "  - 后端已重启（生产关闭 /api/docs、上传校验增强）"
