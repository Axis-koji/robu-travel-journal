import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const DRAFT = 'E:\\Documents\\Codex\\2026-08-01\\robuse-selection-drafts\\Draft\\2026-11-21\\2026-11-21-02-robus-selection-panasonic-er-sc6a-v1';
const SLUG = 'panasonic-er-sc6a-hair-clipper';
const DATE = '2026-11-22';
const BASE = 'https://www.axis-jp.net';
const IMAGES = ['panasonic-er-sc6a-editorial-hero-v2.png', 'panasonic-er-sc6a-rinse-editorial-v2.png'];
const SOURCES = [
  'https://news.panasonic.com/jp/topics/206874',
  'https://panasonic.jp/mens/products/ER-SC6A.html',
  'https://panasonic.jp/mens/products/ER-SC6A/spec.html',
  'https://store.shopping.yahoo.co.jp/panasonic-store/y-er-sc6a.html',
  'https://biccamera.rakuten.co.jp/item/4550719226995/',
  'https://shopping.yahoo.co.jp/product/j/4550719226995/compare.html',
];

const read = (p) => fs.readFileSync(p, 'utf8');
const write = (p, value) => {
  fs.mkdirSync(path.dirname(p), { recursive: true });
  fs.writeFileSync(p, value.replace(/\r?\n/g, '\r\n'), 'utf8');
};
const esc = (v) => v.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('"', '&quot;').replaceAll("'", '&#x27;');

function frontmatter(file) {
  const block = read(file).match(/^---\s*\r?\n([\s\S]*?)\r?\n---/)[1];
  const value = (key) => block.match(new RegExp(`^${key}:\\s*"(.*)"$`, 'm'))?.[1];
  return { title: value('title'), description: value('description'), seoTitle: value('seoTitle') || value('title') };
}

function content(lang) {
  const file = lang === 'ja' ? 'article-local-preview.html' : 'article-local-preview-en.html';
  let body = read(path.join(DRAFT, file)).match(/<div class="article-content">([\s\S]*?)<\/div><\/article>/)[1];
  for (const image of IMAGES) body = body.replaceAll(`./${image}`, `/assets/images/articles/${SLUG}/${image}?v=20261122`);
  return body.replaceAll(' data-purchase-disclosure', '');
}

function page(lang) {
  const prefix = lang === 'ja' ? '' : 'en/';
  const meta = frontmatter(path.join(DRAFT, lang === 'ja' ? 'article.md' : 'article-en.md'));
  const url = `${BASE}/${prefix}articles/${SLUG}/`;
  const hero = `${BASE}/assets/images/articles/${SLUG}/${IMAGES[0]}?v=20261122`;
  const locale = lang === 'ja' ? 'ja_JP' : 'en_US';
  const category = lang === 'ja' ? "Robu's Selection / 美容家電" : "Robu's Selection / Grooming Appliances";
  const disclosure = lang === 'ja'
    ? '記事内にはAI生成の編集画像とアフィリエイトリンクを含みます。'
    : 'This article includes AI-generated editorial images and affiliate links.';
  const schema = {
    '@context': 'https://schema.org', '@type': 'BlogPosting', headline: meta.title, description: meta.description,
    datePublished: DATE, dateModified: DATE, inLanguage: lang, mainEntityOfPage: url,
    image: IMAGES.map((n) => `${BASE}/assets/images/articles/${SLUG}/${n}`), isAccessibleForFree: true,
    author: { '@type': 'Person', name: 'ろぶー' }, publisher: { '@type': 'Organization', name: 'ろぶーの気になる事', url: BASE }, citation: SOURCES,
  };
  return `<!doctype html><html lang="${lang}" translate="no"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="google" content="notranslate"><meta name="robots" content="index,follow,max-image-preview:large"><meta name="referrer" content="strict-origin-when-cross-origin"><meta name="social:publish" content="true"><meta name="social:ai-image" content="true"><meta name="social:disclosure" content="${esc(disclosure)}">
<title>${esc(meta.seoTitle)}</title><meta name="description" content="${esc(meta.description)}"><link rel="canonical" href="${url}"><link rel="alternate" hreflang="ja" href="${BASE}/articles/${SLUG}/"><link rel="alternate" hreflang="en" href="${BASE}/en/articles/${SLUG}/"><link rel="alternate" hreflang="x-default" href="${BASE}/articles/${SLUG}/">
<meta property="og:type" content="article"><meta property="og:locale" content="${locale}"><meta property="og:site_name" content="ろぶーの気になる事"><meta property="og:title" content="${esc(meta.title)}"><meta property="og:description" content="${esc(meta.description)}"><meta property="og:url" content="${url}"><meta property="og:image" content="${hero}"><meta property="og:image:alt" content="${esc(meta.title)}"><meta property="article:section" content="${esc(category)}"><meta property="article:published_time" content="${DATE}T00:00:00+09:00"><meta property="article:modified_time" content="${DATE}T00:00:00+09:00"><meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="/assets/css/contact-feedback-ees-standard.css?v=3" data-contact-feedback-style><link rel="stylesheet" href="/assets/css/draft-article-preview.css?v=20260930-publish-five-1"><link rel="stylesheet" href="/assets/css/robus-selection-theme.css?v=20261025-standard-5" data-robu-selection-theme><style>.robu-article-layout>main.draft-main{max-width:820px}article{overflow-wrap:anywhere}.article-content img{display:block;max-width:100%;width:auto;height:auto;margin:auto;border-radius:10px}.article-content>p>em{display:block;font-size:.9rem;line-height:1.7}.purchase-panel{background:transparent!important;box-shadow:none!important;border:1px solid #b78f4d;border-radius:16px;padding:22px;margin:36px 0}.purchase-panel h2{font-size:min(22px,1.45rem)}.purchase-buttons{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}.purchase-button{display:flex;align-items:center;justify-content:center;min-height:52px;padding:12px 14px;background:#05080b!important;color:#fff7df!important;border:1px solid #b78f4d!important;border-radius:10px;text-align:center;font-weight:800;text-decoration:none}.purchase-button:hover,.purchase-button:focus-visible{background:#ea7317!important;color:#fff!important}.purchase-note{font-size:1rem;line-height:1.8}.disclosure{font-size:.88rem;line-height:1.7}@media(max-width:760px){.purchase-buttons{grid-template-columns:1fr}}</style><script type="application/ld+json">${JSON.stringify(schema)}</script><script defer src="/assets/js/shared-shell.js?v=20261016-browser-language-1"></script></head><body class="draft-preview selection-preview robus-selection-page robu-published-article"><main class="draft-main" data-contact-page><article><div class="robu-selection-label">Robu's Selection</div><div class="selection-subcategory" data-article-category>${esc(category)}</div><div class="article-content">${content(lang)}</div></article></main><script src="/assets/js/contact-feedback.js?v=20260907-1"></script></body></html>`;
}

