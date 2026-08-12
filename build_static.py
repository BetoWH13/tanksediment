import json
import os
import re

"""Safe incremental static builder for TankSediment.

The committed files in static_site are the editorial source of truth. This script
never deletes or overwrites an existing page. extracted_posts.json is legacy
inventory and is used only to create a page that is genuinely missing.

The homepage is maintained by build_homepage.py. The curated blog hub is also
maintained directly in static_site/blog/index.html.
"""

OUT_DIR = "static_site"
SITE_NAME = "Tank Sediment"
PHONE = "855-755-4920"

with open("extracted_posts.json", "r", encoding="utf-8") as f:
    posts = json.load(f)

os.makedirs(OUT_DIR, exist_ok=True)


def clean_content(content):
    if not content:
        return ""
    content = re.sub(r'<!-- /?wp:[^>]*-->', '', content)
    content = re.sub(r'(<p>|^)\s*&nbsp;\s*(</p>|$)', '', content, flags=re.MULTILINE)
    content = re.sub(r'&nbsp;', ' ', content)
    content = re.sub(r'<p>\s*</p>', '', content)
    content = re.sub(r'https?://tanksediment\.com/', '/', content)
    content = re.sub(r'<figure[^>]*>.*?</figure>', '', content, flags=re.DOTALL)
    content = re.sub(r'<img[^>]*/?>', '', content, flags=re.DOTALL)
    content = re.sub(r'607[\s.\-]?610[\s.\-]?3115', PHONE, content)
    content = re.sub(r'<h1([^>]*)>', r'<h2\1>', content, flags=re.IGNORECASE)
    content = re.sub(r'</h1>', '</h2>', content, flags=re.IGNORECASE)
    content = re.sub(r'\n{3,}', '\n\n', content)
    return content.strip()


def render_page(title, body):
    return f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>{title} | {SITE_NAME}</title>
<style>body{{margin:0;font-family:Georgia,'Times New Roman',serif;color:#222;line-height:1.75}}a{{color:#1a6fa8;text-decoration:none}}header{{background:#1a3a4a;color:#fff;padding:1rem 2rem;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:1rem}}header a{{color:#cde}}.brand a{{color:#fff;font-size:1.4rem;font-weight:bold}}main{{max-width:820px;margin:auto;padding:2.5rem 1.5rem}}h1,h2{{color:#1a3a4a}}footer{{background:#111e26;color:#aaa;text-align:center;padding:1.4rem;font-size:.82rem}}footer a{{color:#8ab}}</style></head>
<body><header><div class="brand"><a href="/">{SITE_NAME}</a></div><nav><a href="/">Home</a> · <a href="/blog/">Blog</a> · <a href="/contact-us/">Contact</a> · <a href="tel:8557554920">{PHONE}</a></nav></header>
<main>{body}</main><footer>&copy; {SITE_NAME} — <a href="/affiliate-disclosure/">Affiliate Disclosure</a> · <a href="/privacy-policy/">Privacy Policy</a> · <a href="/disclaimer/">Disclaimer</a> · <a href="/terms-and-conditions/">Terms</a></footer></body></html>'''


created = 0
preserved = 0
for post in posts:
    slug = post.get("post_name", "").strip()
    if not slug or slug == "tank-sediment":
        continue

    rel = os.path.join(slug, "index.html")
    full_path = os.path.join(OUT_DIR, rel)

    # Existing committed output is curated. Never overwrite it from the legacy export.
    if os.path.isfile(full_path):
        print(f"  Preserved: {rel}")
        preserved += 1
        continue

    # The blog hub should normally already exist. If it is absent, fail visibly
    # rather than silently rebuilding a stale hub from old excerpts.
    if slug == "blog":
        raise RuntimeError("static_site/blog/index.html is missing; restore the curated blog hub instead of regenerating it from extracted_posts.json")

    content = clean_content(post.get("post_content", ""))
    date_str = (post.get("post_date") or "")[:10]
    meta = f'<p style="color:#777;font-size:.9rem">Published: {date_str}</p>' if post.get("post_type") == "post" and date_str else ""
    body = f"<h1>{post.get('post_title','Untitled')}</h1>{meta}{content}"

    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(render_page(post.get("post_title", "Untitled"), body))
    print(f"  Created missing page: {rel}")
    created += 1

print(f"\nDone. Preserved {preserved} curated pages; created {created} missing pages. No existing page was overwritten.")