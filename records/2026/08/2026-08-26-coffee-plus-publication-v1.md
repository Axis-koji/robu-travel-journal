# 2026-08-26 「コーヒー プラス」記事公開記録 v1

## オーナー承認

- 2026-08-26、オーナーがコーヒー記事のGitHub公開を明示承認。
- 承認済みのタイトル・本文と画像／動画の掲載順を維持する。
- Pull Requestまでは作成するが、確認前にマージしない。
- WordPressおよびConoHaには触れない。

## 公開対象

- 記事: `https://www.axis-jp.net/articles/news-coffee-plus-20260826/`
- アイキャッチ: `/assets/images/news-coffee-plus-eyecatch-user.jpg`
- 記事内動画: `/assets/videos/news-coffee-plus-inline-user.mp4`
- トップページ新着欄、HTMLサイトマップ、XMLサイトマップ

## 出典と事実確認

- ネスレネスプレッソ株式会社の会社発表（PR TIMES、2026-08-04）: `https://prtimes.jp/main/html/rd/p/000000144.000010896.html`
- ネスレ日本 公式プレスリリース一覧: `https://www.nestle.co.jp/media/pressreleases`
- ネスプレッソ公式サイト: `https://www.nespresso.com/jp/ja/`
- 確認日: 2026-08-26（JST）

公式発表と照合した項目は、発売日2026年8月26日、ヴァーチュオ専用、数量限定、販売チャネル、ストーミオ ゴー（10カプセル・税込1,620円・約230ml・カフェイン約200mg）、ヴィヴィダ（10カプセル・税込1,620円・約230ml・ビタミンB12約0.80µg）、ジンセン ディライト（10カプセル・税込1,566円・約80ml）。健康効果は断定せず、カフェイン摂取と在庫・適合機種について承認済みの注意書きを維持した。

## 素材と権利表示

- 掲載画像と動画はオーナー提供の承認済み記事用素材を無改変で配置した。
- 公式商品写真・公式商品映像として扱わず、画像キャプションに「実際の商品写真ではありません」、動画キャプションに「実際の商品映像ではありません」と明記した。
- 第三者の商品画像は追加していない。
- 元素材のSHA-256:
  - JPG: `B6E4D2E4A2222DD7D85797A6908E5B0B34AF23B8014507E29EAA5DF71EB06943`
  - MP4: `3FAAB2BAD419AF591E3773F56824130445C0FB9D0717481A8C7F12CD667AF674`

## 実装と検証

- 通常の明るい写真中心の記事デザインを使用し、Robu's Selectionの黒背景テーマは使用しない。
- 現行の共通ヘッダー／フッター `shared-shell.js?v=20260816-5` を読み込む。
- EES記事と同じ標準問い合わせフォーム `contact-feedback.js` を読み込む。
- canonical、OGP、Twitter Card、Article JSON-LD、`index,follow` を設定する。
- 記事から既存のベトナムコーヒー記事とグルメ一覧へ内部リンクする。

## 復旧

公開前の基点は `axis/main` の `77daf7c3916e87accd84abf561cd2ca3c5284ca9`。変更はPull Request単位で保持し、必要な場合は公開コミットをrevertして直前版へ戻す。
