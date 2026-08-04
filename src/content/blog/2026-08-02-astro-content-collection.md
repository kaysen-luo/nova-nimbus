---
title: "Astro 的 content collection 踩坑记"
description: "z.date() 和字符串日期的时区大坑"
pubDate: 2026-08-02
category: "技术"
---

在 `content.config.ts` 里我一开始写的是 `pubDate: z.date()`, 然后 frontmatter 用 `pubDate: 2026-08-02`
这种字符串写法。构建居然没报错, 但页面上显示的日期整整早了一天。修了两个小时才发现是 YAML 把纯日期
解析成了 UTC 00:00, 而我本地是 UTC+8, 一 `toLocaleDateString` 就被吞掉半天。

解决方案其实很小: 把 schema 改成 `z.coerce.date()`, 让 Astro 显式做字符串到 Date 的转换; 展示层
统一用 `date.getUTCFullYear() / getUTCMonth() / getUTCDate()`, 不走 locale。这样无论谁在什么时区
构建, 打出来的日期都是 frontmatter 里那个字符串本身。

教训是: 只要一条数据同时经过 YAML、zod、浏览器三层, 就一定要问自己 —— 时区是在谁那里被解释的?
默认答案往往不是你以为的那个。
