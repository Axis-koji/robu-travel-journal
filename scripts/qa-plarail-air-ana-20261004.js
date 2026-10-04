const { chromium } = require('C:/Users/yrt11/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');

(async () => {
  const browser = await chromium.launch({ headless: true, executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe' });
  try {
    for (const width of [390, 1180, 1440]) {
      const page = await browser.newPage({ viewport: { width, height: 900 } });
      for (const route of [
        '/articles/plarail-air-ana-passenger-plane-set/',
        '/en/articles/plarail-air-ana-passenger-plane-set/',
      ]) {
        const response = await page.goto('http://127.0.0.1:8765' + route, { waitUntil: 'networkidle' });
        const data = await page.evaluate(() => ({
          title: document.querySelector('h1.article-title')?.textContent?.trim(),
          imageCount: document.querySelectorAll('.article-content img').length,
          loadedImages: [...document.querySelectorAll('.article-content img')].filter((image) => image.complete && image.naturalWidth > 0).length,
          aiLabels: [...document.querySelectorAll('.article-content em')].filter((node) => /AI生成|AI-generated/.test(node.textContent)).length,
          sources: document.querySelectorAll('.robu-sources li a').length,
          affiliate: document.querySelectorAll('a[rel~="sponsored"]').length,
          conclusion: [...document.querySelectorAll('.article-content h2')].some((heading) => /ろぶーの結論|Robu's Take/.test(heading.textContent)),
          selection: document.body.classList.contains('robus-selection-page'),
          nav: document.querySelectorAll('.main-nav a').length,
          footerSocial: document.querySelectorAll('.site-footer a[href*="facebook"],.site-footer a[href*="instagram"],.site-footer a[href*="x.com"],.site-footer a[href*="reddit"],.site-footer a[href*="tiktok"]').length,
          overflow: document.documentElement.scrollWidth > window.innerWidth,
          robots: document.querySelector('meta[name="robots"]')?.content,
        }));
        if (response.status() !== 200 || !data.title || data.imageCount !== 2 || data.loadedImages !== 2 || data.aiLabels < 2 || data.sources !== 4 || data.affiliate !== 3 || !data.conclusion || !data.selection || data.nav < 2 || data.footerSocial !== 5 || data.overflow || !data.robots?.startsWith('index,follow')) {
          throw new Error(JSON.stringify({ width, route, status: response.status(), ...data }));
        }
        console.log(width, route, 'PASS', JSON.stringify(data));
      }
      await page.goto('http://127.0.0.1:8765/', { waitUntil: 'networkidle' });
      await page.locator('a[data-filter="selection"]').click();
      const category = await page.evaluate(() => ({
        hash: location.hash,
        visibleTarget: [...document.querySelectorAll('#articleCards a')].some((link) => link.getAttribute('href') === '/articles/plarail-air-ana-passenger-plane-set/' && link.offsetParent !== null),
        visibleCount: [...document.querySelectorAll('#articleCards article.card')].filter((card) => card.offsetParent !== null).length,
      }));
      if (category.hash !== '#selection' || !category.visibleTarget || !category.visibleCount) {
        throw new Error(JSON.stringify({ width, category }));
      }
      console.log(width, '/#selection', 'PASS', JSON.stringify(category));
      await page.close();
    }
  } finally {
    await browser.close();
  }
})().catch((error) => { console.error(error); process.exitCode = 1; });
