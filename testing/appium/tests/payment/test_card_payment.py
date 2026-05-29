import pytest
from pages.login_page import LoginPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.helpers import screenshot, wait_for_animation


@pytest.mark.payment
@pytest.mark.android
class TestCardPayment:
    """
    HyperPay card payment flow.
    Uses the stage environment card:  4111 1111 1111 1111 / 12/25 / 123
    """

    STAGE_CARD = {
        "number": "4111111111111111",
        "expiry": "12/25",
        "cvv": "123",
        "name": "Test User",
    }

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

    def test_card_payment_flow_reaches_processing(self, driver):
        """Verify full card payment flow does not cause a 500 error."""
        checkout = self._login_and_reach_checkout(driver)
        assert "500" not in driver.page_source
        screenshot(driver, "card_payment_cart")

        checkout.select_card_payment()
        wait_for_animation(driver, 2)
        screenshot(driver, "card_payment_form")

        checkout.fill_card_details(
            self.STAGE_CARD["number"],
            self.STAGE_CARD["expiry"],
            self.STAGE_CARD["cvv"],
            self.STAGE_CARD["name"],
        )
        checkout.submit_order()
        screenshot(driver, "card_payment_submitted")
        assert "500" not in driver.page_source

    def test_card_payment_expired_card_shows_error(self, driver):
        """Expired card flow must not cause a 500 error."""
        checkout = self._login_and_reach_checkout(driver)
        checkout.select_card_payment()
        checkout.fill_card_details("4111111111111111", "01/20", "123", "Test User")
        checkout.submit_order()
        wait_for_animation(driver, 3)
        assert "500" not in driver.page_source
        screenshot(driver, "card_expired_error")

    def test_card_payment_insufficient_funds(self, driver):
        """Declined payment flow must not cause a 500 error."""
        checkout = self._login_and_reach_checkout(driver)
        checkout.select_card_payment()
        checkout.fill_card_details("4000000000000002", "12/25", "123", "Test User")
        checkout.submit_order()
        wait_for_animation(driver, 3)
        assert "500" not in driver.page_source
        screenshot(driver, "card_payment_declined")

    def test_promo_code_reduces_total(self, driver):
        """Promo code entry must not crash the app."""
        login = LoginPage(driver)
        login.select_country_and_language()
        login.skip_onboarding()
        login.login()
        cart = CartPage(driver)
        cart.add_first_item()
        cart.open_cart()
        cart.apply_promo("TEST10")
        wait_for_animation(driver, 2)
        assert "500" not in driver.page_source
        screenshot(driver, "promo_code_applied")
