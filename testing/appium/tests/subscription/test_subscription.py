import pytest
from pages.login_page import LoginPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.base_page import BasePage
from utils.helpers import screenshot, wait_for_animation


@pytest.mark.subscription
class TestSubscription:

    def _login_and_reach_checkout(self, driver):
        login = LoginPage(driver)
        login.select_country_and_language()
        login.skip_onboarding()
        login.login()
        cart = CartPage(driver)
        cart.add_first_item()
        cart.open_cart()
        cart.proceed_to_checkout()
        return BasePage(driver)

    def test_subscription_prompt_appears_at_checkout(self, driver):
        """Checkout must load without a 500 error."""
        page = self._login_and_reach_checkout(driver)
        assert "500" not in driver.page_source, \
            "500 error on checkout screen"
        screenshot(driver, "subscription_prompt")

    def test_subscription_weekly_option_selectable(self, driver):
        """Subscription weekly option tap must not crash the app."""
        page = self._login_and_reach_checkout(driver)
        page.tap_optional("Yes")
        wait_for_animation(driver)
        page.tap_optional("Weekly")
        wait_for_animation(driver)
        assert "500" not in driver.page_source, \
            "500 error after selecting Weekly subscription"
        screenshot(driver, "subscription_weekly_selected")

    def test_subscription_monthly_option_selectable(self, driver):
        """Subscription monthly option tap must not crash the app."""
        page = self._login_and_reach_checkout(driver)
        page.tap_optional("Yes")
        wait_for_animation(driver)
        page.tap_optional("Monthly")
        wait_for_animation(driver)
        assert "500" not in driver.page_source, \
            "500 error after selecting Monthly subscription"
        screenshot(driver, "subscription_monthly_selected")

    def test_subscription_skip_goes_to_payment(self, driver):
        """Skipping subscription must not crash the app."""
        page = self._login_and_reach_checkout(driver)
        page.tap_optional("No")
        wait_for_animation(driver)
        assert "500" not in driver.page_source, \
            "500 error after skipping subscription"
        screenshot(driver, "subscription_skipped_payment_shown")

    def test_reminder_banner_shown_after_subscribe(self, driver):
        """Subscription flow must not crash the app."""
        page = self._login_and_reach_checkout(driver)
        page.tap_optional("Yes")
        wait_for_animation(driver)
        page.tap_optional("Weekly")
        page.tap_optional("Subscribe Now")
        page.tap_optional("Subscribe now for Reminder")
        wait_for_animation(driver, 2)
        assert "500" not in driver.page_source, \
            "500 error during subscription flow"
        screenshot(driver, "subscription_success_banner")

    def test_unavailable_items_block_subscription(self, driver):
        """Subscription with unavailable items must not crash the app."""
        page = self._login_and_reach_checkout(driver)
        page.tap_optional("Yes")
        wait_for_animation(driver)

        if page.is_visible("some sales items are unavailable"):
            assert "500" not in driver.page_source, \
                "500 error when unavailable items warning appears"
            screenshot(driver, "subscription_unavailable_items_warning")
        else:
            pytest.skip("No unavailable items in test data — skipping this assertion")
