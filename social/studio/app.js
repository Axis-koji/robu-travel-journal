"use strict";
(() => {
  const $ = (id) => document.getElementById(id);
  const meta = {
    instagram: {name: "Instagram", url: "https://www.instagram.com/", help: "画像を保存し、紹介文をコピーしてInstagramの「作成」から投稿してください。プロフィールにはブログのリンクを設定してください。", limit: 2200},
    facebook: {name: "Facebook", url: "https://www.facebook.com/", help: "紹介文をコピーして共有画面を開き、投稿先のFacebookページを選んでください。画像付きの投稿にする場合は、保存した画像をページの投稿画面に添付します。", limit: 63206},
    twitter: {name: "X", url: "https://x.com/", help: "紹介文を入れた投稿画面が開きます。保存した画像を添付し、内容を確認して投稿してください。無料版ではXのAPIを使いません。", limit: 280},
    tiktok: {name: "TikTok", url: "https://www.tiktok.com/upload", help: "12秒の動画を保存し、紹介文をコピーしてアップロードしてください。公開範囲・AI生成・広告に関する表示は、TikTokの投稿画面で内容に合わせて設定してください。", limit: 2200},
    threads: {name: "Threads", url: "https://www.threads.net/", help: "紹介文を入れた投稿画面が開きます。画像を保存して添付し、内容を確認して投稿してください。", limit: 500},
    pinterest: {name: "Pinterest", url: "https://www.pinterest.com/", help: "保存先のボードを選び、画像・紹介文・記事リンクを確認してピンを公開してください。APIのStandard承認前も、この方法で投稿できます。", limit: 500}
  };
  const order = Object.keys(meta);
  const manifest = window.ROBU_SOCIAL_MANIFEST;
  if (!manifest || manifest.version !== 2 || !Array.isArray(manifest.articles)) {
    $("notice").textContent = "記事データがまだありません。接続ガイドに沿って投稿素材を作成し、生成されたアプリを開いてください。";
    $("notice").classList.add("warning");
    $("refresh").disabled = true;
    $("guide-link").href = "https://github.com/Axis-koji/robu-travel-journal/blob/codex/blog-social-automation/docs/SNS_AUTOMATION.md";
    return;
  }
  const repo = manifest.repository;
  if (!/^[\w.-]+\/[\w.-]+$/.test(repo)) return;
  const base = "https://github.com/" + repo;
  $("guide-link").href = base + "/blob/" + (manifest.preview ? "codex/blog-social-automation" : "main") + "/docs/SNS_AUTOMATION.md";
  $("workflow-link").href = base + (manifest.preview ? "/actions" : "/actions/workflows/blog-social.yml");
  $("site-name").textContent = manifest.site_name;
  if (location.protocol === "file:") $("app-download").hidden = true;
  const storageKey = "robu-posting-v2:" + repo;
  let saved = {drafts: {}, done: {}};
  let storageAvailable = true;
  try {
    const stored = JSON.parse(localStorage.getItem(storageKey) || "null");
    if (stored && typeof stored.drafts === "object" && stored.drafts && typeof stored.done === "object" && stored.done) saved = stored;
  } catch { storageAvailable = false; }
  let state = manifest.state || {posts: {}, channels: {}};
  let selected = manifest.articles[0] || null;
  let platform = "instagram";
  let timer;
  const codepoints = (text) => [...text].length;
  function toast(message) { $("toast").textContent = message; $("toast").hidden = false; clearTimeout(timer); timer = setTimeout(() => { $("toast").hidden = true; }, 4500); }
  function persist() {
    try { localStorage.setItem(storageKey, JSON.stringify(saved)); }
    catch { storageAvailable = false; toast("端末に保存できませんでした。この画面を閉じる前に紹介文をコピーしてください。"); }
  }
  function key(article = selected, service = platform) { return article.id + ":" + service; }
  function record(article = selected, service = platform) { return state.posts?.[key(article, service)]?.status || ""; }
  function automated(article = selected, service = platform) {
    return !manifest.preview && manifest.enabled && manifest.automatic.includes(service)
      && !!state.channels?.[service] && !state.channels[service].excluded.includes(article.id);
  }
  function locked(article = selected, service = platform) {
    const reserved = !manifest.preview && manifest.automatic.includes(service) && state.channels?.[service]
      && !state.channels[service].excluded.includes(article.id);
    return reserved || ["published", "accepted", "submitting", "uncertain"].includes(record(article, service));
  }
  function displayDate(value) {
    if (!value) return "公開済み";
    const date = new Date(value);
    return Number.isNaN(date.getTime()) ? "公開済み" : new Intl.DateTimeFormat("ja-JP", {timeZone: "Asia/Tokyo", year: "numeric", month: "short", day: "numeric"}).format(date);
  }
  function showConnections() {
    $("connections").replaceChildren();
    for (const p of order) {
      const on = manifest.enabled && !manifest.preview && manifest.automatic.includes(p) && state.channels?.[p];
      const card = document.createElement("div"); card.className = "connection" + (on ? " auto" : "");
      const label = document.createElement("strong"); label.textContent = meta[p].name;
      const mode = document.createElement("span");
      mode.textContent = on ? "新しい記事を自動投稿" : manifest.automatic.includes(p) ? "自動投稿の設定待ち" : "素材を準備・手動投稿";
      card.append(label, mode); $("connections").append(card);
    }
    $("notice").textContent = manifest.preview
      ? "確認用アプリです。SNSへの自動送信は行いません。紹介文と素材を確認でき、手動で投稿する際にも使えます。"
      : manifest.enabled && manifest.automatic.length
        ? "接続したSNSには新しい記事を自動投稿します。それ以外は、素材を保存して各SNSの画面で投稿してください。"
        : "6つのSNS用の紹介文と素材を用意しました。自動投稿はまだ停止中です。接続が済むまで、各SNSの画面から無料で投稿できます。";
    $("updated").textContent = "素材作成：" + displayDate(manifest.generated_at);
  }
  function articleList() {
    const query = $("search").value.trim().toLocaleLowerCase("ja");
    const articles = manifest.articles.filter(a => a.title.toLocaleLowerCase("ja").includes(query));
    $("article-count").textContent = articles.length + "件";
    $("article-list").replaceChildren();
    for (const a of articles) {
      const button = document.createElement("button"); button.type = "button"; button.className = "article-choice";
      button.setAttribute("aria-current", String(selected?.id === a.id));
      const date = document.createElement("small"); date.textContent = displayDate(a.published);
      const title = document.createElement("strong"); title.textContent = a.title;
      const progress = document.createElement("small"); progress.className = "article-progress";
      const count = order.filter(p => record(a, p) === "published" || saved.done[key(a, p)] === true).length;
      progress.textContent = count ? count + " / 6 投稿済み・完了メモ" : "6つのSNS用の素材あり";
      button.append(date, title, progress);
      button.addEventListener("click", () => { selected = a; articleList(); render(); });
      $("article-list").append(button);
    }
    if (!articles.length) { const note = document.createElement("p"); note.textContent = query ? "一致する記事がありません。" : "新しい記事を公開すると、ここに表示されます。"; $("article-list").append(note); }
  }
  function shareURL() {
    const text = $("caption").value;
    if (locked()) return meta[platform].url;
    if (platform === "twitter") return "https://twitter.com/intent/tweet?" + new URLSearchParams({text});
    if (platform === "threads") return "https://www.threads.net/intent/post?" + new URLSearchParams({text});
    if (platform === "facebook") return "https://www.facebook.com/sharer/sharer.php?" + new URLSearchParams({u: selected.url});
    if (platform === "pinterest") return manifest.preview ? "https://www.pinterest.com/pin-creation-tool/" : "https://www.pinterest.com/pin/create/button/?" + new URLSearchParams({url: selected.url, media: manifest.site_url + "/assets/social/" + selected.id + "/pinterest.jpg", description: text});
    return meta[platform].url;
  }
  function captionChanged() {
    const text = $("caption").value;
    const count = platform === "twitter" ? text.split(/(https?:\/\/\S+)/g).reduce((n, s) => n + (/^https?:\/\//.test(s) ? 23 : 2 * codepoints(s)), 0) : codepoints(text);
    const over = count > meta[platform].limit;
    $("char-count").textContent = (platform === "twitter" ? "目安 " : "") + count + " / " + meta[platform].limit + "字";
    $("caption").setAttribute("aria-invalid", String(over));
    $("open-platform").setAttribute("aria-disabled", String(over && !locked()));
    if (over && !locked()) { $("open-platform").removeAttribute("href"); $("caption-note").textContent = "文字数の上限を超えています。紹介文を短くしてください。"; }
    else { $("open-platform").href = shareURL(); $("caption-note").textContent = locked() ? "自動投稿には記事から作成した文章を使います。変更する場合はブログ側の紹介文を修正してください。" : storageAvailable ? "編集内容はこの端末だけに保存されます。自動投稿の文章は変更しません。" : "この環境では編集内容を保存できません。紹介文をコピーして保管してください。"; }
  }
  function render() {
    if (!selected) return;
    $("empty").hidden = true; $("article-content").hidden = false;
    $("article-title").textContent = selected.title; $("article-date").textContent = displayDate(selected.published);
    $("article-link").href = selected.url;
    $("tabs").replaceChildren();
    for (const p of order) {
      const tab = document.createElement("button"); tab.type = "button"; tab.textContent = meta[p].name; tab.id = "tab-" + p;
      tab.setAttribute("role", "tab"); tab.setAttribute("aria-selected", String(p === platform)); tab.setAttribute("aria-controls", "post-panel"); tab.tabIndex = p === platform ? 0 : -1;
      tab.addEventListener("click", () => { platform = p; render(); $("tab-" + p).focus(); });
      tab.addEventListener("keydown", e => { if (!["ArrowLeft", "ArrowRight", "Home", "End"].includes(e.key)) return; e.preventDefault(); const index = order.indexOf(p); platform = e.key === "Home" ? order[0] : e.key === "End" ? order.at(-1) : order[(index + (e.key === "ArrowRight" ? 1 : -1) + order.length) % order.length]; render(); $("tab-" + platform).focus(); });
      $("tabs").append(tab);
    }
    $("post-panel").setAttribute("aria-labelledby", "tab-" + platform);
    const video = platform === "tiktok";
    $("preview-image").hidden = video; $("preview-video").hidden = !video;
    $("preview-video").pause();
    const source = video ? selected.video : platform === "pinterest" ? selected.pin : selected.image;
    if (video) $("preview-video").src = source;
    else { $("preview-image").src = source; $("preview-image").alt = selected.title + "のSNS投稿用画像"; }
    $("download").href = source; $("download").download = selected.id + "-" + platform + (video ? ".mp4" : ".jpg");
    $("download").textContent = video ? "動画を保存" : "画像を保存";
    $("media-note").textContent = (video ? "縦型・12秒・音声なしのスライド動画。" : platform === "pinterest" ? "縦型画像 1000 × 1500。" : "縦型画像 1080 × 1350。") + (selected.ai_image ? "生成画像の表記を含みます。" : "記事に使用した画像から作成しています。");
    const readonly = locked();
    $("caption").value = !readonly && typeof saved.drafts[key()] === "string" ? saved.drafts[key()] : selected.posts[platform];
    $("caption").readOnly = readonly; $("reset").hidden = readonly;
    const status = record();
    $("delivery-status").className = "status-label" + (["uncertain", "submitting", "rejected"].includes(status) ? " problem" : status === "published" ? " success" : "");
    $("delivery-status").textContent = {published: "投稿済み：SNSから投稿IDを受信", accepted: "旧方式で受付済み：SNSで確認", uncertain: "結果の確認が必要：自動再送は停止", submitting: "処理中または結果未確認", rejected: "自動投稿でエラー"}[status] || (automated() ? "自動投稿の対象" : readonly ? "自動投稿は一時停止中" : saved.done[key()] ? "手動投稿の完了メモあり" : "手動で投稿");
    $("platform-help").textContent = readonly ? (["uncertain", "submitting"].includes(status) ? "重複投稿を防ぐため再送を止めています。SNSで結果を確認し、接続ガイドの復旧手順に沿って対応してください。" : status === "rejected" ? "接続期限・投稿権限・画像の条件を確認してください。実行履歴から原因を確認できます。" : "記事を公開した後、接続先へ自動投稿します。処理の進み具合は実行履歴、実際の表示はSNSで確認してください。") : meta[platform].help;
    $("open-platform").textContent = readonly ? "SNSで確認する ↗" : "投稿画面を開く ↗";
    $("manual-done").checked = saved.done[key()] === true; $("manual-done").disabled = readonly;
    $("manual-done").closest("label").hidden = readonly; $("done-note").hidden = readonly;
    captionChanged();
  }
  $("search").addEventListener("input", articleList);
  $("caption").addEventListener("input", () => { if (!selected || locked()) return; saved.drafts[key()] = $("caption").value; persist(); captionChanged(); });
  $("reset").addEventListener("click", () => { if (!selected) return; delete saved.drafts[key()]; persist(); render(); });
  $("copy").addEventListener("click", async () => { try { await navigator.clipboard.writeText($("caption").value); toast("紹介文をコピーしました"); } catch { $("caption").focus(); $("caption").select(); let copied = false; try { copied = document.execCommand("copy"); } catch {} toast(copied ? "紹介文をコピーしました" : "文章を選択しました。Ctrl+Cでコピーしてください。"); } });
  $("manual-done").addEventListener("change", () => { if (!selected || locked()) return; saved.done[key()] = $("manual-done").checked; persist(); articleList(); render(); });
  $("refresh").addEventListener("click", async () => {
    if (manifest.preview) { toast("確認用アプリです。自動投稿は行っていません。"); return; }
    $("refresh").disabled = true;
    try {
      const response = await fetch("https://raw.githubusercontent.com/" + repo + "/social-state/.social/state.json", {cache: "no-store", credentials: "omit", signal: AbortSignal.timeout(15000)});
      if (!response.ok) throw new Error("unavailable");
      const next = await response.json();
      if (next.version !== 1 || next.repository !== repo || next.site_url !== manifest.site_url || !next.posts) throw new Error("invalid");
      state = {posts: next.posts, channels: next.channels || {}};
      showConnections(); articleList(); render(); toast("投稿状況を更新しました。新しい記事はアプリを開き直すと読み込まれます。");
    } catch { toast("投稿記録を読み込めませんでした。自動投稿の実行履歴を確認してください。"); }
    finally { $("refresh").disabled = false; }
  });
  showConnections(); articleList(); render();
})();
