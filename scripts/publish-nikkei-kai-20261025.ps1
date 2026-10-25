param([string]$RepoRoot = (Split-Path -Parent $PSScriptRoot))

$ErrorActionPreference = 'Stop'
$draft = 'E:\Documents\Codex\2026-08-01\robuse-selection-drafts\Draft\2026-09-17\2026-09-17-02-robus-selection'
$slug = 'nikkei-kai-pr-media-analysis-agent'
$publishedDate = '2026-10-25'
$category = "Robu's Selection / AI・業務支援"
$baseUrl = 'https://www.axis-jp.net'
$imageNames = @('nikkei-kai-pr-analysis-hero.png', 'nikkei-kai-pr-analysis-workflow.png')
$sourceUrls = @('https://prtimes.jp/main/html/rd/p/000000660.000011115.html', 'https://nkbb.nikkei.co.jp/kai/')

function Escape-Html([string]$value) { [System.Net.WebUtility]::HtmlEncode($value) }

function Read-Article([string]$path) {
  $raw = Get-Content -Raw -LiteralPath $path -Encoding utf8
  if ($raw -notmatch '(?s)^---\s*\r?\n(.*?)\r?\n---\s*\r?\n(.*)$') { throw "Front matter not found: $path" }
  $front = $matches[1]
  $body = $matches[2]
  $title = [regex]::Match($front, '(?m)^title:\s*"([^"]+)"\s*$').Groups[1].Value
  $description = [regex]::Match($front, '(?m)^description:\s*"([^"]+)"\s*$').Groups[1].Value
  [pscustomobject]@{ Title=$title; Description=$description; Body=$body }
}

