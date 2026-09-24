"""Validate authored English counterparts without contacting affiliate destinations."""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.lang = None
        self.alternates = {}
        self.affiliates = []
        self.media = []
        self.headings = 0
        self.feed(path.read_text(encoding="utf-8"))

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "html":
            self.lang = attrs.get("lang")
        if tag == "link" and attrs.get("rel") == "alternate":
            self.alternates[attrs.get("hreflang")] = attrs.get("href", "")
        if tag == "a" and "sponsored" in attrs.get("rel", "").split():
            self.affiliates.append(attrs.get("href"))
        if tag in ("img", "source") and attrs.get("src"):
            self.media.append(attrs["src"])
        if tag == "h2":
            self.headings += 1


errors = []
pages = sorted((ROOT / "en/articles").glob("*/index.html"))
for path in pages:
    page = Page(path)
    slug = path.parent.name
    japanese_path = ROOT / "articles" / slug / "index.html"
    if not japanese_path.exists():
        errors.append(f"{slug}: missing Japanese original")
        continue
    japanese = Page(japanese_path)
    if page.lang != "en" or not page.headings:
        errors.append(f"{slug}: missing English language or body headings")
    for lang, expected in (("ja", f"/articles/{slug}/"), ("en", f"/en/articles/{slug}/")):
        for label, candidate in (("English", page), ("Japanese", japanese)):
            if urlparse(candidate.alternates.get(lang, "")).path != expected:
                errors.append(f"{slug}: {label} counterpart missing {lang} link")
    if Counter(page.affiliates) != Counter(japanese.affiliates):
        errors.append(f"{slug}: affiliate destinations differ")
    for src in page.media:
        parsed = urlparse(src)
        if parsed.scheme or parsed.netloc:
            continue
        target = ROOT / unquote(parsed.path.lstrip("/")) if src.startswith("/") else path.parent / unquote(parsed.path)
        if not target.is_file():
            errors.append(f"{slug}: missing local media {src}")
    if "translate.google.com" in path.read_text(encoding="utf-8"):
        errors.append(f"{slug}: runtime translation URL remains")

if errors:
    raise SystemExit("\n".join(errors))
print(f"Authored English counterparts verified: {len(pages)} pages")
