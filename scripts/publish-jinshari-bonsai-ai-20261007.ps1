param([string]$RepoRoot = (Split-Path -Parent $PSScriptRoot))

$ErrorActionPreference = 'Stop'
$draftDir = 'E:\Documents\Codex\2026-08-01\robuse-selection-drafts\Draft\2026-10-07\2026-10-07-01-robu-kininaru-jinshari-bonsai-ai-v1'
$slug = 'jinshari-bonsai-ai-cultural-knowledge'
$publishDate = '2026-10-07'
$titleJa = 'AIは盆栽の「美」を説明できる？JinShariが挑む暗黙知の言語化'
$titleEn = "Can AI Explain the Beauty of Bonsai? Inside JinShari's Attempt to Turn Tacit Knowledge into Words"
$descriptionJa = '盆栽管理アプリJinShariと、盆栽美学を約300冊の専門誌などから言語化する研究計画を紹介。現在使える記録機能と開発中・今後予定のAI機能を分けて確認します。'
$descriptionEn = 'JinShari combines a bonsai record-keeping app with research on how bonsai aesthetics have been described. We separate available features from planned AI functions.'
$categoryJa = 'ろぶーの気になる事 / AI・文化'
$categoryEn = "Robu's Curiosities / AI & Culture"
$hero = 'jinshari-bonsai-ai-hero-v1.png'
$images = @($hero, 'jinshari-human-care-loop-v1.png')

function Escape-Html([string]$value) { [System.Net.WebUtility]::HtmlEncode($value) }

function Read-Body([string]$path, [string]$language) {
  $raw = Get-Content -Raw -LiteralPath $path -Encoding utf8
  if ($raw -notmatch '(?s)^---\s*\r?\n.*?\r?\n---\s*\r?\n(.*)$') { throw "Missing front matter: $path" }
  $body = $matches[1]
  if ($body -match '(?i)公開前メモ|Pre-publication note') { throw "Pre-publication note remains: $path" }
  $body = [regex]::Replace($body, '(?s)\r?\n## (?:公式・一次情報|Official and primary sources)\r?\n.*$', '')

  if ($language -eq 'ja') {
    $body = $body.Replace('## まとめ', '## ろぶーの結論')
    $body = $body.Replace('2026年8月にはマレーシアで開かれた第10回世界盆栽大会へ出展し、9月には学術系クラウドファンディングを開始しました。', '2026年8月にはマレーシアで開かれた第10回世界盆栽大会へ出展し、9月には学術系クラウドファンディングを開始しました。[2][3]')
    $body = $body.Replace('公式サイトが掲げる柱は「生育管理」と「デザイン提案」です。', '公式サイトが掲げる柱は「生育管理」と「デザイン提案」です。[1]')
    $body = $body.Replace('第10回世界盆栽大会では、写真から見どころを可視化するAIプロトタイプの体験デモが行われました。', '第10回世界盆栽大会では、写真から見どころを可視化するAIプロトタイプの体験デモが行われました。[3]')
    $body = $body.Replace('academistで公開された研究計画は3段階です。', 'academistで公開された研究計画は3段階です。[2]')
    $body = $body.Replace('App Storeの掲載内容では、iPhone向けJinShariアプリは無料で、', 'App Storeの掲載内容では、iPhone向けJinShariアプリは無料で[4]、')
    $body = $body.Replace('一方、App Storeは「AIチャット相談」を今後追加予定としています。', '一方、App Storeは「AIチャット相談」を今後追加予定としています。更新履歴でも、デザイン評価とお手本画像生成は最新版開発のため無効化されたとされています。[4]')
    $body = $body.Replace('世界盆栽大会で紹介されたAI生育管理、AI樹形構想、病害虫画像診断なども、公式発表ではプロトタイプまたは開発中の機能を含みます。', '世界盆栽大会で紹介されたAI生育管理、AI樹形構想、病害虫画像診断なども、公式発表ではプロトタイプまたは開発・実証中の機能を含みます。[3][5]')
    $body = $body.Replace('したがって、2026年10月7日時点で、公式サイトに描かれたすべてのAI支援が一般利用できると読むのは早すぎます。', 'したがって、2026年10月7日時点で、公式サイトに描かれたすべてのAI支援が一般利用できると読むのは早すぎます。約300冊の専門誌分析も完了報告ではなく、2026年9月から2028年9月までの研究・実装計画です。[2][4]')
  } else {
    $body = $body.Replace('## Conclusion', "## Robu's Take")
    $body = $body.Replace('The team demonstrated its work at the 10th World Bonsai Convention in Malaysia in August 2026 and launched an academic crowdfunding campaign in September.', 'The team demonstrated its work at the 10th World Bonsai Convention in Malaysia in August 2026 and launched an academic crowdfunding campaign in September.[2][3]')
    $body = $body.Replace('The official site describes two pillars: cultivation management and design suggestions.', 'The official site describes two pillars: cultivation management and design suggestions.[1]')
    $body = $body.Replace('At the World Bonsai Convention, the team demonstrated an AI prototype that used a smartphone photo to visualize points of interest.', 'At the World Bonsai Convention, the team demonstrated an AI prototype that used a smartphone photo to visualize points of interest.[3]')
    $body = $body.Replace('The research plan published on academist has three phases:', 'The research plan published on academist has three phases:[2]')
    $body = $body.Replace('The Japanese App Store listing describes JinShari as a free iPhone app.', 'The Japanese App Store listing describes JinShari as a free iPhone app.[4]')
    $body = $body.Replace('The same listing marks AI chat consultation as a future feature.', 'The same listing marks AI chat consultation as a future feature. Its version history also says design evaluation and sample-image generation were disabled while newer versions are developed.[4]')
    $body = $body.Replace('AI cultivation guidance, AI form planning, and pest or disease image diagnosis described in project materials include functions identified as prototypes or under development.', 'AI cultivation guidance, AI form planning, and pest or disease image diagnosis described in project materials include functions identified as prototypes, under development or being validated.[3][5]')
    $body = $body.Replace('As of October 7, 2026, readers should not assume that every AI capability shown in the project''s vision is generally available in the shipping app.', 'As of October 7, 2026, readers should not assume that every AI capability shown in the project''s vision is generally available in the shipping app. The roughly 300-magazine analysis is also a research plan running from September 2026 toward app implementation in September 2028, not a completed result.[2][4]')
  }
  return $body
}

