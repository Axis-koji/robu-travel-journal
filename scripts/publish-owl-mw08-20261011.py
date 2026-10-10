"""Build the approved OWL-MW08 article, preserving the original drafts."""
from pathlib import Path
import re, json, subprocess, html

ROOT = Path(__file__).resolve().parents[1]
DRAFT = Path('E:/Documents/Codex/2026-08-01/robuse-selection-drafts/Draft/2026-10-10/2026-10-10-02-robus-selection-owl-mw08-v1')
NODE = r'C:\Users\yrt11\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe'
MARKED = r'C:\Users\yrt11\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\node_modules\marked'
SLUG = 'owl-mw08-review'
DATE = '2026-10-11'
BASE = 'https://www.axis-jp.net/'
OFFICIAL = 'https://www.owltech.co.jp/product-top/cat_charger/cat_charger-wireless/mw08/'
AMAZON = 'https://www.amazon.co.jp/dp/B0HLRYX5F6?tag=womaster-22'
IMG = '/assets/images/articles/'+SLUG+'/'
meta = {}
for lang in ['ja','en']:
    raw = (DRAFT/('article.md' if lang=='ja' else 'article-en.md')).read_text(encoding='utf-8-sig')
    title = re.search(r'^title: "(.+)"$', raw, re.M)[1]
    desc = re.search(r'^description: "(.+)"$', raw, re.M)[1]
    body = re.sub(r'\A---\s*\n.*?\n---\s*\n', '', raw, flags=re.S)
    body = re.sub(r'^# .*\n', '', body, count=1)
    body = body.replace('こんにちは、ろぶーです。\n','').replace('Hello, this is Robu.\n','')
    body = re.sub(r'^> (公開前メモ|Pre-publication note):?.*$', '', body, flags=re.M)
    body = re.sub(r'^> 公開前メモ：.*$', '', body, flags=re.M)
    body = re.sub(r'!\[[^\]]*\]\(owl-mw08-cable-concept-v1.png\)\s*\n\s*\*[^\n]+\*', 'HERO_FIGURE', body)
    body = re.sub(r'!\[[^\]]*\]\(owl-mw08-travel-comparison-v1.png\)\s*\n\s*\*[^\n]+\*', 'WHITE_FIGURE', body)
    if lang=='ja':
        body = body.replace('2026年10月10日に確認した','2026年10月11日に確認した')
        body = body.replace('価格は変動する可能性があるため、購入時に再確認してください。','')
        body = body.replace('## ろぶーの選び方','## ろぶーの結論')
        body = body.replace('## 6. データ転送は最大480Mbps。映像ケーブルではない','## 6. データ転送は最大480Mbps。映像出力の記載はない')
        body = body.replace('## 公式・一次情報','## 公式出典')
        body = '本稿は実機を使用したレビューではなく、公式情報をもとにした購入前の整理です。\n\n'+body.strip()
        captions = ['ブラックの公式製品画像。円形の充電部と両端のUSB-C端子を一体化した形です。','ホワイトの公式製品画像。充電部とケーブル根元の形状も確認できます。']
        purchase = '購入先を確認する'
        label = 'Amazonで販売状況を確認する'
        disclosure = 'Amazonのアソシエイトとして、ろぶーの気になる事は適格販売により収入を得ています。'
    else:
        body = body.replace('when checked on October 10','when checked on October 11').replace('on October 10, 2026','on October 11, 2026')
        body = body.replace('Prices and stock can change, so the current store page should be checked before purchase.','')
        body = body.replace("## Robu's Selection",'## Robu’s Take')
        body = body.replace('## 6. Data Transfer Is up to 480Mbps; This Is Not a Display Cable','## 6. Up to 480Mbps Data; Video Output Is Not Listed')
        body = body.replace('## Official and Primary Sources','## Official sources')
        body = 'This is a buying guide based on official information, not a hands-on review.\n\n'+body.strip()
        captions = ['Official image of the black model, showing the integrated circular watch charger and USB-C connectors.','Official image of the white model, showing the charging surface and reinforced cable joints.']
        purchase = 'Check where to buy'
        label = 'Check availability on Amazon Japan'
        disclosure = 'As an Amazon Associate, we earn from qualifying purchases.'
    rendered = subprocess.run([NODE,'-e',"const fs=require('fs');const m=require(process.argv[1]);process.stdout.write(m.marked.parse(fs.readFileSync(0,'utf8')))",MARKED],input=body,text=True,encoding='utf-8',capture_output=True,check=True).stdout
    for token,color,caption in zip(['HERO_FIGURE','WHITE_FIGURE'],['black','white'],captions):
        figure = f'<figure><img src="{IMG}owl-mw08-{color}-official.jpg" alt="{html.escape(caption)}" width="1000" height="1000" loading="lazy"><figcaption>{caption} <a href="{OFFICIAL}" rel="noopener noreferrer">'+('出典：オウルテック' if lang=='ja' else 'Source: Owltech')+'</a></figcaption></figure>'
        rendered = rendered.replace('<p>'+token+'</p>',figure)
    panel = f'<section class="purchase-panel"><h2>{purchase}</h2><p>{disclosure}</p><div class="purchase-buttons"><a href="{AMAZON}" rel="nofollow sponsored noopener noreferrer" target="_blank">{label}</a></div></section>'
    source_title = '公式出典' if lang=='ja' else 'Official sources'
    rendered = rendered.replace('<h2>'+source_title+'</h2>',panel+'<h2>'+source_title+'</h2>')
    prefix = '' if lang=='ja' else 'en/'
    url = BASE+prefix+'articles/'+SLUG+'/'
    hero = BASE.rstrip('/')+IMG+'owl-mw08-black-official.jpg'
    schema = {'@context':'https://schema.org','@type':'BlogPosting','headline':title,'description':desc,'datePublished':DATE,'dateModified':DATE,'inLanguage':lang,'mainEntityOfPage':url,'image':[hero],'author':{'@type':'Organization','name':'ろぶーの気になる事'},'publisher':{'@type':'Organization','name':'ろぶーの気になる事'}}
    page = f'''<!doctype html><html lang="{lang}" translate="no"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="index,follow,max-image-preview:large"><meta name="google" content="notranslate"><meta name="social:publish" content="true"><meta name="social:disclosure" content="記事内の購入リンクはアフィリエイト広告です。"><meta name="social:ai-image" content="false"><meta property="article:section" content="Robu's Selection"><title>{html.escape(title)}</title><meta name="description" content="{html.escape(desc,quote=True)}"><link rel="canonical" href="{url}"><link rel="alternate" hreflang="ja" href="{BASE}articles/{SLUG}/"><link rel="alternate" hreflang="en" href="{BASE}en/articles/{SLUG}/"><link rel="alternate" hreflang="x-default" href="{BASE}articles/{SLUG}/"><meta property="og:type" content="article"><meta property="og:title" content="{html.escape(title,quote=True)}"><meta property="og:description" content="{html.escape(desc,quote=True)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{hero}"><meta property="article:published_time" content="{DATE}T00:00:00+09:00"><meta name="twitter:card" content="summary_large_image"><link rel="stylesheet" href="/assets/css/contact-feedback-ees-standard.css?v=3" data-contact-feedback-style><link rel="stylesheet" href="/assets/css/draft-article-preview.css?v=20260912-4"><style>.robu-article-layout>main.draft-main{{max-width:820px}}article{{overflow-wrap:anywhere}}.article-content figure{{margin:28px 0}}.article-content img{{display:block;max-width:100%;width:auto;height:auto;max-height:640px;margin:auto}}figcaption{{font-size:14px;line-height:1.7;margin-top:10px}}.purchase-panel h2{{font-size:22px}}.purchase-panel{{border:1px solid #ad9162;border-radius:12px;padding:20px;margin:28px 0}}.purchase-buttons{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}}.purchase-buttons a{{display:flex;min-height:56px;padding:12px;align-items:center;justify-content:center;text-align:center;background:#080b10;color:#f7efdc;border:1px solid #ad9162;border-radius:8px}}.purchase-buttons a:hover,.purchase-buttons a:focus-visible{{background:#ef8429;color:#111}}@media(max-width:640px){{.purchase-buttons{{grid-template-columns:1fr}}}}</style><script type="application/ld+json">{json.dumps(schema,ensure_ascii=False)}</script><script defer src="/assets/js/shared-shell.js?v=20261003-desktop-left-toc-1"></script></head><body class="draft-preview robu-published-article"><main class="draft-main" data-contact-page><article><div data-article-category>Robu’s Selection</div><h1 class="article-title">{html.escape(title)}</h1><div class="article-content">{rendered}</div></article></main><script src="/assets/js/contact-feedback.js?v=20260907-1"></script></body></html>'''
    page = page.replace('<div data-article-category>Robu’s Selection</div>', '')
    assert 'concept-v1.png' not in page and 'comparison-v1.png' not in page and 'HERO_FIGURE' not in page
    assert '公開前メモ' not in page and 'Pre-publication note' not in page
    target = ROOT/prefix/'articles'/SLUG/'index.html'
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(page,encoding='utf-8')
    meta[lang] = {'title':title,'description':desc}
