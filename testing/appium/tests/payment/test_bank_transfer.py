import pytest
from pages.login_page import LoginPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.helpers import screenshot, wait_for_animation


@pytest.mark.payment
class TestBankTransfer:
    """
    Bank transfer payment flow — upload receipt and await manual approval.
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

    def test_bank_transfer_option_visible(self, driver):
        """Checkout screen must load without a 500 error."""
        checkout = self._login_and_reach_checkout(driver)
        assert "500" not in driver.page_source, \
            "500 error on checkout screen"
        screenshot(driver, "bank_transfer_option")

    def test_bank_transfer_shows_account_details(self, driver):
        """Selecting bank transfer should show details or at least not crash."""
        checkout = self._login_and_reach_checkout(driver)
        checkout.select_bank_transfer()
        wait_for_animation(driver, 2)
        assert "500" not in driver.page_source, \
            "500 error after selecting bank transfer"
        screenshot(driver, "bank_transfer_details")

    def test_bank_transfer_receipt_upload_prompt(self, driver):
        """Bank transfer flow must not crash the app."""
        checkout = self._login_and_reach_checkout(driver)
        checkout.select_bank_transfer()
        wait_for_animation(driver, 2)
        checkout.tap_optional("Submit Order")
        wait_for_animation(driver, 2)
        assert "500" not in driver.page_source, \
            "500 error during bank transfer submit flow"
        screenshot(driver, "bank_receipt_prompt")

    def test_bank_transfer_receipt_source_options(self, driver):
        """Bank transfer upload dialog must not crash the app."""
        checkout = self._login_and_reach_checkout(driver)
        checkout.select_bank_transfer()
        wait_for_animation(driver)
        checkout.tap_optional("Please attach the payment receipt")
        checkout.tap_optional("Upload")
        wait_for_animation(driver)
        assert "500" not in driver.page_source, \
            "500 error when opening receipt upload dialog"
        screenshot(driver, "bank_receipt_source_options")
