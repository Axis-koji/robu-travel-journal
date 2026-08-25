(function () {
  'use strict';

  var cssHref = '/assets/css/shared-shell.css?v=20260816-4';
  var homePath = window.location.pathname === '/' || window.location.pathname === '/index.html';
  var articlePath = window.location.pathname.indexOf('/articles/') === 0;
  var selectionArticlePaths = [
    '/articles/google-pixel-watch-5/',
    '/articles/garmin-cirqa-smart-band/',
    '/articles/meta-glasses/',
    '/articles/breitling-navitimer-samurai-japan/',
    '/articles/breitling-navitimer-concorde/',
    '/articles/seiko-astron-hab005j/',
    '/articles/casio-gwr-b3000/'
  ];
  var currentPath = window.location.pathname.replace(/index\.html$/, '');
  var selectionArticle = selectionArticlePaths.indexOf(currentPath) !== -1;

  function ensureStyle() {
    if (document.querySelector('link[data-robu-shared-shell]')) return;
    var link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = cssHref;
    link.setAttribute('data-robu-shared-shell', '');
    document.head.appendChild(link);
  }

  function ensureSelectionTheme() {
    if (!selectionArticle) return;
    document.body.classList.add('robus-selection-page');
    if (document.querySelector('link[data-robu-selection-theme]')) return;
    var link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = '/assets/css/robus-selection-theme.css?v=20260816-2';
    link.setAttribute('data-robu-selection-theme', '');
    document.head.appendChild(link);
  }

  function renderSelectionLabel() {
    if (!selectionArticle) return;
    var heading = document.querySelector('body > main h1, body > article h1, body > header:not(.site-header) h1, body h1');
    if (!heading) return;

    var label = document.createElement('div');
    label.className = 'robu-selection-label';
    label.textContent = "Robu's Selection";

    var existing = document.querySelector('.robu-selection-label, .badge, .draft, .status');
    if (existing && !existing.closest('.contact-feedback')) existing.replaceWith(label);
    else heading.parentNode.insertBefore(label, heading);
  }

  function headerMarkup() {
    return '<header class="site-header robu-common-header" data-robu-common-header>' +
      '<a class="brand" href="/">ろぶーの<span>気になる事</span></a>' +
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
      '<div><a class="brand" href="/">ろぶーの<span>気になる事</span></a><p>日常に、少し旅の気分を。</p></div>' +
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
      '<small>© 2026 ろぶーの気になる事. All rights reserved.</small>' +
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

  function articleHeadingRoot() {
    var main = document.querySelector('body > main');
    if (main) return main.querySelector('article') || main;
    return document.querySelector('body > article');
  }

  function articleLayoutRoot() {
    return document.querySelector('body > main, body > article');
  }

  function uniqueHeadingId(heading, index, usedIds) {
    var currentId = heading.id && heading.id.trim();
    if (currentId && !usedIds[currentId]) {
      usedIds[currentId] = true;
      return currentId;
    }

    var baseId = 'article-section-' + (index + 1);
    var candidate = baseId;
    var suffix = 2;
    while (usedIds[candidate] || document.getElementById(candidate)) {
      candidate = baseId + '-' + suffix;
      suffix += 1;
    }
    heading.id = candidate;
    usedIds[candidate] = true;
    return candidate;
  }

  function renderArticleToc() {
    if (!articlePath || document.querySelector('[data-robu-article-toc]')) return;

    var headingRoot = articleHeadingRoot();
    var layoutRoot = articleLayoutRoot();
    if (!headingRoot || !layoutRoot) return;

    var headings = Array.prototype.filter.call(headingRoot.querySelectorAll('h2'), function (heading) {
      return !heading.closest('.contact-feedback') && heading.textContent.trim();
    });
    if (!headings.length) return;

    var usedIds = {};
    var aside = document.createElement('aside');
    aside.className = 'robu-article-toc';
    aside.setAttribute('data-robu-article-toc', '');
    aside.setAttribute('aria-label', 'この記事の目次');

    var details = document.createElement('details');
    details.className = 'robu-article-toc-details';
    details.open = true;

    var summary = document.createElement('summary');
    summary.textContent = 'この記事の目次';
    details.appendChild(summary);

    var nav = document.createElement('nav');
    nav.setAttribute('aria-label', '記事内の見出し');
    var list = document.createElement('ol');

    headings.forEach(function (heading, index) {
      var id = uniqueHeadingId(heading, index, usedIds);
      var item = document.createElement('li');
      var link = document.createElement('a');
      link.href = '#' + id;
      link.textContent = heading.textContent.trim();
      link.setAttribute('data-robu-toc-link', id);
      item.appendChild(link);
      list.appendChild(item);
    });

    nav.appendChild(list);
    details.appendChild(nav);
    aside.appendChild(details);

    // Keep the sticky table of contents inside the article region so it
    // naturally stops before the shared footer instead of overlapping it.
    var articleLayout = document.createElement('div');
    articleLayout.className = 'robu-article-layout';
    articleLayout.setAttribute('data-robu-article-layout', '');
    document.body.insertBefore(articleLayout, layoutRoot);
    articleLayout.appendChild(aside);
    articleLayout.appendChild(layoutRoot);
    document.body.classList.add('has-robu-article-toc');

    var desktopQuery = window.matchMedia('(min-width: 1101px)');
    function keepDesktopTocOpen(event) {
      if (event.matches) details.open = true;
    }
    keepDesktopTocOpen(desktopQuery);
    if (desktopQuery.addEventListener) desktopQuery.addEventListener('change', keepDesktopTocOpen);

    var links = aside.querySelectorAll('[data-robu-toc-link]');
    if ('IntersectionObserver' in window) {
      var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          Array.prototype.forEach.call(links, function (link) {
            link.classList.toggle('is-current', link.getAttribute('data-robu-toc-link') === entry.target.id);
          });
        });
      }, { rootMargin: '-18% 0px -68% 0px', threshold: 0 });
      headings.forEach(function (heading) { observer.observe(heading); });
    }
  }

  function init() {
    ensureStyle();
    ensureSelectionTheme();
    renderHeader();
    renderSelectionLabel();
    renderFooter();
    renderArticleToc();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
}());
