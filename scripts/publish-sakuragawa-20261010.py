"""Build the owner-approved bilingual Sakuragawa article; no remote writes."""
from pathlib import Path
from html import escape
import json
import re
import shutil
import subprocess
import runpy

ROOT = Path(__file__).resolve().parents[1]
DRAFT = Path('E:/Documents/ろぶーの気になる事（記事）/香港飲茶　桜川/draft-20261010-v1')
SLUG = 'hong-kong-yum-cha-sakuragawa-lunch'
DATE = '2026-10-10'
BASE = 'https://www.axis-jp.net/'
FFMPEG = 'E:/Documents/Codex/_tools/ffmpeg/ffmpeg-9.0.1-essentials_build/bin/ffmpeg.exe'
render = runpy.run_path(str(DRAFT / 'build_preview.py'))['render_markdown']
images = list(dict.fromkeys(re.findall(r'!\[[^\]]*\]\(\.\./([^)]*)\)', (DRAFT / 'article-ja.md').read_text(encoding='utf-8'))))
image_dir = ROOT / 'assets/images/articles' / SLUG
video_dir = ROOT / 'assets/videos/articles' / SLUG
image_dir.mkdir(parents=True, exist_ok=True)
video_dir.mkdir(parents=True, exist_ok=True)
for name in images:
    shutil.copy2(DRAFT.parent / name, image_dir / name)
for src in sorted(DRAFT.parent.glob('VID_*.mp4')):
    target = video_dir / (src.stem + '-web.mp4')
    if not target.exists():
        subprocess.run([FFMPEG, '-v', 'error', '-i', str(src), '-vf', 'scale=1280:-2', '-c:v', 'libx264', '-crf', '24', '-preset', 'fast', '-an', '-movflags', '+faststart', str(target)], check=True)

meta = {}
for lang in ('ja', 'en'):
    source = DRAFT / f'article-{lang}.md'
    raw = source.read_text(encoding='utf-8')
    title = re.search(r'^title: "(.*)"$', raw, re.M)[1]
    desc = re.search(r'^description: "(.*)"$', raw, re.M)[1]
    cat = 'ろぶーの気になる事 / グルメ・外食' if lang == 'ja' else "Robu's Curiosities / Food & Restaurants"
    body = re.sub(r'^<h1>.*?</h1>\s*', '', render(source), count=1)
    body = body.replace('Robu’s conclusion', 'Robu’s Take')
    for name in images:
        body = body.replace('../' + name, '/assets/images/articles/' + SLUG + '/' + name)
    for src in DRAFT.parent.glob('VID_*.mp4'):
        body = body.replace('../' + src.name, '/assets/videos/articles/' + SLUG + '/' + src.stem + '-web.mp4')
    body = body.replace('<video controls', '<video muted controls')
    body = body.replace('<p>※この記事は、', '<p class="affiliate-note">※この記事は、').replace('<p>Note: This is an independent', '<p class="affiliate-note">Note: This is an independent')
    prefix = 'articles/' if lang == 'ja' else 'en/articles/'
    url = BASE + prefix + SLUG + '/'
    hero = BASE + 'assets/images/articles/' + SLUG + '/' + images[0]
    schema = {'@context':'https://schema.org','@type':'BlogPosting','headline':title,'description':desc,'datePublished':DATE,'dateModified':DATE,'inLanguage':lang,'mainEntityOfPage':url,'image':[hero],'author':{'@type':'Organization','name':'ろぶーの気になる事'},'publisher':{'@type':'Organization','name':'ろぶーの気になる事','url':BASE}}
    head = f'''<!doctype html><html lang="{lang}" translate="no"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="google" content="notranslate"><meta name="social:publish" content="false"><meta name="robots" content="index,follow,max-image-preview:large">
<title>{escape(title)}</title><meta name="description" content="{escape(desc, quote=True)}">
<link rel="canonical" href="{url}"><link rel="alternate" hreflang="ja" href="{BASE}articles/{SLUG}/"><link rel="alternate" hreflang="en" href="{BASE}en/articles/{SLUG}/"><link rel="alternate" hreflang="x-default" href="{BASE}articles/{SLUG}/">
<meta property="og:type" content="article"><meta property="og:title" content="{escape(title, quote=True)}"><meta property="og:description" content="{escape(desc, quote=True)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{hero}"><meta property="og:site_name" content="ろぶーの気になる事"><meta property="article:section" content="{escape(cat, quote=True)}"><meta property="article:published_time" content="{DATE}T00:00:00+09:00"><meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="/assets/css/contact-feedback-ees-standard.css?v=3" data-contact-feedback-style><link rel="stylesheet" href="/assets/css/draft-article-preview.css?v=20260930-publish-five-1">
<style>.article-content img,.article-content video{{display:block;max-width:100%;height:auto;margin-inline:auto;border-radius:10px}}.article-content figure{{margin:1.6rem 0}}.article-content figcaption{{font-size:.9rem}}.article-content video{{width:100%;max-height:75vh;background:#111}}.article-content .affiliate-note{{font-size:.9rem;line-height:1.7;color:#51483f}}.affiliate-button{{display:block;max-width:520px;margin:1.5rem auto;padding:1rem;text-align:center;background:#a83232;color:#fff!important;border-radius:8px;font-weight:700;text-decoration:none}}.affiliate-button:hover,.affiliate-button:focus-visible{{background:#7e1e1e}}</style>
<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script><script defer src="/assets/js/shared-shell.js?v=20261003-desktop-left-toc-1"></script></head>
<body class="draft-preview robu-published-article"><main class="draft-main" data-contact-page><article><div class="selection-subcategory" data-article-category>{escape(cat)}</div><h1 class="article-title">{escape(title)}</h1><div class="article-content">{body}</div></article></main><script src="/assets/js/contact-feedback.js?v=20260907-1"></script></body></html>'''
    head = head.replace('</style>', '.article-content .affiliate-note{background:transparent;border:0;box-shadow:none;padding:0;border-radius:0}</style>')
    target = ROOT / prefix / SLUG / 'index.html'
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(head, encoding='utf-8')
    meta[lang] = {'title':title, 'description':desc, 'category':cat}

