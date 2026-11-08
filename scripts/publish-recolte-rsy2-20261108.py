"""Publish the approved bilingual recolte RSY-2 article without changing its prose."""
from pathlib import Path
import html
import json
import re
import shutil


ROOT = Path(__file__).resolve().parents[1]
DRAFT = Path(r"E:\Documents\Codex\2026-08-01\robuse-selection-drafts\Draft\2026-11-08\2026-11-08-extra-robu-kininaru-recolte-rsy2-v1")
SLUG = "recolte-auto-cooking-pot-rsy2"
DATE = "2026-11-08"
BASE = "https://www.axis-jp.net"
IMAGES = [
    "recolte-rsy2-evening-kitchen-editorial-v2.png",
    "recolte-rsy2-morning-kitchen-editorial-v4.png",
]
SOURCES = [
    "https://recolte-jp.com/products/auto-cooking-pot/",
    "https://recolte-jp.com/company/",
    "https://recolte-jp.com/rsy-2_lp/",
    "https://recolte-jp.com/admin/wp-content/uploads/2023/02/RSY-2_manual_8.pdf",
    "https://recolte-jp.com/products/rsy-3/",
    "https://ranking.rakuten.co.jp/realtime/208478/",
    "https://shopping.yahoo.co.jp/product/j/4582180200990/compare.html",
]


def frontmatter(path: Path) -> dict[str, str]:
    raw = path.read_text(encoding="utf-8-sig")
    block = re.search(r"\A---\s*\n(.*?)\n---", raw, re.S)[1]
    values = {}
    for key in ("title", "seoTitle", "description"):
        values[key] = re.search(rf'^{key}:\s*"(.*)"$', block, re.M)[1]
    return values


def article_content(lang: str) -> str:
    name = "article-local-preview.html" if lang == "ja" else "article-local-preview-en.html"
    raw = (DRAFT / name).read_text(encoding="utf-8")
    content = re.search(r'<div class="article-content">(.*?)</div></article>', raw, re.S)[1]
    for filename in IMAGES:
        content = content.replace(f'./{filename}', f'/assets/images/articles/{SLUG}/{filename}?v=20261108')
    return content


