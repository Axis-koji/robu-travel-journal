"""Publish the approved bilingual Re・De Kettle 0.6L article."""
from pathlib import Path
import html
import json
import re
import shutil


ROOT = Path(__file__).resolve().parents[1]
DRAFT = Path(r"E:\Documents\Codex\2026-08-01\robuse-selection-drafts\Draft\2026-10-25\2026-10-25-02-robus-selection-rede-kettle-v3")
SLUG = "rede-kettle-06l-buying-guide"
DATE = "2026-10-27"
BASE = "https://www.axis-jp.net"
IMAGES = [f"rede-kettle-official-{n}.jpg" for n in range(1, 5)]


def frontmatter(path: Path) -> dict[str, str]:
    raw = path.read_text(encoding="utf-8-sig")
    block = re.search(r"\A---\s*\n(.*?)\n---", raw, re.S)[1]
    values = {}
    for key in ("title", "description"):
        values[key] = re.search(rf'^{key}:\s*"(.*)"$', block, re.M)[1]
    return values


def article_content(lang: str) -> str:
    name = "article-local-preview.html" if lang == "ja" else "article-local-preview-en.html"
    raw = (DRAFT / name).read_text(encoding="utf-8")
    content = re.search(r'<div class="article-content">(.*?)</div></article>', raw, re.S)[1]
    for filename in IMAGES:
        content = content.replace(f'./{filename}', f'/assets/images/articles/{SLUG}/{filename}')
    return content


def page(lang: str) -> str:
    prefix = "" if lang == "ja" else "en/"
    meta = frontmatter(DRAFT / ("article.md" if lang == "ja" else "article-en.md"))
    url = f"{BASE}/{prefix}articles/{SLUG}/"
    hero = f"{BASE}/assets/images/articles/{SLUG}/{IMAGES[0]}"
    locale = "ja_JP" if lang == "ja" else "en_US"
    category = "Robu's Selection / 家電" if lang == "ja" else "Robu's Selection / Home Appliances"
    sources = [
        "https://pixela-group.jp/press/2026/20261023.html",
        "https://re-de.jp/kettle/",
        "https://re-de.shop/items/6ac49cbbca94ae590f4e23a2",
        "https://re-de.jp/support/kettle/",
        "https://re-de.jp/support/kettle/rd-ek02a-06_manual.pdf",
    ]
    schema = {
        "@context": "https://schema.org", "@type": "BlogPosting",
        "headline": meta["title"], "description": meta["description"],
        "datePublished": DATE, "dateModified": DATE, "inLanguage": lang,
        "mainEntityOfPage": url, "image": [hero],
        "author": {"@type": "Person", "name": "ろぶー"},
        "publisher": {"@type": "Organization", "name": "ろぶーの気になる事", "url": BASE},
        "citation": sources,
    }
    return f'''<!doctype html><html lang="{lang}" translate="no"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="google" content="notranslate"><meta name="robots" content="index,follow,max-image-preview:large"><meta name="referrer" content="strict-origin-when-cross-origin"><meta name="social:publish" content="false"><meta name="social:ai-image" content="false"><meta name="social:disclosure" content="This article uses official press images and contains affiliate links. Social posting is scheduled separately.">
<title>{html.escape(meta['title'])}</title><meta name="description" content="{html.escape(meta['description'], quote=True)}"><link rel="canonical" href="{url}"><link rel="alternate" hreflang="ja" href="{BASE}/articles/{SLUG}/"><link rel="alternate" hreflang="en" href="{BASE}/en/articles/{SLUG}/"><link rel="alternate" hreflang="x-default" href="{BASE}/articles/{SLUG}/">
<meta property="og:type" content="article"><meta property="og:locale" content="{locale}"><meta property="og:site_name" content="ろぶーの気になる事"><meta property="og:title" content="{html.escape(meta['title'], quote=True)}"><meta property="og:description" content="{html.escape(meta['description'], quote=True)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{hero}"><meta property="og:image:alt" content="{html.escape(meta['title'], quote=True)}"><meta property="article:section" content="{html.escape(category, quote=True)}"><meta property="article:published_time" content="{DATE}T00:00:00+09:00"><meta property="article:modified_time" content="{DATE}T00:00:00+09:00"><meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="/assets/css/contact-feedback-ees-standard.css?v=3" data-contact-feedback-style><link rel="stylesheet" href="/assets/css/draft-article-preview.css?v=20260930-publish-five-1"><link rel="stylesheet" href="/assets/css/robus-selection-theme.css?v=20261025-standard-5" data-robu-selection-theme><style>.robu-article-layout>main.draft-main{{max-width:820px}}article{{overflow-wrap:anywhere}}.article-content img{{display:block;max-width:100%;width:auto;height:auto;margin:auto;border-radius:10px}}.article-content>p>em{{display:block;font-size:.9rem;line-height:1.7}}.purchase-panel{{background:transparent!important;box-shadow:none!important;border:1px solid #d8cfbf;border-radius:16px;padding:22px;margin:36px 0}}.purchase-buttons{{display:grid;gap:12px}}.purchase-button{{display:block;padding:14px 16px;border-radius:10px;text-align:center;font-weight:800;text-decoration:none}}.purchase-button.amazon{{background:#ff9900;color:#111}}.purchase-button.rakuten{{background:#bf0000;color:#fff}}.purchase-button.yahoo{{background:#ff0033;color:#fff}}.purchase-note,.disclosure{{font-size:.9rem;line-height:1.7}}</style><script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script><script defer src="/assets/js/shared-shell.js?v=20261016-browser-language-1"></script></head><body class="draft-preview selection-preview robus-selection-page robu-published-article"><main class="draft-main" data-contact-page><article><div class="robu-selection-label">Robu's Selection</div><div class="selection-subcategory" data-article-category>{html.escape(category)}</div><div class="article-content">{article_content(lang)}</div></article></main><script src="/assets/js/contact-feedback.js?v=20260907-1"></script></body></html>'''


