export const html = String.raw`<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>TikTokへ送る | Robu Posting App</title><link rel="stylesheet" href="/style.css"><script src="/app.js" defer></script></head>
<body><main><header><a href="https://www.axis-jp.net/social-studio/">Robu Posting App</a><h1>TikTokへ動画を送る</h1><p>動画を確認して下書きへ送信。最後の編集・公開はTikTokで行います。</p></header>
<p id="message" role="status" aria-live="polite">接続状態を確認しています…</p>
<section id="login" hidden><h2>TikTokに接続</h2><p>表示名の確認と、動画を下書きへ送る権限を使用します。</p><a class="button" href="/oauth/start">TikTokに接続する</a></section>
<section id="workspace" hidden><div class="account"><p>送信先：<strong id="account-name"></strong></p><button id="disconnect" class="secondary" type="button">接続を解除</button></div>
<label for="articles">記事を選ぶ</label><select id="articles"></select><p id="empty" hidden>送信できる記事がありません。ブログで新しい記事を公開すると表示されます。</p>
<div id="editor" class="editor" hidden><div><video id="video" controls playsinline preload="metadata"></video><p id="media-note" class="small"></p></div><div><h2 id="title"></h2><label for="caption">紹介文</label><textarea id="caption" rows="9" readonly></textarea><button id="copy" class="secondary" type="button">紹介文をコピー</button><p class="small">紹介文はTikTokの編集画面で貼り付けてください。</p>
<label class="confirm"><input id="confirm" type="checkbox">動画と送信先を確認しました</label><button id="send" type="button" disabled>TikTokの下書きへ送る</button><button id="check" class="secondary" type="button">送信状況を確認</button><p id="delivery" role="status" aria-live="polite"></p><p>TikTokの受信トレイに通知が届いたら開き、紹介文・公開範囲・AI生成や広告の表示を確認して投稿してください。</p></div></div></section>
<footer><a href="https://www.axis-jp.net/terms/">利用規約</a><a href="https://www.axis-jp.net/privacy-policy/">プライバシーポリシー</a><p>接続情報は暗号化して保管します。「接続を解除」でTikTokの許可と、このアプリの接続情報・送信記録を削除します。TikTok側の動画は削除しません。</p></footer></main></body></html>`;

export const css = String.raw`:root{font-family:system-ui,-apple-system,"Noto Sans JP",sans-serif;color:#10293b;background:#f3f6f9;line-height:1.65}*{box-sizing:border-box}body{margin:0}main{max-width:1000px;margin:40px auto;padding:0 24px}h1{font-size:2rem;margin:14px 0}h2{font-size:1.2rem}header p{margin-bottom:24px}a{color:#09577f}section{background:#fff;padding:26px;border:1px solid #cedae3;border-radius:12px;margin:20px 0}label{display:block;font-weight:600;margin:14px 0 8px}select,textarea,button,.button{font:inherit}select,textarea{width:100%;padding:12px;border:1px solid #8ba0ad;border-radius:6px;background:#fff;color:inherit}button,.button{display:inline-block;background:#126741;color:white;padding:11px 18px;border:0;border-radius:6px;cursor:pointer;text-decoration:none;font-weight:650;margin:8px 8px 8px 0}button:disabled{opacity:.55;cursor:default}.secondary{background:#e6edf2;color:#173749}.account{display:flex;align-items:center;justify-content:space-between;gap:16px;border-bottom:1px solid #d6e0e6;margin-bottom:20px}.editor{display:grid;grid-template-columns:minmax(180px,300px) 1fr;gap:30px;margin-top:24px}video{width:100%;aspect-ratio:9/16;background:#122332;border-radius:8px}.small,footer{font-size:.875rem;color:#526674}.confirm{display:flex;align-items:flex-start;gap:10px;font-size:1rem}.confirm input{width:20px;height:20px;flex-shrink:0;margin-top:4px}#message{padding:12px 16px;background:#e2edf3;border-radius:6px}#delivery{font-weight:600}footer a{margin-right:20px}footer{margin:30px 0}a:focus-visible,button:focus-visible,input:focus-visible,select:focus-visible,textarea:focus-visible{outline:3px solid #d57b16;outline-offset:3px}[hidden]{display:none!important}@media(max-width:680px){main{margin:20px auto;padding:0 16px}section{padding:18px}.editor{grid-template-columns:1fr}.editor video{max-height:460px}.account{align-items:flex-start;flex-direction:column;gap:0}h1{font-size:1.65rem}}`;

