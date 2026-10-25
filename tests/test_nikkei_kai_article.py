import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SLUG = "nikkei-kai-pr-media-analysis-agent"


class NikkeiKaiArticleTests(unittest.TestCase):
    def pages(self):
        return (
            ("ja", ROOT / "articles" / SLUG / "index.html"),
            ("en", ROOT / "en" / "articles" / SLUG / "index.html"),
        )

    def test_bilingual_pages_are_publishable_and_use_shared_shell(self):
        for lang, path in self.pages():
            text = path.read_text(encoding="utf-8")
            with self.subTest(lang=lang):
                self.assertIn('content="index,follow,max-image-preview:large"', text)
                self.assertIn("shared-shell.js", text)
                self.assertIn("robus-selection-page", text)
                self.assertIn("contact-feedback.js", text)
                self.assertIn("contact-feedback-ees-standard.css", text)
                self.assertNotIn("noindex", text.lower())
                self.assertNotIn("unpublished", text.lower())

    def test_content_images_purchase_order_and_disclosure(self):
        for lang, path in self.pages():
            text = path.read_text(encoding="utf-8")
            note = text.index('class="purchase-note"')
            disclosure = text.index('data-purchase-disclosure')
            buttons = text.index('class="purchase-buttons"')
            with self.subTest(lang=lang):
                self.assertLess(buttons, note)
                self.assertLess(note, disclosure)
                article_images = text.count('<img src="/assets/images/articles/' + SLUG + '/')
                self.assertEqual(2, article_images)
                self.assertIn("nofollow sponsored noopener noreferrer", text)
                self.assertNotIn("メールアプリで送信内容を確認する", text)

    def test_catalogue_sitemaps_and_schema(self):
        index = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn(f"{SLUG}-2026-10-25", index)
        self.assertIn(f"'{SLUG}-2026-10-25': ['selection']", index)
        xml = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        self.assertIn(f"https://www.axis-jp.net/articles/{SLUG}/", xml)
        self.assertIn(f"https://www.axis-jp.net/en/articles/{SLUG}/", xml)
        html_sitemap = (ROOT / "sitemap" / "index.html").read_text(encoding="utf-8")
        self.assertIn(f"/articles/{SLUG}/", html_sitemap)
        for _, path in self.pages():
            text = path.read_text(encoding="utf-8")
            start = text.index('<script type="application/ld+json">') + len('<script type="application/ld+json">')
            end = text.index("</script>", start)
            schema = json.loads(text[start:end])
            self.assertEqual("Article", schema["@type"])
            self.assertEqual("2026-10-25", schema["datePublished"])


if __name__ == "__main__":
    unittest.main()
