param([string]$RepoRoot = (Split-Path -Parent $PSScriptRoot))

$ErrorActionPreference = 'Stop'
$draftDir = 'E:\Documents\Codex\2026-08-01\robuse-selection-drafts\Draft\2026-10-06\2026-10-06-01-robu-kininaru-plamo-foundry-v1'
$slug = 'plamo-3-prime-microsoft-foundry'
$publishDate = '2026-10-06'
$titleJa = 'PLaMo 3.0 PrimeがMicrosoft Foundryに登場――国産LLM導入で変わること、変わらないこと'
$titleEn = 'PLaMo 3.0 Prime Comes to Microsoft Foundry: What Changes for Japanese Enterprise AI—and What Does Not'
$descriptionJa = 'PFNの国産LLM「PLaMo 3.0 Prime」がMicrosoft Foundryで提供開始。256kコンテキスト、推論・非推論モデル、料金と導入時の確認点を一次情報で整理します。'
$descriptionEn = 'Preferred Networks has launched PLaMo 3.0 Prime on Microsoft Foundry. Here is what its 256k context, reasoning choices, launch pricing and enterprise route mean in practice.'
$categoryJa = 'ろぶーの気になる事 / AI・技術'
$categoryEn = "Robu's Curiosities / AI & Technology"
$hero = 'plamo-foundry-enterprise-hero-v1.png'
$images = @($hero, 'plamo-reasoning-speed-choice-v1.png')

function Escape-Html([string]$value) { [System.Net.WebUtility]::HtmlEncode($value) }

