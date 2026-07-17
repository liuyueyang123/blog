import { socialLinks } from './socialLinks';

export const profile = {
  name: 'Yael',
  handle: 'yael',
  title: 'Linux / Cloud / SRE / AI Engineering',
  focus: 'Linux / Cloud / SRE / Python / AI 工程实践',
  intro:
    '我关注的不只是如何运行一个系统，也关注它如何被部署、监控、排查和持续改进。',
  location: 'China',
  socialLinks,
};

export const capabilityCards = [
  {
    title: 'Linux 与云计算',
    tech: 'Linux, Shell, Nginx, MySQL, 腾讯云',
    practice: '完成云服务器部署、反向代理、服务运行状态检查与基础排障。',
  },
  {
    title: '容器与云原生',
    tech: 'Docker, containerd, Kubernetes, 镜像构建',
    practice: '理解容器运行链路，能处理镜像、快照、部署和资源占用问题。',
  },
  {
    title: 'SRE 与可观测性',
    tech: 'Prometheus, Grafana, Alertmanager, 日志分析',
    practice: '围绕指标采集、告警、端口进程和网络状态建立排查路径。',
  },
  {
    title: 'Python 与 AI',
    tech: 'PyTorch, Flask, FastAPI, ResNet, Transformer',
    practice: '完成图像分类、深度估计学习、nanoGPT 复现和 Web 推理页面。',
  },
];