export const clientJS = String.raw`"use strict";
const $=id=>document.getElementById(id);
let csrf='', articles=[], current=null, status='not_sent', busy=false, generation=0;
const labels={not_sent:'まだ送信していません。',submitting:'送信受付の結果を確認中です。再送はしていません。',processing:'TikTokで動画を処理しています。',inbox:'TikTokの受信トレイに通知を送りました。TikTokで編集・投稿してください。',published:'TikTokでの投稿が完了しました。',failed:'TikTokで動画の処理に失敗しました。条件を確認してから再送できます。',rejected:'TikTokが受け付けませんでした。接続権限・審査状態・動画の条件を確認してください。',uncertain:'送信結果を確認できません。重複を防ぐため再送は停止しています。TikTokの受信トレイも確認してください。'};
function message(text){$('message').textContent=text;}
function controls(){
 $('send').disabled=busy||!current||!$('confirm').checked||!['not_sent','failed','rejected'].includes(status);
 $('send').textContent=['failed','rejected'].includes(status)?'確認した動画を再送する':'TikTokの下書きへ送る';
 $('check').disabled=busy||!current; $('articles').disabled=busy; $('disconnect').disabled=busy;
 $('delivery').textContent=labels[status]||labels.uncertain;
}
async function api(path,data){
 const r=await fetch(path,{method:data===undefined?'GET':'POST',credentials:'same-origin',cache:'no-store',headers:data===undefined?{}:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:data===undefined?undefined:JSON.stringify(data)});
 const result=await r.json();
 if(!r.ok){const e=new Error(result.error|| (result.duplicate?'この動画はすでに送信を試みています。送信状況を確認してください。':'処理を完了できませんでした。'));e.result=result;throw e;}
 return result;
}
async function check(){
 if(!current)return;
 const id=current.id, version=generation;
 try{const result=await api('/api/status?article='+encodeURIComponent(id));if(version===generation){status=result.status;controls();}}
 catch(e){if(version===generation)message(e.message);}
}
async function select(){
 current=articles.find(a=>a.id===$('articles').value)||null;generation++;
 $('editor').hidden=!current;$('confirm').checked=false;status='checking';controls();
 if(!current)return;
 $('title').textContent=current.title;$('video').src=current.video;$('caption').value=current.caption;
 $('media-note').textContent='12秒・音声なしの縦型スライド動画。'+(current.aiImage?'生成画像の表記を含みます。':'記事に使用した画像から作成しています。');
 await check();
}
$('articles').addEventListener('change',select);
$('confirm').addEventListener('change',controls);
$('check').addEventListener('click',check);
$('copy').addEventListener('click',async()=>{try{await navigator.clipboard.writeText($('caption').value);message('紹介文をコピーしました。TikTokの編集画面で貼り付けてください。');}catch{$('caption').focus();$('caption').select();message('紹介文を選択しました。Ctrl+Cでコピーしてください。');}});
$('send').addEventListener('click',async()=>{
 if($('send').disabled)return;
 busy=true;const retry=['failed','rejected'].includes(status);status='submitting';controls();message('動画をTikTokへ送っています…');
 try{const result=await api('/api/upload',{articleId:current.id,confirmed:true,retry});status=result.status;message('TikTokが動画を受け付けました。送信状況を確認してください。');}
 catch(e){status=e.result?.status||'uncertain';message(e.message);await check();}
 finally{busy=false;$('confirm').checked=false;controls();}
});
$('disconnect').addEventListener('click',async()=>{
 if(!confirm('TikTokの接続を解除し、このアプリの接続情報と送信記録を削除しますか？'))return;
 busy=true;controls();try{const r=await api('/api/disconnect',{});$('workspace').hidden=true;$('login').hidden=false;message(r.revoked?'TikTokの接続を解除し、接続情報と送信記録を削除しました。':'このアプリの接続情報と送信記録を削除しました。TikTok側の解除結果は確認できなかったため、TikTokのアプリ権限設定でも確認してください。');}catch(e){message(e.message);busy=false;controls();}
});
async function start(){
 try{
  const s=await api('/api/session');
  $('login').hidden=s.connected;$('workspace').hidden=!s.connected;
  if(!s.connected){message(new URLSearchParams(location.search).has('login')?'接続をキャンセルしました。必要なときに接続してください。':'TikTokに接続すると、記事の動画を選べます。');return;}
  csrf=s.csrf;$('account-name').textContent=s.name;
  const data=await api('/api/catalog');articles=data.articles;
  for(const a of articles){const option=document.createElement('option');option.value=a.id;option.textContent=a.title;$('articles').append(option);}
  const requested=new URLSearchParams(location.search).get('article');if(articles.some(a=>a.id===requested))$('articles').value=requested;
  $('empty').hidden=articles.length>0;message('接続済みです。送信先と動画を確認してください。');await select();
 }catch(e){message(e.message);}
}
start();`;
