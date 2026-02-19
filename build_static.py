import json
import os
import re
import shutil

with open("extracted_posts.json", "r", encoding="utf-8") as f:
    posts = json.load(f)

OUT_DIR = "static_site"
if os.path.exists(OUT_DIR):
    shutil.rmtree(OUT_DIR)
os.makedirs(OUT_DIR)

SITE_NAME = "Tank Sediment"

# Pages to show in nav (skip blog index slug — we add it manually; skip homepage slug)
SKIP_FROM_NAV = {"blog", "tank-sediment"}
# Legal/footer pages — show in footer only
FOOTER_PAGES = {"terms-and-conditions"}

blog_posts = sorted([p for p in posts if p["post_type"] == "post"],
                    key=lambda p: p.get("post_date") or "", reverse=True)

nav_pages = [p for p in posts
             if p["post_type"] == "page"
             and p["post_name"] not in SKIP_FROM_NAV
             and p["post_name"] not in FOOTER_PAGES]

def clean_content(content):
    if not content:
        return ""
    content = re.sub(r'<!-- /?wp:[^>]*-->', '', content)
    content = re.sub(r'<p>\s*(&nbsp;)?\s*</p>', '', content)
    content = re.sub(r'https?://tanksediment\.com/', '/', content)
    content = re.sub(r'style="[^"]*background[^"]*"', '', content, flags=re.IGNORECASE)
    content = re.sub(r'<figure[^>]*>.*?</figure>', '', content, flags=re.DOTALL)
    content = re.sub(r'<img[^>]*/?>',  '', content, flags=re.DOTALL)
    content = re.sub(r'\n{3,}', '\n\n', content)
    return content.strip()

def auto_excerpt(post, length=200):
    text = re.sub(r'<[^>]+>', '', clean_content(post["post_content"]))
    text = re.sub(r'\s+', ' ', text).strip()
    return (text[:length] + "...") if len(text) > length else text

def build_nav(current_slug):
    items = ['<a href="/"' + (' class="active"' if current_slug == "home" else "") + '>Home</a>']
    items.append('<a href="/blog/"' + (' class="active"' if current_slug == "blog" else "") + '>Blog</a>')
    for p in nav_pages:
        active = ' class="active"' if p["post_name"] == current_slug else ""
        items.append(f'<a href="/{p["post_name"]}/"' + active + f'>{p["post_title"]}</a>')
    return "\n".join(items)

