# Robu 投稿アプリ — Buffer不要・無料で始める

ブログの新しい記事から6つのSNS用の紹介文・画像・短い動画を用意する、PythonとHTMLのアプリです。Buffer・有料の文章生成API・X APIへの接続はありません。

## 最初にできること

- 記事を選び、Instagram／Facebook／X／TikTok／Threads／Pinterestの紹介文を見る。
- 紹介文を調整してコピーする。画像または12秒のスライド動画を保存する。
- 各SNSの投稿画面を開く。投稿が終わったら端末内の完了メモを付ける。
- 自動投稿の接続後は、新しい記事を公開すると接続済みSNSへ直接送信する。

**アプリの作成と、SNSアカウントの接続・公開設定は別の作業です。初期状態では自動送信しません。**

## 無料運用の範囲（2026年9月6日確認）

| SNS | このアプリの対応 | 接続条件 |
| --- | --- | --- |
| Instagram | 画像＋紹介文を公式APIで直接投稿。未接続時は手動 | プロアカウント（ビジネス／クリエイター）、Metaアプリ、投稿権限、アクセストークン |
| Facebook | Facebookページへ画像＋紹介文を直接投稿。未接続時は手動 | ページ管理権限、Metaアプリ、ページトークン。個人プロフィールへのAPI投稿は対象外 |
| Threads | 画像＋紹介文を直接投稿。未接続時は手動 | Threadsアプリ、テスター／公開利用に応じた権限とトークン |
| Pinterest | 画像・紹介文・記事リンクをピンとして直接投稿。未承認時は手動 | ビジネスアカウント、APIアプリのStandard access承認、ボード、トークン |
| X | 紹介文を入れた投稿画面を開く。画像は保存して添付 | API不要。最後の投稿操作は本人が行う |
| TikTok | 画像から縦型動画を作成し、アップロード画面を開く | API不要。最後の投稿操作と公開範囲等の設定は本人が行う |

Metaの権限やアプリ審査の要否は、本人・テスターだけの利用か、外部ユーザーに提供するかで異なります。アプリを作るだけで審査や認可がなくなるわけではありません。

PinterestのTrialで作ったピンは作成者にだけ見えるテスト用です。公開投稿の承認を確認するまで、自動投稿を有効にしない仕組みです。Standard accessはAPIの利用承認であり、Bufferの有料契約ではありません。Xは公式APIが従量課金なので呼び出しません。TikTokのDirect Post APIは自分用の投稿ユーティリティを認めない条件があるため実装していません。

現在の公開GitHubリポジトリでは、通常のGitHub Actions実行環境を無料で利用できます。追加サーバーは借りません。既存ドメイン等の費用は従来どおりです。リポジトリを非公開にする場合は無料枠と料金が変わります。素材にはキャッシュを使い、ダウンロード用の実行成果物は3日で削除します。GitHubの有料利用枠を増やす設定は行いません。

## まずアプリを開く

生成される `social-posting-app.zip` をWindowsのEドライブの任意のフォルダに「すべて展開」してください。中の `social-studio/index.html` をChromeで開きます。Pythonのインストールは不要です。ZIP内から直接開かず、展開してください。

左の記事を選び、SNSのタブを切り替えます。「画像を保存／動画を保存」「紹介文をコピー」「投稿画面を開く」の順で使います。投稿先のアカウントはSNSの画面で確認してください。ボタンを押しても、勝手に投稿はされません。

確認用アプリのPinterestでは、画像を保存してピン作成画面にアップロードします。記事リンクは紹介文の末尾から設定してください。Instagram・TikTokの紹介文にある「プロフィールのブログリンク」を使うには、プロフィールにもブログURLを登録してください。生成画像／広告等の表示は各SNSで投稿内容に合わせて設定します。

