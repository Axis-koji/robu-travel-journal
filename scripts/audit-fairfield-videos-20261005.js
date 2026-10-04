const fs = require('fs');
const path = require('path');
const { chromium } = require('C:/Users/yrt11/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const base = 'http://127.0.0.1:8765/' + encodeURIComponent('ろぶーの気になる事（記事）') + '/' + encodeURIComponent('フェアフィールド京丹波') + '/';
const output = 'E:/Documents/ろぶーの気になる事（記事）/フェアフィールド京丹波/draft-20261005-v1/video-audit-20261005';
const files = ['VID_20260927_125742.mp4','VID_20260926_202841.mp4','VID_20260926_200652.mp4'];
(async()=>{
 fs.mkdirSync(output,{recursive:true});
 const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe'});
 try{
  const page=await browser.newPage({viewport:{width:1280,height:900}});
  for(const file of files){
   await page.goto(base+encodeURIComponent(file),{waitUntil:'domcontentloaded'});
   await page.evaluate(async()=>{
    const v=document.querySelector('video');await new Promise(r=>v.readyState>=1?r():v.addEventListener('loadedmetadata',r,{once:true}));v.pause();v.currentTime=0;v.muted=true;v.playbackRate=8;
    const host=document.createElement('div');host.style.cssText='display:grid;grid-template-columns:1fr 1fr;gap:12px;background:#111;padding:12px';v.style.cssText='position:fixed;width:1px;height:1px;opacity:.01';document.body.append(host);
    await v.play();for(const fraction of [.05,.25,.5,.75,.95]){const target=v.duration*fraction;while(v.currentTime<target&&!v.ended)await new Promise(r=>setTimeout(r,80));const box=document.createElement('figure');box.style.cssText='margin:0;color:white;font:18px sans-serif';const c=document.createElement('canvas');const scale=Math.min(1,600/v.videoWidth);c.width=Math.round(v.videoWidth*scale);c.height=Math.round(v.videoHeight*scale);c.getContext('2d').drawImage(v,0,0,c.width,c.height);const cap=document.createElement('figcaption');cap.textContent=`${Math.round(v.currentTime)}s / ${Math.round(v.duration)}s`;box.append(c,cap);host.append(box);}v.pause();
   });
   await page.screenshot({path:path.join(output,file.replace('.mp4','-contact-sheet.png')),fullPage:true});
   console.log('AUDITED',file);
  }
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1});
