param(
  [string]$RepoRoot = (Split-Path -Parent $PSScriptRoot)
)

$ErrorActionPreference = 'Stop'
$draftRoot = 'E:\Documents\Codex\2026-08-01\robuse-selection-drafts\Draft'
$publishedDate = '2026-09-30'

$articles = @(
  [ordered]@{
    slug='ai-recommendation-link-safety'; source='2026-09-29\2026-09-29-01-robu-kininaru-ai-link-scam-v1'; selection=$false
    title='AIのおすすめリンクは安全？偽サイトへ誘導されないための5つの確認'; enTitle='Are AI-Recommended Links Safe? Five Checks That Help You Avoid Scam Sites'
    category='ろぶーの気になる事 / AI・安全'; excerpt='AIのおすすめリンクを開く前に、公式ドメイン、複数情報源、決済前の再確認など5つの安全確認を整理します。'
    enExcerpt='Five practical checks for safer use of links recommended by AI search and chat tools.'; image='ai-link-risk-hero.png'; imageAlt='AIのおすすめリンクを開く前に安全性を確認するAI生成イメージ'
  },
  [ordered]@{
    slug='notta-memo-pro-buying-guide'; source='2026-09-29\2026-09-29-02-robus-selection-notta-memo-pro-v1'; selection=$true
    title='Notta Memo Proは買い？2万9700円のAIボイスレコーダーを7項目で確認'; enTitle='Should You Buy the Notta Memo Pro? Seven Checks Before Spending ¥29,700'
    category="Robu's Selection / AIボイスレコーダー"; excerpt='価格、発売日、自動同期、文字起こし枠、クラウド運用、録音同意を公式情報から確認します。'
    enExcerpt='A source-based guide to price, release timing, automatic sync, transcription allowance, cloud use and consent.'; image='notta-memo-pro-official-reference-hero-v4.png'; imageAlt='Notta Memo Proの公式製品画像を基にした編集用イメージ'
  },
  [ordered]@{
    slug='jnto-baki-smart-travel-tips'; source='2026-09-28\2026-09-28-codex-v2-01-robu-kininaru-jnto-baki-travel-tips'; selection=$false
    title='訪日旅行のマナーを漫画で伝えると届く？JNTO「刃牙」旅行Tipsを読み解く'; enTitle="Can Manga Make Travel Etiquette Easier to Notice? Reading JNTO's Baki Travel Tips"
    category='ろぶーの気になる事 / 旅行・訪日観光'; excerpt='JNTOと秋田書店の旅行Tipsを、観光庁調査と照らして企画の狙いと未確認の効果に分けて整理します。'
    enExcerpt="A source-based look at JNTO's Baki travel tips and the practical problems visitors report."; image='japan-smart-travel-hero.png'; imageAlt='日本旅行のマナーを漫画風の構図で伝えるAI生成イメージ'
  },
  [ordered]@{
    slug='wakoh-signatures-watch'; source='2026-09-28\2026-09-28-python-02-robus-selection-signatures-watch'; selection=$true
    title='国産ムーブメントと国内最終工程に注目――和工の新ブランド「SIGNATURE(S)」を選ぶ前の確認点'; enTitle="Before Choosing Wakoh's SIGNATURE(S): Japanese Movements and Domestic Final Assembly"
    category="Robu's Selection / 腕時計"; excerpt='和工の新ブランドSIGNATURE(S)のダイバーズとクロノグラフを、仕様、価格、生産工程から確認します。'
    enExcerpt="A source-based guide to Wakoh's SIGNATURE(S) diver and chronograph watches, pricing and production split."; image='signatures-diver-faithful-generated-v3.png'; imageAlt='SIGNATURE(S)のダイバーズを公式発表写真に基づいて再現したAI生成イメージ'
  },
  [ordered]@{
    slug='ricoh-gr-iv-30th-anniversary'; source='2026-09-28\2026-09-28-codex-v2-02-robus-selection-ricoh-gr-iv-30th'; selection=$true
    title='RICOH GR IV 30周年記念モデルは何が特別？限定6,000台を選ぶ前の確認点'; enTitle='What Makes the RICOH GR IV 30th Anniversary Edition Special?'
    category="Robu's Selection / カメラ"; excerpt='限定6,000台の30周年記念モデルについて、通常モデルとの違い、価格、抽選条件を公式情報で確認します。'
    enExcerpt='A source-based guide to the limited RICOH GR IV 30th Anniversary Edition, its differences, price and lottery sale.'; image='gr-iv-30th-editorial-hero.png'; imageAlt='RICOH GR IV 30周年記念モデルをイメージしたAI生成編集画像'
  },
  [ordered]@{
    slug='digital-ad-supply-chain-transparency'; source='2026-09-28\2026-09-28-python-01-robu-kininaru-ad-transparency'; selection=$false
    title='AI時代、ブログの広告は誰が売っている？METIセミナーから考える「見える取引」'; enTitle="Who Sells a Blog's Advertising in the AI Era? Making the Supply Chain Visible"
    category='ろぶーの気になる事 / デジタル広告'; excerpt='METIとIAB Tech Labの情報から、広告販売経路、ads.txt、媒体収益の透明性を整理します。'
    enExcerpt='A source-based guide to digital-ad supply chains, ads.txt and publisher revenue transparency.'; image='ad-supply-chain-hero.png'; imageAlt='デジタル広告の取引経路を可視化したAI生成イメージ'
  }
)