def build_footer():
    links = []
    for p in posts:
        if p["post_name"] in FOOTER_PAGES:
            links.append(f'<a href="/{p["post_name"]}/">{p["post_title"]}</a>')
    return " &middot; ".join(links)

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | {site_name}</title>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: Georgia, 'Times New Roman', serif; color: #222; background: #fff; line-height: 1.75; }}
    a {{ color: #1a6fa8; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}

    header {{ background: #1a3a4a; color: #fff; padding: 1rem 2rem; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 1rem; }}
    .site-title {{ font-size: 1.4rem; font-weight: bold; letter-spacing: 0.03em; }}
    .site-title a {{ color: #fff; }}
    nav {{ display: flex; gap: 1.2rem; flex-wrap: wrap; }}
    nav a {{ color: #cde; font-size: 0.9rem; }}
    nav a:hover, nav a.active {{ color: #fff; text-decoration: underline; }}

    .container {{ max-width: 820px; margin: 0 auto; padding: 2.5rem 1.5rem; }}

    h1 {{ font-size: 2rem; margin-bottom: 0.4rem; color: #1a3a4a; line-height: 1.3; }}
    h2 {{ font-size: 1.45rem; margin: 2rem 0 0.6rem; color: #1a3a4a; }}
    h3 {{ font-size: 1.15rem; margin: 1.5rem 0 0.4rem; color: #333; }}
    h4 {{ font-size: 1rem; margin: 1.2rem 0 0.3rem; color: #444; }}
    p {{ margin-bottom: 1.1rem; }}
    ul, ol {{ margin: 0 0 1.1rem 1.6rem; }}
    li {{ margin-bottom: 0.35rem; }}
    blockquote {{ border-left: 4px solid #1a6fa8; padding: 0.5rem 1rem; margin: 1.5rem 0; color: #555; font-style: italic; background: #f7fafd; }}
    table {{ width: 100%; border-collapse: collapse; margin-bottom: 1.5rem; font-size: 0.95rem; }}
    th, td {{ border: 1px solid #ddd; padding: 0.55rem 0.8rem; text-align: left; }}
    th {{ background: #f0f4f8; font-weight: bold; }}
    hr {{ border: none; border-top: 1px solid #e0e0e0; margin: 1.5rem 0; }}
    .post-meta {{ color: #888; font-size: 0.88rem; margin-bottom: 1.5rem; }}
    .post-content {{ margin-top: 0.5rem; }}

    .blog-list {{ list-style: none; margin: 0; padding: 0; }}
    .blog-list li {{ border-bottom: 1px solid #eee; padding: 1.3rem 0; }}
    .blog-list li:last-child {{ border-bottom: none; }}
    .blog-list h2 {{ margin: 0 0 0.3rem; font-size: 1.2rem; }}
    .blog-list .excerpt {{ color: #555; font-size: 0.93rem; margin-top: 0.3rem; }}

    footer {{ background: #f5f5f5; border-top: 1px solid #ddd; text-align: center; padding: 1.5rem; font-size: 0.82rem; color: #777; margin-top: 3rem; line-height: 2; }}
    footer a {{ color: #666; }}
  </style>
</head>
<body>
  <header>
    <div class="site-title"><a href="/">{site_name}</a></div>
    <nav>{nav}</nav>
  </header>
  <div class="container">
    {body}
  </div>
  <footer>
    &copy; {site_name}<br>
    {footer_links}
  </footer>
</body>
</html>"""

def render_page(title, body_html, slug):
    return HTML_TEMPLATE.format(
        title=title,
        site_name=SITE_NAME,
        nav=build_nav(slug),
        body=body_html,
        footer_links=build_footer()
    )

def write_page(path, html):
    full_path = os.path.join(OUT_DIR, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  Written: {path}")

written = 0

# --- Individual pages and posts ---
for post in posts:
    slug = post["post_name"]
    content = clean_content(post["post_content"])

    if slug == "tank-sediment":
        # This is the WP front page — render as homepage
        items_html = ""
        for bp in blog_posts:
            excerpt = auto_excerpt(bp)
            items_html += f"""<li>
  <h2><a href="/{bp['post_name']}/">{bp['post_title']}</a></h2>
  <div class="excerpt">{excerpt}</div>
</li>"""
        body = f"{content}\n<h2>Latest Articles</h2>\n<ul class='blog-list'>{items_html}</ul>"
        html = render_page("Home", body, "home")
        write_page("index.html", html)
        written += 1

    elif post["post_type"] == "page" and slug == "blog":
        items_html = ""
        for bp in blog_posts:
            excerpt = auto_excerpt(bp)
            items_html += f"""<li>
  <h2><a href="/{bp['post_name']}/">{bp['post_title']}</a></h2>
  <div class="excerpt">{excerpt}</div>
</li>"""
        body = f"<h1>Blog</h1><ul class='blog-list'>{items_html}</ul>"
        html = render_page("Blog", body, "blog")
        write_page("blog/index.html", html)
        written += 1

    else:
        date_str = (post.get("post_date") or "")[:10]
        meta = f'<div class="post-meta">Published: {date_str}</div>' if post["post_type"] == "post" and date_str else ""
        body = f"<h1>{post['post_title']}</h1>{meta}<div class='post-content'>{content}</div>"
        html = render_page(post["post_title"], body, slug)
        write_page(f"{slug}/index.html", html)
        written += 1

print(f"\nDone! {written} pages written to ./{OUT_DIR}/")
