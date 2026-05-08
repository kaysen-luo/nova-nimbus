import { getCollection } from 'astro:content';
import rss from '@astrojs/rss';
import { SITE_DESCRIPTION, SITE_TITLE } from '../consts';

export async function GET(context) {
	// RSS 只推公开博客，夜间随笔是私人空间不进 feed
	const posts = await getCollection('blog', ({ data }) => data.night !== true);
	return rss({
		title: SITE_TITLE,
		description: SITE_DESCRIPTION,
		site: context.site,
		items: posts.map((post) => ({
			...post.data,
			link: `${import.meta.env.BASE_URL}blog/${post.id}/`,
		})),
	});
}
