$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$html = Get-Content -LiteralPath (Join-Path $root 'index.html') -Raw -Encoding utf8
$articles = [regex]::Match($html, '(?s)const articles = \[(.*?)\n\s*\];').Groups[1].Value
$filters = [regex]::Match($html, '(?s)const articleFilters = \{(.*?)\n\s*\};').Groups[1].Value
if (-not $articles -or -not $filters) { throw 'Article catalogue or category mapping could not be parsed.' }
$ids = [regex]::Matches($articles, '(?:["'']id["'']|\bid)\s*:\s*["'']([^"'']+)["'']') | ForEach-Object { $_.Groups[1].Value }
$entries = [regex]::Matches($filters, '["'']([^"'']+)["'']\s*:\s*\[([^\]]*)\]')
$registered = @{}
foreach ($entry in $entries) {
    $key = $entry.Groups[1].Value
    if ($registered.ContainsKey($key)) { throw "Duplicate category mapping: $key" }
    $registered[$key] = $entry.Groups[2].Value
    foreach ($tag in [regex]::Matches($entry.Groups[2].Value, '["'']([^"'']+)["'']')) {
        if ($tag.Groups[1].Value -notin @('gourmet','travel','hotel','vehicles','selection')) { throw "Unknown category for $key" }
    }
}
if ($ids.Count -eq 0) { throw 'No article IDs found.' }
$missing = @($ids | Where-Object { -not $registered.ContainsKey($_) })
if ($missing.Count) { throw "Articles missing explicit category registration: $($missing -join ', ')" }
Write-Output "Category registration verified: $($ids.Count) articles. Empty arrays explicitly mean all-articles only."
