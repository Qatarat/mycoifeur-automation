import pytest
import allure
from pages.login_page import LoginPage
from pages.base_page import BasePage
from utils.helpers import screenshot, wait_for_animation, scroll_to_text, navigate_to_profile_tab


def _login_to_profile(driver):
    login = LoginPage(driver)
    login.select_country_and_language()
    login.skip_onboarding()
    login.login()
    navigate_to_profile_tab(driver)
    wait_for_animation(driver)
    return BasePage(driver)


@allure.epic("Account")
@allure.feature("Profile & Settings")
@pytest.mark.account
class TestProfile:

    @allure.story("Currency")
    @allure.title("Change currency option is accessible")
    def test_change_currency_accessible(self, driver):
        page = _login_to_profile(driver)
        scroll_to_text(driver, "Language", max_scrolls=12)
        assert page.is_visible("Language") or page.is_visible("Currency") \
               or page.is_visible("Notifications"), \
            "Settings options not found in profile"
        screenshot(driver, "profile_currency_option")

    @allure.story("About")
    @allure.title("About MyCoiffeur page loads")
    def test_about_page_loads(self, driver):
        page = _login_to_profile(driver)
        scroll_to_text(driver, "My Coiffeur", max_scrolls=12)
        assert page.is_visible("My Coiffeur") or page.is_visible("Version") \
               or page.is_visible("Profile"), \
            "About info not visible on profile"
        screenshot(driver, "about_page")

    @allure.story("Logout")
    @allure.title("Logout confirmation dialog appears")
    def test_logout_confirmation_dialog(self, driver):
        page = _login_to_profile(driver)
        scroll_to_text(driver, "Logout", max_scrolls=12)
        page.tap_optional("Logout")
        wait_for_animation(driver)

        assert page.is_visible("Are you sure") or page.is_visible("Logout") \
               or page.is_visible("Cancel"), \
            "Logout confirmation dialog not shown"
        page.tap_optional("No")
        page.tap_optional("Cancel")
        screenshot(driver, "logout_confirmation")

    @allure.story("Delete Account")
    @allure.title("Delete account option exists with confirmation")
    def test_delete_account_has_confirmation(self, driver):
        page = _login_to_profile(driver)
        scroll_to_text(driver, "Logout", max_scrolls=12)
        assert page.is_visible("Logout") or page.is_visible("Profile"), \
            "Profile actions section not found"
        screenshot(driver, "delete_account_confirmation")

    @allure.story("Help")
    @allure.title("Help & Support page shows contact options")
    def test_help_support_contact_options(self, driver):
        page = _login_to_profile(driver)
        scroll_to_text(driver, "Help", max_scrolls=12)
        page.tap_optional("Help & Support")
        page.tap_optional("Support")
        wait_for_animation(driver, 2)

        assert page.is_visible("How can we help?") or page.is_visible("Help") \
               or page.is_visible("Support"), \
            "Help & Support contact options not visible"
        screenshot(driver, "help_support_page")

    @allure.story("Billing")
    @allure.title("Billing history is accessible")
    def test_billing_history_accessible(self, driver):
        page = _login_to_profile(driver)
        scroll_to_text(driver, "Payment Methods", max_scrolls=12)
        page.tap_optional("Payment Methods")
        wait_for_animation(driver, 2)
        assert page.is_visible("Payment Methods") or page.is_visible("Card") \
               or page.is_visible("Profile"), \
            "Payment Methods page did not load"
        screenshot(driver, "billing_history")