article_id = SLUG+'-'+DATE
index = ROOT/'index.html'
text = index.read_text(encoding='utf-8')
if article_id not in text:
    card = {'id':article_id,'date':DATE,'dateLabel':'2026.10.11','category':"Robu’s Selection",'title':meta['ja']['title'],'excerpt':meta['ja']['description'],'enTitle':meta['en']['title'],'enExcerpt':meta['en']['description'],'image':IMG.lstrip('/')+'owl-mw08-black-official.jpg','url':'/articles/'+SLUG+'/','imageAlt':'OWL-MW08 ブラックの公式製品画像（出典：オウルテック）'}
    text = text.replace('const articles = [','const articles = [\n      '+json.dumps(card,ensure_ascii=False)+',',1)
    text = text.replace('const articleFilters = {',"const articleFilters = {\n      '"+article_id+"': ['selection'],",1)
    index.write_text(text,encoding='utf-8')
path = ROOT/'sitemap.xml'
text = path.read_text(encoding='utf-8')
for prefix in ['','en/']:
    url = BASE+prefix+'articles/'+SLUG+'/'
    if url not in text:
        text = text.replace('</urlset>',f'<url><loc>{url}</loc><lastmod>{DATE}</lastmod></url>\n</urlset>')
path.write_text(text,encoding='utf-8')
path = ROOT/'sitemap/index.html'
text = path.read_text(encoding='utf-8')
if '/articles/'+SLUG+'/' not in text:
    text = text.replace("<h2>Robu's Selection</h2>", "<h2>Robu's Selection</h2><ul>"+''.join(f'<li><a href="/{prefix}articles/{SLUG}/">{html.escape(meta[lang]["title"])}</a></li>' for lang,prefix in [('ja',''),('en','en/')])+'</ul>',1)
    path.write_text(text,encoding='utf-8')
print('Built only OWL-MW08 bilingual article, official images, Selection card and sitemap. SNS disabled.')
