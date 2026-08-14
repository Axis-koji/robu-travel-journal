(function () {
  'use strict';

  var STORAGE_KEY = 'axis-language-preference';
  var DEFAULT_LOCALE = 'ja';
  var locales = {
    ja: {
      code: 'ja', label: '日本語', language: '表示言語', home: 'ホーム', hotel: 'ホテル', gourmet: 'グルメ', vehicles: '乗り物', travel: '旅行',
      operator: '運営者', privacy: 'プライバシーポリシー', contact: 'お問い合わせ', terms: '利用規約', disclaimer: '広告・免責事項', sitemap: 'サイトマップ',
      menu: 'メインナビゲーション', openMenu: 'メニューを開く', closeMenu: 'メニューを閉じる', backCover: '表紙へ戻る', backPrevious: 'ひとつ前へ戻る',
      notice: ''
    },
    en: {
      code: 'en', label: 'English', language: 'Language', home: 'Home', hotel: 'Hotels', gourmet: 'Food', vehicles: 'Transport', travel: 'Travel',
      operator: 'About', privacy: 'Privacy policy', contact: 'Contact', terms: 'Terms', disclaimer: 'Advertising & disclaimer', sitemap: 'Sitemap',
      menu: 'Main navigation', openMenu: 'Open menu', closeMenu: 'Close menu', backCover: 'Back to home', backPrevious: 'Go back',
      notice: 'This page’s main content is currently available in Japanese. Navigation follows your selected or device language; a reviewed translation will be offered only when it is ready.'
    },
    fr: {
      code: 'fr', label: 'Français', language: 'Langue', home: 'Accueil', hotel: 'Hôtels', gourmet: 'Gastronomie', vehicles: 'Transport', travel: 'Voyages',
      operator: 'À propos', privacy: 'Politique de confidentialité', contact: 'Contact', terms: 'Conditions', disclaimer: 'Publicité et avertissement', sitemap: 'Plan du site',
      menu: 'Navigation principale', openMenu: 'Ouvrir le menu', closeMenu: 'Fermer le menu', backCover: 'Retour à l’accueil', backPrevious: 'Retour',
      notice: 'Le contenu principal de cette page est actuellement disponible en japonais. La navigation suit la langue choisie ou celle de votre appareil; une traduction vérifiée ne sera proposée qu’une fois prête.'
    },
    es: {
      code: 'es', label: 'Español', language: 'Idioma', home: 'Inicio', hotel: 'Hoteles', gourmet: 'Gastronomía', vehicles: 'Transporte', travel: 'Viajes',
      operator: 'Acerca de', privacy: 'Política de privacidad', contact: 'Contacto', terms: 'Condiciones', disclaimer: 'Publicidad y aviso legal', sitemap: 'Mapa del sitio',
      menu: 'Navegación principal', openMenu: 'Abrir menú', closeMenu: 'Cerrar menú', backCover: 'Volver al inicio', backPrevious: 'Volver',
      notice: 'El contenido principal de esta página está disponible actualmente en japonés. La navegación sigue el idioma elegido o el del dispositivo; solo se ofrecerá una traducción revisada cuando esté lista.'
    },
    vi: {
      code: 'vi', label: 'Tiếng Việt', language: 'Ngôn ngữ', home: 'Trang chủ', hotel: 'Khách sạn', gourmet: 'Ẩm thực', vehicles: 'Phương tiện', travel: 'Du lịch',
      operator: 'Giới thiệu', privacy: 'Chính sách quyền riêng tư', contact: 'Liên hệ', terms: 'Điều khoản', disclaimer: 'Quảng cáo và miễn trừ', sitemap: 'Sơ đồ trang',
      menu: 'Điều hướng chính', openMenu: 'Mở menu', closeMenu: 'Đóng menu', backCover: 'Về trang chủ', backPrevious: 'Quay lại',
      notice: 'Nội dung chính của trang này hiện chỉ có bằng tiếng Nhật. Phần điều hướng dùng ngôn ngữ bạn chọn hoặc ngôn ngữ thiết bị; bản dịch đã kiểm duyệt chỉ được cung cấp khi hoàn tất.'
    },
    it: {
      code: 'it', label: 'Italiano', language: 'Lingua', home: 'Home', hotel: 'Hotel', gourmet: 'Gastronomia', vehicles: 'Trasporti', travel: 'Viaggi',
      operator: 'Chi siamo', privacy: 'Informativa sulla privacy', contact: 'Contatti', terms: 'Termini', disclaimer: 'Pubblicità e avvertenze', sitemap: 'Mappa del sito',
      menu: 'Navigazione principale', openMenu: 'Apri menu', closeMenu: 'Chiudi menu', backCover: 'Torna alla home', backPrevious: 'Indietro',
      notice: 'Il contenuto principale di questa pagina è attualmente disponibile in giapponese. La navigazione segue la lingua scelta o quella del dispositivo; una traduzione revisionata sarà proposta solo quando pronta.'
    },
    az: {
      code: 'az', label: 'Azərbaycanca', language: 'Dil', home: 'Ana səhifə', hotel: 'Otellər', gourmet: 'Qastronomiya', vehicles: 'Nəqliyyat', travel: 'Səyahət',
      operator: 'Haqqımızda', privacy: 'Məxfilik siyasəti', contact: 'Əlaqə', terms: 'Şərtlər', disclaimer: 'Reklam və imtina', sitemap: 'Sayt xəritəsi',
      menu: 'Əsas naviqasiya', openMenu: 'Menyunu aç', closeMenu: 'Menyunu bağla', backCover: 'Ana səhifəyə qayıt', backPrevious: 'Geri qayıt',
      notice: 'Bu səhifənin əsas məzmunu hazırda yapon dilindədir. Naviqasiya seçdiyiniz və ya cihazın dilinə uyğun göstərilir; yoxlanılmış tərcümə yalnız hazır olduqda təqdim ediləcək.'
    },
    uk: {
      code: 'uk', label: 'Українська', language: 'Мова', home: 'Головна', hotel: 'Готелі', gourmet: 'Гастрономія', vehicles: 'Транспорт', travel: 'Подорожі',
      operator: 'Про нас', privacy: 'Політика конфіденційності', contact: 'Контакти', terms: 'Умови', disclaimer: 'Реклама та застереження', sitemap: 'Мапа сайту',
      menu: 'Головна навігація', openMenu: 'Відкрити меню', closeMenu: 'Закрити меню', backCover: 'На головну', backPrevious: 'Назад',
      notice: 'Основний вміст цієї сторінки наразі доступний японською. Навігація відповідає вибраній мові або мові пристрою; перевірений переклад з’явиться лише після готовності.'
    },
    yue: {
      code: 'yue', label: '粵語', language: '顯示語言', home: '主頁', hotel: '酒店', gourmet: '美食', vehicles: '交通', travel: '旅行',
      operator: '關於本站', privacy: '私隱政策', contact: '聯絡我哋', terms: '使用條款', disclaimer: '廣告及免責聲明', sitemap: '網站地圖',
      menu: '主要導覽', openMenu: '打開選單', closeMenu: '關閉選單', backCover: '返回主頁', backPrevious: '返回上一頁',
      notice: '呢一頁嘅主要內容目前只有日文。導覽會跟你揀嘅語言或裝置語言顯示；經校對嘅翻譯準備好之後先會提供。'
    },
    zhTW: {
      code: 'zh-Hant', label: '繁體中文', language: '顯示語言', home: '首頁', hotel: '飯店', gourmet: '美食', vehicles: '交通', travel: '旅行',
      operator: '關於本站', privacy: '隱私權政策', contact: '聯絡我們', terms: '使用條款', disclaimer: '廣告與免責聲明', sitemap: '網站地圖',
      menu: '主要導覽', openMenu: '開啟選單', closeMenu: '關閉選單', backCover: '返回首頁', backPrevious: '返回上一頁',
      notice: '本頁主要內容目前僅提供日文。導覽會依您選擇的語言或裝置語言顯示；經審閱的翻譯完成後才會提供。'
    },
    zhCN: {
      code: 'zh-Hans', label: '简体中文', language: '显示语言', home: '首页', hotel: '酒店', gourmet: '美食', vehicles: '交通', travel: '旅行',
      operator: '关于本站', privacy: '隐私政策', contact: '联系我们', terms: '使用条款', disclaimer: '广告与免责声明', sitemap: '网站地图',
      menu: '主导航', openMenu: '打开菜单', closeMenu: '关闭菜单', backCover: '返回首页', backPrevious: '返回上一页',
      notice: '本页主要内容目前仅提供日文。导航会按照您选择的语言或设备语言显示；经审核的翻译完成后才会提供。'
    }
  };

  function normalizeLocale(value) {
    var raw = String(value || '').toLowerCase().replace('_', '-');
    if (raw.indexOf('zh-hant') === 0 || raw === 'zh-tw' || raw === 'zh-hk') return 'zhTW';
    if (raw.indexOf('zh-hans') === 0 || raw === 'zh-cn' || raw === 'zh-sg') return 'zhCN';
    if (raw.indexOf('yue') === 0) return 'yue';
    var primary = raw.split('-')[0];
    return Object.prototype.hasOwnProperty.call(locales, primary) ? primary : DEFAULT_LOCALE;
  }

  function storedLocale() {
    try {
      return window.localStorage.getItem(STORAGE_KEY);
    } catch (error) {
      return null;
    }
  }

  function deviceLocale() {
    var candidates = navigator.languages && navigator.languages.length ? navigator.languages : [navigator.language];
    for (var index = 0; index < candidates.length; index += 1) {
      var locale = normalizeLocale(candidates[index]);
      if (locale !== DEFAULT_LOCALE || String(candidates[index] || '').toLowerCase().indexOf('ja') === 0) return locale;
    }
    return DEFAULT_LOCALE;
  }

  function currentLocale() {
    var stored = storedLocale();
    return stored && locales[stored] ? stored : deviceLocale();
  }

  function setStoredLocale(locale) {
    try {
      window.localStorage.setItem(STORAGE_KEY, locale);
    } catch (error) {
      // The page continues to work when storage is blocked.
    }
  }

  function textForLink(link, dictionary) {
    var href = link.getAttribute('href') || '';
    if (href === '/' || href === '/index.html' || href === 'index.html') return dictionary.home;
    if (href.indexOf('/categories/hotel') === 0) return dictionary.hotel;
    if (href.indexOf('/categories/gourmet') === 0) return dictionary.gourmet;
    if (href.indexOf('/categories/vehicles') === 0) return dictionary.vehicles;
    if (href.indexOf('/categories/travel') === 0 || href.indexOf('/categories/vietnam') === 0) return dictionary.travel;
    if (href.indexOf('/about') === 0) return dictionary.operator;
    if (href.indexOf('/privacy-policy') === 0 || href === 'privacy-policy.html') return dictionary.privacy;
    if (href.indexOf('/contact') === 0) return dictionary.contact;
    if (href.indexOf('/terms') === 0) return dictionary.terms;
    if (href.indexOf('/advertising-disclaimer') === 0) return dictionary.disclaimer;
    if (href.indexOf('/sitemap') === 0) return dictionary.sitemap;
    return null;
  }

  function translateCommon(locale) {
    var dictionary = locales[locale];
    document.querySelectorAll('.main-nav, .nav, .footer-links').forEach(function (container) {
      container.querySelectorAll('a').forEach(function (link) {
        var replacement = textForLink(link, dictionary);
        if (replacement) link.textContent = replacement;
      });
    });

    document.querySelectorAll('.main-nav, .nav').forEach(function (nav) {
      nav.setAttribute('aria-label', dictionary.menu);
    });

    document.querySelectorAll('.menu-toggle').forEach(function (button) {
      button.setAttribute('aria-label', button.getAttribute('aria-expanded') === 'true' ? dictionary.closeMenu : dictionary.openMenu);
    });

    document.querySelectorAll('.actions a').forEach(function (link) {
      if (link.textContent.trim() === '表紙へ戻る' || link.dataset.languageAction === 'home') {
        link.dataset.languageAction = 'home';
        link.textContent = dictionary.backCover;
      }
    });
    document.querySelectorAll('.actions button').forEach(function (button) {
      if (button.textContent.trim() === 'ひとつ前へ戻る' || button.dataset.languageAction === 'back') {
        button.dataset.languageAction = 'back';
        button.textContent = dictionary.backPrevious;
      }
    });

    var notice = document.querySelector('.site-language-notice');
    if (notice) {
      notice.textContent = dictionary.notice;
      notice.hidden = locale === DEFAULT_LOCALE || !dictionary.notice;
      notice.lang = dictionary.code;
    }

    var shellLabel = document.querySelector('.site-language-shell label');
    if (shellLabel) shellLabel.textContent = dictionary.language;
  }

  function addNotice() {
    if (document.querySelector('.language-trigger') || document.querySelector('.site-language-notice')) return;
    var isViewer = /-360\.html$/i.test(window.location.pathname);
    if (isViewer) return;
    var host = document.querySelector('main');
    if (!host) return;
    var notice = document.createElement('aside');
    notice.className = 'site-language-notice';
    notice.setAttribute('role', 'status');
    notice.hidden = true;
    host.parentNode.insertBefore(notice, host);
  }

  function addPicker(locale) {
    if (document.querySelector('.language-trigger') || document.querySelector('.site-language-shell')) return;
    var shell = document.createElement('div');
    shell.className = 'site-language-shell';
    var label = document.createElement('label');
    label.htmlFor = 'site-language-select';
    var select = document.createElement('select');
    select.id = 'site-language-select';
    select.setAttribute('aria-label', locales[locale].language);
    Object.keys(locales).forEach(function (key) {
      var option = document.createElement('option');
      option.value = key;
      option.textContent = locales[key].label;
      select.appendChild(option);
    });
    select.value = locale;
    select.addEventListener('change', function () {
      var next = locales[select.value] ? select.value : DEFAULT_LOCALE;
      setStoredLocale(next);
      translateCommon(next);
      select.setAttribute('aria-label', locales[next].language);
      document.documentElement.dataset.uiLanguage = next;
      if (window.RobuLanguage) window.RobuLanguage.locale = next;
      document.dispatchEvent(new CustomEvent('robu:languagechange', { detail: { locale: next } }));
    });
    shell.appendChild(label);
    shell.appendChild(select);
    document.body.appendChild(shell);
  }

  function init() {
    var locale = currentLocale();
    addNotice();
    addPicker(locale);
    translateCommon(locale);
    document.documentElement.dataset.uiLanguage = locale;
    window.RobuLanguage = {
      locale: locale,
      storageKey: STORAGE_KEY,
      supported: Object.keys(locales),
      normalize: normalizeLocale
    };
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init, { once: true });
  } else {
    init();
  }
})();
