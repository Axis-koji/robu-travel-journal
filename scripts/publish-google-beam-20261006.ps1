param([string]$RepoRoot = (Split-Path -Parent $PSScriptRoot))

$ErrorActionPreference = 'Stop'
$draftDir = 'E:\Documents\Codex\2026-08-01\robuse-selection-drafts\Draft\2026-10-06\2026-10-06-02-robus-selection-hp-dimension-google-beam-v1'
$slug = 'hp-dimension-google-beam-review'
$publishDate = '2026-10-06'
$modifiedDate = '2026-10-07'
$titleJa = 'HP Dimension with Google Beamは導入すべき？659万円からの3D会議を7項目で確認'
$titleEn = 'Should You Deploy HP Dimension with Google Beam? Seven Checks for a 3D Meeting System Starting at ¥6.6 Million'
$descriptionJa = '日本出荷が始まったHP Dimension with Google Beamを公式情報で検証。659万8,900円からの価格、1対1の3D会議、追加費用、ネットワーク要件を整理します。'
$descriptionEn = 'HP Dimension with Google Beam is now shipping in Japan. We examine its price, one-to-one 3D limit, extra costs, network needs, and best-fit use cases.'
$categoryJa = "Robu's Selection / 法人向けテクノロジー"
$categoryEn = "Robu's Selection / Enterprise Technology"
$hero = 'google-beam-telepresence-hero-v1.png'
$images = @($hero, 'google-beam-deployment-checklist-v1.png')

function Escape-Html([string]$value) { [System.Net.WebUtility]::HtmlEncode($value) }

function Read-Body([string]$path, [string]$language) {
  $raw = Get-Content -Raw -LiteralPath $path -Encoding utf8
  if ($raw -notmatch '(?s)^---\s*\r?\n.*?\r?\n---\s*\r?\n(.*)$') { throw "Missing front matter: $path" }
  $body = $matches[1]
  $body = [regex]::Replace($body, '(?s)\r?\n## (?:公式・一次情報|Official and primary sources)\r?\n.*$', '')
  if ($language -eq 'ja') {
    $body = $body.Replace('## 結論', '## ろぶーの結論')
    $body = $body.Replace('日本向け出荷を開始したと発表しました。', '日本向け出荷を開始したと発表しました。[1]')
    $body = $body.Replace('自然なアイコンタクトや身ぶりを伝える法人向けシステムです。', '自然なアイコンタクトや身ぶりを伝える法人向けシステムです。[2][3]')
    $body = $body.Replace('従来型の2Dグループ会議も扱い、TeamsやWebexなどとの相互接続にも言及しています。', '従来型の2Dグループ会議も扱い、TeamsやWebexなどとの相互接続にも言及しています。[2]')
    $body = $body.Replace('壁掛けモデル：659万8,900円', '壁掛けモデル：659万8,900円[2]')
    $body = $body.Replace('フロアスタンドモデル：754万6,000円', 'フロアスタンドモデル：754万6,000円[2]')
    $body = $body.Replace('消費電力の目安は通話中600W、待機時70Wです。', '消費電力の目安は通話中600W、待機時70Wです。[4]')
  } else {
    $body = $body.Replace('## Verdict', "## Robu's Take")
    $body = $body.Replace('had begun shipping to Japan.', 'had begun shipping to Japan.[1]')
    $body = $body.Replace('without requiring 3D glasses or a headset.', 'without requiring 3D glasses or a headset.[2][3]')
    $body = $body.Replace('interoperability with services such as Teams and Webex.', 'interoperability with services such as Teams and Webex.[2]')
    $body = $body.Replace('Wall-mounted model: ¥6,598,900', 'Wall-mounted model: ¥6,598,900[2]')
    $body = $body.Replace('Floor-stand model: ¥7,546,000', 'Floor-stand model: ¥7,546,000[2]')
    $body = $body.Replace('70 W when idle.', '70 W when idle.[4]')
  }
  return $body
}

