"""Publish the approved bilingual radio collaboration article without changing its prose."""
from pathlib import Path
import html
import json
import re
import shutil


ROOT = Path(__file__).resolve().parents[1]
DRAFT = Path(r"E:\Documents\Codex\2026-08-01\robuse-selection-drafts\Draft\2026-11-11\2026-11-11-01-robu-kininaru-radio-next-gen-broadcast-v1")
SLUG = "radio-five-stations-next-generation-broadcast-system"
DATE = "2026-11-12"
BASE = "https://www.axis-jp.net"
IMAGES = [
    "radio-master-control-collaboration-editorial-v1.png",
    "radio-family-listening-resilience-editorial-v1.png",
]
SOURCES = [
    "https://www.tfm.co.jp/company/about/ir/news/103862",
    "https://newsdig.tbs.co.jp/articles/-/3073268?display=1",
    "https://www.joqr.co.jp/",
    "https://www.sony.jp/radio/products/ICF-B09/",
]


def write_utf8(path: Path, value: str) -> None:
    with path.open("w", encoding="utf-8", newline="\r\n") as handle:
        handle.write(value)


def frontmatter(path: Path) -> dict[str, str]:
    raw = path.read_text(encoding="utf-8-sig")
    block = re.search(r"\A---\s*\n(.*?)\n---", raw, re.S)[1]
    values = {}
    for key in ("title", "description"):
        values[key] = re.search(rf'^{key}:\s*"(.*)"$', block, re.M)[1]
    seo_title = re.search(r'^seoTitle:\s*"(.*)"$', block, re.M)
    values["seoTitle"] = seo_title[1] if seo_title else values["title"]
    return values


def article_content(lang: str) -> str:
    name = "article-local-preview.html" if lang == "ja" else "article-local-preview-en.html"
    raw = (DRAFT / name).read_text(encoding="utf-8")
    content = re.search(r'<div class="article-content">(.*?)</div></article>', raw, re.S)[1]
    for filename in IMAGES:
        content = content.replace(f'./{filename}', f'/assets/images/articles/{SLUG}/{filename}?v=20261112')
    content = content.replace('<section class="purchase-panel">', '<section class="purchase-panel" id="purchase">')
    content = re.sub(
        r'<a class="purchase-button ([^"]+)" rel="nofollow sponsored" href="([^"]+)">',
        r'<a class="purchase-button \1" href="\2" target="_blank" rel="nofollow sponsored noopener noreferrer">',
        content,
    )
    return content


