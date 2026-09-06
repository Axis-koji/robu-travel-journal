$ErrorActionPreference = 'Stop'

$root = Split-Path $PSScriptRoot -Parent
$shellPath = Join-Path $root 'assets\js\shared-shell.js'
$shell = Get-Content -LiteralPath $shellPath -Raw -Encoding utf8

if ($shell -notmatch 'meta\[property="article:section"\]') {
    Write-Error 'Shared shell does not detect Selection articles from article:section metadata.'
}

if ($shell -notmatch 'legacySelectionArticlePaths') {
    Write-Error 'Shared shell is missing the legacy Selection compatibility fallback.'
}

$selectionPages = @()
$problems = @()
$expectedSelectionSlugs = @(
    'seiko-lukia-liberty-limited-2026', 'sony-ult-tower-7', 'sharp-niah-ai-home',
    'garmin-fenix-9-pro-titanium-inreach', 'seiko-prospex-hbc011j',
    'openai-jalapeno-ai-chip', 'ai-smartglasses-vietnam-travel', 'seiko-presage-bonsai',
    'gopro-mission-1-pro-ils', 'google-pixel-watch-5', 'garmin-cirqa-smart-band',
    'meta-glasses', 'breitling-navitimer-samurai-japan', 'breitling-navitimer-concorde',
    'seiko-astron-hab005j', 'casio-gwr-b3000'
)

Get-ChildItem -Path (Join-Path $root 'articles') -Recurse -Filter index.html | ForEach-Object {
    $html = Get-Content -LiteralPath $_.FullName -Raw -Encoding utf8
    $sectionValue = $null
    foreach ($meta in [regex]::Matches($html, '<meta\b[^>]*>', 'IgnoreCase')) {
        if ($meta.Value -notmatch '(?i)(?:property|name)=["'']article:section["'']') { continue }
        $content = [regex]::Match($meta.Value, 'content="([^"]*)"|content=''([^'']*)''', 'IgnoreCase')
        if ($content.Success) {
            $sectionValue = if ($content.Groups[1].Success) { $content.Groups[1].Value } else { $content.Groups[2].Value }
            break
        }
    }

    if ($sectionValue -and $sectionValue -match "(?i)Robu.+Selection") {
        $selectionPages += $_.FullName
        if ($html -notmatch '/assets/js/shared-shell\.js') {
            $problems += "$($_.FullName): missing shared-shell.js"
        }
        if ($html -notmatch '/assets/js/contact-feedback\.js') {
            $problems += "$($_.FullName): missing contact-feedback.js"
        }
    }
}

if ($selectionPages.Count -eq 0) {
    Write-Error 'No metadata-labelled Selection pages were found.'
}

foreach ($slug in $expectedSelectionSlugs) {
    $page = Join-Path $root "articles\$slug\index.html"
    if (-not (Test-Path -LiteralPath $page)) {
        $problems += "${slug}: article page is missing"
        continue
    }
    $html = Get-Content -LiteralPath $page -Raw -Encoding utf8
    $hasMetadata = $html -match '(?i)article:section[^>]+Selection'
    $hasCategoryLabel = $html -match '(?is)<(?:span|div|p)[^>]*(?:badge|kicker|status|category)[^>]*>[^<]*Selection'
    $isLegacyFallback = $shell -match [regex]::Escape("/articles/$slug/")
    if (-not ($hasMetadata -or $hasCategoryLabel -or $isLegacyFallback)) {
        $problems += "${slug}: Selection category cannot be detected"
    }
}

if ($problems.Count -gt 0) {
    Write-Error ("Selection theme prerequisites failed:`n" + ($problems -join "`n"))
}

$morningArticle = Join-Path $root 'articles\seiko-lukia-liberty-limited-2026\index.html'
if ($selectionPages -notcontains $morningArticle) {
    Write-Error 'The current Seiko LUKIA article was not detected as a Selection article.'
}

Write-Output ("Selection theme detection verified: {0} current pages; {1} metadata-labelled" -f $expectedSelectionSlugs.Count, $selectionPages.Count)
