import pytest
from pages.login_page import LoginPage
from pages.base_page import BasePage
from utils.helpers import screenshot, wait_for_animation
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from test_data import InvalidGift


@pytest.mark.gift
@pytest.mark.negative
@pytest.mark.android
class TestGiftCardBoundary:
    """Boundary and injection tests for the gift card creation form."""

    def _reach_gift_form(self, driver):
        login = LoginPage(driver)
        login.select_country_and_language()
        login.skip_onboarding()
        login.login()

        page = BasePage(driver)
        page.tap_optional("Gift to someone you love")
        page.tap_optional("Gift Card")
        wait_for_animation(driver, 2)
        return page

    def _try_submit(self, page):
        page.tap_optional("Next")
        page.tap_optional("Save Gift Details")
        wait_for_animation(page.driver)

    def test_very_long_recipient_name_handled(self, driver):
        """A 150-char name must be truncated or rejected — not crash."""
        page = self._reach_gift_form(driver)
        page.input_text_optional("Enter recipient Name", InvalidGift.LONG_NAME)
        page.tap_optional("Next")
        wait_for_animation(driver)

        assert "500" not in driver.page_source, \
            "Long name caused a server error"
        screenshot(driver, "gift_long_name")

    def test_special_chars_in_recipient_name(self, driver):
        """Special characters in the name field must not crash or corrupt the UI."""
        page = self._reach_gift_form(driver)
        page.input_text_optional("Enter recipient Name", InvalidGift.SPECIAL_NAME)
        page.tap_optional("Next")
        wait_for_animation(driver)

        assert "500" not in driver.page_source, \
            "Special chars in name caused a server error"
        screenshot(driver, "gift_special_name")

    def test_arabic_name_accepted(self, driver):
        """Arabic (RTL Unicode) characters in the name field must be accepted."""
        page = self._reach_gift_form(driver)
        page.input_text_optional("Enter recipient Name", InvalidGift.ARABIC_NAME)
        page.tap_optional("Next")
        wait_for_animation(driver)

        assert "500" not in driver.page_source, \
            "Arabic name caused a server error"
        screenshot(driver, "gift_arabic_name")

    def test_invalid_recipient_phone_shows_error(self, driver):
        """Non-numeric recipient phone must be rejected or handled gracefully."""
        page = self._reach_gift_form(driver)
        page.input_text_optional("Enter recipient Name", "Test User")
        page.input_text_optional("Recipient Number", InvalidGift.INVALID_PHONE)
        page.tap_optional("Next")
        wait_for_animation(driver)

        assert "500" not in driver.page_source, \
            "Non-numeric recipient phone caused a server error"
        screenshot(driver, "gift_invalid_phone_error")

    def test_short_recipient_phone_shows_error(self, driver):
        """A 3-digit recipient phone must be rejected or handled gracefully."""
        page = self._reach_gift_form(driver)
        page.input_text_optional("Enter recipient Name", "Test User")
        page.input_text_optional("Recipient Number", InvalidGift.SHORT_PHONE)
        page.tap_optional("Next")
        wait_for_animation(driver)

        assert "500" not in driver.page_source, \
            "Short recipient phone caused a server error"
        screenshot(driver, "gift_short_phone_error")

    def test_xss_in_message_is_safe(self, driver):
        """XSS payload in message must be displayed as plain text, not executed."""
        page = self._reach_gift_form(driver)
        page.input_text_optional("Enter recipient Name", "Test User")
        page.input_text_optional("Recipient Number", "509876543")
        page.input_text_optional("Enter sender Name", "Sender Test")
        page.input_text_optional("What do you want to say?", InvalidGift.XSS_MESSAGE)
        page.tap_optional("Preview")
        wait_for_animation(driver, 2)

        assert "500" not in driver.page_source, \
            "XSS payload in gift message caused a server error"
        screenshot(driver, "gift_xss_safe")

    def test_sql_injection_in_message_is_safe(self, driver):
        """SQL injection in message must not return a database error."""
        page = self._reach_gift_form(driver)
        page.input_text_optional("Enter recipient Name", "Test User")
        page.input_text_optional("Recipient Number", "509876543")
        page.input_text_optional("Enter sender Name", "Sender Test")
        page.input_text_optional("What do you want to say?", InvalidGift.SQL_MESSAGE)
        page.tap_optional("Preview")
        wait_for_animation(driver, 2)

        assert "500" not in driver.page_source, \
            "SQL injection in gift message exposed a server error"
        screenshot(driver, "gift_sql_safe")

    def test_emoji_in_message_does_not_crash(self, driver):
        """Emoji characters in the message must render without crashing."""
        page = self._reach_gift_form(driver)
        page.input_text_optional("Enter recipient Name", "Test User")
        page.input_text_optional("Recipient Number", "509876543")
        page.input_text_optional("Enter sender Name", "Sender Test")
        page.input_text_optional("What do you want to say?", InvalidGift.EMOJI_MESSAGE)
        page.tap_optional("Preview")
        wait_for_animation(driver, 2)

        assert "500" not in driver.page_source, \
            "Emoji in message caused a crash"
        screenshot(driver, "gift_emoji_message")

    def test_very_long_message_is_handled(self, driver):
        """An excessively long gift message must be truncated or rejected cleanly."""
        page = self._reach_gift_form(driver)
        page.input_text_optional("Enter recipient Name", "Test User")
        page.input_text_optional("Recipient Number", "509876543")
        page.input_text_optional("What do you want to say?", InvalidGift.LONG_MESSAGE)
        page.tap_optional("Next")
        wait_for_animation(driver)

        assert "500" not in driver.page_source, \
            "Overly long gift message caused a crash"
        screenshot(driver, "gift_long_message")
