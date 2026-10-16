import json
import unittest
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SLUG = "rog-xbox-ally-x20-seven-checks"


class LinkParser(HTMLParser):
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


class RogArticleTests(unittest.TestCase):
    def pages(self):
        return (
            ("ja", ROOT / "articles" / SLUG / "index.html"),
            ("en", ROOT / "en" / "articles" / SLUG / "index.html"),
        )

    def test_bilingual_pages_have_required_shell_and_order(self):
        for lang, path in self.pages():
            html = path.read_text(encoding="utf-8")
            with self.subTest(lang=lang):
                self.assertIn('content="index,follow,max-image-preview:large"', html)
                self.assertIn("shared-shell.js", html)
                self.assertIn("contact-feedback.js", html)
                greeting = "こんにちは、ろぶーです。" if lang == "ja" else "Hi, I&#39;m Roboo."
                self.assertLess(html.index("<h1"), html.index("<figure>"))
                self.assertLess(html.index("<figure>"), html.index(greeting))
                self.assertNotIn("unpublished", html.lower())
                self.assertNotIn("noindex", html.lower())

    def test_images_sources_and_affiliate_cards(self):
        for lang, path in self.pages():
            html = path.read_text(encoding="utf-8")
            parser = LinkParser()
            parser.feed(html)
            affiliate = [link for link in parser.links if "merchant-card" in link.get("class", "")]
            with self.subTest(lang=lang):
                self.assertEqual(len(parser.images), 2)
                self.assertTrue(all(image.get("alt") for image in parser.images))
                self.assertEqual(len(affiliate), 2)
                self.assertTrue(all("sponsored" in link.get("rel", "") for link in affiliate))
                self.assertIn("B0HH8TC4TK", affiliate[1]["href"])
                self.assertIn("y1gjgfCIQEk", affiliate[0]["href"])
                self.assertNotIn("楽天", html)
                self.assertNotIn("Yahoo", html)

    def test_schema_and_index_registration(self):
        for _, path in self.pages():
            html = path.read_text(encoding="utf-8")
            start = html.index('<script type="application/ld+json">') + len('<script type="application/ld+json">')
            end = html.index("</script>", start)
            schema = json.loads(html[start:end])
            self.assertEqual(schema["@type"], "BlogPosting")
            self.assertEqual(len(schema["citation"]), 5)
        index = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn(f"{SLUG}-2026-10-16", index)
        self.assertIn(f"/articles/{SLUG}/", index)


if __name__ == "__main__":
    unittest.main()
