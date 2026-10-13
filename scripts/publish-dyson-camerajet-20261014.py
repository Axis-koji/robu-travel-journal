"""Build the user-approved Dyson CameraJet article without changing prior drafts."""
from pathlib import Path
import html
import json
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
DRAFT = Path(
    "E:/Documents/Codex/2026-08-01/robuse-selection-drafts/Draft/"
    "2026-10-13/2026-10-13-02-robus-selection-dyson-camerajet-v1"
)
NODE = r"C:\Users\yrt11\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe"
MARKED = r"C:\Users\yrt11\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\node_modules\marked"
SLUG = "dyson-camerajet-seven-checks"
DATE = "2026-10-14"
BASE = "https://www.axis-jp.net/"
IMG_DIR = f"/assets/images/articles/{SLUG}/"
LINKSHARE = (
    "https://click.linksynergy.com/deeplink?id=y1gjgfCIQEk&mid=49460&"
    "murl=https%3A%2F%2Fwww.dyson.co.jp%2Foral-care%2Felectric-toothbrush%2F"
    "camerajet%2Fceramic-pink"
)
RAKUTEN = (
    "https://hb.afl.rakuten.co.jp/ichiba/587917ae.f55fff5b.587917af.f7c82bf2/"
    "?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fdyson%2F638170-01%2F&"
    "link_type=hybrid_url&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJoeWJyaWRfdXJsIiwic2l6ZSI6"
    "IjI0MHgyNDAiLCJuYW0iOjEsIm5hbXAiOiJyaWdodCIsImNvbSI6MSwiY29tcCI6ImRvd24iLCJw"
    "cmljZSI6MSwiYm9yIjoxLCJjb2wiOjEsImJidG4iOjEsInByb2QiOjAsImFtcCI6ZmFsc2V9"
)


def render_markdown(markdown: str) -> str:
    return subprocess.run(
        [
            NODE,
            "-e",
            "const fs=require('fs');const m=require(process.argv[1]);"
            "process.stdout.write(m.marked.parse(fs.readFileSync(0,'utf8')))",
            MARKED,
        ],
        input=markdown,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=True,
    ).stdout


def sponsored_links(rendered: str) -> str:
    return re.sub(
        r'<a href="([^"]*(?:linksynergy\.com|hb\.afl\.rakuten\.co\.jp)[^"]*)">',
        r'<a href="\1" rel="nofollow sponsored noopener noreferrer" target="_blank">',
        rendered,
    )


