param([string]$RepoRoot = (Split-Path -Parent $PSScriptRoot))

$ErrorActionPreference = 'Stop'
$draftRoot = 'E:\Documents\Codex\2026-08-01\robuse-selection-drafts\Draft\2026-10-02'
$publishDate = '2026-10-03'
$items = @(
  [ordered]@{
    slug='sony-berlin-philharmonic-partnership-2026'; folder='2026-10-02-01-robu-kininaru-sony-berlin-phil-v1'
    title='クラシック配信は「保存」から「再創造」へ？ソニー×ベルリン・フィル共創の4領域'
    enTitle="Beyond Recording: Four Areas in Sony and the Berliner Philharmoniker’s Partnership"
    description='ソニーとベルリン・フィル・メディア社の共創を公式発表で確認。収録、アーカイブ、空間体験、演奏者支援の4領域と未発表事項を整理します。'
    enDescription='What Sony and Berliner Philharmoniker Media have announced across capture, archives, immersive access and musician support—and what remains unknown.'
    category='ろぶーの気になる事 / 音楽・技術'; hero='concert-capture-hero-v1.png'
    imageAlt='オーケストラの撮影と収音をイメージしたAI生成画像'
    images=@('concert-capture-hero-v1.png','archive-to-immersive-v1.png')
  },
  [ordered]@{
    slug='kindle-2026-model-comparison'; folder='2026-10-02-02-robu-kininaru-kindle-2026-v2'
    title='新Kindleはどれを選ぶ？2万9980円からの4系列を用途別比較'
    enTitle='Which New Kindle Fits Your Reading? Four 2026 Model Families Compared'
    description='2026年の新Kindleを公式発表の価格、表示、防水、電池、出荷予定で比較。読書スタイル別に4系列の選び方を整理します。'
    enDescription="Compare Amazon’s 2026 Kindle families using official launch prices, displays, water resistance, battery estimates and shipping plans."
    category='ろぶーの気になる事 / 読書・ガジェット'; hero='kindle-lineup-editorial-hero-v1.png'
    imageAlt='4台の電子書籍リーダーを並べたAI生成の比較イメージ。実製品の写真ではありません'
    images=@('kindle-lineup-editorial-hero-v1.png','ereader-reading-scenes-v1.png')
  }
)

