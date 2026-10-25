const { chromium } = require('C:/Users/yrt11/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');

(async () => {
  const browser = await chromium.launch({ headless: true, executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe' });
  try {
    const widths = process.argv[2] ? [Number(process.argv[2])] : [390, 1440];
    const languages = process.argv[3]
      ? [[process.argv[3], process.argv[3] === 'ja' ? '/articles/naniwa-yodogawa-fireworks-2026-exciting-seat/' : '/en/articles/naniwa-yodogawa-fireworks-2026-exciting-seat/']]
      : [['ja', '/articles/naniwa-yodogawa-fireworks-2026-exciting-seat/'], ['en', '/en/articles/naniwa-yodogawa-fireworks-2026-exciting-seat/']];
    for (const width of widths) {
      const page = await browser.newPage({ viewport: { width, height: 900 } });
      for (const [lang, route] of languages) {
        const response = await page.goto(`http://127.0.0.1:8765${route}`, { waitUntil: 'networkidle' });
        const data = await page.evaluate(() => {
          const buttons = document.querySelector('.purchase-buttons');
          const note = document.querySelector('.purchase-note');
          const disclosure = document.querySelector('[data-purchase-disclosure]');
          const video = document.querySelector('video');
          return {
            title: document.querySelector('h1.article-title')?.textContent?.trim(),
            images: document.querySelectorAll('.article-content img').length,
            loadedImages: [...document.querySelectorAll('.article-content img')].filter(i => i.complete && i.naturalWidth > 0).length,
            toc: document.querySelectorAll('[data-robu-article-toc] a').length,
            seatRows: document.querySelectorAll('.article-content table')[1]?.querySelectorAll('tbody tr').length,
            video: Boolean(video && video.controls && !video.autoplay && video.preload === 'metadata'),
            videoSource: video?.querySelector('source')?.src || '',
            contact: document.querySelectorAll('.site-footer a[href="/contact/"]').length,
            contactForm: document.querySelectorAll('.contact-feedback .contact-form').length,
            affiliateOrder: Boolean(buttons && note && disclosure && (buttons.compareDocumentPosition(note) & Node.DOCUMENT_POSITION_FOLLOWING) && (note.compareDocumentPosition(disclosure) & Node.DOCUMENT_POSITION_FOLLOWING)),
            affiliateButtons: document.querySelectorAll('.purchase-buttons a').length,
            overflow: document.documentElement.scrollWidth > window.innerWidth,
            robots: document.querySelector('meta[name="robots"]')?.content,
            socialPublish: document.querySelector('meta[name="social:publish"]')?.content,
            aiImage: document.querySelector('meta[name="social:ai-image"]')?.content,
          };
        });
        if (response.status() !== 200 || !data.title || data.images !== 6 || data.loadedImages !== 6 || data.toc < 8 || data.seatRows !== 6 || !data.video || !data.videoSource.endsWith('yodogawa-fireworks-finale-118s.mp4') || data.contact !== 1 || data.contactForm !== 1 || !data.affiliateOrder || data.affiliateButtons !== 1 || data.overflow || !data.robots?.startsWith('index,follow') || data.socialPublish !== 'true' || data.aiImage !== 'false') {
          throw new Error(JSON.stringify({ width, lang, status: response.status(), ...data }));
        }
        console.log(width, lang, 'PASS', JSON.stringify(data));
      }
      await page.close();
    }
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
