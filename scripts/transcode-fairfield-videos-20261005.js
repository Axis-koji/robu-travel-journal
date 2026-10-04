const fs = require('fs');
const path = require('path');
const { chromium } = require('C:/Users/yrt11/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');

const sourceDir = 'E:/Documents/ろぶーの気になる事（記事）/フェアフィールド京丹波';
const sourceBaseUrl = 'http://127.0.0.1:8765/' + encodeURIComponent('ろぶーの気になる事（記事）') + '/' + encodeURIComponent('フェアフィールド京丹波') + '/';
const outputDir = path.resolve(__dirname, '../assets/videos/articles/fairfield-by-marriott-kyoto-kyotamba-stay');
const files = [
  { file: 'VID_20260927_125742.mp4' },
  { file: 'VID_20260926_202841.mp4' },
  { file: 'VID_20260926_200652.mp4' },
];

(async () => {
  fs.mkdirSync(outputDir, { recursive: true });
  const browser = await chromium.launch({
    headless: true,
    executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe',
    args: ['--allow-file-access-from-files', '--autoplay-policy=no-user-gesture-required'],
  });
  try {
    const page = await browser.newPage();
    for (const item of files) {
      const file = item.file;
      const targetName = file.replace(/\.mp4$/i, '-muted-720p.webm');
      const target = path.join(outputDir, targetName);
      if (fs.existsSync(target) && fs.statSync(target).size > 100000) {
        console.log('EXISTS', targetName, fs.statSync(target).size);
        continue;
      }
      console.log('START', file);
      const sourceUrl = sourceBaseUrl + encodeURIComponent(file);
      await page.goto(sourceUrl, { waitUntil: 'domcontentloaded', timeout: 30000 });
      const [download, details] = await Promise.all([
        page.waitForEvent('download', { timeout: 240000 }),
        page.evaluate(async ({ targetName }) => {
        const video = document.querySelector('video');
        video.muted = true;
        video.playsInline = true;
        await new Promise((resolve, reject) => {
          video.onloadedmetadata = resolve;
          video.onerror = () => reject(new Error('Video load failed'));
        });
        const stream = video.captureStream();
        for (const track of stream.getAudioTracks()) stream.removeTrack(track);
        const mimeType = MediaRecorder.isTypeSupported('video/webm;codecs=vp8')
          ? 'video/webm;codecs=vp8' : 'video/webm';
        const recorder = new MediaRecorder(stream, { mimeType, videoBitsPerSecond: 2200000 });
        const chunks = [];
        recorder.ondataavailable = (event) => { if (event.data.size) chunks.push(event.data); };
        const stopped = new Promise((resolve) => { recorder.onstop = resolve; });
        recorder.start(1000);
        await video.play();
        await new Promise((resolve) => { video.onended = resolve; });
        recorder.stop();
        await stopped;
        const blob = new Blob(chunks, { type: mimeType });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = targetName;
        link.click();
        return { duration: video.duration, width: video.videoWidth, height: video.videoHeight, bytes: blob.size, mimeType };
        }, { targetName })
      ]);
      await download.saveAs(target);
      console.log('DONE', targetName, JSON.stringify(details));
    }
  } finally {
    await browser.close();
  }
})().catch((error) => { console.error(error); process.exitCode = 1; });
