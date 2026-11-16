import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const DRAFT = 'E:\\Documents\\Codex\\2026-08-01\\robuse-selection-drafts\\Draft\\2026-11-09\\2026-11-09-02-robus-selection-yukyu-jinrou-v3';
const SLUG = 'yukyu-jinrou-tensei-oboro-nari';
const DATE = '2026-11-16';
const BASE = 'https://www.axis-jp.net';
const IMAGES = ['yukyu-jinrou-razor-craft-editorial-v4.png', 'yukyu-jinrou-product-front-rear-editorial-v4.png'];
const SOURCES = [
  'https://yamasei21.co.jp/news/3024/',
  'https://yukyujinrou.com/products/sen-001?variant=46595147104455',
  'https://yukyujinrou.com/collections/item-all',
  'https://yukyujinrou.com/products/blade-30?variant=46955277418695',
  'https://yukyujinrou.com/pages/faq',
  'https://yukyujinrou.com/blogs/journal/how-to-use',
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
  for (const image of IMAGES) body = body.replaceAll(`./${image}`, `/assets/images/articles/${SLUG}/${image}?v=20261116`);
  body = body
    .replaceAll('class="purchase-buttons"', 'class="official-purchase-buttons"')
    .replaceAll('class="purchase-button ', 'class="official-purchase-button ')
    .replaceAll(' data-purchase-disclosure', '');
  return body;
}

function page(lang) {
  const prefix = lang === 'ja' ? '' : 'en/';
  const meta = frontmatter(path.join(DRAFT, lang === 'ja' ? 'article.md' : 'article-en.md'));
  const url = `${BASE}/${prefix}articles/${SLUG}/`;
  const hero = `${BASE}/assets/images/articles/${SLUG}/${IMAGES[0]}?v=20261116`;
  const locale = lang === 'ja' ? 'ja_JP' : 'en_US';
  const category = lang === 'ja' ? "Robu's Selection / 日本のものづくり" : "Robu's Selection / Japanese Craft";
  const disclosure = lang === 'ja' ? '※記事内にはAI生成の編集画像を含みます。アフィリエイトリンクはありません。' : 'This article includes AI-generated editorial images and contains no affiliate links.';
  const schema = {
    '@context': 'https://schema.org', '@type': 'BlogPosting', headline: meta.title, description: meta.description,
    datePublished: DATE, dateModified: DATE, inLanguage: lang, mainEntityOfPage: url,
    image: IMAGES.map((n) => `${BASE}/assets/images/articles/${SLUG}/${n}`), isAccessibleForFree: true,
    author: { '@type': 'Person', name: 'ろぶー' }, publisher: { '@type': 'Organization', name: 'ろぶーの気になる事', url: BASE }, citation: SOURCES,
  };
  return `<!doctype html><html lang="${lang}" translate="no"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="google" content="notranslate"><meta name="robots" content="index,follow,max-image-preview:large"><meta name="referrer" content="strict-origin-when-cross-origin"><meta name="social:publish" content="false"><meta name="social:ai-image" content="true"><meta name="social:disclosure" content="${esc(disclosure)}">
<title>${esc(meta.seoTitle)}</title><meta name="description" content="${esc(meta.description)}"><link rel="canonical" href="${url}"><link rel="alternate" hreflang="ja" href="${BASE}/articles/${SLUG}/"><link rel="alternate" hreflang="en" href="${BASE}/en/articles/${SLUG}/"><link rel="alternate" hreflang="x-default" href="${BASE}/articles/${SLUG}/">
<meta property="og:type" content="article"><meta property="og:locale" content="${locale}"><meta property="og:site_name" content="ろぶーの気になる事"><meta property="og:title" content="${esc(meta.title)}"><meta property="og:description" content="${esc(meta.description)}"><meta property="og:url" content="${url}"><meta property="og:image" content="${hero}"><meta property="og:image:alt" content="${esc(meta.title)}"><meta property="article:section" content="${esc(category)}"><meta property="article:published_time" content="${DATE}T00:00:00+09:00"><meta property="article:modified_time" content="${DATE}T00:00:00+09:00"><meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="/assets/css/contact-feedback-ees-standard.css?v=3" data-contact-feedback-style><link rel="stylesheet" href="/assets/css/draft-article-preview.css?v=20260930-publish-five-1"><link rel="stylesheet" href="/assets/css/robus-selection-theme.css?v=20261025-standard-5" data-robu-selection-theme><style>.robu-article-layout>main.draft-main{max-width:820px}article{overflow-wrap:anywhere}.article-content img{display:block;max-width:100%;width:auto;height:auto;margin:auto;border-radius:10px}.article-content>p>em{display:block;font-size:.9rem;line-height:1.7}.official-purchase-buttons{display:flex;flex-wrap:wrap;gap:12px}.official-purchase-button{display:inline-flex;align-items:center;justify-content:center;min-height:48px;padding:10px 18px;border:1px solid #b88a44;border-radius:8px;text-decoration:none;font-weight:800}.official-purchase-button:hover{background:#d97706;color:#fff}.purchase-note{font-size:1rem;line-height:1.8}.disclosure{font-size:.88rem;line-height:1.7}</style><script type="application/ld+json">${JSON.stringify(schema)}</script><script defer src="/assets/js/shared-shell.js?v=20261016-browser-language-1"></script></head><body class="draft-preview selection-preview robus-selection-page robu-published-article"><main class="draft-main" data-contact-page><article><div class="robu-selection-label">Robu's Selection</div><div class="selection-subcategory" data-article-category>${esc(category)}</div><div class="article-content">${content(lang)}</div></article></main><script src="/assets/js/contact-feedback.js?v=20260907-1"></script></body></html>`;
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
    id, date: DATE, dateLabel: '2026.11.16', category: "Robu's Selection / 日本のものづくり",
    title: metadata.ja.title, digestTitle: '日本の技を手元に置く、悠久刃楼の両刃カミソリ',
    digestLead: '精密加工と伝統着色を重ねた「天青朧なり」。剃る時間まで美しくする一本を紹介します。',
    excerpt: metadata.ja.description, enTitle: metadata.en.title, enExcerpt: metadata.en.description,
    image: `assets/images/articles/${SLUG}/${IMAGES[0]}`, url: `/articles/${SLUG}/`,
    imageAlt: '悠久刃楼「天青朧なり」を公式写真に合わせて表現したAI生成の編集用画像',
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

write(path.join(ROOT, 'records', '2026', '11', '2026-11-16-yukyu-jinrou-publication.md'), `# 悠久刃楼「天青朧なり」記事 公開記録

- 公開日: 2026-11-16（ユーザー指定）
- 公開承認: ユーザーの明示承認
- 分類: Robu's Selection / 日本のものづくり
- 日本語・英語: ユーザー確認済みの第3版
- 画像: 公式商品写真を基準に形状と配色を合わせたAI生成の編集用画像2枚。本文中に明記
- アフィリエイト: 完全一致する案件なし。ユーザー指示によりアフィリエイトなしで公開
- 購入導線: 悠久刃楼の公式商品ページ、商品一覧、専用替刃
- SNS: 記事公開のみ。自動投稿は実行せず、公開メタデータも無効
`);

for (const file of [indexPath, sitemapPath, htmlSitemapPath]) write(file, read(file));
console.log('Published YUKYU JINROU production files');
