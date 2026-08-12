"""Tank Sediment homepage safeguard.

The curated homepage is maintained directly at static_site/index.html.
Do not regenerate it from legacy content or templates: that could reintroduce
older claims or undo the current symptom-first service funnel.

This script intentionally verifies that the committed homepage exists and
leaves it unchanged.
"""
from pathlib import Path

homepage = Path("static_site/index.html")
if not homepage.is_file():
    raise SystemExit(
        "static_site/index.html is missing. Restore the curated homepage from version control; "
        "do not synthesize it from legacy source data."
    )

text = homepage.read_text(encoding="utf-8")
required = [
    "Start with your symptom",
    "tel:8557554920",
    "/water-heater-sediment-removal/",
    "/how-to-flush-a-tankless-water-heater/",
    "/how-to-test-your-water-for-hardness-at-home/",
    "/contact-us/",
]
missing = [item for item in required if item not in text]
if missing:
    raise SystemExit(f"Homepage safeguard failed; expected funnel markers are missing: {missing}")

print("Homepage verified; curated static_site/index.html left unchanged.")
