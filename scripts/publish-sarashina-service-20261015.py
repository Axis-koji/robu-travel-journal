"""Build the user-approved bilingual Sarashina Service article."""
from pathlib import Path
import html
import json
import re
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[1]
DRAFT = Path(
    "E:/Documents/Codex/2026-08-01/robuse-selection-drafts/Draft/"
    "2026-10-14/2026-10-14-01-robu-kininaru-sarashina-service-v1"
)
NODE = r"C:\Users\yrt11\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe"
MARKED = r"C:\Users\yrt11\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\node_modules\marked"
SLUG = "sarashina-service-six-models-beta"
PUBLISH_DATE = "2026-10-16"
BASE = "https://www.axis-jp.net/"
IMAGE_DIR = f"/assets/images/articles/{SLUG}/"
SOURCES = [
    "https://www.sbintuitions.co.jp/news/press/20261013_01/",
    "https://www.sbintuitions.co.jp/news/press/20260630_01/",
    "https://www.sbintuitions.co.jp/blog/entry/2026/06/30/100000",
    "https://www.sbintuitions.co.jp/blog/entry/2026/07/02/101054",
    "https://www.sbintuitions.co.jp/blog/entry/2026/07/03/100056",
    "https://www.sbintuitions.co.jp/blog/entry/2026/07/01/071349",
    "https://www.sbintuitions.co.jp/blog/entry/2026/07/14/100002",
]


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


meta = {}
for lang in ("ja", "en"):
    source = DRAFT / ("article-v2.md" if lang == "ja" else "article-en-v2.md")
    raw = source.read_text(encoding="utf-8-sig")
    title = re.search(r'^title: "(.+)"$', raw, re.M)[1]
    description = re.search(r'^description: "(.+)"$', raw, re.M)[1]
    body = re.sub(r"\A---\s*\n.*?\n---\s*\n", "", raw, flags=re.S)
    body = re.sub(r"^# .*\n", "", body, count=1)
    body = re.sub(r"^> (?:公開前メモ|Pre-publication note):?.*$", "", body, flags=re.M)

    image_specs = [
        (
            "sarashina-service-six-models-hero-v1.png",
            "開発者と利用者が6つのAI機能を一緒に確認する編集用イメージ",
            "編集部制作のAIイメージ。実在の画面、公式UI、性能評価を再現したものではありません。",
            "A developer and a user reviewing six coordinated AI capabilities",
            "AI-generated editorial image. It does not reproduce the real service, an official interface, or benchmark results.",
        ),
        (
            "sarashina-service-evaluation-pipeline-v1.png",
            "開発者と確認担当者が検索・順位付け・安全確認・翻訳の流れを検証する編集用イメージ",
            "編集部制作のAIイメージ。実際のAPI構成、公式画面、安全性保証を示すものではありません。",
            "A developer and reviewer testing retrieval, ranking, safety, and translation checkpoints",
            "AI-generated editorial image. It is not an actual API architecture, interface, or guarantee of safety.",
        ),
    ]
    for index, (filename, alt_ja, caption_ja, alt_en, caption_en) in enumerate(image_specs, start=1):
        alt = alt_ja if lang == "ja" else alt_en
        caption = caption_ja if lang == "ja" else caption_en
        body = re.sub(
            rf"!\[[^\]]*\]\({re.escape(filename)}\)\s*\n\s*\*[^\n]+\*",
            f"IMAGE_{index}",
            body,
            count=1,
        )
        figure = (
            f'<figure><img src="{IMAGE_DIR}{filename}" alt="{html.escape(alt, quote=True)}" '
            f'width="1672" height="941" loading="lazy"><figcaption>{html.escape(caption)}</figcaption></figure>'
        )
        body = body.replace(f"IMAGE_{index}", figure)

    if lang == "ja":
        body = body.replace("## ろぶーの見方", "## ろぶーの結論")
    else:
        body = body.replace("## Robu's view", "## Robu’s Take")

    rendered = render_markdown(body.strip())
    # Marked escapes raw HTML only when configured to do so; with the shared runtime it preserves figures.
    rendered = rendered.replace("<p><figure>", "<figure>").replace("</figure></p>", "</figure>")
    assert "公開前メモ" not in rendered and "Pre-publication note" not in rendered
    assert "noindex" not in rendered
    assert rendered.count("<figure>") == 2

    prefix = "" if lang == "ja" else "en/"
    url = f"{BASE}{prefix}articles/{SLUG}/"
    hero = f"{BASE.rstrip('/')}{IMAGE_DIR}{image_specs[0][0]}"
    schema = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": title,
        "description": description,
        "datePublished": PUBLISH_DATE,
        "dateModified": PUBLISH_DATE,
        "inLanguage": lang,
        "mainEntityOfPage": url,
        "image": [hero],
        "author": {"@type": "Organization", "name": "ろぶーの気になる事"},
        "publisher": {"@type": "Organization", "name": "ろぶーの気になる事"},
        "citation": SOURCES,
    }
    page = f'''<!doctype html><html lang="{lang}" translate="no"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="google" content="notranslate"><meta name="robots" content="index,follow,max-image-preview:large"><meta name="social:publish" content="false"><meta name="social:ai-image" content="true">
<title>{html.escape(title)}</title><meta name="description" content="{html.escape(description, quote=True)}"><link rel="canonical" href="{url}"><link rel="alternate" hreflang="ja" href="{BASE}articles/{SLUG}/"><link rel="alternate" hreflang="en" href="{BASE}en/articles/{SLUG}/"><link rel="alternate" hreflang="x-default" href="{BASE}articles/{SLUG}/">
<meta property="og:type" content="article"><meta property="og:title" content="{html.escape(title, quote=True)}"><meta property="og:description" content="{html.escape(description, quote=True)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{hero}"><meta property="article:section" content="ろぶーの気になる事 / AI・テクノロジー"><meta property="article:published_time" content="{PUBLISH_DATE}T00:00:00+09:00"><meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="/assets/css/contact-feedback-ees-standard.css?v=3" data-contact-feedback-style><link rel="stylesheet" href="/assets/css/draft-article-preview.css?v=20260930-publish-five-1">
<style>.robu-article-layout>main.draft-main{{max-width:820px}}article{{overflow-wrap:anywhere}}.article-content figure{{margin:28px 0}}.article-content img{{display:block;max-width:100%;width:auto;height:auto;max-height:640px;margin:auto;border-radius:10px}}figcaption{{font-size:14px;line-height:1.7;margin-top:10px}}@media(max-width:640px){{.article-content figure{{margin:20px 0}}}}</style>
<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script><script defer src="/assets/js/shared-shell.js?v=20261016-browser-language-1"></script></head><body class="draft-preview robu-published-article"><main class="draft-main" data-contact-page><article><h1 class="article-title">{html.escape(title)}</h1><div class="article-content">{rendered}</div></article></main><script src="/assets/js/contact-feedback.js?v=20260907-1"></script></body></html>'''
    assert 'meta name="robots" content="index,follow,max-image-preview:large"' in page
    assert "shared-shell.js" in page and "contact-feedback.js" in page
    target = ROOT / prefix / "articles" / SLUG / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(page, encoding="utf-8")
    meta[lang] = {"title": title, "description": description}


