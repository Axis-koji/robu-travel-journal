import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const canonicalOrigin = 'https://www.axis-jp.net';
const errors = [];
const textExtensions = new Set(['.html', '.xml', '.txt', '.js', '.mjs', '.css']);
const ignoredDirectories = new Set(['.git', '.github', 'node_modules', 'scripts', 'wordpress-published']);

function walk(directory) {
  const files = [];
  for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
    if (entry.isDirectory() && ignoredDirectories.has(entry.name)) continue;
    const fullPath = path.join(directory, entry.name);
    if (entry.isDirectory()) files.push(...walk(fullPath));
    else files.push(fullPath);
  }
  return files;
}

function relative(file) {
  return path.relative(root, file).split(path.sep).join('/');
}

const cname = fs.readFileSync(path.join(root, 'CNAME'), 'utf8').trim();
if (cname !== 'www.axis-jp.net') {
  errors.push(`CNAME must be exactly www.axis-jp.net (found: ${cname || '(empty)'})`);
}

const publicFiles = walk(root).filter((file) => textExtensions.has(path.extname(file).toLowerCase()));
for (const file of publicFiles) {
  const source = fs.readFileSync(file, 'utf8');
  if (/https?:\/\/axis-jp\.net(?=[/:?#\s"'])/i.test(source)) {
    errors.push(`${relative(file)} contains a non-www absolute URL`);
  }
}

const indexFiles = publicFiles.filter((file) => path.basename(file).toLowerCase() === 'index.html');
for (const file of indexFiles) {
  const source = fs.readFileSync(file, 'utf8');
  const canonical = source.match(/<link\s+rel=["']canonical["']\s+href=["']([^"']+)["']/i)?.[1];
  if (!canonical) {
    errors.push(`${relative(file)} is missing rel=canonical`);
  } else if (!canonical.startsWith(`${canonicalOrigin}/`) && canonical !== `${canonicalOrigin}/`) {
    errors.push(`${relative(file)} has a canonical URL outside ${canonicalOrigin}: ${canonical}`);
  }

  const ogUrl = source.match(/<meta\s+property=["']og:url["']\s+content=["']([^"']+)["']/i)?.[1];
  if (ogUrl && !ogUrl.startsWith(`${canonicalOrigin}/`) && ogUrl !== `${canonicalOrigin}/`) {
    errors.push(`${relative(file)} has an og:url outside ${canonicalOrigin}: ${ogUrl}`);
  }
}

const sitemap = fs.readFileSync(path.join(root, 'sitemap.xml'), 'utf8');
const sitemapUrls = [...sitemap.matchAll(/<loc>([^<]+)<\/loc>/gi)].map((match) => match[1].trim());
if (sitemapUrls.length === 0) errors.push('sitemap.xml contains no <loc> entries');
for (const url of sitemapUrls) {
  if (!url.startsWith(`${canonicalOrigin}/`) && url !== `${canonicalOrigin}/`) {
    errors.push(`sitemap.xml contains a URL outside ${canonicalOrigin}: ${url}`);
  }
}

const robots = fs.readFileSync(path.join(root, 'robots.txt'), 'utf8');
if (!robots.includes(`Sitemap: ${canonicalOrigin}/sitemap.xml`)) {
  errors.push(`robots.txt must reference ${canonicalOrigin}/sitemap.xml`);
}

if (errors.length) {
  console.error('www canonical-domain check failed:');
  for (const error of errors) console.error(`- ${error}`);
  process.exit(1);
}

console.log(`www canonical-domain check passed for ${indexFiles.length} index pages and ${sitemapUrls.length} sitemap URLs.`);
