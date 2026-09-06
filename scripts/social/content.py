"""Extract the site's existing HTML metadata without generating new factual claims."""
import re
from datetime import datetime, timedelta, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit

PLATFORMS = ("facebook", "instagram", "twitter", "tiktok", "threads", "pinterest")


class Metadata(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.meta, self.title, self.canonical = {}, "", ""
        self.in_title = False
        self.has_article = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "meta":
            self.meta[a.get("property", a.get("name", "")).lower()] = a.get("content", "")
        if tag == "link" and "canonical" in a.get("rel", "").split():
            self.canonical = a.get("href", "")
        if tag == "title":
            self.in_title = True
        if tag == "article":
            self.has_article = True

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data


def clean(text):
    return re.sub(r"\s+", " ", str(text)).strip()


def local_image(root, page_path, reference, site_url):
    """Only use checked-out, same-site images. Never fetch arbitrary article URLs."""
    if not reference:
        raise ValueError(f"{page_path}: og:image がありません")
    parsed = urlsplit(reference)
    allowed_hosts = {urlsplit(site_url).hostname, "axis-jp.net", "www.axis-jp.net"}
    if parsed.scheme and parsed.scheme != "https":
        raise ValueError("画像URLにはHTTPSを使用してください")
    if parsed.netloc and parsed.hostname not in allowed_hosts:
        raise ValueError("SNS用画像を記事フォルダまたはassetsに保存してください")
    relative = unquote(parsed.path)
    candidate = root / relative.lstrip("/") if relative.startswith("/") else root / page_path.parent / relative
    resolved = candidate.resolve()
    if not resolved.is_relative_to(root.resolve()) or not resolved.is_file():
        raise ValueError(f"ローカル画像が見つかりません: {reference}")
    if resolved.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"}:
        raise ValueError("SNS画像はPNG/JPEG/WebPにしてください")
    return resolved


def catalog(root, config, now=None):
    root = Path(root)
    now = now or datetime.now(timezone.utc)
    site = config["site_url"].rstrip("/")
    if urlsplit(site).scheme != "https" or urlsplit(site).path:
        raise ValueError("site_urlにはパスなしのHTTPS URLを指定してください")
    result = []
    for path in sorted(root.glob("articles/*/index.html")):
        rel = path.relative_to(root)
        slug = path.parent.name
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", slug):
            raise ValueError(f"記事フォルダ名が不正です: {slug}")
        html = path.read_text(encoding="utf-8-sig")
        parser = Metadata()
        parser.feed(html)
        meta = parser.meta
        override = config.get("overrides", {}).get(slug, {})
        if (override.get("publish") is False or meta.get("social:publish", "").lower() == "false"
                or "noindex" in meta.get("robots", "").lower()
                or meta.get("article:status", "").lower() == "draft"
                or not (parser.has_article or meta.get("og:type") == "article")):
            continue
        published = meta.get("article:published_time", "")
        if published:
            when = datetime.fromisoformat(published.replace("Z", "+00:00"))
            if (when if when.tzinfo else when.replace(tzinfo=timezone(timedelta(hours=9)))) > now:
                continue
        title = clean(override.get("title") or meta.get("og:title") or parser.title.split("｜")[0])
        description = clean(override.get("description") or meta.get("og:description") or meta.get("description", ""))
        if not title or not description:
            raise ValueError(f"{rel}: タイトルとdescriptionを設定してください")
        # Always use the verified production host, including for older non-www articles.
        url = f"{site}/articles/{quote(slug)}/"
        ai_image = override.get("ai_image", meta.get("social:ai-image") == "true" or bool(
            re.search(r"生成(?:した|AI|イメージ|画像)|AI[-・ ]?(?:生成|イメージ)", html, re.I)))
        result.append({"id": slug, "path": str(rel), "url": url, "title": title,
                       "description": description, "published": published,
                       "image_ref": override.get("image") or meta.get("og:image", ""),
                       "ai_image": bool(ai_image),
                       "disclosure": clean(override.get("disclosure") or meta.get("social:disclosure", ""))})
    return result


def clip(text, length):
    return text if len(text) <= length else text[:max(0, length - 1)] + "…"


def caption(article, platform):
    notice = article.get("disclosure", "")
    image_notice = "※画像は生成イメージです。" if article.get("ai_image") else ""
    if platform == "twitter":
        # Conservative 2 units per Unicode character; URL costs 23 on X.
        suffix = "\n" + article["url"]
        note = " ".join(x for x in (notice, image_notice) if x)
        remaining = (280 - 23 - 2) // 2 - len(note) - (1 if note else 0)
        if remaining < 12:
            raise ValueError("X用の広告表記が長すぎます")
        return "\n".join(x for x in (note, clip(article["title"], remaining)) if x) + suffix
    if platform in {"instagram", "tiktok"}:
        end = "続きはプロフィールのブログリンクから。\n「" + clip(article["title"], 60) + "」をご覧ください。"
    else:
        end = article["url"]
    limit = {"facebook": 1500, "instagram": 1800, "threads": 450, "pinterest": 450, "tiktok": 1800}[platform]
    fixed = "\n\n".join(x for x in (notice, clip(article["title"], 100), image_notice, end) if x)
    description = clip(article["description"], max(0, limit - len(fixed) - 2))
    return "\n\n".join(x for x in (notice, clip(article["title"], 100), description, image_notice, end) if x)
