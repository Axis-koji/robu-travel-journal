$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$articleDir = Join-Path $root 'articles\soufuren-kyoto-shichijo-omiya'
$article = Join-Path $articleDir 'index.html'
$html = Get-Content -LiteralPath $article -Raw -Encoding utf8

$jsonBlock = [regex]::Match($html, '<script type="application/ld\+json">(.*?)</script>', 'Singleline')
if (-not $jsonBlock.Success) { Write-Error 'JSON-LD block is missing.' }
$null = $jsonBlock.Groups[1].Value | ConvertFrom-Json

[xml](Get-Content -LiteralPath (Join-Path $root 'sitemap.xml') -Raw -Encoding utf8) | Out-Null
foreach ($name in @('soufuren-storefront.jpg','soufuren-menu.jpg','soufuren-counter-kitchen.jpg','soufuren-cooking-philosophy.jpg','soufuren-noodles-on-griddle.jpg','soufuren-noodles-browning.jpg','soufuren-yakisoba-finishing.jpg','soufuren-takeout-yakisoba.jpg','soufuren-yakisoba-video.mp4')) {
  if (-not (Test-Path -LiteralPath (Join-Path $articleDir $name))) { Write-Error "Missing media: $name" }
  if ($html -notmatch [regex]::Escape($name)) { Write-Error "Unreferenced media: $name" }
}
if (($html | Select-String -Pattern '/assets/js/contact-feedback.js' -AllMatches).Matches.Count -ne 1) { Write-Error 'Contact loader must occur once.' }
if ($html -match 'noindex') { Write-Error 'Article must be indexable.' }
Write-Output 'Soufuren article structure and media verified.'