function Source-Section([string]$language) {
  $sources = @(
    @('JinShari official website', 'https://www.jinshari.jp/'),
    @('academist, 盆栽の魅力を世界中に届けたい！', 'https://academist-cf.com/projects/428?lang=ja'),
    @('JinShari project release, World Bonsai Convention demonstration and research plan', 'https://prtimes.jp/main/html/rd/p/000000002.000189591.html'),
    @('Apple App Store, JinShari', 'https://apps.apple.com/jp/app/jinshari/id6755102859'),
    @('ICT Startup League, JinShari', 'https://startupleague.jp/leaguers/2618/')
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
  $caption = if ($language -eq 'ja') { 'AI生成による記事用イメージです。実際のJinShari画面や研究資料ではありません。' } else { 'AI-generated editorial image; not an actual JinShari interface or research material.' }
  $html = [regex]::Replace($html, '(<p><img [^>]+/></p>)', ('$1' + '<p class="robu-image-caption">' + (Escape-Html $caption) + '</p>'))
  if ($language -eq 'ja') {
    $html = ([regex]::new('(</p><p class="robu-image-caption">.*?</p>)')).Replace($html, '$1<p>こんにちは、ろぶーです。</p>', 1)
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
  $imageAlt = if ($language -eq 'ja') { '盆栽と専門誌と分析画面を結ぶAI生成編集イメージ' } else { 'AI-generated editorial image connecting bonsai, specialist magazines and an analytical interface' }
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
    id=$id; date=$publishDate; dateLabel='2026.10.07'; category=$categoryJa
    title=$titleJa; digestTitle='AIは盆栽の美を言葉にできる？'; digestLead='JinShariの記録アプリと文化研究を、現在使える機能と今後のAI計画に分けて確認します。'; excerpt=$descriptionJa
    enTitle=$titleEn; enExcerpt=$descriptionEn
    image='assets/images/articles/' + $slug + '/' + $hero
    url='/articles/' + $slug + '/'; imageAlt='盆栽と専門誌と分析画面を結ぶAI生成編集イメージ'
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
# Owner-approved publication — JinShari bonsai AI and cultural research

- Publication date: 2026-10-07
- Category: ろぶーの気になる事 / AI・文化
- The owner explicitly approved this article for publication under the established publication rules.
- Japanese and English articles were checked against five official, project-owner and platform sources; 12 claim-level checks passed.
- The article separates the shipping record-keeping app from AI chat, design, cultivation and diagnosis functions described as future, disabled, prototype or in development.
- The roughly 300-magazine analysis is presented as a research plan, not a completed or peer-reviewed result.
- Two original AI-generated editorial images are visibly labeled and are not presented as product screenshots or research material.
- No affiliate links are present. The owner separately approved Facebook and Instagram publication after site publication.
"@
[IO.File]::WriteAllText((Join-Path $recordDir '2026-10-07-publish-jinshari-bonsai-ai-v1.md'), $record, [Text.UTF8Encoding]::new($false))

Write-Output 'Built bilingual JinShari article, two images, homepage card, sitemaps, and publication record.'
