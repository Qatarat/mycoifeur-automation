"""
SalonPage — page object for the salon/provider profile screen.
Covers: salon name, rating, services list, gallery, reviews tab,
        back navigation, and Book Now entry point.
"""
from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage
from utils.helpers import wait_for_animation


class SalonPage(BasePage):

    # ── Locators ───────────────────────────────────────────────────────────────

    SALON_NAME_XPATH = (
        '//*[@content-desc="salon_name" or @resource-id="salon_name" '
        'or contains(@content-desc,"salon") or contains(@content-desc,"Salon")]'
    )
    RATING_XPATH = (
        '//*[@content-desc="salon_rating" or contains(@content-desc,"rating") '
        'or contains(@content-desc,"stars") or contains(@text,"★")]'
    )
    SERVICES_LIST_XPATH = '//*[@content-desc="services_list" or @resource-id="services_list"]'
    GALLERY_XPATH = '//*[@content-desc="gallery" or contains(@content-desc,"gallery")]'
    REVIEWS_TAB_LABELS = ["Reviews", "Review", "Ratings & Reviews"]
    BOOK_NOW_LABELS = ["Book Now", "Book", "Reserve"]
    BACK_LABELS = ["Back", "Navigate up"]

    # ── Navigation ─────────────────────────────────────────────────────────────

    def open_salon(self, index: int = 0):
        """Tap the salon card at *index* from the home/browse listing."""
        cards = self.driver.find_elements(
            AppiumBy.XPATH,
            '//*[@content-desc="salon_card" or @content-desc="provider_card"]'
        )
        if cards and index < len(cards):
            cards[index].click()
        else:
            # Fallback: tap the first tappable image/card visible
            self.tap_optional("Book Now")
        wait_for_animation(self.driver, 2)
        return self

    def tap_back(self):
        """Navigate back from the salon profile."""
        for label in self.BACK_LABELS:
            if self.is_visible(label, timeout=2):
                self.tap_optional(label)
                break
        else:
            self.driver.back()
        wait_for_animation(self.driver)
        return self

    def tap_reviews_tab(self):
        """Tap the Reviews tab on the salon profile."""
        for label in self.REVIEWS_TAB_LABELS:
            if self.is_visible(label, timeout=2):
                self.tap_optional(label)
                wait_for_animation(self.driver, 2)
                return self
        return self

    def tap_book_now(self):
        """Tap the primary Book Now / Book / Reserve button."""
        for label in self.BOOK_NOW_LABELS:
            if self.is_visible(label, timeout=2):
                self.tap_optional(label)
                wait_for_animation(self.driver, 2)
                return self
        return self

    # ── Data retrieval ─────────────────────────────────────────────────────────

    def get_salon_name(self) -> str:
        """Return the text of the salon name element, or empty string."""
        try:
            el = self.driver.find_element(AppiumBy.XPATH, self.SALON_NAME_XPATH)
            return el.get_attribute("text") or el.get_attribute("content-desc") or ""
        except Exception:
            return ""

    def get_rating(self) -> str:
        """Return the rating text/content-desc, or empty string."""
        try:
            el = self.driver.find_element(AppiumBy.XPATH, self.RATING_XPATH)
            return el.get_attribute("text") or el.get_attribute("content-desc") or ""
        except Exception:
            return ""

    # ── Interactions ────────────────────────────────────────────────────────────

    def scroll_gallery(self, direction: str = "left"):
        """Swipe the gallery strip horizontally."""
        size = self.driver.get_window_size()
        w, h = size["width"], size["height"]
        mid_y = h // 2
        if direction == "left":
            start_x, end_x = int(w * 0.8), int(w * 0.2)
        else:
            start_x, end_x = int(w * 0.2), int(w * 0.8)
        try:
            self.driver.execute_script(
                "mobile: swipeGesture",
                {"startX": start_x, "startY": mid_y,
                 "endX": end_x, "endY": mid_y, "speed": 600},
            )
        except Exception:
            self.driver.swipe(start_x, mid_y, end_x, mid_y, 600)
        wait_for_animation(self.driver)
        return self

    # ── Assertions ─────────────────────────────────────────────────────────────

    def assert_salon_profile_loaded(self):
        page = self.driver.page_source
        assert "Something went wrong" not in page, "Salon profile crashed"
        assert "500" not in page, "500 error on salon profile"
        return self

    def assert_services_visible(self):
        page = self.driver.page_source
        assert (
            "service" in page.lower()
            or "Service" in page
            or self.is_visible("Services", timeout=5)
        ), "Services list not visible on salon profile"
        return self
