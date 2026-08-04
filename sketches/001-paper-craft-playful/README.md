## Variant: 纸感手账 (Paper-craft playful)

### Design stance
一本被翻旧的手工日记本 —— 温暖、可触摸、女性化但不甜腻, 用手写字体和奶油纸色替代任何数字化装饰。

### Key choices
- Palette: 严格 5 色 —— 奶油纸 `#f7f2e8` 底, 深咖 `#3d3428` 墨, 柔棕 `#8a7d6b` 辅文, 卡片 `#fdfaf3` + `#e8dfc9` 细边, 唯一 accent 是烧橙 `#d97742`, 仅用于头像字母、tag、hover 与当前 nav。
- Typography: 标题与 nav 用 Google Font `Caveat` (手写) 建立「手账」信号; 正文回落到 `Georgia` 系统衬线; 日期与年份用等宽 + `tabular-nums` 保持数字对齐。
- Layout: 单列 720px 上限, header 用 CSS 圆角方块画头像 (无图片), nav 是一行文字链接而非 tab, 3 张 post 卡片交替 `rotate(±0.3deg)` 模拟便签贴纸, 单层柔和阴影, 卡片间距充足留白。
- Interaction: 仅 `background-color` + `transform: translateY(-2px)` + 颜色变化, 全部 150ms `ease-out`, 无 layout 属性动画; `prefers-reduced-motion` 下禁用 transition 与 rotate。

### Trade-offs
- Strong at: 建立强烈的作者人格与温度, 让「个人博客」看起来真的属于一个人而不是模板; 阅读节奏慢, 适合日记类内容; 视觉噪音极低。
- Weak at: 手写字体在长标题、代码块、密集技术清单里读起来吃力; 单列 720 对宽屏是浪费; 旋转卡片在移动端反而会显得抖动; 不适合大量列表/表格类技术内容。

### Best for
以日记与随笔为主、技术贴为辅的低频更新型个人站 —— 一周 1–2 篇、每篇需要「被慢慢读」的那种。
