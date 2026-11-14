import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const DRAFT = 'E:\\Documents\\Codex\\2026-08-01\\robuse-selection-drafts\\Draft\\2026-11-14\\2026-11-14-extra-robu-kininaru-cosori-turboblaze-6l-v2';
const SLUG = 'cosori-turboblaze-6l-air-fryer';
const DATE = '2026-11-14';
const BASE = 'https://www.axis-jp.net';
const IMAGES = [
  'cosori-turboblaze-evening-kitchen-editorial-v1.png',
  'cosori-turboblaze-crispy-reheat-editorial-v1.png',
  'cosori-turboblaze-food-range-editorial-v1.png',
  'cosori-turboblaze-space-check-editorial-v1.png',
];
const OG_IMAGE = IMAGES[1];
const SOURCES = [
  'https://vesync.jp/products/cosori-turbo-blaze-6l-air-fryer',
  'https://vesync.jp/pages/cosori',
  'https://prtimes.jp/main/html/rd/p/000000044.000090820.html',
  'https://item.rakuten.co.jp/vesync/kaapafcsnjp0284y/',
  'https://vesync.jp/pages/recipes-turboblaze-fried-chicken',
  'https://vesync.jp/pages/recipes-turboblaze-spiced-steak',
  'https://vesync.jp/pages/recipes-turboblaze-beef-jerky',
  'https://vesync.jp/pages/recipes-turboblaze-homemade-fermented-butter',
  'https://vesync.jp/blogs/recipes/herb-and-fish-sauce-roast-pork-1',
  'https://vesync.jp/pages/recipe-dc-cheese-frittata',
  'https://ranking.rakuten.co.jp/daily/100644/',
  'https://ranking.rakuten.co.jp/weekly/100644/',
  'https://ranking.rakuten.co.jp/realtime/564331/',
  'https://www.env.go.jp/press/files/jp/17803.pdf',
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
  const hero = `${BASE}/assets/images/articles/${SLUG}/${OG_IMAGE}?v=20261114`;
  const locale = lang === 'ja' ? 'ja_JP' : 'en_US';
  const category = lang === 'ja'
    ? 'ろぶーの気になる事 / 家電・キッチン / 売れ筋チェック'
    : "Robu's Curiosities / Kitchen Appliances / Bestseller Check";
  const disclosure = lang === 'ja'
    ? '※記事内にはアフィリエイトリンクとAI生成の編集画像を含みます。'
    : 'This article includes affiliate links and AI-generated editorial images.';
  const schema = {
    '@context': 'https://schema.org',
    '@type': 'BlogPosting',
    headline: meta.title,
    description: meta.description,
    datePublished: DATE,
    dateModified: DATE,
    inLanguage: lang,
    mainEntityOfPage: url,
    image: IMAGES.map((name) => `${BASE}/assets/images/articles/${SLUG}/${name}`),
    isAccessibleForFree: true,
    author: { '@type': 'Person', name: 'ろぶー' },
    publisher: { '@type': 'Organization', name: 'ろぶーの気になる事', url: BASE },
    citation: SOURCES,
  };
  return `<!doctype html><html lang="${lang}" translate="no"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="google" content="notranslate"><meta name="robots" content="index,follow,max-image-preview:large"><meta name="referrer" content="strict-origin-when-cross-origin"><meta name="social:publish" content="false"><meta name="social:ai-image" content="true"><meta name="social:disclosure" content="${escapeHtml(disclosure)}">
<title>${escapeHtml(meta.seoTitle)}</title><meta name="description" content="${escapeHtml(meta.description)}"><link rel="canonical" href="${url}"><link rel="alternate" hreflang="ja" href="${BASE}/articles/${SLUG}/"><link rel="alternate" hreflang="en" href="${BASE}/en/articles/${SLUG}/"><link rel="alternate" hreflang="x-default" href="${BASE}/articles/${SLUG}/">
<meta property="og:type" content="article"><meta property="og:locale" content="${locale}"><meta property="og:site_name" content="ろぶーの気になる事"><meta property="og:title" content="${escapeHtml(meta.title)}"><meta property="og:description" content="${escapeHtml(meta.description)}"><meta property="og:url" content="${url}"><meta property="og:image" content="${hero}"><meta property="og:image:alt" content="${escapeHtml(meta.title)}"><meta property="article:section" content="${escapeHtml(category)}"><meta property="article:published_time" content="${DATE}T00:00:00+09:00"><meta property="article:modified_time" content="${DATE}T00:00:00+09:00"><meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="/assets/css/contact-feedback-ees-standard.css?v=3" data-contact-feedback-style><link rel="stylesheet" href="/assets/css/draft-article-preview.css?v=20260930-publish-five-1"><link rel="stylesheet" href="/assets/css/robus-selection-theme.css?v=20261025-standard-5" data-robu-selection-theme><style>.robu-article-layout>main.draft-main{max-width:820px}article{overflow-wrap:anywhere}.article-content img{display:block;max-width:100%;width:auto;height:auto;margin:auto;border-radius:10px}.article-content>p>em{display:block;font-size:.9rem;line-height:1.7}.article-content table{width:100%;border-collapse:collapse;margin:1.25rem 0;font-size:.95rem}.article-content th,.article-content td{border:1px solid #b7a98f;padding:.7rem .75rem;text-align:left;vertical-align:top}.article-content th{background:#f4ead7;font-weight:700}.article-content table+table{margin-top:1.75rem}@media(max-width:700px){.article-content{overflow-wrap:anywhere}.article-content table{display:block;overflow-x:auto;white-space:normal}.article-content th,.article-content td{min-width:8.5rem}}</style><script type="application/ld+json">${JSON.stringify(schema)}</script><script defer src="/assets/js/shared-shell.js?v=20261016-browser-language-1"></script></head><body class="draft-preview robu-regular-article-page robu-published-article"><main class="draft-main" data-contact-page><article><div class="robu-selection-label">${lang === 'ja' ? 'ろぶーの気になる事' : "Robu's Curiosities"}</div><div class="selection-subcategory" data-article-category>${escapeHtml(category)}</div><div class="article-content">${articleContent(lang)}</div></article></main><script src="/assets/js/contact-feedback.js?v=20260907-1"></script></body></html>`;
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
    id: articleId,
    date: DATE,
    dateLabel: '2026.11.14',
    category: 'ろぶーの気になる事 / 家電・キッチン / 売れ筋チェック',
    title: metadata.ja.title,
    digestTitle: '唐揚げも発酵も。COSORI 6Lと4.7Lを比べる',
    digestLead: '惣菜の温め直し、肉料理、朝食、発酵、ドライまで。使い道と容量、置き場所、電源を具体的に整理します。',
    excerpt: metadata.ja.description,
    enTitle: metadata.en.title,
    enExcerpt: metadata.en.description,
    image: `assets/images/articles/${SLUG}/${OG_IMAGE}`,
    url: `/articles/${SLUG}/`,
    imageAlt: '温め直した唐揚げや惣菜が食卓に並ぶ様子を表したAI生成の編集用イメージ',
  };
  index = index.replace('const articles = [', `const articles = [\n      ${JSON.stringify(card)},`);
  index = index.replace('const articleFilters = {', `const articleFilters = {\n      '${articleId}': [],`);
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

write(path.join(ROOT, 'records', '2026', '11', '2026-11-14-cosori-turboblaze-publication.md'), `# COSORI TurboBlaze 6L 比較記事 公開記録

- 公開承認: 2026-11-14、ユーザーの明示承認
- 分類: ろぶーの気になる事 / 家電・キッチン / 売れ筋チェック
- 日本語・英語: Claude執筆後、ユーザー読み合わせとChatGPT最終確認を反映したv2
- 画像: AI生成の編集用画像4枚。公式写真や実際の製品外観・調理結果ではない旨を本文中に明記
- アフィリエイト: Amazon、楽天市場、Yahoo!ショッピング。広告リンクであることを購入欄で明記
- ファクトチェック: COSORI・VeSync公式情報、公式楽天店、公式レシピ、楽天ランキング、環境省資料の14件
- SNS: 今回は記事公開のみ。SNS投稿は実行せず、公開メタデータも無効
`);

for (const generated of [indexPath, sitemapPath, htmlSitemapPath]) write(generated, read(generated));

console.log('Published COSORI production files');
