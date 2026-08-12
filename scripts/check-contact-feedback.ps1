$ErrorActionPreference = 'Stop'

$articlePages = Get-ChildItem -Path (Join-Path $PSScriptRoot '..\articles') -Recurse -Filter index.html
$missing = @()

foreach ($page in $articlePages) {
    $html = Get-Content -LiteralPath $page.FullName -Raw -Encoding utf8
    $hasDirectLoader = $html -match '/assets/js/contact-feedback\.js'
    $hasSharedLoader = $html -match '/assets/js/site\.js'

    if (-not ($hasDirectLoader -or $hasSharedLoader)) {
        $missing += $page.FullName
    }
}

if ($missing.Count -gt 0) {
    Write-Error ("Article pages missing the shared contact form loader:`n" + ($missing -join "`n"))
}

Write-Output ("Contact form loader verified: {0} article pages" -f $articlePages.Count)
