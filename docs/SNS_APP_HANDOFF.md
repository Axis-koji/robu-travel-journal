# Robu 投稿アプリ｜使い方・保存場所・タスク引き継ぎ

記録日：2026年9月6日（日本時間）

## 最初に読む要点

**Bufferを使わず、無料で始めるSNS投稿アプリを作成済み。確認用ZIPを保存済み。実際のSNSへの自動投稿は未稼働。**

目的は、ブログの記事制作に集中するため、新しい公開記事から6つのSNS向けの紹介文・画像・動画を用意し、接続条件を満たすSNSへ自動投稿すること。日々の想定は新しい記事から2〜3件。YouTubeは今回は対象外。

この記録は2026年9月6日時点の状態を示す。別のタスクで再開するときは、下記のGitHub PRの現在の状態も確認すること。

## 保存先と見つけ方

| 対象 | 場所・名前 | 状態・用途 |
| --- | --- | --- |
| 確認用アプリ本体 | ChatGPTの保存ファイル `Robu-Posting-App.zip` | 作成・保存済み。ファイル名で検索して取得できる |
| アプリのソースコード | [Axis-koji/robu-travel-journal](https://github.com/Axis-koji/robu-travel-journal) | 本番ブログに使っているリポジトリ |
| 作業ブランチ | `codex/blog-social-automation` | 本アプリとドキュメントの保存先 |
| 本番への取り込み候補 | [PR #53](https://github.com/Axis-koji/robu-travel-journal/pull/53) | 記録時点ではDraft・未マージ |
| アプリ実装の確定版 | [コミット 0367bb6](https://github.com/Axis-koji/robu-travel-journal/commit/0367bb6626e8752356cce0175d9dead1184af6c1) | Buffer不要の無料版。以後の記録追加とは区別する |
| この引き継ぎMarkdown | [docs/SNS_APP_HANDOFF.md](https://github.com/Axis-koji/robu-travel-journal/blob/codex/blog-social-automation/docs/SNS_APP_HANDOFF.md) | 別タスクで最初に読む記録 |
| 詳しい設定・復旧手順 | [docs/SNS_AUTOMATION.md](https://github.com/Axis-koji/robu-travel-journal/blob/codex/blog-social-automation/docs/SNS_AUTOMATION.md) | Secrets・Variables・Pages設定・接続・重複防止の説明 |
| Notionの記録先 | [Robu 投稿アプリ｜使い方・保存場所・引き継ぎ（2026-09-06）](https://app.notion.com/p/3d36e74ea10f81a2b817f45d21fe8f41?pvs=204) | 「AI記事制作ワークフロー（公開前）」配下。本文とアプリZIPを保存済み |
| NotebookLMへの登録 | このMarkdownをソースとして登録する | 保存結果は末尾に記録。登録前の状態と区別する |
| 本番アプリの予定URL | `https://www.axis-jp.net/social-studio/` | **公開設定後に使うURL。記録時点で公開済みとは扱わない** |

旧URLの `KojiMorimoto/robu-travel-journal` ではなく、**Axis-koji側**が対象。初期に検討したBuffer経由の案は、ユーザーの「Bufferを使わず、最初は無料」という指示により置き換えた。Bufferへの申し込み・支払いはしていない。

## 今すぐ確認用アプリを使う

1. `Robu-Posting-App.zip` をダウンロードする。
2. Windowsで右クリックし、「すべて展開」を選ぶ。ZIPの中から直接開かない。
3. 保存先は空き容量のあるEドライブを推奨する。例：`E:\Documents\Codex\Apps\Robu-Posting-App\`。**これは保存先の例であり、このPC上に配置済みという意味ではない。**
4. 展開したフォルダ内の `social-studio/index.html` をChromeで開く。生成済みアプリを利用するだけならPythonのインストールは不要。
5. 左側で記事を選び、Instagram・Facebook・X・TikTok・Threads・Pinterestのタブを切り替える。
6. 「画像を保存」または「動画を保存」を押す。
7. 必要なら紹介文を編集し、「紹介文をコピー」を押す。
8. 「投稿画面を開く」でSNSへ移動し、投稿先アカウントを確認する。保存した画像・動画を添付して投稿を確定する。
9. 投稿後は「このSNSへの投稿を完了した」にチェックを付け、端末内のメモとして使える。

確認用ZIPには実際の `vietnam-coffee` 記事を1本入れている。サンプルを含む確認用アプリであり、ブログの最新記事をその場で自動取得するアプリではない。最新記事の継続反映には、後述のGitHub公開処理の設定が必要。

紹介文の編集と完了チェックは、同じChrome・端末だけに保存する。別端末には同期しない。完了チェックはSNS側の投稿成功を確認する機能ではない。自動投稿に使う文章はブログのメタ情報から作り、端末内の編集文章とは連動しない。

## SNSごとの対応

| SNS | 無料版の実装 | 自動化に残っている条件 |
| --- | --- | --- |
| Instagram | 紹介文・縦型画像の準備、公式APIによる直接投稿 | プロアカウント、Instagram Login方式のアプリ・投稿権限・トークン、実投稿の確認 |
| Facebook | 紹介文・縦型画像の準備、Facebookページへの直接投稿 | ページ管理権限・ページトークン、実投稿の確認。個人プロフィールはAPI投稿対象外 |
| Threads | 紹介文・縦型画像の準備、公式APIによる直接投稿 | Threadsアプリ・本人認可・トークン、実投稿の確認 |
| Pinterest | 紹介文・縦型画像・記事リンクの準備、ピンの直接投稿 | APIアプリのStandard access承認・ボード・トークン。Trialのまま公開自動投稿をしない |
| X | 紹介文を入れた投稿画面を開く。画像は保存して添付 | **最後の投稿操作は手動**。有料の公式APIを呼び出す実装はない |
| TikTok | 既存画像から12秒の縦型スライド動画を作り、アップロード画面を開く | **最後の投稿操作は手動**。個人用Direct Post APIの制約により自動送信は実装していない |

生成する画像は元記事の画像全体を収め、架空の商品部品や写真を作り直さない。Instagram用は1080×1350、Pinterest用は1000×1500、TikTok用は1080×1920・12秒・音声なし。生成画像の表記を含む場合がある。

Instagram・TikTokの案内にある「プロフィールのブログリンク」を利用するには、各プロフィールにもブログURLを登録する。公開範囲、AI生成・広告等の表示は、投稿内容に応じてSNS側で設定する。

## 完了していること

- Pythonの素材生成処理、日本語のHTML/CSS/JavaScript投稿画面。
- 4SNSへの公式APIによる直接投稿処理。接続は1つずつ追加できる。
- X・TikTokを含む6SNSの無料の投稿準備・手動投稿導線。
- GitHub Actionsの公開後トリガー、投稿記録、過去記事除外、重複投稿防止。
- 送信前の記録保存が失敗したら送信を止める処理。
- 通信結果不明の場合は勝手に再送しない処理。
- 新しいSNSを接続するとき、それ以前の記事をまとめて送らない処理。
- 実記事から素材と確認用ZIPを生成。
- ローカルの26項目のテスト成功。JavaScript構文、HTMLの操作要素・参照ファイル、ZIPの整合性確認。
- [GitHub CI成功](https://github.com/Axis-koji/robu-travel-journal/actions/runs/34034265067)。

## まだ行っていないこと

- PR #53のmainへのマージ。
- GitHub Pagesの公開元を従来のブランチ公開からGitHub Actionsへ切り替える作業。
- 投稿記録の `initialize` とSNS接続の `connect`。
- SNSアカウントの開発者登録・本人認可・権限設定・トークン設定。
- 実アカウントへの投稿と、各SNSでの表示・公開範囲の確認。
- トークンの自動更新とOAuthログイン画面の実装。
- ユーザーのWindows PC／Eドライブへのアプリ配置。

テスト成功は、SNSの本人アカウントへ投稿できたことを意味しない。現在のZIPも自動送信を行わない。

## 次のタスクが再開するときの順序

1. このMarkdownと `docs/SNS_AUTOMATION.md` を読む。PR #53の最新状態とブランチを確認し、作成済みアプリを一から作り直さない。
2. 確認用ZIPを開き、必要なら画面・文言の調整を行う。
3. 本番適用を進める段階でPRをmainへ取り込み、現在のPages・CNAME・HTTPS設定を確認する。
4. 自動送信は `SOCIAL_PUBLISH_ENABLED=false` のまま、対象リポジトリを設定して `initialize` と `preview` を実行する。
5. プレビュー成功後にPagesをGitHub Actions公開へ切り替え、SNS送信を停止したままブログ・アプリを公開する。ドメインは `www.axis-jp.net`、HTTPSを保持する。
6. 接続するSNSを1つ選び、本人の認可を行う。必要な値をGitHub ActionsのSecretsとVariablesへ設定して `connect` を実行する。
7. 接続条件を確認したうえで自動投稿を有効にし、その後に新しく公開する記事で投稿結果を確認する。順次ほかのSNSも追加する。

自動投稿の対象は公開済みの記事。記事制作ワークフローにある「記事本文は本人が公開を判断する」という運用と、公開後のSNS投稿を区別する。

有料プランへの申し込み、Xの有料API、ブラウザでのパスワード保存、投稿制限の回避はこのアプリに含めない。接続に使う秘密情報は、このMarkdown・Notion・NotebookLM・Gitのファイルへ書かない。

## 実装を探すためのファイル一覧

| リポジトリ内の場所 | 内容 |
| --- | --- |
| `social/studio/index.html` | 投稿画面のHTML |
| `social/studio/style.css` | 画面のデザイン |
| `social/studio/app.js` | 記事選択、コピー、素材保存、手動完了メモ |
| `scripts/social/content.py` | 記事のメタ情報とSNS紹介文の作成 |
| `scripts/social/media.py` | 画像・12秒動画の生成とキャッシュ |
| `scripts/social/providers.py` | Instagram・Facebook・Threads・Pinterestの公式API接続 |
| `scripts/social/publish.py` | 投稿記録、重複防止、失敗時の扱い |
| `scripts/social/studio.py` | 投稿画面用データとZIPの生成 |
| `scripts/social/__main__.py` | catalog/build/initialize/connect/check/publish/resolveの入口 |
| `social/config.json` | サイトURL、SNS、1回の上限、記事ごとの上書き設定 |
| `.github/workflows/blog-social.yml` | 記事公開・素材生成・SNS投稿のワークフロー |
| `tests/social/test_social.py` | 26項目のテスト |

## ZIPが見つからない場合の再生成

まずChatGPTの保存ファイルで `Robu-Posting-App.zip` を検索する。Notionへの添付が完了している場合は、引き継ぎページの添付からも取得できる。

再生成する場合は、GitHubの作業ブランチからソースを取得し、Python 3.12・Pillow・ffmpeg・日本語フォントを用意して次を実行する。詳細は `docs/SNS_AUTOMATION.md` を参照。

```bash
python -m pip install -r scripts/social/requirements.txt
python -m scripts.social build --preview-article vietnam-coffee
```

出力は `_site/social-posting-app.zip`。これは配布名 `Robu-Posting-App.zip` と生成時のファイル名が違うだけ。確認用生成にはSNSの認可情報は不要。

作成済み配布ZIPの大きさは521,295バイト。SHA-256は次のとおり。再生成時は作成日時などが変わるため、ZIP全体のハッシュが一致するとは限らない。

```text
b88752fbf36550f74cb287e052ab95198675fe9476f7372278f634707474895c
```

作成時の一時作業フォルダは `/workspace/scratch/03e119202cfe/robu-travel-journal-live`。一時領域がなくなっていても、GitHubと保存済みZIPから再開できる。ユーザーのPC上の保存先とは別。

## 記録の保存状況

- GitHub：このMarkdownとREADMEの案内をPR #53のブランチに保存。本番mainへのマージとは別。
- Notion：既存の「AI記事制作ワークフロー（公開前）」配下へ本文とアプリZIPを保存済み。
- NotebookLM：Googleへのログインが必要なため、この時点では未保存。ログイン後、このMarkdownをソースに追加する。
- ChatGPT：配布ZIP `Robu-Posting-App.zip` と、引き継ぎMarkdown `Robu-Posting-App-Handoff.md` を保存。

## 他のタスクに渡す文

```text
Robu 投稿アプリの続きです。GitHubのAxis-koji/robu-travel-journal、PR #53、ブランチcodex/blog-social-automationのdocs/SNS_APP_HANDOFF.mdとdocs/SNS_AUTOMATION.mdを先に読んでください。Buffer不要の無料版は実装済みで、確認用ZIPはRobu-Posting-App.zipです。記録時点では本番未適用・SNS未接続・自動投稿未稼働です。現在の状態を確認して、その続きから作業してください。
```