image_target = ROOT / "assets" / "images" / "articles" / SLUG
image_target.mkdir(parents=True, exist_ok=True)
for filename in (
    "sarashina-service-six-models-hero-v1.png",
    "sarashina-service-evaluation-pipeline-v1.png",
):
    shutil.copy2(DRAFT / filename, image_target / filename)


article_id = f"{SLUG}-{PUBLISH_DATE}"
index = ROOT / "index.html"
text = index.read_text(encoding="utf-8")
if article_id not in text:
    card = {
        "id": article_id,
        "date": PUBLISH_DATE,
        "dateLabel": "2026.10.16",
        "category": "ろぶーの気になる事 / AI・テクノロジー",
        "title": meta["ja"]["title"],
        "digestTitle": "無料の国産AI、6モデルをどう使い分ける？",
        "digestLead": "生成、検索、順位付け、安全確認、翻訳の役割を具体例で整理します。",
        "excerpt": meta["ja"]["description"],
        "enTitle": meta["en"]["title"],
        "enExcerpt": meta["en"]["description"],
        "image": f"assets/images/articles/{SLUG}/sarashina-service-six-models-hero-v1.png",
        "url": f"/articles/{SLUG}/",
        "imageAlt": "6つのAI機能を一緒に確認するAI生成編集イメージ",
    }
    text = text.replace("const articles = [", "const articles = [\n      " + json.dumps(card, ensure_ascii=False) + ",", 1)
    text = text.replace("const articleFilters = {", f"const articleFilters = {{\n      '{article_id}': [],", 1)
    index.write_text(text, encoding="utf-8")


sitemap = ROOT / "sitemap.xml"
text = sitemap.read_text(encoding="utf-8")
for prefix in ("", "en/"):
    url = f"{BASE}{prefix}articles/{SLUG}/"
    if url not in text:
        text = text.replace("</urlset>", f"<url><loc>{url}</loc><lastmod>{PUBLISH_DATE}</lastmod></url>\n</urlset>")
sitemap.write_text(text, encoding="utf-8")


html_sitemap = ROOT / "sitemap" / "index.html"
text = html_sitemap.read_text(encoding="utf-8")
if f"/articles/{SLUG}/" not in text:
    items = (
        f'<li><a href="/articles/{SLUG}/">{html.escape(meta["ja"]["title"])}</a></li>'
        f'<li><a href="/en/articles/{SLUG}/">{html.escape(meta["en"]["title"])}</a></li>'
    )
    text = text.replace("<h2>AI・テクノロジー</h2>", "<h2>AI・テクノロジー</h2><ul>" + items + "</ul>", 1)
    html_sitemap.write_text(text, encoding="utf-8")


record = ROOT / "records" / "2026" / "10" / "2026-10-16-sarashina-service-publication.md"
record.parent.mkdir(parents=True, exist_ok=True)
record.write_text(
    "# Sarashinaサービス記事 公開記録\n\n"
    "- 公開承認: 2026-10-16、ユーザーの明示承認\n"
    "- 日本語・英語: 訂正版 v2 を使用\n"
    "- 画像: AI生成編集イメージ2枚、読者向け表示あり\n"
    "- SNS自動配信: 未承認のため無効\n"
    "- 確認: SB Intuitionsの公式発表・公式技術ブログ7件を公開直前に再確認\n",
    encoding="utf-8",
)

print("Built the approved bilingual Sarashina Service article, images, catalogue card, and sitemaps.")
