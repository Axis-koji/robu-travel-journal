"""Build the approved bilingual HomePod mini 2 article."""
from pathlib import Path
import html
import json
import re
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[1]
DRAFT = Path(
    "E:/Documents/Codex/automation-2-tmp/git-sync-20261018-v1/Draft/"
    "2026-10-18/2026-10-18-02-robu-kininaru-homepod-mini-2-v3"
)
NODE = r"C:\Users\yrt11\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe"
MARKED = r"C:\Users\yrt11\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\node_modules\marked"
SLUG = "homepod-mini-2-buying-guide"
PUBLISH_DATE = "2026-10-19"
BASE = "https://www.axis-jp.net/"
IMAGE_DIR = f"/assets/images/articles/{SLUG}/"
APPLE_URL = "https://www.apple.com/jp/shop/buy-homepod/homepod-mini/"
SOURCES = [
    ("Apple Newsroom：次世代のHomePod miniを発表", "https://www.apple.com/jp/newsroom/2026/10/apple-announces-the-next-generation-of-homepod-mini/"),
    ("Apple Store：HomePod mini 2を予約注文", APPLE_URL),
    ("Apple：Home", "https://www.apple.com/jp/home/"),
    ("Apple：HomePod mini 2 技術仕様", "https://www.apple.com/jp/homepod-mini/specs/"),
]
DESCRIPTIONS = {
    "ja": "HomePod mini 2をApple公式情報で検証。24,800円、S10、音響構成、4台サラウンド条件、Mac・iPhone連携、スマートホーム機能を購入前に整理します。",
    "en": "A seven-point buying guide to HomePod mini 2, covering its ¥24,800 price, S10 chip, audio design, four-speaker surround requirements, Mac and iPhone compatibility, and smart-home features.",
}
IMAGE_SPECS = [
    (
        "homepod-mini-2-editorial-hero-v2.png",
        "公式形状を参考に球体に近い外観へ整えたHomePod mini 2のAI生成編集画像",
        "AI生成イメージ：Apple公式の形状を参考にした編集画像です。Appleの製品写真ではなく、色や細部は実物と異なる場合があります。",
        "AI-generated editorial image of HomePod mini 2 speakers with proportions based on Apple's official design",
        "AI-generated image based on Apple's official product shape. This is not an Apple photograph, and colors or details may differ from the actual product.",
    ),
    (
        "homepod-mini-2-four-speaker-surround-v3.png",
        "テレビの前後に同じHomePod mini 2を4台配置したサラウンド構成のAI生成編集画像",
        "AI生成イメージ：HomePod mini 2だけで組む4台構成の説明用画像です。Appleの製品写真や設置保証図ではありません。",
        "AI-generated editorial image showing a television with four matching HomePod mini 2 speakers",
        "AI-generated image explaining a four-unit HomePod mini 2 setup. It is not an Apple photograph or an installation guarantee.",
    ),
]


def render_markdown(markdown: str) -> str:
    return subprocess.run(
        [NODE, "-e", "const fs=require('fs');const m=require(process.argv[1]);process.stdout.write(m.marked.parse(fs.readFileSync(0,'utf8')))", MARKED],
        input=markdown,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=True,
    ).stdout


def purchase_panel(lang: str) -> str:
    if lang == "ja":
        heading = "購入先"
        intro = "現時点で同一商品を確認できた購入先はApple公式です。価格、色ごとの在庫、配送日は変わるため、注文画面で最新情報を確認してください。"
        store = "Apple公式ストア"
        action = "価格・在庫を見る"
        note = "Amazon、楽天市場、Yahoo!ショッピングでは同一商品を確認できなかったため、旧モデルや周辺機器への誤案内を避けて掲載していません。"
    else:
        heading = "Where to buy"
        intro = "Apple's official store is the only retailer where the exact product could be verified at this stage. Prices, color availability and delivery dates can change, so check the current order page."
        store = "Apple Official Store"
        action = "Check price and availability"
        note = "No exact listing was verified at Amazon Japan, Rakuten Ichiba or Yahoo! Shopping, so those links are omitted to avoid directing readers to an older model or accessory."
    return f'''<section class="purchase-panel" id="purchase" aria-labelledby="purchase-heading"><span class="purchase-kicker">{html.escape(heading)}</span><h2 id="purchase-heading">{html.escape(heading)}</h2><p>{html.escape(intro)}</p><a class="merchant-card apple" href="{APPLE_URL}" target="_blank" rel="noopener noreferrer"><span class="merchant-mark" aria-hidden="true">Apple</span><span class="merchant-copy"><strong>{html.escape(store)}</strong><small>HomePod mini 2</small></span><span class="merchant-action">{html.escape(action)}<span aria-hidden="true">→</span></span></a><p class="purchase-note">{html.escape(note)}</p></section>'''


