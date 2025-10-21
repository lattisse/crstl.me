#!/usr/bin/env python3
import os
import markdown
from datetime import datetime

# Paths
POSTS_MD = "posts-md"
BLOGS_HTML = "blogs"
TEMPLATES = "templates"

# Load templates
with open(os.path.join(TEMPLATES, "post.html"), "r", encoding="utf-8") as f:
    POST_TEMPLATE = f.read()

blog_index_template_path = os.path.join(TEMPLATES, "blog.html")
blog_index_template: str = ""
if os.path.exists(blog_index_template_path):
    with open(blog_index_template_path, "r", encoding="utf-8") as f:
        blog_index_template = f.read()

# Ensure output folder exists
os.makedirs(BLOGS_HTML, exist_ok=True)

# Collect posts
posts_data: list[tuple[str, str, str, str]] = []

for filename in os.listdir(POSTS_MD):
    if not filename.endswith(".md"):
        continue

    filepath = os.path.join(POSTS_MD, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.read().split("\n")

    # Defaults
    title: str = filename.replace(".md", "").replace("-", " ").title()
    date: str = datetime.now().strftime("%Y-%m-%d")
    tag: str = ""

    # parse frontmatter
    # expects: title:, date:, tag: (in any order)
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("title:"):
            title = line.split(":", 1)[1].strip()
            lines.pop(i)
            continue
        if line.startswith("date:"):
            date = line.split(":", 1)[1].strip()
            lines.pop(i)
            continue
        if line.startswith("tag:"):
            tag = line.split(":", 1)[1].strip()
            lines.pop(i)
            continue
        i += 1

    md_content = "\n".join(lines)
    html_content = markdown.markdown(md_content, extensions=["fenced_code", "tables"])

    # Build post HTML
    post_html = (
        POST_TEMPLATE.replace("{{ title }}", title)
        .replace("{{ date }}", date)
        .replace("{{ tag }}", tag)
        .replace("{{ content }}", html_content)
    )

    post_name = filename.replace(".md", "")
    post_folder = os.path.join(BLOGS_HTML, post_name)
    os.makedirs(post_folder, exist_ok=True)

    # write index.html inside folder
    out_path = os.path.join(post_folder, "index.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(post_html)

    # store folder name for index links
    posts_data.append((title, date, post_name, tag))

# Generate blog index
if blog_index_template:
    post_entries: list[str] = []
    # sort by actual datetime descending
    sorted_posts = sorted(
        posts_data, key=lambda x: datetime.strptime(x[1], "%Y-%m-%d"), reverse=True
    )

    for title, date, filename, tag in sorted_posts:
        entry = f'''
        <li>
            <a href="{filename}/">{title}</a>
            <span class="date">{date}</span>
            <p class="tagline">{tag}</p>
        </li>
        '''

        post_entries.append(entry)

    posts_list_html: str = "<ul>\n" + "\n".join(post_entries) + "\n</ul>"
    blog_index_html: str = blog_index_template.replace("{{ posts }}", posts_list_html)

    with open(os.path.join(BLOGS_HTML, "index.html"), "w", encoding="utf-8") as f:
        f.write(blog_index_html)

    print("Generated blogs/index.html")
else:
    print("No blog index template found — skipped index generation.")
