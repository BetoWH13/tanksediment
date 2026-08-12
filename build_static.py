import json
import os
import re
import shutil

with open("extracted_posts.json", "r", encoding="utf-8") as f:
    posts = json.load(f)

OUT_DIR = "static_site"

# Files/pages that are maintained directly in static_site and must survive rebuilds.
# In addition to the fixed infrastructure files below, preserve every existing
# one-level */index.html page except the blog hub. This prevents old content in
# extracted_posts.json from overwriting the safety/editorial cleanup work.
PRESERVE = {
    "404.html",
    "robots.txt",
    "sitemap.xml",
    "affiliate-disclosure/index.html",
    "privacy-policy/index.html",
    "disclaimer/index.html",
    "calculator/index.html",
}

if os.path.isdir(OUT_DIR):
    for name in os.listdir(OUT_DIR):
        rel = f"{name}/index.html"
        if name != "blog" and os.path.isfile(os.path.join(OUT_DIR, rel)):
            PRESERVE.add(rel)

preserved = {}
for fname in PRESERVE:
    fpath = os.path.join(OUT_DIR, fname)
    if os.path.isfile(fpath):
        with open(fpath, "r", encoding="utf-8") as f:
            preserved[fname] = f.read()

if os.path.exists(OUT_DIR):
    shutil.rmtree(OUT_DIR)
os.makedirs(OUT_DIR)

for fname, content in preserved.items():
    full = os.path.join(OUT_DIR, fname)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)

SITE_NAME = "Tank Sediment"
SKIP_FROM_NAV = {"blog", "tank-sediment"}
FOOTER_PAGES = {"terms-and-conditions"}

blog_posts = sorted(
    [p for p in posts if p["post_type"] == "post"],
    key=lambda p: p.get("post_date") or "",
    reverse=True,
)
nav_pages = [
    p for p in posts
    if p["post_type"] == "page"
    and p["post_name"] not in SKIP_FROM_NAV
    and p["post_name"] not in FOOTER_PAGES
]


def clean_content(content, strip_title=None):
    if not content:
        return ""
    content = re.sub(r'<!-- /?wp:[^>]*-->', '', content)
    content = re.sub(r'(<p>|^)\s*&nbsp;\s*(</p>|$)', '', content, flags=re.MULTILINE)
    content = re.sub(r'&nbsp;', ' ', content)
    content = re.sub(r'<p>\s*</p>', '', content)
    content = re.sub(r'https?://tanksediment\.com/', '/', content)
    content = re.sub(r'style="[^"]*background[^"]*"', '', content, flags=re.IGNORECASE)
    content = re.sub(r'<figure[^>]*>.*?</figure>', '', content, flags=re.DOTALL)
    content = re.sub(r'<img[^>]*/?>', '', content, flags=re.DOTALL)
    content = re.sub(r'<ul>\s*<li style="list-style-type: none;">\s*<ul>', '<ul>', content)
    content = re.sub(r'</ul>\s*</li>\s*</ul>', '</ul>', content)
    content = re.sub(r'607[\s.\-]?610[\s.\-]?3115', '855-755-4920', content)
    content = re.sub(r'<h1([^>]*)>', r'<h2\1>', content, flags=re.IGNORECASE)
    content = re.sub(r'</h1>', r'</h2>', content, flags=re.IGNORECASE)
    content = re.sub(r'\n{3,}', '\n\n', content)
    return content.strip()


def auto_excerpt(post, length=145):
    text = re.sub(r'<[^>]+>', '', clean_content(post["post_content"]))
    text = re.sub(r'\s+', ' ', text).strip()
    return (text[:length].rstrip() + "…") if len(text) > length else text


