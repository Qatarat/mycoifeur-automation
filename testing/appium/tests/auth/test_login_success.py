import pytest

from pages.login_page import LoginPage
from test_data import ValidData


@pytest.mark.auth
@pytest.mark.android
class TestLoginSuccess:
    def test_login_with_bangladesh_country_search(self, driver):
        login = LoginPage(driver)
        login.login(ValidData.PHONE, ValidData.OTP)
        login.assert_logged_in()
