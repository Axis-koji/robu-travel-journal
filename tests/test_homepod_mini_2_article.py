import json
import unittest
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SLUG = "homepod-mini-2-buying-guide"


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.images = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "a":
            self.links.append(values)
        if tag == "img":
            self.images.append(values)


class HomePodMini2ArticleTests(unittest.TestCase):
    def pages(self):
        return (
            ("ja", ROOT / "articles" / SLUG / "index.html"),
            ("en", ROOT / "en" / "articles" / SLUG / "index.html"),
        )

    def test_bilingual_pages_use_normal_article_shell(self):
        for lang, path in self.pages():
            text = path.read_text(encoding="utf-8")
            with self.subTest(lang=lang):
                self.assertIn('content="index,follow,max-image-preview:large"', text)
                self.assertIn("shared-shell.js", text)
                self.assertIn("contact-feedback.js", text)
                self.assertIn("ろぶーの気になる事 / オーディオ", text)
                self.assertNotIn("Robu's Selection", text)
                self.assertNotIn("Robu’s Selection", text)
                self.assertNotIn("unpublished", text.lower())
                self.assertNotIn("noindex", text.lower())
                greeting = "こんにちは、ろぶーです。" if lang == "ja" else "Hi, I&#39;m Roboo."
                self.assertLess(text.index("<h1"), text.index("<figure>"))
                self.assertLess(text.index("<figure>"), text.index(greeting))
                self.assertIn("ろぶーの結論" if lang == "ja" else "Robu’s Take", text)

    def test_images_and_apple_purchase_destination(self):
        for lang, path in self.pages():
            text = path.read_text(encoding="utf-8")
            parser = PageParser()
            parser.feed(text)
            with self.subTest(lang=lang):
                self.assertEqual(2, len(parser.images))
                self.assertTrue(all(image.get("alt") for image in parser.images))
                self.assertIn("AI-generated editorial images are used", text)
                self.assertIn("https://www.apple.com/jp/shop/buy-homepod/homepod-mini/", text)
                self.assertNotIn("nofollow sponsored", text)
                self.assertIn("homepod-mini-2-four-speaker-surround-v3.png", text)

    def test_claims_and_sources_are_present(self):
        ja = (ROOT / "articles" / SLUG / "index.html").read_text(encoding="utf-8")
        en = (ROOT / "en" / "articles" / SLUG / "index.html").read_text(encoding="utf-8")
        self.assertIn("前後のペアごとに同じモデル", ja)
        self.assertIn("HomePod mini 2だけで構成するなら4台", ja)
        self.assertIn("99,200円", ja)
        self.assertIn("matching models within the front and rear pairs", en)
        for url in (
            "https://www.apple.com/jp/newsroom/2026/10/apple-announces-the-next-generation-of-homepod-mini/",
            "https://www.apple.com/jp/shop/buy-homepod/homepod-mini/",
            "https://www.apple.com/jp/home/",
            "https://www.apple.com/jp/homepod-mini/specs/",
        ):
            self.assertIn(url, ja)
            self.assertIn(url, en)

    def test_catalogue_and_sitemaps(self):
        article_id = f"{SLUG}-2026-10-19"
        index = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn(article_id, index)
        self.assertIn(f"'{article_id}': []", index)
        self.assertIn(f'"url": "/articles/{SLUG}/"', index)
        xml = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        self.assertIn(f"https://www.axis-jp.net/articles/{SLUG}/", xml)
        self.assertIn(f"https://www.axis-jp.net/en/articles/{SLUG}/", xml)
        html_sitemap = (ROOT / "sitemap" / "index.html").read_text(encoding="utf-8")
        self.assertIn(f"/articles/{SLUG}/", html_sitemap)
        self.assertIn(f"/en/articles/{SLUG}/", html_sitemap)

    def test_json_ld_and_local_assets(self):
        for lang, path in self.pages():
            text = path.read_text(encoding="utf-8")
            start = text.index('<script type="application/ld+json">') + len('<script type="application/ld+json">')
            end = text.index("</script>", start)
            schema = json.loads(text[start:end])
            with self.subTest(lang=lang):
                self.assertEqual("BlogPosting", schema["@type"])
                self.assertEqual("2026-10-19", schema["datePublished"])
                self.assertEqual(4, len(schema["citation"]))
        image_dir = ROOT / "assets" / "images" / "articles" / SLUG
        self.assertTrue((image_dir / "homepod-mini-2-editorial-hero-v2.png").is_file())
        self.assertTrue((image_dir / "homepod-mini-2-four-speaker-surround-v3.png").is_file())


if __name__ == "__main__":
    unittest.main()
