import copy
import urllib.error
import zipfile
import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch
from scripts.social.__main__ import wait_for_media
from scripts.social.content import PLATFORMS, caption, catalog, local_image
from scripts.social.publish import DeliveryError, configure, publish, resolve
from scripts.social.providers import Direct, Rejected, automatic_platforms, connection_settings
from scripts.social.studio import export_studio


CONFIG = {"site_url": "https://www.axis-jp.net", "site_name": "ろぶーの気になる事",
          "platforms": list(PLATFORMS), "max_articles_per_run": 3}
ARTICLE = {"id": "new-article", "title": "新しい旅の記事", "description": "旅先で役立つ情報を紹介します。",
           "url": "https://www.axis-jp.net/articles/new-article/", "ai_image": True, "disclosure": "",
           "image_url": "https://www.axis-jp.net/assets/social/new-article/instagram.jpg",
           "pin_url": "https://www.axis-jp.net/assets/social/new-article/pinterest.jpg",
           "video_url": "https://www.axis-jp.net/assets/social/new-article/tiktok.mp4", "media_hash": "abc", "published": "2026-09-06"}
ENV = {"SOCIAL_PUBLISH_ENABLED": "true", "SOCIAL_AUTO_PLATFORMS": "facebook,instagram,threads,pinterest",
       "PINTEREST_STANDARD_ACCESS": "true", "PINTEREST_BOARD_ID": "400", "PINTEREST_ACCESS_TOKEN": "test-pin",
       "FACEBOOK_PAGE_ID": "100", "FACEBOOK_PAGE_ACCESS_TOKEN": "test-fb",
       "INSTAGRAM_USER_ID": "200", "INSTAGRAM_ACCESS_TOKEN": "test-ig",
       "THREADS_USER_ID": "300", "THREADS_ACCESS_TOKEN": "test-th"}

class MemoryLedger:
    def __init__(self, excluded=()):
        self.data = {"excluded": list(excluded), "posts": {}, "channels": {p: {"target": c["target"], "excluded": []} for p, c in connection_settings(ENV).items()}}
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


class FakeDirect:
    def __init__(self, ledger, env=ENV):
        self.sent = []
        self.ledger = ledger
        self.settings = connection_settings(env)
        self.timeout_for = None
        self.reject_for = None

    def check(self):
        return {p: {"target": c["target"]} for p, c in self.settings.items()}

    def create(self, article, platform):
        assert self.ledger.persisted["posts"][article["id"] + ":" + platform]["status"] == "submitting"
        self.sent.append((article["id"], platform))
        if platform == self.timeout_for:
            raise TimeoutError()
        if platform == self.reject_for:
            raise Rejected("invalid")
        return str(len(self.sent))


