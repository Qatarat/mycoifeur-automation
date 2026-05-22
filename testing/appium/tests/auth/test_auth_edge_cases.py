"""
Auth edge cases — phone formatting, OTP input quirks, session behaviour.
"""
import pytest
from appium.webdriver.common.appiumby import AppiumBy
from pages.login_page import LoginPage
from test_data import ValidData, InvalidPhone, BoundaryValues


@pytest.mark.auth
@pytest.mark.boundary
class TestPhoneInputEdgeCases:

    def test_phone_with_leading_spaces_trimmed_or_rejected(self, driver):
        """Leading/trailing spaces around phone number — must not crash, should trim."""
        login = LoginPage(driver)
        login.enter_phone("  " + ValidData.PHONE + "  ")
        login.tap_continue()
        # Either proceeds to OTP (spaces trimmed) or shows validation error
        page = driver.page_source
        assert "Something went wrong" not in page
        assert "500" not in page

    def test_phone_with_country_code_plus_prefix(self, driver):
        """User types +880 prefix — should be handled."""
        login = LoginPage(driver)
        login.enter_phone("+880" + ValidData.PHONE)
        login.tap_continue()
        page = driver.page_source
        assert "Something went wrong" not in page

    def test_phone_all_same_digits(self, driver):
        """'1111111111' — valid format but invalid number."""
        login = LoginPage(driver)
        login.enter_phone("1111111111")
        login.tap_continue()
        page = driver.page_source
        assert "Something went wrong" not in page

    def test_phone_starting_with_zero(self, driver):
        """Phone starting with 0 — some regions use 0XXXXXXXXX format."""
        login = LoginPage(driver)
        login.enter_phone("0" + ValidData.PHONE[1:])
        login.tap_continue()
        page = driver.page_source
        assert "Something went wrong" not in page

    def test_phone_with_dots(self, driver):
        """Dots in phone number — e.g. 880.168.522.0417"""
        login = LoginPage(driver)
        login.enter_phone("880.168.522.0417")
        login.tap_continue()
        page = driver.page_source
        assert "Something went wrong" not in page

    def test_phone_with_parentheses(self, driver):
        """Formatted phone (880) 1685220417 — common copy-paste format."""
        login = LoginPage(driver)
        login.enter_phone("(880) 1685220417")
        login.tap_continue()
        page = driver.page_source
        assert "Something went wrong" not in page

    def test_phone_exactly_max_length_not_exceeded(self, driver):
        """Phone input should cap at max digits, not allow infinite input."""
        login = LoginPage(driver)
        field = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "phone_input")
        field.send_keys("1" * 20)  # 20 digits
        entered = field.text.replace(" ", "").replace("-", "").replace("+", "")
        assert len(entered) <= 15  # E.164 max is 15 digits

    def test_uppercase_in_phone_field_not_accepted(self, driver):
        """Phone field should be numeric — alpha chars must be blocked or ignored."""
        login = LoginPage(driver)
        login.enter_phone("ABCDEFGHIJ")
        login.tap_continue()
        page = driver.page_source
        assert "Enter OTP" not in page  # Must not reach OTP screen

    def test_phone_with_emoji_does_not_crash(self, driver):
        """Emoji in phone field — must not crash the app."""
        login = LoginPage(driver)
        login.enter_phone("📱8801685220417")
        login.tap_continue()
        assert "500" not in driver.page_source


@pytest.mark.auth
@pytest.mark.boundary
class TestOTPEdgeCases:

    def test_otp_with_spaces_between_digits(self, driver):
        """OTP '1 2 3 4' with spaces — should be trimmed or rejected clearly."""
        login = LoginPage(driver)
        login.login_phone_only(ValidData.PHONE)
        otp_field = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "otp_input")
        otp_field.send_keys("1 2 3 4")
        driver.find_element(AppiumBy.ACCESSIBILITY_ID, "verify_button").click()
        page = driver.page_source
        assert "Something went wrong" not in page
        assert "500" not in page

    def test_otp_uppercase_letters_blocked(self, driver):
        """OTP is numeric-only — uppercase must be rejected."""
        login = LoginPage(driver)
        login.login_phone_only(ValidData.PHONE)
        otp_field = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "otp_input")
        otp_field.send_keys("ABCD")
        driver.find_element(AppiumBy.ACCESSIBILITY_ID, "verify_button").click()
        assert "Cart" not in driver.page_source  # Must not log in

    def test_otp_special_chars_blocked(self, driver):
        """OTP '!@#$' must be rejected."""
        login = LoginPage(driver)
        login.login_phone_only(ValidData.PHONE)
        otp_field = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "otp_input")
        otp_field.send_keys("!@#$")
        driver.find_element(AppiumBy.ACCESSIBILITY_ID, "verify_button").click()
        assert "Cart" not in driver.page_source

    def test_otp_very_long_input_does_not_crash(self, driver):
        """100-digit OTP input — must not crash or show server error."""
        login = LoginPage(driver)
        login.login_phone_only(ValidData.PHONE)
        otp_field = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "otp_input")
        otp_field.send_keys("1" * 100)
        driver.find_element(AppiumBy.ACCESSIBILITY_ID, "verify_button").click()
        assert "500" not in driver.page_source
        assert "crash" not in driver.page_source.lower()
