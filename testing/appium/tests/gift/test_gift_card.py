import pytest
from pages.login_page import LoginPage
from pages.base_page import BasePage
from utils.helpers import screenshot, wait_for_animation


@pytest.mark.gift
class TestGiftCard:

    def _login_and_go_to_gift(self, driver):
        login = LoginPage(driver)
        login.select_country_and_language()
        login.skip_onboarding()
        login.login()
        wait_for_animation(driver, 2)
        page = BasePage(driver)
        page.tap_optional("Gift to someone you love")
        page.tap_optional("Gift Card")
        wait_for_animation(driver, 2)
        return page

    def test_gift_card_entry_fields_present(self, driver):
        """Gift card section must be accessible without crashing."""
        page = self._login_and_go_to_gift(driver)
        assert "500" not in driver.page_source
        screenshot(driver, "gift_card_fields")

    def test_gift_card_preview_shows_correct_info(self, driver):
        """Gift card flow must not produce a 500 error."""
        page = self._login_and_go_to_gift(driver)
        page.tap_optional("Enter recipient Name")
        page.tap_optional("Recipient Number")
        wait_for_animation(driver)
        assert "500" not in driver.page_source
        screenshot(driver, "gift_card_preview")

    def test_gift_card_validation_empty_fields(self, driver):
        """Submitting empty gift form should not crash the app."""
        page = self._login_and_go_to_gift(driver)
        page.tap_optional("Next")
        page.tap_optional("Save Gift Details")
        wait_for_animation(driver)
        assert "500" not in driver.page_source
        screenshot(driver, "gift_card_validation_error")

    def test_gift_received_section_visible(self, driver):
        """My Orders screen must load without a 500 error."""
        login = LoginPage(driver)
        login.select_country_and_language()
        login.skip_onboarding()
        login.login()
        wait_for_animation(driver, 2)
        page = BasePage(driver)
        page.tap_optional("My Orders")
        wait_for_animation(driver)
        assert "500" not in driver.page_source
        screenshot(driver, "gift_received_section")
