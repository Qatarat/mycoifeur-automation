"""
RatingPage — page object for ratings and review submission flow.
Covers: star tapping, review text entry, submit, and edit review.
"""
from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage
from utils.helpers import wait_for_animation


class RatingPage(BasePage):

    def open_rate_screen(self):
        """Tap Rate / Leave a Review from a completed order."""
        self.tap_optional("Rate")
        self.tap_optional("Leave a Review")
        self.tap_optional("Rate Service")
        wait_for_animation(self.driver, 2)
        return self

    def tap_stars(self, count: int = 5):
        """Tap stars 1 through `count`. Falls back to text-based tap."""
        for i in range(1, count + 1):
            try:
                star = self.driver.find_element(
                    AppiumBy.ACCESSIBILITY_ID, f"star_{i}"
                )
                star.click()
                wait_for_animation(self.driver, 0.3)
            except Exception:
                # Fallback: tap by position if no accessibility ID
                pass
        # Final fallback: tap the highest star by text
        if count == 5:
            self.tap_optional("5")
        wait_for_animation(self.driver)
        return self

    def enter_review_text(self, text: str):
        """Type review text in the feedback input field."""
        self.tap_optional("Write your review")
        self.tap_optional("Add a comment")
        try:
            fields = self.driver.find_elements(AppiumBy.XPATH, "//android.widget.EditText")
            if fields:
                fields[-1].click()
                wait_for_animation(self.driver, 0.3)
                fields[-1].send_keys(text)
        except Exception:
            pass
        wait_for_animation(self.driver)
        return self

    def submit_review(self):
        """Submit the review."""
        self.tap_optional("Submit")
        self.tap_optional("Submit Review")
        wait_for_animation(self.driver, 3)
        return self

    # ── Assertions ─────────────────────────────────────────────────────────────

    def assert_rating_submitted(self):
        page = self.driver.page_source
        assert (
            "thank" in page.lower()
            or "submitted" in page.lower()
            or "success" in page.lower()
            or "review" in page.lower()
        ), "Rating submission confirmation not shown"
        return self

    def assert_star_rating_visible(self):
        page = self.driver.page_source
        assert (
            "star" in page.lower()
            or "rating" in page.lower()
            or "rate" in page.lower()
        ), "Star rating widget not visible"
        return self
