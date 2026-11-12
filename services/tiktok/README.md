# Robu Posting App — TikTok connection

Cloudflare Workers + D1で動かす、既存ブログ専用のTikTok連携サービス。
ブログ本体は引き続きGitHub Pages。ConoHaへのログインやサイトの移転は不要。

## 実装範囲

- Login Kit WebのOAuth、state照合・一回限りの認証、本人の表示名の確認。
- `user.info.basic` と `video.upload` のみ。Direct Post・`video.publish`は使わない。
- トークンはWorkerのSecretを鍵にAES-256-GCMで暗号化し、D1へ保存。ブラウザにはHttpOnlyセッションCookieだけを渡す。
- トークン更新時の排他制御、更新されたrefresh tokenの保存。
- 公開中の `https://www.axis-jp.net/social-studio/data.js` をJSONとして読み、記事IDから自サイト内の動画URLを組み立てる。外部スクリプトの実行や任意URLの代理取得は行わない。
- 動画・送信先の確認後、Content Posting APIのUploadで下書き送信。紹介文はTikTokの編集画面で貼り付ける。
- 同じアカウント・記事の送信をDBの一意制約で管理。受付結果不明では再送しない。TikTokが明確に拒否・失敗した場合のみ、本人の確認操作で再送できる。
- 接続解除時にTikTokの許可を取り消し、D1の接続情報・セッション・送信記録を削除。TikTokの既存動画は削除しない。

## 現在の状態

このコードの追加だけではAPIは有効にならない。Cloudflareへの配置、Secret設定、TikTokの試験・審査は別途必要。モックテストの成功を実アカウントへの送信成功と扱わない。

## 配置手順（担当者用）

1. 既存のCloudflareアカウントでWorkers Freeを確認する。有料プランへの変更は行わない。
2. D1データベース `robu-tiktok` を作成し、`schema.sql` を適用する。
3. `wrangler.example.jsonc` を `wrangler.jsonc` にコピーし、作成されたD1 IDと実際のHTTPS公開先を設定する。例示用のIDやホストをそのまま登録しない。
4. WorkerにSecretとして `TIKTOK_CLIENT_KEY`、`TIKTOK_CLIENT_SECRET`、`TOKEN_ENCRYPTION_KEY`（暗号学的乱数32バイトのbase64url表現）を設定する。鍵・トークンをGit、チャット、コマンドライン引数、操作ログへ出さない。
5. `APP_ORIGIN` に実際のHTTPS originを設定して配置する。コールバックは、そのoriginに `/oauth/callback` を付けたURL。リクエストログは認証コードを含むためObservabilityを有効化しない。
6. 最初はTikTokのSandbox `Robu API Test`（ID `7684535758350288904`）のキーを使う。Login KitとContent Posting APIを追加し、実際のcallbackを登録。対象の本人アカウントを試験ユーザーとして認可する。
7. この実装は `PULL_FROM_URL` を使うため、**使う環境ごとに** `https://www.axis-jp.net/` のURL prefix所有確認が必要。Productionでは2026-09-12に確認済み。Sandboxに新しい確認ファイルが求められたら、そのファイルもブログへ配置して検証する。
8. 本人が接続し、試験用の動画を選び、内容を確認して下書き送信を試す。受信トレイへの到着を確認する。本番投稿はTikTok内で本人が行う。
9. 実際の認証・動画選択・下書き送信・TikTok通知を記録し、審査の説明・デモ動画として提出する。動かない画面や合成した成功画面をデモにしない。
10. 認可情報の取扱いを既存サイトのプライバシーポリシーに反映し、審査が通った後でProductionキーに切り替える。SandboxとProductionではDBを分ける。

サービスの利用者は、認証した自分のTikTokアカウントにだけ送信できる。ほかの利用者の接続情報・送信記録にはアクセスできない。セッションは12時間。トークン更新は操作時に行い、自動投稿・定期送信は追加しない。

既存投稿アプリからは、配置完了後に `実際のサービスorigin/?article=記事ID` へリンクする。公開先未確定の段階では、既存アプリの動く手動投稿導線を置き換えない。

## 検証

Node.js 22.13以上で `npm test`。NodeのSQLiteを使い、本物のスキーマ、OAuth state再利用拒否、Cookie属性、権限不足、CSRF、ユーザー間の分離、二重送信防止、エラー時の再送抑止、暗号化・更新を確認する。外部APIはモックであり、テスト中は動画を送らない。

## 公式資料

- [TikTok Login Kit Web](https://developers.tiktok.com/doc/login-kit-web/)
- [User Access Token Management](https://developers.tiktok.com/docs/en/oauth-user-access-token-management)
- [Upload](https://developers.tiktok.com/docs/en/content-posting-api-get-started-upload-content)
- [Get Post Status](https://developers.tiktok.com/docs/en/content-posting-api-reference-get-video-status)
- [Workers pricing](https://developers.cloudflare.com/workers/platform/pricing/)
- [D1 pricing](https://developers.cloudflare.com/d1/platform/pricing/)

Workers Freeは1日100,000リクエスト・1回のCPU時間10ms。D1にも無料枠があり、Freeの上限到達時は処理が停止する。無料枠内での実測確認が必要であり、追加料金の契約変更は行わない。
