import os, re

PILLAR_URL = "/flush-water-heater-sediment/"

# Pages to inject a link into, phrase to link, replacement text
TARGETS = {
    "how-to-flush-your-water-heater":           ("flush", "flush water heater sediment"),
    "how-to-flush-a-tankless-water-heater":     ("flush", "flush water heater sediment"),
    "how-often-should-you-flush-your-water-heater": ("flush", "flush water heater sediment"),
    "how-to-clean-sediment":                    ("flush", "flush water heater sediment"),
    "annual-maintenance-checklist-for-your-water-heater": ("flush", "flush water heater sediment"),
    "keeping-your-water-heater-clear":          ("flush", "flush water heater sediment"),
    "5-signs-your-water-heater-has-sediment-buildup": ("flush", "flush water heater sediment"),
    "is-sediment-buildup-dangerous":            ("flush", "flush water heater sediment"),
}

updated = 0

for slug, (phrase, anchor_text) in TARGETS.items():
    path = os.path.join("static_site", slug, "index.html")
    if not os.path.exists(path):
        print(f"  SKIP (not found): {slug}")
        continue

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    if PILLAR_URL in content:
        print(f"  SKIP (already linked): {slug}")
        continue

    # Find first occurrence of phrase inside post-content, replace with linked version
    post_match = re.search(r'(<div class=[\'"]post-content[\'"]>)(.*?)(</div>\s*</div>\s*<footer)', content, re.DOTALL)
    if not post_match:
        print(f"  SKIP (no post-content): {slug}")
        continue

    post_section = post_match.group(2)
    new_section, count = re.subn(
        re.escape(phrase),
        f'<a href="{PILLAR_URL}">{anchor_text}</a>',
        post_section,
        count=1,
        flags=re.IGNORECASE
    )

    if count == 0:
        print(f"  SKIP (phrase not found): {slug}")
        continue

    new_content = content[:post_match.start(2)] + new_section + content[post_match.end(2):]
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"  Linked: {slug}")
    updated += 1

print(f"\nDone. {updated} pages updated with flush pillar link.")
