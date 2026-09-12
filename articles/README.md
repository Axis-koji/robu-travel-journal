# 記事フォルダ

## 正式フォーマット（必須）

公開済み記事、未公開ドラフト、今後作成する新規記事は、すべて
[`records/2026/09/2026-09-13-article-shell-formal-standard-v1.md`](../records/2026/09/2026-09-13-article-shell-formal-standard-v1.md)
を正式フォーマットとして使用します。記事ごとに別のヘッダーやフッターを作ってはいけません。

公開用HTMLでは、次の共通部品を必ず読み込みます。

```html
<script src="/assets/js/shared-shell.js"></script>
```

共通部品が記事カテゴリを判定し、次の見た目と操作を自動適用します。

- 「ろぶーの気になる事」: 写真入りタブ、クリーム／サンド系のヘッダーと本文背景
- 「Robu’s Selection」: 写真入りタブ、黒に近い濃紺のヘッダーと本文、アイボリー文字、金系アクセント
- 共通フッター: Facebook、Instagram、X、Reddit、TikTokの5つを、運営者の公開ページへ直接リンク
- 言語ボタン: 日本語、English、简体中文、繁體中文、粵語、Tiếng Việtを表示し、Google翻訳で現在の記事を開く
- 問い合わせ: 従来の共通「問い合わせ・ご感想」フォーム
- 商品購入ボタン: Amazon、楽天、Yahoo!ショッピングを同じ寸法で並べ、通常時は各サービス色、ホバー時はオレンジ

記事画像は実物や公式情報から大きく離れない内容にし、AI生成画像を使う場合はキャプションに「AI生成イメージ」と明記します。自分で撮影した写真にはAI生成表記を付けません。

この正式フォーマットは毎回の個別指示を不要にするための共通ルールです。新規記事の作成・変換・公開処理でも必ず継承し、公開前にChromeで通常記事とSelection記事の表示、画像、リンク、スマートフォン表示を確認します。

記事は1本につき1つのMarkdownファイルで管理します。

- `vietnam-coffee.md` — ベトナムコーヒー
- `vietnam-grab.md` — ベトナムでのGrab利用
- `weekend-drive.md` — 週末ドライブ
- `travel-note.md` — 旅ノート

新しい記事を追加するときは、日付・カテゴリー・表紙用の一言・画像パス・本文を同じ形式で記録します。画像は `../assets/images/` に保存します。

公開用HTMLは、共通の `/assets/js/site.js` または `/assets/js/contact-feedback.js` を読み込み、記事末尾に「問い合わせ・ご感想」フォームが自動表示される状態にします。Pull Requestでは `scripts/check-contact-feedback.ps1` が全記事を確認します。
