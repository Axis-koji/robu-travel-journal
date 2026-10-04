param([string]$RepoRoot = (Split-Path -Parent $PSScriptRoot))

$ErrorActionPreference = 'Stop'
$draftDir = 'E:\Documents\Codex\2026-08-01\robuse-selection-drafts\Draft\2026-10-03\2026-10-03-01-robu-kininaru-elyza-rsi-research-v2'
$slug = 'elyza-rsi-research-ai-improves-ai'
$publishDate = '2026-10-04'
$titleJa = 'AIがAIを作る時代は来た？ELYZA RSI Researchの3成果と限界'
$titleEn = 'Has AI Started Building AI? Three ELYZA Results—and the Limits'
$descriptionJa = 'AIが次のAIを開発する時代は本当に始まったのか。ELYZA RSI Researchの国産LLM、評価基準、ハーネス改善という3成果と、未実現のRSI、安全性の課題を公式情報で検証します。'
$descriptionEn = 'Has AI really started developing the next AI? A source-checked look at three ELYZA RSI Research results, their limits and why recursive self-improvement has not yet been achieved.'
$categoryJa = 'ろぶーの気になる事 / AI・技術'
$categoryEn = "Robu's Curiosities / AI & Technology"
$hero = 'elyza-rsi-human-oversight-hero-v1.png'
$images = @($hero, 'elyza-model-benchmark-harness-v1.png')

function Escape-Html([string]$value) { [System.Net.WebUtility]::HtmlEncode($value) }

function Read-Body([string]$path) {
  $raw = Get-Content -Raw -LiteralPath $path -Encoding utf8
  if ($raw -notmatch '(?s)^---\s*\r?\n.*?\r?\n---\s*\r?\n(.*)$') { throw "Missing front matter: $path" }
  $body = $matches[1]
  if ($body -match '(?i)公開前メモ|Pre-publication note') { throw "Pre-publication note remains: $path" }
  $body = $body.Replace("## Robu's conclusion", "## Robu's Take")
  return $body
}

function Source-Section([string]$language) {
  $sources = @(
    @('ELYZA, ELYZA RSI Research launch and research results (2026-10-02)', 'https://elyza.ai/news/2026/10/02/rsiresearch'),
    @('ELYZA official Hugging Face model card, dense 33B model', 'https://huggingface.co/elyza/ELYZA-Thinking-1.0-llm-jp-4-33b'),
    @('ELYZA official Hugging Face model card, 32B-A3B MoE model', 'https://huggingface.co/elyza/ELYZA-Thinking-1.0-llm-jp-4-32b-a3b'),
    @('ELYZA official GitHub repository, ELYZA Agent Tasks: Customer Service', 'https://github.com/elyza-inc/elyza-agent-tasks-customer-service'),
    @('ELYZA Voice Agent official announcement (2026-10-02)', 'https://elyza.ai/news/2026/10/02/voiceagent')
  )
  $items = for ($i = 0; $i -lt $sources.Count; $i++) {
    '<li id="source-' + ($i + 1) + '"><a href="' + $sources[$i][1] + '" target="_blank" rel="noopener noreferrer">' + (Escape-Html $sources[$i][0]) + '</a></li>'
  }
  $heading = if ($language -eq 'ja') { '主な一次・公式情報' } else { 'Primary and official sources' }
  return '<section class="robu-sources"><h2>' + (Escape-Html $heading) + '</h2><ol>' + ($items -join '') + '</ol></section>'
}

function Disclosure-Section([string]$language) {
  if ($language -eq 'ja') {
    return '<aside class="robu-editorial-note"><strong>この記事の制作について：</strong>AIを調査・構成・日英草稿の補助に使い、記載内容を公式一次資料と照合したうえで、運営者の公開承認を経て掲載しています。</aside>'
  }
  return '<aside class="robu-editorial-note"><strong>How this article was made:</strong> AI assisted research, structure and the Japanese and English drafts. The claims were checked against first-party sources, and the site owner approved publication.</aside>'
}

