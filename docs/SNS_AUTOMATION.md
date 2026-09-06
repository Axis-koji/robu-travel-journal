# ブログ公開から6つのSNSへ自動投稿

## 追加した機能

対象は **Axis-koji/robu-travel-journal**、公開URLは **https://www.axis-jp.net** です。
KojiMorimoto側は古いフォークで、2026年9月6日に確認した実際の公開元と異なります。

1. mainに追加された articles/記事名/index.html のOGメタタグから紹介内容を用意します。
2. 記事画像からInstagram画像、Pinterest画像、TikTok用の12秒縦型スライド動画を作ります。
3. 記事と素材をGitHub Pagesに公開します。
4. 公開成功後、公開コミットと素材URLを確認してからBuffer APIへ6件の投稿を送ります。

YouTubeは対象外です。動画は画像と文章の紹介スライドで、ナレーションやBGMはありません。
自動要約AIは呼ばず、元記事にない体験談や仕様を生成しません。
画像内の製品を描き直さず、元画像の全体が見えるように配置します。
SNSからの流入先はアフィリエイト直リンクではなくブログ記事です。

**導入しただけでは実投稿しません。接続・初期化・有効化が必要です。**
本番アカウントへのAPI接続・実投稿は、アカウント未接続のため未検証です。

## Bufferの準備