class DeliveryTests(unittest.TestCase):
    def setUp(self):
        self.ledger = MemoryLedger()
        self.client = FakeDirect(self.ledger)

    def run_publish(self):
        publish([copy.deepcopy(ARTICLE)], CONFIG, self.ledger, self.client, env=ENV, verify=lambda url: None)

    def test_only_four_free_platforms_and_edits_do_not_duplicate(self):
        self.run_publish()
        publish([{**ARTICLE, "title": "変更後"}], CONFIG, self.ledger, self.client, env=ENV, verify=lambda url: None)
        self.assertEqual({p for _, p in self.client.sent}, {"facebook", "instagram", "threads", "pinterest"})
        self.assertEqual(len(self.client.sent), 4)

    def test_existing_articles_are_excluded(self):
        self.ledger.persisted["excluded"] = [ARTICLE["id"]]
        self.run_publish()
        self.assertFalse(self.client.sent)

    def test_unknown_send_is_not_retried_but_others_finish(self):
        self.client.timeout_for = "facebook"
        with self.assertRaises(DeliveryError): self.run_publish()
        self.client.timeout_for = None
        with self.assertRaises(DeliveryError): self.run_publish()
        self.assertEqual(len(self.client.sent), 4)

    def test_failed_write_ahead_prevents_sending(self):
        self.ledger.fail_at = 1
        with self.assertRaises(DeliveryError): self.run_publish()
        self.assertFalse(self.client.sent)

    def test_failed_success_save_cannot_duplicate(self):
        self.ledger.fail_at = 2
        with self.assertRaises(DeliveryError): self.run_publish()
        self.ledger.fail_at = None
        with self.assertRaises(DeliveryError): self.run_publish()
        self.assertEqual(sum(p == "facebook" for _, p in self.client.sent), 1)

    def test_explicit_rejection_retries_only_failed_target(self):
        self.client.reject_for = "pinterest"
        with self.assertRaises(DeliveryError): self.run_publish()
        self.client.reject_for = None
        self.run_publish()
        self.assertEqual(len(self.client.sent), 5)

    def test_disabled_prevents_any_post(self):
        with self.assertRaises(DeliveryError): publish([ARTICLE], CONFIG, self.ledger, self.client, env={})
        self.assertFalse(self.client.sent)

    def test_no_connections_needs_no_credentials(self):
        client = FakeDirect(self.ledger, {})
        publish([ARTICLE], CONFIG, self.ledger, client, env=ENV)
        self.assertFalse(client.sent)

    def test_missing_credentials_or_paid_platform_rejected(self):
        for env in ({"SOCIAL_AUTO_PLATFORMS": "instagram"}, {"SOCIAL_AUTO_PLATFORMS": "twitter"}, {"SOCIAL_AUTO_PLATFORMS": "tiktok"}):
            with self.assertRaises(DeliveryError): Direct(env)

    def test_pinterest_trial_cannot_publish(self):
        with self.assertRaises(DeliveryError): Direct({**ENV, "PINTEREST_STANDARD_ACCESS": "false"})

    def test_one_connected_platform_can_run_independently(self):
        client = FakeDirect(self.ledger, {**ENV, "SOCIAL_AUTO_PLATFORMS": "threads"})
        publish([ARTICLE], CONFIG, self.ledger, client, env=ENV, verify=lambda _: None)
        self.assertEqual(client.sent, [(ARTICLE["id"], "threads")])

    def test_missing_target_initialization_prevents_backfill(self):
        self.ledger.persisted["channels"] = {}
        with self.assertRaises(DeliveryError): self.run_publish()
        self.assertFalse(self.client.sent)
        configure(self.ledger, [ARTICLE], self.client)
        self.run_publish()
        self.assertFalse(self.client.sent)

    def test_adding_target_excludes_manual_history(self):
        del self.ledger.persisted["channels"]["pinterest"]
        configure(self.ledger, [ARTICLE], self.client)
        self.run_publish()
        self.assertEqual(len(self.client.sent), 3)

    def test_explicit_resume_boundary_excludes_manual_posts(self):
        configure(self.ledger, [ARTICLE], self.client, exclude_current=True)
        self.run_publish()
        self.assertFalse(self.client.sent)

    def test_bad_image_does_not_block_other_image_types(self):
        def verify(url):
            if url.endswith("pinterest.jpg"): raise OSError()
        with self.assertRaises(DeliveryError):
            publish([ARTICLE], CONFIG, self.ledger, self.client, env=ENV, verify=verify)
        self.assertEqual(len(self.client.sent), 3)

    def test_uncertain_old_articles_do_not_starve_new_ones(self):
        articles = [{**ARTICLE, "id": "article-" + str(i)} for i in range(4)]
        for article in articles[:3]:
            for p in self.client.settings:
                self.ledger.persisted["posts"][article["id"] + ":" + p] = {"status": "uncertain"}
        with self.assertRaises(DeliveryError):
            publish(articles, CONFIG, self.ledger, self.client, env=ENV, verify=lambda _: None)
        self.assertEqual(len(self.client.sent), 4)

    def test_published_record_cannot_be_reset_to_retry(self):
        self.run_publish()
        with self.assertRaises(DeliveryError): resolve(self.ledger, ARTICLE["id"] + ":facebook", "retry")