編集文章と完了チェックは、開いたChrome・端末だけの記録です。別の端末との同期やSNSでの投稿確認は行いません。ブラウザのデータ削除で消える場合があります。自動投稿に使う文章はブログのメタ情報から生成し、端末内の編集文章とは連動しません。

公開設定後のアプリURLは `https://www.axis-jp.net/social-studio/` です。公開済み記事・素材だけを表示し、パスワードやトークンの入力画面は置きません。検索対象外の指定はしますが、このURLや投稿記録は秘密の管理画面ではありません。設定変更や自動投稿の操作にはGitHubの権限が必要です。

## GitHubで無料の素材生成を開始する

対象は **Axis-koji/robu-travel-journal** です。古いKojiMorimoto側のリポジトリでは有効にしません。

1. この変更をmainに取り込みます。現在のサイト公開方式・CNAME・HTTPS設定を控えてください。
2. GitHub → Settings → Secrets and variables → Actions → Variablesで、`SOCIAL_SITE_REPOSITORY` を `Axis-koji/robu-travel-journal`、`SOCIAL_PUBLISH_ENABLED` を `false` に設定します。`SOCIAL_AUTO_PLATFORMS` は未設定で始められます。
3. Actions → **Robu free posting app** → Run workflow → main → `initialize` を1回実行します。現在ある公開記事を除外して投稿記録を作ります。SNSへの送信はありません。再初期化は拒否されます。
4. 同じ画面で `preview` を実行します。記事フォルダ名は既定の `vietnam-coffee` など、存在する記事を指定してください。Artifactsの `social-preview-and-plan` を保存・展開し、その中の `_site/social-posting-app.zip` をさらに展開して確認できます。この実行ではブログを公開しません。
5. プレビューが成功したら、Settings → Pages → Build and deployment → Sourceを **GitHub Actions** に変更します。これは従来の「Deploy from a branch」からの切り替えです。Custom domainの `www.axis-jp.net` とEnforce HTTPSを保持してください。
6. Actionsから `publish` を実行します。ブログとアプリを公開しますが、`SOCIAL_PUBLISH_ENABLED=false` なのでSNSには送信しません。Pagesの公開成功と既存記事の表示を確認してください。
7. 以後、mainへ新しい記事を追加すると、アプリに紹介文と素材が届きます。PCを閉じていてもGitHub側で実行します。

初期化直後の本番アプリは、過去記事を除外するため空です。確認用アプリだけに指定した既存記事を表示できます。本番アプリには初期化後の記事を新しい順に最大30件表示します。それ以前の投稿記録は保持されます。素材・投稿対象は記事のHTMLから判定するため、記事一覧だけを更新しても新規記事にはなりません。

## 自動投稿の接続

最初は1つだけ接続して動作確認し、必要に応じて追加できます。6つの接続を揃える必要はありません。

### GitHub ActionsのSecrets（非公開）

接続するSNSのものだけ設定します。値をGitのファイル、公開アプリ、チャット、ログに貼り付けないでください。

| Secret | 内容 |
| --- | --- |
| `FACEBOOK_PAGE_ACCESS_TOKEN` | 対象Facebookページのアクセストークン |
| `INSTAGRAM_ACCESS_TOKEN` | Instagram Loginで取得した対象プロアカウントのトークン |
| `THREADS_ACCESS_TOKEN` | 対象Threadsユーザーのトークン |
| `PINTEREST_ACCESS_TOKEN` | Standard承認済みアプリから、対象ボードへ書き込めるトークン |

GitHubの投稿記録用トークンはActions標準の `GITHUB_TOKEN` を使います。PATの購入やBuffer APIキーは不要です。

### Variables（非秘密）