function Build-Page([string]$language) {
  $source = Join-Path $draftDir $(if ($language -eq 'ja') { 'article.md' } else { 'article-en.md' })
  $html = (ConvertFrom-Markdown -InputObject (Read-Body $source)).Html
  $html = [regex]::Replace($html, '(?s)^\s*<h1[^>]*>.*?</h1>\s*', '')
  $assetDir = Join-Path $RepoRoot ('assets\images\articles\' + $slug)
  New-Item -ItemType Directory -Force -Path $assetDir | Out-Null
  foreach ($image in $images) {
    $sourceImage = Join-Path $draftDir $image
    if (-not (Test-Path -LiteralPath $sourceImage)) { throw "Missing image: $sourceImage" }
    Copy-Item -LiteralPath $sourceImage -Destination (Join-Path $assetDir $image) -Force
    $html = $html.Replace('src="' + $image + '"', 'src="/assets/images/articles/' + $slug + '/' + $image + '"')
  }
  $caption = if ($language -eq 'ja') { 'AI生成による記事用イメージです。実際の研究画面や製品写真ではありません。' } else { 'AI-generated editorial image; not an actual research interface or product photograph.' }
  $html = [regex]::Replace($html, '(<p><img [^>]+/></p>)', ('$1' + '<p class="robu-image-caption">' + (Escape-Html $caption) + '</p>'))
  $html = [regex]::Replace($html, '(?<![A-Za-z])\[([1-5])\]', '<a class="source-ref" href="#source-$1">[$1]</a>')
  $html += (Disclosure-Section $language)
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
  $imageAlt = if ($language -eq 'ja') { '人間がAIモデルの開発・評価・改善ループを監督するAI生成編集イメージ' } else { 'AI-generated editorial image of a human supervising an AI development and evaluation loop' }
  $page = @"
<!doctype html>
<html lang="$language" translate="no"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="google" content="notranslate"><meta name="social:publish" content="false">
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
<style>.article-content img{display:block;max-width:100%;height:auto;margin-inline:auto}.robu-image-caption{font-size:.78rem;color:#5a6f73;margin-top:-.6rem}.robu-editorial-note{margin:2rem 0;padding:1rem;border:1px solid rgba(120,145,150,.35);border-radius:10px;font-size:.86rem;line-height:1.7}.article-content table{display:block;max-width:100%;overflow-x:auto}</style>
<script type="application/ld+json">$schema</script>
<script defer src="/assets/js/shared-shell.js?v=20261003-desktop-left-toc-1"></script>
</head><body class="draft-preview robu-published-article"><main class="draft-main" data-contact-page><article>
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
    title=$titleJa; digestTitle='AIがAIを作る時代は来た？'; digestLead='ELYZAの三つの成果と、まだ実現していない自己改善AIの境界を公式情報で確認します。'; excerpt=$descriptionJa
    enTitle=$titleEn; enExcerpt=$descriptionEn
    image='assets/images/articles/' + $slug + '/' + $hero
    url='/articles/' + $slug + '/'; imageAlt='人間がAIの開発と評価を監督するAI生成編集イメージ'
  } | ConvertTo-Json -Compress -Depth 4
  $index = [regex]::Replace($index, 'const articles = \[', 'const articles = [' + "`n      " + $card + ',', 1)
  $index = [regex]::Replace($index, 'const articleFilters = \{', 'const articleFilters = {' + "`n      '" + $id + "': [],", 1)
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
if (-not $sitemapHtml.Contains('/articles/' + $slug + '/')) {
  $marker = '        <h2>AI・テクノロジー</h2>' + "`r`n        <ul>"
  $links = '          <li><a href="/articles/' + $slug + '/">' + (Escape-Html $titleJa) + '</a></li>' + "`r`n" +
    '          <li><a href="/en/articles/' + $slug + '/">' + (Escape-Html $titleEn) + ' (English)</a></li>'
  $sitemapHtml = $sitemapHtml.Replace($marker, $marker + "`r`n" + $links)
  [IO.File]::WriteAllText($sitemapHtmlPath, $sitemapHtml, [Text.UTF8Encoding]::new($false))
}

$recordDir = Join-Path $RepoRoot 'records\2026\10'
New-Item -ItemType Directory -Force -Path $recordDir | Out-Null
$record = @"
# Owner-approved publication — ELYZA RSI Research

- Publication date: 2026-10-04
- Category: ろぶーの気になる事 / AI・技術
- The owner explicitly approved publication and delegated final editorial judgment to Codex because of illness.
- The original v1 draft remains unchanged; publication uses the separately saved v2 bundle.
- Japanese and English articles were checked against five first-party sources; 13 claim-level checks passed.
- The headline and introduction were revised for clarity without changing the central conclusion that RSI itself has not been achieved.
- Two original AI-generated editorial images are visibly labeled and are not presented as research screenshots or product photographs.
- No affiliate links are present. No SNS publication action was requested or performed.
"@
[IO.File]::WriteAllText((Join-Path $recordDir '2026-10-04-publish-elyza-rsi-research-v1.md'), $record, [Text.UTF8Encoding]::new($false))

Write-Output 'Built bilingual ELYZA article, two images, homepage card, sitemaps, and publication record.'