def build_nav(current_slug):
    items = ['<a href="/"' + (' class="active"' if current_slug == "home" else "") + '>Home</a>']
    items.append('<a href="/blog/"' + (' class="active"' if current_slug == "blog" else "") + '>Blog</a>')
    for p in nav_pages:
        active = ' class="active"' if p["post_name"] == current_slug else ""
        items.append(f'<a href="/{p["post_name"]}/"{active}>{p["post_title"]}</a>')
    return "\n".join(items)


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | {site_name}</title>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: Georgia, 'Times New Roman', serif; color: #222; background: #fff; line-height: 1.75; }}
    a {{ color: #1a6fa8; text-decoration: none; }} a:hover {{ text-decoration: underline; }}
    header {{ background:#1a3a4a; color:#fff; padding:1rem 2rem; display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:1rem; }}
    .site-title {{ font-size:1.4rem; font-weight:bold; letter-spacing:.03em; }} .site-title a {{ color:#fff; }}
    nav {{ display:flex; gap:1.2rem; flex-wrap:wrap; align-items:center; }} nav a {{ color:#cde; font-size:.9rem; }} nav a:hover, nav a.active {{ color:#fff; }}
    .phone-cta {{ color:#fff; font-weight:bold; background:rgba(255,255,255,.12); padding:.3rem .85rem; border-radius:3px; white-space:nowrap; }}
    .container {{ max-width:1040px; margin:0 auto; padding:2.8rem 1.5rem; }}
    h1 {{ font-size:2.1rem; margin-bottom:.5rem; color:#1a3a4a; line-height:1.25; }} h2 {{ font-size:1.45rem; margin:2rem 0 .7rem; color:#1a3a4a; }} h3 {{ font-size:1.1rem; color:#333; }}
    p {{ margin-bottom:1.1rem; }} ul,ol {{ margin:0 0 1.1rem 1.6rem; }} li {{ margin-bottom:.35rem; }}
    .post-meta {{ color:#888; font-size:.88rem; margin-bottom:1.5rem; }} .post-content {{ max-width:820px; margin:0 auto; }}
    blockquote {{ border-left:4px solid #1a6fa8; padding:.5rem 1rem; margin:1.5rem 0; color:#555; background:#f7fafd; }}
    table {{ width:100%; border-collapse:collapse; margin-bottom:1.5rem; font-size:.95rem; }} th,td {{ border:1px solid #ddd; padding:.55rem .8rem; text-align:left; }} th {{ background:#f0f4f8; }}
    .hub-intro {{ display:grid; grid-template-columns:1.4fr .8fr; gap:1rem; align-items:stretch; margin:1.2rem 0 2.2rem; }}
    .hub-lead {{ background:linear-gradient(135deg,#f5f9fb,#e8f1f5); border:1px solid #d7e5ec; border-radius:12px; padding:1.6rem; }} .hub-lead p {{ color:#4b5c65; margin:0; max-width:680px; }}
    .service-card {{ background:#1a3a4a; color:#fff; border-radius:12px; padding:1.5rem; display:flex; flex-direction:column; justify-content:center; }} .service-card h2 {{ color:#fff; margin:0 0 .45rem; }} .service-card p {{ color:#d5e4eb; font-size:.93rem; }} .service-card a {{ display:inline-block; width:max-content; background:#fff; color:#1a3a4a; font-weight:bold; padding:.55rem .9rem; border-radius:5px; }}
    .section-kicker {{ text-transform:uppercase; letter-spacing:.09em; font-size:.75rem; color:#70838d; font-weight:bold; margin-bottom:.25rem; }}
    .featured-grid {{ display:grid; grid-template-columns:repeat(3,1fr); gap:1rem; margin:1rem 0 2.4rem; }} .featured-card {{ border:1px solid #dce6eb; border-radius:12px; padding:1.35rem; background:#fff; box-shadow:0 6px 20px rgba(20,50,65,.06); display:flex; flex-direction:column; min-height:235px; }}
    .featured-card .tag,.article-card .tag {{ display:inline-block; width:max-content; font:700 .72rem/1.2 Arial,sans-serif; letter-spacing:.04em; text-transform:uppercase; color:#46606d; background:#edf4f7; border-radius:999px; padding:.3rem .55rem; margin-bottom:.75rem; }}
    .featured-card h2 {{ margin:0 0 .55rem; font-size:1.22rem; }} .featured-card p {{ color:#596970; font-size:.93rem; flex:1; }} .read-link {{ font-weight:bold; font-size:.9rem; }}
    .topic-strip {{ display:grid; grid-template-columns:repeat(4,1fr); gap:.75rem; margin:1rem 0 2.5rem; }} .topic-pill {{ border:1px solid #dce6eb; border-radius:10px; padding:1rem; background:#f9fbfc; }} .topic-pill strong {{ display:block; color:#1a3a4a; margin-bottom:.2rem; }} .topic-pill span {{ color:#667780; font-size:.85rem; }}
    .article-grid {{ display:grid; grid-template-columns:repeat(3,1fr); gap:.9rem; margin-top:1rem; }} .article-card {{ border:1px solid #e0e7ea; border-radius:10px; padding:1.15rem; background:#fff; display:flex; flex-direction:column; min-height:210px; transition:transform .15s ease, box-shadow .15s ease; }} .article-card:hover {{ transform:translateY(-2px); box-shadow:0 8px 20px rgba(20,50,65,.08); }} .article-card h2 {{ font-size:1.05rem; margin:0 0 .45rem; line-height:1.35; }} .article-card p {{ color:#617078; font-size:.88rem; flex:1; margin-bottom:.8rem; }}
    footer {{ background:#111e26; color:#aaa; text-align:center; padding:1.5rem; font-size:.82rem; margin-top:3rem; line-height:2; }} footer a {{ color:#8ab; }}
    @media(max-width:820px) {{ .hub-intro{{grid-template-columns:1fr}} .featured-grid,.article-grid{{grid-template-columns:repeat(2,1fr)}} .topic-strip{{grid-template-columns:repeat(2,1fr)}} }}
    @media(max-width:560px) {{ header{{padding:.75rem 1rem}} nav{{gap:.7rem}} nav a{{font-size:.82rem}} .container{{padding:1.5rem 1rem}} h1{{font-size:1.65rem}} .featured-grid,.article-grid,.topic-strip{{grid-template-columns:1fr}} .featured-card,.article-card{{min-height:0}} }}
  </style>
</head>
<body>
<header><div class="site-title"><a href="/">{site_name}</a></div><nav>{nav}<a href="tel:8557554920" class="phone-cta">&#128222; 855-755-4920</a></nav></header>
<div class="container">{body}</div>
<footer>&copy; {site_name} &mdash; <a href="/affiliate-disclosure/">Affiliate Disclosure</a> &middot; <a href="/privacy-policy/">Privacy Policy</a> &middot; <a href="/disclaimer/">Disclaimer</a> &middot; <a href="/terms-and-conditions/">Terms &amp; Conditions</a> &middot; <a href="/contact-us/">Contact Us</a></footer>
</body></html>"""


def render_page(title, body_html, slug):
    return HTML_TEMPLATE.format(title=title, site_name=SITE_NAME, nav=build_nav(slug), body=body_html)


def write_page(path, html):
    full_path = os.path.join(OUT_DIR, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  Written: {path}")


def topic_for(post):
    text = f"{post['post_name']} {post['post_title'].lower()}"
    if "tankless" in text or "electric-vs-gas" in text or "tank-vs" in text or "materials" in text or "solar" in text:
        return "Heater types"
    if "hard-water" in text or "soft-water" in text or "softener" in text or "hardness" in text:
        return "Hard water"
    if "flush" in text or "clean" in text or "maintenance" in text:
        return "Maintenance"
    return "Sediment signs"


def blog_hub_body():
    by_slug = {p["post_name"]: p for p in blog_posts}
    featured_slugs = [
        "water-heater-sediment-removal",
        "how-to-flush-a-tankless-water-heater",
        "5-signs-your-water-heater-has-sediment-buildup",
    ]
    featured = [by_slug[s] for s in featured_slugs if s in by_slug]
    featured_set = {p["post_name"] for p in featured}
    featured_html = "".join(
        f'''<article class="featured-card"><span class="tag">{topic_for(p)}</span><h2><a href="/{p['post_name']}/">{p['post_title']}</a></h2><p>{auto_excerpt(p,165)}</p><a class="read-link" href="/{p['post_name']}/">Open guide &rarr;</a></article>'''
        for p in featured
    )
    cards_html = "".join(
        f'''<article class="article-card"><span class="tag">{topic_for(p)}</span><h2><a href="/{p['post_name']}/">{p['post_title']}</a></h2><p>{auto_excerpt(p,125)}</p><a class="read-link" href="/{p['post_name']}/">Read guide &rarr;</a></article>'''
        for p in blog_posts if p["post_name"] not in featured_set
    )
    return f'''
      <h1>Water Heater &amp; Sediment Guides</h1>
      <div class="hub-intro">
        <div class="hub-lead"><div class="section-kicker">Start with the problem</div><h2>Find the guide that matches what you are seeing.</h2><p>Use these guides to understand sediment, hard water, maintenance decisions, and when a water-heater problem deserves professional service. The goal is useful decision support — not risky one-size-fits-all repair instructions.</p></div>
        <aside class="service-card"><h2>Rather have someone look at it?</h2><p>The call may connect you with an independent third-party service provider or service network.</p><a href="tel:8557554920">Call 855-755-4920</a></aside>
      </div>
      <div class="section-kicker">Good places to start</div><h2>Featured guides</h2><div class="featured-grid">{featured_html}</div>
      <div class="section-kicker">Browse the library</div><h2>Choose a topic</h2>
      <div class="topic-strip"><div class="topic-pill"><strong>Sediment signs</strong><span>Symptoms, causes &amp; what they may mean</span></div><div class="topic-pill"><strong>Maintenance</strong><span>Flush, clean &amp; service decisions</span></div><div class="topic-pill"><strong>Hard water</strong><span>Hardness, scale &amp; treatment context</span></div><div class="topic-pill"><strong>Heater types</strong><span>Tank, tankless, gas, electric &amp; solar</span></div></div>
      <div class="section-kicker">All guides</div><h2>Explore the full library</h2><div class="article-grid">{cards_html}</div>
    '''


written = 0
for post in posts:
    slug = post["post_name"]
    if slug == "tank-sediment":
        continue
    if post["post_type"] == "page" and slug == "blog":
        write_page("blog/index.html", render_page("Guides", blog_hub_body(), "blog"))
        written += 1
        continue

    rel = f"{slug}/index.html"
    if rel in preserved:
        print(f"  Preserved: {rel}")
        continue

    content = clean_content(post["post_content"], strip_title=post["post_title"])
    date_str = (post.get("post_date") or "")[:10]
    meta = f'<div class="post-meta">Published: {date_str}</div>' if post["post_type"] == "post" and date_str else ""
    body = f"<div class='post-content'><h1>{post['post_title']}</h1>{meta}{content}</div>"
    write_page(rel, render_page(post["post_title"], body, slug))
    written += 1

print(f"\nDone! {written} generated pages written to ./{OUT_DIR}/; curated pages preserved.")