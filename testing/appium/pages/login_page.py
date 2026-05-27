import time
from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage
from utils.helpers import scroll_to_text, wait_for_animation


class LoginPage(BasePage):
    BANGLADESH_DIAL_CODE = "880"
    BANGLADESH_COUNTRY = "Bangladesh"
    COUNTRY_SEARCH_TEXT = "Bangladesh"
    DEFAULT_PHONE = "1316314566"
    DEFAULT_OTP = "1234"
    ANDROID_KEYCODES = {
        "a": 29,
        "b": 30,
        "c": 31,
        "d": 32,
        "e": 33,
        "f": 34,
        "g": 35,
        "h": 36,
        "i": 37,
        "j": 38,
        "k": 39,
        "l": 40,
        "m": 41,
        "n": 42,
        "o": 43,
        "p": 44,
        "q": 45,
        "r": 46,
        "s": 47,
        "t": 48,
        "u": 49,
        "v": 50,
        "w": 51,
        "x": 52,
        "y": 53,
        "z": 54,
    }

    def skip_onboarding(self):
        return self

    def select_country_and_language(self, country="Saudi Arabia", language="English"):
        return self

    def _country_search_fields(self):
        return self.driver.find_elements(AppiumBy.XPATH, "//android.widget.EditText")

    def _is_country_picker_open(self):
        source = self.driver.page_source
        return "Search Country" in source or "Afghanistan" in source or self.COUNTRY_SEARCH_TEXT in source

    def _tap_first_match(self, xpaths):
        for xpath in xpaths:
            for element in self.driver.find_elements(AppiumBy.XPATH, xpath):
                try:
                    element.click()
                    wait_for_animation(self.driver, 0.5)
                    return True
                except Exception:
                    continue
        return False

    def _open_country_code_selector(self):
        if self._is_country_picker_open():
            return

        self.driver.implicitly_wait(1)
        if self._tap_first_match([
            '//*[@text="+966" or @content-desc="+966"]',
            '//*[contains(@text,"+966") or contains(@content-desc,"+966")]',
            '//*[@text="+880" or @content-desc="+880"]',
            '//*[contains(@text,"+880") or contains(@content-desc,"+880")]',
            '//*[contains(@text,"+") or contains(@content-desc,"+")]',
        ]):
            self.driver.implicitly_wait(10)
            return
        self.driver.implicitly_wait(10)

        fields = self._country_search_fields()
        if fields:
            rect = fields[0].rect
            x = rect["x"] + int(rect["width"] * 0.22)
            y = rect["y"] + rect["height"] // 2
        else:
            size = self.driver.get_window_size()
            x = int(size["width"] * 0.22)
            y = int(size["height"] * 0.42)

        try:
            self.driver.execute_script("mobile: clickGesture", {"x": x, "y": y})
        except Exception:
            self.driver.tap([(x, y)])
        wait_for_animation(self.driver, 0.5)

    def _tap_first_country_result(self, search_field):
        rect = search_field.rect
        x = rect["x"] + rect["width"] // 2
        y = rect["y"] + rect["height"] + 95
        try:
            self.driver.hide_keyboard()
            wait_for_animation(self.driver, 0.3)
        except Exception:
            pass

        try:
            self.driver.execute_script("mobile: clickGesture", {"x": x, "y": y})
        except Exception:
            self.driver.tap([(x, y)])
        wait_for_animation(self.driver, 1)

    def _assert_bangladesh_selected(self):
        if "+880" not in self.driver.page_source:
            raise AssertionError("Bangladesh country code was not selected before phone entry")

    def _tap_bangladesh_with_scrollable(self):
        selector = (
            'new UiScrollable(new UiSelector().scrollable(true))'
            f'.scrollTextIntoView("{self.BANGLADESH_COUNTRY}")'
        )
        self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, selector).click()
        wait_for_animation(self.driver, 1)
        return True

    def _tap_bangladesh_result_by_text(self):
        locators = [
            '//*[@text="Bangladesh" and @class!="android.widget.EditText"]',
            '//*[contains(@text,"Bangladesh") and @class!="android.widget.EditText"]',
            '//*[@content-desc="Bangladesh"]',
            '//*[contains(@content-desc,"Bangladesh")]',
        ]
        previous_wait = None
        try:
            previous_wait = self.driver.timeouts.implicit_wait
        except Exception:
            pass

        self.driver.implicitly_wait(1)
        try:
            for xpath in locators:
                matches = self.driver.find_elements(AppiumBy.XPATH, xpath)
                for match in matches:
                    try:
                        element_class = match.get_attribute("class") or ""
                    except Exception:
                        element_class = ""
                    if element_class == "android.widget.EditText":
                        continue
                    try:
                        match.click()
                        wait_for_animation(self.driver, 1)
                        return True
                    except Exception:
                        continue
        finally:
            self.driver.implicitly_wait(previous_wait if previous_wait is not None else 10)
        return False

    def _field_contains_text(self, field, text):
        candidates = [getattr(field, "text", "")]
        for attr in ("text", "value"):
            try:
                candidates.append(field.get_attribute(attr))
            except Exception:
                pass
        expected = text.lower()
        return any(expected in (candidate or "").lower() for candidate in candidates)

    def _type_with_android_keycodes(self, text):
        for char in text.lower():
            keycode = 7 + int(char) if char.isdigit() else self.ANDROID_KEYCODES.get(char)
            if keycode is not None:
                self.driver.press_keycode(keycode)
                time.sleep(0.05)

    def _hide_keyboard_optional(self):
        try:
            self.driver.hide_keyboard()
            wait_for_animation(self.driver, 0.4)
        except Exception:
            pass

    def _tap_primary_phone_button_by_position(self):
        size = self.driver.get_window_size()
        x = size["width"] // 2
        y = int(size["height"] * 0.54)
        try:
            self.driver.execute_script("mobile: clickGesture", {"x": x, "y": y})
        except Exception:
            self.driver.tap([(x, y)])
        wait_for_animation(self.driver, 2)

    def _search_bangladesh_country(self):
        fields = self._country_search_fields()
        if not fields:
            raise AssertionError("Country search field was not available")

        search_field = fields[0]
        try:
            search_field.click()
            wait_for_animation(self.driver, 0.3)
        except Exception:
            pass
        search_field.clear()
        search_field.send_keys(self.COUNTRY_SEARCH_TEXT)
        wait_for_animation(self.driver, 0.8)
        if not self._field_contains_text(search_field, self.COUNTRY_SEARCH_TEXT):
            search_field.clear()
            self._type_with_android_keycodes(self.COUNTRY_SEARCH_TEXT)
        wait_for_animation(self.driver, 2)
        return search_field

    def _select_bangladesh_country_code(self):
        if "+880" in self.driver.page_source:
            return self

        self._open_country_code_selector()
        search_field = self._search_bangladesh_country()

        selected = self._tap_bangladesh_result_by_text()
        if not selected and "+880" not in self.driver.page_source:
            try:
                selected = self._tap_bangladesh_with_scrollable()
            except Exception:
                selected = False
        if not selected and "+880" not in self.driver.page_source:
            try:
                scroll_to_text(self.driver, self.BANGLADESH_COUNTRY, max_scrolls=20).click()
                selected = True
            except Exception:
                selected = False
        if not selected and "+880" not in self.driver.page_source:
            self._tap_first_country_result(search_field)
        wait_for_animation(self.driver)
        self._assert_bangladesh_selected()
        return self

    def _normalize_phone_for_entry(self, phone):
        phone = phone.strip().replace("+", "").replace(" ", "")
        if phone.startswith(self.BANGLADESH_DIAL_CODE):
            phone = phone[len(self.BANGLADESH_DIAL_CODE):]
        return phone

    def enter_phone(self, phone):
        phone = self._normalize_phone_for_entry(phone)
        self.tap_optional("User Login", timeout=1)
        self.tap_optional("Mobile Number", timeout=1)
        self._select_bangladesh_country_code()
        el = self.driver.find_element(AppiumBy.XPATH, "//android.widget.EditText")
        el.clear()
        el.send_keys(phone)
        return self

    def accept_terms(self):
        self.tap_optional("By clicking continue")
        return self

    def tap_continue(self):
        self._hide_keyboard_optional()
        self.tap_optional("Send Verification Code")
        self.tap_optional("Continue")
        if "Send Verification Code" in self.driver.page_source:
            self._tap_primary_phone_button_by_position()
        wait_for_animation(self.driver, 2)
        return self

    def enter_otp(self, otp="1234"):
        fields = self.driver.find_elements(AppiumBy.XPATH, "//android.widget.EditText")
        if not fields:
            raise AssertionError("OTP input field was not available")
        fields[0].click()
        wait_for_animation(self.driver, 0.4)
        self._type_with_android_keycodes(otp)
        wait_for_animation(self.driver, 0.8)
        return self

    def tap_verify(self):
        if self._is_logged_in():
            return self
        self._hide_keyboard_optional()
        if self.is_visible("Verify Code", timeout=2):
            self.tap("Verify Code")
        elif self._is_logged_in():
            return self
        else:
            self.tap("Verify")
        wait_for_animation(self.driver, 3)
        return self

    def _is_logged_in(self):
        return (
            self.is_visible("Cart", timeout=1)
            or self.is_visible("My Orders", timeout=1)
            or self.is_visible("Home", timeout=1)
            or self.is_visible("Categories", timeout=1)
        )

    def login_phone_only(self, phone=DEFAULT_PHONE):
        """Enter phone and tap Continue but stop before OTP. Used by negative OTP tests."""
        self.enter_phone(phone)
        self.accept_terms()
        self.tap_continue()
        return self

    def login(self, phone=DEFAULT_PHONE, otp=DEFAULT_OTP):
        self.select_country_and_language()
        self.skip_onboarding()
        self.enter_phone(phone)
        self.accept_terms()
        self.tap_continue()
        self.enter_otp(otp)
        self.tap_verify()
        return self

    def assert_logged_in(self):
        assert self._is_logged_in(), \
            "Login failed — expected to see a logged-in home, cart, or orders screen after login"
        return self
