const { chromium } = require('C:/Users/yrt11/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');

(async () => {
  const browser = await chromium.launch({
    headless: true,
    executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe',
  });

  try {
    for (const width of [390, 1440]) {
      const page = await browser.newPage({ viewport: { width, height: 900 } });

      for (const [lang, route] of [
        ['ja', '/articles/generative-ai-team-responsibilities-2026/'],
        ['en', '/en/articles/generative-ai-team-responsibilities-2026/'],
      ]) {
        const response = await page.goto(`http://127.0.0.1:8765${route}`, {
          waitUntil: 'networkidle',
        });

        const data = await page.evaluate(() => {
          const buttons = document.querySelector('.purchase-buttons, .robu-marketplace-buttons');
          const note = document.querySelector('.purchase-note');
          const disclosure = document.querySelector('[data-purchase-disclosure]');
          const purchasePanel = document.querySelector('.purchase-panel');
          const bodyBackground = getComputedStyle(document.body).backgroundColor;
          const purchaseBackground = purchasePanel ? getComputedStyle(purchasePanel).backgroundColor : null;

          return {
            title: document.querySelector('h1.article-title')?.textContent?.trim(),
            images: document.querySelectorAll('.article-content img').length,
            loadedImages: [...document.querySelectorAll('.article-content img')]
              .filter((image) => image.complete && image.naturalWidth > 0).length,
            aiLabels: document.querySelectorAll('.ai-image-disclosure').length,
            toc: document.querySelectorAll('[data-robu-article-toc] a').length,
            closeHeading: [...document.querySelectorAll('.article-content h2')]
              .some((heading) => /ろぶーのまとめ|Robu['’]s Wrap-Up/.test(heading.textContent)),
            contact: document.querySelectorAll('.site-footer a[href="/contact/"]').length,
            contactForm: document.querySelectorAll('.contact-feedback .contact-form').length,
            contactOpen: document.querySelector('.contact-details')?.open === true,
            purchasePanelTransparent: purchaseBackground === 'rgba(0, 0, 0, 0)',
            purchaseOrder: Boolean(
              buttons && note && disclosure
              && (buttons.compareDocumentPosition(note) & Node.DOCUMENT_POSITION_FOLLOWING)
              && (note.compareDocumentPosition(disclosure) & Node.DOCUMENT_POSITION_FOLLOWING)
            ),
            merchantButtons: document.querySelectorAll('.purchase-buttons a, .robu-marketplace-buttons a').length,
            mailPreviewButton: document.body.innerText.includes('メールアプリで送信内容を確認する')
              || document.body.innerText.includes('Review in your email app'),
            overflow: document.documentElement.scrollWidth > window.innerWidth,
            robots: document.querySelector('meta[name="robots"]')?.content,
            bodyBackground,
            purchaseBackground,
          };
        });

        if (
          response.status() !== 200
          || !data.title
          || data.images !== 2
          || data.loadedImages !== 2
          || data.aiLabels !== 2
          || data.toc < 5
          || !data.closeHeading
          || data.contact !== 1
          || data.contactForm !== 1
          || !data.purchasePanelTransparent
          || !data.purchaseOrder
          || data.merchantButtons !== 3
          || data.mailPreviewButton
          || data.overflow
          || !data.robots?.startsWith('index,follow')
        ) {
          throw new Error(JSON.stringify({ width, lang, status: response.status(), ...data }));
        }

        console.log(width, lang, 'PASS', JSON.stringify(data));
      }

      await page.close();
    }
  } finally {
    await browser.close();
  }
})().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
