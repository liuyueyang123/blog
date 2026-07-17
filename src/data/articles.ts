import type { Article } from '../types/content';

export const articles: Article[] = [
  {
    slug: 'prometheus-port-restart',
    title: 'Prometheus 重启时端口被占用的原因',
    category: 'SRE',
    excerpt: '从 systemd、残留进程和端口监听三个层面拆解一次启动失败。',
    date: '2026-07-01',
    readTime: '6 min',
    content: ['服务重启失败时，先不要急着反复 restart。更稳的路径是查看 systemd 状态、读取 journalctl 日志，再确认端口由哪个进程监听。', '浏览器访问页面不会占用 Prometheus 的监听端口，真正的问题通常来自旧进程残留或服务管理混乱。'],
  },
  {
    slug: 'docker-containerd-dockerd',
    title: 'Docker、containerd 与 dockerd 的关系',
    category: 'Cloud Native',
    excerpt: '理解 Docker 命令背后的运行时链路，避免磁盘清理时误判。',
    date: '2026-07-03',
    readTime: '7 min',
    content: ['Docker CLI 只是入口，dockerd 负责管理上层体验，containerd 则处理更底层的容器生命周期。', '排查磁盘占用时需要同时看镜像层、容器数据、快照目录和命名空间。'],
  },
  {
    slug: 'soft-link-hard-link',
    title: '软链接和硬链接的底层区别',
    category: 'Linux',
    excerpt: '用 inode、路径和文件系统边界理解两类链接。',
    date: '2026-07-05',
    readTime: '5 min',
    content: ['硬链接指向同一个 inode，软链接保存的是路径。', '理解这点后，删除源文件、跨文件系统和目录链接这些行为就不再靠死记。'],
  },
  {
    slug: 'transformer-multi-head-attention',
    title: 'Transformer 多头注意力机制',
    category: 'AI',
    excerpt: '从 Q/K/V、注意力分数到多头拼接理解 Transformer 的核心模块。',
    date: '2026-07-08',
    readTime: '8 min',
    content: ['多头注意力让模型从不同子空间观察 token 之间的关系。', '它不是简单重复，而是把表示拆成多个视角，再合并成更丰富的上下文表达。'],
  },
  {
    slug: 'resnet-gradient',
    title: 'ResNet 为什么能缓解梯度消失',
    category: 'Computer Vision',
    excerpt: '残差连接如何让深层网络更容易训练。',
    date: '2026-07-10',
    readTime: '6 min',
    content: ['ResNet 的残差连接为梯度提供更直接的传播路径。', '对图像分类项目来说，它能让较深模型在训练中保持稳定，但泛化仍依赖数据和训练策略。'],
  },
];
