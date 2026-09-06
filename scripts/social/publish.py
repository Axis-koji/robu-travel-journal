"""Buffer API client and GitHub-backed write-ahead delivery ledger.

Ambiguous responses are never automatically retried, including a runner dying
after Buffer accepts a request but before the result can be recorded.
"""
import base64
import hashlib
import json
import os
import urllib.error
import urllib.request
from datetime import datetime, timezone
from .content import payload


class DeliveryError(RuntimeError):
    pass


def request(url, token, data=None, method=None):
    body = None if data is None else json.dumps(data).encode()
    req = urllib.request.Request(url, body, headers={
        "Authorization": "Bearer " + token, "Content-Type": "application/json",
        "Accept": "application/json", "User-Agent": "robu-social/1"}, method=method)
    with urllib.request.urlopen(req, timeout=45) as response:
        return json.load(response)


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


class Buffer:
    def __init__(self, token):
        if not token:
            raise DeliveryError("BUFFER_API_KEYが未設定です")
        self.token = token

    def graphql(self, query, variables=None):
        return request("https://api.buffer.com", self.token, {"query": query, "variables": variables or {}})

    def channels(self):
        result = self.graphql("query { account { organizations { id name } } }")
        if result.get("errors") or not result.get("data", {}).get("account"):
            raise DeliveryError("Bufferアカウントの取得に失敗しました")
        channels = []
        for org in result["data"]["account"]["organizations"]:
            result = self.graphql("query($org: OrganizationId!) { channels(input: {organizationId: $org}) { id name service isDisconnected isLocked isQueuePaused metadata { ... on PinterestMetadata { boards { serviceId } } } } }", {"org": org["id"]})
            if result.get("errors") or "channels" not in result.get("data", {}):
                raise DeliveryError("Bufferチャンネルの取得に失敗しました")
            channels.extend(result["data"]["channels"])
        return channels

    def create(self, post):
        return self.graphql("mutation($input: CreatePostInput!) { createPost(input: $input) { __typename ... on PostActionSuccess { post { id } } ... on MutationError { message } } }", {"input": post})


def connections(config, client, env=os.environ):
    configured = {p: env.get("BUFFER_CHANNEL_" + p.upper(), "") for p in config["platforms"]}
    if any(not v for v in configured.values()) or not env.get("PINTEREST_BOARD_ID"):
        raise DeliveryError("6つのBUFFER_CHANNEL_*とPINTEREST_BOARD_IDを設定してください")
    if len(set(configured.values())) != len(configured):
        raise DeliveryError("同じBufferチャンネルIDが重複しています")
    available = {c["id"]: c for c in client.channels()}
    for platform, channel_id in configured.items():
        c = available.get(channel_id)
        if not c or c["service"] != platform or c["isDisconnected"] or c["isLocked"]:
            raise DeliveryError(f"{platform}: 接続・契約プラン・チャンネルIDを確認してください")
        if platform == "pinterest":
            boards = [b["serviceId"] for b in (c.get("metadata") or {}).get("boards", [])]
            if env["PINTEREST_BOARD_ID"] not in boards:
                raise DeliveryError("PinterestのボードIDが接続先に存在しません")
    return configured


def verify_public(url):
    req = urllib.request.Request(url, headers={"User-Agent": "robu-social/1"})
    with urllib.request.urlopen(req, timeout=30) as response:
        content_type = response.headers.get("Content-Type", "")
        if response.status != 200:
            raise DeliveryError("公開ページまたは素材が未反映です")
        if url.endswith(".mp4") and not content_type.startswith("video/"):
            raise DeliveryError("動画が公開されていません")
        if url.endswith(".jpg") and not content_type.startswith("image/"):
            raise DeliveryError("画像が公開されていません")
        response.read(1024)


def publish(plan, config, ledger, client, env=os.environ, verify=verify_public):
    if env.get("SOCIAL_PUBLISH_ENABLED") != "true":
        raise DeliveryError("SOCIAL_PUBLISH_ENABLED=trueが必要です")
    data = ledger.load()
    channel_ids = connections(config, client, env)
    errors = [key + ": 前回の結果が不明です。Bufferで確認してresolveしてください"
              for key, record in data["posts"].items()
              if record.get("status") in {"submitting", "uncertain"}]
    candidates = [a for a in plan if a["id"] not in data["excluded"]
                  and any(data["posts"].get(a["id"] + ":" + p, {}).get("status")
                          not in {"accepted", "submitting", "uncertain"} for p in config["platforms"])]
    for article in candidates[:config["max_articles_per_run"]]:
        try:
            for key in ("url", "image_url", "pin_url", "video_url"):
                verify(article[key])
        except Exception:
            errors.append(article["id"] + ": 公開URL／素材の確認に失敗。未送信です")
            continue
        for platform in config["platforms"]:
            key = article["id"] + ":" + platform
            previous = data["posts"].get(key, {})
            if previous.get("status") == "accepted":
                continue
            if previous.get("status") in {"submitting", "uncertain"}:
                errors.append(key + ": 前回の結果が不明です。Bufferで確認してresolveしてください")
                continue
            post = payload(article, platform, channel_ids[platform], env.get("PINTEREST_BOARD_ID", ""))
            record = {"status": "submitting", "attempted_at": datetime.now(timezone.utc).isoformat(),
                      "payload_hash": hashlib.sha256(json.dumps(post, sort_keys=True).encode()).hexdigest()}
            data["posts"][key] = record
            ledger.save()
            try:
                response = client.create(post)
            except Exception:
                record["status"] = "uncertain"
                errors.append(key + ": 通信結果が不明です。自動再送を停止しました")
            else:
                action = (response.get("data") or {}).get("createPost") or {}
                if not response.get("errors") and action.get("__typename") == "PostActionSuccess" and (action.get("post") or {}).get("id"):
                    record.update(status="accepted", buffer_post_id=action["post"]["id"])
                    print(key + ": Buffer受付済み（各SNSへの配信結果はBufferで確認）")
                elif not response.get("errors") and action.get("__typename") != "PostActionSuccess" and action.get("message"):
                    record["status"] = "rejected"
                    errors.append(key + ": Bufferが拒否しました。投稿条件と契約プランを確認してください")
                else:
                    record["status"] = "uncertain"
                    errors.append(key + ": API応答が不明です。自動再送を停止しました")
            ledger.save()
    if errors:
        raise DeliveryError("\n".join(errors))
    remaining = len(candidates) - config["max_articles_per_run"]
    if remaining > 0:
        raise DeliveryError(f"一度に送る上限に達しました。残り{remaining}記事はpublishを再実行してください")


def resolve(ledger, key, outcome, post_id=""):
    data = ledger.load()
    record = data["posts"].get(key)
    if not record or record.get("status") not in {"submitting", "uncertain", "accepted"}:
        raise DeliveryError("解決対象の投稿記録がありません")
    if outcome == "accepted":
        if not post_id:
            raise DeliveryError("Bufferで確認した投稿IDが必要です")
        record.update(status="accepted", buffer_post_id=post_id)
    elif outcome == "retry":
        record["status"] = "rejected"
    else:
        raise DeliveryError("outcomeはacceptedまたはretryです")
    ledger.save()
