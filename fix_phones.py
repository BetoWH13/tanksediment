import os, re

ROGUE = "607-610-3115"
CANONICAL = "855-755-4920"

fixed_pages = []

for root, dirs, files in os.walk('static_site'):
    for f in files:
        if not f.endswith('.html'):
            continue
        path = os.path.join(root, f)
        with open(path, 'r', encoding='utf-8') as fh:
            content = fh.read()

        if ROGUE in content:
            new_content = content.replace(ROGUE, CANONICAL)
            with open(path, 'w', encoding='utf-8') as fh:
                fh.write(new_content)
            count = content.count(ROGUE)
            rel = path.replace('static_site' + os.sep, '')
            fixed_pages.append((rel, count))
            print(f"  Fixed {count}x in: {rel}")

if fixed_pages:
    print(f"\nTotal pages fixed: {len(fixed_pages)}")
else:
    print("Nothing to fix.")
