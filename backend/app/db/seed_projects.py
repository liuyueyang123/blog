"""Seed script: import the 5 existing projects from frontend data into MySQL"""

from sqlalchemy import select

from app.db.base import SessionLocal
from app.models.project import Project

# 前端 socialLinks.githubUrl 当前为占位符
GITHUB_PLACEHOLDER = "https://github.com/"

SEED_PROJECTS = [
    {
        "slug": "food-101-classifier",
        "title": "Food-101 食品分类系统",
        "subtitle": "十类食品图像分类与 Web 推理页面",
        "cover_tone": "vision",
        "tags": ["Python", "PyTorch", "ResNet18", "Flask", "图像预处理"],
        "role": "负责数据处理、训练策略调整、过拟合分析和 Web 推理页面。",
        "result": "验证准确率从 44.25% 提升到 68.25%。",
        "overview": "围绕 Food-101 子集完成图像分类训练，使用数据增强和两阶段训练策略提升泛化能力。",
        "highlights": ["完成 10 类食品图像分类", "分析训练准确率过高与验证准确率偏低的问题", "完成可交互的 Web 推理页面"],
        "github_url": GITHUB_PLACEHOLDER,
        "sort_order": 1,
    },
    {
        "slug": "nanogpt-learning",
        "title": "nanoGPT 复现与原理学习",
        "subtitle": "从字符级数据到 Transformer 训练流程",
        "cover_tone": "terminal",
        "tags": ["Python", "PyTorch", "Transformer", "Tokenizer"],
        "role": "复现实验流程，梳理 Tokenizer、Embedding、多头注意力和自回归生成。",
        "result": "完成本地训练与技术讲解素材整理。",
        "overview": "通过 nanoGPT 学习语言模型的最小可运行结构，理解数据处理、损失计算和生成机制。",
        "highlights": ["完成字符级和子词级数据处理学习", "梳理多头注意力与残差连接", "制作相关技术讲解视频"],
        "github_url": GITHUB_PLACEHOLDER,
        "sort_order": 2,
    },
    {
        "slug": "depth-anything-study",
        "title": "Depth Anything 深度估计",
        "subtitle": "单目深度估计论文阅读与可视化",
        "cover_tone": "depth",
        "tags": ["Python", "PyTorch", "计算机视觉", "单目深度估计"],
        "role": "完成论文阅读、模型原理梳理、数据处理和结果可视化。",
        "result": "形成面向机器人、自动驾驶、AR/VR 的应用分析。",
        "overview": "围绕单目深度估计模型理解图像到深度图的推理路径和应用边界。",
        "highlights": ["梳理模型原理和数据流", "分析可视化结果", "总结三维重建和导航场景价值"],
        "github_url": GITHUB_PLACEHOLDER,
        "sort_order": 3,
    },
    {
        "slug": "smart-agriculture-sre",
        "title": "智能农业监控与 SRE 实践",
        "subtitle": "从业务指标到 Prometheus/Grafana 可观测性",
        "cover_tone": "sre",
        "tags": ["Flask", "Docker", "Kubernetes", "Prometheus", "Grafana"],
        "role": "设计 /metrics 指标接口、容器部署路径和可视化监控面板。",
        "result": "展示请求次数、告警数、环境评分、温湿度和服务状态。",
        "overview": "把业务监控和 SRE 思维结合，建立可观察、可排查、可复盘的服务展示。",
        "highlights": ["实现基础指标采集", "设计 Grafana 面板", "具备服务部署与问题排查实践"],
        "github_url": GITHUB_PLACEHOLDER,
        "sort_order": 4,
    },
    {
        "slug": "portfolio-cloud-deploy",
        "title": "个人博客与云服务器部署",
        "subtitle": "Vue 3 作品集、博客与后续 FastAPI 接入规划",
        "cover_tone": "web",
        "tags": ["Vue 3", "Vite", "GSAP", "FastAPI", "Nginx", "腾讯云"],
        "role": "从零设计作品集站点，规划 GitHub、服务器拉取、Nginx 托管和后端接入。",
        "result": "形成可提交 GitHub、可在云服务器构建部署的前端项目。",
        "overview": "服务于面试展示、技术博客、项目复盘和后续 API 化改造。",
        "highlights": ["静态数据集中管理", "预留 API 替换边界", "建立部署文档和工程规范"],
        "github_url": GITHUB_PLACEHOLDER,
        "sort_order": 5,
    },
]


def seed_projects() -> None:
    db = SessionLocal()
    try:
        created = 0
        skipped = 0
        for item in SEED_PROJECTS:
            existing = db.execute(
                select(Project).where(Project.slug == item["slug"])
            ).scalar_one_or_none()
            if existing:
                skipped += 1
                continue
            db.add(Project(**item))
            created += 1
        db.commit()
        print(f"[OK] Seed complete: {created} created, {skipped} skipped")
    finally:
        db.close()


if __name__ == "__main__":
    seed_projects()
