"""Rebuild the Tank Sediment homepage without reintroducing legacy claims.

The public homepage is intentionally informational. Do not add claims that the site
is a plumbing company, physical sediment estimates, universal maintenance intervals,
or unsupported lifespan/efficiency promises here.
"""
from pathlib import Path

FEATURED = [
    ("sediment-buildup-in-water-heater", "Sediment Buildup in a Water Heater", "What sediment is, why it can accumulate, common signs, and questions to consider before maintenance or service."),
    ("flush-water-heater-sediment", "Water Heater Flushing", "Understand what flushing is intended to do, when owners commonly consider it, and why heater condition matters before work begins."),
    ("water-heater-sediment-removal", "Sediment Removal Options", "Compare maintenance and professional-service paths without assuming every heater should be handled the same way."),
    ("hard-water-water-heater-damage", "Hard Water and Water Heaters", "How mineral-rich water relates to scale formation and why local water conditions can change maintenance needs."),
    ("water-heater-anode-rod-sediment", "Anode Rods and Sediment", "Learn the different roles of corrosion protection, mineral scale, rust, and tank maintenance."),
    ("5-signs-your-water-heater-has-sediment-buildup", "Signs Worth Investigating", "Noises, changes in hot-water performance, and visible discharge can have more than one cause. Start with context rather than a diagnosis."),
]

CATEGORIES = [
    ("Sediment Basics", [
        ("what-causes-sediment-buildup-in-water-heaters", "What Causes Sediment Buildup?"),
        ("the-science-behind-sediment-buildup", "The Science Behind Sediment"),
        ("is-sediment-buildup-dangerous", "Is Sediment Buildup Dangerous?"),
        ("how-sediment-impacts-your-water-heater", "How Sediment Can Affect a Heater"),
    ]),
    ("Maintenance", [
        ("how-to-clean-sediment", "Cleaning Sediment"),
        ("how-to-flush-your-water-heater", "Water Heater Flushing"),
        ("how-often-should-you-flush-your-water-heater", "How Often to Consider Flushing"),
        ("annual-maintenance-checklist-for-your-water-heater", "Maintenance Checklist"),
    ]),
    ("Hard Water", [
        ("hard-water-vs-soft-water", "Hard Water vs. Soft Water"),
        ("hard-water-and-your-water-heater", "Hard Water and Your Heater"),
        ("how-to-test-your-water-for-hardness-at-home", "Water Hardness Testing"),
        ("common-myths-about-water-heaters-and-hard-water", "Common Hard-Water Myths"),
    ]),
    ("Heater Types", [
        ("tank-vs-tankless-water-heaters", "Tank vs. Tankless"),
        ("electric-vs-gas-water-heaters", "Electric vs. Gas"),
        ("solar-water-heaters-hard-water", "Solar Water Heaters"),
        ("how-to-flush-a-tankless-water-heater", "Tankless Maintenance Context"),
    ]),
]

featured_html = "\n".join(
    f'<div class="feat-card"><h3><a href="/{slug}/">{title}</a></h3><p>{excerpt}</p><a class="read-more" href="/{slug}/">Read guide →</a></div>'
    for slug, title, excerpt in FEATURED
)
category_html = "\n".join(
    '<div class="cat-section"><h3>'+title+'</h3><ul class="cat-list">'+
    ''.join(f'<li><a href="/{slug}/">{label}</a></li>' for slug, label in links)+
    '</ul></div>' for title, links in CATEGORIES
)

