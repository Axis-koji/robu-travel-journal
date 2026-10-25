param([string]$RepoRoot = (Split-Path -Parent $PSScriptRoot))

$ErrorActionPreference = 'Stop'
$draft = 'E:\Documents\Codex\2026-08-01\robuse-selection-drafts\Draft\2026-10-25\2026-10-25-01-robu-kininaru-yodogawa-fireworks-2026'
$slug = 'naniwa-yodogawa-fireworks-2026-exciting-seat'
$publishedDate = '2026-10-25'
$categoryJa = 'ろぶーの気になる事 / 旅行 / 花火大会'
$categoryEn = "Robu's Curiosities / Travel / Fireworks Festival"
$baseUrl = 'https://www.axis-jp.net'
$hero = 'IMG_20261017_191305.jpg'
$assets = @(
  'img-exciting-01.jpg', 'img-exciting-map.png', 'IMG_20261017_163913.jpg',
  'IMG_20261017_164209.jpg', 'IMG_20261017_191305.jpg', 'IMG_20261017_191307.jpg',
  'yodogawa-fireworks-highlight-poster.jpg', 'yodogawa-fireworks-finale-118s.mp4'
)
$sourceUrls = @(
  'https://www.yodohanabi.com/gaiyou.html',
  'https://www.yodohanabi.com/sale.html',
  'https://www.yodohanabi.com/program.html',
  'https://www.yodohanabi.com/faq.html'
)

function Escape-Html([string]$value) { [System.Net.WebUtility]::HtmlEncode($value) }

function Read-Article([string]$path) {
  $raw = Get-Content -Raw -LiteralPath $path -Encoding utf8
  if ($raw -notmatch '(?s)^---\s*\r?\n(.*?)\r?\n---\s*\r?\n(.*)$') { throw "Front matter not found: $path" }
  $front = $matches[1]
  $body = $matches[2]
  $title = [regex]::Match($front, '(?m)^title:\s*"([^"]+)"\s*$').Groups[1].Value
  $description = [regex]::Match($front, '(?m)^description:\s*"([^"]+)"\s*$').Groups[1].Value
  if (-not $title -or -not $description) { throw "Title or description missing: $path" }
  [pscustomobject]@{ Title=$title; Description=$description; Body=$body }
}