def page(lang: str) -> str:
    prefix = "" if lang == "ja" else "en/"
    meta = frontmatter(DRAFT / ("article.md" if lang == "ja" else "article-en.md"))
    url = f"{BASE}/{prefix}articles/{SLUG}/"
    hero = f"{BASE}/assets/images/articles/{SLUG}/{IMAGES[0]}?v=20261108"
    locale = "ja_JP" if lang == "ja" else "en_US"
    category = "ろぶーの気になる事 / 家電・キッチン / 売れ筋チェック" if lang == "ja" else "Robu's Curiosities / Kitchen Appliances / Bestseller Check"
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
<link rel="stylesheet" href="/assets/css/contact-feedback-ees-standard.css?v=3" data-contact-feedback-style><link rel="stylesheet" href="/assets/css/draft-article-preview.css?v=20260930-publish-five-1"><style>.robu-article-layout>main.draft-main{{max-width:820px}}article{{overflow-wrap:anywhere}}.article-content img{{display:block;max-width:100%;width:auto;height:auto;margin:auto;border-radius:10px}}.article-content>p>em{{display:block;font-size:.9rem;line-height:1.7}}.purchase-panel{{background:transparent!important;box-shadow:none!important;border:1px solid #d8cfbf;border-radius:16px;padding:22px;margin:36px 0}}.purchase-buttons{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}}.purchase-button{{display:flex;align-items:center;justify-content:center;min-height:52px;padding:12px 14px;border:1px solid #b78f4d;border-radius:10px;text-align:center;font-weight:800;text-decoration:none}}.purchase-note,.disclosure{{font-size:.9rem;line-height:1.7}}@media(max-width:760px){{.purchase-buttons{{grid-template-columns:1fr}}}}</style><script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script><script defer src="/assets/js/shared-shell.js?v=20261016-browser-language-1"></script></head><body class="draft-preview robu-published-article"><main class="draft-main" data-contact-page><article><div class="selection-subcategory" data-article-category>{html.escape(category)}</div><div class="article-content">{article_content(lang)}</div></article></main><script src="/assets/js/contact-feedback.js?v=20260907-1"></script></body></html>'''


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
        "id": article_id,
        "date": DATE,
        "dateLabel": "2026.11.08",
        "category": "ろぶーの気になる事 / 家電・キッチン / 売れ筋チェック",
        "title": metadata["ja"]["title"],
        "digestTitle": "疲れた夜に、温かい一品をおまかせ",
        "digestLead": "材料を入れて待つ間に別のことができる、自動調理ポットの魅力と注意点を確認します。",
        "excerpt": metadata["ja"]["description"],
        "enTitle": metadata["en"]["title"],
        "enExcerpt": metadata["en"]["description"],
        "image": f"assets/images/articles/{SLUG}/{IMAGES[0]}",
        "url": f"/articles/{SLUG}/",
        "imageAlt": "夜の台所で自動調理ポットに調理を任せ、食卓でひと息つく様子を表したAI生成の編集用イメージ",
    }
    text = text.replace("const articles = [", "const articles = [\n      " + json.dumps(card, ensure_ascii=False, separators=(",", ":")) + ",", 1)
    text = text.replace("const articleFilters = {", f"const articleFilters = {{\n      '{article_id}': [],", 1)
    index.write_text(text, encoding="utf-8")

sitemap = ROOT / "sitemap.xml"
text = sitemap.read_text(encoding="utf-8")
if f"{BASE}/articles/{SLUG}/" not in text:
    block = f'''<url><loc>{BASE}/articles/{SLUG}/</loc><lastmod>{DATE}</lastmod><xhtml:link rel="alternate" hreflang="ja" href="{BASE}/articles/{SLUG}/"/><xhtml:link rel="alternate" hreflang="en" href="{BASE}/en/articles/{SLUG}/"/><xhtml:link rel="alternate" hreflang="x-default" href="{BASE}/articles/{SLUG}/"/></url>\n<url><loc>{BASE}/en/articles/{SLUG}/</loc><lastmod>{DATE}</lastmod><xhtml:link rel="alternate" hreflang="ja" href="{BASE}/articles/{SLUG}/"/><xhtml:link rel="alternate" hreflang="en" href="{BASE}/en/articles/{SLUG}/"/><xhtml:link rel="alternate" hreflang="x-default" href="{BASE}/articles/{SLUG}/"/></url>\n'''
    sitemap.write_text(text.replace("</urlset>", block + "</urlset>"), encoding="utf-8")

html_sitemap = ROOT / "sitemap" / "index.html"
text = html_sitemap.read_text(encoding="utf-8")
if f"/articles/{SLUG}/" not in text:
    items = (f'<ul><li><a href="/articles/{SLUG}/">{html.escape(metadata["ja"]["title"])}</a></li>'
             f'<li><a href="/en/articles/{SLUG}/">{html.escape(metadata["en"]["title"])}</a></li></ul>')
    text = text.replace("<h2>AI・テクノロジー</h2>", "<h2>AI・テクノロジー</h2>" + items, 1)
    html_sitemap.write_text(text, encoding="utf-8")

record = ROOT / "records" / "2026" / "11" / "2026-11-08-recolte-rsy2-publication.md"
record.parent.mkdir(parents=True, exist_ok=True)
record.write_text("""# レコルト RSY-2記事 公開記録

- 公開承認: 2026-11-08、ユーザーの明示承認
- 分類: ろぶーの気になる事 / 家電・キッチン / 売れ筋チェック
- 日本語・英語: 承認済み最終稿
- 画像: AI生成の編集用画像2枚。正確な外観・公式画像ではない旨を本文中に明記
- アフィリエイト: Amazon、楽天市場、Yahoo!ショッピング。可視開示と sponsored 属性を設定
- ファクトチェック: レコルト公式ページ・会社情報・LP・取扱説明書・RSY-3公式ページ、楽天とYahoo!の確認日つき市場情報
- SNS: ユーザーが同日投稿を明示承認。公開後の実行結果を別途確認
""", encoding="utf-8")

print("Published recolte RSY-2 production files")
