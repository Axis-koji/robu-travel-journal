import copy
import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch
from scripts.social.content import PLATFORMS, caption, catalog, local_image, payload
from scripts.social.publish import DeliveryError, publish


CONFIG = {"site_url": "https://www.axis-jp.net", "site_name": "ろぶーの気になる事",
          "platforms": list(PLATFORMS), "max_articles_per_run": 3}
ARTICLE = {"id": "new-article", "title": "新しい旅の記事", "description": "旅先で役立つ情報を紹介します。",
           "url": "https://www.axis-jp.net/articles/new-article/", "ai_image": True, "disclosure": "",
           "image_url": "https://www.axis-jp.net/assets/social/new-article/instagram.jpg",
           "pin_url": "https://www.axis-jp.net/assets/social/new-article/pinterest.jpg",
           "video_url": "https://www.axis-jp.net/assets/social/new-article/tiktok.mp4"}
ENV = {"SOCIAL_PUBLISH_ENABLED": "true", "PINTEREST_BOARD_ID": "board",
       **{"BUFFER_CHANNEL_" + p.upper(): "channel-" + p for p in PLATFORMS}}


class MemoryLedger:
    def __init__(self, excluded=()):
        self.data = {"excluded": list(excluded), "posts": {}}
        self.persisted = copy.deepcopy(self.data)
        self.saves = 0
        self.fail_at = None

    def load(self):
        self.data = copy.deepcopy(self.persisted)
        return self.data

    def save(self):
        self.saves += 1
        if self.saves == self.fail_at:
            raise DeliveryError("write failed")
        self.persisted = copy.deepcopy(self.data)


class FakeBuffer:
    def __init__(self, ledger):
        self.sent = []
        self.ledger = ledger
        self.timeout_for = None
        self.reject_for = None

    def channels(self):
        return [{"id": "channel-" + p, "service": p, "isDisconnected": False, "isLocked": False,
                 "metadata": {"boards": [{"serviceId": "board"}]}} for p in PLATFORMS]

    def create(self, post):
        platform = post["channelId"].removeprefix("channel-")
        # The write-ahead record must exist remotely before an external send.
        assert self.ledger.persisted["posts"][ARTICLE["id"] + ":" + platform]["status"] == "submitting"
        self.sent.append(post)
        if platform == self.timeout_for:
            raise TimeoutError()
        if platform == self.reject_for:
            return {"data": {"createPost": {"__typename": "ValidationError", "message": "invalid"}}}
        return {"data": {"createPost": {"__typename": "PostActionSuccess", "post": {"id": str(len(self.sent))}}}}


class DeliveryTests(unittest.TestCase):
    def setUp(self):
        self.ledger = MemoryLedger()
        self.client = FakeBuffer(self.ledger)

    def run_publish(self, **kwargs):
        publish([copy.deepcopy(ARTICLE)], CONFIG, self.ledger, self.client, env=ENV, verify=lambda url: None, **kwargs)

    def test_six_platforms_and_rerun_or_edit_does_not_duplicate(self):
        self.run_publish()
        modified = {**ARTICLE, "title": "修正後のタイトル"}
        publish([modified], CONFIG, self.ledger, self.client, env=ENV, verify=lambda url: None)
        self.assertEqual(len(self.client.sent), 6)

    def test_existing_articles_are_excluded(self):
        self.ledger = MemoryLedger([ARTICLE["id"]])
        self.run_publish()
        self.assertEqual(self.client.sent, [])

    def test_ambiguous_delivery_is_not_retried_but_other_channels_finish(self):
        self.client.timeout_for = "facebook"
        with self.assertRaises(DeliveryError):
            self.run_publish()
        self.assertEqual(len(self.client.sent), 6)
        self.client.timeout_for = None
        with self.assertRaises(DeliveryError):
            self.run_publish()
        self.assertEqual(len(self.client.sent), 6)

    def test_failed_write_ahead_prevents_sending(self):
        self.ledger.fail_at = 1
        with self.assertRaises(DeliveryError):
            self.run_publish()
        self.assertFalse(self.client.sent)

    def test_failed_success_record_preserves_pending_on_next_run(self):
        self.ledger.fail_at = 2
        with self.assertRaises(DeliveryError):
            self.run_publish()
        self.ledger.fail_at = None
        with self.assertRaises(DeliveryError):
            self.run_publish()
        self.assertEqual(sum(p["channelId"] == "channel-facebook" for p in self.client.sent), 1)

    def test_explicit_rejection_can_retry_without_resending_successes(self):
        self.client.reject_for = "pinterest"
        with self.assertRaises(DeliveryError):
            self.run_publish()
        self.client.reject_for = None
        self.run_publish()
        self.assertEqual(len(self.client.sent), 7)

    def test_missing_channel_prevents_any_post(self):
        with self.assertRaises(DeliveryError):
            publish([ARTICLE], CONFIG, self.ledger, self.client, env={"SOCIAL_PUBLISH_ENABLED": "true"})
        self.assertFalse(self.client.sent)

    def test_disabled_prevents_any_post(self):
        with self.assertRaises(DeliveryError):
            publish([ARTICLE], CONFIG, self.ledger, self.client, env={})
        self.assertFalse(self.client.sent)

    def test_unpublished_assets_prevent_any_post(self):
        def fail(url):
            raise OSError()
        with self.assertRaises(DeliveryError):
            publish([ARTICLE], CONFIG, self.ledger, self.client, env=ENV, verify=fail)
        self.assertFalse(self.client.sent)


