param([string]$RepoRoot = (Split-Path -Parent $PSScriptRoot))

$ErrorActionPreference = 'Stop'
$draftDir = 'E:\Documents\Codex\2026-08-01\robuse-selection-drafts\Draft\2026-10-03\2026-10-03-02-robus-selection-plarail-air-ana-v1'
$slug = 'plarail-air-ana-passenger-plane-set'
$publishDate = '2026-10-04'
$titleJa = 'プラレールエアー ANA旅客機セットは買い？離着陸と旋回ギミックを解説'
$titleEn = 'Is the Plarail Air ANA Passenger Plane Set Worth ¥8,800? Takeoff and Banking Explained'
$descriptionJa = 'プラレールエアー ANA旅客機セットの価格、車輪収納、カーブでの旋回、専用レール、アジア版との違いを公式情報で確認します。'
$descriptionEn = 'An official-source guide to the Plarail Air ANA set: price, wheel retraction, banking motion, specialized track and the separate red Asian edition.'
$categoryJa = "Robu's Selection / おもちゃ"
$categoryEn = "Robu's Selection / Toys"
$hero = 'plarail-air-banking-balanced-review-candidate-v4.png'
$images = @($hero, 'plarail-air-gear-retraction-logo-free-v4.png')

function Escape-Html([string]$value) { [System.Net.WebUtility]::HtmlEncode($value) }

function Read-Body([string]$path) {
  $raw = Get-Content -Raw -LiteralPath $path -Encoding utf8
  if ($raw -notmatch '(?s)^---\s*\r?\n.*?\r?\n---\s*\r?\n(.*)$') { throw "Missing front matter: $path" }
  $body = $matches[1]
  $body = [regex]::Replace($body, '(?m)^> (?:公開前メモ|Pre-publication note)[：:].*(?:\r?\n)?', '')
  $body = $body.Replace("## Robu's conclusion", "## Robu's Take").Replace("## Robu's verdict", "## Robu's Take")
  return $body
}

function Source-Section([string]$language) {
  $sources = @(
    @('Takara Tomy product release (2026-08-19)', 'https://www.takaratomy.co.jp/release/product/2026/16119.html'),
    @('Takara Tomy official product feature page', 'https://www.takaratomy.co.jp/products/plarail/tettei/set/plarailair_ana/'),
    @('Takara Tomy Plarail October 2026 new-products page', 'https://www.takaratomy.co.jp/products/plarail/new/2610.htm'),
    @('Takara Tomy official instruction-manual portal', 'https://www.takaratomy.co.jp/support/manual/')
  )
  $items = for ($i = 0; $i -lt $sources.Count; $i++) {
    '<li id="source-' + ($i + 1) + '"><a href="' + $sources[$i][1] + '" target="_blank" rel="noopener noreferrer">' + (Escape-Html $sources[$i][0]) + '</a></li>'
  }
  $heading = if ($language -eq 'ja') { '主な一次・公式情報' } else { 'Primary and official sources' }
  return '<section class="robu-sources"><h2>' + (Escape-Html $heading) + '</h2><ol>' + ($items -join '') + '</ol></section>'
}