function Escape-Html([string]$value) {
  if ($null -eq $value) { return '' }
  return [System.Net.WebUtility]::HtmlEncode($value)
}

function Read-FrontMatter([string]$text) {
  $meta = @{}
  if ($text -match '(?s)^---\s*\r?\n(.*?)\r?\n---\s*\r?\n(.*)$') {
    $frontMatterText = $matches[1]
    $bodyText = $matches[2]
    foreach ($line in ($frontMatterText -split '\r?\n')) {
      if ($line -match '^([A-Za-z][A-Za-z0-9]*):\s*(.*)$') {
        $key = $matches[1]
        $value = $matches[2].Trim()
        if ($value.StartsWith('"') -and $value.EndsWith('"')) { $value = $value.Substring(1, $value.Length - 2) }
        $meta[$key] = $value
      }
    }
    return @{ Meta=$meta; Body=$bodyText }
  }
  return @{ Meta=$meta; Body=$text }
}

function Build-Page([hashtable]$item, [string]$language) {
  $fileName = if ($language -eq 'ja') { 'article.md' } else { 'article-en.md' }
  $sourceDir = Join-Path $draftRoot $item.source
  $parsed = Read-FrontMatter (Get-Content -Raw -LiteralPath (Join-Path $sourceDir $fileName))
  $meta = $parsed.Meta
  $body = $parsed.Body
  $html = (ConvertFrom-Markdown -InputObject $body).Html
  $html = [regex]::Replace($html, '(?s)^\s*<h1[^>]*>.*?</h1>\s*', '')

  $imageMatches = [regex]::Matches($body, '!\[[^\]]*\]\((?:\./)?([^\s\)]+)(?:\s+"[^"]*")?\)')
  $assetDir = Join-Path $RepoRoot ('assets\images\articles\' + $item.slug)
  New-Item -ItemType Directory -Force -Path $assetDir | Out-Null
  foreach ($match in $imageMatches) {
    $name = [IO.Path]::GetFileName($match.Groups[1].Value)
    $sourceImage = Join-Path $sourceDir $name
    if (-not (Test-Path -LiteralPath $sourceImage)) { throw "Missing image: $sourceImage" }
    Copy-Item -LiteralPath $sourceImage -Destination (Join-Path $assetDir $name) -Force
  }
  $html = [regex]::Replace($html, 'src="(?:\./)?([^/"\s]+\.(?:png|jpe?g|webp))"', { param($m) 'src="/assets/images/articles/' + $item.slug + '/' + $m.Groups[1].Value + '"' })
  $html = [regex]::Replace($html, '<a href="(https://(?:www\.amazon\.co\.jp|hb\.afl\.rakuten\.co\.jp|ck\.jp\.ap\.valuecommerce\.com)[^"]*)">', '<a href="$1" target="_blank" rel="nofollow sponsored noopener noreferrer">')
  $html = [regex]::Replace($html, '<a href="(https?://[^"]*)">', '<a href="$1" target="_blank" rel="noopener noreferrer">')

  $title = if ($meta.title) { $meta.title } elseif ($language -eq 'ja') { $item.title } else { $item.enTitle }
  $seoTitle = if ($meta.seoTitle) { $meta.seoTitle } else { $title }
  $description = if ($meta.metaDescription) { $meta.metaDescription } elseif ($meta.description) { $meta.description } elseif ($language -eq 'ja') { $item.excerpt } else { $item.enExcerpt }
  $langPath = if ($language -eq 'ja') { '' } else { 'en/' }
  $canonical = "https://www.axis-jp.net/${langPath}articles/$($item.slug)/"
  $alternateJa = "https://www.axis-jp.net/articles/$($item.slug)/"
  $alternateEn = "https://www.axis-jp.net/en/articles/$($item.slug)/"
  $ogImage = "https://www.axis-jp.net/assets/images/articles/$($item.slug)/$($item.image)"
  $pageClass = if ($item.selection) { 'draft-preview robus-selection-page' } else { 'draft-preview' }
  $label = if ($item.selection) { '<div class="robu-selection-label">Robu''s Selection</div>' } else { '' }
  $category = if ($language -eq 'ja') { $item.category } elseif ($item.selection) { "Robu's Selection" } else { "Robu's Curiosities" }
  $locale = if ($language -eq 'ja') { 'ja_JP' } else { 'en_US' }
  $inLanguage = if ($language -eq 'ja') { 'ja-JP' } else { 'en' }
  $schema = [ordered]@{
    '@context'='https://schema.org'; '@type'='Article'; headline=$title; description=$description
    datePublished=$publishedDate; dateModified=$publishedDate; inLanguage=$inLanguage
    mainEntityOfPage=[ordered]@{'@type'='WebPage';'@id'=$canonical}; image=@($ogImage)
    articleSection=$category; author=[ordered]@{'@type'='Organization';name='ろぶーの気になる事'}
    publisher=[ordered]@{'@type'='Organization';name='ろぶーの気になる事';url='https://www.axis-jp.net/'}; isAccessibleForFree=$true
  } | ConvertTo-Json -Compress -Depth 6

  $page = @"
<!doctype html>
<html lang="$language" translate="no"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="google" content="notranslate"><meta name="social:publish" content="false">
<meta name="referrer" content="strict-origin-when-cross-origin"><meta name="robots" content="index,follow,max-image-preview:large">
<title>$(Escape-Html $seoTitle)</title>
<meta name="description" content="$(Escape-Html $description)">
<link rel="canonical" href="$canonical">
<link rel="alternate" hreflang="ja" href="$alternateJa"><link rel="alternate" hreflang="en" href="$alternateEn"><link rel="alternate" hreflang="x-default" href="$alternateJa">
<meta property="og:type" content="article"><meta property="og:locale" content="$locale"><meta property="og:site_name" content="ろぶーの気になる事">
<meta property="og:title" content="$(Escape-Html $title)"><meta property="og:description" content="$(Escape-Html $description)">
<meta property="og:url" content="$canonical"><meta property="og:image" content="$ogImage"><meta property="og:image:alt" content="$(Escape-Html $item.imageAlt)">
<meta property="article:section" content="$(Escape-Html $category)"><meta property="article:published_time" content="2026-09-30T00:00:00+09:00"><meta property="article:modified_time" content="2026-09-30T00:00:00+09:00">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="$(Escape-Html $title)"><meta name="twitter:description" content="$(Escape-Html $description)"><meta name="twitter:image" content="$ogImage">
<link rel="stylesheet" href="/assets/css/contact-feedback-ees-standard.css?v=3" data-contact-feedback-style>
<link rel="stylesheet" href="/assets/css/draft-article-preview.css?v=20260930-publish-five-1">
<style>.article-content ul:has(a[href*="womaster-22"]){list-style:none;padding:0;display:grid;gap:12px}.article-content li:has(a[href*="womaster-22"]){margin:0}.article-content a[href*="womaster-22"],.article-content a[href*="hb.afl.rakuten"],.article-content a[href*="ck.jp.ap.valuecommerce"]{display:flex;min-height:52px;align-items:center;justify-content:center;padding:10px 14px;border-radius:10px;color:#fff;font-weight:800;text-align:center;text-decoration:none}.article-content a[href*="womaster-22"]{background:#146eb4}.article-content a[href*="hb.afl.rakuten"]{background:#bf0000}.article-content a[href*="ck.jp.ap.valuecommerce"]{background:#fff;color:#d71920;border:2px solid #d71920}</style>
<script type="application/ld+json">$schema</script>
<script defer src="/assets/js/shared-shell.js?v=20260926-browser-language-1"></script>
</head><body class="$pageClass"><main class="draft-main" data-contact-page><article>
$label
<div class="selection-subcategory" data-article-category>$(Escape-Html $category)</div>
<h1 class="article-title">$(Escape-Html $title)</h1>
<div class="article-content">
$html
</div>
</article></main><script src="/assets/js/contact-feedback.js?v=20260907-1"></script></body></html>
"@

  $targetDir = if ($language -eq 'ja') { Join-Path $RepoRoot ('articles\' + $item.slug) } else { Join-Path $RepoRoot ('en\articles\' + $item.slug) }
  New-Item -ItemType Directory -Force -Path $targetDir | Out-Null
  [IO.File]::WriteAllText((Join-Path $targetDir 'index.html'), $page, [Text.UTF8Encoding]::new($false))
}

foreach ($item in $articles) {
  Build-Page $item 'ja'
  Build-Page $item 'en'
}

$indexPath = Join-Path $RepoRoot 'index.html'
$index = Get-Content -Raw -LiteralPath $indexPath
$cards = foreach ($item in $articles) {
  $obj = [ordered]@{
    id="$($item.slug)-$publishedDate"; date=$publishedDate; dateLabel='2026.09.30'; category=$item.category
    title=$item.title; digestTitle=$item.title; digestLead=$item.excerpt; excerpt=$item.excerpt
    enTitle=$item.enTitle; enExcerpt=$item.enExcerpt; image="assets/images/articles/$($item.slug)/$($item.image)"
    url="/articles/$($item.slug)/"; imageAlt=$item.imageAlt
  }
  '      ' + ($obj | ConvertTo-Json -Compress -Depth 4) + ','
}
$cardText = ($cards -join "`r`n") + "`r`n"
if ($index -notmatch 'ai-recommendation-link-safety-2026-09-30') {
  $index = $index.Replace("    const articles = [`r`n", "    const articles = [`r`n$cardText")
  $filters = foreach ($item in $articles) { $filter = if ($item.selection) { "['selection']" } elseif ($item.slug -eq 'jnto-baki-smart-travel-tips') { "['travel']" } else { '[]' }; "      '$($item.slug)-$publishedDate': $filter," }
  $index = $index.Replace("    const articleFilters = {`r`n", "    const articleFilters = {`r`n$($filters -join "`r`n")`r`n")
  [IO.File]::WriteAllText($indexPath, $index, [Text.UTF8Encoding]::new($false))
}

$sitemapPath = Join-Path $RepoRoot 'sitemap.xml'
$sitemap = Get-Content -Raw -LiteralPath $sitemapPath
if ($sitemap -notmatch 'ai-recommendation-link-safety') {
  $nodes = foreach ($item in $articles) {
    "  <url><loc>https://www.axis-jp.net/articles/$($item.slug)/</loc><lastmod>$publishedDate</lastmod></url>`r`n  <url><loc>https://www.axis-jp.net/en/articles/$($item.slug)/</loc><lastmod>$publishedDate</lastmod></url>"
  }
  $sitemap = $sitemap.Replace('</urlset>', ($nodes -join "`r`n") + "`r`n</urlset>")
  [IO.File]::WriteAllText($sitemapPath, $sitemap, [Text.UTF8Encoding]::new($false))
}

$recordDir = Join-Path $RepoRoot 'records\2026\09'
New-Item -ItemType Directory -Force -Path $recordDir | Out-Null
$record = @"
# Publication record — six owner-approved articles

- Approved and published on: 2026-09-30
- Scope: Notta Memo Pro, SIGNATURE(S), JNTO Baki travel tips, AI-recommended link safety, RICOH GR IV 30th Anniversary, digital-ad supply-chain transparency
- Each Japanese and English page includes Amazon Associates, Rakuten Affiliate, and ValueCommerce Yahoo! Shopping search links with an affiliate disclosure.
- Source draft bundles and earlier images were preserved.
"@
[IO.File]::WriteAllText((Join-Path $recordDir '2026-09-30-publish-six-owner-approved-v1.md'), $record, [Text.UTF8Encoding]::new($false))

Write-Output "Built $($articles.Count) Japanese pages, $($articles.Count) English pages, homepage entries, sitemap entries, images, and a publication record."