function Read-Body([string]$path, [string]$language) {
  $raw = Get-Content -Raw -LiteralPath $path -Encoding utf8
  if ($raw -notmatch '(?s)^---\s*\r?\n.*?\r?\n---\s*\r?\n(.*)$') { throw "Missing front matter: $path" }
  $body = $matches[1]
  if ($body -match '(?i)公開前メモ|Pre-publication note') { throw "Pre-publication note remains: $path" }

  if ($language -eq 'ja') {
    $body = $body.Replace('## まとめ', '## ろぶーの結論')
    $body = $body.Replace('提供開始したと発表しました。', '提供開始したと発表しました。[1]')
    $body = $body.Replace('PLaMo 3.0 Primeは256kのコンテキスト長に対応します。PFNは、従来の64kから拡張し、長文処理やAIエージェントでの利用を想定したと説明しています。', 'PLaMo 3.0 Primeは256kのコンテキスト長に対応します。PFNは、従来の64kから拡張し、長文処理やAIエージェントでの利用を想定したと説明しています。[2][3]')
    $body = $body.Replace('MicrosoftはFoundryを、企業向けAIアプリやエージェントを構築・管理する統合プラットフォームと説明しています。', 'MicrosoftはFoundryを、AIアプリやエージェントを構築・管理する統合プラットフォームと説明しています。法人専用ではなく、Azureアカウントと有効なサブスクリプションがあれば個人開発者も利用できますが、一般向けの会話サービスではなく開発基盤です。[4]')
    $price = @"

PFNが公表した提供開始時のPLaMo 3.0 Primeのモデル利用料金は、NVIDIA A100 GPU 1枚につき1時間3.99ドル、H100 GPU 1枚につき1時間6.99ドルで、どちらもAzureのインフラ費用が別にかかります。これはChatGPTの月額料金のような固定プランではありません。必要なGPU構成と稼働時間で総額が変わるため、検証前にAzure側の見積もりと停止条件を決めておく必要があります。[1]
"@
    $body = $body.Replace('ただし、実際のデータ保存場所、ログの扱い、学習への利用有無、提供リージョン、料金、SLAは、契約画面と最新のMicrosoft資料で確認が必要です。', $price + "`n`nただし、実際のデータ保存場所、ログの扱い、学習への利用有無、提供リージョン、料金、SLAは、契約画面と最新のMicrosoft資料で確認が必要です。")
    $body = $body.Replace('比較対象、プロンプト、採点方法、推論設定、利用料金の条件が変われば結果も変わります。', '比較対象、プロンプト、採点方法、推論設定、利用料金の条件が変われば結果も変わります。[2][3]')
    $body = $body.Replace('導入前には、自社の匿名化済みサンプルで、正答率、根拠提示、再現性、禁止事項への応答を確かめるべきです。', '導入前には、自社の匿名化済みサンプルで、正答率、根拠提示、再現性、禁止事項への応答を確かめるべきです。AIの回答やリンクをそのまま信じないための確認手順は、関連記事「[AIのおすすめリンクは安全？](/articles/ai-recommendation-link-safety/)」でも整理しています。')
    $body = $body.Replace('PFNは日本語の自然さや業務文脈への対応を特徴として示していますが、', 'PFNは日本語の自然さや業務文脈への対応を特徴として示していますが[5]、')
  } else {
    $body = $body.Replace('## Conclusion', "## Robu's Take")
    $body = $body.Replace('are now available through Microsoft Foundry.', 'are now available through Microsoft Foundry.[1]')
    $body = $body.Replace('PLaMo 3.0 Prime supports a 256k context window. PFN says it expanded the model from 64k to support longer documents and agent-style workflows.', 'PLaMo 3.0 Prime supports a 256k context window. PFN says it expanded the model from 64k to support longer documents and agent-style workflows.[2][3]')
    $body = $body.Replace('Microsoft describes Foundry as a unified platform for building and managing enterprise AI applications and agents.', 'Microsoft describes Foundry as a unified platform for building and managing AI applications and agents. It is not restricted to corporations: an individual developer can use it with an Azure account and an active subscription, but it is a development platform rather than a consumer chat service.[4]')
    $price = @"

At launch, PFN lists the PLaMo 3.0 Prime model charge at 3.99 US dollars per NVIDIA A100 GPU-hour or 6.99 US dollars per H100 GPU-hour, plus separate Azure infrastructure costs. This is not a flat monthly plan like a consumer chatbot subscription. The total depends on the GPU configuration and running time, so a trial should start with an Azure estimate, a budget alert and an explicit shutdown rule.[1]
"@
    $body = $body.Replace('The announcement alone does not establish whether a particular deployment meets an organization''s requirements.', $price + "`n`nThe announcement alone does not establish whether a particular deployment meets an organization's requirements.")
    $body = $body.Replace('Rankings can change with the prompt set, scoring method, inference settings, comparison models, and price assumptions.', 'Rankings can change with the prompt set, scoring method, inference settings, comparison models, and price assumptions.[2][3]')
    $body = $body.Replace('A serious procurement test should use anonymized examples from the organization''s own work and measure factual accuracy, citations, repeatability, refusal behavior, latency, and review time under the same conditions used for competing models.', 'A serious procurement test should use anonymized examples from the organization''s own work and measure factual accuracy, citations, repeatability, refusal behavior, latency, and review time under the same conditions used for competing models. Our related guide, [Are AI-Recommended Links Safe?](/en/articles/ai-recommendation-link-safety/), gives a practical cross-checking routine for AI answers and links.')
    $body = $body.Replace('PFN positions it as a model designed for natural Japanese and business context,', 'PFN positions it as a model designed for natural Japanese and business context[5],')
  }
  return $body
}