meta = {}
for lang in ("ja", "en"):
    source = DRAFT / ("article-v4.md" if lang == "ja" else "article-en.md")
    raw = source.read_text(encoding="utf-8-sig")
    title = re.search(r'^title: "(.+)"$', raw, re.M)[1]
    desc = re.search(r'^description: "(.+)"$', raw, re.M)[1]
    body = re.sub(r"\A---\s*\n.*?\n---\s*\n", "", raw, flags=re.S)
    body = re.sub(r"^# .*\n", "", body, count=1)
    body = body.replace("こんにちは、ろぶーです。\n", "").replace("Hello, I'm Robu.\n", "")
    body = re.sub(r"^> (?:公開前メモ|Pre-publication note):?.*$", "", body, flags=re.M)
    body = re.sub(r"^> 公開前メモ：.*$", "", body, flags=re.M)
    body = re.sub(
        r"!\[[^\]]*\]\(dyson-camerajet-editorial-hero-v1\.png\)\s*\n\s*\*[^\n]+\*",
        "HERO_FIGURE",
        body,
    )
    body = re.sub(
        r"!\[[^\]]*\]\(dyson-camerajet-usage-v1\.png\)\s*\n\s*\*[^\n]+\*",
        "USAGE_FIGURE",
        body,
    )
    if lang == "ja":
        body = body.replace("## 公式情報", "## 公式出典")
        captions = (
            "カメラとジェットを備えた電動歯ブラシ、給水充電ドック、ケースの編集用AIイメージ。公式製品写真ではなく、細部は実物と異なります。",
            "電動歯ブラシを使いながらスマートフォンの磨き範囲を確認する編集用AIイメージ。画面は公式UIではありません。",
        )
    else:
        body = body.replace("on October 13, 2026", "on October 14, 2026")
        body = body.replace("when checked on October 13", "when checked on October 14")
        affiliate = (
            "\n*Advertisement: The following purchase links are affiliate links. "
            "This site may earn a commission if you buy through them.*\n\n"
            f"- [Check CameraJet availability at the Dyson official store]({LINKSHARE})\n"
            f"- [Check price and points at the Dyson official Rakuten store]({RAKUTEN})\n\n"
        )
        body = body.replace("## 2. A 100k-pixel camera finds gaps", affiliate + "## 2. A 100k-pixel camera finds gaps")
        body = body.replace("## Robu's conclusion", "## Robu’s Take")
        captions = (
            "AI-generated editorial concept of the camera-and-jet toothbrush, refill charging dock, and case. This is not an official product photograph, and details may differ.",
            "AI-generated editorial concept of a person checking brushing coverage on a phone. The screen is not the official MyDyson interface.",
        )

    rendered = sponsored_links(render_markdown(body.strip()))
    for token, filename, caption in (
        ("HERO_FIGURE", "dyson-camerajet-editorial-hero-v1.png", captions[0]),
        ("USAGE_FIGURE", "dyson-camerajet-usage-v1.png", captions[1]),
    ):
        figure = (
            f'<figure><img src="{IMG_DIR}{filename}" alt="{html.escape(caption, quote=True)}" '
            'width="1672" height="941" loading="lazy"><figcaption>'
            f"{html.escape(caption)}</figcaption></figure>"
        )
        rendered = rendered.replace(f"<p>{token}</p>", figure)
    rendered = re.sub(
        r"<p><em>((?:広告：|Advertisement:)[^<]+)</em></p>",
        r'<p class="affiliate-note"><em>\1</em></p>',
        rendered,
    )

    prefix = "" if lang == "ja" else "en/"
    url = f"{BASE}{prefix}articles/{SLUG}/"
    hero = f"{BASE.rstrip('/')}{IMG_DIR}dyson-camerajet-editorial-hero-v1.png"
    schema = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": title,
        "description": desc,
        "datePublished": DATE,
        "dateModified": DATE,
        "inLanguage": lang,
        "mainEntityOfPage": url,
        "image": [hero],
        "author": {"@type": "Organization", "name": "ろぶーの気になる事"},
        "publisher": {"@type": "Organization", "name": "ろぶーの気になる事"},
        "citation": [
            "https://www.dyson.co.jp/oral-care/electric-toothbrush/camerajet/ceramic-pink",
            "https://www.dyson.co.jp/oral-care/electric-toothbrush/camerajet/ceramic-ultra-blue",
            "https://www.dyson.co.jp/discover/news/latest/introducing-camerajet",
            "https://www.dyson.co.jp/support/journey/tools/976005-01",
            "https://www.dyson.com/oral-care/electric-toothbrush/camerajet/ceramic-pink",
        ],
    }
    page = f'''<!doctype html><html lang="{lang}" translate="no"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="index,follow,max-image-preview:large"><meta name="google" content="notranslate"><meta name="social:publish" content="true"><meta name="social:disclosure" content="記事内の購入リンクはアフィリエイト広告です。"><meta name="social:ai-image" content="true"><meta property="article:section" content="Robu's Selection"><title>{html.escape(title)}</title><meta name="description" content="{html.escape(desc, quote=True)}"><link rel="canonical" href="{url}"><link rel="alternate" hreflang="ja" href="{BASE}articles/{SLUG}/"><link rel="alternate" hreflang="en" href="{BASE}en/articles/{SLUG}/"><link rel="alternate" hreflang="x-default" href="{BASE}articles/{SLUG}/"><meta property="og:type" content="article"><meta property="og:title" content="{html.escape(title, quote=True)}"><meta property="og:description" content="{html.escape(desc, quote=True)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{hero}"><meta property="article:published_time" content="{DATE}T00:00:00+09:00"><meta name="twitter:card" content="summary_large_image"><link rel="stylesheet" href="/assets/css/contact-feedback-ees-standard.css?v=3" data-contact-feedback-style><link rel="stylesheet" href="/assets/css/draft-article-preview.css?v=20260912-4"><style>.robu-article-layout>main.draft-main{{max-width:820px}}article{{overflow-wrap:anywhere}}.article-content figure{{margin:28px 0}}.article-content img{{display:block;max-width:100%;width:auto;height:auto;max-height:640px;margin:auto}}figcaption{{font-size:14px;line-height:1.7;margin-top:10px}}.affiliate-note{{font-size:.9rem;color:#6f665c;margin-top:1.25rem}}.affiliate-note+ul{{margin-top:.5rem}}@media(max-width:640px){{.article-content figure{{margin:20px 0}}}}</style><script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script><script defer src="/assets/js/shared-shell.js?v=20261003-desktop-left-toc-1"></script></head><body class="draft-preview robu-published-article"><main class="draft-main" data-contact-page><article><h1 class="article-title">{html.escape(title)}</h1><div class="article-content">{rendered}</div></article></main><script src="/assets/js/contact-feedback.js?v=20260907-1"></script></body></html>'''
    assert "noindex" not in page
    assert "公開前メモ" not in page and "Pre-publication note" not in page
    assert page.count('rel="nofollow sponsored noopener noreferrer"') == 2
    assert '<p class="affiliate-note">' in page
    assert "HERO_FIGURE" not in page and "USAGE_FIGURE" not in page
    target = ROOT / prefix / "articles" / SLUG / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(page, encoding="utf-8")
    meta[lang] = {"title": title, "description": desc}