const metadata = { ja: frontmatter(path.join(DRAFT, 'article.md')), en: frontmatter(path.join(DRAFT, 'article-en.md')) };
for (const lang of ['ja', 'en']) write(path.join(ROOT, ...(lang === 'ja' ? [] : ['en']), 'articles', SLUG, 'index.html'), page(lang));
const imageDir = path.join(ROOT, 'assets', 'images', 'articles', SLUG);
fs.mkdirSync(imageDir, { recursive: true });
for (const image of IMAGES) fs.copyFileSync(path.join(DRAFT, image), path.join(imageDir, image));

const id = `${SLUG}-${DATE}`;
const indexPath = path.join(ROOT, 'index.html');
let index = read(indexPath);
if (!index.includes(id)) {
  const card = {
    id, date: DATE, dateLabel: '2026.11.22', category: "Robu's Selection / 美容家電",
    title: metadata.ja.title, digestTitle: 'プロ仕様の切れ味を、自宅のセルフカットへ',
    digestLead: '日本製刃、約9,800ストローク/分、39段階ダイヤル、防水設計。ER-SC6Aの魅力を7項目で紹介します。',
    excerpt: metadata.ja.description, enTitle: metadata.en.title, enExcerpt: metadata.en.description,
    image: `assets/images/articles/${SLUG}/${IMAGES[0]}`, url: `/articles/${SLUG}/`,
    imageAlt: 'Panasonic ER-SC6A-Sの形状と配色を参考にしたAI生成の編集用画像',
  };
  index = index.replace('const articles = [', `const articles = [\n      ${JSON.stringify(card)},`);
  index = index.replace('const articleFilters = {', `const articleFilters = {\n      '${id}': ['selection'],`);
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
  const items = `<ul><li><a href="/articles/${SLUG}/">${esc(metadata.ja.title)}</a></li><li><a href="/en/articles/${SLUG}/">${esc(metadata.en.title)}</a></li></ul>`;
  write(htmlSitemapPath, htmlSitemap.replace("<h2>Robu's Selection</h2>", `<h2>Robu's Selection</h2>${items}`));
}

write(path.join(ROOT, 'records', '2026', '11', '2026-11-22-panasonic-er-sc6a-publication.md'), `# Panasonic ER-SC6A記事 公開記録

- 公開日: 2026-11-22
- 公開承認: ユーザーの明示承認
- 分類: Robu's Selection / 美容家電
- 日本語・英語: ユーザー確認済みの修正版
- 画像: 公式商品写真で形状と配色を確認して制作したAI生成の編集用画像2枚。本文中に明記
- アフィリエイト: Amazon、楽天市場、Yahoo!ショッピングのER-SC6A-S販売・検索導線と広告開示を掲載
- SNS: いつもの公開ルールにより、本記事のみ投稿対象として公開メタデータを有効化
`);

for (const file of [indexPath, sitemapPath, htmlSitemapPath]) write(file, read(file));
console.log('Published Panasonic ER-SC6A production files');
