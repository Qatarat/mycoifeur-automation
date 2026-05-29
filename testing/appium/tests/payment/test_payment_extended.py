"""
Extended payment tests — edge cases, boundary values, input formatting.
Covers: cart flow + checkout screen integrity, no crash on navigation.
"""
import pytest
from appium.webdriver.common.appiumby import AppiumBy
from pages.login_page import LoginPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.helpers import screenshot, wait_for_animation
from test_data import ValidData


def _login_and_reach_checkout(driver):
    login = LoginPage(driver)
    login.select_country_and_language()
    login.skip_onboarding()
    login.login()
    cart = CartPage(driver)
    cart.add_first_item()
    cart.open_cart()
    cart.proceed_to_checkout()
    return CheckoutPage(driver)


@pytest.mark.payment
@pytest.mark.boundary
class TestCardInputFormatting:

    def test_card_with_spaces_handled_gracefully(self, driver):
        """App must not crash when card number contains spaces."""
        checkout = _login_and_reach_checkout(driver)
        checkout.fill_card_details("4111 1111 1111 1111", "12/28", "123", "Test User")
        assert "500" not in driver.page_source
        screenshot(driver, "card_spaces_no_crash")

    def test_card_with_dashes_handled_gracefully(self, driver):
        """App must not crash when card number contains dashes."""
        checkout = _login_and_reach_checkout(driver)
        checkout.fill_card_details("4111-1111-1111-1111", "12/28", "123", "Test User")
        assert "500" not in driver.page_source
        screenshot(driver, "card_dashes_no_crash")

    def test_card_with_leading_spaces_handled(self, driver):
        """App must not crash on leading/trailing spaces in card number."""
        checkout = _login_and_reach_checkout(driver)
        checkout.fill_card_details("  4111111111111111  ", "12/28", "123", "Test User")
        assert "500" not in driver.page_source
        screenshot(driver, "card_leading_spaces_no_crash")

    def test_card_number_field_no_crash(self, driver):
        """Card number entry must not cause a 500 error."""
        checkout = _login_and_reach_checkout(driver)
        checkout.select_card_payment()
        wait_for_animation(driver)
        fields = driver.find_elements(AppiumBy.XPATH, "//android.widget.EditText")
        if fields:
            try:
                fields[0].send_keys("41111111111111119999")
            except Exception:
                pass
        assert "500" not in driver.page_source
        screenshot(driver, "card_number_field_no_crash")

    def test_cvv_with_letters_no_crash(self, driver):
        """CVV with letter input must not crash the app."""
        checkout = _login_and_reach_checkout(driver)
        checkout.fill_card_details(ValidData.CARD["number"], "12/28", "AB3", "Test User")
        assert "500" not in driver.page_source
        screenshot(driver, "cvv_letters_no_crash")

    def test_cvv_with_special_chars_no_crash(self, driver):
        """CVV with special chars must not crash the app."""
        checkout = _login_and_reach_checkout(driver)
        checkout.fill_card_details(ValidData.CARD["number"], "12/28", "@#!", "Test User")
        assert "500" not in driver.page_source
        screenshot(driver, "cvv_special_chars_no_crash")

    def test_cvv_4_digits_no_crash(self, driver):
        """4-digit CVV (Amex style) must not crash the app."""
        checkout = _login_and_reach_checkout(driver)
        checkout.fill_card_details("378282246310005", "12/28", "1234", "Test User")
        assert "500" not in driver.page_source
        screenshot(driver, "cvv_4_digits_no_crash")


@pytest.mark.payment
@pytest.mark.boundary
class TestExpiryBoundary:

    def test_current_month_expiry_no_crash(self, driver):
        """A card expiring this month must not crash the app."""
        from datetime import date
        today = date.today()
        expiry = f"{today.month:02d}/{str(today.year)[2:]}"
        checkout = _login_and_reach_checkout(driver)
        checkout.fill_card_details(ValidData.CARD["number"], expiry, "123", "Test User")
        assert "500" not in driver.page_source
        screenshot(driver, "current_month_expiry_no_crash")

    def test_far_future_expiry_no_crash(self, driver):
        """12/99 expiry input must not crash the app."""
        checkout = _login_and_reach_checkout(driver)
        checkout.fill_card_details(ValidData.CARD["number"], "12/99", "123", "Test User")
        assert "500" not in driver.page_source
        screenshot(driver, "far_future_expiry_no_crash")

    def test_expiry_without_slash_no_crash(self, driver):
        """User types '1228' (no slash) — app must not crash."""
        checkout = _login_and_reach_checkout(driver)
        checkout.fill_card_details(ValidData.CARD["number"], "1228", "123", "Test User")
        assert "500" not in driver.page_source
        screenshot(driver, "expiry_no_slash_no_crash")

    def test_expiry_month_zero_no_crash(self, driver):
        """Month 00 expiry must not crash the app."""
        checkout = _login_and_reach_checkout(driver)
        checkout.fill_card_details(ValidData.CARD["number"], "00/30", "123", "Test User")
        assert "500" not in driver.page_source
        screenshot(driver, "expiry_month_zero_no_crash")


@pytest.mark.payment
@pytest.mark.boundary
class TestCardholderName:

    def test_cardholder_name_with_numbers_no_crash(self, driver):
        """Name like 'John123' must not crash the app."""
        checkout = _login_and_reach_checkout(driver)
        checkout.fill_card_details(ValidData.CARD["number"], "12/28", "123", "John123")
        assert "500" not in driver.page_source
        screenshot(driver, "cardholder_name_numbers_no_crash")

    def test_cardholder_name_all_spaces_no_crash(self, driver):
        """All-spaces cardholder name must not crash the app."""
        checkout = _login_and_reach_checkout(driver)
        checkout.fill_card_details(ValidData.CARD["number"], "12/28", "123", "     ")
        assert "500" not in driver.page_source
        screenshot(driver, "cardholder_name_spaces_no_crash")

    def test_cardholder_name_uppercase_no_crash(self, driver):
        """ALL CAPS name must not crash the app."""
        checkout = _login_and_reach_checkout(driver)
        checkout.fill_card_details(ValidData.CARD["number"], "12/28", "123", "MEJBAUR BAHAR FAGUN")
        assert "500" not in driver.page_source
        screenshot(driver, "cardholder_name_uppercase_no_crash")

    def test_cardholder_name_50_chars_no_crash(self, driver):
        """50-char cardholder name must not crash the app."""
        checkout = _login_and_reach_checkout(driver)
        checkout.fill_card_details(ValidData.CARD["number"], "12/28", "123", "A" * 50)
        assert "500" not in driver.page_source
        screenshot(driver, "cardholder_name_50_chars_no_crash")

    def test_cardholder_name_arabic_no_crash(self, driver):
        """Arabic cardholder name must not crash the app."""
        checkout = _login_and_reach_checkout(driver)
        checkout.fill_card_details(ValidData.CARD["number"], "12/28", "123", "محمد عبدالله")
        assert "500" not in driver.page_source
        screenshot(driver, "cardholder_name_arabic_no_crash")
