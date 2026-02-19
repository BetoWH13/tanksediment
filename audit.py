import os, re
from collections import defaultdict

issues = defaultdict(list)

for root, dirs, files in os.walk('static_site'):
    for f in files:
        if f.endswith('.html'):
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8') as fh:
                content = fh.read()
            rel = path.replace('static_site\\', '')

            # &nbsp; spam
            n = content.count('&nbsp;')
            if n > 3:
                issues[rel].append(f'nbsp spam x{n}')

            # Escaped backslash-quotes in content (from SQL parser)
            bq = content.count('\\"')
            if bq > 0:
                issues[rel].append(f'escaped quotes x{bq}')

            # Duplicate H1 (page title repeated inside post-content)
            h1s = re.findall(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL | re.IGNORECASE)
            clean = [re.sub(r'<[^>]+>', '', h).strip() for h in h1s]
            if len(clean) >= 2 and clean[0].lower() in clean[1].lower():
                issues[rel].append(f'duplicate h1: "{clean[0][:50]}"')

            # double-encoded ampersand
            if '&amp;amp;' in content:
                issues[rel].append('double-encoded &amp;amp;')

            # nested empty lists
            if 'list-style-type: none' in content:
                # Show context
                idx = content.find('list-style-type: none')
                issues[rel].append(f'nested empty lists (ctx: {repr(content[max(0,idx-30):idx+60])})')

            # img tags still present
            if '<img' in content:
                issues[rel].append('img tags present')

            # PHP leftovers
            if '<?php' in content:
                issues[rel].append('PHP code present')

print(f"Pages audited: {sum(1 for r,d,fs in os.walk('static_site') for f in fs if f.endswith('.html'))}\n")
if issues:
    for page, probs in sorted(issues.items()):
        print(f"{page}")
        for p in probs:
            print(f"  - {p}")
else:
    print("No issues found!")
