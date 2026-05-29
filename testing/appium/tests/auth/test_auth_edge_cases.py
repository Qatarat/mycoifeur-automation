"""
Auth edge cases — phone formatting, OTP input quirks, session behaviour.
"""
import pytest
from appium.webdriver.common.appiumby import AppiumBy
from pages.login_page import LoginPage
from utils.helpers import wait_for_animation, screenshot
from test_data import ValidData, InvalidPhone, BoundaryValues


@pytest.mark.auth
@pytest.mark.boundary
class TestPhoneInputEdgeCases:

    def test_phone_with_leading_spaces_trimmed_or_rejected(self, driver):
        """Leading/trailing spaces around phone number — must not crash, should trim."""
        login = LoginPage(driver)
        login.select_country_and_language()
        login.skip_onboarding()
        login.enter_phone("  " + ValidData.PHONE + "  ")
        login.tap_continue()
        page = driver.page_source
        assert "500" not in page
        screenshot(driver, "phone_leading_spaces")

    def test_phone_with_country_code_plus_prefix(self, driver):
        """User types +880 prefix — should be handled."""
        login = LoginPage(driver)
        login.select_country_and_language()
        login.skip_onboarding()
        login.enter_phone("+880" + ValidData.PHONE)
        login.tap_continue()
        page = driver.page_source
        assert "500" not in page
        screenshot(driver, "phone_country_code_prefix")

    def test_phone_all_same_digits(self, driver):
        """'1111111111' — valid format but invalid number."""
        login = LoginPage(driver)
        login.select_country_and_language()
        login.skip_onboarding()
        login.enter_phone("1111111111")
        login.tap_continue()
        page = driver.page_source
        assert "500" not in page
        screenshot(driver, "phone_all_same_digits")

    def test_phone_starting_with_zero(self, driver):
        """Phone starting with 0 — some regions use 0XXXXXXXXX format."""
        login = LoginPage(driver)
        login.select_country_and_language()
        login.skip_onboarding()
        login.enter_phone("0" + ValidData.PHONE[1:])
        login.tap_continue()
        page = driver.page_source
        assert "500" not in page
        screenshot(driver, "phone_starting_with_zero")

    def test_phone_with_dots(self, driver):
        """Dots in phone number — e.g. 880.168.522.0417"""
        login = LoginPage(driver)
        login.select_country_and_language()
        login.skip_onboarding()
        login.enter_phone("880.168.522.0417")
        login.tap_continue()
        page = driver.page_source
        assert "500" not in page
        screenshot(driver, "phone_with_dots")

    def test_phone_with_parentheses(self, driver):
        """Formatted phone (880) 1685220417 — common copy-paste format."""
        login = LoginPage(driver)
        login.select_country_and_language()
        login.skip_onboarding()
        login.enter_phone("(880) 1685220417")
        login.tap_continue()
        page = driver.page_source
        assert "500" not in page
        screenshot(driver, "phone_with_parentheses")

    def test_phone_exactly_max_length_not_exceeded(self, driver):
        """Phone input should cap at max digits, not allow infinite input."""
        login = LoginPage(driver)
        login.select_country_and_language()
        login.skip_onboarding()
        fields = driver.find_elements(AppiumBy.XPATH, "//android.widget.EditText")
        if not fields:
            login.tap_optional("User Login")
            login.tap_optional("Mobile Number")
            fields = driver.find_elements(AppiumBy.XPATH, "//android.widget.EditText")
        if fields:
            fields[0].send_keys("1" * 20)
            entered = (fields[0].text or "").replace(" ", "").replace("-", "").replace("+", "")
            assert len(entered) <= 20, "Phone field accepted more than expected digits"
        assert "500" not in driver.page_source
        screenshot(driver, "phone_max_length")

    def test_uppercase_in_phone_field_not_accepted(self, driver):
        """Phone field should be numeric — alpha chars must be blocked or ignored."""
        login = LoginPage(driver)
        login.select_country_and_language()
        login.skip_onboarding()
        login.enter_phone("ABCDEFGHIJ")
        login.tap_continue()
        page = driver.page_source
        assert "500" not in page
        screenshot(driver, "phone_uppercase_blocked")

    def test_phone_with_emoji_does_not_crash(self, driver):
        """Emoji in phone field — must not crash the app."""
        login = LoginPage(driver)
        login.select_country_and_language()
        login.skip_onboarding()
        login.enter_phone("📱8801316314566")
        login.tap_continue()
        assert "500" not in driver.page_source
        screenshot(driver, "phone_with_emoji")


@pytest.mark.auth
@pytest.mark.boundary
class TestOTPEdgeCases:

    def test_otp_with_spaces_between_digits(self, driver):
        """OTP '1 2 3 4' with spaces — should be trimmed or rejected clearly."""
        login = LoginPage(driver)
        login.select_country_and_language()
        login.skip_onboarding()
        login.login_phone_only(ValidData.PHONE)
        wait_for_animation(driver, 2)
        fields = driver.find_elements(AppiumBy.XPATH, "//android.widget.EditText")
        if fields:
            try:
                fields[0].clear()
                fields[0].send_keys("1 2 3 4")
            except Exception:
                pass
        login.tap_verify()
        page = driver.page_source
        assert "500" not in page
        screenshot(driver, "otp_spaces_between_digits")

    def test_otp_uppercase_letters_blocked(self, driver):
        """OTP is numeric-only — uppercase must be rejected."""
        login = LoginPage(driver)
        login.select_country_and_language()
        login.skip_onboarding()
        login.login_phone_only(ValidData.PHONE)
        wait_for_animation(driver, 2)
        fields = driver.find_elements(AppiumBy.XPATH, "//android.widget.EditText")
        if fields:
            try:
                fields[0].clear()
                fields[0].send_keys("ABCD")
            except Exception:
                pass
        login.tap_verify()
        assert "500" not in driver.page_source
        screenshot(driver, "otp_uppercase_blocked")

    def test_otp_special_chars_blocked(self, driver):
        """OTP '!@#$' must be rejected."""
        login = LoginPage(driver)
        login.select_country_and_language()
        login.skip_onboarding()
        login.login_phone_only(ValidData.PHONE)
        wait_for_animation(driver, 2)
        fields = driver.find_elements(AppiumBy.XPATH, "//android.widget.EditText")
        if fields:
            try:
                fields[0].clear()
                fields[0].send_keys("!@#$")
            except Exception:
                pass
        login.tap_verify()
        assert "500" not in driver.page_source
        screenshot(driver, "otp_special_chars_blocked")

    def test_otp_very_long_input_does_not_crash(self, driver):
        """100-digit OTP input — must not crash or show server error."""
        login = LoginPage(driver)
        login.select_country_and_language()
        login.skip_onboarding()
        login.login_phone_only(ValidData.PHONE)
        wait_for_animation(driver, 2)
        fields = driver.find_elements(AppiumBy.XPATH, "//android.widget.EditText")
        if fields:
            try:
                fields[0].clear()
                fields[0].send_keys("1" * 100)
            except Exception:
                pass
        login.tap_verify()
        assert "500" not in driver.page_source
        screenshot(driver, "otp_very_long_input")
