"""Build the user-approved bilingual ROG XBOX Ally X20 article."""
from pathlib import Path
import html
import json
import re
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[1]
DRAFT = Path(
    "E:/Documents/Codex/2026-08-01/robuse-selection-drafts/Draft/"
    "2026-10-16/2026-10-16-02-robus-selection-rog-xbox-ally-x20-v11"
)
NODE = r"C:\Users\yrt11\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe"
MARKED = r"C:\Users\yrt11\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\node_modules\marked"
SLUG = "rog-xbox-ally-x20-seven-checks"
PUBLISH_DATE = "2026-10-16"
BASE = "https://www.axis-jp.net/"
IMAGE_DIR = f"/assets/images/articles/{SLUG}/"
ASUS_URL = (
    "https://click.linksynergy.com/deeplink?id=y1gjgfCIQEk&mid=43708&"
    "murl=https%3A%2F%2Fstore.asus.com%2Fjp%2Frog-xbox-ally-x20-"
    "rc74xa-rz2r24g1t-gaming-handheld.html"
)
AMAZON_URL = (
    "https://www.amazon.co.jp/dp/B0HH8TC4TK?th=1&linkCode=ll2&"
    "tag=womaster-22&linkId=0ba080687b20a4b04054fd52fdb70152&ref_=as_li_ss_tl"
)
SOURCES = [
    ("ASUS JAPAN：ROG XBOX Ally X20を10月16日に発売", "https://www.asus.com/jp/news/rog-xbox-ally-x20-on-shelf/"),
    ("ASUS JAPAN：ROG XBOX Ally X20シリーズ予約開始", "https://www.asus.com/jp/news/rog-xbox-ally-x20-pre-order-start/"),
    ("ROG日本：ROG XBOX Ally X20 製品ページ", "https://rog.asus.com/jp/gaming-handhelds/rog-ally/rog-xbox-ally-x20-2026/"),
    ("ASUS Store：RC74XA-RZ2R24G1T", "https://store.asus.com/jp/rog-xbox-ally-x20-rc74xa-rz2r24g1t-gaming-handheld.html"),
    ("Xbox日本：ROG XBOX AllyとGame Pass", "https://www.xbox.com/ja-JP/handhelds/rog-xbox-ally/"),
]
DESCRIPTIONS = {
    "ja": "ROG XBOX Ally X20を25万8800円、7.4型OLED、Ryzen AI Z2 Extreme、操作系、80Wh、756g、Windows運用の7項目で公式情報から確認します。",
    "en": "A seven-point buying guide to the ROG XBOX Ally X20, covering its ¥258,800 price, 7.4-inch OLED display, Ryzen AI Z2 Extreme, controls, 80Wh battery, 756g weight and Windows experience.",
}
IMAGE_SPECS = [
    (
        "rog-xbox-ally-x20-editorial-hero-v2.png",
        "ROG XBOX Ally X20の半透明ブラック筐体、ゴールド装飾、緑のXboxボタンを参考にしたAI生成編集画像",
        "ASUS公式の製品仕様と外観説明を参考にしたAI生成編集イメージです。公式写真や実機写真ではなく、細部や寸法は実物と異なる場合があります。",
        "AI-generated editorial image inspired by the translucent black shell, gold details and green Xbox button of the ROG XBOX Ally X20",
        "AI-generated editorial image based on official product descriptions. It is not an ASUS photograph or a substitute for hands-on inspection.",
    ),
    (
        "handheld-gaming-travel-context-v1.png",
        "列車内で大型携帯ゲーミングPCと充電器を持ち運ぶ場面を表したAI生成編集画像",
        "使用場面を表すAI生成の概念イメージです。実機、付属充電器、列車設備の再現ではありません。",
        "AI-generated editorial image showing a large handheld gaming PC and charger during train travel",
        "AI-generated concept image illustrating a travel scenario. It does not reproduce the device, charger or train equipment.",
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
        kicker, title = "購入先", "販売店を選ぶ"
        disclosure = "<strong>広告：</strong>以下の購入先リンクはアフィリエイトリンクです。リンク経由の購入により、当サイトが報酬を受け取る場合があります。"
        note = "価格、在庫、キャンペーン、付属品は変わるため、最終条件はリンク先で確認してください。"
        action = "価格・在庫を見る"
        asus_detail, amazon_detail = "ASUS公式ストア", "Amazon.co.jp"
    else:
        kicker, title = "WHERE TO BUY", "Choose a retailer"
        disclosure = "<strong>Advertisement:</strong> the following retailer links are affiliate links. This site may receive a commission from qualifying purchases."
        note = "Prices, availability, promotions and included items may change. Check the final terms on the retailer page."
        action = "Check price and availability"
        asus_detail, amazon_detail = "ASUS Official Store", "Amazon Japan"
    return f'''<section class="purchase-panel" id="purchase" aria-labelledby="purchase-heading"><span class="purchase-kicker">{kicker}</span><h2 id="purchase-heading">{title}</h2><p class="affiliate-note">{disclosure}</p><div class="merchant-grid"><a class="merchant-card asus" href="{html.escape(ASUS_URL, quote=True)}" target="_blank" rel="nofollow sponsored noopener noreferrer"><span class="merchant-mark asus" aria-hidden="true">ASUS</span><span class="merchant-copy"><strong>{asus_detail}</strong><small>ROG XBOX Ally X20</small></span><span class="merchant-action">{action}<span aria-hidden="true">→</span></span></a><a class="merchant-card amazon" href="{html.escape(AMAZON_URL, quote=True)}" target="_blank" rel="nofollow sponsored noopener noreferrer"><span class="merchant-mark amazon" aria-hidden="true">Amazon</span><span class="merchant-copy"><strong>{amazon_detail}</strong><small>ROG XBOX Ally X20</small></span><span class="merchant-action">{action}<span aria-hidden="true">→</span></span></a></div><p class="purchase-note">{note}</p></section>'''


def source_panel(lang: str) -> str:
    heading = "公式・一次情報" if lang == "ja" else "Primary sources"
    items = "".join(
        f'<li><a href="{url}" target="_blank" rel="noopener noreferrer">{html.escape(label)}</a></li>'
        for label, url in SOURCES
    )
    note = (
        "価格・仕様確認日：2026年10月16日。実機未使用の購入ガイドです。"
        if lang == "ja"
        else "Price and specifications checked on 16 October 2026. This is a non-hands-on buying guide."
    )
    return f'<section aria-labelledby="sources-heading"><h2 id="sources-heading">{heading}</h2><ol class="source-list">{items}</ol><p class="article-note">{note}</p></section>'


def related_panel(lang: str) -> str:
    if lang == "ja":
        return '<aside class="related-panel" aria-label="関連記事"><strong>あわせて読みたい</strong><a href="/articles/crazy-taxi-world-tour-seven-things/">WindowsやXboxで遊べる新作ゲームの確認ポイント</a><a href="/articles/google-pixel-watch-5/">携帯デバイスの画面・電池・地域差を確認する</a></aside>'
    return '<aside class="related-panel" aria-label="Related articles"><strong>Related reading</strong><a href="/en/articles/crazy-taxi-world-tour-seven-things/">What to check before playing a new Windows or Xbox game</a><a href="/en/articles/google-pixel-watch-5/">Checking the display, battery and regional details of a mobile device</a></aside>'


meta = {}
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
        figure = f'<figure><img src="{IMAGE_DIR}{filename}" alt="{html.escape(alt, quote=True)}" width="1672" height="941" loading="lazy"><figcaption>{html.escape(caption)}</figcaption></figure>'
        body = body.replace(f"IMAGE_{index}", figure)

    purchase_start = "## 購入先" if lang == "ja" else "## Where to buy"
    sources_start = "## 公式・一次情報" if lang == "ja" else "## Primary sources"
    body = re.sub(
        rf"{re.escape(purchase_start)}.*?(?={re.escape(sources_start)})",
        "RELATED_PANEL\n\nPURCHASE_PANEL\n\n",
        body,
        flags=re.S,
    )
    body = re.sub(rf"{re.escape(sources_start)}.*\Z", "SOURCE_PANEL", body, flags=re.S)
    rendered = render_markdown(body.strip())
    rendered = rendered.replace("<p><figure>", "<figure>").replace("</figure></p>", "</figure>")
    rendered = rendered.replace("<p>RELATED_PANEL</p>", related_panel(lang))
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
        "citation": [url for _, url in SOURCES],
    }
    page = f'''<!doctype html><html lang="{lang}" translate="no"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="google" content="notranslate"><meta name="robots" content="index,follow,max-image-preview:large"><meta name="social:publish" content="false"><meta name="social:ai-image" content="true"><meta name="social:disclosure" content="AI-generated editorial images are used. Affiliate links appear only in the purchase section."><title>{html.escape(title)}</title><meta name="description" content="{html.escape(description, quote=True)}"><link rel="canonical" href="{url}"><link rel="alternate" hreflang="ja" href="{BASE}articles/{SLUG}/"><link rel="alternate" hreflang="en" href="{BASE}en/articles/{SLUG}/"><link rel="alternate" hreflang="x-default" href="{BASE}articles/{SLUG}/"><meta property="og:type" content="article"><meta property="og:title" content="{html.escape(title, quote=True)}"><meta property="og:description" content="{html.escape(description, quote=True)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{hero}"><meta property="article:section" content="ろぶーの気になる事 / ガジェット"><meta property="article:published_time" content="{PUBLISH_DATE}T00:00:00+09:00"><meta name="twitter:card" content="summary_large_image"><link rel="stylesheet" href="/assets/css/contact-feedback-ees-standard.css?v=3" data-contact-feedback-style><link rel="stylesheet" href="/assets/css/draft-article-preview.css?v=20260930-publish-five-1"><style>.robu-article-layout>main.draft-main{{max-width:820px}}article{{overflow-wrap:anywhere}}.article-content figure{{margin:28px 0}}.article-content img{{display:block;max-width:100%;width:auto;height:auto;max-height:640px;margin:auto;border-radius:10px}}figcaption{{font-size:14px;line-height:1.7;margin-top:10px}}.purchase-panel{{margin:46px 0 34px;padding:26px;border:1px solid #d5dce7;border-radius:20px;background:linear-gradient(145deg,#fbfcfe,#f1f4f8);box-shadow:0 16px 36px rgba(16,24,40,.09)}}.purchase-panel h2{{margin:.15em 0 .55em;padding:0;border:0}}.purchase-kicker{{display:inline-flex;padding:4px 10px;border-radius:999px;background:#e8eefb;color:#254b9c;font-size:.78rem;font-weight:900;letter-spacing:.08em}}.affiliate-note{{margin:0 0 18px;color:#475467;font-size:.95rem}}.merchant-grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}}.merchant-card{{display:grid;grid-template-columns:auto 1fr;align-items:center;gap:12px;min-height:126px;padding:18px;border:1px solid #cad2df;border-radius:16px;background:#fff;color:#18212b!important;text-decoration:none;box-shadow:0 8px 18px rgba(16,24,40,.07)}}.merchant-card:hover,.merchant-card:focus-visible{{transform:translateY(-2px);box-shadow:0 13px 26px rgba(16,24,40,.13);border-color:#6d8fe5}}.merchant-mark{{display:flex;align-items:center;justify-content:center;width:78px;height:46px;border-radius:11px;font-weight:950}}.merchant-mark.asus{{background:#071b2b;color:#fff;font-style:italic;letter-spacing:.08em}}.merchant-mark.amazon{{position:relative;background:#fff4dd;color:#111}}.merchant-mark.amazon:after{{content:"";position:absolute;left:17px;right:12px;bottom:9px;height:5px;border-bottom:3px solid #ff9900;border-radius:0 0 55% 55%}}.merchant-copy strong,.merchant-copy small{{display:block}}.merchant-copy small{{color:#667085}}.merchant-action{{grid-column:1/-1;display:flex;justify-content:space-between;padding-top:11px;border-top:1px solid #e4e8ee;color:#1749b7;font-weight:850}}.purchase-note{{margin:16px 0 0;color:#667085;font-size:.9rem}}.related-panel{{display:grid;gap:8px;margin:32px 0;padding:18px 20px;border-left:4px solid #7594d8;background:#f4f7fc}}.source-list{{padding-left:1.4em}}@media(max-width:640px){{.merchant-grid{{grid-template-columns:1fr}}.purchase-panel{{padding:20px 16px}}}}</style><script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script><script defer src="/assets/js/shared-shell.js?v=20261016-browser-language-1"></script></head><body class="draft-preview robu-published-article"><main class="draft-main" data-contact-page><article><div class="selection-subcategory" data-article-category>ろぶーの気になる事 / ガジェット</div><h1 class="article-title">{html.escape(title)}</h1><div class="article-content">{rendered}</div></article></main><script src="/assets/js/contact-feedback.js?v=20260907-1"></script></body></html>'''
    assert page.count("<figure>") == 2
    assert 'rel="nofollow sponsored noopener noreferrer"' in page
    assert "unpublished" not in page.lower()
    assert "ろぶーの結論" in page if lang == "ja" else "Robu’s Take" in page
    target = ROOT / prefix / "articles" / SLUG / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(page, encoding="utf-8")
    meta[lang] = {"title": title, "description": description}


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
        "dateLabel": "2026.10.16",
        "category": "ろぶーの気になる事 / ガジェット",
        "title": meta["ja"]["title"],
        "digestTitle": "ROG XBOX Ally X20、25万8,800円の価値は？",
        "digestLead": "OLED、重さ、電池、Windows運用を7項目で確認します。",
        "excerpt": meta["ja"]["description"],
        "enTitle": meta["en"]["title"],
        "enExcerpt": meta["en"]["description"],
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
    items = f'<ul><li><a href="/articles/{SLUG}/">{html.escape(meta["ja"]["title"])}</a></li><li><a href="/en/articles/{SLUG}/">{html.escape(meta["en"]["title"])}</a></li></ul>'
    text = text.replace("<h2>AI・テクノロジー</h2>", "<h2>AI・テクノロジー</h2>" + items, 1)
    html_sitemap.write_text(text, encoding="utf-8")

record = ROOT / "records" / "2026" / "10" / "2026-10-16-rog-xbox-ally-x20-publication.md"
record.parent.mkdir(parents=True, exist_ok=True)
record.write_text(
    "# ROG XBOX Ally X20記事 公開記録\n\n"
    "- 公開承認: 2026-10-16、ユーザーの明示承認\n"
    "- 日本語・英語: v11を使用\n"
    "- 画像: AI生成編集イメージ2枚、読者向け注記あり\n"
    "- 購入先: ASUS公式とAmazon、記事末尾のマーク付きカード\n"
    "- 楽天・Yahoo!: 同一型番の本体を確認できなかったため掲載なし\n"
    "- SNS自動配信: 今回は未承認のため無効\n"
    "- ファクトチェック: 公式・一次情報5件、18項目を確認\n",
    encoding="utf-8",
)

print("Built the approved bilingual ROG XBOX Ally X20 article, branded purchase cards, images, catalogue card, and sitemaps.")
