import { html, clientJS, css } from './ui.mjs';

const SITE = 'https://www.axis-jp.net';
const API = 'https://open.tiktokapis.com/v2';
const SESSION = '__Host-robu-tiktok';
const STATE = '__Host-robu-tiktok-state';
const enc = new TextEncoder();
const scopes = ['user.info.basic', 'video.upload'];
const random = () => b64(crypto.getRandomValues(new Uint8Array(32)));
const now = () => Math.floor(Date.now() / 1000);
class Failure extends Error {
  constructor(status, message) { super(message); this.status = status; }
}
class Rejection extends Failure {}
const reject = (status, message) => { throw new Failure(status, message); };
function b64(bytes) { return btoa(String.fromCharCode(...bytes)).replaceAll('+', '-').replaceAll('/', '_').replace(/=+$/, ''); }
function unb64(s) { return Uint8Array.from(atob(s.replaceAll('-', '+').replaceAll('_', '/')), c => c.charCodeAt(0)); }
export async function digest(value) { return b64(new Uint8Array(await crypto.subtle.digest('SHA-256', enc.encode(value)))); }
async function key(env) { return crypto.subtle.importKey('raw', unb64(env.TOKEN_ENCRYPTION_KEY), 'AES-GCM', false, ['encrypt', 'decrypt']); }
export async function seal(env, owner, data) {
  const iv = crypto.getRandomValues(new Uint8Array(12));
  const encrypted = await crypto.subtle.encrypt({name:'AES-GCM', iv, additionalData:enc.encode(owner)}, await key(env), enc.encode(JSON.stringify(data)));
  return b64(iv) + '.' + b64(new Uint8Array(encrypted));
}
export async function unseal(env, owner, data) {
  const [iv, encrypted] = data.split('.');
  const plain = await crypto.subtle.decrypt({name:'AES-GCM', iv:unb64(iv), additionalData:enc.encode(owner)}, await key(env), unb64(encrypted));
  return JSON.parse(new TextDecoder().decode(plain));
}
function cookie(name, value, age) { return `${name}=${value}; Path=/; Secure; HttpOnly; SameSite=Lax; Max-Age=${age}`; }
function cookies(request) { return Object.fromEntries((request.headers.get('Cookie') || '').split(';').map(s => s.trim().split('='))); }
function response(body, status=200, type='application/json; charset=utf-8', extra={}) {
  return new Response(type.startsWith('application/json') ? JSON.stringify(body) : body, {status, headers:{
    'Content-Type':type, 'Cache-Control':'no-store', 'Referrer-Policy':'no-referrer',
    'X-Content-Type-Options':'nosniff', 'X-Frame-Options':'DENY', 'X-Robots-Tag':'noindex, nofollow',
    'Content-Security-Policy':`default-src 'none'; script-src 'self'; style-src 'self'; connect-src 'self'; media-src ${SITE}; img-src 'self' ${SITE}; base-uri 'none'; frame-ancestors 'none'; form-action 'self'`,
    ...extra
  }});
}
function redirect(path, setCookies=[]) {
  const r = response('', 303, 'text/plain', {Location:path});
  for (const c of setCookies) r.headers.append('Set-Cookie', c);
  return r;
}
function configured(env) {
  try {
    const origin = new URL(env.APP_ORIGIN);
    return origin.protocol === 'https:' && origin.origin === env.APP_ORIGIN && env.DB &&
      env.TIKTOK_CLIENT_KEY && env.TIKTOK_CLIENT_SECRET && unb64(env.TOKEN_ENCRYPTION_KEY).length === 32;
  } catch { return false; }
}
async function limitedText(message, max=65536) {
  if (Number(message.headers.get('Content-Length')) > max) reject(413, 'データが大きすぎます。');
  const reader = message.body?.getReader();
  if (!reader) return '';
  const pieces=[]; let length=0;
  try {
    while (true) {
      const {value, done} = await reader.read(); if(done) break;
      length += value.byteLength;
      if (length > max) { await reader.cancel(); reject(413, 'データが大きすぎます。'); }
      pieces.push(value);
    }
  } finally { reader.releaseLock(); }
  const result = new Uint8Array(length); let offset=0;
  for(const p of pieces) {result.set(p, offset);offset+=p.length;}
  return new TextDecoder().decode(result);
}
async function api(env, path, body, token, form=false) {
  let r, data;
  try {
    r = await (env.transport || fetch)(API + path, {
      method:body === undefined ? 'GET' : 'POST', redirect:'error', signal:AbortSignal.timeout(20000),
      headers:{'Content-Type':form ? 'application/x-www-form-urlencoded' : 'application/json', ...(token ? {Authorization:'Bearer '+token} : {})},
      body:body === undefined ? undefined : form ? new URLSearchParams(body).toString() : JSON.stringify(body)
    });
    const text = await limitedText(r); data = text ? JSON.parse(text) : {};
  } catch { throw new Failure(502, 'TikTokとの通信結果を確認できません。時間をおいて状態を確認してください。'); }
  const error = typeof data.error === 'string' ? data.error : data.error?.code;
  if (r.status >= 500) throw new Failure(502, 'TikTokの処理結果を確認できません。自動再送はしていません。');
  if (!r.ok || (error && error !== 'ok')) throw new Rejection(400, 'TikTokが処理を受け付けませんでした。接続権限・審査状態・動画の条件を確認してください。');
  return data;
}
function tokenData(raw, expectedOwner) {
  if (typeof raw.open_id !== 'string' || !raw.open_id || (expectedOwner && raw.open_id !== expectedOwner) ||
      typeof raw.access_token !== 'string' || !raw.access_token || typeof raw.refresh_token !== 'string' || !raw.refresh_token ||
      !scopes.every(s => String(raw.scope || '').split(',').includes(s)) ||
      !Number.isFinite(raw.expires_in) || raw.expires_in <= 0 || !Number.isFinite(raw.refresh_expires_in) || raw.refresh_expires_in <= 0)
    reject(400, 'TikTokのプロフィールと下書き送信の両方を許可して、もう一度接続してください。');
  return {access:raw.access_token, refresh:raw.refresh_token, expires:now()+raw.expires_in, refreshExpires:now()+raw.refresh_expires_in};
}
async function session(request, env, required=true) {
  const value = cookies(request)[SESSION];
  const row = /^[\w-]{43}$/.test(value || '') ? await env.DB.prepare('SELECT * FROM sessions WHERE session_hash=? AND expires>?').bind(await digest(value), now()).first() : null;
  if (!row && required) reject(401, 'TikTokに接続してください。');
  return row;
}
async function access(env, owner) {
  const row = await env.DB.prepare('SELECT * FROM accounts WHERE open_id=?').bind(owner).first();
  if (!row) reject(401, 'TikTokに接続し直してください。');
  const tokens = await unseal(env, owner, row.sealed_tokens);
  if(tokens.expires > now()+120) return tokens.access;
  if(tokens.refreshExpires <= now()+120) reject(401, 'TikTokの接続期限が切れました。接続し直してください。');
  const lock = random();
  const claim = await env.DB.prepare('UPDATE accounts SET lock_id=?,lock_until=? WHERE open_id=? AND lock_until<?').bind(lock,now()+60,owner,now()).run();
  if(claim.meta.changes !== 1) reject(409, '接続を更新中です。少し待ってから操作してください。');
  try {
    const current = await env.DB.prepare('SELECT sealed_tokens FROM accounts WHERE open_id=?').bind(owner).first();
    const latest = await unseal(env, owner, current.sealed_tokens);
    if(latest.expires > now()+120) return latest.access;
    const raw = await api(env,'/oauth/token/',{client_key:env.TIKTOK_CLIENT_KEY,client_secret:env.TIKTOK_CLIENT_SECRET,grant_type:'refresh_token',refresh_token:latest.refresh},undefined,true);
    const fresh = tokenData(raw, owner);
    const update = await env.DB.prepare('UPDATE accounts SET sealed_tokens=? WHERE open_id=? AND lock_id=?').bind(await seal(env,owner,fresh),owner,lock).run();
    if(update.meta.changes !== 1) reject(409, '接続状態が変わりました。接続し直してください。');
    return fresh.access;
  } finally {await env.DB.prepare('UPDATE accounts SET lock_id=\'\',lock_until=0 WHERE open_id=? AND lock_id=?').bind(owner,lock).run();}
}
export function parseCatalog(text) {
  const match = /^\s*window\.ROBU_SOCIAL_MANIFEST\s*=\s*([\s\S]+);\s*$/.exec(text);
  if(!match) reject(502, '記事データを読み込めません。');
  let data; try {data=JSON.parse(match[1]);} catch {reject(502,'記事データを読み込めません。');}
  if(data.version !== 2 || data.repository !== 'Axis-koji/robu-travel-journal' || String(data.site_url||'').replace(/\/$/,'') !== SITE || !Array.isArray(data.articles)) reject(502,'記事データの形式を確認できません。');
  return data.articles.filter(a=>typeof a.id === 'string' && /^[a-zA-Z0-9_-]{1,160}$/.test(a.id)).slice(0,30).map(a=>({
    id:a.id, title:String(a.title||a.id).slice(0,500), caption:String(a.posts?.tiktok||'').slice(0,6000),
    video:SITE+'/assets/social/'+a.id+'/tiktok.mp4', aiImage:a.ai_image === true
  }));
}
async function catalog(env) {
  const r = await (env.transport||fetch)(SITE+'/social-studio/data.js',{redirect:'error',signal:AbortSignal.timeout(15000)});
  if(!r.ok) reject(502,'記事データを取得できません。');
  return parseCatalog(await limitedText(r,1024*1024));
}
async function callback(request, env, url) {
  const state = url.searchParams.get('state'), ownState = cookies(request)[STATE];
  if(!state || state !== ownState || !/^[\w-]{43}$/.test(state)) reject(400,'認証を開始した画面から、接続をやり直してください。');
  const used = await env.DB.prepare('DELETE FROM oauth_states WHERE state_hash=? AND expires>? RETURNING state_hash').bind(await digest(state),now()).first();
  if(!used) reject(400,'認証の期限が切れました。接続をやり直してください。');
  if(url.searchParams.has('error')) return redirect('/?login=cancelled',[cookie(STATE,'',0)]);
  const code = url.searchParams.get('code');
  if(!code || code.length>4096) reject(400,'認証コードを確認できません。');
  const raw = await api(env,'/oauth/token/',{client_key:env.TIKTOK_CLIENT_KEY,client_secret:env.TIKTOK_CLIENT_SECRET,code,grant_type:'authorization_code',redirect_uri:env.APP_ORIGIN+'/oauth/callback'},undefined,true);
  const tokens = tokenData(raw);
  const user = await api(env,'/user/info/?fields=open_id,display_name',undefined,tokens.access);
  if(user.data?.user?.open_id !== raw.open_id) reject(400,'接続アカウントを確認できません。');
  const id=random(), csrf=random();
  const encrypted = await seal(env,raw.open_id,tokens);
  await env.DB.batch([
    env.DB.prepare('INSERT INTO accounts(open_id,display_name,sealed_tokens) VALUES(?,?,?) ON CONFLICT(open_id) DO UPDATE SET display_name=excluded.display_name,sealed_tokens=excluded.sealed_tokens,lock_id=\'\',lock_until=0').bind(raw.open_id,String(user.data.user.display_name||'TikTok').slice(0,200),encrypted),
    env.DB.prepare('DELETE FROM sessions WHERE open_id=? OR expires<?').bind(raw.open_id,now()),
    env.DB.prepare('INSERT INTO sessions(session_hash,open_id,csrf,expires) VALUES(?,?,?,?)').bind(await digest(id),raw.open_id,csrf,now()+43200)
  ]);
  return redirect('/',[cookie(STATE,'',0),cookie(SESSION,id,43200)]);
}
async function send(env, s, data) {
  if(data.confirmed !== true || typeof data.articleId !== 'string') reject(400,'動画と送信先を確認してください。');
  const article=(await catalog(env)).find(a=>a.id === data.articleId);
  if(!article) reject(404,'記事が見つかりません。');
  const token = await access(env,s.open_id);
  if(data.retry === true) await env.DB.prepare('DELETE FROM uploads WHERE open_id=? AND article_id=? AND status IN (\'rejected\',\'failed\')').bind(s.open_id,article.id).run();
  const claim=await env.DB.prepare('INSERT OR IGNORE INTO uploads(open_id,article_id,status,created) VALUES(?,?,\'submitting\',?)').bind(s.open_id,article.id,now()).run();
  if(claim.meta.changes !== 1) {
    const previous=await env.DB.prepare('SELECT status FROM uploads WHERE open_id=? AND article_id=?').bind(s.open_id,article.id).first();
    return response({status:previous?.status||'uncertain', duplicate:true},409);
  }
  try {
    const result=await api(env,'/post/publish/inbox/video/init/',{source_info:{source:'PULL_FROM_URL',video_url:article.video}},token);
    if(typeof result.data?.publish_id !== 'string' || !result.data.publish_id) throw new Failure(502,'送信結果を確認できません。');
    await env.DB.prepare('UPDATE uploads SET publish_id=?,status=\'processing\' WHERE open_id=? AND article_id=?').bind(result.data.publish_id,s.open_id,article.id).run();
    return response({status:'processing'});
  } catch(e) {
    const status=e instanceof Rejection ? 'rejected' : 'uncertain';
    await env.DB.prepare('UPDATE uploads SET status=? WHERE open_id=? AND article_id=?').bind(status,s.open_id,article.id).run();
    throw e;
  }
}
async function checkStatus(env,s,articleId) {
  const row=await env.DB.prepare('SELECT * FROM uploads WHERE open_id=? AND article_id=?').bind(s.open_id,articleId).first();
  if(!row) return response({status:'not_sent'});
  if(!row.publish_id || ['published','failed'].includes(row.status) || row.checked>now()-10) return response({status:row.status});
  const result=await api(env,'/post/publish/status/fetch/',{publish_id:row.publish_id},await access(env,s.open_id));
  const status={SEND_TO_USER_INBOX:'inbox',PUBLISH_COMPLETE:'published',FAILED:'failed',PROCESSING_DOWNLOAD:'processing',PROCESSING_UPLOAD:'processing'}[result.data?.status]||'uncertain';
  await env.DB.prepare('UPDATE uploads SET status=?,checked=? WHERE open_id=? AND article_id=?').bind(status,now(),s.open_id,articleId).run();
  return response({status});
}
export default {
  async fetch(request,env) {
    try {
      const url = new URL(request.url);
      if(!['GET','POST'].includes(request.method)) return response({error:'許可されていない操作です。'},405);
      if(url.pathname==='/' && request.method==='GET') return response(html,200,'text/html; charset=utf-8');
      if(url.pathname==='/app.js' && request.method==='GET') return response(clientJS,200,'text/javascript; charset=utf-8');
      if(url.pathname==='/style.css' && request.method==='GET') return response(css,200,'text/css; charset=utf-8');
      if(!configured(env)) reject(503,'TikTokの接続設定を準備しています。');
      if(url.origin !== env.APP_ORIGIN) reject(403,'登録されたアドレスから開いてください。');
      if(url.pathname==='/oauth/callback' && request.method==='GET') return await callback(request,env,url);
      if(url.pathname==='/oauth/start' && request.method==='GET') {
        const state=random();
        await env.DB.batch([env.DB.prepare('DELETE FROM oauth_states WHERE expires<?').bind(now()),env.DB.prepare('INSERT INTO oauth_states(state_hash,expires) VALUES(?,?)').bind(await digest(state),now()+600)]);
        const target=new URL('https://www.tiktok.com/v2/auth/authorize/');
        target.search=new URLSearchParams({client_key:env.TIKTOK_CLIENT_KEY,scope:scopes.join(','),response_type:'code',redirect_uri:env.APP_ORIGIN+'/oauth/callback',state,disable_auto_auth:'1'}).toString();
        return redirect(target.href,[cookie(STATE,state,600)]);
      }
      const s=await session(request,env,false);
      if(url.pathname==='/api/session' && request.method==='GET') {
        if(!s) return response({connected:false});
        const account=await env.DB.prepare('SELECT display_name FROM accounts WHERE open_id=?').bind(s.open_id).first();
        return response({connected:true,name:account.display_name,csrf:s.csrf});
      }
      if(!s) reject(401,'TikTokに接続してください。');
      if(request.method==='POST') {
        if(request.headers.get('Origin') !== env.APP_ORIGIN || request.headers.get('X-CSRF-Token') !== s.csrf) reject(403,'画面を開き直して操作してください。');
        if(!(request.headers.get('Content-Type')||'').startsWith('application/json')) reject(415,'操作内容を確認できません。');
        let data; try {data=JSON.parse(await limitedText(request,2048));} catch(e) {if(e instanceof Failure) throw e; reject(400,'操作内容を確認できません。');}
        if(!data || Array.isArray(data) || typeof data !== 'object') reject(400,'操作内容を確認できません。');
        if(url.pathname==='/api/upload') return await send(env,s,data);
        if(url.pathname==='/api/disconnect') {
          const row=await env.DB.prepare('SELECT sealed_tokens FROM accounts WHERE open_id=?').bind(s.open_id).first();
          const tokens=await unseal(env,s.open_id,row.sealed_tokens);
          let revoked=true;
          try {await api(env,'/oauth/revoke/',{client_key:env.TIKTOK_CLIENT_KEY,client_secret:env.TIKTOK_CLIENT_SECRET,token:tokens.access},undefined,true);} catch {revoked=false;}
          await env.DB.prepare('DELETE FROM accounts WHERE open_id=?').bind(s.open_id).run();
          return response({connected:false,revoked},200,undefined,{'Set-Cookie':cookie(SESSION,'',0)});
        }
      }
      if(url.pathname==='/api/catalog' && request.method==='GET') return response({articles:await catalog(env)});
      if(url.pathname==='/api/status' && request.method==='GET') {
        const id=url.searchParams.get('article');
        if(!/^[a-zA-Z0-9_-]{1,160}$/.test(id||'')) reject(400,'記事を選んでください。');
        return await checkStatus(env,s,id);
      }
      return response({error:'ページが見つかりません。'},404);
    } catch(e) {return response({error:e instanceof Failure ? e.message : '処理を完了できませんでした。時間をおいて確認してください。'},e instanceof Failure ? e.status : 500);}
  }
};
