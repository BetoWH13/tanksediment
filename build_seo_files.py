import os
from datetime import date

DOMAIN = "https://tanksediment.com"
OUT_DIR = "static_site"
TODAY = date.today().isoformat()


def existing_routes():
    routes = []
    if os.path.isfile(os.path.join(OUT_DIR, "index.html")):
        routes.append("")
    if os.path.isdir(OUT_DIR):
        for name in sorted(os.listdir(OUT_DIR)):
            if os.path.isfile(os.path.join(OUT_DIR, name, "index.html")):
                routes.append(f"{name}/")
    return routes


def seo_meta(route):
    slug = route.rstrip("/")
    if route == "":
        return "1.0", "weekly"
    if slug == "blog":
        return "0.9", "weekly"
    if slug in {
        "sediment-buildup-in-water-heater",
        "flush-water-heater-sediment",
        "water-heater-sediment-removal",
        "hard-water-water-heater-damage",
        "water-heater-anode-rod-sediment",
        "calculator",
    }:
        return "0.9", "weekly"
    if slug in {"affiliate-disclosure", "privacy-policy", "disclaimer", "terms-and-conditions"}:
        return "0.3", "yearly"
    return "0.8", "monthly"


routes = existing_routes()
entries = []
for route in routes:
    priority, changefreq = seo_meta(route)
    entries.append(f"""  <url>
    <loc>{DOMAIN}/{route}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>{changefreq}</changefreq>
    <priority>{priority}</priority>
  </url>""")

sitemap = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n" + "\n".join(entries) + "\n</urlset>\n"
with open(os.path.join(OUT_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write(sitemap)

robots = f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n"
with open(os.path.join(OUT_DIR, "robots.txt"), "w", encoding="utf-8") as f:
    f.write(robots)

print(f"SEO files written from {len(routes)} actual static routes.")