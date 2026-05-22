"""
Extended payment tests — edge cases, boundary values, input formatting.
Covers: card with spaces/dashes, far-future expiry, CVV edge cases,
        cardholder name variants, international cards, currency display.
"""
import pytest
from appium.webdriver.common.appiumby import AppiumBy
from pages.login_page import LoginPage
from pages.cart_page import CartPage
from test_data import ValidData, InvalidCard, BoundaryValues


@pytest.mark.payment
@pytest.mark.boundary
class TestCardInputFormatting:

    @pytest.mark.parametrize("card_number", [
        "4111 1111 1111 1111",   # spaces — common paste format
        "4111-1111-1111-1111",   # dashes — common typed format
        "  4111111111111111  ",  # leading/trailing spaces
    ])
    def test_card_with_separators_handled_gracefully(self, driver, card_number):
        """App should either accept formatted input or show a clear validation error."""
        login = LoginPage(driver)
        login.login(ValidData.PHONE, ValidData.OTP)
        cart = CartPage(driver)
        cart.add_item_and_go_to_checkout()
        driver.find_element(AppiumBy.ACCESSIBILITY_ID, "card_number_field").send_keys(card_number)
        driver.find_element(AppiumBy.ACCESSIBILITY_ID, "card_expiry_field").send_keys("12/28")
        driver.find_element(AppiumBy.ACCESSIBILITY_ID, "card_cvv_field").send_keys("123")
        driver.find_element(AppiumBy.ACCESSIBILITY_ID, "cardholder_name_field").send_keys("Test User")
        page_source = driver.page_source
        # Either processes or shows user-friendly validation — must NOT crash
        assert "Something went wrong" not in page_source
        assert "500" not in page_source

    def test_card_number_max_16_digits_enforced(self, driver):
        """Input field must not accept more than 19 chars (16 digits + 3 spaces)."""
        login = LoginPage(driver)
        login.login(ValidData.PHONE, ValidData.OTP)
        cart = CartPage(driver)
        cart.add_item_and_go_to_checkout()
        field = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "card_number_field")
        field.send_keys("41111111111111119999")  # 20 digits
        entered = field.text.replace(" ", "").replace("-", "")
        assert len(entered) <= 16

    def test_cvv_with_letters_shows_error(self, driver):
        login = LoginPage(driver)
        login.login(ValidData.PHONE, ValidData.OTP)
        cart = CartPage(driver)
        cart.add_item_and_go_to_checkout()
        driver.find_element(AppiumBy.ACCESSIBILITY_ID, "card_number_field").send_keys(ValidData.CARD_NUMBER)
        driver.find_element(AppiumBy.ACCESSIBILITY_ID, "card_expiry_field").send_keys("12/28")
        driver.find_element(AppiumBy.ACCESSIBILITY_ID, "card_cvv_field").send_keys("AB3")
        driver.find_element(AppiumBy.ACCESSIBILITY_ID, "pay_button").click()
        page_source = driver.page_source
        assert "invalid" in page_source.lower() or "error" in page_source.lower() or "CVV" in page_source

    def test_cvv_with_special_chars_shows_error(self, driver):
        login = LoginPage(driver)
        login.login(ValidData.PHONE, ValidData.OTP)
        cart = CartPage(driver)
        cart.add_item_and_go_to_checkout()
        driver.find_element(AppiumBy.ACCESSIBILITY_ID, "card_cvv_field").send_keys("@#!")
        driver.find_element(AppiumBy.ACCESSIBILITY_ID, "pay_button").click()
        assert "invalid" in driver.page_source.lower() or "error" in driver.page_source.lower()

    def test_cvv_4_digits_for_amex(self, driver):
        """Amex cards use 4-digit CVV — app should accept it."""
        login = LoginPage(driver)
        login.login(ValidData.PHONE, ValidData.OTP)
        cart = CartPage(driver)
        cart.add_item_and_go_to_checkout()
        driver.find_element(AppiumBy.ACCESSIBILITY_ID, "card_number_field").send_keys("378282246310005")
        driver.find_element(AppiumBy.ACCESSIBILITY_ID, "card_expiry_field").send_keys("12/28")
        driver.find_element(AppiumBy.ACCESSIBILITY_ID, "card_cvv_field").send_keys("1234")
        assert "Something went wrong" not in driver.page_source


