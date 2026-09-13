$ErrorActionPreference = 'Stop'

$root = Split-Path $PSScriptRoot -Parent
$articlePages = Get-ChildItem -Path (Join-Path $root 'articles') -Recurse -Filter index.html
$shellPath = Join-Path $root 'assets\js\shared-shell.js'
$stylePath = Join-Path $root 'assets\css\shared-shell.css'
$shell = Get-Content -LiteralPath $shellPath -Raw -Encoding utf8
$style = Get-Content -LiteralPath $stylePath -Raw -Encoding utf8
$problems = @()

foreach ($page in $articlePages) {
    $html = Get-Content -LiteralPath $page.FullName -Raw -Encoding utf8
    if ($html -notmatch '/assets/js/shared-shell\.js') {
        $problems += "$($page.FullName): missing shared-shell.js"
    }

    if ($html -match 'Content-Security-Policy') {
        $requiredCspText = @(
            'https://www.axis-jp.net',
            'https://www.gstatic.com',
            'https://translate.googleapis.com',
            'https://translate-pa.googleapis.com'
        )

        foreach ($required in $requiredCspText) {
            if (-not $html.Contains($required)) {
                $problems += "$($page.FullName): CSP blocks Google website translation dependency: $required"
            }
        }
    }
}

$requiredShellText = @(
    'robu-language-picker',
    'translate.google.com/translate',
    "{ code: 'ja', label: '日本語' }",
    "{ code: 'en', label: 'English' }"
)

foreach ($required in $requiredShellText) {
    if (-not $shell.Contains($required)) {
        $problems += "shared-shell.js: missing required translation setting: $required"
    }
}

$retiredShellText = @(
    "{ code: 'zh-CN'",
    "{ code: 'zh-TW'",
    "{ code: 'yue'",
    "{ code: 'vi'"
)

foreach ($retired in $retiredShellText) {
    if ($shell.Contains($retired)) {
        $problems += "shared-shell.js: retired translation setting remains: $retired"
    }
}

$requiredStyles = @('.robu-header-tools', '.robu-language-picker', '.robu-language-menu')
foreach ($required in $requiredStyles) {
    if (-not $style.Contains($required)) {
        $problems += "shared-shell.css: missing required translation style: $required"
    }
}

if ($problems.Count -gt 0) {
    Write-Error ("Article shell verification failed:`n" + ($problems -join "`n"))
}

Write-Output ("Article shell and translation menu verified: {0} article pages" -f $articlePages.Count)
