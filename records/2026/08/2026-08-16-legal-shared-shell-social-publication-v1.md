# 2026-08-16 法務ページ・共通ヘッダー／フッター公開記録 v1

## オーナー指示

- GitHub経由で公開する。
- ConoHa WINGには同じ版の控えを残す。
- ConoHa WINGのWordPress本体、フォルダー、テーマ、プラグイン、データベースには触れない。
- ヘッダーとフッターを公開ページで共通化する。
- フッターのFacebook、Instagram、Xをクリック可能なブランド色のボタンにする。

## 対象

- 利用規約 `/terms/`
- 広告・免責事項 `/advertising-disclaimer/`
- プライバシーポリシー `/privacy-policy/`
- 問い合わせ見出しの中央配置
- 旅行ノート記事画像の表示修正
- 公開HTML 22ページの共通ヘッダー／フッター読込み
- 共通部品 `assets/js/shared-shell.js` と `assets/css/shared-shell.css`

## SNSリンク

オーナー個人または当サイト専用のSNSプロフィールURLは公開リポジトリ内で確認できなかった。架空のプロフィールへ接続しないため、初版では各サービスの公式トップページへ接続する。

- Facebook: `https://www.facebook.com/`
- Instagram: `https://www.instagram.com/`
- X: `https://x.com/`

専用アカウントURLが確定した場合は、別の変更としてリンク先だけを差し替える。

## 検証

- 22ページがローカルHTTPで200を返し、共通部品を1回だけ読み込むことを確認。
- 規約、旅行記事、黒背景の時計記事、404、トップページで共通フッターを確認。
- 記事ページで共通ヘッダー、スマートフォン用メニュー、SNSリンクを確認。
- 問い合わせフォームの既存検査は16記事で合格。
- ブラウザの警告・エラーログは0件。
- WordPressへの変更は行っていない。

## 公開と保管

- GitHub公開先: `Axis-koji/robu-travel-journal`
- GitHub Pages正式URL: `https://www.axis-jp.net/`
- ConoHa WING: WordPress外の非公開保管先が確認できた場合のみ同一版を保存する。ログインまたは安全な絶対パスを確認できない場合は `ConoHa同期待ち` とする。

## 復旧

公開前の基点は `axis/main` の `fb9ee0a`。変更はPull Request単位で保持し、必要な場合は公開コミットをrevertして直前版へ戻す。
