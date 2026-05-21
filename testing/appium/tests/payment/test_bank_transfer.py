import os
import pytest
from pages.login_page import LoginPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.helpers import screenshot, wait_for_animation


SAMPLE_RECEIPT = os.path.join(
    os.path.dirname(__file__), "../../assets/sample_receipt.jpg"
)


@pytest.mark.payment
class TestBankTransfer:
    """
    Bank transfer payment flow — upload receipt and await manual approval.
    """

    def test_bank_transfer_option_visible(self, driver):
        """Bank transfer option should appear in payment screen."""
        login = LoginPage(driver)
        login.select_country_and_language()
        login.skip_onboarding()
        login.login()

        cart = CartPage(driver)
        cart.add_first_item()
        cart.open_cart()
        cart.proceed_to_checkout()

        checkout = CheckoutPage(driver)
        assert checkout.is_visible("Bank Transfer") or \
               checkout.is_visible("Bank Name"), \
            "Bank transfer option not visible"
        screenshot(driver, "bank_transfer_option")

    def test_bank_transfer_shows_account_details(self, driver):
        """Selecting bank transfer should show account holder info."""
        login = LoginPage(driver)
        login.select_country_and_language()
        login.skip_onboarding()
        login.login()

        cart = CartPage(driver)
        cart.add_first_item()
        cart.open_cart()
        cart.proceed_to_checkout()

        checkout = CheckoutPage(driver)
        checkout.select_bank_transfer()
        wait_for_animation(driver, 2)

        assert checkout.is_visible("Bank Name") or \
               checkout.is_visible("Account Holder Name") or \
               checkout.is_visible("Transaction Reference"), \
            "Bank account details not displayed"
        screenshot(driver, "bank_transfer_details")

    def test_bank_transfer_receipt_upload_prompt(self, driver):
        """Receipt upload prompt should appear after selecting bank transfer."""
        login = LoginPage(driver)
        login.select_country_and_language()
        login.skip_onboarding()
        login.login()

        cart = CartPage(driver)
        cart.add_first_item()
        cart.open_cart()
        cart.proceed_to_checkout()

        checkout = CheckoutPage(driver)
        checkout.select_bank_transfer()
        wait_for_animation(driver, 2)

        checkout.tap_optional("Submit Order")
        wait_for_animation(driver, 2)

        assert checkout.is_visible("Please attach the payment receipt") or \
               checkout.is_visible("upload"), \
            "Receipt upload prompt not shown"
        screenshot(driver, "bank_receipt_prompt")

    def test_bank_transfer_receipt_source_options(self, driver):
        """Upload dialog should offer Camera and Gallery options."""
        login = LoginPage(driver)
        login.select_country_and_language()
        login.skip_onboarding()
        login.login()

        cart = CartPage(driver)
        cart.add_first_item()
        cart.open_cart()
        cart.proceed_to_checkout()

        checkout = CheckoutPage(driver)
        checkout.select_bank_transfer()
        wait_for_animation(driver)
        checkout.tap_optional("Please attach the payment receipt")
        checkout.tap_optional("Upload")
        wait_for_animation(driver)

        assert checkout.is_visible("Take a Photo") or \
               checkout.is_visible("Choose from Gallery"), \
            "Photo source options not shown"
        screenshot(driver, "bank_receipt_source_options")
