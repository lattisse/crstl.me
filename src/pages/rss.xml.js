import rss from "@astrojs/rss";
import { getCollection } from "astro:content";

export async function GET() {
  const posts = await getCollection("blog");

  return rss({
    title: "Crystal's Blog",
    description:
      "Linux, coding, physics, and the universe. Mostly random stuff I find cool or want to experiment with.",
    site: "https://crstl.me",
    items: posts
      .sort((a, b) => b.data.pubDate - a.data.pubDate)
      .map((post) => ({
        title: post.data.title,
        description: post.data.description,
        link: `/blog/${post.id}`,
        pubDate: post.data.pubDate,
      })),
  });
}