class ContentTests(unittest.TestCase):
    def test_japanese_x_caption_fits_conservative_weight_and_keeps_url(self):
        article = {**ARTICLE, "title": "日本語の長いタイトル" * 70, "disclosure": "広告を含む記事"}
        text = caption(article, "twitter")
        self.assertTrue(text.endswith(article["url"]))
        self.assertLessEqual(len(text.removesuffix(article["url"])) * 2 + 23, 280)

    def test_payloads_have_media_and_platform_metadata(self):
        for platform in PLATFORMS:
            post = payload(ARTICLE, platform, "id", "board")
            self.assertEqual(post["schedulingType"], "automatic")
            self.assertFalse(post["needsApproval"])
            self.assertTrue(post["assets"])
        self.assertIn("video", payload(ARTICLE, "tiktok", "id")["assets"][0])
        self.assertEqual(payload(ARTICLE, "pinterest", "id", "board")["metadata"]["pinterest"]["url"], ARTICLE["url"])
        self.assertTrue(payload(ARTICLE, "instagram", "id")["metadata"]["instagram"]["isAiGenerated"])

    def test_pinterest_requires_board(self):
        with self.assertRaises(ValueError):
            payload(ARTICLE, "pinterest", "id")

    def test_social_caption_limits(self):
        article = {**ARTICLE, "title": "長い" * 100, "description": "説明です。" * 500}
        for platform, limit in (("threads", 500), ("pinterest", 500), ("instagram", 2200), ("tiktok", 2200)):
            self.assertLessEqual(len(caption(article, platform)), limit)

    def test_catalog_skips_drafts_noindex_and_future_dates(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for slug, extra in (("visible", ""), ("draft", '<meta name="social:publish" content="false">'),
                                ("noindex", '<meta name="robots" content="noindex,follow">'),
                                ("future", '<meta property="article:published_time" content="2099-01-01">')):
                file = root / "articles" / slug / "index.html"
                file.parent.mkdir(parents=True)
                file.write_text('<title>記事｜ブログ</title><meta name="description" content="紹介">' + extra + "<article>本文</article>")
            entries = catalog(root, CONFIG)
            self.assertEqual([a["id"] for a in entries], ["visible"])
            self.assertEqual(entries[0]["url"], "https://www.axis-jp.net/articles/visible/")

    def test_og_article_without_article_element_is_supported(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            file = root / "articles" / "watch" / "index.html"
            file.parent.mkdir(parents=True)
            file.write_text('<title>時計</title><meta name="description" content="紹介">'
                            '<meta property="og:type" content="article"><main>本文</main>')
            self.assertEqual(catalog(root, CONFIG)[0]["id"], "watch")

    def test_path_traversal_and_external_images_are_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for reference in ("https://other.example/photo.jpg", "../../../../outside.jpg", "file:///etc/passwd"):
                with self.assertRaises(ValueError):
                    local_image(root, Path("articles/example/index.html"), reference, CONFIG["site_url"])


if __name__ == "__main__":
    unittest.main()
