import json, re

with open('extracted_posts.json', 'r', encoding='utf-8') as f:
    posts = json.load(f)

blog_posts = sorted([p for p in posts if p['post_type'] == 'post'],
                    key=lambda p: p.get('post_date') or '', reverse=True)

def clean_excerpt(content, length=130):
    text = re.sub(r'<[^>]+>', '', content or '')
    text = re.sub(r'&nbsp;', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return (text[:length] + '...') if len(text) > length else text

# ── Category definitions (slug lists) ──────────────────────────────────────
CATEGORIES = [
    {
        'title': 'Sediment Basics',
        'slugs': [
            'what-causes-sediment-buildup-in-water-heaters',
            'the-science-behind-sediment-buildup',
            'is-sediment-buildup-dangerous',
            '5-signs-your-water-heater-has-sediment-buildup',
            'how-sediment-impacts-your-water-heater',
            'keeping-your-water-heater-clear',
        ]
    },
    {
        'title': 'Cleaning &amp; Flushing',
        'slugs': [
            'how-to-clean-sediment',
            'how-to-flush-your-water-heater',
            'how-to-flush-a-tankless-water-heater',
            'how-often-should-you-flush-your-water-heater',
            'annual-maintenance-checklist-for-your-water-heater',
        ]
    },
    {
        'title': 'Hard Water',
        'slugs': [
            'hard-water-vs-soft-water',
            'how-hard-water-impacts-your-energy-bills',
            'the-link-between-hard-water-and-plumbing-repairs',
            'how-water-softeners-can-prevent-sediment-buildup',
            'how-to-test-your-water-for-hardness-at-home',
            'common-myths-about-water-heaters-and-hard-water',
        ]
    },
    {
        'title': 'Water Heater Types &amp; Technology',
        'slugs': [
            'tank-vs-tankless-water-heaters',
            'electric-vs-gas-water-heaters',
            'solar-water-heaters-hard-water',
            'hard-water-and-your-water-heater',
            'innovative-technologies-for-combating-hard-water',
            'comparing-the-longevity-of-different-water-heater-materials',
        ]
    },
]

# ── Featured articles ──────────────────────────────────────────────────────
# Each entry is either a slug string (looked up from WP posts)
# or a dict with {slug, title, excerpt} for manually created pillar pages.
FEATURED_SLUGS = [
    {'slug': 'sediment-buildup-in-water-heater',
     'title': 'Sediment Buildup in Water Heater: Complete Guide',
     'excerpt': 'Everything you need to know — causes, warning signs, dangers, and step-by-step removal. The definitive guide.'},
    {'slug': 'flush-water-heater-sediment',
     'title': 'Flush Water Heater Sediment: Full Guide',
     'excerpt': 'When to flush, how often, what equipment you need, and a step-by-step process to clear sediment from any tank.'},
    {'slug': 'water-heater-sediment-removal',
     'title': 'Water Heater Sediment Removal: Methods &amp; Costs',
     'excerpt': 'DIY vs. professional removal methods, real cost breakdowns, and when to replace instead of clean.'},
    {'slug': 'hard-water-water-heater-damage',
     'title': 'Hard Water Water Heater Damage: Signs &amp; Prevention',
     'excerpt': 'Hard water silently cuts your water heater lifespan in half. Learn the signs, real costs, and how to stop the damage.'},
    {'slug': 'water-heater-anode-rod-sediment',
     'title': 'Water Heater Anode Rod &amp; Sediment: The Connection',
     'excerpt': 'The anode rod directly affects sediment and rust buildup. Learn when to inspect it, replace it, and flush at the same time.'},
    'how-to-clean-sediment',
    'how-to-flush-your-water-heater',
    '5-signs-your-water-heater-has-sediment-buildup',
    'is-sediment-buildup-dangerous',
    'hard-water-vs-soft-water',
    'what-causes-sediment-buildup-in-water-heaters',
]

post_by_slug = {p['post_name']: p for p in blog_posts}

# Build featured cards HTML
featured_html = ''
for item in FEATURED_SLUGS:
    if isinstance(item, dict):
        slug, title, excerpt = item['slug'], item['title'], item['excerpt']
    else:
        p = post_by_slug.get(item)
        if not p:
            continue
        slug = p['post_name']
        title = p['post_title']
        excerpt = clean_excerpt(p.get('post_content', ''))
    featured_html += f'''      <div class="feat-card">
        <h3><a href="/{slug}/">{title}</a></h3>
        <p>{excerpt}</p>
        <a href="/{slug}/" class="read-more">Read guide &rarr;</a>
      </div>\n'''

# Build category sections HTML
categories_html = ''
for cat in CATEGORIES:
    items = ''
    for slug in cat['slugs']:
        p = post_by_slug.get(slug)
        if not p:
            continue
        items += f'        <li><a href="/{p["post_name"]}/">{p["post_title"]}</a></li>\n'
    if items:
        categories_html += f'''    <div class="cat-section">
      <h3>{cat["title"]}</h3>
      <ul class="cat-list">
{items}      </ul>
    </div>\n'''

FOOTER = '''  <footer>
    &copy; Tank Sediment &mdash;
    <a href="/affiliate-disclosure/">Affiliate Disclosure</a> &middot;
    <a href="/privacy-policy/">Privacy Policy</a> &middot;
    <a href="/disclaimer/">Disclaimer</a> &middot;
    <a href="/terms-and-conditions/">Terms &amp; Conditions</a> &middot;
    <a href="/contact-us/">Contact Us</a>
  </footer>'''

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Tank Sediment | Water Heater Maintenance &amp; Sediment Removal</title>
  <meta name="description" content="Expert guides on water heater sediment removal, flushing, and maintenance. Call us at 855-755-4920.">
  <style>
    *,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
    body{{font-family:Georgia,serif;color:#222;background:#fff;line-height:1.75}}
    a{{color:#1a6fa8;text-decoration:none}}
    a:hover{{text-decoration:underline}}
    header{{background:#1a3a4a;padding:1rem 2rem;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:1rem}}
    .site-title a{{color:#fff;font-size:1.4rem;font-weight:bold}}
    nav a{{color:#cde;font-size:.9rem;margin-left:1.2rem}}
    nav a:hover{{color:#fff}}
    .phone-cta{{color:#fff;font-weight:bold;font-size:.9rem;background:rgba(255,255,255,.12);padding:.3rem .85rem;border-radius:3px;white-space:nowrap;margin-left:1.2rem}}
    .phone-cta:hover{{background:rgba(255,255,255,.25);text-decoration:none}}

    /* Hero */
    .hero{{background:#1a3a4a;color:#fff;padding:4rem 2rem;text-align:center}}
    .hero h1{{font-size:2.2rem;color:#fff;margin-bottom:1rem;line-height:1.3;max-width:680px;margin-left:auto;margin-right:auto}}
    .hero p{{color:#cde;font-size:1.05rem;margin-bottom:1.5rem}}
    .cta-phone{{display:inline-block;background:#fff;color:#1a3a4a;font-weight:bold;font-size:1.3rem;padding:.75rem 2rem;border-radius:4px;letter-spacing:.02em}}
    .cta-phone:hover{{background:#e8f0f7;text-decoration:none}}

    /* Intro */
    .intro{{max-width:820px;margin:0 auto;padding:2.5rem 1.5rem 1rem}}
    .intro p{{font-size:1.05rem;color:#444;margin-bottom:1rem}}

    /* Featured */
    .featured{{max-width:960px;margin:0 auto;padding:1rem 1.5rem 2.5rem}}
    .featured h2{{font-size:1.5rem;color:#1a3a4a;margin-bottom:1.2rem}}
    .feat-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:1.2rem}}
    .feat-card{{border:1px solid #e0eaf2;border-radius:6px;padding:1.3rem;background:#f7fafd}}
    .feat-card h3{{font-size:1rem;color:#1a3a4a;margin-bottom:.4rem;line-height:1.4}}
    .feat-card h3 a{{color:inherit}}
    .feat-card h3 a:hover{{color:#1a6fa8;text-decoration:none}}
    .feat-card p{{font-size:.88rem;color:#666;margin-bottom:.75rem}}
    .read-more{{font-size:.88rem;color:#1a6fa8;font-weight:bold}}

    /* Categories */
    .categories{{background:#f7fafd;padding:2.5rem 1.5rem}}
    .categories-inner{{max-width:960px;margin:0 auto}}
    .categories h2{{font-size:1.5rem;color:#1a3a4a;margin-bottom:1.5rem}}
    .cat-grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:1.5rem}}
    .cat-section h3{{font-size:1.05rem;color:#1a3a4a;font-weight:bold;margin-bottom:.6rem;padding-bottom:.4rem;border-bottom:2px solid #1a6fa8}}
    .cat-list{{list-style:none;padding:0}}
    .cat-list li{{padding:.35rem 0;border-bottom:1px solid #e8e8e8}}
    .cat-list li:last-child{{border-bottom:none}}
    .cat-list a{{color:#333;font-size:.95rem}}
    .cat-list a:hover{{color:#1a6fa8}}

    footer{{background:#111e26;color:#aaa;text-align:center;padding:1.5rem;font-size:.82rem;line-height:2;margin-top:0}}
    footer a{{color:#8ab}}
    footer a:hover{{color:#fff}}
    @media(max-width:900px){{
      .feat-grid{{grid-template-columns:repeat(2,1fr)}}
      .cat-grid{{grid-template-columns:repeat(2,1fr)}}
    }}
    @media(max-width:560px){{
      .hero h1{{font-size:1.6rem}}
      .hero p{{font-size:.95rem}}
      .cta-phone{{font-size:1.1rem;padding:.65rem 1.4rem}}
      .feat-grid{{grid-template-columns:1fr}}
      .cat-grid{{grid-template-columns:1fr}}
      header{{padding:.75rem 1rem}}
      nav a{{margin-left:.7rem;font-size:.85rem}}
      .intro{{padding:1.5rem 1rem .5rem}}
      .featured{{padding:.5rem 1rem 1.5rem}}
      .categories{{padding:1.5rem 1rem}}
    }}
  </style>
</head>
<body>
  <header>
    <div class="site-title"><a href="/">Tank Sediment</a></div>
    <nav>
      <a href="/">Home</a>
      <a href="/blog/">Blog</a>
      <a href="/contact-us/">Contact Us</a>
      <a href="tel:8557554920" class="phone-cta">&#128222; 855-755-4920</a>
    </nav>
  </header>

  <div class="hero">
    <h1>Water Heater Sediment &mdash; Guides, Tips &amp; Fixes</h1>
    <p>Expert advice on cleaning, flushing, and maintaining your water heater.<br>Have a question? Call us now:</p>
    <a href="tel:8557554920" class="cta-phone">&#128222; 855-755-4920</a>
  </div>

  <div class="intro">
    <p>Sediment buildup is one of the most common &mdash; and most overlooked &mdash; causes of water heater inefficiency. Minerals like calcium and magnesium settle at the bottom of your tank over time, reducing heating efficiency, raising energy bills, and shortening the lifespan of your unit.</p>
    <p>Whether you need a step-by-step flushing guide, want to understand hard water, or are comparing tank vs. tankless heaters, you'll find everything you need below.</p>
  </div>

  <div class="featured">
    <h2>Start Here &mdash; Most Popular Guides</h2>
    <div class="feat-grid">
{featured_html}    </div>
  </div>

  <div class="categories">
    <div class="categories-inner">
      <h2>Browse by Topic</h2>
      <div class="cat-grid">
{categories_html}      </div>
    </div>
  </div>

{FOOTER}
</body>
</html>'''

with open('static_site/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Done - homepage rebuilt')
