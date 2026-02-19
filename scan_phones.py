import os, re

CANONICAL = "855-755-4920"
CANONICAL_DIGITS = "8557554920"

# Patterns to catch phone numbers in various formats
PHONE_PATTERN = re.compile(
    r'(?<!\w)'                        # not preceded by word char
    r'(\(?\d{3}\)?[\s.\-]?\d{3}[\s.\-]?\d{4})'
    r'(?!\w)',                         # not followed by word char
    re.IGNORECASE
)

found = {}   # page -> list of (phone_string, context)

for root, dirs, files in os.walk('static_site'):
    for f in files:
        if not f.endswith('.html'):
            continue
        path = os.path.join(root, f)
        with open(path, 'r', encoding='utf-8') as fh:
            content = fh.read()

        rel = path.replace('static_site' + os.sep, '')
        matches = PHONE_PATTERN.finditer(content)
        for m in matches:
            number = m.group(1)
            digits = re.sub(r'\D', '', number)
            ctx = content[max(0, m.start()-40):m.end()+40].replace('\n', ' ')
            if digits != CANONICAL_DIGITS:
                found.setdefault(rel, []).append((number, ctx.strip()))

if found:
    print(f"ROGUE PHONE NUMBERS FOUND:\n")
    for page, hits in sorted(found.items()):
        print(f"  {page}")
        for number, ctx in hits:
            print(f"    Number : {number}")
            print(f"    Context: ...{ctx}...")
            print()
else:
    print("All good — no rogue phone numbers found.")

# Also count how many times canonical appears per page
print(f"\n--- Canonical ({CANONICAL}) occurrences per page ---")
for root, dirs, files in os.walk('static_site'):
    for f in files:
        if not f.endswith('.html'):
            continue
        path = os.path.join(root, f)
        with open(path, 'r', encoding='utf-8') as fh:
            content = fh.read()
        rel = path.replace('static_site' + os.sep, '')
        count = len(re.findall(CANONICAL_DIGITS, content))
        if count != 1:
            print(f"  {rel}: {count} occurrences  {'<-- MULTIPLE!' if count > 1 else '<-- MISSING!'}")
