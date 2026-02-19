import os, re

NEW_FOOTER = '''  <footer>
    &copy; Tank Sediment &mdash;
    <a href="/affiliate-disclosure/">Affiliate Disclosure</a> &middot;
    <a href="/privacy-policy/">Privacy Policy</a> &middot;
    <a href="/disclaimer/">Disclaimer</a> &middot;
    <a href="/terms-and-conditions/">Terms &amp; Conditions</a> &middot;
    <a href="/contact-us/">Contact Us</a>
  </footer>'''

updated = 0
skipped = 0

for root, dirs, files in os.walk('static_site'):
    for f in files:
        if not f.endswith('.html'):
            continue
        path = os.path.join(root, f)
        with open(path, 'r', encoding='utf-8') as fh:
            content = fh.read()

        # Replace anything between <footer> and </footer>
        new_content = re.sub(
            r'<footer>.*?</footer>',
            NEW_FOOTER,
            content,
            flags=re.DOTALL
        )

        if new_content != content:
            with open(path, 'w', encoding='utf-8') as fh:
                fh.write(new_content)
            print(f'  Updated: {path.replace("static_site" + os.sep, "")}')
            updated += 1
        else:
            skipped += 1

print(f'\nDone. Updated: {updated}  Skipped (no footer found): {skipped}')
