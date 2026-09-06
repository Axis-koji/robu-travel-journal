"""Direct publishing with a durable write-ahead record; uncertain sends never retry."""
import base64
import hashlib
import json
import os
import urllib.error
import urllib.request
from datetime import datetime, timezone
from .content import caption
from .providers import DeliveryError, Rejected, request


class Ledger:
    branch = "social-state"
    path = ".social/state.json"

    def __init__(self, repo, token, site_url):
        if not repo or not token:
            raise DeliveryError("GITHUB_REPOSITORY/GITHUB_TOKENが未設定です")
        self.repo, self.token, self.site_url = repo, token, site_url
        self.base = "https://api.github.com/repos/" + repo
        self.sha = None
        self.data = None

    def load(self):
        try:
            result = request(self.base + "/contents/" + self.path + "?ref=" + self.branch, self.token)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                raise DeliveryError("投稿記録がありません。先にinitializeを実行してください") from None
            raise DeliveryError(f"投稿記録の読込失敗: HTTP {e.code}") from None
        self.sha = result["sha"]
        self.data = json.loads(base64.b64decode(result["content"]))
        if (self.data.get("version") != 1 or self.data.get("repository") != self.repo
                or self.data.get("site_url") != self.site_url):
            raise DeliveryError("投稿記録のバージョン・リポジトリ・公開URLが一致しません")
        return self.data

    def initialize(self, article_ids, head):
        try:
            request(self.base + "/git/ref/heads/" + self.branch, self.token)
        except urllib.error.HTTPError as e:
            if e.code != 404:
                raise
        else:
            raise DeliveryError("social-stateブランチは既に存在します。初期化を繰り返すことはできません")
        request(self.base + "/git/refs", self.token, {"ref": "refs/heads/" + self.branch, "sha": head})
        self.data = {"version": 1, "repository": self.repo, "site_url": self.site_url,
                     "excluded": sorted(article_ids), "posts": {}}
        self.save()

    def save(self):
        body = {"branch": self.branch, "message": "Record social delivery state [skip ci]",
                "content": base64.b64encode(json.dumps(self.data, ensure_ascii=False, indent=2).encode()).decode()}
        if self.sha:
            body["sha"] = self.sha
        try:
            result = request(self.base + "/contents/" + self.path, self.token, body, "PUT")
        except Exception:
            raise DeliveryError("投稿記録を保存できません。送信を停止しました。GitHub Actionsの権限とsocial-stateを確認してください") from None
        self.sha = result["content"]["sha"]


def configure(ledger, articles, client, exclude_current=False):
    """Activate targets at an explicit boundary; never backfill manual history."""
    targets = client.check()
    data = ledger.load()
    channels = data.setdefault("channels", {})
    for platform, target in targets.items():
        old = channels.get(platform, {})
        if old.get("target") and old["target"] != target["target"]:
            raise DeliveryError(f"{platform}: 既存の投稿先と違います。記録を確認してから接続先を変更してください")
        if not old:
            channels[platform] = {"target": target["target"], "excluded": sorted(a["id"] for a in articles),
                                  "configured_at": datetime.now(timezone.utc).isoformat()}
        elif exclude_current:
            old["excluded"] = sorted(set(old.get("excluded", [])) | {a["id"] for a in articles})
            old["configured_at"] = datetime.now(timezone.utc).isoformat()
    ledger.save()
    print("接続を記録しました。現在ある記事は各接続先への自動投稿から除外しました。")


def verify_public(url):
    req = urllib.request.Request(url, headers={"User-Agent": "robu-social/2"})
    with urllib.request.urlopen(req, timeout=30) as response:
        content_type = response.headers.get("Content-Type", "")
        if response.status != 200:
            raise DeliveryError("公開ページまたは素材が未反映です")
        if url.endswith(".jpg") and not content_type.startswith("image/"):
            raise DeliveryError("画像が公開されていません")
        response.read(1024)


def eligible(data, article, platform):
    return (article["id"] not in data["excluded"]
            and article["id"] not in data.get("channels", {}).get(platform, {}).get("excluded", []))


def publish(plan, config, ledger, client, env=os.environ, verify=verify_public):
    if env.get("SOCIAL_PUBLISH_ENABLED") != "true":
        raise DeliveryError("SOCIAL_PUBLISH_ENABLED=trueが必要です")
    data = ledger.load()
    platforms = list(client.settings)
    if not platforms:
        print("自動投稿先はありません。投稿アプリから無料の手動投稿を利用できます。")
        return
    targets = client.check()
    for platform, target in targets.items():
        if data.get("channels", {}).get(platform, {}).get("target") != target["target"]:
            raise DeliveryError(f"{platform}: 先にconnectで接続を初期化してください。過去記事の一斉投稿を防止します")
    errors = [key + ": 前回の結果が不明です。SNSで確認してresolveしてください"
              for key, record in data["posts"].items()
              if record.get("status") in {"submitting", "uncertain"}]
    pending = lambda a, p: eligible(data, a, p) and data["posts"].get(a["id"] + ":" + p, {}).get("status") not in {
        "published", "accepted", "submitting", "uncertain", "manual_done"}
    candidates = [a for a in plan if any(pending(a, p) for p in platforms)]
    candidates.sort(key=lambda a: (a.get("published", ""), a["id"]))
    for article in candidates[:config["max_articles_per_run"]]:
        for platform in platforms:
            if not pending(article, platform):
                continue
            key = article["id"] + ":" + platform
            try:
                verify(article["url"])
                verify(article["pin_url"] if platform == "pinterest" else article["image_url"])
            except Exception:
                errors.append(key + ": 公開URL／画像の確認に失敗。未送信です")
                continue
            record = {"status": "submitting", "attempted_at": datetime.now(timezone.utc).isoformat(),
                      "payload_hash": hashlib.sha256((caption(article, platform) + article["media_hash"]).encode()).hexdigest()}
            data["posts"][key] = record
            ledger.save()  # Must succeed BEFORE any external write.
            try:
                post_id = client.create(article, platform)
                if not post_id:
                    raise DeliveryError("投稿IDなし")
            except Rejected as e:
                record["status"] = "rejected"
                errors.append(key + ": " + str(e))
            except Exception:
                record["status"] = "uncertain"
                errors.append(key + ": 投稿結果が不明です。自動再送を停止しました")
            else:
                record.update(status="published", post_id=post_id)
                print(key + ": SNSから投稿IDを受信しました")
            ledger.save()
    if len(candidates) > config["max_articles_per_run"]:
        errors.append(f"上限に達しました。残り{len(candidates) - config['max_articles_per_run']}記事はpublishを再実行してください")
    if errors:
        raise DeliveryError("\n".join(errors))


def resolve(ledger, key, outcome, post_id=""):
    data = ledger.load()
    record = data["posts"].get(key)
    if not record or record.get("status") not in {"submitting", "uncertain", "accepted", "published"}:
        raise DeliveryError("解決対象の投稿記録がありません")
    if outcome == "published":
        if not post_id:
            raise DeliveryError("SNSで確認した投稿IDが必要です")
        record.update(status="published", post_id=post_id)
    elif outcome == "retry":
        if record.get("status") in {"published", "accepted"}:
            raise DeliveryError("投稿済み／受付済みの記録は再送できません")
        record["status"] = "rejected"
    else:
        raise DeliveryError("outcomeはpublishedまたはretryです")
    ledger.save()