function Purchase-Section([string]$language) {
  $query = [uri]::EscapeDataString('プラレールエアー ANA旅客機セット')
  $amazon = 'https://www.amazon.co.jp/s?k=' + $query + '&tag=womaster-22'
  $rakutenTarget = 'https://search.rakuten.co.jp/search/mall/' + $query + '/'
  $rakuten = 'https://hb.afl.rakuten.co.jp/ichiba/573b428c.29ab7cd1.573b428d.a8ea33bd/?pc=' + [uri]::EscapeDataString($rakutenTarget) + '&link_type=text'
  $yahooTarget = 'https://shopping.yahoo.co.jp/search?p=' + $query
  $yahoo = 'https://ck.jp.ap.valuecommerce.com/servlet/referral?sid=3447653&pid=892705892&vc_url=' + [uri]::EscapeDataString($yahooTarget)
  if ($language -eq 'ja') {
    $heading = '購入先を確認する'
    $disclosure = '以下はアフィリエイトリンクです。当サイトに報酬が発生する場合があります。価格、在庫、販売元、ANA版か赤色アジア版かを購入前に確認してください。'
    $labels = @('Amazonで商品名を確認する', '楽天市場で商品名を確認する', 'Yahoo!ショッピングで商品名を確認する')
    $internal = '<p class="purchase-note">オンライン購入時は販売元とURLも確認してください。詳しくは<a href="/articles/ai-recommendation-link-safety/">AIのおすすめリンクは安全？</a>で整理しています。</p>'
  } else {
    $heading = 'Check current sellers'
    $disclosure = 'These are affiliate links. We may earn a commission. Check the current seller, price, stock, and whether the listing is the Japanese ANA edition or the separate red Asian edition.'
    $labels = @('Search Amazon Japan', 'Search Rakuten', 'Search Yahoo! Shopping Japan')
    $internal = '<p class="purchase-note">Check the seller and destination URL before ordering. Our <a href="/en/articles/ai-recommendation-link-safety/">guide to AI-recommended links</a> explains the basic checks.</p>'
  }
  $urls = @($amazon, $rakuten, $yahoo)
  $classes = @('amazon', 'rakuten', 'yahoo')
  $buttons = for ($i = 0; $i -lt 3; $i++) {
    '<a class="robu-marketplace-button ' + $classes[$i] + '" href="' + (Escape-Html $urls[$i]) + '" target="_blank" rel="nofollow sponsored noopener noreferrer">' + (Escape-Html $labels[$i]) + '</a>'
  }
  return '<section class="robu-marketplace-section" data-selection-purchase-standard="astron-hab005j"><h2>' + (Escape-Html $heading) + '</h2><p class="note" data-purchase-disclosure>' + (Escape-Html $disclosure) + '</p><div class="robu-marketplace-buttons">' + ($buttons -join '') + '</div>' + $internal + '</section>'
}