class ProviderTests(unittest.TestCase):
    def test_official_payloads_and_container_publish_sequence(self):
        calls = []
        def transport(url, token, data, method, form=False):
            calls.append((url, data, form))
            if "?fields=status_code" in url: return {"status_code": "FINISHED"}
            if "?fields=status" in url: return {"status": "FINISHED"}
            return {"id": "123"}
        client = Direct(ENV, transport=transport, sleep=lambda _: None)
        for platform in client.settings: self.assertEqual(client.create(ARTICLE, platform), "123")
        self.assertEqual(len(calls), 8)
        self.assertTrue(calls[0][0].startswith("https://graph.facebook.com/v26.0/"))
        self.assertEqual(calls[2][0], "https://graph.instagram.com/v26.0/123?fields=status_code")
        self.assertEqual(calls[3][1], {"creation_id": "123"})
        self.assertEqual(calls[6][1], {"creation_id": "123"})
        self.assertEqual(calls[7][1]["media_source"]["source_type"], "image_url")
        self.assertFalse(calls[7][2])
        self.assertTrue(all("test-" not in url for url, _, _ in calls))

    def test_error_bodies_never_leak_tokens(self):
        def transport(*args, **kwargs): return {"error": {"message": "SECRET"}}
        with self.assertRaises(Rejected) as caught: Direct(ENV, transport=transport).create(ARTICLE, "facebook")
        self.assertNotIn("SECRET", str(caught.exception))

    def test_unfinished_container_is_never_published(self):
        calls = []
        def transport(url, *args, **kwargs):
            calls.append(url)
            return {"status_code": "IN_PROGRESS"} if "?fields" in url else {"id": "123"}
        with self.assertRaises(DeliveryError):
            Direct(ENV, transport=transport, sleep=lambda _: None).create(ARTICLE, "instagram")
        self.assertFalse(any("media_publish" in url for url in calls))


class ReleaseTests(unittest.TestCase):
    def test_social_image_is_verified_with_cache_busting_url(self):
        class Headers:
            @staticmethod
            def get_content_type():
                return "image/jpeg"

        class Response:
            headers = Headers()
            def __enter__(self): return self
            def __exit__(self, *args): return False
            @staticmethod
            def read(_): return b"x"

        article = copy.deepcopy(ARTICLE)
        with patch("scripts.social.__main__.urllib.request.urlopen", return_value=Response()) as opened:
            wait_for_media([article], attempts=1, delay=0)
        self.assertEqual(article["image_url"], ARTICLE["image_url"] + "?v=abc")
        self.assertEqual(opened.call_args.args[0].full_url, article["image_url"])


class StudioTests(unittest.TestCase):
    def test_portable_app_keeps_secrets_out_and_escapes_script_data(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "social/studio").mkdir(parents=True)
            (root / "social/studio/index.html").write_text("<!doctype html>")
            out = root / "out"
            media = out / "assets/social/new-article"
            media.mkdir(parents=True)
            for name in ("instagram.jpg", "pinterest.jpg", "tiktok.mp4"): (media / name).write_bytes(b"fixture")
            data = export_studio(root, out, [{**ARTICLE, "title": "</script><script>alert(1)</script>"}], CONFIG,
                                 state={"posts": {}, "token": "SECRET"}, env={**ENV, "FAKE_SECRET": "SECRET"})
            output = (out / "social-studio/data.js").read_text()
            self.assertNotIn("SECRET", output)
            self.assertNotIn("</script>", output)
            self.assertEqual(len(data["articles"][0]["posts"]), 6)
            with zipfile.ZipFile(out / "social-posting-app.zip") as archive:
                self.assertIn("social-studio/index.html", archive.namelist())
                self.assertIn("assets/social/new-article/tiktok.mp4", archive.namelist())


class ContentTests(unittest.TestCase):
    def test_japanese_x_caption_fits_conservative_weight_and_keeps_url(self):
        article = {**ARTICLE, "title": "日本語の長いタイトル" * 70, "disclosure": "広告を含む記事"}
        text = caption(article, "twitter")
        self.assertTrue(text.endswith(article["url"]))
        self.assertLessEqual(len(text.removesuffix(article["url"])) * 2 + 23, 280)

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