@pytest.mark.payment
@pytest.mark.boundary
class TestExpiryBoundary:

    def test_current_month_expiry_is_valid(self, driver):
        """A card expiring this month must be accepted (not yet expired)."""
        from datetime import date
        today = date.today()
        expiry = f"{today.month:02d}/{str(today.year)[2:]}"
        login = LoginPage(driver)
        login.login(ValidData.PHONE, ValidData.OTP)
        cart = CartPage(driver)
        cart.add_item_and_go_to_checkout()
        driver.find_element(AppiumBy.ACCESSIBILITY_ID, "card_number_field").send_keys(ValidData.CARD_NUMBER)
        driver.find_element(AppiumBy.ACCESSIBILITY_ID, "card_expiry_field").send_keys(expiry)
        assert "expired" not in driver.page_source.lower()

    def test_far_future_expiry_accepted(self, driver):
        """12/99 is technically valid input — must not be rejected as malformed."""
        login = LoginPage(driver)
        login.login(ValidData.PHONE, ValidData.OTP)
        cart = CartPage(driver)
        cart.add_item_and_go_to_checkout()
        driver.find_element(AppiumBy.ACCESSIBILITY_ID, "card_number_field").send_keys(ValidData.CARD_NUMBER)
        driver.find_element(AppiumBy.ACCESSIBILITY_ID, "card_expiry_field").send_keys("12/99")
        driver.find_element(AppiumBy.ACCESSIBILITY_ID, "card_cvv_field").send_keys("123")
        driver.find_element(AppiumBy.ACCESSIBILITY_ID, "cardholder_name_field").send_keys("Test User")
        assert "invalid" not in driver.page_source.lower()

    def test_expiry_without_slash_handled(self, driver):
        """User types '1228' (no slash) — app should format or show hint."""
        login = LoginPage(driver)
        login.login(ValidData.PHONE, ValidData.OTP)
        cart = CartPage(driver)
        cart.add_item_and_go_to_checkout()
        field = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "card_expiry_field")
        field.send_keys("1228")
        # Should auto-format to 12/28 or show format hint — must not crash
        assert "Something went wrong" not in driver.page_source

    def test_expiry_month_zero_shows_error(self, driver):
        login = LoginPage(driver)
        login.login(ValidData.PHONE, ValidData.OTP)
        cart = CartPage(driver)
        cart.add_item_and_go_to_checkout()
        driver.find_element(AppiumBy.ACCESSIBILITY_ID, "card_number_field").send_keys(ValidData.CARD_NUMBER)
        driver.find_element(AppiumBy.ACCESSIBILITY_ID, "card_expiry_field").send_keys("00/30")
        driver.find_element(AppiumBy.ACCESSIBILITY_ID, "pay_button").click()
        assert "invalid" in driver.page_source.lower() or "error" in driver.page_source.lower()


@pytest.mark.payment
@pytest.mark.boundary
class TestCardholderName:

    def test_cardholder_name_with_numbers_handled(self, driver):
        """Name like 'John123' — some gateways reject this, UI should guide user."""
        login = LoginPage(driver)
        login.login(ValidData.PHONE, ValidData.OTP)
        cart = CartPage(driver)
        cart.add_item_and_go_to_checkout()
        driver.find_element(AppiumBy.ACCESSIBILITY_ID, "cardholder_name_field").send_keys("John123")
        assert "Something went wrong" not in driver.page_source

    def test_cardholder_name_all_spaces_shows_error(self, driver):
        login = LoginPage(driver)
        login.login(ValidData.PHONE, ValidData.OTP)
        cart = CartPage(driver)
        cart.add_item_and_go_to_checkout()
        driver.find_element(AppiumBy.ACCESSIBILITY_ID, "card_number_field").send_keys(ValidData.CARD_NUMBER)
        driver.find_element(AppiumBy.ACCESSIBILITY_ID, "card_expiry_field").send_keys("12/28")
        driver.find_element(AppiumBy.ACCESSIBILITY_ID, "card_cvv_field").send_keys("123")
        driver.find_element(AppiumBy.ACCESSIBILITY_ID, "cardholder_name_field").send_keys("     ")
        driver.find_element(AppiumBy.ACCESSIBILITY_ID, "pay_button").click()
        assert "invalid" in driver.page_source.lower() or "required" in driver.page_source.lower() or "error" in driver.page_source.lower()

    def test_cardholder_name_uppercase_accepted(self, driver):
        """ALL CAPS name is standard on physical cards — must be accepted."""
        login = LoginPage(driver)
        login.login(ValidData.PHONE, ValidData.OTP)
        cart = CartPage(driver)
        cart.add_item_and_go_to_checkout()
        driver.find_element(AppiumBy.ACCESSIBILITY_ID, "card_number_field").send_keys(ValidData.CARD_NUMBER)
        driver.find_element(AppiumBy.ACCESSIBILITY_ID, "card_expiry_field").send_keys("12/28")
        driver.find_element(AppiumBy.ACCESSIBILITY_ID, "card_cvv_field").send_keys("123")
        driver.find_element(AppiumBy.ACCESSIBILITY_ID, "cardholder_name_field").send_keys("MEJBAUR BAHAR FAGUN")
        assert "invalid" not in driver.page_source.lower()
        assert "error" not in driver.page_source.lower()

    def test_cardholder_name_50_chars_handled(self, driver):
        long_name = "A" * 50
        login = LoginPage(driver)
        login.login(ValidData.PHONE, ValidData.OTP)
        cart = CartPage(driver)
        cart.add_item_and_go_to_checkout()
        driver.find_element(AppiumBy.ACCESSIBILITY_ID, "cardholder_name_field").send_keys(long_name)
        assert "Something went wrong" not in driver.page_source

    def test_cardholder_name_arabic_handled(self, driver):
        """Arabic cardholder name — some gateways reject Unicode names."""
        login = LoginPage(driver)
        login.login(ValidData.PHONE, ValidData.OTP)
        cart = CartPage(driver)
        cart.add_item_and_go_to_checkout()
        driver.find_element(AppiumBy.ACCESSIBILITY_ID, "cardholder_name_field").send_keys("محمد عبدالله")
        assert "crash" not in driver.page_source.lower()
        assert "500" not in driver.page_source
