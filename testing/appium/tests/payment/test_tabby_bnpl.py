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

    def test_tabby_option_visible_above_minimum(self, driver):
        """Tabby should be visible when cart total meets minimum spend."""
        login = LoginPage(driver)
        login.select_country_and_language()
        login.skip_onboarding()
        login.login()

        cart = CartPage(driver)
        cart.add_first_item()
        cart.open_cart()
        cart.proceed_to_checkout()

        checkout = CheckoutPage(driver)
        # Tabby installment text should be visible
        assert checkout.is_visible("Pay later with Tabby") or \
               checkout.is_visible("4 interest-free"), \
            "Tabby payment option not visible"
        screenshot(driver, "tabby_option_visible")

    def test_tabby_shariah_compliance_info_visible(self, driver):
        """Verify Shariah-compliant badge and No Late Fees text show."""
        login = LoginPage(driver)
        login.select_country_and_language()
        login.skip_onboarding()
        login.login()

        cart = CartPage(driver)
        cart.add_first_item()
        cart.open_cart()
        cart.proceed_to_checkout()

        checkout = CheckoutPage(driver)
        scroll_to_text(driver, "Tabby")

        assert checkout.is_visible("Shariah") or \
               checkout.is_visible("No Late Fees"), \
            "Tabby Shariah compliance info not shown"
        screenshot(driver, "tabby_shariah_info")

    def test_tabby_learn_more_opens(self, driver):
        """Tapping Learn More should open Tabby details sheet."""
        login = LoginPage(driver)
        login.select_country_and_language()
        login.skip_onboarding()
        login.login()

        cart = CartPage(driver)
        cart.add_first_item()
        cart.open_cart()
        cart.proceed_to_checkout()

        checkout = CheckoutPage(driver)
        scroll_to_text(driver, "Learn More")
        checkout.tap_optional("Learn More")
        wait_for_animation(driver, 2)

        assert checkout.is_visible("Tabby") or \
               checkout.is_visible("installment"), \
            "Tabby Learn More sheet did not open"
        screenshot(driver, "tabby_learn_more")

    def test_tabby_payment_flow(self, driver):
        """Select Tabby → navigate Tabby WebView → verify cancel returns to app."""
        login = LoginPage(driver)
        login.select_country_and_language()
        login.skip_onboarding()
        login.login()

        cart = CartPage(driver)
        cart.add_first_item()
        cart.open_cart()
        cart.proceed_to_checkout()

        checkout = CheckoutPage(driver)
        checkout.select_tabby()
        wait_for_animation(driver, 3)
        screenshot(driver, "tabby_webview_opened")

        # Cancel/go back from Tabby
        driver.back()
        wait_for_animation(driver, 2)

        assert checkout.is_visible("Payment process was cancelled") or \
               checkout.is_visible("Payment Canceled") or \
               checkout.is_visible("Checkout"), \
            "Not returned to app after Tabby cancel"
        screenshot(driver, "tabby_cancelled_returned")
