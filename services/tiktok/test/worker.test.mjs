import test from 'node:test';
import assert from 'node:assert/strict';
import { DatabaseSync } from 'node:sqlite';
import { readFileSync } from 'node:fs';
import worker, {digest,seal,unseal,parseCatalog} from '../worker.mjs';
import {clientJS} from '../ui.mjs';
import { Script } from 'node:vm';

const ORIGIN='https://tiktok.example.com';
const SCHEMA=readFileSync(new URL('../schema.sql',import.meta.url),'utf8');
const manifest={version:2,repository:'Axis-koji/robu-travel-journal',site_url:'https://www.axis-jp.net',articles:[{id:'sample',title:'確認用の記事',video:'https://evil.example/video.mp4',posts:{tiktok:'紹介文'}}]};
class D1 {
  constructor(){this.db=new DatabaseSync(':memory:');this.db.exec(SCHEMA);}
  prepare(sql){const db=this.db;return {bind(...values){return {async first(){return db.prepare(sql).get(...values)||null;},async run(){const r=db.prepare(sql).run(...values);return {success:true,meta:{changes:r.changes}};}};}};}
  async batch(queries){this.db.exec('BEGIN');try{const results=[];for(const q of queries)results.push(await q.run());this.db.exec('COMMIT');return results;}catch(e){this.db.exec('ROLLBACK');throw e;}}
}
const json=(value,status=200)=>new Response(JSON.stringify(value),{status,headers:{'Content-Type':'application/json'}});
function environment(){
 const calls=[];const env={APP_ORIGIN:ORIGIN,DB:new D1(),TIKTOK_CLIENT_KEY:'test-key',TIKTOK_CLIENT_SECRET:'test-secret',TOKEN_ENCRYPTION_KEY:Buffer.alloc(32,7).toString('base64url')};
 env.transport=async(url,options={})=>{
  calls.push({url,options});
  if(url.endsWith('/social-studio/data.js'))return new Response('window.ROBU_SOCIAL_MANIFEST = '+JSON.stringify(manifest)+';\n');
  if(url.endsWith('/oauth/token/'))return json({open_id:'owner',access_token:'private-access',refresh_token:'private-refresh',expires_in:86400,refresh_expires_in:31536000,scope:'user.info.basic,video.upload'});
  if(url.includes('/user/info/'))return json({data:{user:{open_id:'owner',display_name:'ろぶー'}},error:{code:'ok'}});
  if(url.endsWith('/inbox/video/init/'))return json({data:{publish_id:'v_inbox_url~test'},error:{code:'ok'}});
  if(url.endsWith('/status/fetch/'))return json({data:{status:'SEND_TO_USER_INBOX'},error:{code:'ok'}});
  if(url.endsWith('/oauth/revoke/'))return json({});
  throw new Error('Unexpected endpoint');
 };
 return {env,calls};
}
async function login(env){
 const start=await worker.fetch(new Request(ORIGIN+'/oauth/start'),env);
 assert.equal(start.status,303);
 const cookie=start.headers.get('set-cookie').split(';')[0];
 const auth=new URL(start.headers.get('location'));
 const state=auth.searchParams.get('state');
 const url=ORIGIN+'/oauth/callback?'+new URLSearchParams({code:'one-time-code',state});
 const r=await worker.fetch(new Request(url,{headers:{Cookie:cookie}}),env);
 return {start,auth,callback:r,url,stateCookie:cookie,cookie:r.headers.getSetCookie().find(c=>c.startsWith('__Host-robu-tiktok='))?.split(';')[0]};
}
async function client(env){
 const l=await login(env);assert.equal(l.callback.status,303);
 const session=await worker.fetch(new Request(ORIGIN+'/api/session',{headers:{Cookie:l.cookie}}),env);
 const s=await session.json();
 return {l,s,request:(path,body)=>new Request(ORIGIN+path,{method:body===undefined?'GET':'POST',headers:{Cookie:l.cookie,Origin:ORIGIN,'X-CSRF-Token':s.csrf,'Content-Type':'application/json'},body:body===undefined?undefined:JSON.stringify(body)})};
}

