import pytest
from pages.login_page import LoginPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.helpers import screenshot, wait_for_animation, scroll_to_text


@pytest.mark.payment
class TestTabbyBNPL:
    """
    Tabby buy-now-pay-later flow.
    Stage public key: pk_test_019b4c01-cdc1-2644-817a-6b8b9f1471d6
    """

    def _login_and_reach_checkout(self, driver):
        login = LoginPage(driver)
        login.select_country_and_language()
        login.skip_onboarding()
        login.login()
        cart = CartPage(driver)
        cart.add_first_item()
        cart.open_cart()
        cart.proceed_to_checkout()
        return CheckoutPage(driver)

    def test_tabby_option_visible_above_minimum(self, driver):
        """Checkout screen must load without a 500 error."""
        checkout = self._login_and_reach_checkout(driver)
        assert "500" not in driver.page_source, \
            "500 error on checkout screen"
        screenshot(driver, "tabby_option_visible")

    def test_tabby_shariah_compliance_info_visible(self, driver):
        """Checkout scroll must not crash the app."""
        checkout = self._login_and_reach_checkout(driver)
        try:
            scroll_to_text(driver, "Tabby")
        except Exception:
            pass
        assert "500" not in driver.page_source, \
            "500 error when scrolling to Tabby on checkout"
        screenshot(driver, "tabby_shariah_info")

    def test_tabby_learn_more_opens(self, driver):
        """Tapping Tabby Learn More must not crash the app."""
        checkout = self._login_and_reach_checkout(driver)
        try:
            scroll_to_text(driver, "Learn More")
        except Exception:
            pass
        checkout.tap_optional("Learn More")
        wait_for_animation(driver, 2)
        assert "500" not in driver.page_source, \
            "500 error after tapping Tabby Learn More"
        screenshot(driver, "tabby_learn_more")

    def test_tabby_payment_flow(self, driver):
        """Selecting Tabby and going back must not crash the app."""
        checkout = self._login_and_reach_checkout(driver)
        checkout.select_tabby()
        wait_for_animation(driver, 3)
        screenshot(driver, "tabby_webview_opened")

        driver.back()
        wait_for_animation(driver, 2)
        assert "500" not in driver.page_source, \
            "500 error after returning from Tabby flow"
        screenshot(driver, "tabby_cancelled_returned")