def source_panel(lang: str) -> str:
    heading = "公式・一次情報" if lang == "ja" else "Official and primary sources"
    labels = (
        [label for label, _ in SOURCES]
        if lang == "ja"
        else [
            "Apple Newsroom: Apple announces the next generation of HomePod mini",
            "Apple Store: preorder HomePod mini 2",
            "Apple: Home",
            "Apple: HomePod mini 2 technical specifications",
        ]
    )
    items = "".join(
        f'<li><a href="{url}" target="_blank" rel="noopener noreferrer">{html.escape(label)}</a></li>'
        for label, (_, url) in zip(labels, SOURCES)
    )
    note = (
        "価格・仕様・発売条件は2026年10月19日にApple公式情報で再確認しました。購入前に最新情報をご確認ください。"
        if lang == "ja"
        else "Price, specifications and release conditions were rechecked against Apple's official information on 19 October 2026. Confirm the latest details before purchase."
    )
    return f'<section aria-labelledby="sources-heading"><h2 id="sources-heading">{heading}</h2><ol class="source-list">{items}</ol><p class="article-note">{note}</p></section>'


metadata = {}
for lang in ("ja", "en"):
    source = DRAFT / ("article.md" if lang == "ja" else "article-en.md")
    raw = source.read_text(encoding="utf-8-sig")
    title = re.search(r'^title: "(.+)"$', raw, re.M)[1]
    body = re.sub(r"\A---\s*\n.*?\n---\s*\n", "", raw, flags=re.S)
    body = re.sub(r"^# .*\n", "", body, count=1)

    for index, (filename, alt_ja, caption_ja, alt_en, caption_en) in enumerate(IMAGE_SPECS, start=1):
        alt = alt_ja if lang == "ja" else alt_en
        caption = caption_ja if lang == "ja" else caption_en
        body = re.sub(
            rf"!\[[^\]]*\]\({re.escape(filename)}\)\s*\n\s*[^\n]+",
            f"IMAGE_{index}",
            body,
            count=1,
        )
        figure = f'<figure><img src="{IMAGE_DIR}{filename}" alt="{html.escape(alt, quote=True)}" width="1536" height="1024" loading="lazy"><figcaption>{html.escape(caption)}</figcaption></figure>'
        body = body.replace(f"IMAGE_{index}", figure)

    purchase_heading = "## 購入先" if lang == "ja" else "## Where to buy"
    source_heading = "## 公式・一次情報" if lang == "ja" else "## Official and primary sources"
    body = re.sub(
        rf"{re.escape(purchase_heading)}.*?(?={re.escape(source_heading)})",
        "PURCHASE_PANEL\n\n",
        body,
        flags=re.S,
    )
    body = re.sub(rf"{re.escape(source_heading)}.*\Z", "SOURCE_PANEL", body, flags=re.S)
    rendered = render_markdown(body.strip())
    rendered = rendered.replace("<p><figure>", "<figure>").replace("</figure></p>", "</figure>")
    rendered = rendered.replace("<p>PURCHASE_PANEL</p>", purchase_panel(lang))
    rendered = rendered.replace("<p>SOURCE_PANEL</p>", source_panel(lang))

    prefix = "" if lang == "ja" else "en/"
    url = f"{BASE}{prefix}articles/{SLUG}/"
    hero = f"{BASE.rstrip('/')}{IMAGE_DIR}{IMAGE_SPECS[0][0]}"
    description = DESCRIPTIONS[lang]
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
        "author": {"@type": "Person", "name": "ろぶー"},
        "publisher": {"@type": "Organization", "name": "ろぶーの気になる事", "url": BASE.rstrip("/")},
        "citation": [source_url for _, source_url in SOURCES],
    }
    page = f'''<!doctype html><html lang="{lang}" translate="no"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="google" content="notranslate"><meta name="robots" content="index,follow,max-image-preview:large"><meta name="social:publish" content="false"><meta name="social:ai-image" content="true"><meta name="social:disclosure" content="AI-generated editorial images are used. No affiliate link is included in this article."><title>{html.escape(title)}</title><meta name="description" content="{html.escape(description, quote=True)}"><link rel="canonical" href="{url}"><link rel="alternate" hreflang="ja" href="{BASE}articles/{SLUG}/"><link rel="alternate" hreflang="en" href="{BASE}en/articles/{SLUG}/"><link rel="alternate" hreflang="x-default" href="{BASE}articles/{SLUG}/"><meta property="og:type" content="article"><meta property="og:title" content="{html.escape(title, quote=True)}"><meta property="og:description" content="{html.escape(description, quote=True)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{hero}"><meta property="article:section" content="ろぶーの気になる事 / オーディオ"><meta property="article:published_time" content="{PUBLISH_DATE}T00:00:00+09:00"><meta name="twitter:card" content="summary_large_image"><link rel="stylesheet" href="/assets/css/contact-feedback-ees-standard.css?v=3" data-contact-feedback-style><link rel="stylesheet" href="/assets/css/draft-article-preview.css?v=20260930-publish-five-1"><style>.robu-article-layout>main.draft-main{{max-width:820px}}article{{overflow-wrap:anywhere}}.article-content figure{{margin:28px 0}}.article-content img{{display:block;max-width:100%;width:auto;height:auto;max-height:640px;margin:auto;border-radius:10px}}figcaption{{font-size:14px;line-height:1.7;margin-top:10px}}.purchase-panel{{margin:46px 0 34px;padding:26px;border:1px solid #d8cfbf;border-radius:20px;background:linear-gradient(145deg,#fffdf8,#f5efe4);box-shadow:0 16px 36px rgba(61,45,29,.08)}}.purchase-panel h2{{margin:.15em 0 .55em;padding:0;border:0}}.purchase-kicker{{display:inline-flex;padding:4px 10px;border-radius:999px;background:#ece3d4;color:#76572f;font-size:.78rem;font-weight:900;letter-spacing:.08em}}.merchant-card{{display:grid;grid-template-columns:auto 1fr;align-items:center;gap:12px;max-width:560px;min-height:116px;margin-top:18px;padding:18px;border:1px solid #d2c4af;border-radius:16px;background:#fff;color:#18212b!important;text-decoration:none;box-shadow:0 8px 18px rgba(61,45,29,.07)}}.merchant-card:hover,.merchant-card:focus-visible{{transform:translateY(-2px);box-shadow:0 13px 26px rgba(61,45,29,.13);border-color:#9f7e4d}}.merchant-mark{{display:flex;align-items:center;justify-content:center;width:78px;height:46px;border-radius:11px;background:#111;color:#fff;font-weight:900}}.merchant-copy strong,.merchant-copy small{{display:block}}.merchant-copy small{{color:#667085}}.merchant-action{{grid-column:1/-1;display:flex;justify-content:space-between;padding-top:11px;border-top:1px solid #e4e8ee;color:#6c4c22;font-weight:850}}.purchase-note{{margin:16px 0 0;color:#667085;font-size:.9rem}}.source-list{{padding-left:1.4em}}@media(max-width:640px){{.purchase-panel{{padding:20px 16px}}}}</style><script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script><script defer src="/assets/js/shared-shell.js?v=20261016-browser-language-1"></script></head><body class="draft-preview robu-published-article"><main class="draft-main" data-contact-page><article><div class="selection-subcategory" data-article-category>ろぶーの気になる事 / オーディオ</div><h1 class="article-title">{html.escape(title)}</h1><div class="article-content">{rendered}</div></article></main><script src="/assets/js/contact-feedback.js?v=20260907-1"></script></body></html>'''
    assert page.count("<figure>") == 2
    assert "Robu's Selection" not in page and "Robu’s Selection" not in page
    assert "unpublished" not in page.lower()
    assert "ろぶーの結論" in page if lang == "ja" else "Robu’s Take" in page
    target = ROOT / prefix / "articles" / SLUG / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(page, encoding="utf-8")
    metadata[lang] = {"title": title, "description": description}


