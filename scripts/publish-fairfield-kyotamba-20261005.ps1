param([string]$RepoRoot = (Split-Path -Parent $PSScriptRoot))
$ErrorActionPreference = 'Stop'
$draftDir = 'E:\Documents\ろぶーの気になる事（記事）\フェアフィールド京丹波\draft-20261005-v1'
$mediaDir = Split-Path -Parent $draftDir
$slug = 'fairfield-by-marriott-kyoto-kyotamba-stay'
$publishDate = '2026-10-05'
$titleJa = 'フェアフィールド京都京丹波宿泊記｜道の駅の食と温泉を楽しむ一泊'
$titleEn = 'A Night at Fairfield by Marriott Kyoto Kyotamba: Local Food, Hot Springs and a Roadside-Station Breakfast'
$descriptionJa = 'フェアフィールド・バイ・マリオット京都京丹波の実宿泊記。スプリングスひよしの温泉、味夢の里の黒豆うどん、栗おこわなど、道の駅と地域の食を楽しんだ一泊を紹介します。'
$descriptionEn = 'A firsthand stay at Fairfield by Marriott Kyoto Kyotamba, including Springs Hiyoshi, black soybean udon, local snacks and an outdoor roadside-station breakfast.'
$categoryJa = 'ろぶーの気になる事 / 旅行・宿泊'
$categoryEn = "Robu's Curiosities / Travel & Hotels"
$hero = 'IMG_20260927_111945.jpg'
$images = @('IMG_20260927_111945.jpg','IMG_20260926_182842.jpg','IMG_20260926_191544.jpg','IMG_20260926_203500.jpg','IMG_20260926_161741.jpg','IMG_20260927_182150.jpg','IMG_20260927_125451.jpg')
$videoMap = [ordered]@{
  'VID_20260927_125742.mp4'='VID_20260927_125742-muted-720p.webm'
  'VID_20260926_202841.mp4'='VID_20260926_202841-muted-720p.webm'
  'VID_20260926_200652.mp4'='VID_20260926_200652-muted-720p.webm'
}
function Escape-Html([string]$v){[System.Net.WebUtility]::HtmlEncode($v)}
function Read-Body([string]$path){
  $raw=Get-Content -Raw -LiteralPath $path -Encoding utf8
  if($raw -notmatch '(?s)^---\s*\r?\n.*?\r?\n---\s*\r?\n(.*)$'){throw "Missing front matter: $path"}
  $body=$matches[1]
  if($body -match '(?i)公開前メモ|Pre-publication note|publishApproved'){throw "Draft-only content remains: $path"}
  return $body.Replace("## Robu’s verdict","## Robu’s Take")
}
function Build-Page([string]$language){
  $source=Join-Path $draftDir $(if($language -eq 'ja'){'article-ja.md'}else{'article-en.md'})
  $html=(ConvertFrom-Markdown -InputObject (Read-Body $source)).Html
  $html=[regex]::Replace($html,'(?s)^\s*<h1[^>]*>.*?</h1>\s*','')
  $imageDir=Join-Path $RepoRoot ('assets\images\articles\'+$slug); New-Item -ItemType Directory -Force -Path $imageDir|Out-Null
  foreach($image in $images){$src=Join-Path $mediaDir $image;if(!(Test-Path $src)){throw "Missing image: $src"};Copy-Item $src (Join-Path $imageDir $image) -Force;$html=$html.Replace('../'+$image,'/assets/images/articles/'+$slug+'/'+$image)}
  $videoDir=Join-Path $RepoRoot ('assets\videos\articles\'+$slug)
  foreach($old in $videoMap.Keys){$new=$videoMap[$old];$video=Join-Path $videoDir $new;if(!(Test-Path $video)){throw "Missing web video: $video"};$html=$html.Replace('../'+$old,'/assets/videos/articles/'+$slug+'/'+$new)}
  $html=[regex]::Replace($html,'<video controls playsinline preload="metadata"','<video controls playsinline muted preload="metadata"')
  $html=[regex]::Replace($html,'<a href="(https://hb\.afl\.rakuten\.co\.jp/[^"]+)"','<a class="rakuten-cta" href="$1" target="_blank" rel="nofollow sponsored noopener noreferrer"')
  $title=if($language -eq 'ja'){$titleJa}else{$titleEn};$desc=if($language -eq 'ja'){$descriptionJa}else{$descriptionEn};$cat=if($language -eq 'ja'){$categoryJa}else{$categoryEn}
  $prefix=if($language -eq 'ja'){'articles/'}else{'en/articles/'};$canonical='https://www.axis-jp.net/'+$prefix+$slug+'/';$jaUrl='https://www.axis-jp.net/articles/'+$slug+'/';$enUrl='https://www.axis-jp.net/en/articles/'+$slug+'/'
  $imageUrls=@($images|ForEach-Object{'https://www.axis-jp.net/assets/images/articles/'+$slug+'/'+$_})
  $schema=[ordered]@{'@context'='https://schema.org';'@type'='BlogPosting';headline=$title;description=$desc;datePublished=$publishDate;dateModified=$publishDate;inLanguage=$(if($language -eq 'ja'){'ja-JP'}else{'en'});mainEntityOfPage=[ordered]@{'@type'='WebPage';'@id'=$canonical};image=$imageUrls;articleSection=$cat;author=[ordered]@{'@type'='Organization';name='ろぶーの気になる事'};publisher=[ordered]@{'@type'='Organization';name='ろぶーの気になる事';url='https://www.axis-jp.net/'};isAccessibleForFree=$true}|ConvertTo-Json -Compress -Depth 6
  $locale=if($language -eq 'ja'){'ja_JP'}else{'en_US'};$alt=if($language -eq 'ja'){'フェアフィールド京都京丹波の屋外テーブルに並べた栗おこわ、卵、藤稔などの朝食'}else{'Outdoor breakfast at Fairfield Kyoto Kyotamba with chestnut okowa, eggs and Fujiminori grapes'}
  $page=@"
<!doctype html><html lang="$language" translate="no"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="google" content="notranslate"><meta name="social:publish" content="false"><meta name="referrer" content="strict-origin-when-cross-origin"><meta name="robots" content="index,follow,max-image-preview:large"><title>$(Escape-Html $title)</title><meta name="description" content="$(Escape-Html $desc)"><link rel="canonical" href="$canonical"><link rel="alternate" hreflang="ja" href="$jaUrl"><link rel="alternate" hreflang="en" href="$enUrl"><link rel="alternate" hreflang="x-default" href="$jaUrl"><meta property="og:type" content="article"><meta property="og:locale" content="$locale"><meta property="og:site_name" content="ろぶーの気になる事"><meta property="og:title" content="$(Escape-Html $title)"><meta property="og:description" content="$(Escape-Html $desc)"><meta property="og:url" content="$canonical"><meta property="og:image" content="$($imageUrls[0])"><meta property="og:image:alt" content="$(Escape-Html $alt)"><meta property="article:section" content="$(Escape-Html $cat)"><meta property="article:published_time" content="${publishDate}T00:00:00+09:00"><meta property="article:modified_time" content="${publishDate}T00:00:00+09:00"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="$(Escape-Html $title)"><meta name="twitter:description" content="$(Escape-Html $desc)"><meta name="twitter:image" content="$($imageUrls[0])"><link rel="stylesheet" href="/assets/css/contact-feedback-ees-standard.css?v=3" data-contact-feedback-style><link rel="stylesheet" href="/assets/css/draft-article-preview.css?v=20260930-publish-five-1"><style>.article-content img,.article-content video{display:block;max-width:100%;height:auto;margin-inline:auto;border-radius:10px}.article-content video{width:100%;max-height:75vh;background:#111}.article-content table{display:block;max-width:100%;overflow-x:auto}.rakuten-cta{display:block;max-width:520px;margin:1.5rem auto;padding:1rem;text-align:center;background:#bf0000;color:#fff!important;border-radius:8px;font-weight:700;text-decoration:none}.article-content>p:last-child{font-size:.84rem;color:#5f6d70}</style><script type="application/ld+json">$schema</script><script defer src="/assets/js/shared-shell.js?v=20261003-desktop-left-toc-1"></script></head><body class="draft-preview robu-published-article"><main class="draft-main" data-contact-page><article><div class="selection-subcategory" data-article-category>$(Escape-Html $cat)</div><h1 class="article-title">$(Escape-Html $title)</h1><div class="article-content">$html</div></article></main><script src="/assets/js/contact-feedback.js?v=20260907-1"></script></body></html>
"@
  $target=Join-Path $RepoRoot ($prefix.Replace('/','\')+$slug);New-Item -ItemType Directory -Force -Path $target|Out-Null;[IO.File]::WriteAllText((Join-Path $target 'index.html'),$page,[Text.UTF8Encoding]::new($false))
}
Build-Page 'ja';Build-Page 'en'
$id=$slug+'-'+$publishDate;$indexPath=Join-Path $RepoRoot 'index.html';$index=Get-Content -Raw $indexPath -Encoding utf8
if(!$index.Contains('"id":"'+$id+'"')){$card=[ordered]@{id=$id;date=$publishDate;dateLabel='2026.10.05';category=$categoryJa;title=$titleJa;digestTitle='道の駅の食と温泉で楽しむ、京丹波の一泊';digestLead='実際に泊まり、黒豆うどん、栗おこわ、温泉、緑の景色まで体験しました。';excerpt=$descriptionJa;enTitle=$titleEn;enExcerpt=$descriptionEn;image='assets/images/articles/'+$slug+'/'+$hero;url='/articles/'+$slug+'/';imageAlt='フェアフィールド京都京丹波で楽しんだ京丹波の朝食'}|ConvertTo-Json -Compress -Depth 4;$index=[regex]::Replace($index,'const articles = \[','const articles = ['+"`n      "+$card+',',1);$index=[regex]::Replace($index,'const articleFilters = \{','const articleFilters = {'+"`n      '"+$id+"': ['travel','hotel'],",1);[IO.File]::WriteAllText($indexPath,$index,[Text.UTF8Encoding]::new($false))}
$map=Join-Path $RepoRoot 'sitemap.xml';$xml=Get-Content -Raw $map -Encoding utf8;foreach($p in @('articles/','en/articles/')){$url='https://www.axis-jp.net/'+$p+$slug+'/';if(!$xml.Contains($url)){$xml=$xml.Replace('</urlset>','  <url><loc>'+$url+'</loc><lastmod>'+$publishDate+"</lastmod></url>`n</urlset>")}};[IO.File]::WriteAllText($map,$xml,[Text.UTF8Encoding]::new($false))
$htmlMap=Join-Path $RepoRoot 'sitemap\index.html';$sm=Get-Content -Raw $htmlMap -Encoding utf8;if(!$sm.Contains('/articles/'+$slug+'/')){$needle='<h2>ホテル・グルメ</h2>';$links=$needle+"`r`n        <ul>`r`n          <li><a href=`"/articles/$slug/`">$(Escape-Html $titleJa)</a></li>`r`n          <li><a href=`"/en/articles/$slug/`">$(Escape-Html $titleEn) (English)</a></li>";$sm=$sm.Replace($needle+"`r`n        <ul>",$links);[IO.File]::WriteAllText($htmlMap,$sm,[Text.UTF8Encoding]::new($false))}
$cave=Join-Path $RepoRoot 'articles\shizushi-drive\index.html';$ch=Get-Content -Raw $cave -Encoding utf8;$old='<p>こちらは今回の宿泊体験の紹介ではなく、ドライブの拠点としてのご案内です。お部屋や設備、宿泊プラン、空室状況を確かめながら、旅の予定に合うか検討してみてください。</p>';$new='<p>実際に宿泊した記録は、<a href="/articles/'+$slug+'/">フェアフィールド京都京丹波宿泊記｜道の駅の食と温泉を楽しむ一泊</a>にまとめました。温泉、夕食、部屋、翌朝の地元朝食まで写真と動画で紹介しています。</p>';$ch=$ch.Replace($old,$new);[IO.File]::WriteAllText($cave,$ch,[Text.UTF8Encoding]::new($false))
$recordDir=Join-Path $RepoRoot 'records\2026\10';New-Item -ItemType Directory -Force -Path $recordDir|Out-Null;$record=@"
# Owner-approved publication — Fairfield Kyoto Kyotamba stay

- Publication date: 2026-10-05
- Category: ろぶーの気になる事 / 旅行・宿泊
- The owner explicitly approved publication after reviewing the local draft.
- Japanese and English articles were checked against seven official sources; first-person claims are clearly separated from current official facility information.
- Seven owner photographs and three muted, web-compressed owner videos are included. Original media remains unchanged.
- One disclosed Rakuten Travel affiliate link is present with sponsored/nofollow attributes. No Marriott Bonvoy Amex referral link is used.
- The earlier Shizushi Cave article now links to this firsthand hotel stay; this article links back to the cave article.
- No SNS publication action was requested or performed.
"@;[IO.File]::WriteAllText((Join-Path $recordDir '2026-10-05-publish-fairfield-kyotamba-v1.md'),$record,[Text.UTF8Encoding]::new($false))
Write-Output 'Built bilingual Fairfield article, media, homepage card, reciprocal link, sitemaps, and publication record.'
