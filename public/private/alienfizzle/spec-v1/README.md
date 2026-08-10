# 舰舰别炸 (Alien Fizzle)

> 近未来星际殖民时代，外星文明侵入殖民星 Aurelia 掠夺超导材料 Aurelium — 玩家拖拽战舰守线拦截敌群的竖屏微信小游戏。

## 技术栈

- 单 HTML + inline `<script>` + 2D Canvas
- 60 fps `requestAnimationFrame` 主循环 (dt 秒)
- HiDPI 后备缓冲 (2-3× scale), CSS 逻辑尺寸 414×736
- 输入: 触屏 + 鼠标 (`pointerX` / `pointerDown`), 拖拽移动主角
- 存储: `localStorage` + `wx.setStorage` 统一抽象层
- 微信小游戏 AppID: `wx52bccee83c7ef0de`

## 如何跑起来

1. 直接浏览器打开 `demo.html` (`file://` 或 http server)
2. URL 调试参数: `?debug=1` / `?focus=<skillId>` / `?forceCards=id1,id2,id3`

## 文件结构

| 文件 | 用途 |
|------|------|
| `data.json` | 所有数值 SSOT (Single Source of Truth) |
| `GAMEPLAY.md` | 玩法机制 + 公式 |
| `ENTITIES.md` | 卡/敌/道具实体表 |
| `README.md` | 本文件 |

## 术语

见 `terms.js` (代码源头) — 所有文档用 `T.xxx.yyy` 引用术语。