function Build-Page([string]$language) {
  $sourceName = if ($language -eq 'ja') { 'article.md' } else { 'article-en.md' }
  $article = Read-Article (Join-Path $draft $sourceName)
  $html = (ConvertFrom-Markdown -InputObject $article.Body).Html
  $html = [regex]::Replace($html, '(?s)^\s*<h1[^>]*>.*?</h1>\s*', '')
  foreach ($asset in $assets) {
    $html = $html.Replace('src="' + $asset + '"', 'src="/assets/images/articles/' + $slug + '/' + $asset + '"')
  }
  $html = [regex]::Replace($html, '<a href="(https?://[^"]+)">', '<a href="$1" target="_blank" rel="noopener noreferrer">')
  if ($html -notmatch 'yodogawa-fireworks-finale-118s\.mp4') { throw "Final video missing from $language output" }
  if ($html -match '撮影：ろぶー|Photo:\s*Robu') { throw "Removed photographer credit returned in $language output" }
  if ($html -notmatch 'data-purchase-disclosure') { throw "Affiliate disclosure missing from $language output" }

  $prefix = if ($language -eq 'ja') { '' } else { 'en/' }
  $category = if ($language -eq 'ja') { $categoryJa } else { $categoryEn }
  $canonical = "$baseUrl/$($prefix)articles/$slug/"
  $heroUrl = "$baseUrl/assets/images/articles/$slug/$hero"
  $locale = if ($language -eq 'ja') { 'ja_JP' } else { 'en_US' }
  $schema = [ordered]@{
    '@context'='https://schema.org'; '@type'='BlogPosting'; headline=$article.Title; description=$article.Description
    datePublished=$publishedDate; dateModified=$publishedDate; inLanguage=$(if ($language -eq 'ja') { 'ja-JP' } else { 'en' })
    mainEntityOfPage=[ordered]@{'@type'='WebPage';'@id'=$canonical}; image=@($heroUrl); articleSection=$category
    citation=$sourceUrls; isAccessibleForFree=$true
    author=[ordered]@{'@type'='Person';name='ろぶー'}
    publisher=[ordered]@{'@type'='Organization';name='ろぶーの気になる事';url="$baseUrl/"}
  } | ConvertTo-Json -Compress -Depth 7

  $page = @"
<!doctype html><html lang="$language" translate="no"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="google" content="notranslate"><meta name="robots" content="index,follow,max-image-preview:large"><meta name="referrer" content="strict-origin-when-cross-origin"><meta name="social:publish" content="true"><meta name="social:ai-image" content="false"><meta name="social:disclosure" content="This article contains an affiliate link to Ticket Pia.">
<title>$(Escape-Html $article.Title)</title><meta name="description" content="$(Escape-Html $article.Description)">
<link rel="canonical" href="$canonical"><link rel="alternate" hreflang="ja" href="$baseUrl/articles/$slug/"><link rel="alternate" hreflang="en" href="$baseUrl/en/articles/$slug/"><link rel="alternate" hreflang="x-default" href="$baseUrl/articles/$slug/">
<meta property="og:type" content="article"><meta property="og:locale" content="$locale"><meta property="og:site_name" content="ろぶーの気になる事"><meta property="og:title" content="$(Escape-Html $article.Title)"><meta property="og:description" content="$(Escape-Html $article.Description)"><meta property="og:url" content="$canonical"><meta property="og:image" content="$heroUrl"><meta property="og:image:alt" content="$(Escape-Html $article.Title)"><meta property="article:section" content="$(Escape-Html $category)"><meta property="article:published_time" content="${publishedDate}T00:00:00+09:00"><meta property="article:modified_time" content="${publishedDate}T00:00:00+09:00">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="$(Escape-Html $article.Title)"><meta name="twitter:description" content="$(Escape-Html $article.Description)"><meta name="twitter:image" content="$heroUrl">
<link rel="stylesheet" href="/assets/css/contact-feedback-ees-standard.css?v=3" data-contact-feedback-style><link rel="stylesheet" href="/assets/css/draft-article-preview.css?v=20261025-yodogawa-1"><style>.article-content img{display:block;max-width:100%;height:auto;margin-inline:auto;border-radius:10px}.article-content video{display:block;width:100%;max-width:720px;height:auto;margin:1.25rem auto;border-radius:12px;background:#000}.article-content table{display:block;max-width:100%;overflow-x:auto;border-collapse:collapse}.article-content th,.article-content td{padding:.65rem;border:1px solid rgba(180,190,200,.35);vertical-align:top}.purchase-panel{background:transparent!important;box-shadow:none!important;margin:2rem 0}.purchase-buttons{display:flex;flex-wrap:wrap;gap:.75rem;margin:1rem 0}.purchase-button{display:inline-flex;align-items:center;justify-content:center;padding:.75rem 1rem;border:1px solid #ad9162;border-radius:8px;background:#080b10;color:#f7efdc!important;text-decoration:none;font-weight:800}.purchase-note,.disclosure{font-size:.9rem;color:#5f6d70}</style><script type="application/ld+json">$schema</script><script defer src="/assets/js/shared-shell.js?v=20261025-related-contact-2"></script>
</head><body class="draft-preview robu-published-article robu-regular-article-page"><main class="draft-main" data-contact-page><article><div class="selection-subcategory" data-article-category>$(Escape-Html $category)</div><h1 class="article-title">$(Escape-Html $article.Title)</h1><div class="article-content">$html</div></article></main><script src="/assets/js/contact-feedback.js?v=20260907-1"></script></body></html>
"@
  $target = Join-Path $RepoRoot ($prefix + 'articles\' + $slug + '\index.html')
  New-Item -ItemType Directory -Force -Path (Split-Path $target -Parent) | Out-Null
  [IO.File]::WriteAllText($target, $page, [Text.UTF8Encoding]::new($false))
  return $article
}

$ja = Build-Page 'ja'
$en = Build-Page 'en'

$assetTarget = Join-Path $RepoRoot ('assets\images\articles\' + $slug)
New-Item -ItemType Directory -Force -Path $assetTarget | Out-Null
foreach ($asset in $assets) { Copy-Item -LiteralPath (Join-Path $draft $asset) -Destination (Join-Path $assetTarget $asset) -Force }

$articleId = "$slug-$publishedDate"
$indexPath = Join-Path $RepoRoot 'index.html'
$index = Get-Content -Raw -LiteralPath $indexPath -Encoding utf8
if ($index -notmatch [regex]::Escape($articleId)) {
  $card = [ordered]@{ id=$articleId; date=$publishedDate; dateLabel='2026.10.25'; category=$categoryJa; title=$ja.Title; digestTitle='エキサイティングシートで体感した淀川の花火'; digestLead='協賛席6タイプ、会場図、本人撮影の写真と約2分の映像で紹介します。'; excerpt=$ja.Description; enTitle=$en.Title; enExcerpt=$en.Description; image="assets/images/articles/$slug/$hero"; url="/articles/$slug/"; imageAlt='エキサイティングシートの観客席越しに夜空へ広がるなにわ淀川花火大会の花火' } | ConvertTo-Json -Compress
  $index = [regex]::Replace($index, 'const articles = \[', "const articles = [`r`n      $card,", 1)
  $index = [regex]::Replace($index, 'const articleFilters = \{', "const articleFilters = {`r`n      '$articleId': ['travel'],", 1)
  [IO.File]::WriteAllText($indexPath, $index, [Text.UTF8Encoding]::new($false))
}

$sitemapPath = Join-Path $RepoRoot 'sitemap.xml'
$sitemap = Get-Content -Raw -LiteralPath $sitemapPath -Encoding utf8
foreach ($prefix in @('', 'en/')) {
  $url = "$baseUrl/$($prefix)articles/$slug/"
  if ($sitemap -notmatch [regex]::Escape($url)) { $sitemap = $sitemap.Replace('</urlset>', "  <url><loc>$url</loc><lastmod>$publishedDate</lastmod></url>`r`n</urlset>") }
}
[IO.File]::WriteAllText($sitemapPath, $sitemap, [Text.UTF8Encoding]::new($false))

$htmlSitemapPath = Join-Path $RepoRoot 'sitemap\index.html'
$htmlSitemap = Get-Content -Raw -LiteralPath $htmlSitemapPath -Encoding utf8
if ($htmlSitemap -notmatch [regex]::Escape("/articles/$slug/")) {
  $links = '<li><a href="/articles/' + $slug + '/">' + (Escape-Html $ja.Title) + '</a></li><li><a href="/en/articles/' + $slug + '/">' + (Escape-Html $en.Title) + '</a></li>'
  $anchor = '<li><a href="/articles/suito-kurawanka-fireworks-2026-report/">水都くらわんか花火大会2026｜4,877発とドローンショー</a></li>'
  $htmlSitemap = $htmlSitemap.Replace($anchor, $links + $anchor)
  [IO.File]::WriteAllText($htmlSitemapPath, $htmlSitemap, [Text.UTF8Encoding]::new($false))
}

$recordPath = Join-Path $RepoRoot 'records\2026\10\2026-10-25-naniwa-yodogawa-fireworks-publication.md'
$record = @"
# なにわ淀川花火大会2026記事 公開記録

- 公開承認: 2026-10-25、ユーザーの明示承認
- 分類: $categoryJa
- 日本語・英語: 承認済み原稿をそのまま使用
- 本人撮影素材: 写真、会場図、約1分58秒の花火映像
- 映像: 自動再生なし、metadataのみ先読み、poster設定
- 座席比較: 6タイプ、価格を除いて形式と特徴を掲載
- 広告表示: チケットぴあの注意書き後に通常テキストで表示
- SNS: 本記事のみ投稿する明示承認あり
- 公開URL: $baseUrl/articles/$slug/
"@
New-Item -ItemType Directory -Force -Path (Split-Path $recordPath -Parent) | Out-Null
[IO.File]::WriteAllText($recordPath, $record, [Text.UTF8Encoding]::new($false))

Write-Output 'Built the approved bilingual Yodogawa fireworks article, media, catalogue card, sitemaps, and publication record.'