test('OAuth is single use, cookies secure, and tokens never reach browser',async()=>{
 const {env,calls}=environment();const {l,s}=await client(env);
 assert.equal(l.auth.searchParams.get('redirect_uri'),ORIGIN+'/oauth/callback');
 assert.equal(l.auth.searchParams.get('scope'),'user.info.basic,video.upload');
 assert.match(l.callback.headers.get('set-cookie'),/Secure; HttpOnly; SameSite=Lax/);
 const body=JSON.stringify(s);assert.ok(!body.includes('private-'));assert.equal(s.name,'ろぶー');
 const row=env.DB.db.prepare('SELECT * FROM accounts').get();assert.ok(!row.sealed_tokens.includes('private-'));
 assert.equal((await unseal(env,'owner',row.sealed_tokens)).access,'private-access');
 assert.ok(calls.filter(c=>c.url.includes('oauth/token')).every(c=>c.options.redirect==='error'));
 const replay=await worker.fetch(new Request(l.url,{headers:{Cookie:l.stateCookie}}),env);assert.equal(replay.status,400);
 assert.equal(calls.filter(c=>c.url.endsWith('/oauth/token/')).length,1);
});
test('missing browser state is rejected before exchanging code',async()=>{
 const {env,calls}=environment();const r=await worker.fetch(new Request(ORIGIN+'/oauth/callback?code=stolen&state=bad'),env);
 assert.equal(r.status,400);assert.equal(calls.length,0);
});
test('cancelled OAuth consumes state without creating an account',async()=>{
 const {env}=environment();const r=await worker.fetch(new Request(ORIGIN+'/oauth/start'),env);
 const state=new URL(r.headers.get('location')).searchParams.get('state');
 const result=await worker.fetch(new Request(ORIGIN+'/oauth/callback?'+new URLSearchParams({state,error:'access_denied'}),{headers:{Cookie:r.headers.get('set-cookie').split(';')[0]}}),env);
 assert.equal(result.headers.get('location'),'/?login=cancelled');assert.equal(env.DB.db.prepare('SELECT count(*) AS n FROM accounts').get().n,0);
});
test('missing upload scope prevents login and token persistence',async()=>{
 const {env}=environment();const transport=env.transport;
 env.transport=async(url,opts)=>url.endsWith('/oauth/token/')?json({open_id:'owner',access_token:'a',refresh_token:'b',scope:'user.info.basic',expires_in:1000,refresh_expires_in:1000}):transport(url,opts);
 const l=await login(env);assert.equal(l.callback.status,400);assert.equal(env.DB.db.prepare('SELECT count(*) AS n FROM accounts').get().n,0);
});
test('mutations require same origin, CSRF and explicit video confirmation',async()=>{
 const {env,calls}=environment();const c=await client(env);
 const request=c.request('/api/upload',{articleId:'sample',confirmed:true});request.headers.set('Origin','https://evil.example');
 assert.equal((await worker.fetch(request,env)).status,403);
 const csrf=c.request('/api/upload',{articleId:'sample',confirmed:true});csrf.headers.delete('X-CSRF-Token');
 assert.equal((await worker.fetch(csrf,env)).status,403);
 assert.equal((await worker.fetch(c.request('/api/upload',{articleId:'sample',confirmed:false}),env)).status,400);
 assert.equal(calls.filter(c=>c.url.endsWith('/inbox/video/init/')).length,0);
});
test('only own-site video is submitted and duplicate requests do not send twice',async()=>{
 const {env,calls}=environment();const c=await client(env);const body={articleId:'sample',confirmed:true};
 const results=await Promise.all([worker.fetch(c.request('/api/upload',body),env),worker.fetch(c.request('/api/upload',body),env)]);
 assert.deepEqual(results.map(r=>r.status).sort(),[200,409]);
 const sends=calls.filter(c=>c.url.endsWith('/inbox/video/init/'));assert.equal(sends.length,1);
 assert.deepEqual(JSON.parse(sends[0].options.body),{source_info:{source:'PULL_FROM_URL',video_url:'https://www.axis-jp.net/assets/social/sample/tiktok.mp4'}});
 const status=await worker.fetch(c.request('/api/status?article=sample'),env);assert.deepEqual(await status.json(),{status:'inbox'});
 assert.equal((await worker.fetch(c.request('/api/upload',{...body,retry:true}),env)).status,409);
});
test('ambiguous network failures block retry, even with retry flag',async()=>{
 const {env,calls}=environment();const c=await client(env);const transport=env.transport;
 env.transport=async(url,opts)=>{if(url.endsWith('/inbox/video/init/')){calls.push({url});throw new Error('network after send');}return transport(url,opts);};
 const body={articleId:'sample',confirmed:true};assert.equal((await worker.fetch(c.request('/api/upload',body),env)).status,502);
 const state=await worker.fetch(c.request('/api/status?article=sample'),env);assert.deepEqual(await state.json(),{status:'uncertain'});
 assert.equal((await worker.fetch(c.request('/api/upload',{...body,retry:true}),env)).status,409);
 assert.equal(calls.filter(c=>c.url.endsWith('/inbox/video/init/')).length,1);
});
test('explicit API rejection can be retried only by a confirmed retry action',async()=>{
 const {env}=environment();const c=await client(env);const transport=env.transport;let attempts=0;
 env.transport=async(url,opts)=>{if(url.endsWith('/inbox/video/init/')&&attempts++===0)return json({error:{code:'scope_not_authorized'}},401);return transport(url,opts);};
 const body={articleId:'sample',confirmed:true};assert.equal((await worker.fetch(c.request('/api/upload',body),env)).status,400);
 assert.equal((await worker.fetch(c.request('/api/upload',body),env)).status,409);
 assert.equal((await worker.fetch(c.request('/api/upload',{...body,retry:true}),env)).status,200);
});
test('refresh stores rotated credentials; competing updates are locked',async()=>{
 const {env,calls}=environment();const c=await client(env);
 const old={access:'expired',refresh:'old-refresh',expires:1,refreshExpires:9999999999};
 env.DB.db.prepare('UPDATE accounts SET sealed_tokens=?').run(await seal(env,'owner',old));
 const r=await worker.fetch(c.request('/api/upload',{articleId:'sample',confirmed:true}),env);assert.equal(r.status,200);
 const row=env.DB.db.prepare('SELECT * FROM accounts').get();const tokens=await unseal(env,'owner',row.sealed_tokens);
 assert.equal(tokens.refresh,'private-refresh');assert.equal(row.lock_until,0);
 assert.equal(new URLSearchParams(calls.filter(c=>c.url.endsWith('/oauth/token/')).at(-1).options.body).get('refresh_token'),'old-refresh');
 env.DB.db.prepare('UPDATE accounts SET sealed_tokens=?,lock_until=?').run(await seal(env,'owner',old),9999999999);
 const locked=await worker.fetch(c.request('/api/status?article=sample'),env);assert.equal(locked.status,409);
});
test('sessions isolate accounts and disconnect deletes only their own data',async()=>{
 const {env}=environment();const c=await client(env);
 await worker.fetch(c.request('/api/upload',{articleId:'sample',confirmed:true}),env);
 const value='x'.repeat(43),otherTokens=await seal(env,'other',{access:'other',refresh:'r',expires:9999999999});
 env.DB.db.prepare('INSERT INTO accounts(open_id,display_name,sealed_tokens) VALUES(?,?,?)').run('other','別アカウント',otherTokens);
 env.DB.db.prepare('INSERT INTO sessions VALUES(?,?,?,?)').run(await digest(value),'other','csrf',9999999999);
 const r=await worker.fetch(new Request(ORIGIN+'/api/status?article=sample',{headers:{Cookie:'__Host-robu-tiktok='+value}}),env);
 assert.deepEqual(await r.json(),{status:'not_sent'});
 const disconnected=await worker.fetch(c.request('/api/disconnect',{}),env);assert.equal(disconnected.status,200);
 assert.equal(env.DB.db.prepare('SELECT count(*) AS n FROM uploads').get().n,0);
 assert.equal(env.DB.db.prepare('SELECT open_id FROM accounts').get().open_id,'other');
 assert.equal((await worker.fetch(c.request('/api/catalog'),env)).status,401);
});
test('tokens are bound to their account; malformed and executable catalogs are rejected',async()=>{
 const {env}=environment();const data=await seal(env,'owner',{access:'secret'});
 await assert.rejects(()=>unseal(env,'someone-else',data));
 assert.throws(()=>parseCatalog('window.ROBU_SOCIAL_MANIFEST = (function(){return {}})();'));
 assert.throws(()=>parseCatalog('window.ROBU_SOCIAL_MANIFEST = {};'));
 assert.equal(parseCatalog('window.ROBU_SOCIAL_MANIFEST = '+JSON.stringify(manifest)+';')[0].video,'https://www.axis-jp.net/assets/social/sample/tiktok.mp4');
});
test('missing deployment configuration is explicit and script parses without browser execution',async()=>{
 const r=await worker.fetch(new Request(ORIGIN+'/api/session'),{});assert.equal(r.status,503);
 const page=await worker.fetch(new Request(ORIGIN+'/'),{});assert.equal(page.status,200);assert.match(page.headers.get('Content-Security-Policy'),/frame-ancestors 'none'/);
 new Script(clientJS);
});