function Build-Page([string]$language) {
  $sourceName = if ($language -eq 'ja') { 'article.md' } else { 'article-en.md' }
  $article = Read-Article (Join-Path $draft $sourceName)
  $html = (ConvertFrom-Markdown -InputObject $article.Body).Html
  $html = [regex]::Replace($html, '(?s)^\s*<h1[^>]*>.*?</h1>\s*', '')
  foreach ($imageName in $imageNames) {
    $html = $html.Replace('src="./' + $imageName + '"', 'src="/assets/images/articles/' + $slug + '/' + $imageName + '"')
  }
  $html = [regex]::Replace($html, '<a href="(https?://[^"]+)">', '<a href="$1" target="_blank" rel="noopener noreferrer">')

  $prefix = if ($language -eq 'ja') { '' } else { 'en/' }
  $canonical = "$baseUrl/$($prefix)articles/$slug/"
  $hero = "$baseUrl/assets/images/articles/$slug/$($imageNames[0])"
  $locale = if ($language -eq 'ja') { 'ja_JP' } else { 'en_US' }
  $schema = [ordered]@{
    '@context'='https://schema.org'; '@type'='Article'; headline=$article.Title; description=$article.Description
    datePublished=$publishedDate; dateModified=$publishedDate; inLanguage=$language; mainEntityOfPage=$canonical
    image=@($hero); articleSection=$category; citation=$sourceUrls
    author=[ordered]@{'@type'='Person';name='ろぶー'}
    publisher=[ordered]@{'@type'='Organization';name='ろぶーの気になる事';url="$baseUrl/"}
  } | ConvertTo-Json -Compress -Depth 6

  $page = @"
<!doctype html><html lang="$language" translate="no"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="google" content="notranslate"><meta name="robots" content="index,follow,max-image-preview:large"><meta name="social:publish" content="false"><meta name="social:ai-image" content="true">
<title>$(Escape-Html $article.Title)</title><meta name="description" content="$(Escape-Html $article.Description)">
<link rel="canonical" href="$canonical"><link rel="alternate" hreflang="ja" href="$baseUrl/articles/$slug/"><link rel="alternate" hreflang="en" href="$baseUrl/en/articles/$slug/"><link rel="alternate" hreflang="x-default" href="$baseUrl/articles/$slug/">
<meta property="og:type" content="article"><meta property="og:locale" content="$locale"><meta property="og:site_name" content="ろぶーの気になる事"><meta property="og:title" content="$(Escape-Html $article.Title)"><meta property="og:description" content="$(Escape-Html $article.Description)"><meta property="og:url" content="$canonical"><meta property="og:image" content="$hero"><meta property="article:section" content="$(Escape-Html $category)"><meta property="article:published_time" content="2026-10-25T00:00:00+09:00"><meta property="article:modified_time" content="2026-10-25T00:00:00+09:00">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="$(Escape-Html $article.Title)"><meta name="twitter:description" content="$(Escape-Html $article.Description)"><meta name="twitter:image" content="$hero">
<link rel="stylesheet" href="/assets/css/draft-article-preview.css?v=20261025-nikkei-kai-1"><script type="application/ld+json">$schema</script><script defer src="/assets/js/shared-shell.js?v=20261025-purchase-order-1"></script>
</head><body class="draft-preview robus-selection-page robu-published-article"><main class="draft-main"><article><div class="robu-selection-label">Robu&apos;s Selection</div><div class="selection-subcategory" data-article-category>$(Escape-Html $category)</div><h1 class="article-title">$(Escape-Html $article.Title)</h1><div class="article-content">$html</div></article></main></body></html>
"@
  $target = Join-Path $RepoRoot ($prefix + 'articles\' + $slug + '\index.html')
  New-Item -ItemType Directory -Force -Path (Split-Path $target -Parent) | Out-Null
  [IO.File]::WriteAllText($target, $page, [Text.UTF8Encoding]::new($false))
  return $article
}

$ja = Build-Page 'ja'
$en = Build-Page 'en'

$imageTarget = Join-Path $RepoRoot ('assets\images\articles\' + $slug)
New-Item -ItemType Directory -Force -Path $imageTarget | Out-Null
foreach ($imageName in $imageNames) { Copy-Item -LiteralPath (Join-Path $draft $imageName) -Destination (Join-Path $imageTarget $imageName) -Force }

$articleId = "$slug-$publishedDate"
$indexPath = Join-Path $RepoRoot 'index.html'
$index = Get-Content -Raw -LiteralPath $indexPath -Encoding utf8
if ($index -notmatch [regex]::Escape($articleId)) {
  $card = [ordered]@{ id=$articleId; date=$publishedDate; dateLabel='2026.10.25'; category=$category; title=$ja.Title; digestTitle='NIKKEI KAIの報道分析Agentを確認'; digestLead='機能、向く企業、導入前の確認点を公式情報から整理します。'; excerpt=$ja.Description; enTitle=$en.Title; enExcerpt=$en.Description; image="assets/images/articles/$slug/$($imageNames[0])"; url="/articles/$slug/"; imageAlt='広報担当者が報道件数やテーマ別の傾向を分析するAI生成イメージ' } | ConvertTo-Json -Compress
  $index = $index.Replace('const articles = [', "const articles = [`r`n      $card,", [StringComparison]::Ordinal)
  $index = $index.Replace('const articleFilters = {', "const articleFilters = {`r`n      '$articleId': ['selection'],", [StringComparison]::Ordinal)
  [IO.File]::WriteAllText($indexPath, $index, [Text.UTF8Encoding]::new($false))
}

$sitemapPath = Join-Path $RepoRoot 'sitemap.xml'
$sitemap = Get-Content -Raw -LiteralPath $sitemapPath -Encoding utf8
foreach ($prefix in @('', 'en/')) {
  $url = "$baseUrl/$($prefix)articles/$slug/"
  if ($sitemap -notmatch [regex]::Escape($url)) { $sitemap = $sitemap.Replace('</urlset>', "<url><loc>$url</loc><lastmod>$publishedDate</lastmod></url>`r`n</urlset>") }
}
[IO.File]::WriteAllText($sitemapPath, $sitemap, [Text.UTF8Encoding]::new($false))

$htmlSitemapPath = Join-Path $RepoRoot 'sitemap\index.html'
$htmlSitemap = Get-Content -Raw -LiteralPath $htmlSitemapPath -Encoding utf8
if ($htmlSitemap -notmatch [regex]::Escape("/articles/$slug/")) {
  $links = '<ul><li><a href="/articles/' + $slug + '/">' + (Escape-Html $ja.Title) + '</a></li><li><a href="/en/articles/' + $slug + '/">' + (Escape-Html $en.Title) + '</a></li></ul>'
  $htmlSitemap = $htmlSitemap.Replace("<h2>Robu's Selection</h2>", "<h2>Robu's Selection</h2>$links")
  [IO.File]::WriteAllText($htmlSitemapPath, $htmlSitemap, [Text.UTF8Encoding]::new($false))
}

$recordPath = Join-Path $RepoRoot 'records\2026\10\2026-10-25-nikkei-kai-publication.md'
New-Item -ItemType Directory -Force -Path (Split-Path $recordPath -Parent) | Out-Null
$record = @"
# NIKKEI KAI 広報・報道分析Agent記事 公開記録

- 公開承認: 2026-10-25、ユーザーの明示承認
- 分類: Robu's Selection / AI・業務支援
- 日本語・英語: 承認済み原稿を使用
- 画像: AI生成編集イメージ2枚、各画像直後に注記あり
- 購入先: Amazon、楽天市場、Yahoo!ショッピング
- 広告表示: 記事・書籍説明、購入ボタン、価格等の注意書きの後に通常テキストで表示
- SNS自動配信: 今回は未承認のため無効
- 公開URL: $baseUrl/articles/$slug/
"@
[IO.File]::WriteAllText($recordPath, $record, [Text.UTF8Encoding]::new($false))

Write-Output 'Built the approved bilingual NIKKEI KAI article, images, catalogue card, sitemaps, and publication record.'
