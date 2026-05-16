import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const blog = defineCollection({
	// Load Markdown and MDX files in the `src/content/blog/` directory.
	loader: glob({ base: './src/content/blog', pattern: '**/*.{md,mdx}' }),
	// Type-check frontmatter using a schema
	schema: ({ image }) =>
		z.object({
			title: z.string(),
			description: z.string(),
			// Transform string to Date object
			pubDate: z.coerce.date(),
			updatedDate: z.coerce.date().optional(),
			heroImage: z.optional(image()),
			// 🌙 夜间随笔标记 — true 时归入 /blog/night/ 子路由 + 详情页深紫主题
			night: z.boolean().optional().default(false),
		}),
});

// 🎵 唱片集 — 歌词 + Suno prompt 归档
const songs = defineCollection({
	loader: glob({ base: './src/content/songs', pattern: '**/*.{md,mdx}' }),
	schema: z.object({
		title: z.string(),
		// 副标题 / 体裁标签 (e.g. "国风慢板 trap")
		subtitle: z.string().optional(),
		// 首次成型日期
		pubDate: z.coerce.date(),
		// 最近一次编曲调整日期
		updatedDate: z.coerce.date().optional(),
		// 一句话简介 / 创作背景
		description: z.string().optional(),
		// Suno Style 字段 — 支持多版本编曲对照
		styles: z
			.array(
				z.object({
					version: z.string(), // v1 / v2 / ...
					label: z.string().optional(), // "首版" / "去二胡+Rhodes 暖底"
					date: z.coerce.date().optional(),
					prompt: z.string(),
					excludeStyles: z.string().optional(),
					charCount: z.number().optional(),
				}),
			)
			.default([]),
		// 平台 (suno / 网易天音 / heartmula)
		platform: z.enum(['suno', 'tianyin', 'heartmula', 'other']).default('suno'),
		// 状态: draft (草稿) / generated (跑过音频) / shipped (定稿)
		status: z.enum(['draft', 'generated', 'shipped']).default('draft'),
	}),
});

export const collections = { blog, songs };
