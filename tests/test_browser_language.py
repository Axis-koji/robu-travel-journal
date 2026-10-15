import unittest

from playwright.sync_api import sync_playwright


BASE = "http://127.0.0.1:18777"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"


class BrowserLanguageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(
            executable_path=CHROME,
            headless=True,
        )

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()

    def context(self, locale):
        return self.browser.new_context(locale=locale)

    def test_home_uses_english_browser_language_on_first_visit(self):
        context = self.context("en-US")
        page = context.new_page()
        page.set_default_timeout(10_000)
        page.goto(BASE + "/", wait_until="domcontentloaded")
        self.assertEqual(page.locator("html").get_attribute("lang"), "en")
        href = page.locator('a[href*="sarashina-service-six-models-beta"]').first.get_attribute("href")
        self.assertEqual(href, "/en/articles/sarashina-service-six-models-beta/")
        context.close()

    def test_home_uses_japanese_browser_language_on_first_visit(self):
        context = self.context("ja-JP")
        page = context.new_page()
        page.set_default_timeout(10_000)
        page.goto(BASE + "/", wait_until="domcontentloaded")
        self.assertEqual(page.locator("html").get_attribute("lang"), "ja")
        href = page.locator('a[href*="sarashina-service-six-models-beta"]').first.get_attribute("href")
        self.assertEqual(href, "/articles/sarashina-service-six-models-beta/")
        context.close()

    def test_english_browser_redirects_default_article_to_authored_english(self):
        context = self.context("en-US")
        page = context.new_page()
        page.set_default_timeout(10_000)
        page.goto(
            BASE + "/articles/sarashina-service-six-models-beta/",
            wait_until="domcontentloaded",
        )
        self.assertEqual(page.url, BASE + "/en/articles/sarashina-service-six-models-beta/")
        self.assertEqual(page.locator("html").get_attribute("lang"), "en")
        context.close()

    def test_manual_japanese_choice_overrides_english_browser(self):
        context = self.context("en-US")
        page = context.new_page()
        page.set_default_timeout(10_000)
        page.goto(BASE + "/", wait_until="domcontentloaded")
        page.locator(".language-trigger").click()
        page.locator('[data-lang="ja"]').click()
        page.goto(
            BASE + "/articles/sarashina-service-six-models-beta/",
            wait_until="domcontentloaded",
        )
        self.assertEqual(page.url, BASE + "/articles/sarashina-service-six-models-beta/")
        self.assertEqual(page.locator("html").get_attribute("lang"), "ja")
        context.close()

    def test_article_shell_images_and_mobile_width(self):
        context = self.browser.new_context(locale="ja-JP", viewport={"width": 390, "height": 844})
        page = context.new_page()
        page.set_default_timeout(10_000)
        page.goto(
            BASE + "/articles/sarashina-service-six-models-beta/",
            wait_until="domcontentloaded",
        )
        self.assertEqual(page.locator("[data-robu-common-header]").count(), 1)
        self.assertEqual(page.locator("[data-robu-common-footer]").count(), 1)
        self.assertEqual(page.locator(".article-content figure").count(), 2)
        self.assertLessEqual(
            page.evaluate("document.documentElement.scrollWidth"),
            page.evaluate("document.documentElement.clientWidth"),
        )
        english_href = page.locator('[data-robu-translation-language="en"]').get_attribute("href")
        self.assertEqual(english_href, "/en/articles/sarashina-service-six-models-beta/")
        context.close()


if __name__ == "__main__":
    unittest.main()