image_target = ROOT / "assets" / "images" / "articles" / SLUG
image_target.mkdir(parents=True, exist_ok=True)
for filename, *_ in IMAGE_SPECS:
    shutil.copy2(DRAFT / filename, image_target / filename)

article_id = f"{SLUG}-{PUBLISH_DATE}"
index = ROOT / "index.html"
text = index.read_text(encoding="utf-8")
if article_id not in text:
    card = {
        "id": article_id,
        "date": PUBLISH_DATE,
        "dateLabel": "2026.10.19",
        "category": "ろぶーの気になる事 / オーディオ",
        "title": metadata["ja"]["title"],
        "digestTitle": "HomePod mini 2、24,800円の価値は？",
        "digestLead": "S10、音響、4台サラウンド、Mac連携を7項目で確認します。",
        "excerpt": metadata["ja"]["description"],
        "enTitle": metadata["en"]["title"],
        "enExcerpt": metadata["en"]["description"],
        "image": f"assets/images/articles/{SLUG}/{IMAGE_SPECS[0][0]}",
        "url": f"/articles/{SLUG}/",
        "imageAlt": IMAGE_SPECS[0][1],
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
    items = f'<ul><li><a href="/articles/{SLUG}/">{html.escape(metadata["ja"]["title"])}</a></li><li><a href="/en/articles/{SLUG}/">{html.escape(metadata["en"]["title"])}</a></li></ul>'
    text = text.replace("<h2>AI・テクノロジー</h2>", "<h2>AI・テクノロジー</h2>" + items, 1)
    html_sitemap.write_text(text, encoding="utf-8")

record = ROOT / "records" / "2026" / "10" / "2026-10-19-homepod-mini-2-publication.md"
record.parent.mkdir(parents=True, exist_ok=True)
record.write_text(
    "# HomePod mini 2記事 公開記録\n\n"
    "- 公開承認: 2026-10-19、ユーザーの明示承認\n"
    "- 分類: 通常の『ろぶーの気になる事』。Robu's Selectionではない\n"
    "- 日本語・英語: v3を使用\n"
    "- 画像: AI生成編集イメージ2枚、読者向け注記あり\n"
    "- 購入先: Apple公式のみ。同一商品を確認できない販売店は掲載なし\n"
    "- アフィリエイト: 確認済みリンクなし\n"
    "- SNS自動配信: 今回は未承認のため無効\n"
    "- ファクトチェック: Apple公式・一次情報4件、4台構成の条件を再確認して反映\n",
    encoding="utf-8",
)

print("Built the approved bilingual HomePod mini 2 article, images, catalogue card, and sitemaps.")
