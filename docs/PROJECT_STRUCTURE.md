# Project Structure

```text
E:\BLOG
├─ images                  # 原始参考图，不移动不删除
├─ public
│  └─ resume               # 简历占位说明
├─ src
│  ├─ assets/styles        # 全局样式与 CSS 变量
│  ├─ components           # 通用、首页、项目、技能、排障组件
│  ├─ composables          # GSAP 动画封装
│  ├─ data                 # 静态内容数据，后续可替换为 API
│  ├─ router               # Vue Router
│  ├─ types                # 内容类型
│  └─ views                # 路由页面
├─ docs
├─ index.html
├─ package.json
└─ vite.config.ts
```

静态内容集中在 `src/data`，页面只消费数据，后续可以在同一边界替换为 FastAPI 请求。
