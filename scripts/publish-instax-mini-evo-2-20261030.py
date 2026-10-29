"""Publish the approved bilingual instax mini Evo 2 article."""
from pathlib import Path
import html
import json
import re
import shutil


ROOT = Path(__file__).resolve().parents[1]
DRAFT = Path(r"E:\Documents\Codex\2026-08-01\robuse-selection-drafts\Draft\2026-10-28\2026-10-28-02-robus-selection-instax-mini-evo-2-v1")
SLUG = "instax-mini-evo-2-share-memories"
DATE = "2026-10-30"
BASE = "https://www.axis-jp.net"
IMAGES = [
    "instax-mini-evo-2-hand-off-memory-v2.png",
    "instax-mini-evo-2-official-front-angle.png",
    "instax-mini-evo-2-handwritten-memory-v2.png",
    "instax-mini-evo-2-official-back-lcd.png",
]
SOURCES = [
    "https://www.fujifilm.com/jp/en/news/hq/14132",
    "https://instax.jp/mini_evo_2/",
    "https://instax.jp/item/camera/instax-mini-evo2/",
    "https://www.fujifilm.com/jp/ja/consumer/instax/cameras/minievo2/design",
    "https://www.fujifilm.com/jp/ja/news/list/12295",
    "https://www.fujifilm.com/jp/ja/news/list/14128",
    "https://magazine.instax.jp/cheki-press/interview/090-minilinkplus-nakakipantz/",
    "https://magazine.instax.jp/cheki-press/summary/35459/",
]


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
    category = "Robu's Selection / カメラ" if lang == "ja" else "Robu's Selection / Cameras"
    schema = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": meta["title"],
        "description": meta["description"],
        "datePublished": DATE,
        "dateModified": DATE,
        "inLanguage": lang,
        "mainEntityOfPage": url,
        "image": [hero],
        "author": {"@type": "Person", "name": "ろぶー"},
        "publisher": {"@type": "Organization", "name": "ろぶーの気になる事", "url": BASE},
        "citation": SOURCES,
    }
    return f'''<!doctype html><html lang="{lang}" translate="no"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="google" content="notranslate"><meta name="robots" content="index,follow,max-image-preview:large"><meta name="referrer" content="strict-origin-when-cross-origin"><meta name="social:publish" content="true"><meta name="social:ai-image" content="true"><meta name="social:disclosure" content="※記事内にはAI生成の編集画像、引用した公式画像、アフィリエイトリンクを含みます。">
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
        "id": article_id,
        "date": DATE,
        "dateLabel": "2026.10.30",
        "category": "Robu's Selection / カメラ",
        "title": metadata["ja"]["title"],
        "digestTitle": "その場で渡せる一枚と、残せる5秒",
        "digestLead": "チェキの原点に、4.5インチタッチパネルと5秒動画が加わった新しい思い出の残し方を紹介します。",
        "excerpt": metadata["ja"]["description"],
        "enTitle": metadata["en"]["title"],
        "enExcerpt": metadata["en"]["description"],
        "image": f"assets/images/articles/{SLUG}/{IMAGES[0]}",
        "url": f"/articles/{SLUG}/",
        "imageAlt": "旅先のカフェで小さな写真を相手へ手渡すAI生成の編集用イメージ",
    }
    text = text.replace("const articles = [", "const articles = [\n      " + json.dumps(card, ensure_ascii=False, separators=(",", ":")) + ",", 1)
    text = text.replace("const articleFilters = {", f"const articleFilters = {{\n      '{article_id}': ['selection'],", 1)
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

record = ROOT / "records" / "2026" / "10" / "2026-10-30-instax-mini-evo-2-publication.md"
record.parent.mkdir(parents=True, exist_ok=True)
record.write_text("""# instax mini Evo 2記事 公開記録

- 公開承認: 2026-10-30、ユーザーの明示承認
- 分類: Robu's Selection / カメラ
- 日本語・英語: 承認済み最終稿
- 画像: AI生成の編集用イメージ2枚、富士フイルム公式引用画像2枚、本文中に注記と出典
- アフィリエイト: Amazon、楽天市場、Yahoo!ショッピングの検索導線
- SNS: 本公開とは分けて扱う
- ファクトチェック: 富士フイルム公式製品ページ、ニュースリリース、公式メディア
""", encoding="utf-8")

print("Published instax mini Evo 2 production files")
