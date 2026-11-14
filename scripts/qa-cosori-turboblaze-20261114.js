const { chromium } = require('C:/Users/yrt11/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');

(async () => {
  const browser = await chromium.launch({
    headless: true,
    executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe',
  });
  const results = [];
  for (const language of ['ja', 'en']) {
    for (const width of [390, 1280]) {
      const page = await browser.newPage({ viewport: { width, height: 900 } });
      const url = `http://127.0.0.1:18771/${language === 'ja' ? '' : 'en/'}articles/cosori-turboblaze-6l-air-fryer/`;
      await page.goto(url, { waitUntil: 'networkidle' });
      const result = await page.evaluate(() => ({
        title: document.querySelector('h1')?.textContent?.trim(),
        images: [...document.images].filter((image) => image.closest('.article-content')).length,
        brokenImages: [...document.images].filter((image) => image.closest('.article-content') && !image.complete).length,
        tables: document.querySelectorAll('.article-content table').length,
        purchaseButtons: document.querySelectorAll('.purchase-button').length,
        header: Boolean(document.querySelector('header')),
        contact: Boolean(document.querySelector('[data-contact-feedback], .contact-feedback, #contact-feedback')),
        horizontalOverflow: document.documentElement.scrollWidth > document.documentElement.clientWidth + 1,
        robots: document.querySelector('meta[name="robots"]')?.content,
        socialPublish: document.querySelector('meta[name="social:publish"]')?.content,
      }));
      if (!result.title || result.images !== 4 || result.brokenImages || result.tables < 3 || result.purchaseButtons !== 3 || !result.header || result.horizontalOverflow || result.robots?.includes('noindex') || result.socialPublish !== 'true') {
        throw new Error(`${language}/${width}: ${JSON.stringify(result)}`);
      }
      await page.screenshot({ path: `.tmp-cosori-${language}-${width}.png`, fullPage: true });
      results.push({ language, width, ...result });
      await page.close();
    }
  }
  await browser.close();
  console.log(JSON.stringify(results, null, 2));
})().catch((error) => {
  console.error(error);
  process.exit(1);
});
