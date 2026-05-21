import time
from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage
from utils.helpers import wait_for_animation


class LoginPage(BasePage):

    def skip_onboarding(self):
        self.tap_optional("Skip")
        return self

    def select_country_and_language(self, country="Saudi Arabia", language="English"):
        self.tap_optional("Select your country")
        self.tap_optional(country)
        self.tap_optional("Select your language")
        self.tap_optional(language)
        wait_for_animation(self.driver, 1)
        return self

    def enter_phone(self, phone):
        self.tap_optional("Login to your account")
        self.tap_optional("Enter phone number")
        el = self.driver.find_element(AppiumBy.XPATH, "//android.widget.EditText")
        el.clear()
        el.send_keys(phone)
        return self

    def accept_terms(self):
        self.tap_optional("By clicking continue")
        return self

    def tap_continue(self):
        self.tap_optional("Continue")
        wait_for_animation(self.driver, 2)
        return self

    def enter_otp(self, otp="1234"):
        # OTP is usually 6 separate input boxes or one field
        try:
            el = self.driver.find_element(AppiumBy.XPATH, "//android.widget.EditText")
            el.send_keys(otp)
        except Exception:
            for digit in otp:
                fields = self.driver.find_elements(AppiumBy.XPATH, "//android.widget.EditText")
                if fields:
                    fields[0].send_keys(digit)
                    time.sleep(0.15)
        return self

    def tap_verify(self):
        self.tap("Verify")
        wait_for_animation(self.driver, 3)
        return self

    def login(self, phone="8801685220417", otp="1234"):
        self.select_country_and_language()
        self.skip_onboarding()
        self.enter_phone(phone)
        self.accept_terms()
        self.tap_continue()
        self.enter_otp(otp)
        self.tap_verify()
        return self

    def assert_logged_in(self):
        assert self.is_visible("Cart") or self.is_visible("My Orders"), \
            "Login failed — expected to see Cart or My Orders after login"
        return self
