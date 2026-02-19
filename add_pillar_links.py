import os, re

PILLAR_URL = "/sediment-buildup-in-water-heater/"
PILLAR_ANCHOR = '<a href="/sediment-buildup-in-water-heater/">sediment buildup in water heaters</a>'

# Pages to inject a link into, and what phrase to link (first occurrence only)
TARGETS = {
    "5-signs-your-water-heater-has-sediment-buildup": "sediment buildup",
    "is-sediment-buildup-dangerous": "sediment buildup",
    "how-sediment-impacts-your-water-heater": "sediment buildup",
    "the-science-behind-sediment-buildup": "sediment buildup",
    "how-to-clean-sediment": "sediment buildup",
    "how-to-flush-your-water-heater": "sediment buildup",
    "how-often-should-you-flush-your-water-heater": "sediment buildup",
    "keeping-your-water-heater-clear": "sediment buildup",
    "how-water-softeners-can-prevent-sediment-buildup": "sediment buildup",
    "annual-maintenance-checklist-for-your-water-heater": "sediment buildup",
}

updated = 0

for slug, phrase in TARGETS.items():
    path = os.path.join("static_site", slug, "index.html")
    if not os.path.exists(path):
        print(f"  SKIP (not found): {slug}")
        continue

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Skip if pillar link already present
    if PILLAR_URL in content:
        print(f"  SKIP (already linked): {slug}")
        continue

    # Find first occurrence of phrase inside post-content div, replace with linked version
    # Only replace inside the post-content section, not in nav/footer
    post_content_match = re.search(r'<div class=[\'"]post-content[\'"]>(.*?)</div>\s*</div>\s*<footer', content, re.DOTALL)
    if not post_content_match:
        print(f"  SKIP (no post-content found): {slug}")
        continue

    post_section = post_content_match.group(1)
    # Replace first occurrence of phrase (case-insensitive) with linked version
    new_section, count = re.subn(
        re.escape(phrase),
        f'<a href="{PILLAR_URL}">{phrase}</a>',
        post_section,
        count=1,
        flags=re.IGNORECASE
    )

    if count == 0:
        print(f"  SKIP (phrase not found in content): {slug}")
        continue

    new_content = content[:post_content_match.start(1)] + new_section + content[post_content_match.end(1):]

    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"  Linked: {slug}")
    updated += 1

print(f"\nDone. {updated} pages updated with pillar link.")
