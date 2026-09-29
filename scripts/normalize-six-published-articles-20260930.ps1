param([string]$RepoRoot = (Split-Path -Parent $PSScriptRoot))

$ErrorActionPreference = 'Stop'
$slugs = @(
  'ai-recommendation-link-safety',
  'digital-ad-supply-chain-transparency',
  'jnto-baki-smart-travel-tips',
  'notta-memo-pro-buying-guide',
  'ricoh-gr-iv-30th-anniversary',
  'wakoh-signatures-watch'
)
$selectionSlugs = @('notta-memo-pro-buying-guide', 'ricoh-gr-iv-30th-anniversary', 'wakoh-signatures-watch')
$affiliatePattern = '(?s)<h2 id="(?<id>[^"]+)">(?<heading>[^<]+)</h2>\r?\n<ul>\r?\n(?<items>(?:<li><a [^\r\n]+</a></li>\r?\n){3})</ul>\r?\n<p><em>(?<disclosure>[^<]+)</em></p>'
$inlineStylePattern = '(?s)<style>\.article-content ul:has\(a\[href\*="womaster-22"\]\).*?</style>\r?\n'
$utf8 = [System.Text.UTF8Encoding]::new($false)

foreach ($language in @('ja', 'en')) {
  foreach ($slug in $slugs) {
    $relative = if ($language -eq 'ja') { "articles/$slug/index.html" } else { "en/articles/$slug/index.html" }
    $path = Join-Path $RepoRoot $relative
    $html = [System.IO.File]::ReadAllText($path, $utf8)
    $selection = $selectionSlugs -contains $slug
    if ($html.Contains('robu-published-article')) { throw "Already normalized: $relative" }
    $styleMatches = [regex]::Matches($html, $inlineStylePattern)
    $affiliateMatches = [regex]::Matches($html, $affiliatePattern)
    if ($styleMatches.Count -ne 1 -or $affiliateMatches.Count -ne 1) {
      throw "Expected one inline style and one affiliate block in $relative; found $($styleMatches.Count) and $($affiliateMatches.Count)"
    }
    $match = $affiliateMatches[0]
    $links = [regex]::Matches($match.Groups['items'].Value, '<li>(<a [^\r\n]+</a>)</li>')
    if ($links.Count -ne 3) { throw "Expected three affiliate anchors: $relative" }
    $shopClasses = @('amazon', 'rakuten', 'yahoo')
    $buttons = for ($index = 0; $index -lt 3; $index++) {
      $anchor = $links[$index].Groups[1].Value
      $anchor -replace '^<a ', "<a class=`"robu-marketplace-button $($shopClasses[$index])`" "
    }
    $heading = if ($selection) {
      if ($language -eq 'ja') { '購入先を確認する' } else { 'Check where to buy' }
    } else {
      $match.Groups['heading'].Value.Replace('（広告）', '').Replace(' (affiliate links)', '')
    }
    $sectionAttr = if ($selection) { ' data-selection-purchase-standard="astron-hab005j"' } else { '' }
    $disclosure = $match.Groups['disclosure'].Value
    $standardDisclosure = if ($language -eq 'ja') {
      '掲載している各販売先へのリンクはアフィリエイトリンクです。購入等により当サイトに報酬が発生する場合があります。価格・在庫・販売元は各ページでご確認ください。'
    } else {
      'These are affiliate links. We may earn a commission from qualifying purchases. Check each store for current prices, availability and seller details.'
    }
    $leadDisclosure = if ($selection) { $standardDisclosure } else { $disclosure }
    $additionalNote = if ($selection) { "`n<p class=`"purchase-note`"><em>$disclosure</em></p>" } else { '' }
    $replacement = "<section class=`"robu-marketplace-section`"$sectionAttr>`n<h2 id=`"$($match.Groups['id'].Value)`">$heading</h2>`n<p class=`"note`" data-purchase-disclosure>$leadDisclosure</p>`n<div class=`"robu-marketplace-buttons`">`n$($buttons -join "`n")`n</div>$additionalNote`n</section>"
    $html = $html.Remove($match.Index, $match.Length).Insert($match.Index, $replacement)
    $html = [regex]::Replace($html, $inlineStylePattern, '', 1)
    $html = $html.Replace('<body class="draft-preview', '<body class="draft-preview robu-published-article')
    $html = [regex]::Replace($html, '/assets/js/shared-shell\.js\?v=[^"\s]+', '/assets/js/shared-shell.js?v=20260930-layout-affiliate-2')
    if (-not $html.Contains('robu-published-article')) { throw "Body class failed: $relative" }
    [System.IO.File]::WriteAllText($path, $html, $utf8)
    Write-Output "Normalized $relative"
  }
}