| Variable | 内容 |
| --- | --- |
| `SOCIAL_AUTO_PLATFORMS` | 自動化するSNSだけをカンマ区切り。例：`facebook,instagram,threads`。最初は空 |
| `FACEBOOK_PAGE_ID` | Facebookページの数値ID |
| `INSTAGRAM_USER_ID` | Instagram LoginのAPIで取得したユーザーID。ユーザー名ではない |
| `THREADS_USER_ID` | Threads APIのユーザーID |
| `PINTEREST_BOARD_ID` | 投稿先ボードの数値ID |
| `PINTEREST_STANDARD_ACCESS` | PinterestのStandard承認後だけ `true` |
| `META_GRAPH_VERSION` | 任意。既定は `v26.0` |
| `SOCIAL_SITE_REPOSITORY` | `Axis-koji/robu-travel-journal` |
| `SOCIAL_PUBLISH_ENABLED` | 初期は `false`、接続確認後に `true` |

### 各SNSで用意するもの

- **Facebook：** Meta for Developersで用途に合うアプリを作り、ページに対する `pages_manage_posts` と `pages_read_engagement` 等の必要権限を取得します。ページ一覧を取得する操作には `pages_show_list` も必要です。ページを管理できるユーザーから発行したページトークンを使います。
- **Instagram：** この実装は **Instagram API with Instagram Login** を使います。`instagram_business_basic` と `instagram_business_content_publish` を許可し、対応するプロアカウントのID・トークンを使ってください。Facebook Login方式のトークンとは混在させません。
- **Threads：** Threads用アプリを作り、本人／テスターの承諾または必要な審査を済ませ、`threads_basic` と `threads_content_publish` を許可します。
- **Pinterest：** ビジネスアカウントでアプリを作り、OAuthで `boards:read`、`pins:write` 等の必要権限を許可します。公開投稿にはStandard accessへの申請が必要です。本人だけの利用でもOAuthの動作を示す録画が求められます。

トークンには期限や失効条件があります。可能な場合は長期トークンを使い、失効時は再認可してSecretを更新します。この版はトークンの自動更新・OAuthログイン画面を備えていません。アカウント作成・開発者登録・認可は本人の操作が必要です。

### 接続を有効にする順序

1. `SOCIAL_PUBLISH_ENABLED=false` のまま、接続先のSecretsとVariablesを設定します。
2. Actionsでmainの `connect` を実行します。アカウント／ボードのIDを読み取り確認し、新しい接続先についてその時点の既存記事を除外します。SNSへの投稿はありません。読み取り成功だけでは、投稿権限や公開審査の完了までは保証できません。
3. `SOCIAL_PUBLISH_ENABLED=true` にし、`publish` を実行してアプリ表示を更新します。connect以前の記事は自動投稿しません。
4. 次に公開する記事で実際の投稿を確認します。アプリの「投稿状況を更新」とGitHub Actionsの実行履歴を確認し、各SNSでも画像・リンク・公開範囲を確認してください。
5. 追加のSNSも同じ手順で接続できます。追加先には、それ以前の記事をまとめて送りません。

自動投稿を一時停止する場合は `SOCIAL_PUBLISH_ENABLED=false` にしてください。停止中に手動で投稿した記事は、再開後の自動投稿と重複する可能性があります。**自動対象の記事は停止中も手動投稿しない**でください。停止期間にすでに手動投稿した場合は、停止したままActionsの `connect` で `exclude_current` にチェックを付けて実行します。現在ある記事を自動投稿から除外した後に再開できます。通常の接続追加時にはこのチェックを付けません。

## 記事の情報と投稿素材

対象は `articles/<記事フォルダ名>/index.html`。`<article>` または `og:type=article` を含み、タイトルとdescriptionを設定してください。

