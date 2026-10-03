const { chromium } = require('C:/Users/yrt11/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');

(async () => {
  const browser = await chromium.launch({ headless: true, executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe' });
  try {
    for (const width of [390, 1280]) {
      const page = await browser.newPage({ viewport: { width, height: 850 } });
      for (const path of [
        '/articles/sony-berlin-philharmonic-partnership-2026/',
        '/en/articles/sony-berlin-philharmonic-partnership-2026/',
        '/articles/kindle-2026-model-comparison/',
        '/en/articles/kindle-2026-model-comparison/',
      ]) {
        const response = await page.goto('http://127.0.0.1:8765' + path, { waitUntil: 'networkidle' });
        const data = await page.evaluate(() => ({
          title: document.querySelector('h1.article-title')?.textContent,
          imageCount: document.querySelectorAll('.article-content img').length,
          loadedImages: [...document.querySelectorAll('.article-content img')].filter(i => i.complete && i.naturalWidth > 0).length,
          sources: document.querySelectorAll('.robu-sources li a').length,
          affiliate: document.querySelectorAll('a[rel~="sponsored"]').length,
          overflow: document.documentElement.scrollWidth > window.innerWidth,
          conclusion: [...document.querySelectorAll('.article-content h2')].some(h => /ろぶーの結論|Robu's Take/.test(h.textContent)),
        }));
        if (response.status() !== 200 || !data.title || data.imageCount !== 2 || data.loadedImages !== 2 || !data.sources || !data.conclusion || data.overflow) {
          throw new Error(JSON.stringify({ width, path, status: response.status(), ...data }));
        }
        if (path.includes('kindle') ? data.affiliate !== 4 : data.affiliate !== 0) {
          throw new Error(JSON.stringify({ width, path, affiliate: data.affiliate }));
        }
        console.log(width, path, 'PASS', data.imageCount + ' images', data.sources + ' sources', data.affiliate + ' affiliate links');
      }
      await page.close();
    }
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
