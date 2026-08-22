"""Seed script: import the 4 skill groups + 28 items from frontend data into MySQL"""

from sqlalchemy import select

from app.db.base import SessionLocal
from app.models.skill import SkillGroup, SkillItem

SEED_SKILLS = [
    {
        "title": "Linux 与基础设施",
        "summary": "面向服务部署、运行检查和基础排障的系统能力。",
        "sort_order": 1,
        "items": [
            {"name": "Linux", "direction": "基础设施", "scenario": "日常开发环境、服务器部署和权限/进程检查。", "status": "有项目实践", "sort_order": 1},
            {"name": "Shell", "direction": "基础设施", "scenario": "编写基础脚本，配合日志、端口和进程排查。", "status": "能够独立完成基础操作", "sort_order": 2},
            {"name": "VMware", "direction": "基础设施", "scenario": "搭建虚拟机实验环境，处理 NAT 网络异常。", "status": "能够排查常见问题", "sort_order": 3},
            {"name": "腾讯云", "direction": "云服务器", "scenario": "部署个人站点，规划 Git 拉取与 Nginx 托管流程。", "status": "有项目实践", "sort_order": 4},
            {"name": "Nginx", "direction": "Web 服务", "scenario": "托管前端静态文件，预留 /api 反向代理结构。", "status": "能够独立完成基础操作", "sort_order": 5},
            {"name": "MySQL", "direction": "数据服务", "scenario": "为后续博客和用户内容存储预留数据层。", "status": "正在系统学习", "sort_order": 6},
            {"name": "systemd", "direction": "服务管理", "scenario": "检查服务启动失败、重启状态和日志。", "status": "能够排查常见问题", "sort_order": 7},
            {"name": "SSH", "direction": "远程管理", "scenario": "连接云服务器，执行部署和服务检查。", "status": "能够独立完成基础操作", "sort_order": 8},
        ],
    },
    {
        "title": "容器与云原生",
        "summary": "理解容器运行时、镜像、部署和编排的基础链路。",
        "sort_order": 2,
        "items": [
            {"name": "Docker", "direction": "容器", "scenario": "构建镜像、运行容器、检查镜像和数据占用。", "status": "有项目实践", "sort_order": 1},
            {"name": "containerd", "direction": "容器运行时", "scenario": "分析 Docker 与 containerd 的关系和快照目录。", "status": "正在系统学习", "sort_order": 2},
            {"name": "Kubernetes", "direction": "服务编排", "scenario": "学习基础部署、服务编排和资源状态检查。", "status": "正在系统学习", "sort_order": 3},
            {"name": "镜像构建", "direction": "交付", "scenario": "为 Flask/FastAPI 服务设计基础镜像构建流程。", "status": "能够独立完成基础操作", "sort_order": 4},
            {"name": "容器部署", "direction": "交付", "scenario": "将应用以容器方式运行并观察服务状态。", "status": "有项目实践", "sort_order": 5},
            {"name": "基础网络与存储", "direction": "云原生基础", "scenario": "排查容器端口、数据目录和网络连通性。", "status": "正在系统学习", "sort_order": 6},
        ],
    },
    {
        "title": "SRE 与可观测性",
        "summary": "围绕指标、日志、告警和故障复盘建立清晰排障路径。",
        "sort_order": 3,
        "items": [
            {"name": "Prometheus", "direction": "指标采集", "scenario": "设计 /metrics 接口并采集服务指标。", "status": "有项目实践", "sort_order": 1},
            {"name": "Grafana", "direction": "可视化", "scenario": "展示请求、告警、温湿度、环境评分等面板。", "status": "有项目实践", "sort_order": 2},
            {"name": "Alertmanager", "direction": "告警", "scenario": "理解告警流转与通知配置的基础流程。", "status": "正在系统学习", "sort_order": 3},
            {"name": "日志分析", "direction": "排障", "scenario": "使用 journalctl 和应用日志定位启动失败。", "status": "能够排查常见问题", "sort_order": 4},
            {"name": "端口与进程排查", "direction": "排障", "scenario": "使用 ps、ss 等工具判断端口占用和旧进程残留。", "status": "能够排查常见问题", "sort_order": 5},
            {"name": "服务可用性检查", "direction": "SRE", "scenario": "从页面访问、服务状态、端口监听分层定位问题。", "status": "有项目实践", "sort_order": 6},
        ],
    },
    {
        "title": "编程、开发与 AI",
        "summary": "用 Python 和前端能力把模型、服务和展示页面串起来。",
        "sort_order": 4,
        "items": [
            {"name": "Python", "direction": "编程", "scenario": "模型训练、数据处理、Web 后端和脚本任务。", "status": "有项目实践", "sort_order": 1},
            {"name": "Flask", "direction": "Web 后端", "scenario": "实现 Food-101 Web 推理页面和接口。", "status": "有项目实践", "sort_order": 2},
            {"name": "FastAPI", "direction": "Web 后端", "scenario": "为后续博客 API 和项目接口预留演进路线。", "status": "正在系统学习", "sort_order": 3},
            {"name": "Vue 3", "direction": "前端", "scenario": "构建个人作品集、博客和面试展示站。", "status": "有项目实践", "sort_order": 4},
            {"name": "PyTorch", "direction": "深度学习", "scenario": "训练 ResNet、复现 nanoGPT、学习深度估计。", "status": "有项目实践", "sort_order": 5},
            {"name": "Transformer", "direction": "深度学习", "scenario": "学习注意力、位置编码、残差连接和自回归生成。", "status": "正在系统学习", "sort_order": 6},
            {"name": "ResNet", "direction": "计算机视觉", "scenario": "用于 Food-101 十类食品图像分类。", "status": "有项目实践", "sort_order": 7},
            {"name": "数据增强", "direction": "模型训练", "scenario": "缓解过拟合，将验证准确率从 44.25% 提升到 68.25%。", "status": "有项目实践", "sort_order": 8},
        ],
    },
]


def seed_skills() -> None:
    db = SessionLocal()
    try:
        groups_created = 0
        items_created = 0
        for group_data in SEED_SKILLS:
            existing = db.execute(
                select(SkillGroup).where(SkillGroup.title == group_data["title"])
            ).scalar_one_or_none()
            if existing:
                continue

            items_data = group_data.pop("items")
            group = SkillGroup(**group_data)
            db.add(group)
            db.flush()  # 获取 group.id

            for item_data in items_data:
                db.add(SkillItem(group_id=group.id, **item_data))
                items_created += 1

            groups_created += 1

        db.commit()
        print(f"[OK] Seed complete: {groups_created} groups, {items_created} items created")
    finally:
        db.close()


if __name__ == "__main__":
    seed_skills()
