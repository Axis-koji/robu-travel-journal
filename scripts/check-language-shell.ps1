$ErrorActionPreference = 'Stop'

$projectRoot = Split-Path -Parent $PSScriptRoot
$targets = Get-ChildItem -LiteralPath $projectRoot -Recurse -File -Filter '*.html' |
  Where-Object {
    $_.FullName -notmatch '[\\/]wordpress-published[\\/]' -and
    $_.FullName -notmatch '[\\/]backups?[\\/]'
  }

$errors = New-Object System.Collections.Generic.List[string]
foreach ($file in $targets) {
  $content = [System.IO.File]::ReadAllText($file.FullName)
  $styleCount = ([regex]::Matches($content, '/assets/css/site-language\.css')).Count
  $scriptCount = ([regex]::Matches($content, '/assets/js/site-language\.js')).Count
  if ($styleCount -ne 1) { $errors.Add("style=$styleCount $($file.FullName)") }
  if ($scriptCount -ne 1) { $errors.Add("script=$scriptCount $($file.FullName)") }
}

$protected = Get-ChildItem -LiteralPath $projectRoot -Recurse -File -Filter '*.html' |
  Where-Object { $_.FullName -match '[\\/]wordpress-published[\\/]' }
foreach ($file in $protected) {
  $content = [System.IO.File]::ReadAllText($file.FullName)
  if ($content -match '/assets/(css|js)/site-language\.') {
    $errors.Add("protected-file-changed $($file.FullName)")
  }
}

if ($errors.Count -gt 0) {
  $errors | ForEach-Object { Write-Error $_ }
  exit 1
}

Write-Output "Verified $($targets.Count) public HTML files; protected WordPress source copies are untouched."
