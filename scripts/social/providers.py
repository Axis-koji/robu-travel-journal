"""Official APIs only. No paid endpoints, browser login or stored passwords."""
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from .content import caption, clip


class DeliveryError(RuntimeError):
    pass


class Rejected(DeliveryError):
    """An explicit API rejection, as opposed to an unknown delivery outcome."""


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        # Never forward an access token to a redirect target.
        return None


def request(url, token, data=None, method=None, form=False):
    body = None if data is None else (
        urllib.parse.urlencode(data).encode() if form else json.dumps(data).encode())
    req = urllib.request.Request(url, body, headers={
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded" if form else "application/json",
        "Accept": "application/json", "User-Agent": "robu-social/2"}, method=method)
    with urllib.request.build_opener(NoRedirect).open(req, timeout=45) as response:
        return json.load(response)


SETTINGS = {
    "facebook": ("FACEBOOK_PAGE_ID", "FACEBOOK_PAGE_ACCESS_TOKEN"),
    "instagram": ("INSTAGRAM_USER_ID", "INSTAGRAM_ACCESS_TOKEN"),
    "threads": ("THREADS_USER_ID", "THREADS_ACCESS_TOKEN"),
    "pinterest": ("PINTEREST_BOARD_ID", "PINTEREST_ACCESS_TOKEN"),
}


def automatic_platforms(env=os.environ):
    names = [p.strip() for p in env.get("SOCIAL_AUTO_PLATFORMS", "").split(",") if p.strip()]
    if len(names) != len(set(names)) or set(names) - SETTINGS.keys():
        raise DeliveryError("自動投稿先はfacebook,instagram,threads,pinterestから指定してください。X・TikTokは手動投稿です")
    return names


def connection_settings(env=os.environ):
    settings = {}
    version = env.get("META_GRAPH_VERSION") or "v26.0"
    if not re.fullmatch(r"v\d+\.0", version):
        raise DeliveryError("META_GRAPH_VERSIONが不正です")
    for platform in automatic_platforms(env):
        id_name, token_name = SETTINGS[platform]
        target, token = env.get(id_name, "").strip(), env.get(token_name, "").strip()
        if not re.fullmatch(r"[0-9]+", target) or not token:
            raise DeliveryError(f"{platform}: {id_name}と{token_name}を設定してください")
        if platform == "pinterest" and env.get("PINTEREST_STANDARD_ACCESS") != "true":
            raise DeliveryError("Pinterestの公開投稿にはStandard access承認が必要です。承認後にPINTEREST_STANDARD_ACCESS=trueを設定してください")
        settings[platform] = {"target": target, "token": token, "version": version}
    return settings


class Direct:
    def __init__(self, env=os.environ, transport=request, sleep=time.sleep):
        self.settings = connection_settings(env)
        self.transport, self.sleep = transport, sleep

    def call(self, platform, path, data=None, method=None):
        c = self.settings[platform]
        base = {"facebook": "https://graph.facebook.com/" + c["version"],
                # Instagram publishing authenticated via Facebook Login uses the
                # Facebook Graph host. graph.instagram.com is for Instagram Login.
                "instagram": "https://graph.facebook.com/" + c["version"],
                "threads": "https://graph.threads.net/v1.0",
                "pinterest": "https://api.pinterest.com/v5"}[platform]
        # Meta's Page publishing endpoints accept the Page token as a form
        # parameter. Supplying it there mirrors Graph API Explorer and avoids
        # deployments where the bearer header is accepted for reads but the
        # same token is rejected for Page photo creation.
        if platform == "facebook" and data is not None:
            data = {**data, "access_token": c["token"]}
        try:
            result = self.transport(base + "/" + path, c["token"], data, method, form=platform != "pinterest")
        except urllib.error.HTTPError as e:
            if 400 <= e.code < 500:
                # Meta/Pinterest error messages may contain request details. Expose
                # only numeric classification fields in public Actions logs.
                api_code = api_subcode = None
                try:
                    payload = json.load(e)
                    error = payload.get("error", {}) if isinstance(payload, dict) else {}
                    api_code = error.get("code")
                    api_subcode = error.get("error_subcode")
                except Exception:
                    pass
                details = ""
                if isinstance(api_code, int):
                    details += f" / API {api_code}"
                if isinstance(api_subcode, int):
                    details += f" / subcode {api_subcode}"
                raise Rejected(f"{platform}: APIが拒否しました（HTTP {e.code}{details}）。権限・期限・投稿条件を確認してください") from None
            raise DeliveryError(f"{platform}: API通信の結果が不明です") from None
        if not isinstance(result, dict):
            raise DeliveryError(f"{platform}: API応答が不明です")
        if result.get("error"):
            raise Rejected(f"{platform}: APIが拒否しました。接続権限と素材を確認してください")
        return result

    def check(self):
        """Read-only identity check. Does not prove publishing permission or app review."""
        result = {}
        for platform, c in self.settings.items():
            fields = "id,username" if platform in {"instagram", "threads"} else "id,name"
            path = "boards/" + c["target"] if platform == "pinterest" else c["target"] + "?fields=" + fields
            response = self.call(platform, path)
            if str(response.get("id", "")) != c["target"]:
                raise DeliveryError(f"{platform}: 接続先IDを確認できません")
            result[platform] = {"target": c["target"], "name": response.get("username") or response.get("name", "")}
        return result

    def ready(self, platform, container_id):
        field = "status_code" if platform == "instagram" else "status"
        for attempt in range(5):
            response = self.call(platform, container_id + "?fields=" + field)
            status = response.get(field)
            if status == "FINISHED":
                return
            if status in {"ERROR", "EXPIRED"}:
                raise Rejected(f"{platform}: 素材の処理が失敗しました。未公開です")
            if status != "IN_PROGRESS":
                raise DeliveryError(f"{platform}: 素材の処理結果が不明です")
            if attempt < 4:
                self.sleep(60)
        raise DeliveryError(f"{platform}: 素材の処理待ちです。自動再送を停止しました")

    @staticmethod
    def identifier(result):
        value = result.get("post_id") or result.get("id")
        if not value or not re.fullmatch(r"[0-9_]+", str(value)):
            raise DeliveryError("投稿IDを確認できません。SNSで投稿結果を確認してください")
        return str(value)

    def create(self, article, platform):
        if platform not in self.settings:
            raise DeliveryError("未接続のSNSです")
        target = self.settings[platform]["target"]
        text = caption(article, platform)
        if platform == "facebook":
            return self.identifier(self.call(platform, target + "/photos", {
                "url": article["image_url"], "caption": text, "published": "true"}))
        if platform == "pinterest":
            return self.identifier(self.call(platform, "pins", {
                "board_id": target, "title": clip(article["title"], 100),
                "description": text, "link": article["url"], "alt_text": clip(article["title"], 500),
                "media_source": {"source_type": "image_url", "url": article["pin_url"]}}))
        if platform == "instagram":
            container = self.identifier(self.call(platform, target + "/media", {
                "image_url": article["image_url"], "caption": text}))
            self.ready(platform, container)
            return self.identifier(self.call(platform, target + "/media_publish", {"creation_id": container}))
        container = self.identifier(self.call(platform, target + "/threads", {
            "media_type": "IMAGE", "image_url": article["image_url"], "text": text}))
        self.ready(platform, container)
        return self.identifier(self.call(platform, target + "/threads_publish", {"creation_id": container}))
