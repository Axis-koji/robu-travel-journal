import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const DRAFT = 'E:\\Documents\\Codex\\2026-08-01\\robuse-selection-drafts\\Draft\\2026-11-13\\2026-11-13-02-robus-selection-shunkai-neutral-atom-v8';
const SLUG = 'shunkai-neutral-atom-quantum-computer';
const DATE = '2026-11-14';
const BASE = 'https://www.axis-jp.net';
const IMAGES = ['shunkai-neutral-atom-lab-editorial-v1.png', 'neutral-atom-optical-tweezers-editorial-v1.png'];
const SOURCES = [
  'https://www.ims.ac.jp/news/2026/08/0824.html',
  'https://www.ims.ac.jp/en/news/2026/08/0824.html',
  'https://www.cao.go.jp/minister/2602_k_onoda/kaiken/20260825.html',
  'https://rd.hitachi.co.jp/_ct/17824971',
  'https://www.jst.go.jp/moonshot/program/goal6/6D_ohmori.html',
];

const read = (p) => fs.readFileSync(p, 'utf8');
const write = (p, value) => {
  fs.mkdirSync(path.dirname(p), { recursive: true });
  fs.writeFileSync(p, value.replace(/\r?\n/g, '\r\n'), 'utf8');
};
const escapeHtml = (value) => value.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('"', '&quot;').replaceAll("'", '&#x27;');

function frontmatter(file) {
  const block = read(file).match(/^---\s*\r?\n([\s\S]*?)\r?\n---/)[1];
  const value = (key) => block.match(new RegExp(`^${key}:\\s*"(.*)"$`, 'm'))?.[1];
  return { title: value('title'), description: value('description'), seoTitle: value('seoTitle') || value('title') };
}

function articleContent(lang) {
  const name = lang === 'ja' ? 'article-local-preview.html' : 'article-local-preview-en.html';
  let content = read(path.join(DRAFT, name)).match(/<div class="article-content">([\s\S]*?)<\/div><\/article>/)[1];
  for (const image of IMAGES) {
    content = content.replaceAll(`./${image}`, `/assets/images/articles/${SLUG}/${image}?v=20261114`);
  }
  return content;
}

function page(lang) {
  const prefix = lang === 'ja' ? '' : 'en/';
  const meta = frontmatter(path.join(DRAFT, lang === 'ja' ? 'article.md' : 'article-en.md'));
  const url = `${BASE}/${prefix}articles/${SLUG}/`;
  const hero = `${BASE}/assets/images/articles/${SLUG}/${IMAGES[0]}?v=20261114`;
  const locale = lang === 'ja' ? 'ja_JP' : 'en_US';
  const category = lang === 'ja' ? "Robu's Selection / 量子技術" : "Robu's Selection / Quantum Technology";
  const disclosure = lang === 'ja' ? '※記事内にはAI生成の編集画像を含みます。' : 'This article includes AI-generated editorial images.';
  const schema = {
    '@context': 'https://schema.org', '@type': 'BlogPosting', headline: meta.title,
    description: meta.description, datePublished: DATE, dateModified: DATE, inLanguage: lang,
    mainEntityOfPage: url, image: IMAGES.map((name) => `${BASE}/assets/images/articles/${SLUG}/${name}`),
    isAccessibleForFree: true, author: { '@type': 'Person', name: 'ろぶー' },
    publisher: { '@type': 'Organization', name: 'ろぶーの気になる事', url: BASE }, citation: SOURCES,
  };
  return `<!doctype html><html lang="${lang}" translate="no"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="google" content="notranslate"><meta name="robots" content="index,follow,max-image-preview:large"><meta name="referrer" content="strict-origin-when-cross-origin"><meta name="social:publish" content="false"><meta name="social:ai-image" content="true"><meta name="social:disclosure" content="${escapeHtml(disclosure)}">
<title>${escapeHtml(meta.seoTitle)}</title><meta name="description" content="${escapeHtml(meta.description)}"><link rel="canonical" href="${url}"><link rel="alternate" hreflang="ja" href="${BASE}/articles/${SLUG}/"><link rel="alternate" hreflang="en" href="${BASE}/en/articles/${SLUG}/"><link rel="alternate" hreflang="x-default" href="${BASE}/articles/${SLUG}/">
<meta property="og:type" content="article"><meta property="og:locale" content="${locale}"><meta property="og:site_name" content="ろぶーの気になる事"><meta property="og:title" content="${escapeHtml(meta.title)}"><meta property="og:description" content="${escapeHtml(meta.description)}"><meta property="og:url" content="${url}"><meta property="og:image" content="${hero}"><meta property="og:image:alt" content="${escapeHtml(meta.title)}"><meta property="article:section" content="${escapeHtml(category)}"><meta property="article:published_time" content="${DATE}T00:00:00+09:00"><meta property="article:modified_time" content="${DATE}T00:00:00+09:00"><meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="/assets/css/contact-feedback-ees-standard.css?v=3" data-contact-feedback-style><link rel="stylesheet" href="/assets/css/draft-article-preview.css?v=20260930-publish-five-1"><link rel="stylesheet" href="/assets/css/robus-selection-theme.css?v=20261025-standard-5" data-robu-selection-theme><style>.robu-article-layout>main.draft-main{max-width:820px}article{overflow-wrap:anywhere}.article-content img{display:block;max-width:100%;width:auto;height:auto;margin:auto;border-radius:10px}.article-content>p>em{display:block;font-size:.9rem;line-height:1.7}</style><script type="application/ld+json">${JSON.stringify(schema)}</script><script defer src="/assets/js/shared-shell.js?v=20261016-browser-language-1"></script></head><body class="draft-preview selection-preview robus-selection-page robu-published-article"><main class="draft-main" data-contact-page><article><div class="robu-selection-label">Robu's Selection</div><div class="selection-subcategory" data-article-category>${escapeHtml(category)}</div><div class="article-content">${articleContent(lang)}</div></article></main><script src="/assets/js/contact-feedback.js?v=20260907-1"></script></body></html>`;
}

