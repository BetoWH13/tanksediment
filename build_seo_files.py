import json, os
from datetime import date

DOMAIN = "https://tanksediment.com"
TODAY = date.today().isoformat()

with open("extracted_posts.json", "r", encoding="utf-8") as f:
    posts = json.load(f)

# All slugs from extracted posts (excluding homepage slug tank-sediment and blog placeholder)
post_slugs = [p["post_name"] for p in posts
              if p["post_name"] not in ("tank-sediment", "blog")]

# Static pages not in extracted_posts
static_slugs = [
    "",                        # homepage
    "blog",
    "affiliate-disclosure",
    "privacy-policy",
    "disclaimer",
]

all_urls = []

# Homepage first
all_urls.append(("", "1.0", "weekly"))

# Blog index
all_urls.append(("blog/", "0.9", "weekly"))

# Manually created pillar/SEO pages (high priority)
EXTRA_SLUGS = [
    "sediment-buildup-in-water-heater",
    "flush-water-heater-sediment",
    "water-heater-sediment-removal",
    "hard-water-water-heater-damage",
    "water-heater-anode-rod-sediment",
]
for slug in EXTRA_SLUGS:
    all_urls.append((f"{slug}/", "0.9", "weekly"))

# All post/page slugs
for slug in post_slugs:
    all_urls.append((f"{slug}/", "0.8", "monthly"))

# Legal pages (lower priority)
for slug in ["affiliate-disclosure", "privacy-policy", "disclaimer"]:
    all_urls.append((f"{slug}/", "0.3", "yearly"))

# ── sitemap.xml ────────────────────────────────────────────────────────────
sitemap_entries = ""
for path, priority, changefreq in all_urls:
    url = f"{DOMAIN}/{path}"
    sitemap_entries += f"""  <url>
    <loc>{url}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>{changefreq}</changefreq>
    <priority>{priority}</priority>
  </url>\n"""

sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{sitemap_entries}</urlset>"""

with open("static_site/sitemap.xml", "w", encoding="utf-8") as f:
    f.write(sitemap)
print(f"sitemap.xml written ({len(all_urls)} URLs)")

# ── robots.txt ─────────────────────────────────────────────────────────────
robots = f"""User-agent: *
Allow: /

Sitemap: {DOMAIN}/sitemap.xml
"""

with open("static_site/robots.txt", "w", encoding="utf-8") as f:
    f.write(robots)
print("robots.txt written")