function Escape-Html([string]$value) { [System.Net.WebUtility]::HtmlEncode($value) }
function Read-Body([string]$path) {
  $raw = Get-Content -Raw -LiteralPath $path -Encoding utf8
  if ($raw -notmatch '(?s)^---\s*\r?\n.*?\r?\n---\s*\r?\n(.*)$') { throw "Missing front matter: $path" }
  $body = $matches[1]
  $body = [regex]::Replace($body, '(?m)^> (?:公開前メモ|Pre-publication note):.*(?:\r?\n)?', '')
  $body = $body.Replace("## Robu's verdict", "## Robu's Take").Replace("## Robu's take", "## Robu's Take")
  return $body
}
function Source-Section([string]$folder, [string]$language) {
  $lines = Get-Content -LiteralPath (Join-Path $folder 'sources.md') -Encoding utf8
  $list = [System.Collections.Generic.List[string]]::new()
  foreach ($line in $lines) {
    if ($line -match '^([1-9])\. (.+?) (https://\S+)\s*$') {
      $number=$matches[1]; $label=$matches[2]; $url=$matches[3]
      $list.Add('<li id="source-'+$number+'"><a href="'+(Escape-Html $url)+'" target="_blank" rel="noopener noreferrer">'+(Escape-Html $label)+'</a></li>')
    }
  }
  if ($list.Count -eq 0) { throw "No official sources: $folder" }
  $heading=if($language -eq 'ja'){'主な一次・公式情報'}else{'Primary and official sources'}
  return '<section class="robu-sources"><h2>'+(Escape-Html $heading)+'</h2><ol>'+($list -join '')+'</ol></section>'
}
function Purchase-Section([string]$language) {
  if ($language -eq 'ja') {
    $heading='購入先を確認する'; $note='以下はAmazonの公式商品ページへのアフィリエイトリンクです。価格・在庫・出荷予定は変わるため、購入前に販売者と最新表示を確認してください。'
    $labels=@('Kindle 16GBを確認する','Kindle 32GBを確認する','Kindle Paperwhiteを確認する','Kindle Colorsoftを確認する')
  } else {
    $heading='Check official product listings'; $note='The links below lead to Amazon product pages and include an affiliate tag. Check the current seller, price, availability and shipping date before purchase.'
    $labels=@('Kindle 16GB','Kindle 32GB','Kindle Paperwhite','Kindle Colorsoft')
  }
  $ids=@('B0G4SMGD8C','B0FZDDVH3G','B0GV5VHTL6','B0GV62167S')
  $buttons=[System.Collections.Generic.List[string]]::new()
  for($i=0;$i -lt $ids.Count;$i++) {
    $url='https://www.amazon.co.jp/dp/'+$ids[$i]+'?tag=womaster-22'
    $buttons.Add('<a class="robu-marketplace-button amazon" href="'+$url+'" target="_blank" rel="nofollow sponsored noopener noreferrer">'+(Escape-Html $labels[$i])+'</a>')
  }
  return '<section class="robu-marketplace-section"><h2>'+(Escape-Html $heading)+'</h2><p class="note" data-purchase-disclosure>'+(Escape-Html $note)+'</p><div class="robu-marketplace-buttons">'+($buttons -join '')+'</div></section>'
}
function Build-Page($item, [string]$language) {
  $sourceDir=Join-Path $draftRoot $item.folder
  $body=Read-Body (Join-Path $sourceDir $(if($language -eq 'ja'){'article.md'}else{'article-en.md'}))
  if ($item.slug -like 'sony-*') {
    $greeting=if($language -eq 'ja'){'こんにちは、ろぶーです。'}else{"Hello, I'm Robu."}
    $body=[regex]::Replace($body, '(?m)^(# .+\r?\n)', ('$1' + "`n" + $greeting + "`n"), 1)
  }
  $html=(ConvertFrom-Markdown -InputObject $body).Html
  $html=[regex]::Replace($html,'(?s)^\s*<h1[^>]*>.*?</h1>\s*','')
  foreach($imageName in $item.images) {
    $imageSource=Join-Path $sourceDir $imageName
    if(-not (Test-Path -LiteralPath $imageSource)){throw "Missing image: $imageSource"}
    $assetDir=Join-Path $RepoRoot ('assets\images\articles\'+$item.slug)
    New-Item -ItemType Directory -Force -Path $assetDir | Out-Null
    Copy-Item -LiteralPath $imageSource -Destination (Join-Path $assetDir $imageName) -Force
    $html=$html.Replace('src="'+$imageName+'"','src="/assets/images/articles/'+$item.slug+'/'+$imageName+'"')
  }
  $imageAlt=if($language -eq 'ja'){'AI生成による記事用イメージ。実際の商品や公演の写真ではありません'}else{'AI-generated editorial illustration, not a photograph of the actual product or performance'}
  $html=[regex]::Replace($html,'(<img\s+[^>]*alt=")[^"]*(")',('$1'+(Escape-Html $imageAlt)+'$2'))
  $caption=if($language -eq 'ja'){'AI生成イメージです。実際の公演・機器・商品写真ではありません。'}else{'AI-generated editorial image; not a photograph of the actual performance or products.'}
  $html=[regex]::Replace($html,'(<p><img [^>]+/></p>)', ('$1' + '<p class="robu-image-caption">'+(Escape-Html $caption)+'</p>'))
  $html=[regex]::Replace($html,'(?<![A-Za-z])\[([1-5])\]','<a class="source-ref" href="#source-$1">[$1]</a>')
  if($item.slug -like 'kindle-*') { $html += (Purchase-Section $language) }
  $html += (Source-Section $sourceDir $language)
  $title=if($language -eq 'ja'){$item.title}else{$item.enTitle}
  $description=if($language -eq 'ja'){$item.description}else{$item.enDescription}
  $category=if($language -eq 'ja'){$item.category}else{"Robu's Curiosities"}
  $path=if($language -eq 'ja'){'articles/'}else{'en/articles/'}
  $canonical='https://www.axis-jp.net/'+$path+$item.slug+'/'
  $jaUrl='https://www.axis-jp.net/articles/'+$item.slug+'/'
  $enUrl='https://www.axis-jp.net/en/articles/'+$item.slug+'/'
  $ogImage='https://www.axis-jp.net/assets/images/articles/'+$item.slug+'/'+$item.hero
  $schema=[ordered]@{
    '@context'='https://schema.org'; '@type'='Article'; headline=$title; description=$description
    datePublished=$publishDate; dateModified=$publishDate; inLanguage=$(if($language -eq 'ja'){'ja-JP'}else{'en'})
    mainEntityOfPage=[ordered]@{'@type'='WebPage';'@id'=$canonical}; image=@($ogImage); articleSection=$category
    author=[ordered]@{'@type'='Organization';name='ろぶーの気になる事'}
    publisher=[ordered]@{'@type'='Organization';name='ろぶーの気になる事';url='https://www.axis-jp.net/'}
    isAccessibleForFree=$true
  } | ConvertTo-Json -Compress -Depth 6
  $locale=if($language -eq 'ja'){'ja_JP'}else{'en_US'}
  $page=@"
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
<meta property="og:url" content="$canonical"><meta property="og:image" content="$ogImage"><meta property="og:image:alt" content="$(Escape-Html $item.imageAlt)">
<meta property="article:section" content="$(Escape-Html $category)"><meta property="article:published_time" content="${publishDate}T00:00:00+09:00"><meta property="article:modified_time" content="${publishDate}T00:00:00+09:00">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="$(Escape-Html $title)"><meta name="twitter:description" content="$(Escape-Html $description)"><meta name="twitter:image" content="$ogImage">
<link rel="stylesheet" href="/assets/css/contact-feedback-ees-standard.css?v=3" data-contact-feedback-style>
<link rel="stylesheet" href="/assets/css/draft-article-preview.css?v=20260930-publish-five-1">
<style>.article-content img{display:block;max-width:100%;height:auto;margin-inline:auto}.robu-image-caption{font-size:.78rem;color:#5a6f73;margin-top:-.6rem}.robu-marketplace-section h2{font-size:clamp(18px,2vw,22px)}.robu-marketplace-buttons{display:grid;gap:10px}.robu-marketplace-button.amazon{display:block;padding:12px 16px;border-radius:9px;background:#146eb4;color:#fff;font-weight:700;text-align:center;text-decoration:none}.robu-marketplace-button.amazon:focus-visible{outline:3px solid #102f38;outline-offset:2px}.article-content table{display:block;max-width:100%;overflow-x:auto}</style>
<script type="application/ld+json">$schema</script>
<script defer src="/assets/js/shared-shell.js?v=20260930-layout-affiliate-2"></script>
</head><body class="draft-preview robu-published-article"><main class="draft-main" data-contact-page><article>
<div class="selection-subcategory" data-article-category>$(Escape-Html $category)</div>
<h1 class="article-title">$(Escape-Html $title)</h1>
<div class="article-content">$html</div>
</article></main><script src="/assets/js/contact-feedback.js?v=20260907-1"></script></body></html>
"@
  $target=Join-Path $RepoRoot ($path.Replace('/','\')+$item.slug)
  New-Item -ItemType Directory -Force -Path $target | Out-Null
  [IO.File]::WriteAllText((Join-Path $target 'index.html'),$page,[Text.UTF8Encoding]::new($false))
}

foreach($item in $items){Build-Page $item 'ja'; Build-Page $item 'en'}
$indexPath=Join-Path $RepoRoot 'index.html'
$index=Get-Content -Raw -LiteralPath $indexPath -Encoding utf8
foreach($item in $items){
  $id=$item.slug+'-'+$publishDate
  if($index.Contains('"id":"'+$id+'"')){continue}
  $card=[ordered]@{
    id=$id; date=$publishDate; dateLabel='2026.10.03'; category=$item.category
    title=$item.title; digestTitle=$item.title; digestLead=$item.description; excerpt=$item.description
    enTitle=$item.enTitle; enExcerpt=$item.enDescription
    image='assets/images/articles/'+$item.slug+'/'+$item.hero
    url='/articles/'+$item.slug+'/'; imageAlt=$item.imageAlt
  } | ConvertTo-Json -Compress -Depth 4
  $index=[regex]::Replace($index,'const articles = \[','const articles = ['+"`n      "+$card+',' ,1)
  $index=[regex]::Replace($index,'const articleFilters = \{','const articleFilters = {'+"`n      '"+$id+"': []," ,1)
}
[IO.File]::WriteAllText($indexPath,$index,[Text.UTF8Encoding]::new($false))
$sitemapPath=Join-Path $RepoRoot 'sitemap.xml'
$sitemap=Get-Content -Raw -LiteralPath $sitemapPath -Encoding utf8
foreach($item in $items){
  foreach($path in @('articles/','en/articles/')){
    $url='https://www.axis-jp.net/'+$path+$item.slug+'/'
    if(-not $sitemap.Contains($url)){$sitemap=$sitemap.Replace('</urlset>','  <url><loc>'+$url+'</loc><lastmod>'+$publishDate+"</lastmod></url>`n</urlset>")}
  }
}
[IO.File]::WriteAllText($sitemapPath,$sitemap,[Text.UTF8Encoding]::new($false))
$recordDir=Join-Path $RepoRoot 'records\2026\10'
New-Item -ItemType Directory -Force -Path $recordDir | Out-Null
$record=@"
# Owner-approved publication — two reviewed articles

- Published: $publishDate
- Category: ろぶーの気になる事 for both Sony × Berliner Philharmoniker and Kindle 2026.
- Original unpublished draft bundles remain unchanged; the earlier Selection version of the Kindle draft is retained.
- Fact checking: Sony's 2026 partnership and Amazon's 2026 Kindle announcement were checked against the primary links listed on each article page.
- Kindle price and availability are explicitly dated to the 2026-10-01 announcement; the article is not a hands-on review.
- Four AI-generated editorial images are labeled as illustrations, not official or hands-on product photography.
- Kindle purchase links use the site's existing Amazon Associates tag with a visible disclosure. Sony has no affiliate link because no corresponding product or offer was announced.
- User explicitly approved publication after reviewing the two drafts.
"@
[IO.File]::WriteAllText((Join-Path $recordDir '2026-10-03-publish-two-reviewed-articles-v1.md'),$record,[Text.UTF8Encoding]::new($false))
Write-Output 'Built two bilingual articles, four images, homepage cards, sitemap entries, and publication record.'