html = f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Tank Sediment | Water Heater Sediment Guides</title>
<meta name="description" content="Practical information about water heater sediment, hard water, maintenance questions, and when professional help may make sense.">
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}body{{font-family:Georgia,serif;color:#222;background:#fff;line-height:1.75}}a{{color:#1a6fa8;text-decoration:none}}a:hover{{text-decoration:underline}}header{{background:#1a3a4a;padding:1rem 2rem;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:1rem}}.site-title a{{color:#fff;font-size:1.4rem;font-weight:bold}}nav a{{color:#cde;font-size:.9rem;margin-left:1.2rem}}.phone-cta{{color:#fff;font-weight:bold;background:rgba(255,255,255,.12);padding:.35rem .85rem;border-radius:3px;white-space:nowrap}}.hero{{background:#1a3a4a;color:#fff;padding:4rem 2rem;text-align:center}}.hero h1{{font-size:2.2rem;line-height:1.3;max-width:760px;margin:0 auto 1rem}}.hero p{{color:#cde;max-width:760px;margin:0 auto 1.5rem}}.cta-phone{{display:inline-block;background:#fff;color:#1a3a4a;font-weight:bold;padding:.75rem 1.4rem;border-radius:4px}}.intro,.featured,.service-note{{max-width:960px;margin:0 auto;padding:2rem 1.5rem}}.intro,.service-note{{max-width:820px}}.intro p,.service-note p{{margin-bottom:1rem;color:#444}}.notice{{background:#f0f8ff;padding:1rem 1.25rem;border-left:4px solid #1a6fa8;border-radius:0 6px 6px 0}}.featured h2,.categories h2,.service-note h2{{color:#1a3a4a;margin-bottom:1.2rem}}.feat-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:1.2rem}}.feat-card{{border:1px solid #e0eaf2;border-radius:6px;padding:1.2rem;background:#f7fafd}}.feat-card h3{{font-size:1rem;line-height:1.4;margin-bottom:.45rem}}.feat-card p{{font-size:.9rem;color:#666}}.read-more{{font-size:.88rem;font-weight:bold}}.categories{{background:#f7fafd;padding:2.5rem 1.5rem}}.categories-inner{{max-width:960px;margin:auto}}.cat-grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:1.5rem}}.cat-section h3{{font-size:1.05rem;color:#1a3a4a;border-bottom:2px solid #1a6fa8;padding-bottom:.4rem;margin-bottom:.6rem}}.cat-list{{list-style:none}}.cat-list li{{padding:.35rem 0;border-bottom:1px solid #e8e8e8}}.cat-list a{{color:#333;font-size:.94rem}}footer{{background:#111e26;color:#aaa;text-align:center;padding:1.5rem;font-size:.82rem;line-height:2}}footer a{{color:#8ab}}@media(max-width:900px){{.feat-grid{{grid-template-columns:repeat(2,1fr)}}.cat-grid{{grid-template-columns:repeat(2,1fr)}}}}@media(max-width:560px){{header{{padding:.75rem 1rem}}nav a{{margin-left:.6rem;font-size:.82rem}}.hero{{padding:3rem 1rem}}.hero h1{{font-size:1.65rem}}.feat-grid,.cat-grid{{grid-template-columns:1fr}}}}
</style></head><body>
<header><div class="site-title"><a href="/">Tank Sediment</a></div><nav><a href="/">Home</a><a href="/blog/">Blog</a><a href="/contact-us/">Service Help</a><a href="tel:8557554920" class="phone-cta">855-755-4920</a></nav></header>
<section class="hero"><h1>Understand Water Heater Sediment Before You Decide What to Do</h1><p>Plain-language guides about sediment buildup, hard water, maintenance questions, and signs that may be worth discussing with a qualified professional.</p><a href="tel:8557554920" class="cta-phone">Connect with a service provider</a></section>
<section class="intro"><p>Minerals and other material can settle inside tank-style water heaters over time. How much accumulates, how quickly it happens, and whether it is affecting a particular heater depend on local water chemistry, heater design, usage, age, and maintenance history.</p><p>Tank Sediment is an informational site. We do not inspect your heater and we cannot determine its internal condition from a webpage.</p><p class="notice"><strong>Maintenance context tool:</strong> Use the <a href="/calculator/"><strong>Water Heater Maintenance Context Tool</strong></a> to organize what you know about heater age, last service, and water hardness. It does not estimate a physical amount of sediment inside the tank.</p></section>
<section class="featured"><h2>Start Here</h2><div class="feat-grid">{featured_html}</div></section>
<section class="categories"><div class="categories-inner"><h2>Browse by Topic</h2><div class="cat-grid">{category_html}</div></div></section>
<section class="service-note"><h2>Need Service Help?</h2><p>If you want professional help, the phone number on this site may connect you with an independent third-party service provider or service network. Tank Sediment is not the plumbing company performing the work.</p><p>Before authorizing work, confirm the provider's identity, scope, pricing, licensing where applicable, and any warranty terms directly with that provider.</p></section>
<footer>&copy; Tank Sediment — <a href="/affiliate-disclosure/">Affiliate Disclosure</a> · <a href="/privacy-policy/">Privacy Policy</a> · <a href="/disclaimer/">Disclaimer</a> · <a href="/terms-and-conditions/">Terms &amp; Conditions</a> · <a href="/contact-us/">Service Help</a></footer>
</body></html>'''

Path('static_site/index.html').write_text(html, encoding='utf-8')
print('Done - safety-framed homepage rebuilt')
