"""
HomePage — page object for the main home feed screen.
Covers: carousel interaction, featured provider cards, category chips,
        pull-to-refresh, and navigation to sub-sections.
"""
from pages.base_page import BasePage
from utils.helpers import wait_for_animation, scroll_to_text


class HomePage(BasePage):

    # ── Navigation ─────────────────────────────────────────────────────────────

    def go_to_home(self):
        """Tap the Home tab in the bottom navigation bar."""
        self.tap_optional("Home")
        wait_for_animation(self.driver)
        return self

    # ── Assertions ─────────────────────────────────────────────────────────────

    def assert_home_loaded(self):
        """Verify the home feed is visible after login."""
        assert (
            self.is_visible("Home", timeout=10)
            or self.is_visible("Browse", timeout=5)
            or self.is_visible("Featured", timeout=5)
            or self.is_visible("Welcome", timeout=5)
        ), "Home screen did not load after login"
        return self

    def assert_no_crash(self):
        page = self.driver.page_source
        assert "Something went wrong" not in page, "Crash banner visible on home feed"
        assert "500" not in page, "500 error visible on home feed"
        return self

    # ── Interactions ────────────────────────────────────────────────────────────

    def scroll_feed_down(self, times=2):
        from appium.webdriver.common.appiumby import AppiumBy
        size = self.driver.get_window_size()
        start_x = size["width"] // 2
        start_y = int(size["height"] * 0.75)
        end_y = int(size["height"] * 0.25)
        for _ in range(times):
            try:
                self.driver.execute_script(
                    "mobile: swipeGesture",
                    {"startX": start_x, "startY": start_y,
                     "endX": start_x, "endY": end_y, "speed": 800},
                )
            except Exception:
                self.driver.swipe(start_x, start_y, start_x, end_y, 800)
            wait_for_animation(self.driver, 1)
        return self

    def tap_first_book_now(self):
        """Tap the first visible 'Book Now' button on the home feed."""
        self.tap_optional("Book Now")
        wait_for_animation(self.driver, 2)
        return self

    def tap_category_chip(self, category: str):
        """Tap a category chip (e.g. 'Haircut', 'Massage')."""
        self.tap_optional(category)
        wait_for_animation(self.driver)
        return self

    def is_banner_visible(self):
        """Check if a promotional banner / carousel is present."""
        page = self.driver.page_source
        return (
            "banner" in page.lower()
            or "offer" in page.lower()
            or "promo" in page.lower()
        )