function Source-Section([string]$language) {
  $sources = @(
    @('Preferred Networks, PLaMo 3.0 Prime and PLaMo Translate launch on Microsoft Foundry (2026-10-06)', 'https://www.preferred.jp/ja/news/pr20261006'),
    @('Preferred Networks, official release of PLaMo 3.0 Prime (2026-06-22)', 'https://www.preferred.jp/ja/news/pr20260622'),
    @('Preferred Networks technical blog, PLaMo 3.0 Prime release details (2026-06-22)', 'https://www.preferred.jp/ja/blog/tech/plamo-3-0-prime-release'),
    @('Microsoft Learn, What is Microsoft Foundry?', 'https://learn.microsoft.com/en-us/azure/foundry/what-is-foundry'),
    @('Preferred Networks, PLaMo Translate plans and features (2026-07-01)', 'https://www.preferred.jp/ja/news/pr20260701')
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
  $html = (ConvertFrom-Markdown -InputObject (Read-Body $source $language)).Html
  $html = [regex]::Replace($html, '(?s)^\s*<h1[^>]*>.*?</h1>\s*', '')
  $assetDir = Join-Path $RepoRoot ('assets\images\articles\' + $slug)
  New-Item -ItemType Directory -Force -Path $assetDir | Out-Null
  foreach ($image in $images) {
    $sourceImage = Join-Path $draftDir $image
    if (-not (Test-Path -LiteralPath $sourceImage)) { throw "Missing image: $sourceImage" }
    Copy-Item -LiteralPath $sourceImage -Destination (Join-Path $assetDir $image) -Force
    $html = $html.Replace('src="' + $image + '"', 'src="/assets/images/articles/' + $slug + '/' + $image + '"')
  }
  $caption = if ($language -eq 'ja') { 'AI生成による記事用イメージです。実際のMicrosoft Foundry画面やPLaMo製品画像ではありません。' } else { 'AI-generated editorial image; not an actual Microsoft Foundry interface or PLaMo product image.' }
  $html = [regex]::Replace($html, '(<p><img [^>]+/></p>)', ('$1' + '<p class="robu-image-caption">' + (Escape-Html $caption) + '</p>'))
  if ($language -eq 'ja') {
    $html = [regex]::Replace($html, '(</p><p class="robu-image-caption">.*?</p>)', '$1<p>こんにちは、ろぶーです。</p>', 1)
  }
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
  $imageAlt = if ($language -eq 'ja') { '日本企業が国産LLMと長文資料を評価するAI生成編集イメージ' } else { 'AI-generated editorial image of a team evaluating a Japanese language model and long documents' }
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
    id=$id; date=$publishDate; dateLabel='2026.10.06'; category=$categoryJa
    title=$titleJa; digestTitle='国産LLMがMicrosoft Foundryへ'; digestLead='PLaMo 3.0 Primeの256kコンテキスト、推論モデル、料金と導入時の注意点を公式情報で確認します。'; excerpt=$descriptionJa
    enTitle=$titleEn; enExcerpt=$descriptionEn
    image='assets/images/articles/' + $slug + '/' + $hero
    url='/articles/' + $slug + '/'; imageAlt='日本企業が国産LLMを評価するAI生成編集イメージ'
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
  $links = '          <li><a href="/articles/' + $slug + '/">' + (Escape-Html $titleJa) + '</a></li>' + "`r`n" +
    '          <li><a href="/en/articles/' + $slug + '/">' + (Escape-Html $titleEn) + ' (English)</a></li>'
  $sitemapHtml = [regex]::Replace($sitemapHtml, '(\s*<h2>AI・テクノロジー</h2>\s*<ul>)', '$1' + "`r`n" + $links, 1)
  [IO.File]::WriteAllText($sitemapHtmlPath, $sitemapHtml, [Text.UTF8Encoding]::new($false))
}

$recordDir = Join-Path $RepoRoot 'records\2026\10'
New-Item -ItemType Directory -Force -Path $recordDir | Out-Null
$record = @"
# Owner-approved publication — PLaMo 3.0 Prime on Microsoft Foundry

- Publication date: 2026-10-06
- Category: ろぶーの気になる事 / AI・技術
- The owner explicitly approved this article for publication under the established publication rules.
- Japanese and English articles were checked against five first-party sources; 12 claim-level checks passed, including launch pricing.
- The article clarifies that Microsoft Foundry is an enterprise-oriented development platform but is not legally restricted to corporations.
- Launch pricing is stated as PFN's per-GPU-hour model charge plus separate Azure infrastructure costs; no flat monthly-cost claim is made.
- Two original AI-generated editorial images are visibly labeled and are not presented as product screenshots.
- No affiliate links are present. No SNS publication action was requested or performed.
"@
[IO.File]::WriteAllText((Join-Path $recordDir '2026-10-06-publish-plamo-foundry-v1.md'), $record, [Text.UTF8Encoding]::new($false))

Write-Output 'Built bilingual PLaMo Foundry article, two images, homepage card, sitemaps, and publication record.'
