"""Build the approved expanded Gemini draft using the shared article shell."""
from pathlib import Path
from html import escape
import argparse, json, re, shutil

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path('E:/Documents/gemini-rewrite-preview/index.html')
ASSETS = Path('E:/Documents/Codex/2026-08-01/robuse-selection-drafts/Draft/2026-10-10/2026-10-10-01-robu-kininaru-gemini-agent-v1')
SLUG = 'gemini-agent-enterprise-work'
DATE = '2026-10-11'
BASE = 'https://www.axis-jp.net/'
parser = argparse.ArgumentParser()
parser.add_argument('--social', action='store_true')
args = parser.parse_args()
publish_social = 'true' if args.social else 'false'
titles = {'ja':'Gemini agentって何？ 調べものから資料作りまで、AIに任せる仕事の話', 'en':'What Is Gemini Agent? From Research to Presentations, Explained Simply'}
descs = {'ja':'企業向けGemini agentで何が便利になる？ 資料作りを例に、作業手順の共有、AIの分担、権限と費用の管理を公式情報から整理。普段のGeminiとの違いや、導入前に確認したい点も紹介します。', 'en':'A plain-language look at Google Cloud’s enterprise Gemini agent: research, presentations, reusable skills, agent coordination and controls, with practical questions to ask before adopting it.'}
image_names = ['gemini-agent-workflow-hero-v1.png', 'gemini-agent-governance-flow-v1.png']
image_dir = ROOT/'assets/images/articles'/SLUG
image_dir.mkdir(parents=True, exist_ok=True)
for name in image_names:
    shutil.copy2(ASSETS/name, image_dir/name)
