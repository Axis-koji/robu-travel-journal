$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$shell = Get-Content (Join-Path $root 'assets\js\shared-shell.js') -Raw -Encoding utf8
$expected = @(
  'sony-ult-tower-7', 'garmin-fenix-9-pro-titanium-inreach', 'seiko-prospex-hbc011j',
  'seiko-presage-bonsai', 'gopro-mission-1-pro-ils', 'google-pixel-watch-5',
  'breitling-navitimer-samurai-japan', 'breitling-navitimer-concorde',
  'seiko-astron-hab005j', 'casio-gwr-b3000'
)
foreach ($slug in $expected) {
  if ($shell -notmatch [regex]::Escape("'/articles/$slug/':")) { Write-Error "Missing Amazon mapping: $slug" }
}
if ($shell -match [regex]::Escape("'/articles/garmin-cirqa-smart-band/':")) { Write-Error 'Noindex Garmin CIRQA must not have an Amazon mapping.' }
if ($shell -notmatch "link\.rel = 'nofollow sponsored noopener noreferrer'") { Write-Error 'Amazon links are missing required rel attributes.' }
if ($shell -notmatch "disclosure\.className = 'note'") { Write-Error 'Per-article disclosure is missing.' }
if ($shell -notmatch [regex]::Escape("https://room.rakuten.co.jp/room_4b003bc175/1700392030842251")) { Write-Error 'Verified HBC011J Rakuten ROOM link is missing.' }
if ($shell -notmatch "rakutenLink\.rel = 'nofollow sponsored noopener noreferrer'") { Write-Error 'Rakuten ROOM links are missing required rel attributes.' }

$legal = Get-Content (Join-Path $root 'advertising-disclaimer\index.html') -Raw -Encoding utf8
if (([regex]::Matches($legal, 'amazon-associates-disclosure:start')).Count -ne 1 -or
    ([regex]::Matches($legal, 'amazon-associates-disclosure:end')).Count -ne 1) {
  Write-Error 'Amazon Associates disclosure markers must occur exactly once.'
}
if ($legal -notmatch 'Amazon\.co\.jp' -or $legal -notmatch 'amazon-associates-disclosure') { Write-Error 'Amazon Associates participant statement is missing.' }
Write-Output 'Amazon affiliate mappings verified: 10 articles; CIRQA excluded'
