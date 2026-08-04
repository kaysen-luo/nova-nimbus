## Variant: 有机森林 (Organic forest)

### Design stance
现代衬线遇上泥土色 — 深色成熟的编辑部气质, 女性感来自曲线与克制, 不来自糖果色。

### Key choices
- Palette: 骨白底 `#faf7f2` + 深森林墨 `#1f2820` + 苔灰 `#6b6f66`, 单一强调色为陶土锈红 `#a04d3a`, 白卡 `#ffffff` 配 `#e5e0d5` 细线边框, 不用任何渐变/发光/阴影。
- Typography: Noto Serif SC (400/500/600) 承担正文与标题, 提供 CJK 现代衬线的稳重感; 日期与元信息使用 `ui-monospace` 并开启 `tabular-nums`, 数字对齐更工整。
- Layout: 240px 左侧栏 + 主内容双列布局。侧栏容纳头像、身份、垂直导航, 主区把文章排成日期 / 正文的横向行, 用 `border-bottom` 分隔, 没有卡片盒感, 更接近 Are.na / Kinfolk 的编辑排版; 720px 以下侧栏塌到顶部, 导航转成横向。
- Interaction: 悬停时行背景切到白卡、标题变陶土色、导航项加 4px 位移, 全部 150ms `ease-out`; 仅使用 color / background-color / transform, 尊重 `prefers-reduced-motion`。

### Trade-offs
- Strong at: 长文阅读的沉浸感、内容分类清晰、留白优雅, 适合把"写字"这件事本身当作主角。
- Weak at: 视觉冲击力较弱, 首屏没有大图/大标题, 对追求"惊艳感"的访客可能显得过于安静; 侧栏在中等宽度下会挤压主区。

### Best for
喜欢慢读、想把博客做成个人档案室而非流量入口的写作者。
