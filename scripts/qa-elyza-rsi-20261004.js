const { chromium } = require('C:/Users/yrt11/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');

(async () => {
  const browser = await chromium.launch({ headless: true, executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe' });
  try {
    for (const width of [390, 1180, 1440]) {
      const page = await browser.newPage({ viewport: { width, height: 900 } });
      for (const route of [
        '/articles/elyza-rsi-research-ai-improves-ai/',
        '/en/articles/elyza-rsi-research-ai-improves-ai/',
      ]) {
        const response = await page.goto('http://127.0.0.1:8765' + route, { waitUntil: 'networkidle' });
        const data = await page.evaluate(() => ({
          title: document.querySelector('h1.article-title')?.textContent?.trim(),
          imageCount: document.querySelectorAll('.article-content img').length,
          loadedImages: [...document.querySelectorAll('.article-content img')].filter((image) => image.complete && image.naturalWidth > 0).length,
          aiLabels: [...document.querySelectorAll('.robu-image-caption')].filter((node) => /AI生成|AI-generated/.test(node.textContent)).length,
          sources: document.querySelectorAll('.robu-sources li a').length,
          internalLinks: [...document.querySelectorAll('.article-content a')].filter((node) => /segt-ai-evaluation/.test(node.getAttribute('href') || '')).length,
          conclusion: [...document.querySelectorAll('.article-content h2')].some((heading) => /ろぶーの結論|Robu's Take/.test(heading.textContent)),
          prePublicationNote: /公開前メモ|Pre-publication note/.test(document.body.innerText),
          nav: document.querySelectorAll('.main-nav a').length,
          footerSocial: document.querySelectorAll('.site-footer a[href*="facebook"],.site-footer a[href*="instagram"],.site-footer a[href*="x.com"],.site-footer a[href*="reddit"],.site-footer a[href*="tiktok"]').length,
          overflow: document.documentElement.scrollWidth > window.innerWidth,
          robots: document.querySelector('meta[name="robots"]')?.content,
          socialPublish: document.querySelector('meta[name="social:publish"]')?.content,
          disclosure: document.querySelectorAll('.robu-editorial-note').length,
        }));
        if (response.status() !== 200 || !data.title || data.imageCount !== 2 || data.loadedImages !== 2 || data.aiLabels !== 2 || data.sources !== 5 || data.internalLinks < 1 || !data.conclusion || data.prePublicationNote || data.nav < 2 || data.footerSocial !== 5 || data.overflow || !data.robots?.startsWith('index,follow') || data.socialPublish !== 'false' || data.disclosure !== 1) {
          throw new Error(JSON.stringify({ width, route, status: response.status(), ...data }));
        }
        console.log(width, route, 'PASS', JSON.stringify(data));
      }
      await page.goto('http://127.0.0.1:8765/', { waitUntil: 'networkidle' });
      const home = await page.evaluate(() => ({
        target: [...document.querySelectorAll('#articleCards a')].some((link) => link.getAttribute('href') === '/articles/elyza-rsi-research-ai-improves-ai/'),
        duplicateCount: [...document.querySelectorAll('#articleCards article.card')].filter((card) => card.querySelector('a[href="/articles/elyza-rsi-research-ai-improves-ai/"]')).length,
      }));
      if (!home.target || home.duplicateCount !== 1) throw new Error(JSON.stringify({ width, home }));
      console.log(width, '/', 'PASS', JSON.stringify(home));
      await page.close();
    }
  } finally {
    await browser.close();
  }
})().catch((error) => { console.error(error); process.exitCode = 1; });