metadata = {lang: frontmatter(DRAFT / ("article.md" if lang == "ja" else "article-en.md")) for lang in ("ja", "en")}
for lang in ("ja", "en"):
    prefix = Path() if lang == "ja" else Path("en")
    target = ROOT / prefix / "articles" / SLUG / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(page(lang), encoding="utf-8")

image_dir = ROOT / "assets" / "images" / "articles" / SLUG
image_dir.mkdir(parents=True, exist_ok=True)
for filename in IMAGES:
    shutil.copy2(DRAFT / filename, image_dir / filename)

article_id = f"{SLUG}-{DATE}"
index = ROOT / "index.html"
text = index.read_text(encoding="utf-8")
if article_id not in text:
    card = {
        "id": article_id, "date": DATE, "dateLabel": "2026.10.27",
        "category": "Robu's Selection / 家電", "title": metadata["ja"]["title"],
        "digestTitle": "機能から生まれた、美しいケトル",
        "digestLead": "二重構造、注ぎやすいノズル、8段階温度設定を公式写真で紹介します。",
        "excerpt": metadata["ja"]["description"], "enTitle": metadata["en"]["title"],
        "enExcerpt": metadata["en"]["description"],
        "image": f"assets/images/articles/{SLUG}/{IMAGES[0]}", "url": f"/articles/{SLUG}/",
        "imageAlt": "Re・De Kettle 0.6Lの3色を並べた公式メインビジュアル",
    }
    text = text.replace("const articles = [", "const articles = [\n      " + json.dumps(card, ensure_ascii=False, separators=(",", ":")) + ",", 1)
    text = text.replace("const articleFilters = {", f"const articleFilters = {{\n      '{article_id}': ['selection','appliance'],", 1)
    index.write_text(text, encoding="utf-8")

sitemap = ROOT / "sitemap.xml"
text = sitemap.read_text(encoding="utf-8")
if f"{BASE}/articles/{SLUG}/" not in text:
    block = f'''<url><loc>{BASE}/articles/{SLUG}/</loc><lastmod>{DATE}</lastmod><xhtml:link rel="alternate" hreflang="ja" href="{BASE}/articles/{SLUG}/"/><xhtml:link rel="alternate" hreflang="en" href="{BASE}/en/articles/{SLUG}/"/><xhtml:link rel="alternate" hreflang="x-default" href="{BASE}/articles/{SLUG}/"/></url>\n<url><loc>{BASE}/en/articles/{SLUG}/</loc><lastmod>{DATE}</lastmod><xhtml:link rel="alternate" hreflang="ja" href="{BASE}/articles/{SLUG}/"/><xhtml:link rel="alternate" hreflang="en" href="{BASE}/en/articles/{SLUG}/"/><xhtml:link rel="alternate" hreflang="x-default" href="{BASE}/articles/{SLUG}/"/></url>\n'''
    text = text.replace("</urlset>", block + "</urlset>")
    sitemap.write_text(text, encoding="utf-8")

html_sitemap = ROOT / "sitemap" / "index.html"
text = html_sitemap.read_text(encoding="utf-8")
if f"/articles/{SLUG}/" not in text:
    items = (f'<ul><li><a href="/articles/{SLUG}/">{html.escape(metadata["ja"]["title"])}</a></li>'
             f'<li><a href="/en/articles/{SLUG}/">{html.escape(metadata["en"]["title"])}</a></li></ul>')
    text = text.replace("<h2>Robu's Selection</h2>", "<h2>Robu's Selection</h2>" + items, 1)
    html_sitemap.write_text(text, encoding="utf-8")

record = ROOT / "records" / "2026" / "10" / "2026-10-27-rede-kettle-publication.md"
record.parent.mkdir(parents=True, exist_ok=True)
record.write_text("""# Re・De Kettle 0.6L記事 公開記録

- 公開承認: 2026-10-27、ユーザーの明示承認
- 分類: Robu's Selection / 家電
- 日本語・英語: 購入者目線の承認済み最終稿
- 画像: A-Stage／PIXELA Group公式プレス素材4枚、出典明記
- アフィリエイト: Amazon、楽天市場、Yahoo!ショッピングの検索導線
- SNS: 公開後、朝7時30分の予約投稿を別途設定
- ファクトチェック: 公式発表、製品ページ、公式ストア、FAQ、取扱説明書
""", encoding="utf-8")

print("Published Re・De Kettle production files")
