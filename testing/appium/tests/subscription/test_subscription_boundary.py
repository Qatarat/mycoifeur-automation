import pytest
from pages.login_page import LoginPage
from pages.cart_page import CartPage
from pages.base_page import BasePage
from utils.helpers import screenshot, wait_for_animation


@pytest.mark.subscription
@pytest.mark.negative
@pytest.mark.android
class TestSubscriptionBoundary:
    """Edge-case and boundary tests for subscription flows."""

    def _login_and_reach_subscription_prompt(self, driver):
        login = LoginPage(driver)
        login.select_country_and_language()
        login.skip_onboarding()
        login.login()
        cart = CartPage(driver)
        cart.add_first_item()
        cart.open_cart()
        cart.proceed_to_checkout()
        return BasePage(driver)

    def test_skipping_subscription_reaches_payment(self, driver):
        """Tapping 'No' at subscription prompt must not crash the app."""
        base = self._login_and_reach_subscription_prompt(driver)
        base.tap_optional("No")
        wait_for_animation(driver, 2)
        assert "500" not in driver.page_source, \
            "500 error after declining subscription"
        screenshot(driver, "subscription_skip_to_payment")

    def test_weekly_then_back_resets_selection(self, driver):
        """Selecting Weekly then pressing back must not crash the app."""
        base = self._login_and_reach_subscription_prompt(driver)
        base.tap_optional("Yes")
        wait_for_animation(driver)
        base.tap_optional("Weekly")
        wait_for_animation(driver)
        base.tap_optional("Back")
        wait_for_animation(driver)
        assert "500" not in driver.page_source, \
            "500 error after navigating back from Weekly subscription"
        screenshot(driver, "subscription_back_resets")

    def test_subscription_prompt_has_both_options(self, driver):
        """Subscription prompt must not cause a 500 error."""
        base = self._login_and_reach_subscription_prompt(driver)
        assert "500" not in driver.page_source, \
            "500 error on subscription prompt screen"
        screenshot(driver, "subscription_prompt_options")

    def test_subscription_frequency_options_shown(self, driver):
        """Tapping 'Yes' on subscription prompt must not crash the app."""
        base = self._login_and_reach_subscription_prompt(driver)
        base.tap_optional("Yes")
        wait_for_animation(driver)
        assert "500" not in driver.page_source, \
            "500 error after selecting subscription"
        screenshot(driver, "subscription_frequency_options")

    def test_cancel_active_subscription_declined(self, driver):
        """Cancel subscription 'No' must not crash the app."""
        login = LoginPage(driver)
        login.select_country_and_language()
        login.skip_onboarding()
        login.login()

        base = BasePage(driver)
        base.tap_optional("Active Subscription")
        base.tap_optional("Subscriptions")
        wait_for_animation(driver)
        screenshot(driver, "subscription_active_list")

        base.tap_optional("Cancel Subscription")
        wait_for_animation(driver)
        base.tap_optional("No")
        wait_for_animation(driver)
        assert "500" not in driver.page_source, \
            "500 error when declining subscription cancel"
        screenshot(driver, "subscription_cancel_declined")

    def test_billing_history_accessible(self, driver):
        """Billing history page must load without a 500 error."""
        login = LoginPage(driver)
        login.select_country_and_language()
        login.skip_onboarding()
        login.login()

        base = BasePage(driver)
        base.tap_optional("Active Subscription")
        base.tap_optional("Subscriptions")
        wait_for_animation(driver)
        base.tap_optional("Billing History")
        wait_for_animation(driver)
        assert "500" not in driver.page_source, \
            "500 error on Billing History page"
        screenshot(driver, "subscription_billing_history")
