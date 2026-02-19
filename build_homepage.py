import json, re

with open('extracted_posts.json', 'r', encoding='utf-8') as f:
    posts = json.load(f)

blog_posts = sorted([p for p in posts if p['post_type'] == 'post'],
                    key=lambda p: p.get('post_date') or '', reverse=True)

links = ''
for p in blog_posts:
    links += f'<li><a href="/{p["post_name"]}/">{p["post_title"]}</a></li>\n'

html = f"""<!DOCTYPE html>
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
    .hero{{background:#1a3a4a;color:#fff;padding:3.5rem 2rem;text-align:center}}
    .hero h1{{font-size:2.2rem;color:#fff;margin-bottom:1rem;line-height:1.3}}
    .hero p{{color:#cde;font-size:1.1rem;margin-bottom:1.5rem}}
    .cta-phone{{display:inline-block;background:#fff;color:#1a3a4a;font-weight:bold;font-size:1.3rem;padding:.75rem 2rem;border-radius:4px;letter-spacing:.02em}}
    .cta-phone:hover{{background:#e8f0f7;text-decoration:none}}
    .container{{max-width:820px;margin:0 auto;padding:2.5rem 1.5rem}}
    h2{{font-size:1.5rem;color:#1a3a4a;margin-bottom:1rem}}
    ul.post-list{{list-style:none;padding:0}}
    ul.post-list li{{border-bottom:1px solid #eee;padding:.75rem 0}}
    ul.post-list li:last-child{{border-bottom:none}}
    ul.post-list a{{color:#1a3a4a;font-size:1rem}}
    ul.post-list a:hover{{color:#1a6fa8}}
    footer{{background:#111e26;color:#aaa;text-align:center;padding:1.5rem;font-size:.82rem;line-height:2}}
    footer a{{color:#8ab}}
  </style>
</head>
<body>
  <header>
    <div class="site-title"><a href="/">Tank Sediment</a></div>
    <nav>
      <a href="/">Home</a>
      <a href="/blog/">Blog</a>
      <a href="/contact-us/">Contact Us</a>
    </nav>
  </header>

  <div class="hero">
    <h1>Water Heater Sediment &mdash; Guides, Tips &amp; Fixes</h1>
    <p>Expert advice on cleaning, flushing, and maintaining your water heater.<br>Have a question? Call us now:</p>
    <a href="tel:8557554920" class="cta-phone">&#128222; 855-755-4920</a>
  </div>

  <div class="container">
    <h2>All Articles</h2>
    <ul class="post-list">
{links}    </ul>
  </div>

  <footer>
    &copy; Tank Sediment &mdash;
    <a href="/terms-and-conditions/">Terms and Conditions</a> &middot;
    <a href="/contact-us/">Contact Us</a>
  </footer>
</body>
</html>"""

with open('static_site/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Done')