image_target = ROOT / "assets" / "images" / "articles" / SLUG
image_target.mkdir(parents=True, exist_ok=True)
for filename in ("dyson-camerajet-editorial-hero-v1.png", "dyson-camerajet-usage-v1.png"):
    shutil.copy2(DRAFT / filename, image_target / filename)

article_id = f"{SLUG}-{DATE}"
index = ROOT / "index.html"
text = index.read_text(encoding="utf-8")
if article_id not in text:
    card = {
        "id": article_id,
        "date": DATE,
        "dateLabel": "2026.10.14",
        "category": "Robu’s Selection / 生活家電",
        "title": meta["ja"]["title"],
        "digestTitle": "7万9800円のCameraJet、買う前に見る7項目",
        "digestLead": "カメラ、ジェット、手入れ、アプリ、試験条件まで公式情報で確認します。",
        "excerpt": meta["ja"]["description"],
        "enTitle": meta["en"]["title"],
        "enExcerpt": meta["en"]["description"],
        "image": f"assets/images/articles/{SLUG}/dyson-camerajet-editorial-hero-v1.png",
        "url": f"/articles/{SLUG}/",
        "imageAlt": "カメラとジェットを備えた電動歯ブラシのAI生成編集イメージ",
    }
    text = text.replace("const articles = [", "const articles = [\n      " + json.dumps(card, ensure_ascii=False) + ",", 1)
    text = text.replace("const articleFilters = {", f"const articleFilters = {{\n      '{article_id}': ['selection'],", 1)
    index.write_text(text, encoding="utf-8")

sitemap = ROOT / "sitemap.xml"
text = sitemap.read_text(encoding="utf-8")
for prefix in ("", "en/"):
    url = f"{BASE}{prefix}articles/{SLUG}/"
    if url not in text:
        text = text.replace("</urlset>", f"<url><loc>{url}</loc><lastmod>{DATE}</lastmod></url>\n</urlset>")
sitemap.write_text(text, encoding="utf-8")

html_sitemap = ROOT / "sitemap" / "index.html"
text = html_sitemap.read_text(encoding="utf-8")
if f'/articles/{SLUG}/' not in text:
    items = (
        f'<li><a href="/articles/{SLUG}/">{html.escape(meta["ja"]["title"])}</a></li>'
        f'<li><a href="/en/articles/{SLUG}/">{html.escape(meta["en"]["title"])}</a></li>'
    )
    text = text.replace("<h2>Robu's Selection</h2><ul>", "<h2>Robu's Selection</h2><ul>" + items, 1)
    html_sitemap.write_text(text, encoding="utf-8")

print("Built the approved bilingual Dyson CameraJet article, images, index card, and sitemaps.")
