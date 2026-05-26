from pages import login_page as login_page_module
from pages.login_page import LoginPage


class FakeElement:
    def __init__(self):
        self.cleared = False
        self.typed = []

    def clear(self):
        self.cleared = True

    def send_keys(self, value):
        self.typed.append(value)


class FakeDriver:
    def __init__(self):
        self.country_search = FakeElement()
        self.phone_input = FakeElement()

    def find_elements(self, by, value):
        return [self.country_search]

    def find_element(self, by, value):
        return self.phone_input


def test_enter_phone_selects_bangladesh_code_before_typing(monkeypatch):
    driver = FakeDriver()
    page = LoginPage.__new__(LoginPage)
    page.driver = driver
    calls = []

    monkeypatch.setattr(login_page_module, "wait_for_animation", lambda *args, **kwargs: None)
    monkeypatch.setattr(page, "is_visible", lambda text, timeout=5: False)
    monkeypatch.setattr(page, "tap", lambda text: calls.append(("tap", text)) or page)
    monkeypatch.setattr(page, "tap_optional", lambda text, timeout=1: calls.append(("tap_optional", text)) or page)

    page.enter_phone("8801316314566")

    assert calls[:2] == [("tap", "+966"), ("tap", "Bangladesh")]
    assert driver.country_search.cleared is True
    assert driver.country_search.typed == ["Bangladesh"]
    assert driver.phone_input.cleared is True
    assert driver.phone_input.typed == ["1316314566"]