- `og:title` / `og:description` / `og:image` を優先します。元記事にない事実は生成しません。
- 画像はリポジトリ内のPNG/JPEG/WebP。外部サイトの画像を自動取得しません。
- 下書き、`noindex`、`social:publish=false`、未来の公開日時の記事は対象外です。
- 日付のみは日本時間で扱います。未来日時になった瞬間のタイマー実行はありません。日時経過後のmain更新または `publish` 実行で検出します。
- 生成画像は紹介文と素材に表記します。誤判定は `social:ai-image` または `social/config.json` のoverrideで調整します。明示的に無効にする場合はoverrideの `ai_image: false` を使ってください。
- 広告等の補足は `social:disclosure` に設定すると各SNSの紹介文にも入ります。
- 商品画像は縦横比を保ち、全体を収めます。架空の部品や商品描写を加えません。
- TikTok用は元の静止画から作る12秒の縦型スライド動画です。実際に撮影した映像や音声ではありません。
- 自動投稿は各SNSにつき記事1本を1投稿にします。同じ記事の編集で再投稿はしません。1回の実行上限は新規記事3本です。超えた場合は `publish` を再実行します。

## エラーと重複投稿防止

投稿履歴はGitHubの `social-state` ブランチに記録します。送信前に記録を書き、SNSから投稿IDを受け取った後で投稿済みにします。保存できない場合は次の送信を止めます。

- `published`：SNS APIから投稿IDを受信。実際の表示やSNSのその後の審査までは保証しません。
- `rejected`：APIが明示的に拒否。設定修正後に再実行できます。
- `submitting` / `uncertain`：結果不明。再送による二重投稿を避けるため自動再送しません。他のSNSへの投稿は続けます。
- `accepted`：旧方式の受付記録がある場合。移行時も再送しません。

画像の処理待ちは最大5回確認します。ネットワークや応答が不明なときは、勝手に同じ投稿を繰り返しません。GitHubの実行通知はご自身の通知設定に従います。このアプリ自体からメール・DMは送りません。

結果不明の復旧は、そのSNSで投稿の有無を確認した後に行います。ローカルで `GITHUB_REPOSITORY` と記録を書き込める `GITHUB_TOKEN` を安全に設定して実行します。

```bash
# 投稿を確認できたとき
python -m scripts.social resolve --key 記事フォルダ名:threads --outcome published --post-id 確認した投稿ID
# 投稿が存在しないと確認できたときだけ
python -m scripts.social resolve --key 記事フォルダ名:threads --outcome retry
```

公開済み／旧方式で受付済みの記録は、retryへの変更を拒否します。台帳を削除してやり直す運用はしません。初期化・公開・投稿は同じ同時実行制御に入れ、公開コミットの照合後に送信します。

## 開発・ローカル確認

Python 3.12、Pillow、ffmpeg、Noto Sans CJKが必要です。生成済みアプリの利用だけならPythonは不要です。

```bash
python -m pip install -r scripts/social/requirements.txt
python -m unittest discover -s tests/social -v
node --check social/studio/app.js
python -m scripts.social build --preview-article vietnam-coffee
```

Windowsで生成する場合は `SOCIAL_FONT` に日本語フォントの絶対パスを設定し、ffmpegをPATHに置いてください。生成先は `_site/social-posting-app.zip` です。プレビューの生成にはSNSの秘密情報は不要です。

この版の検証は、記事抽出・文字数・無料の投稿先制限・台帳保存失敗・通信結果不明・重複防止・公式APIの要求形式・ZIPの内容を対象としたローカルテストです。本人のSNSへの実投稿は、認可情報がないため未検証です。

## 公式資料

- [Instagramの投稿](https://developers.facebook.com/documentation/instagram-platform/content-publishing)
- [Facebookページの投稿](https://developers.facebook.com/documentation/pages-api/posts)
- [Threadsの投稿](https://developers.facebook.com/documentation/threads/posts)
- [Pinterestのアクセス区分と申請](https://developers.pinterest.com/docs/key-concepts/access-tiers/)
- [X API料金](https://docs.x.com/x-api/getting-started/pricing)
- [TikTokのContent Sharing Guidelines](https://developers.tiktok.com/doc/content-sharing-guidelines)
- [GitHub Actionsの利用料金](https://docs.github.com/en/billing/concepts/product-billing/github-actions)
- [GitHub Pagesのカスタムワークフロー](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)
