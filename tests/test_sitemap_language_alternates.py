from pathlib import Path
import unittest
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
NS = {
    "sm": "http://www.sitemaps.org/schemas/sitemap/0.9",
    "xhtml": "http://www.w3.org/1999/xhtml",
}
SLUGS = (
    "sarashina-service-six-models-beta",
    "rog-xbox-ally-x20-seven-checks",
    "homepod-mini-2-buying-guide",
)


class SitemapLanguageAlternatesTests(unittest.TestCase):
    def test_affected_bilingual_pairs_are_reciprocal(self):
        tree = ET.parse(ROOT / "sitemap.xml")
        by_loc = {
            node.find("sm:loc", NS).text: node
            for node in tree.findall("sm:url", NS)
        }

        for slug in SLUGS:
            ja = f"https://www.axis-jp.net/articles/{slug}/"
            en = f"https://www.axis-jp.net/en/articles/{slug}/"
            expected = {"ja": ja, "en": en, "x-default": ja}

            for page_url in (ja, en):
                self.assertIn(page_url, by_loc)
                alternates = {
                    link.attrib["hreflang"]: link.attrib["href"]
                    for link in by_loc[page_url].findall("xhtml:link", NS)
                }
                self.assertEqual(alternates, expected)


if __name__ == "__main__":
    unittest.main()