const metadata = {
  ja: frontmatter(path.join(DRAFT, 'article.md')),
  en: frontmatter(path.join(DRAFT, 'article-en.md')),
};
for (const lang of ['ja', 'en']) {
  write(path.join(ROOT, ...(lang === 'ja' ? [] : ['en']), 'articles', SLUG, 'index.html'), page(lang));
}
const imageDir = path.join(ROOT, 'assets', 'images', 'articles', SLUG);
fs.mkdirSync(imageDir, { recursive: true });
for (const image of IMAGES) fs.copyFileSync(path.join(DRAFT, image), path.join(imageDir, image));

const articleId = `${SLUG}-${DATE}`;
const indexPath = path.join(ROOT, 'index.html');
let index = read(indexPath);
if (!index.includes(articleId)) {
  const card = {
    id: articleId, date: DATE, dateLabel: '2026.11.14', category: "Robu's Selection / 量子技術",
    title: metadata.ja.title, digestTitle: '原子を光で並べる、日本発の量子コンピュータ',
    digestLead: '約50量子ビットから2030年度の1万物理量子ビットへ。仕組みと開発体制を一次情報で確認します。',
    excerpt: metadata.ja.description, enTitle: metadata.en.title, enExcerpt: metadata.en.description,
    image: `assets/images/articles/${SLUG}/${IMAGES[0]}`, url: `/articles/${SLUG}/`,
    imageAlt: '中性原子量子コンピュータの光学系と原子配列モニターを表したAI生成の編集用イメージ',
  };
  index = index.replace('const articles = [', `const articles = [\n      ${JSON.stringify(card)},`);
  index = index.replace('const articleFilters = {', `const articleFilters = {\n      '${articleId}': ['selection'],`);
  write(indexPath, index);
}

const sitemapPath = path.join(ROOT, 'sitemap.xml');
let sitemap = read(sitemapPath);
if (!sitemap.includes(`${BASE}/articles/${SLUG}/`)) {
  const block = `<url><loc>${BASE}/articles/${SLUG}/</loc><lastmod>${DATE}</lastmod><xhtml:link rel="alternate" hreflang="ja" href="${BASE}/articles/${SLUG}/"/><xhtml:link rel="alternate" hreflang="en" href="${BASE}/en/articles/${SLUG}/"/><xhtml:link rel="alternate" hreflang="x-default" href="${BASE}/articles/${SLUG}/"/></url>\n<url><loc>${BASE}/en/articles/${SLUG}/</loc><lastmod>${DATE}</lastmod><xhtml:link rel="alternate" hreflang="ja" href="${BASE}/articles/${SLUG}/"/><xhtml:link rel="alternate" hreflang="en" href="${BASE}/en/articles/${SLUG}/"/><xhtml:link rel="alternate" hreflang="x-default" href="${BASE}/articles/${SLUG}/"/></url>\n`;
  write(sitemapPath, sitemap.replace('</urlset>', `${block}</urlset>`));
}

const htmlSitemapPath = path.join(ROOT, 'sitemap', 'index.html');
let htmlSitemap = read(htmlSitemapPath);
if (!htmlSitemap.includes(`/articles/${SLUG}/`)) {
  const items = `<ul><li><a href="/articles/${SLUG}/">${escapeHtml(metadata.ja.title)}</a></li><li><a href="/en/articles/${SLUG}/">${escapeHtml(metadata.en.title)}</a></li></ul>`;
  write(htmlSitemapPath, htmlSitemap.replace('<h2>AI・テクノロジー</h2>', `<h2>AI・テクノロジー</h2>${items}`));
}

write(path.join(ROOT, 'records', '2026', '11', '2026-11-14-shunkai-neutral-atom-publication.md'), `# 中性原子量子コンピュータ「春海」記事 公開記録

- 公開承認: 2026-11-14、ユーザーの明示承認
- 分類: Robu's Selection / 量子技術
- 日本語・英語: 読み合わせで防御的・否定的な但し書きを整理し、冷却装置と誤り耐性の説明を平易にしたv8
- 画像: AI生成の編集用画像2枚。公式写真や実際の装置構成ではない旨を本文中に明記
- アフィリエイト: なし
- ファクトチェック: IMS、内閣府、日立、JSTの一次・公式情報5件
- SNS: 今回は記事公開のみ。SNS投稿は実行せず、公開メタデータも無効
`);

for (const generated of [indexPath, sitemapPath, htmlSitemapPath]) write(generated, read(generated));

console.log('Published Shunkai production files');