def page(lang: str) -> str:
    prefix = "" if lang == "ja" else "en/"
    meta = frontmatter(DRAFT / ("article.md" if lang == "ja" else "article-en.md"))
    url = f"{BASE}/{prefix}articles/{SLUG}/"
    hero = f"{BASE}/assets/images/articles/{SLUG}/{IMAGES[0]}?v=20261112"
    locale = "ja_JP" if lang == "ja" else "en_US"
    category = "ろぶーの気になる事 / メディア・放送" if lang == "ja" else "Robu's Curiosities / Media & Broadcasting"
    disclosure = ("※記事内にはAI生成の編集画像とアフィリエイトリンクを含みます。" if lang == "ja"
                  else "This article includes AI-generated editorial images and affiliate links.")
    schema = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": meta["title"],
        "description": meta["description"],
        "datePublished": DATE,
        "dateModified": DATE,
        "inLanguage": lang,
        "mainEntityOfPage": url,
        "image": [f"{BASE}/assets/images/articles/{SLUG}/{name}" for name in IMAGES],
        "isAccessibleForFree": True,
        "author": {"@type": "Person", "name": "ろぶー"},
        "publisher": {"@type": "Organization", "name": "ろぶーの気になる事", "url": BASE},
        "citation": SOURCES,
    }
    return f'''<!doctype html><html lang="{lang}" translate="no"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="google" content="notranslate"><meta name="robots" content="index,follow,max-image-preview:large"><meta name="referrer" content="strict-origin-when-cross-origin"><meta name="social:publish" content="true"><meta name="social:ai-image" content="true"><meta name="social:disclosure" content="{html.escape(disclosure, quote=True)}">
<title>{html.escape(meta['seoTitle'])}</title><meta name="description" content="{html.escape(meta['description'], quote=True)}"><link rel="canonical" href="{url}"><link rel="alternate" hreflang="ja" href="{BASE}/articles/{SLUG}/"><link rel="alternate" hreflang="en" href="{BASE}/en/articles/{SLUG}/"><link rel="alternate" hreflang="x-default" href="{BASE}/articles/{SLUG}/">
<meta property="og:type" content="article"><meta property="og:locale" content="{locale}"><meta property="og:site_name" content="ろぶーの気になる事"><meta property="og:title" content="{html.escape(meta['title'], quote=True)}"><meta property="og:description" content="{html.escape(meta['description'], quote=True)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{hero}"><meta property="og:image:alt" content="{html.escape(meta['title'], quote=True)}"><meta property="article:section" content="{html.escape(category, quote=True)}"><meta property="article:published_time" content="{DATE}T00:00:00+09:00"><meta property="article:modified_time" content="{DATE}T00:00:00+09:00"><meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="/assets/css/contact-feedback-ees-standard.css?v=3" data-contact-feedback-style><link rel="stylesheet" href="/assets/css/draft-article-preview.css?v=20260930-publish-five-1"><style>.robu-article-layout>main.draft-main{{max-width:820px}}article{{overflow-wrap:anywhere}}.article-content img{{display:block;max-width:100%;width:auto;height:auto;margin:auto;border-radius:10px}}.article-content>p>em{{display:block;font-size:.9rem;line-height:1.7}}.purchase-panel{{background:transparent!important;box-shadow:none!important;border:1px solid #d8cfbf;border-radius:16px;padding:22px;margin:36px 0}}.purchase-panel h2{{font-size:min(22px,1.45rem)}}.purchase-buttons{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}}.purchase-button{{display:flex;align-items:center;justify-content:center;min-height:52px;padding:12px 14px;border-radius:10px;text-align:center;font-weight:800;text-decoration:none}}.purchase-button.amazon{{background:#ff9900;color:#111}}.purchase-button.rakuten{{background:#bf0000;color:#fff}}.purchase-button.yahoo{{background:#6f2dbd;color:#fff}}.purchase-button:hover,.purchase-button:focus-visible{{filter:brightness(.92);outline:3px solid #1e6bb8;outline-offset:2px}}.purchase-note,.disclosure{{font-size:.9rem;line-height:1.7}}@media(max-width:760px){{.purchase-buttons{{grid-template-columns:1fr}}}}</style><script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script><script defer src="/assets/js/shared-shell.js?v=20261016-browser-language-1"></script></head><body class="draft-preview robu-published-article"><main class="draft-main" data-contact-page><article><div class="selection-subcategory" data-article-category>{html.escape(category)}</div><div class="article-content">{article_content(lang)}</div></article></main><script src="/assets/js/contact-feedback.js?v=20260907-1"></script></body></html>'''


metadata = {lang: frontmatter(DRAFT / ("article.md" if lang == "ja" else "article-en.md")) for lang in ("ja", "en")}
for lang in ("ja", "en"):
    prefix = Path() if lang == "ja" else Path("en")
    target = ROOT / prefix / "articles" / SLUG / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    write_utf8(target, page(lang))

image_dir = ROOT / "assets" / "images" / "articles" / SLUG
image_dir.mkdir(parents=True, exist_ok=True)
for filename in IMAGES:
    shutil.copy2(DRAFT / filename, image_dir / filename)

