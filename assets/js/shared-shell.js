(function () {
  'use strict';

  var analyticsMeasurementId = 'G-609VD0NVVF';
  var consentStorageKey = 'robu_google_consent_v1';

  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };

  function readStoredConsent() {
    try {
      return window.localStorage.getItem(consentStorageKey);
    } catch (error) {
      return null;
    }
  }

  function storeConsent(value) {
    try {
      window.localStorage.setItem(consentStorageKey, value);
    } catch (error) {
      // Continue with the visitor's choice for the current page.
    }
  }

  var storedConsent = readStoredConsent();
  window.gtag('consent', 'default', {
    analytics_storage: storedConsent === 'granted' ? 'granted' : 'denied',
    ad_storage: 'denied',
    ad_user_data: 'denied',
    ad_personalization: 'denied',
    wait_for_update: 500
  });

  var cssHref = '/assets/css/shared-shell.css?v=20260913-formal-2';
  var selectionCssHref = '/assets/css/robus-selection-theme.css?v=20260913-formal-2';
  var homePath = window.location.pathname === '/' || window.location.pathname === '/index.html';
  var articlePath = window.location.pathname.indexOf('/articles/') === 0;
  // Older Selection pages predate article:section metadata. Keep them as a
  // compatibility fallback, while new pages are detected from their category.
  var legacySelectionArticlePaths = [
    '/articles/seiko-prospex-hbc011j/',
    '/articles/google-pixel-watch-5/',
    '/articles/garmin-cirqa-smart-band/',
    '/articles/meta-glasses/',
    '/articles/breitling-navitimer-samurai-japan/',
    '/articles/breitling-navitimer-concorde/',
    '/articles/seiko-astron-hab005j/',
    '/articles/casio-gwr-b3000/'
  ];
  var regularArticleNavigation = {
    '/articles/kyoto-favorite-unagi-day/': 'gourmet',
    '/articles/soufuren-kyoto-shichijo-omiya/': 'gourmet',
    '/articles/android-motion-assist-guided-vision/': 'vehicles',
    '/articles/aoi-noen-fruit-cafe/': 'gourmet',
    '/articles/jr-east-midori-no-madoguchi-ai/': 'vehicles',
    '/articles/vietnam-japan-travel-news/': 'travel',
    '/articles/news-coffee-plus-20260826/': 'gourmet',
    '/articles/nasa-coffies-solar-ai/': 'travel',
    '/articles/europe-ees-etias-guide/': 'travel',
    '/articles/2026-08-09-spain-eclipse/': 'travel',
    '/articles/2026-08-08-travel-vietnam-hotel-digest/': 'travel',
    '/articles/suma-seaworld-hotel/': 'hotel',
    '/articles/hong-kong-dim-sum-shiki/': 'gourmet',
    '/articles/vietnam-coffee/': 'travel',
    '/articles/vietnam-grab/': 'vehicles',
    '/articles/weekend-drive-preparation/': 'vehicles',
    '/articles/travel-memory-notes/': 'travel',
    '/articles/boso-train-replacement/': 'vehicles'
  };
  var currentPath = window.location.pathname.replace(/index\.html$/, '');

  function isSelectionLabel(value) {
    return /robu[\u2018\u2019'\-\s]*s?\s*selection/i.test(value || '');
  }

  function isSelectionArticle() {
    if (!articlePath) return false;
    if (document.body.classList.contains('robus-selection-page')) return true;

    var section = document.querySelector('meta[property="article:section"], meta[name="article:section"]');
    if (section && isSelectionLabel(section.getAttribute('content'))) return true;

    var category = document.querySelector('[data-article-category], .robu-selection-label, .badge, .kicker');
    if (category && isSelectionLabel(category.textContent)) return true;

    return legacySelectionArticlePaths.indexOf(currentPath) !== -1;
  }

  function ensureStyle() {
    var link = document.querySelector('link[data-robu-shared-shell]');
    if (link) {
      link.href = cssHref;
      return;
    }
    link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = cssHref;
    link.setAttribute('data-robu-shared-shell', '');
    document.head.appendChild(link);
  }

  function ensureSelectionTheme(shellTheme) {
    if (shellTheme !== 'selection') return;
    document.body.classList.add('robus-selection-page');
    var link = document.querySelector('link[data-robu-selection-theme]');
    if (link) {
      link.href = selectionCssHref;
      return;
    }
    link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = selectionCssHref;
    link.setAttribute('data-robu-selection-theme', '');
    document.head.appendChild(link);
  }

  function renderSelectionLabel(shellTheme) {
    if (shellTheme !== 'selection') return;
    var heading = document.querySelector('body > main h1, body > article h1, body > header:not(.site-header) h1, body h1');
    if (!heading) return;

    var label = document.createElement('div');
    label.className = 'robu-selection-label';
    label.textContent = 'Robu’s Selection';

    var existing = document.querySelector('.robu-selection-label, .badge, .draft, .status');
    if (existing && !existing.closest('.contact-feedback')) existing.replaceWith(label);
    else heading.parentNode.insertBefore(label, heading);
  }

  function renderMarketplaceLinks() {
    var products = {
      '/articles/sony-ult-tower-7/': ['Sony ULT TOWER 7', 'Sony ULT TOWER 7'],
      '/articles/garmin-fenix-9-pro-titanium-inreach/': ['Garmin fenix 9 Pro inReach', 'Garmin fēnix 9シリーズ'],
      '/articles/garmin-cirqa-smart-band/': ['Garmin CIRQA Smart Band', 'Garmin CIRQA'],
      '/articles/meta-glasses/': ['Meta AI Glasses', 'Meta AI Glasses'],
      '/articles/seiko-prospex-hbc011j/': ['セイコー プロスペックス HBC011J', 'セイコー プロスペックス HBC011J', 'https://room.rakuten.co.jp/room_4b003bc175/1700392030842251'],
      '/articles/seiko-presage-bonsai/': ['セイコー プレザージュ HCC011J', 'セイコー プレザージュ HCC011J'],
      '/articles/gopro-mission-1-pro-ils/': ['GoPro MISSION 1 PRO ILS', 'GoPro MISSION 1 PRO ILS'],
      '/articles/google-pixel-watch-5/': ['Google Pixel Watch 5', 'Google Pixel Watch 5'],
      '/articles/breitling-navitimer-samurai-japan/': ['ブライトリング ナビタイマー GMT 41 侍ジャパン', 'ナビタイマー GMT 41 侍ジャパン'],
      '/articles/breitling-navitimer-concorde/': ['Breitling AB01389C1C1P1', 'Breitling AB01389C1C1P1'],
      '/articles/seiko-astron-hab005j/': ['セイコー アストロン HAB005J', 'セイコー アストロン HAB005J'],
      '/articles/casio-gwr-b3000/': ['CASIO G-SHOCK GWR-B3000-1AJF', 'CASIO G-SHOCK GWR-B3000-1AJF']
    };
    var product = products[currentPath];
    if (!product || document.querySelector('[data-marketplace-links], .purchase-buttons')) return;

    var section = document.createElement('section');
    section.className = 'robu-marketplace-section';
    section.setAttribute('data-marketplace-links', '');
    var heading = document.createElement('h2');
    heading.textContent = '購入先を確認する';
    var disclosure = document.createElement('p');
    disclosure.className = 'note';
    disclosure.textContent = 'Amazonのリンクはアフィリエイトリンクです。楽天ROOMが表示される記事では、そのリンクもアフィリエイトリンクです。価格・在庫・販売元は各ページでご確認ください。';
    var buttons = document.createElement('div');
    buttons.className = 'robu-marketplace-buttons';
    var destinations = [
      { className: 'amazon', href: 'https://www.amazon.co.jp/s?' + new URLSearchParams({k: product[0], tag: 'womaster-22'}), rel: 'nofollow sponsored noopener noreferrer', text: 'Amazonで詳細を見る' },
      { className: 'rakuten', href: product[2] || 'https://search.rakuten.co.jp/search/mall/' + encodeURIComponent(product[0]) + '/', rel: product[2] ? 'nofollow sponsored noopener noreferrer' : 'noopener noreferrer', text: product[2] ? '楽天市場で詳細を見る' : '楽天市場で探す' },
      { className: 'yahoo', href: 'https://shopping.yahoo.co.jp/search?p=' + encodeURIComponent(product[0]), rel: 'noopener noreferrer', text: 'Yahoo!ショッピングで探す' }
    ];
    destinations.forEach(function (destination) {
      var link = document.createElement('a');
      link.className = 'robu-marketplace-button ' + destination.className;
      link.href = destination.href;
      link.target = '_blank';
      link.rel = destination.rel;
      link.textContent = destination.text;
      buttons.appendChild(link);
    });
    section.append(heading, disclosure, buttons);

    var root = articleHeadingRoot();
    if (!root) return;
    var sourceHeading = Array.prototype.find.call(root.querySelectorAll('h2'), function (item) {
      return /公式(?:出典|情報)|確認した公式情報/.test(item.textContent);
    });
    var sourceSection = sourceHeading && sourceHeading.closest('section');
    if (sourceSection) sourceSection.parentNode.insertBefore(section, sourceSection);
    else if (sourceHeading) sourceHeading.parentNode.insertBefore(section, sourceHeading);
    else root.appendChild(section);
  }

  function currentNavigationKey(shellTheme) {
    if (shellTheme === 'selection') return 'selection';
    if (/^\/about\/?$/.test(currentPath)) return 'about';
    return regularArticleNavigation[currentPath] || 'home';
  }

  function headerMarkup(shellTheme, currentNavKey) {
    var selection = shellTheme === 'selection';
    var brand = selection ? 'Robu’s Selection' : 'ろぶーの<span>気になる事</span>';
    var navigationItems = [
      ['home', '/', 'ホーム'],
      ['gourmet', '/#gourmet', 'グルメ'],
      ['vehicles', '/#vehicles', '乗り物'],
      ['travel', '/#travel', '旅行'],
      ['hotel', '/#hotel', 'ホテル'],
      ['selection', '/#selection', 'Robu’s Selection'],
      ['about', '/about/', '運営者']
    ];
    var navigation = navigationItems.map(function (item) {
      var current = item[0] === currentNavKey ? ' aria-current="page"' : '';
      return '<a href="' + item[1] + '"' + current + '>' + item[2] + '</a>';
    }).join('');

    return '<header class="site-header robu-common-header" id="robuCommonHeader" data-robu-common-header data-shell-theme="' + shellTheme + '">' +
      '<a class="brand" href="/">' + brand + '</a>' +
      '<button class="menu-toggle" type="button" aria-label="メニューを開く" aria-expanded="false" aria-controls="robuCommonNavigation">☰</button>' +
      '<nav class="main-nav" id="robuCommonNavigation" aria-label="メインナビゲーション">' +
      navigation +
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
      '<button type="button" class="privacy-settings" data-robu-consent-settings>Cookie設定 / Cookie settings</button>' +
      '</div>' +
      '<div class="social-links" aria-label="SNSリンク">' +
      '<a class="social-link social-facebook" href="https://www.facebook.com/profile.php?id=61593907652973" target="_blank" rel="noopener noreferrer" aria-label="Facebookを開く">Facebook</a>' +
      '<a class="social-link social-instagram" href="https://www.instagram.com/robusandesu/" target="_blank" rel="noopener noreferrer" aria-label="Instagramを開く">Instagram</a>' +
      '<a class="social-link social-x" href="https://x.com/Robusandesu" target="_blank" rel="noopener noreferrer" aria-label="Xを開く">X</a>' +
      '<a class="social-link social-reddit" href="https://www.reddit.com/user/No-Dinner-6194/" target="_blank" rel="noopener noreferrer" aria-label="Redditを開く">Reddit</a>' +
      '<a class="social-link social-tiktok" href="https://www.tiktok.com/@user7868731611087" target="_blank" rel="noopener noreferrer" aria-label="TikTokを開く">TikTok</a>' +
      '</div>' +
      '<small>© 2026 ろぶーの気になる事. All rights reserved.</small>' +
      '</footer>';
  }

  function elementFrom(markup) {
    var template = document.createElement('template');
    template.innerHTML = markup.trim();
    return template.content.firstElementChild;
  }

  function isReplaceableSiteHeader(header) {
    if (header.parentNode !== document.body) return false;
    if (header.hasAttribute('data-robu-common-header')) return true;
    if (header.querySelector('h1, h2, h3, article, section')) return false;

    var children = Array.prototype.slice.call(header.children);
    var shellOnly = children.length && children.every(function (child) {
      return child.matches('a[href="/"], a[href="/index.html"], button.menu-toggle, nav.main-nav');
    });

    if (header.classList.contains('site-header')) return shellOnly;
    return children.length === 1 && children[0].matches('a.brand[href="/"], a.brand[href="/index.html"]');
  }

  function bindHeaderMenu(header) {
    var toggle = header.querySelector('.menu-toggle');
    var nav = header.querySelector('.main-nav');

    function setMenuOpen(open) {
      toggle.setAttribute('aria-expanded', String(open));
      toggle.setAttribute('aria-label', open ? 'メニューを閉じる' : 'メニューを開く');
      nav.classList.toggle('is-open', open);
    }

    setMenuOpen(false);
    toggle.addEventListener('click', function (event) {
      // Some older pages still load site.js. Keep this shared control as the
      // single owner of the replacement header's menu state.
      event.stopImmediatePropagation();
      setMenuOpen(toggle.getAttribute('aria-expanded') !== 'true');
    });
    nav.addEventListener('click', function (event) {
      if (event.target.closest('a')) setMenuOpen(false);
    });
    document.addEventListener('keydown', function (event) {
      if (event.key !== 'Escape' || toggle.getAttribute('aria-expanded') !== 'true') return;
      setMenuOpen(false);
      toggle.focus();
    });

    var desktopQuery = window.matchMedia('(min-width: 981px)');
    function closeDesktopMenu(event) {
      if (event.matches) setMenuOpen(false);
    }
    if (desktopQuery.addEventListener) desktopQuery.addEventListener('change', closeDesktopMenu);
  }

  function renderHeader(shellTheme, currentNavKey) {
    if (homePath) return;
    var header = elementFrom(headerMarkup(shellTheme, currentNavKey));
    var replaceableHeaders = Array.prototype.filter.call(document.body.children, function (child) {
      return child.tagName === 'HEADER' && isReplaceableSiteHeader(child);
    });

    if (replaceableHeaders.length) {
      replaceableHeaders[0].replaceWith(header);
      replaceableHeaders.slice(1).forEach(function (legacyHeader) { legacyHeader.remove(); });
    } else {
      document.body.insertBefore(header, document.body.firstChild);
    }

    bindHeaderMenu(header);
  }

  function renderFooter() {
    var footer = elementFrom(footerMarkup());
    var current = document.querySelector('body > footer');
    if (current) current.replaceWith(footer);
    else document.body.appendChild(footer);

    var settingsButton = footer.querySelector('[data-robu-consent-settings]');
    if (settingsButton) settingsButton.addEventListener('click', function () {
      showConsentBanner(true);
    });
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

  function loadGoogleAnalytics() {
    if (document.querySelector('script[data-robu-google-analytics]')) return;
    window.gtag('js', new Date());
    window.gtag('config', analyticsMeasurementId);
    var script = document.createElement('script');
    script.async = true;
    script.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(analyticsMeasurementId);
    script.setAttribute('data-robu-google-analytics', '');
    document.head.appendChild(script);
  }

  function consentBannerMarkup() {
    return '<section class="robu-consent-banner" data-robu-consent-banner role="dialog" aria-labelledby="robuConsentTitle" aria-describedby="robuConsentDescription">' +
      '<div class="robu-consent-copy">' +
      '<strong id="robuConsentTitle">Cookieとアクセス解析 / Cookies &amp; analytics</strong>' +
      '<p id="robuConsentDescription">サイト改善のためGoogle Analyticsを使用します。分析Cookieを許可するか選択してください。We use Google Analytics to improve this site. You can accept or reject analytics cookies.</p>' +
      '<a href="/privacy-policy/">プライバシーポリシー / Privacy policy</a>' +
      '</div>' +
      '<div class="robu-consent-actions">' +
      '<button type="button" data-robu-consent="denied">拒否 / Reject</button>' +
      '<button type="button" class="is-primary" data-robu-consent="granted">同意する / Accept</button>' +
      '</div>' +
      '</section>';
  }

  function applyConsent(value) {
    storeConsent(value);
    storedConsent = value;
    window.gtag('consent', 'update', {
      analytics_storage: value === 'granted' ? 'granted' : 'denied',
      ad_storage: 'denied',
      ad_user_data: 'denied',
      ad_personalization: 'denied'
    });
    if (value === 'granted') loadGoogleAnalytics();
    var banner = document.querySelector('[data-robu-consent-banner]');
    if (banner) banner.remove();
  }

  function showConsentBanner(force) {
    if (!force && storedConsent) return;
    var current = document.querySelector('[data-robu-consent-banner]');
    if (current) current.remove();
    var banner = elementFrom(consentBannerMarkup());
    banner.querySelectorAll('[data-robu-consent]').forEach(function (button) {
      button.addEventListener('click', function () {
        applyConsent(button.getAttribute('data-robu-consent'));
      });
    });
    document.body.appendChild(banner);
    var preferred = banner.querySelector('[data-robu-consent="' + (storedConsent || 'denied') + '"]');
    if (preferred) preferred.focus();
  }

  function init() {
    var shellTheme = isSelectionArticle() ? 'selection' : 'regular';
    var currentNavKey = currentNavigationKey(shellTheme);
    document.body.setAttribute('data-shell-theme', shellTheme);
    if (articlePath && shellTheme === 'regular') document.body.classList.add('robu-regular-article-page');
    ensureStyle();
    ensureSelectionTheme(shellTheme);
    renderHeader(shellTheme, currentNavKey);
    renderSelectionLabel(shellTheme);
    renderMarketplaceLinks();
    renderFooter();
    renderArticleToc();
    if (storedConsent === 'granted') loadGoogleAnalytics();
    else if (!storedConsent) showConsentBanner(false);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
}());
