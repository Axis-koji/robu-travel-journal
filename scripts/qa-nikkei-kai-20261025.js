const { chromium } = require('C:/Users/yrt11/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');

(async () => {
  const browser = await chromium.launch({ headless: true, executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe' });
  try {
    for (const width of [390, 1440]) {
      const page = await browser.newPage({ viewport: { width, height: 900 } });
      for (const [lang, route] of [
        ['ja', '/articles/nikkei-kai-pr-media-analysis-agent/'],
        ['en', '/en/articles/nikkei-kai-pr-media-analysis-agent/'],
      ]) {
        const response = await page.goto('http://127.0.0.1:8765' + route, { waitUntil: 'networkidle' });
        const data = await page.evaluate(() => {
          const buttons = document.querySelector('.purchase-buttons, .robu-marketplace-buttons');
          const note = document.querySelector('.purchase-note');
          const disclosure = document.querySelector('[data-purchase-disclosure]');
          return {
            title: document.querySelector('h1.article-title')?.textContent?.trim(),
            images: document.querySelectorAll('.article-content img').length,
            loadedImages: [...document.querySelectorAll('.article-content img')].filter((image) => image.complete && image.naturalWidth > 0).length,
            toc: document.querySelectorAll('[data-robu-article-toc] a').length,
            contact: document.querySelectorAll('.site-footer a[href="/contact/"]').length,
            sources: document.querySelectorAll('.article-content a[href^="https://prtimes.jp"], .article-content a[href^="https://nkbb.nikkei.co.jp"]').length,
            purchaseOrder: Boolean(buttons && note && disclosure && (buttons.compareDocumentPosition(note) & Node.DOCUMENT_POSITION_FOLLOWING) && (note.compareDocumentPosition(disclosure) & Node.DOCUMENT_POSITION_FOLLOWING)),
            overflow: document.documentElement.scrollWidth > window.innerWidth,
            robots: document.querySelector('meta[name="robots"]')?.content,
          };
        });
        if (response.status() !== 200 || !data.title || data.images !== 2 || data.loadedImages !== 2 || data.toc < 5 || data.contact !== 1 || data.sources < 2 || !data.purchaseOrder || data.overflow || !data.robots?.startsWith('index,follow')) {
          throw new Error(JSON.stringify({ width, lang, status: response.status(), ...data }));
        }
        await page.screenshot({ path: `.tmp-nikkei-${lang}-${width}.png`, fullPage: true });
        console.log(width, lang, 'PASS', JSON.stringify(data));
      }
      await page.close();
    }
  } finally {
    await browser.close();
  }
})().catch((error) => { console.error(error); process.exitCode = 1; });
