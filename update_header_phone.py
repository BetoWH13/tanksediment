import os, re

# The phone link to inject into every header nav
PHONE_HTML = '<a href="tel:8557554920" class="phone-cta">&#128222; 855-755-4920</a>'

# CSS to add for the phone button (injected before </style>)
PHONE_CSS = """    .phone-cta { color: #fff; font-weight: bold; font-size: .9rem; background: rgba(255,255,255,.12); padding: .3rem .85rem; border-radius: 3px; white-space: nowrap; }
    .phone-cta:hover { background: rgba(255,255,255,.25); text-decoration: none; }"""

updated = 0
skipped = 0

for root, dirs, files in os.walk('static_site'):
    for f in files:
        if not f.endswith('.html'):
            continue
        path = os.path.join(root, f)
        with open(path, 'r', encoding='utf-8') as fh:
            content = fh.read()

        # Skip if phone already added
        if 'phone-cta' in content:
            skipped += 1
            continue

        # 1. Inject CSS before </style>
        content = content.replace('  </style>', PHONE_CSS + '\n  </style>', 1)

        # 2. Inject phone into nav (append before </nav>)
        content = re.sub(r'(</nav>)', PHONE_HTML + r'\1', content, count=1)

        with open(path, 'w', encoding='utf-8') as fh:
            fh.write(content)
        updated += 1

print(f'Done. Updated: {updated}  Already had phone: {skipped}')