function Source-Section([string]$language) {
  $sources = @(
    @('Google Japan Blog, Google Beam begins shipping to Japan (2026-10-05)', 'https://blog.google/intl/ja-jp/feed/google-beam-expansion/'),
    @('HP Japan, HP Dimension with Google Beam launch announcement (2026-08-27)', 'https://jp.ext.hp.com/info/newsroom/2026/20260827/'),
    @('HP Japan, HP Dimension with Google Beam product page', 'https://www.hp.com/jp-ja/solutions/hp-dimension.html'),
    @('HP, HP Dimension with Google Beam product brief and additional specifications', 'https://h20195.www2.hp.com/v2/getpdf.aspx/c09181708.pdf'),
    @('Google, Google Beam expands with new regions, partners and customers', 'https://blog.google/innovation-and-ai/technology/research/google-beam-expansion/')
  )
  $items = for ($i = 0; $i -lt $sources.Count; $i++) {
    '<li id="source-' + ($i + 1) + '"><a href="' + $sources[$i][1] + '" target="_blank" rel="noopener noreferrer">' + (Escape-Html $sources[$i][0]) + '</a></li>'
  }
  $heading = if ($language -eq 'ja') { '主な一次・公式情報' } else { 'Primary and official sources' }
  return '<section class="robu-sources"><h2>' + (Escape-Html $heading) + '</h2><ol>' + ($items -join '') + '</ol></section>'
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
  $caption = if ($language -eq 'ja') { 'AI生成による記事用イメージです。実際のHP製品写真やGoogle Beamの画面ではありません。' } else { 'AI-generated editorial image; not an actual HP product photograph or Google Beam interface.' }
  $html = [regex]::Replace($html, '(<p><img [^>]+/></p>)', ('$1' + '<p class="robu-image-caption">' + (Escape-Html $caption) + '</p>'))
  $html = [regex]::Replace($html, '(?<![A-Za-z])\[([1-5])\]', '<a class="source-ref" href="#source-$1">[$1]</a>')
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
    datePublished=$publishDate; dateModified=$modifiedDate; inLanguage=$(if ($language -eq 'ja') { 'ja-JP' } else { 'en' })
    mainEntityOfPage=[ordered]@{'@type'='WebPage';'@id'=$canonical}; image=$imageUrls; articleSection=$category
    author=[ordered]@{'@type'='Organization';name='ろぶーの気になる事'}
    publisher=[ordered]@{'@type'='Organization';name='ろぶーの気になる事';url='https://www.axis-jp.net/'}
    isAccessibleForFree=$true
  } | ConvertTo-Json -Compress -Depth 6
  $locale = if ($language -eq 'ja') { 'ja_JP' } else { 'en_US' }
  $imageAlt = if ($language -eq 'ja') { '企業向け3D会議室で1対1の遠隔会話をする様子のAI生成編集イメージ' } else { 'AI-generated editorial image of a one-to-one remote conversation in an enterprise 3D meeting room' }
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
<meta property="article:section" content="$(Escape-Html $category)"><meta property="article:published_time" content="${publishDate}T00:00:00+09:00"><meta property="article:modified_time" content="${modifiedDate}T00:00:00+09:00">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="$(Escape-Html $title)"><meta name="twitter:description" content="$(Escape-Html $description)"><meta name="twitter:image" content="$($imageUrls[0])">
<link rel="stylesheet" href="/assets/css/contact-feedback-ees-standard.css?v=3" data-contact-feedback-style>
<link rel="stylesheet" href="/assets/css/draft-article-preview.css?v=20260930-publish-five-1">
<style>.article-content img{display:block;max-width:100%;height:auto;margin-inline:auto}.robu-image-caption{font-size:.78rem;color:#b9b4a8;margin-top:-.6rem}.article-content table{display:block;max-width:100%;overflow-x:auto}</style>
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
    id=$id; date=$publishDate; dateLabel='2026.10.06'; category=$categoryJa
    title=$titleJa; digestTitle='659万円からの3D会議、導入価値は？'; digestLead='1対1の3D会議、追加費用、回線条件まで公式情報で確認します。'; excerpt=$descriptionJa
    enTitle=$titleEn; enExcerpt=$descriptionEn
    image='assets/images/articles/' + $slug + '/' + $hero
    url='/articles/' + $slug + '/'; imageAlt='企業向け3D会議室で1対1の遠隔会話をする様子のAI生成編集イメージ'
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
    $sitemap = $sitemap.Replace('</urlset>', '  <url><loc>' + $url + '</loc><lastmod>' + $modifiedDate + "</lastmod></url>`n</urlset>")
  }
}
[IO.File]::WriteAllText($sitemapPath, $sitemap, [Text.UTF8Encoding]::new($false))

$sitemapHtmlPath = Join-Path $RepoRoot 'sitemap\index.html'
$sitemapHtml = Get-Content -Raw -LiteralPath $sitemapHtmlPath -Encoding utf8
if (-not $sitemapHtml.Contains('/articles/' + $slug + '/')) {
  $links = '          <li><a href="/articles/' + $slug + '/">' + (Escape-Html $titleJa) + '</a></li>' + "`r`n" +
    '          <li><a href="/en/articles/' + $slug + '/">' + (Escape-Html $titleEn) + ' (English)</a></li>'
  $sitemapHtml = [regex]::Replace($sitemapHtml, '(\s*<h2>Robu''s Selection</h2>\s*<ul>)', '$1' + "`r`n" + $links, 1)
  [IO.File]::WriteAllText($sitemapHtmlPath, $sitemapHtml, [Text.UTF8Encoding]::new($false))
}

$recordDir = Join-Path $RepoRoot 'records\2026\10'
New-Item -ItemType Directory -Force -Path $recordDir | Out-Null
$record = @"
# Owner-approved publication — HP Dimension with Google Beam

- Publication date: 2026-10-06; final publication processing completed on 2026-10-07 JST.
- Category: Robu's Selection / 法人向けテクノロジー
- The owner explicitly approved this article for publication under the established publication rules.
- Japanese and English articles were checked against five first-party sources; 12 claim-level checks passed.
- The article states that this is an enterprise system and evaluates whether organizations should deploy it; it does not present the product as a consumer purchase.
- Japanese launch prices are ¥6,598,900 for the wall-mounted model and ¥7,546,000 for the floor-stand model, including tax; license, installation, maintenance, room, furniture and construction costs are disclosed as separate.
- The article limits the 3D core experience to one-to-one use, distinguishes conventional 2D group meetings, and discloses the six-versus-seven-camera discrepancy in HP's public material.
- Two original AI-generated editorial images are visibly labeled and are not presented as HP or Google product images.
- No affiliate links are present. No SNS publication action was requested or performed.
"@
[IO.File]::WriteAllText((Join-Path $recordDir '2026-10-06-publish-google-beam-v1.md'), $record, [Text.UTF8Encoding]::new($false))

Write-Output 'Built bilingual Google Beam article, two images, homepage Selection card, sitemaps, and publication record.'