function Build-Page([string]$language) {
  $source = Join-Path $draftDir $(if ($language -eq 'ja') { 'article.md' } else { 'article-en.md' })
  $html = (ConvertFrom-Markdown -InputObject (Read-Body $source)).Html
  $html = [regex]::Replace($html, '(?s)^\s*<h1[^>]*>.*?</h1>\s*', '')
  foreach ($image in $images) {
    $sourceImage = Join-Path $draftDir $image
    if (-not (Test-Path -LiteralPath $sourceImage)) { throw "Missing image: $sourceImage" }
    $assetDir = Join-Path $RepoRoot ('assets\images\articles\' + $slug)
    New-Item -ItemType Directory -Force -Path $assetDir | Out-Null
    Copy-Item -LiteralPath $sourceImage -Destination (Join-Path $assetDir $image) -Force
    $html = $html.Replace('src="' + $image + '"', 'src="/assets/images/articles/' + $slug + '/' + $image + '"')
  }
  $html = [regex]::Replace($html, '(?<![A-Za-z])\[([1-4])\]', '<a class="source-ref" href="#source-$1">[$1]</a>')
  $html += (Purchase-Section $language)
  $html += (Source-Section $language)

  $title = if ($language -eq 'ja') { $titleJa } else { $titleEn }
  $description = if ($language -eq 'ja') { $descriptionJa } else { $descriptionEn }
  $category = if ($language -eq 'ja') { $categoryJa } else { $categoryEn }
  $path = if ($language -eq 'ja') { 'articles/' } else { 'en/articles/' }
  $canonical = 'https://www.axis-jp.net/' + $path + $slug + '/'
  $jaUrl = 'https://www.axis-jp.net/articles/' + $slug + '/'
  $enUrl = 'https://www.axis-jp.net/en/articles/' + $slug + '/'
  $imageUrls = @($images | ForEach-Object { 'https://www.axis-jp.net/assets/images/articles/' + $slug + '/' + $_ })
  $schema = [ordered]@{
    '@context'='https://schema.org'; '@type'='Article'; headline=$title; description=$description
    datePublished=$publishDate; dateModified=$publishDate; inLanguage=$(if ($language -eq 'ja') { 'ja-JP' } else { 'en' })
    mainEntityOfPage=[ordered]@{'@type'='WebPage';'@id'=$canonical}; image=$imageUrls; articleSection=$category
    author=[ordered]@{'@type'='Organization';name='ろぶーの気になる事'}
    publisher=[ordered]@{'@type'='Organization';name='ろぶーの気になる事';url='https://www.axis-jp.net/'}
    isAccessibleForFree=$true
  } | ConvertTo-Json -Compress -Depth 6
  $locale = if ($language -eq 'ja') { 'ja_JP' } else { 'en_US' }
  $imageAlt = if ($language -eq 'ja') { '青い曲線レール上で約50度の自然なバンク旋回をする旅客機玩具のAI生成イメージ' } else { 'AI-generated image of a toy passenger plane banking on a curved blue rail' }
  $page = @"
<!doctype html>
<html lang="$language" translate="no"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="google" content="notranslate"><meta name="social:publish" content="true">
<meta name="referrer" content="strict-origin-when-cross-origin"><meta name="robots" content="index,follow,max-image-preview:large">
<title>$(Escape-Html $title)</title><meta name="description" content="$(Escape-Html $description)">
<link rel="canonical" href="$canonical">
<link rel="alternate" hreflang="ja" href="$jaUrl"><link rel="alternate" hreflang="en" href="$enUrl"><link rel="alternate" hreflang="x-default" href="$jaUrl">
<meta property="og:type" content="article"><meta property="og:locale" content="$locale"><meta property="og:site_name" content="ろぶーの気になる事">
<meta property="og:title" content="$(Escape-Html $title)"><meta property="og:description" content="$(Escape-Html $description)">
<meta property="og:url" content="$canonical"><meta property="og:image" content="$($imageUrls[0])"><meta property="og:image:alt" content="$(Escape-Html $imageAlt)">
<meta property="article:section" content="$(Escape-Html $category)"><meta property="article:published_time" content="${publishDate}T00:00:00+09:00"><meta property="article:modified_time" content="${publishDate}T00:00:00+09:00">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="$(Escape-Html $title)"><meta name="twitter:description" content="$(Escape-Html $description)"><meta name="twitter:image" content="$($imageUrls[0])">
<link rel="stylesheet" href="/assets/css/contact-feedback-ees-standard.css?v=3" data-contact-feedback-style>
<link rel="stylesheet" href="/assets/css/draft-article-preview.css?v=20260930-publish-five-1">
<style>.article-content img{display:block;max-width:100%;height:auto;margin-inline:auto}.article-content>p>em{display:block;font-size:.82rem;line-height:1.6;color:var(--robu-selection-muted,#b9b4a8)}.robu-marketplace-section h2{font-size:clamp(18px,2vw,22px)}.article-content table{display:block;max-width:100%;overflow-x:auto}</style>
<script type="application/ld+json">$schema</script>
<script defer src="/assets/js/shared-shell.js?v=20261003-desktop-left-toc-1"></script>
</head><body class="draft-preview robu-published-article robus-selection-page"><main class="draft-main" data-contact-page><article>
<div class="robu-selection-label">Robu's Selection</div>
<div class="selection-subcategory" data-article-category>$(Escape-Html $category)</div>
<h1 class="article-title">$(Escape-Html $title)</h1>
<div class="article-content">$html</div>
</article></main><script src="/assets/js/contact-feedback.js?v=20260907-1"></script></body></html>
"@
  $target = Join-Path $RepoRoot ($path.Replace('/', '\') + $slug)
  New-Item -ItemType Directory -Force -Path $target | Out-Null
  [IO.File]::WriteAllText((Join-Path $target 'index.html'), $page, [Text.UTF8Encoding]::new($false))
}

Build-Page 'ja'
Build-Page 'en'

$id = $slug + '-' + $publishDate
$indexPath = Join-Path $RepoRoot 'index.html'
$index = Get-Content -Raw -LiteralPath $indexPath -Encoding utf8
if (-not $index.Contains('"id":"' + $id + '"')) {
  $card = [ordered]@{
    id=$id; date=$publishDate; dateLabel='2026.10.04'; category=$categoryJa
    title=$titleJa; digestTitle=$titleJa; digestLead=$descriptionJa; excerpt=$descriptionJa
    enTitle=$titleEn; enExcerpt=$descriptionEn
    image='assets/images/articles/' + $slug + '/' + $hero
    url='/articles/' + $slug + '/'; imageAlt='青い曲線レール上で約50度の自然なバンク旋回をする旅客機玩具のAI生成イメージ'
  } | ConvertTo-Json -Compress -Depth 4
  $index = [regex]::Replace($index, 'const articles = \[', 'const articles = [' + "`n      " + $card + ',', 1)
  $index = [regex]::Replace($index, 'const articleFilters = \{', 'const articleFilters = {' + "`n      '" + $id + "': ['selection'],", 1)
  [IO.File]::WriteAllText($indexPath, $index, [Text.UTF8Encoding]::new($false))
}

$sitemapPath = Join-Path $RepoRoot 'sitemap.xml'
$sitemap = Get-Content -Raw -LiteralPath $sitemapPath -Encoding utf8
foreach ($path in @('articles/', 'en/articles/')) {
  $url = 'https://www.axis-jp.net/' + $path + $slug + '/'
  if (-not $sitemap.Contains($url)) {
    $sitemap = $sitemap.Replace('</urlset>', '  <url><loc>' + $url + '</loc><lastmod>' + $publishDate + "</lastmod></url>`n</urlset>")
  }
}
[IO.File]::WriteAllText($sitemapPath, $sitemap, [Text.UTF8Encoding]::new($false))

$sitemapHtmlPath = Join-Path $RepoRoot 'sitemap\index.html'
$sitemapHtml = Get-Content -Raw -LiteralPath $sitemapHtmlPath -Encoding utf8
$sitemapLink = '          <li><a href="/articles/' + $slug + '/">' + (Escape-Html $titleJa) + '</a></li>'
if (-not $sitemapHtml.Contains('/articles/' + $slug + '/')) {
  $sitemapHtml = $sitemapHtml.Replace('        <h2>Robu''s Selection</h2>' + "`r`n        <ul>", '        <h2>Robu''s Selection</h2>' + "`r`n        <ul>`r`n" + $sitemapLink)
  [IO.File]::WriteAllText($sitemapHtmlPath, $sitemapHtml, [Text.UTF8Encoding]::new($false))
}

$recordDir = Join-Path $RepoRoot 'records\2026\10'
New-Item -ItemType Directory -Force -Path $recordDir | Out-Null
$record = @"
# Owner-approved publication — Plarail Air ANA passenger plane set

- Publication date: 2026-10-04
- Category: Robu's Selection / おもちゃ
- User explicitly approved publication after reviewing the local article and image candidates.
- Japanese and English articles were checked against four Takara Tomy official sources; 14 claim-level checks passed.
- The article distinguishes the Japanese ANA edition from the planned red original edition for several Asian markets.
- Two original AI-generated editorial images are visibly labeled and are not presented as official product photographs.
- Marketplace links are search links with visible affiliate disclosure and do not assert stock or authorised-seller status.
- No SNS publication action was requested or performed.
"@
[IO.File]::WriteAllText((Join-Path $recordDir '2026-10-04-publish-plarail-air-ana-v1.md'), $record, [Text.UTF8Encoding]::new($false))

Write-Output 'Built bilingual Plarail article, two images, homepage card, category mapping, sitemaps, and publication record.'
