(function () {
  'use strict';

  var cssHref = '/assets/css/shared-shell.css?v=20260816-2';
  var homePath = window.location.pathname === '/' || window.location.pathname === '/index.html';

  function ensureStyle() {
    if (document.querySelector('link[data-robu-shared-shell]')) return;
    var link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = cssHref;
    link.setAttribute('data-robu-shared-shell', '');
    document.head.appendChild(link);
  }

  function headerMarkup() {
    return '<header class="site-header robu-common-header" data-robu-common-header>' +
      '<a class="brand" href="/">ろぶーの<span>気になること</span></a>' +
      '<button class="menu-toggle" type="button" aria-label="メニューを開く" aria-expanded="false" aria-controls="robuCommonNavigation">☰</button>' +
      '<nav class="main-nav" id="robuCommonNavigation" aria-label="メインナビゲーション">' +
      '<a href="/">ホーム</a>' +
      '<a href="/#gourmet">グルメ</a>' +
      '<a href="/#vehicles">乗り物</a>' +
      '<a href="/#travel">旅行</a>' +
      '<a href="/#hotel">ホテル</a>' +
      '<a href="/#selection">Robu\'s Selection</a>' +
      '<a href="/about/">運営者</a>' +
      '</nav></header>';
  }

  function footerMarkup() {
    return '<footer class="site-footer robu-common-footer" data-robu-common-footer>' +
      '<div><a class="brand" href="/">ろぶーの<span>気になること</span></a><p>日常に、少し旅の気分を。</p></div>' +
      '<div class="footer-links">' +
      '<a href="/about/">運営者情報</a>' +
      '<a href="/privacy-policy/">プライバシーポリシー</a>' +
      '<a href="/terms/">利用規約</a>' +
      '<a href="/advertising-disclaimer/">広告・免責事項</a>' +
      '<a href="/contact/">お問い合わせ</a>' +
      '<a href="/sitemap/">サイトマップ</a>' +
      '</div>' +
      '<div class="social-links" aria-label="SNSリンク">' +
      '<a class="social-link social-facebook" href="https://www.facebook.com/" target="_blank" rel="noopener noreferrer" aria-label="Facebookを開く">Facebook</a>' +
      '<a class="social-link social-instagram" href="https://www.instagram.com/" target="_blank" rel="noopener noreferrer" aria-label="Instagramを開く">Instagram</a>' +
      '<a class="social-link social-x" href="https://x.com/" target="_blank" rel="noopener noreferrer" aria-label="Xを開く">X</a>' +
      '</div>' +
      '<small>© 2026 ろぶーの気になること. All rights reserved.</small>' +
      '</footer>';
  }

  function elementFrom(markup) {
    var template = document.createElement('template');
    template.innerHTML = markup.trim();
    return template.content.firstElementChild;
  }

  function renderHeader() {
    if (homePath) return;
    var header = elementFrom(headerMarkup());
    var current = document.querySelector('body > header.site-header');
    if (current) current.replaceWith(header);
    else document.body.insertBefore(header, document.body.firstChild);

    var toggle = header.querySelector('.menu-toggle');
    var nav = header.querySelector('.main-nav');
    toggle.addEventListener('click', function () {
      var open = toggle.getAttribute('aria-expanded') !== 'true';
      toggle.setAttribute('aria-expanded', String(open));
      toggle.setAttribute('aria-label', open ? 'メニューを閉じる' : 'メニューを開く');
      nav.classList.toggle('is-open', open);
    });
  }

  function renderFooter() {
    var footer = elementFrom(footerMarkup());
    var current = document.querySelector('body > footer');
    if (current) current.replaceWith(footer);
    else document.body.appendChild(footer);
  }

  function init() {
    ensureStyle();
    renderHeader();
    renderFooter();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
}());
