import os, re

LINK_SENTENCE_HARD = '<p>For a full breakdown of how hard water damages your water heater over time, see: <a href="/hard-water-water-heater-damage/">hard water water heater damage</a>.</p>'
LINK_SENTENCE_ANODE = '<p>Learn how the anode rod connects to sediment and rust buildup: <a href="/water-heater-anode-rod-sediment/">water heater anode rod and sediment</a>.</p>'

HARD_URL = "/hard-water-water-heater-damage/"
ANODE_URL = "/water-heater-anode-rod-sediment/"

# WP-extracted articles (use post-content pattern)
HARD_WATER_TARGETS = [
    "hard-water-vs-soft-water",
    "hard-water-and-your-water-heater",
    "how-water-softeners-can-prevent-sediment-buildup",
    "how-hard-water-impacts-your-energy-bills",
    "the-link-between-hard-water-and-plumbing-repairs",
    "how-to-test-your-water-for-hardness-at-home",
    "what-causes-sediment-buildup-in-water-heaters",
    "the-science-behind-sediment-buildup",
]

ANODE_TARGETS = [
    "how-to-flush-your-water-heater",
    "annual-maintenance-checklist-for-your-water-heater",
    "how-to-clean-sediment",
    "keeping-your-water-heater-clear",
    "is-sediment-buildup-dangerous",
    "5-signs-your-water-heater-has-sediment-buildup",
    "how-sediment-impacts-your-water-heater",
]

# Pillar pages (use .related div pattern)
HARD_PILLAR_TARGETS = [
    "sediment-buildup-in-water-heater",
    "flush-water-heater-sediment",
    "water-heater-sediment-removal",
    "water-heater-anode-rod-sediment",
]

ANODE_PILLAR_TARGETS = [
    "sediment-buildup-in-water-heater",
    "flush-water-heater-sediment",
    "water-heater-sediment-removal",
    "hard-water-water-heater-damage",
]

updated = 0

def inject_post_content(slug, url, sentence):
    global updated
    path = os.path.join("static_site", slug, "index.html")
    if not os.path.exists(path):
        print(f"  SKIP (not found): {slug}")
        return
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if url in content:
        print(f"  SKIP (already linked): {slug}")
        return
    new_content = re.sub(
        r'(</div>\s*</div>\s*<footer)',
        sentence + r'\n  \1',
        content, count=1
    )
    if new_content != content:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"  Linked: {slug}")
        updated += 1
    else:
        print(f"  SKIP (pattern not matched): {slug}")

def inject_pillar(slug, url, sentence):
    global updated
    path = os.path.join("static_site", slug, "index.html")
    if not os.path.exists(path):
        print(f"  SKIP (not found): {slug}")
        return
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if url in content:
        print(f"  SKIP (already linked): {slug}")
        return
    new_content = content.replace(
        '<div class="related">',
        sentence + '\n\n    <div class="related">',
        1
    )
    if new_content != content:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"  Linked (pillar): {slug}")
        updated += 1
    else:
        print(f"  SKIP (related div not found): {slug}")

print("=== Hard Water Damage links ===")
for slug in HARD_WATER_TARGETS:
    inject_post_content(slug, HARD_URL, LINK_SENTENCE_HARD)
for slug in HARD_PILLAR_TARGETS:
    inject_pillar(slug, HARD_URL, LINK_SENTENCE_HARD)

print("\n=== Anode Rod Sediment links ===")
for slug in ANODE_TARGETS:
    inject_post_content(slug, ANODE_URL, LINK_SENTENCE_ANODE)
for slug in ANODE_PILLAR_TARGETS:
    inject_pillar(slug, ANODE_URL, LINK_SENTENCE_ANODE)

print(f"\nDone. {updated} pages updated.")
