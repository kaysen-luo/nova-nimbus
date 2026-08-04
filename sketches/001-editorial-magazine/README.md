## Variant: 编辑杂志 (Editorial magazine)

### Design stance
把高端印刷杂志的封面感搬到网页 —— 用排版、留白与细线规矩建立层级, 用一抹酒红做全局的主张, 不靠柔美色也能表达自信的女性感.

### Key choices
- Palette: 纸白 `#fbfaf7` + 近黑墨 `#0f0f0f` + 暖灰 `#7a7570`, 单一酒红强调色 `#8b1e3f` 仅用于报头、编辑推荐 kicker 与 hover; 拉引块用牛皮纸 `#f2eee5`. 无渐变、无阴影、无发光.
- Typography: Playfair Display 900 italic 撑报头与 feature 大标题、拉引; Noto Serif SC 700 承担中文正文标题、400 承担正文; 日期/kicker 用 mono 大写小型字, `letter-spacing: 0.08–0.28em` (印刷规约例外), 全站 `tabular-nums`.
- Layout: 顶部整幅报头 (上下双细线 + 日期/期号 + 巨大刊名), 中央导航小型 mono; feature 采用 2:1 双栏, 正文双栏排, 侧栏拉引块; 下方两篇文章并列, 中间 1px 垂直分隔线; 全部内容居于 `max-width: 960px`. 圆角一律为 0.
- Interaction: 仅 150ms `color` 过渡 (标题/导航 hover 变酒红), 无 transform、无布局属性动画; 尊重 `prefers-reduced-motion`.

### Trade-offs
- Strong at: 一眼看上去"这是个有主张的人在写东西", 长文可读性极佳, 中英混排毫无违和, 老派又不显土, 打印友好.
- Weak at: 首屏信息密度低 —— 报头就吃掉一屏; 大量细线在低 DPI 屏幕上要小心; feature 的双栏正文在 tablet 竖屏尴尬 (已在 720px 断点合并单栏); 不适合追求"信息流刷刷刷"的短平快场景.

### Best for
写长文、写得慢、想让读者慢下来的博主 —— 尤其当作者本人希望自己的字比头像先被记住.
