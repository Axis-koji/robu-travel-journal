$ErrorActionPreference = 'Stop'

$projectRoot = Split-Path -Parent $PSScriptRoot
$utf8NoBom = [System.Text.UTF8Encoding]::new($false)
$styleTag = '  <link rel="stylesheet" href="/assets/css/site-language.css">'
$scriptTag = '  <script src="/assets/js/site-language.js"></script>'

$targets = Get-ChildItem -LiteralPath $projectRoot -Recurse -File -Filter '*.html' |
  Where-Object {
    $_.FullName -notmatch '[\\/]wordpress-published[\\/]' -and
    $_.FullName -notmatch '[\\/]backups?[\\/]'
  }

foreach ($file in $targets) {
  $content = [System.IO.File]::ReadAllText($file.FullName, $utf8NoBom)

  if ($content -notmatch '/assets/css/site-language\.css') {
    if ($content -notmatch '</head>') {
      throw "Missing </head>: $($file.FullName)"
    }
    $content = $content -replace '</head>', "$styleTag`r`n</head>"
  }

  if ($content -notmatch '/assets/js/site-language\.js') {
    if ($content -notmatch '</body>') {
      throw "Missing </body>: $($file.FullName)"
    }
    $content = $content -replace '</body>', "$scriptTag`r`n</body>"
  }

  [System.IO.File]::WriteAllText($file.FullName, $content, $utf8NoBom)
}

Write-Output "Updated $($targets.Count) HTML files."