article_id = SLUG + '-' + DATE
index = ROOT / 'index.html'
text = index.read_text(encoding='utf-8')
if article_id not in text:
    card = {'id':article_id,'date':DATE,'dateLabel':'2026.10.10','category':meta['ja']['category'],'title':meta['ja']['title'],'digestTitle':'桜川で楽しむ、2種類の飲茶ランチ','digestLead':'点心、お粥、焼きそばと単品のマンゴープリンを実食。','excerpt':meta['ja']['description'],'enTitle':meta['en']['title'],'enExcerpt':meta['en']['description'],'image':'assets/images/articles/'+SLUG+'/'+images[0],'url':'/articles/'+SLUG+'/','imageAlt':'香港飲茶 桜川の点心と大根餅'}
    text = text.replace('const articles = [','const articles = [\n      '+json.dumps(card, ensure_ascii=False, separators=(',',':'))+',',1)
    text = text.replace('const articleFilters = {',"const articleFilters = {\n      '"+article_id+"': ['gourmet'],",1)
    index.write_text(text, encoding='utf-8')
path = ROOT / 'sitemap.xml'
text = path.read_text(encoding='utf-8')
for prefix in ('articles/','en/articles/'):
    url = BASE + prefix + SLUG + '/'
    if url not in text:
        text = text.replace('</urlset>',f'<url><loc>{url}</loc><lastmod>{DATE}</lastmod></url>\n</urlset>')
path.write_text(text,encoding='utf-8')
path = ROOT / 'sitemap/index.html'
text = path.read_text(encoding='utf-8')
if '/articles/'+SLUG+'/' not in text:
    text = text.replace('<h2>ホテル・グルメ</h2>', '<h2>ホテル・グルメ</h2>\n<ul>'+''.join(f'<li><a href="/{prefix}{SLUG}/">{escape(meta[lang]["title"])}</a></li>' for lang,prefix in [('ja','articles/'),('en','en/articles/')])+'</ul>',1)
    path.write_text(text,encoding='utf-8')
print('Built bilingual article, photographs, three web videos, gourmet card and sitemaps.')
