import os, re

PILLAR_URL = "/water-heater-sediment-removal/"
LINK_SENTENCE = '<p>For a complete overview of all removal methods and costs, see our guide on <a href="/water-heater-sediment-removal/">water heater sediment removal</a>.</p>'

# Pages that use the standard post-content div (WP-extracted articles)
POST_CONTENT_TARGETS = [
    "how-to-clean-sediment",
    "how-to-flush-your-water-heater",
    "5-signs-your-water-heater-has-sediment-buildup",
    "is-sediment-buildup-dangerous",
    "how-sediment-impacts-your-water-heater",
    "the-science-behind-sediment-buildup",
    "annual-maintenance-checklist-for-your-water-heater",
    "keeping-your-water-heater-clear",
    "what-causes-sediment-buildup-in-water-heaters",
]

# Pillar pages — inject before the .related div
PILLAR_TARGETS = [
    "sediment-buildup-in-water-heater",
    "flush-water-heater-sediment",
]

updated = 0

for slug in POST_CONTENT_TARGETS:
    path = os.path.join("static_site", slug, "index.html")
    if not os.path.exists(path):
        print(f"  SKIP (not found): {slug}")
        continue
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if PILLAR_URL in content:
        print(f"  SKIP (already linked): {slug}")
        continue
    # Inject sentence just before closing </div> of post-content
    new_content = re.sub(
        r'(</div>\s*</div>\s*<footer)',
        LINK_SENTENCE + r'\n  \1',
        content, count=1
    )
    if new_content != content:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"  Linked: {slug}")
        updated += 1
    else:
        print(f"  SKIP (pattern not matched): {slug}")

for slug in PILLAR_TARGETS:
    path = os.path.join("static_site", slug, "index.html")
    if not os.path.exists(path):
        print(f"  SKIP (not found): {slug}")
        continue
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if PILLAR_URL in content:
        print(f"  SKIP (already linked): {slug}")
        continue
    # Inject before the related div
    new_content = content.replace(
        '<div class="related">',
        LINK_SENTENCE + '\n\n    <div class="related">',
        1
    )
    if new_content != content:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"  Linked (pillar): {slug}")
        updated += 1
    else:
        print(f"  SKIP (related div not found): {slug}")

print(f"\nDone. {updated} pages updated with removal pillar link.")