ja = SOURCE.read_text(encoding='utf-8').split('</h1>',1)[1].split('</main>',1)[0].strip()
ja = ja.replace('元の記事にあった「スキル」という言葉は','「スキル」という言葉は')
ja = ja.replace('<h2>僕なら、まず下書きまで任せたい</h2>', '<h2>仕事を進めるための三つの仕組み</h2>')
ja = ja.replace('市場の動きを調べ、その内容を表に整理して、説明用のスライドにまとめる。Googleは、こうした複数の作業をつないで進める例を紹介しています。', 'Googleは、市場の動向を調べ、Sheetsで財務モデルを作り、両方の内容を説明するスライドにまとめる例を紹介しています。複数のアプリにまたがる作業をつなぐ考え方です。')
ja = ja.replace('<p>僕なら「資料を読む」「下書きを作る」と、「外へ送る」「公開する」は分けたいです。便利だからといって全部を任せるのではなく、確認する場所を決めておく。そのための管理機能にも、企業向けサービスとしての意味があると感じます。</p>\n<p>調査や資料の下書きを任せられるのは便利そうです。一方で、メールの送信や記事の公開まで、確認なしで進めてほしいわけではありません。</p>\n<p>僕なら、まずは情報を集めて整理するところまで。外に出す前には自分で読む。そんな使い方から始めたいです。</p>', '<p>僕なら「資料を読む」「下書きを作る」と、「外へ送る」「公開する」は分けたいです。まずは情報を集めて整理するところまで任せ、外に出す前には自分で読む。その境界を決められる管理機能にも、企業向けサービスとしての意味があると感じます。</p>')
bodies = {'ja':ja, 'en':(ROOT/'records/2026/10/gemini-agent-body-en.html').read_text(encoding='utf-8')}
captions = {'ja':['資料作りの流れを表したAI生成イメージ。GoogleやGeminiの実画面ではありません。','権限・操作記録・人による確認を表したAI生成イメージ。Googleの公式構成図ではありません。'], 'en':['AI-generated illustration of a document workflow, not a real Google or Gemini interface.','AI-generated illustration of permissions, action records and human review, not an official Google architecture diagram.']}
sources = [('Google公式発表','Google announcement','https://blog.google/innovation-and-ai/infrastructure-and-cloud/google-cloud/gemini-at-work/'),('Google Cloud：Gemini agentの紹介','Google Cloud: Introducing Gemini agent','https://cloud.google.com/blog/products/ai-machine-learning/welcome-to-gemini-at-work-2026')]
for lang in ['ja','en']:
    body = bodies[lang]
    anchors = ['<h2>例えば、会議の資料を作るとき</h2>', '<h3>何を任せて、どこで止めるか</h3>'] if lang=='ja' else ['<h2>Take preparing a meeting presentation</h2>', '<h3>Deciding what is allowed—and when to stop</h3>']
    for name, caption, anchor in zip(image_names,captions[lang],anchors):
        figure = f'<figure><img src="/assets/images/articles/{SLUG}/{name}" alt="{escape(caption)}" width="1672" height="941" loading="lazy"><figcaption>{caption}</figcaption></figure>'
        body = body.replace(anchor,figure+'\n'+anchor,1)
    body += '<h2>'+('公式情報' if lang=='ja' else 'Official sources')+'</h2><ul>'+''.join(f'<li><a href="{url}">{labelja if lang=="ja" else labelen}</a></li>' for labelja,labelen,url in sources)+'</ul>'
    prefix = '' if lang=='ja' else 'en/'
    url = BASE+prefix+'articles/'+SLUG+'/'
    hero = BASE+'assets/images/articles/'+SLUG+'/'+image_names[0]
    schema = {'@context':'https://schema.org','@type':'BlogPosting','headline':titles[lang],'description':descs[lang],'datePublished':DATE,'dateModified':DATE,'inLanguage':lang,'mainEntityOfPage':url,'image':[hero],'author':{'@type':'Organization','name':'ろぶーの気になる事'},'publisher':{'@type':'Organization','name':'ろぶーの気になる事'}}
    page = f'''<!doctype html><html lang="{lang}" translate="no"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="google" content="notranslate"><meta name="robots" content="index,follow,max-image-preview:large"><meta name="social:publish" content="{publish_social}"><meta name="social:ai-image" content="true">
<title>{escape(titles[lang])}</title><meta name="description" content="{escape(descs[lang],quote=True)}"><link rel="canonical" href="{url}"><link rel="alternate" hreflang="ja" href="{BASE}articles/{SLUG}/"><link rel="alternate" hreflang="en" href="{BASE}en/articles/{SLUG}/"><link rel="alternate" hreflang="x-default" href="{BASE}articles/{SLUG}/">
<meta property="og:type" content="article"><meta property="og:title" content="{escape(titles[lang],quote=True)}"><meta property="og:description" content="{escape(descs[lang],quote=True)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{hero}"><meta property="article:section" content="ろぶーの気になる事 / AI・テクノロジー"><meta property="article:published_time" content="{DATE}T00:00:00+09:00"><meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="/assets/css/contact-feedback-ees-standard.css?v=3" data-contact-feedback-style><link rel="stylesheet" href="/assets/css/draft-article-preview.css?v=20260930-publish-five-1">
<style>.robu-article-layout>main.draft-main{{max-width:820px}}article{{overflow-wrap:anywhere}}.article-content figure{{margin:28px 0}}.article-content img{{display:block;max-width:100%;height:auto;margin:auto;border-radius:10px}}figcaption{{font-size:14px;line-height:1.7;margin-top:10px}}</style>
<script type="application/ld+json">{json.dumps(schema,ensure_ascii=False)}</script><script defer src="/assets/js/shared-shell.js?v=20261003-desktop-left-toc-1"></script></head><body class="draft-preview robu-published-article"><main class="draft-main" data-contact-page><article><h1 class="article-title">{escape(titles[lang])}</h1><div class="article-content">{body}</div></article></main><script src="/assets/js/contact-feedback.js?v=20260907-1"></script></body></html>'''
    assert '書き直し案' not in page and '元の記事にあった' not in page
    target = ROOT/prefix/'articles'/SLUG/'index.html'
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(page,encoding='utf-8')
article_id = SLUG+'-'+DATE
path = ROOT/'index.html'
text = path.read_text(encoding='utf-8')
if article_id not in text:
    card = {'id':article_id,'date':DATE,'dateLabel':'2026.10.11','category':'ろぶーの気になる事 / AI・テクノロジー','title':titles['ja'],'excerpt':descs['ja'],'enTitle':titles['en'],'enExcerpt':descs['en'],'image':'assets/images/articles/'+SLUG+'/'+image_names[0],'url':'/articles/'+SLUG+'/','imageAlt':captions['ja'][0]}
    text = text.replace('const articles = [','const articles = [\n      '+json.dumps(card,ensure_ascii=False)+',',1)
    text = text.replace('const articleFilters = {',"const articleFilters = {\n      '"+article_id+"': [],",1)
    path.write_text(text,encoding='utf-8')
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
    text = text.replace('<h2>AI・テクノロジー</h2>', '<h2>AI・テクノロジー</h2><ul>'+''.join(f'<li><a href="/{prefix}articles/{SLUG}/">{escape(titles[lang])}</a></li>' for lang,prefix in [('ja',''),('en','en/')])+'</ul>',1)
    path.write_text(text,encoding='utf-8')
print('Built approved bilingual Gemini article; social publish:', publish_social)
