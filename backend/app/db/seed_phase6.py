"""Seed script: import troubleshooting cases, timeline items and profile"""

from sqlalchemy import select, func

from app.db.base import SessionLocal
from app.models.troubleshooting import TroubleshootingCase
from app.models.timeline import TimelineItem
from app.models.profile import Profile

SEED_CASES = [
    {
        "slug": "prometheus-port-still-used",
        "title": "Prometheus 重启失败",
        "symptom": "Prometheus restart 后启动失败，端口仍被旧进程占用。",
        "process": "先看 systemd 状态，再查 journalctl 日志，随后用 ps 和 ss 验证进程与端口监听。",
        "tools": ["systemctl", "journalctl", "ps", "ss"],
        "root_cause": "旧 Prometheus 进程未退出，新 systemd 进程无法监听同一端口。",
        "resolution": "清理残留进程后重新启动服务，并确认页面访问和端口监听状态一致。",
        "review": "浏览器打开页面不会占用服务监听端口，问题来自服务进程管理混乱。",
        "sort_order": 1,
    },
    {
        "slug": "vmware-nat-network",
        "title": "VMware NAT 网络异常",
        "symptom": "VMnet8 丢失，虚拟机无法访问网络。",
        "process": "检查虚拟网络编辑器、Windows 网络适配器、ipconfig 输出和设备管理器状态。",
        "tools": ["VMware 虚拟网络编辑器", "Windows 网络适配器", "ipconfig", "设备管理器"],
        "root_cause": "NAT 虚拟网卡、驱动或相关服务状态异常。",
        "resolution": "围绕 VMnet8、NAT 服务和网卡驱动逐层恢复网络路径。",
        "review": "虚拟机网络问题要分清虚拟网络、宿主机网卡和系统服务三个层面。",
        "sort_order": 2,
    },
    {
        "slug": "docker-containerd-disk",
        "title": "Docker 与 containerd 磁盘占用",
        "symptom": "Docker/Kubernetes 环境中镜像、快照和容器数据占用过大。",
        "process": "从 ctr、docker images、du、df 和 snapshot 目录确认空间来源。",
        "tools": ["ctr", "docker images", "du", "df", "containerd snapshots"],
        "root_cause": "镜像层、容器数据、containerd 命名空间和快照目录混在一起，缺少分层认知。",
        "resolution": "区分 dockerd、containerd、命名空间和底层镜像内容后再清理。",
        "review": "磁盘清理不能只看 Docker 命令，要理解运行时和存储目录的关系。",
        "sort_order": 3,
    },
    {
        "slug": "model-overfitting",
        "title": "模型过拟合分析",
        "symptom": "训练准确率接近 100%，验证准确率只有 44% 左右。",
        "process": "对比训练集与验证集表现，检查数据增强、学习率和训练策略。",
        "tools": ["PyTorch", "训练日志", "准确率曲线", "数据增强"],
        "root_cause": "模型记住训练数据，泛化能力不足。",
        "resolution": "增加数据增强、随机擦除，调整训练策略和学习率。",
        "review": "最终验证准确率提升至 68.25%，说明泛化改善比单看训练准确率更重要。",
        "sort_order": 4,
    },
]

SEED_TIMELINE = [
    {"time_label": "阶段 01", "title": "学习 Python 与计算机基础", "detail": "建立编程、数据处理和基础算法能力。", "sort_order": 1},
    {"time_label": "阶段 02", "title": "完成 AI 课程项目", "detail": "围绕图像分类和模型训练建立第一批项目实践。", "sort_order": 2},
    {"time_label": "阶段 03", "title": "复现 nanoGPT 与 Depth Anything", "detail": "从语言模型和视觉模型两条线理解深度学习系统。", "sort_order": 3},
    {"time_label": "阶段 04", "title": "学习 Linux、Docker、Kubernetes", "detail": "把注意力从模型扩展到服务部署和运行环境。", "sort_order": 4},
    {"time_label": "阶段 05", "title": "学习 Prometheus、Grafana 与 SRE", "detail": "开始用可观测性和排障思维看待系统稳定性。", "sort_order": 5},
    {"time_label": "阶段 06", "title": "搭建个人技术博客", "detail": "把项目、文章、复盘和面试展示沉淀成长期资产。", "sort_order": 6},
]

SEED_PROFILE = {
    "name": "Yael",
    "handle": "yael",
    "title": "Linux / Cloud / SRE / AI Engineering",
    "focus": "Linux / Cloud / SRE / Python / AI 工程实践",
    "intro": "我关注的不只是如何运行一个系统，也关注它如何被部署、监控、排查和持续改进。",
    "location": "China",
    "github_url": "https://github.com/",
    "email": "TODO_REPLACE",
    "bilibili_url": "TODO_REPLACE",
    "douyin_url": "TODO_REPLACE",
    "xiaohongshu_url": "TODO_REPLACE",
    "resume_url": "/resume/resume-placeholder.pdf",
    "capability_cards": [
        {
            "title": "Linux 与云计算",
            "tech": "Linux, Shell, Nginx, MySQL, 腾讯云",
            "practice": "完成云服务器部署、反向代理、服务运行状态检查与基础排障。",
        },
        {
            "title": "容器与云原生",
            "tech": "Docker, containerd, Kubernetes, 镜像构建",
            "practice": "理解容器运行链路，能处理镜像、快照、部署和资源占用问题。",
        },
        {
            "title": "SRE 与可观测性",
            "tech": "Prometheus, Grafana, Alertmanager, 日志分析",
            "practice": "围绕指标采集、告警、端口进程和网络状态建立排查路径。",
        },
        {
            "title": "Python 与 AI",
            "tech": "PyTorch, Flask, FastAPI, ResNet, Transformer",
            "practice": "完成图像分类、深度估计学习、nanoGPT 复现和 Web 推理页面。",
        },
    ],
}


def seed_phase6() -> None:
    db = SessionLocal()
    try:
        # 故障案例
        cases_created = 0
        for item in SEED_CASES:
            existing = db.execute(
                select(TroubleshootingCase).where(TroubleshootingCase.slug == item["slug"])
            ).scalar_one_or_none()
            if existing:
                continue
            db.add(TroubleshootingCase(**item))
            cases_created += 1

        # 时间线
        timeline_created = 0
        for item in SEED_TIMELINE:
            existing = db.execute(
                select(TimelineItem).where(TimelineItem.title == item["title"])
            ).scalar_one_or_none()
            if existing:
                continue
            db.add(TimelineItem(**item))
            timeline_created += 1

        # 个人资料（单行）
        profile_created = 0
        count = db.execute(select(func.count(Profile.id))).scalar() or 0
        if count == 0:
            db.add(Profile(**SEED_PROFILE))
            profile_created = 1

        db.commit()
        print(
            f"[OK] Seed complete: {cases_created} cases, "
            f"{timeline_created} timeline items, {profile_created} profile"
        )
    finally:
        db.close()


if __name__ == "__main__":
    seed_phase6()
