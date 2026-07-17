import type { TroubleshootingCase } from '../types/content';

export const troubleshootingCases: TroubleshootingCase[] = [
  {
    slug: 'prometheus-port-still-used',
    title: 'Prometheus 重启失败',
    symptom: 'Prometheus restart 后启动失败，端口仍被旧进程占用。',
    process: '先看 systemd 状态，再查 journalctl 日志，随后用 ps 和 ss 验证进程与端口监听。',
    tools: ['systemctl', 'journalctl', 'ps', 'ss'],
    rootCause: '旧 Prometheus 进程未退出，新 systemd 进程无法监听同一端口。',
    resolution: '清理残留进程后重新启动服务，并确认页面访问和端口监听状态一致。',
    review: '浏览器打开页面不会占用服务监听端口，问题来自服务进程管理混乱。',
  },
  {
    slug: 'vmware-nat-network',
    title: 'VMware NAT 网络异常',
    symptom: 'VMnet8 丢失，虚拟机无法访问网络。',
    process: '检查虚拟网络编辑器、Windows 网络适配器、ipconfig 输出和设备管理器状态。',
    tools: ['VMware 虚拟网络编辑器', 'Windows 网络适配器', 'ipconfig', '设备管理器'],
    rootCause: 'NAT 虚拟网卡、驱动或相关服务状态异常。',
    resolution: '围绕 VMnet8、NAT 服务和网卡驱动逐层恢复网络路径。',
    review: '虚拟机网络问题要分清虚拟网络、宿主机网卡和系统服务三个层面。',
  },
  {
    slug: 'docker-containerd-disk',
    title: 'Docker 与 containerd 磁盘占用',
    symptom: 'Docker/Kubernetes 环境中镜像、快照和容器数据占用过大。',
    process: '从 ctr、docker images、du、df 和 snapshot 目录确认空间来源。',
    tools: ['ctr', 'docker images', 'du', 'df', 'containerd snapshots'],
    rootCause: '镜像层、容器数据、containerd 命名空间和快照目录混在一起，缺少分层认知。',
    resolution: '区分 dockerd、containerd、命名空间和底层镜像内容后再清理。',
    review: '磁盘清理不能只看 Docker 命令，要理解运行时和存储目录的关系。',
  },
  {
    slug: 'model-overfitting',
    title: '模型过拟合分析',
    symptom: '训练准确率接近 100%，验证准确率只有 44% 左右。',
    process: '对比训练集与验证集表现，检查数据增强、学习率和训练策略。',
    tools: ['PyTorch', '训练日志', '准确率曲线', '数据增强'],
    rootCause: '模型记住训练数据，泛化能力不足。',
    resolution: '增加数据增强、随机擦除，调整训练策略和学习率。',
    review: '最终验证准确率提升至 68.25%，说明泛化改善比单看训练准确率更重要。',
  },
];
