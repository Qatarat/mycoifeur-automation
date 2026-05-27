from pages import login_page as login_page_module
from pages.login_page import LoginPage


class FakeElement:
    def __init__(self):
        self.cleared = False
        self.typed = []
        self.text = ""

    def clear(self):
        self.cleared = True
        self.text = ""

    def send_keys(self, value):
        self.typed.append(value)
        self.text += value


class FakeDriver:
    def __init__(self):
        self.country_search = FakeElement()
        self.phone_input = FakeElement()
        self.page_source = ""

    def find_elements(self, by, value):
        return [self.country_search]

    def find_element(self, by, value):
        return self.phone_input

    def implicitly_wait(self, timeout):
        return None


def test_enter_phone_selects_bangladesh_code_before_typing(monkeypatch):
    driver = FakeDriver()
    page = LoginPage.__new__(LoginPage)
    page.driver = driver
    calls = []

    monkeypatch.setattr(login_page_module, "wait_for_animation", lambda *args, **kwargs: None)
    monkeypatch.setattr(page, "is_visible", lambda text, timeout=5: False)
    monkeypatch.setattr(page, "_open_country_code_selector", lambda: calls.append(("open_country_selector", None)))
    monkeypatch.setattr(page, "_tap_bangladesh_result_by_text", lambda: False)
    monkeypatch.setattr(page, "_tap_bangladesh_with_scrollable", lambda: False)

    def tap_first_country_result(field):
        calls.append(("tap_first_country_result", None))
        driver.page_source = "+880"

    monkeypatch.setattr(page, "_tap_first_country_result", tap_first_country_result)
    monkeypatch.setattr(page, "_assert_bangladesh_selected", lambda: calls.append(("assert_country_selected", None)))
    monkeypatch.setattr(page, "tap", lambda text: calls.append(("tap", text)) or page)
    monkeypatch.setattr(page, "tap_optional", lambda text, timeout=1: calls.append(("tap_optional", text)) or page)

    page.enter_phone("1316314566")

    assert ("open_country_selector", None) in calls
    assert ("tap_first_country_result", None) in calls
    assert driver.country_search.cleared is True
    assert driver.country_search.typed == ["Bangladesh"]
    assert driver.phone_input.cleared is True
    assert driver.phone_input.typed == ["1316314566"]
