const { chromium } = require('C:/Users/yrt11/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const slug = 'fairfield-by-marriott-kyoto-kyotamba-stay';
const baseUrl = process.env.PREVIEW_URL || 'http://127.0.0.1:8877';
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe'});
 try{
  for(const width of [390,1180,1440]){
   const page=await browser.newPage({viewport:{width,height:900}});
   for(const route of [`/articles/${slug}/`,`/en/articles/${slug}/`]){
    const response=await page.goto(baseUrl+route,{waitUntil:'domcontentloaded'});await page.waitForTimeout(1200);
    const d=await page.evaluate(()=>({
      title:document.querySelector('h1.article-title')?.textContent?.trim(),images:document.querySelectorAll('.article-content img').length,uniqueImages:new Set([...document.querySelectorAll('.article-content img')].map(i=>i.getAttribute('src'))).size,
      loaded:[...document.querySelectorAll('.article-content img')].filter(i=>i.complete&&i.naturalWidth>0).length,
      videos:document.querySelectorAll('.article-content video').length,autoplay:[...document.querySelectorAll('video')].filter(v=>v.autoplay).length,
      sources:[...document.querySelectorAll('.article-content a')].filter(a=>/marriott\.com|ajim\.info|springs-hiyoshi|kkr\.mlit|penguinbakery/.test(a.href)).length,
      affiliate:[...document.querySelectorAll('a')].filter(a=>a.href.includes('hb.afl.rakuten.co.jp')).map(a=>a.rel),
      disclosure:(document.body.innerText.match(/楽天トラベルのアフィリエイト広告|Rakuten Travel affiliate advertisement/g)||[]).length,
      cave:[...document.querySelectorAll('a')].filter(a=>a.href.includes('/articles/shizushi-drive/')).length,
      conclusion:[...document.querySelectorAll('h2')].some(h=>/ろぶーの結論|Robu’s Take/.test(h.textContent)),
      nav:document.querySelectorAll('.main-nav a').length,social:document.querySelectorAll('.site-footer a[href*="facebook"],.site-footer a[href*="instagram"],.site-footer a[href*="x.com"],.site-footer a[href*="reddit"],.site-footer a[href*="tiktok"]').length,
      overflow:document.documentElement.scrollWidth>window.innerWidth,robots:document.querySelector('meta[name="robots"]')?.content,socialPublish:document.querySelector('meta[name="social:publish"]')?.content,
      bad:/公開前|要レビュー|AIを制作補助|Pre-publication|review required/i.test(document.body.innerText)
    }));
    if(response.status()!==200||!d.title||d.images!==8||d.uniqueImages!==7||d.loaded!==8||d.videos!==3||d.autoplay||d.sources<7||d.affiliate.length!==1||!d.affiliate[0].includes('sponsored')||d.disclosure!==1||d.cave<1||!d.conclusion||d.nav<2||d.social!==5||d.overflow||!d.robots?.startsWith('index,follow')||d.socialPublish!=='true'||d.bad)throw new Error(JSON.stringify({width,route,status:response.status(),...d}));
    console.log(width,route,'PASS',JSON.stringify(d));
   }
   await page.goto(baseUrl+'/',{waitUntil:'domcontentloaded'});await page.waitForTimeout(500);
   const home=await page.evaluate(s=>({count:[...document.querySelectorAll('#articleCards article.card')].filter(card=>card.querySelector(`a[href="/articles/${s}/"]`)).length}),slug);
   if(home.count!==1)throw new Error(JSON.stringify({width,home}));
   await page.goto(baseUrl+'/articles/shizushi-drive/',{waitUntil:'domcontentloaded'});await page.waitForTimeout(500);
   const reciprocal=await page.locator(`a[href="/articles/${slug}/"]`).count();if(reciprocal!==1)throw new Error('Missing reciprocal link');
   console.log(width,'shell/home/reciprocal PASS');await page.close();
  }
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1});