article_id = f"{SLUG}-{DATE}"
index = ROOT / "index.html"
text = index.read_text(encoding="utf-8")
if article_id not in text:
    card = {
        "id": article_id,
        "date": DATE,
        "dateLabel": "2026.11.12",
        "category": "ろぶーの気になる事 / メディア・放送",
        "title": metadata["ja"]["title"],
        "digestTitle": "ラジオ5社が「心臓部」の共同化へ",
        "digestLead": "次世代放送システムの構想と、災害時の放送継続、番組づくりへの意味を一次情報で読み解きます。",
        "excerpt": metadata["ja"]["description"],
        "enTitle": metadata["en"]["title"],
        "enExcerpt": metadata["en"]["description"],
        "image": f"assets/images/articles/{SLUG}/{IMAGES[0]}",
        "url": f"/articles/{SLUG}/",
        "imageAlt": "放送局のマスター設備を前に複数の技術者が共同運用を検討するAI生成の編集用イメージ",
    }
    text = text.replace("const articles = [", "const articles = [\n      " + json.dumps(card, ensure_ascii=False, separators=(",", ":")) + ",", 1)
    text = text.replace("const articleFilters = {", f"const articleFilters = {{\n      '{article_id}': [],", 1)
    write_utf8(index, text)

sitemap = ROOT / "sitemap.xml"
text = sitemap.read_text(encoding="utf-8")
if f"{BASE}/articles/{SLUG}/" not in text:
    block = f'''<url><loc>{BASE}/articles/{SLUG}/</loc><lastmod>{DATE}</lastmod><xhtml:link rel="alternate" hreflang="ja" href="{BASE}/articles/{SLUG}/"/><xhtml:link rel="alternate" hreflang="en" href="{BASE}/en/articles/{SLUG}/"/><xhtml:link rel="alternate" hreflang="x-default" href="{BASE}/articles/{SLUG}/"/></url>\n<url><loc>{BASE}/en/articles/{SLUG}/</loc><lastmod>{DATE}</lastmod><xhtml:link rel="alternate" hreflang="ja" href="{BASE}/articles/{SLUG}/"/><xhtml:link rel="alternate" hreflang="en" href="{BASE}/en/articles/{SLUG}/"/><xhtml:link rel="alternate" hreflang="x-default" href="{BASE}/articles/{SLUG}/"/></url>\n'''
    write_utf8(sitemap, text.replace("</urlset>", block + "</urlset>"))

html_sitemap = ROOT / "sitemap" / "index.html"
text = html_sitemap.read_text(encoding="utf-8")
if f"/articles/{SLUG}/" not in text:
    items = (f'<ul><li><a href="/articles/{SLUG}/">{html.escape(metadata["ja"]["title"])}</a></li>'
             f'<li><a href="/en/articles/{SLUG}/">{html.escape(metadata["en"]["title"])}</a></li></ul>')
    text = text.replace("<h2>AI・テクノロジー</h2>", "<h2>AI・テクノロジー</h2>" + items, 1)
    write_utf8(html_sitemap, text)

record = ROOT / "records" / "2026" / "11" / "2026-11-12-radio-five-stations-publication.md"
record.parent.mkdir(parents=True, exist_ok=True)
write_utf8(record, """# ラジオ5社・次世代放送システム記事 公開記録

- 公開承認: 2026-11-12、ユーザーの明示承認
- 分類: ろぶーの気になる事 / メディア・放送
- 日本語・英語: 承認済み最終稿
- 画像: AI生成の編集用画像2枚。実際の設備・会議・災害場面ではない旨を本文中に明記
- アフィリエイト: Sony ICF-B09のAmazon、楽天市場、Yahoo!ショッピング。可視開示と sponsored 属性を設定
- ファクトチェック: TOKYO FM、TBS NEWS DIG、文化放送、ソニーの一次・公式情報4件
- SNS: ユーザーが公開後の投稿を依頼。サイト公開確認後に投稿素材を生成し、実投稿は別途確認する
""")

for generated in (index, sitemap, html_sitemap):
    write_utf8(generated, generated.read_text(encoding="utf-8"))

print("Published radio five-stations production files")
