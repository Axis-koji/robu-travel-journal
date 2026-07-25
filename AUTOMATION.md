# ブログ更新の半自動運用

## 基本方針

記事作成、写真配置、表示検査までは自動化します。実際の公開はKojiがGitHubのPull Requestを確認し、`main`へマージしたときだけ行います。

## 更新手順

1. Kojiがテーマ、写真、希望内容をCodexへ渡す。
2. CodexがClaude向けの文章作成プロンプトと、Gemini向けの調査プロンプトを用意する。
3. Claudeは文章案、Geminiは調査結果を作成する。
4. Codexが内容を照合し、記事と写真配置を完成させる。
5. `draft/記事名` ブランチへ保存し、Pull Requestを作る。
6. GitHub Actionsが文字化け、内部用表示、画像不足などを検査する。
7. Kojiが公開前ページと確認項目を見る。
8. KojiがPull RequestをマージするとGitHub Pagesへ公開される。

## APIについて

通常はログイン済みブラウザでClaudeとGeminiを利用します。有料APIキーは自動使用しません。APIが必要な場合は、利用前にKojiの許可を得ます。

## フォルダ

- `articles/`: 記事本文
- `assets/images/`: 記事写真・表紙・カテゴリー画像
- `templates/`: 新規記事のひな型
- `scripts/`: 公開前の自動検査
- `.github/workflows/`: GitHub上で動く自動処理