[Buffer](https://buffer.com/)で次の6アカウントを接続してください。

| SNS | 接続先 |
|---|---|
| Facebook | 「ろぶーの気になる事」のFacebookページ |
| Instagram | ビジネスまたはクリエイターのプロアカウント |
| X | 仕事用アカウント |
| TikTok | 仕事用アカウント。Bufferで自動公開可能な接続にする |
| Threads | 投稿先アカウント |
| Pinterest | 投稿先アカウントと保存先ボード |

Instagram・TikTokのプロフィールにはブログのリンクを設定してください。
アカウントがクリックできるプロフィールリンクに対応していることも確認してください。
紹介文は「プロフィールのブログリンクから」と案内します。
TikTok側でリンクを設定できない場合は、案内をアカウントに合う文面に変更してから有効化します。

Buffer無料プランは3チャンネルまでです。6アカウントを1つのBufferで扱うには有料プランが必要です。
料金・上限は[契約時の料金ページ](https://buffer.com/pricing)で確認してください。
この変更は契約・課金・SNS連携を申し込みません。Zapierの契約は不要です。

BufferのSettings → APIで個人APIキーを作り、GitHub Secretに登録します。
キーをHTML・設定JSON・チャットに書かないでください。

チャンネルIDとPinterestボードIDは、手元のリポジトリで次のコマンドから取得できます。
APIキーを求められたら入力します（画面には表示されません）。

    python -m pip install -r scripts/social/requirements.txt
    python -m scripts.social check

表示されたnameとserviceをアカウントと照合し、idを下のVariablesに登録します。
Pinterestボードは metadata.boards の serviceId を使います。チャンネルIDとは別です。

## GitHub設定

対象リポジトリの Settings → Secrets and variables → Actions に登録します。

| 種別 | 名前 | 値 |
|---|---|---|
| Secret | BUFFER_API_KEY | Bufferの個人APIキー |
| Variable | BUFFER_CHANNEL_FACEBOOK | FacebookのBufferチャンネルID |
| Variable | BUFFER_CHANNEL_INSTAGRAM | InstagramのBufferチャンネルID |
| Variable | BUFFER_CHANNEL_TWITTER | XのBufferチャンネルID（名前はTWITTER） |
| Variable | BUFFER_CHANNEL_TIKTOK | TikTokのBufferチャンネルID |
| Variable | BUFFER_CHANNEL_THREADS | ThreadsのBufferチャンネルID |
| Variable | BUFFER_CHANNEL_PINTEREST | PinterestのBufferチャンネルID |
| Variable | PINTEREST_BOARD_ID | PinterestのボードserviceId |
| Variable | SOCIAL_SITE_REPOSITORY | Axis-koji/robu-travel-journal |
| Variable | SOCIAL_PUBLISH_ENABLED | 接続確認後にtrue。準備中はfalse |

GITHUB_TOKENはGitHub Actionsが自動発行します。個人アクセストークンは不要です。
記録用social-stateブランチへ書き込むジョブには contents: write が必要です。
組織ポリシーやブランチルールで禁止されている場合は初期化時に停止します。

## 有効化の順番

1. 変更をmainへ反映します。変数未設定なら新しい公開・投稿処理は動きません。
2. Actions → **Blog publish and social** → Run workflow で **preview** を実行します。
   確認用の記事名の初期値はvietnam-coffeeです。SNSには送信されません。
   実行結果のsocial-preview-and-planをダウンロードし、画像・動画・captions.jsonを確認します。
3. 上記のSecretとVariablesを登録します。SOCIAL_PUBLISH_ENABLEDはまずfalseにします。
4. 同じワークフローをmainで **initialize** にして1回だけ実行します。
   現時点の既存記事はすべて除外され、過去記事の大量投稿を防ぎます。
   初期化後から、まだ公開していない新しい記事を追加してください。
5. Settings → Pages → Build and deployment → Source を **GitHub Actions** に変更します。
   従来のブランチ公開からの切り替えです。Custom domainのwww.axis-jp.netとHTTPS設定を維持します。
6. **publish** を手動実行します。SNS送信はfalseのままなのでサイトと素材の公開だけを確認できます。
7. Bufferの接続先と生成例を確認できたら、SOCIAL_PUBLISH_ENABLEDをtrueにします。
   次の新着記事のmainへのpushから、自動公開と6SNSへの送信が動きます。

記事より先にSNS投稿が出ないよう、このワークフローがGitHub Pages公開も担当します。
現在の公開経路と同時稼働させず、手順5で切り替えてください。
ブログを更新する手元のPythonスクリプトは変更する必要がありません。

## 記事ごとの設定

基本情報はog:title、og:description、og:imageから読み取ります。
古いaxis-jp.netの記事も、SNSに渡すURLはwww.axis-jp.netに統一します。
画像は同じリポジトリ内のPNG/JPEG/WebPが必要です。外部画像は取得しません。

投稿対象外にするにはHTMLに次のタグを追加します。

    <meta name="social:publish" content="false">

robots=noindex、article:status=draft、未来のarticle:published_timeも対象外です。
日付のみ・時差指定なしの公開日は日本時間として扱います。
未来日になった記事は、その日以降のpushまたはpublish実行時に検出されます。
公開日時ぴったりに起動する予約投稿機能ではありません。

SNS向けに調整する場合はsocial/config.jsonのoverridesに記事フォルダ名を追加できます。
次の例は設定の一部分です。site_url等の既存キーは残してください。

    "overrides": {
      "記事フォルダ名": {
        "title": "SNS向けの見出し",
        "description": "記事に書かれている内容の紹介",
        "image": "/articles/記事フォルダ名/hero.jpg",
        "ai_image": false,
        "disclosure": "PR：この記事にはアフィリエイトリンクが含まれます。"
      }
    }

disclosureは各SNS紹介文の冒頭に表示します。
HTMLのmeta name="social:disclosure"でも指定できます。
生成画像の自動判定が誤っている場合はai_imageを明示してください。
生成画像は画像・紹介文に注記し、Instagram/TikTokのAPIフラグも設定します。

## 重複防止・エラー対応

- 投稿記録はmainと分離したsocial-stateブランチの.social/state.jsonに残します。
- 同じ記事フォルダ名とSNSの組み合わせは、受付済みなら再送しません。本文修正も再投稿しません。
- 一部のSNSだけ成功した場合、成功済みを飛ばして残りを処理します。
- API送信前にsubmittingを永続保存します。
  通信切断・応答不明・送信後の保存失敗は、重複防止を優先して自動再送を止めます。
- acceptedは**Buffer受付済み**です。SNS側の最終公開成功とは別です。
  Bufferの配信エラーや再認証通知も確認してください。
- 1回の実行で新着記事を最大3本扱います。残りがあるとジョブに表示します。
  publishを再実行すると、成功済みを飛ばして残りを処理します。
- 初期化した投稿記録を削除したり、initializeを繰り返したりしないでください。

送信結果が不明な場合は、Bufferの送信済み・キュー・失敗一覧で記事を確認します。
resolveはその確認結果を記録する管理コマンドで、SNSへの送信自体はしません。
GitHub書込権限のある環境でGITHUB_TOKENとGITHUB_REPOSITORYを設定して実行します。

Bufferに存在する投稿を受付済みとして記録する例：

    python -m scripts.social resolve --key "記事フォルダ名:facebook" --outcome accepted --post-id "確認したBuffer投稿ID"

Bufferに存在しないこと、または配信が失敗したことを確認して再送可能に戻す例：

    python -m scripts.social resolve --key "記事フォルダ名:facebook" --outcome retry

その後publishを再実行します。Buffer側から同じ投稿が再配信されないことを確認してください。
GitHubの投稿記録への書き込みが失敗した場合は、API送信せず停止します。

## 停止・切り戻し

SNSだけ止める場合はSOCIAL_PUBLISH_ENABLED=falseにします。サイト公開は継続できます。
公開も従来方式へ戻す場合はSOCIAL_SITE_REPOSITORYを空にし、
PagesのSourceを元のブランチ公開（main / root）へ戻します。
すでにBufferが受け付けた投稿は、この変数では取り消されません。Bufferで個別に確認します。

## 開発・確認

    python -m unittest discover -s tests/social -v
    python -m scripts.social catalog

画像・動画にはPillow、日本語のNoto Sans CJK、FFmpegが必要です。Actionsでは自動で用意します。
ローカルではSOCIAL_FONTに日本語フォントファイルのパスを指定できます。
出力をリポジトリの外へ保存する例：

    python -m scripts.social build --preview-article vietnam-coffee --out ../social-preview --plan ../social-preview-plan/plan.json

## 確認した公式仕様

- [Buffer API開始手順](https://developers.buffer.com/guides/getting-started.html)
- [CreatePostInput](https://developers.buffer.com/types/CreatePostInput.html)
- [Instagram投稿メタデータ](https://developers.buffer.com/types/InstagramPostMetadataInput.html)
- [TikTok投稿メタデータ](https://developers.buffer.com/types/TikTokPostMetadataInput.html)
- [Pinterest投稿メタデータ](https://developers.buffer.com/types/PinterestPostMetadataInput.html)
- [GitHub Pagesのカスタムワークフロー](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)

API型は2026年9月6日時点で照合しました。
TikTokはAPI型に掲載されていますが、ガイドの対応SNS一覧には記載がなく、
実アカウントでの自動投稿可否は接続後の検証が必要です。
