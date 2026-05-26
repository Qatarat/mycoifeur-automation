import time
from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage
from utils.helpers import scroll_to_text, wait_for_animation


class LoginPage(BasePage):

    def skip_onboarding(self):
        return self

    def select_country_and_language(self, country="Saudi Arabia", language="English"):
        return self

    def _select_bangladesh_country_code(self):
        self.tap("+966")
        fields = self.driver.find_elements(AppiumBy.XPATH, "//android.widget.EditText")
        if fields:
            fields[0].send_keys("Bangladesh")
            wait_for_animation(self.driver, 0.5)
        try:
            self.tap("Bangladesh")
        except Exception:
            scroll_to_text(self.driver, "Bangladesh", max_scrolls=20).click()
            wait_for_animation(self.driver)

    def enter_phone(self, phone):
        phone = phone.replace("+", "").replace(" ", "")
        if phone.startswith("880"):
            phone = phone[3:]
            if self.is_visible("+966", timeout=1):
                try:
                    self._select_bangladesh_country_code()
                except Exception:
                    for option in ("+880", "880", "(880)"):
                        self.tap_optional(option, timeout=1)
        self.tap_optional("User Login", timeout=1)
        self.tap_optional("Mobile Number", timeout=1)
        el = self.driver.find_element(AppiumBy.XPATH, "//android.widget.EditText")
        el.clear()
        el.send_keys(phone)
        return self

    def accept_terms(self):
        self.tap_optional("By clicking continue")
        return self

    def tap_continue(self):
        self.tap_optional("Send Verification Code")
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
        if self.is_visible("Verify Code", timeout=2):
            self.tap("Verify Code")
        else:
            self.tap("Verify")
        wait_for_animation(self.driver, 3)
        return self

    def login_phone_only(self, phone="8801316314566"):
        """Enter phone and tap Continue but stop before OTP. Used by negative OTP tests."""
        self.enter_phone(phone)
        self.accept_terms()
        self.tap_continue()
        return self

    def login(self, phone="8801316314566", otp="1234"):
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
