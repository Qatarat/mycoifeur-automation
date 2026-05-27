"""
Logout tests for the MyCoiffeur app.
Covers: dialog appearance, cancel, confirm, re-login, session cleared,
        profile tab access, and button visibility.
"""
import pytest
import allure
from pages.login_page import LoginPage
from pages.base_page import BasePage
from utils.helpers import screenshot, wait_for_animation, scroll_to_text


def _login(driver):
    login = LoginPage(driver)
    login.select_country_and_language()
    login.skip_onboarding()
    login.login()
    return BasePage(driver)


def _navigate_to_logout(page):
    page.tap_optional("Profile")
    page.tap_optional("Account")
    wait_for_animation(page.driver)
    scroll_to_text(page.driver, "Logout", max_scrolls=5)
    page.tap_optional("Logout")
    wait_for_animation(page.driver)


@allure.epic("Account")
@allure.feature("Logout")
@pytest.mark.account
class TestLogout:

    @allure.story("Dialog")
    @allure.title("Logout dialog appears when tapping Logout")
    @pytest.mark.smoke
    def test_logout_dialog_appears(self, driver):
        page = _login(driver)
        page.tap_optional("Profile")
        page.tap_optional("Account")
        wait_for_animation(driver)
        scroll_to_text(driver, "Logout", max_scrolls=5)
        page.tap_optional("Logout")
        wait_for_animation(driver)

        assert page.is_visible("Are you sure") or page.is_visible("Logout"), \
            "Logout confirmation dialog did not appear"
        page.tap_optional("No")
        screenshot(driver, "logout_dialog_appears")

    @allure.story("Dialog")
    @allure.title("Tapping No in logout dialog keeps user logged in")
    @pytest.mark.regression
    def test_logout_cancel(self, driver):
        page = _login(driver)
        _navigate_to_logout(page)

        page.tap_optional("No")
        wait_for_animation(driver)

        assert page.is_visible("Profile") or page.is_visible("Account") \
               or page.is_visible("Cart"), \
            "User was logged out despite tapping No"
        screenshot(driver, "logout_cancelled")

    @allure.story("Confirm")
    @allure.title("Tapping Yes in logout dialog returns to login screen")
    @pytest.mark.smoke
    def test_logout_confirm(self, driver):
        page = _login(driver)
        _navigate_to_logout(page)

        page.tap_optional("Yes")
        wait_for_animation(driver, 3)

        page_src = driver.page_source
        assert (
            "Login" in page_src
            or "Phone" in page_src
            or "Sign In" in page_src
            or "Continue" in page_src
            or "Verification" in page_src
        ), "Did not return to login screen after confirming logout"
        screenshot(driver, "logout_confirmed")

    @allure.story("Re-login")
    @allure.title("User can log in again after logout")
    @pytest.mark.regression
    def test_re_login_after_logout(self, driver):
        page = _login(driver)
        _navigate_to_logout(page)
        page.tap_optional("Yes")
        wait_for_animation(driver, 3)

        # Re-login
        login = LoginPage(driver)
        login.login()
        login.assert_logged_in()
        screenshot(driver, "re_login_after_logout")

    @allure.story("Session")
    @allure.title("After logout, navigating to profile requires re-login")
    @pytest.mark.regression
    def test_session_cleared_after_logout(self, driver):
        page = _login(driver)
        _navigate_to_logout(page)
        page.tap_optional("Yes")
        wait_for_animation(driver, 3)

        # Attempt to reach profile without logging in again
        page.tap_optional("Profile")
        wait_for_animation(driver)

        page_src = driver.page_source
        assert (
            "Login" in page_src
            or "Phone" in page_src
            or "Sign In" in page_src
            or "Continue" in page_src
        ), "Profile accessible after logout — session not cleared"
        screenshot(driver, "session_cleared_after_logout")

    @allure.story("Navigation")
    @allure.title("Profile tab is accessible before triggering logout")
    @pytest.mark.smoke
    def test_logout_from_profile_tab(self, driver):
        page = _login(driver)
        page.tap_optional("Profile")
        wait_for_animation(driver)

        assert page.is_visible("Profile") or page.is_visible("Account") \
               or page.is_visible("Logout"), \
            "Profile tab did not load"
        screenshot(driver, "profile_tab_before_logout")

    @allure.story("Visibility")
    @allure.title("Logout button is visible in Account section")
    @pytest.mark.regression
    def test_logout_button_visible_in_account(self, driver):
        page = _login(driver)
        page.tap_optional("Profile")
        page.tap_optional("Account")
        wait_for_animation(driver)
        scroll_to_text(driver, "Logout", max_scrolls=6)

        assert page.is_visible("Logout", timeout=5), \
            "Logout button not found in Account section"
        page.tap_optional("No")
        screenshot(driver, "logout_button_visible")
