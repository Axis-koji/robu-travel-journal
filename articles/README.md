# 記事フォルダ

記事は1本につき1つのMarkdownファイルで管理します。

- `vietnam-coffee.md` — ベトナムコーヒー
- `vietnam-grab.md` — ベトナムでのGrab利用
- `weekend-drive.md` — 週末ドライブ
- `travel-note.md` — 旅ノート

新しい記事を追加するときは、日付・カテゴリー・表紙用の一言・画像パス・本文を同じ形式で記録します。画像は `../assets/images/` に保存します。

公開用HTMLは、共通の `/assets/js/site.js` または `/assets/js/contact-feedback.js` を読み込み、記事末尾に「問い合わせ・ご感想」フォームが自動表示される状態にします。Pull Requestでは `scripts/check-contact-feedback.ps1` が全記事を確認します。
