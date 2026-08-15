(function () {
  'use strict';

  function initMenu() {
    var toggle = document.querySelector('.menu-toggle');
    var nav = document.querySelector('.main-nav');

    if (!toggle || !nav) return;

    if (!nav.id) nav.id = 'main-navigation';
    toggle.setAttribute('aria-controls', nav.id);

    function setMenuOpen(open) {
      nav.classList.toggle('is-open', open);
      toggle.setAttribute('aria-expanded', String(open));
      toggle.setAttribute('aria-label', open ? 'メニューを閉じる' : 'メニューを開く');
    }

    setMenuOpen(toggle.getAttribute('aria-expanded') === 'true');

    toggle.addEventListener('click', function () {
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
  }

  function copyWithFallback(text) {
    var activeElement = document.activeElement;
    var field = document.createElement('textarea');
    var copied = false;

    field.value = text;
    field.setAttribute('readonly', '');
    field.style.position = 'fixed';
    field.style.top = '0';
    field.style.left = '-9999px';
    field.style.opacity = '0';
    document.body.appendChild(field);
    field.focus();
    field.select();
    field.setSelectionRange(0, field.value.length);

    try {
      copied = document.execCommand('copy');
    } catch (error) {
      copied = false;
    }

    field.remove();
    if (activeElement && typeof activeElement.focus === 'function') activeElement.focus();
    return copied;
  }

  async function copyText(text) {
    if (window.isSecureContext && navigator.clipboard && typeof navigator.clipboard.writeText === 'function') {
      try {
        await navigator.clipboard.writeText(text);
        return true;
      } catch (error) {
        // Permission denial and older browser behavior are handled below.
      }
    }

    return copyWithFallback(text);
  }

  function initCopyButtons() {
    document.querySelectorAll('[data-copy-link]').forEach(function (button) {
      var originalLabel = button.textContent;
      var resetTimer;

      button.setAttribute('aria-live', 'polite');
      button.addEventListener('click', async function () {
        var canonical = document.querySelector('link[rel="canonical"]');
        var link = button.dataset.copyLink || (canonical && canonical.href) || window.location.href;
        var copied = await copyText(link);

        window.clearTimeout(resetTimer);
        button.textContent = copied ? 'リンクをコピーしました' : 'リンクをコピーできませんでした';
        resetTimer = window.setTimeout(function () {
          button.textContent = originalLabel;
        }, 2000);
      });
    });
  }

  function loadContactFeedback() {
    if (document.querySelector('script[data-contact-feedback-loader]')) return;
    var script = document.createElement('script');
    script.src = '/assets/js/contact-feedback.js?v=20260816-2';
    script.defer = true;
    script.dataset.contactFeedbackLoader = '';
    document.head.appendChild(script);
  }

  function init() {
    initMenu();
    initCopyButtons();
    loadContactFeedback();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init, { once: true });
  } else {
    init();
  }
})();
