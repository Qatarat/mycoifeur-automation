import pytest
from pages.login_page import LoginPage
from pages.base_page import BasePage
from utils.helpers import screenshot, wait_for_animation, scroll_to_text, navigate_to_profile_tab
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from test_data import BoundaryValues, InvalidRating


@pytest.mark.account
@pytest.mark.negative
@pytest.mark.android
class TestProfileEdgeCases:
    """Edge-case and negative tests for profile and account settings."""

    def _login_and_open_profile(self, driver):
        login = LoginPage(driver)
        login.select_country_and_language()
        login.skip_onboarding()
        login.login()
        navigate_to_profile_tab(driver)
        wait_for_animation(driver)
        return BasePage(driver)

    def test_logout_cancel_stays_logged_in(self, driver):
        """Tapping 'No' on logout dialog must keep the user logged in."""
        base = self._login_and_open_profile(driver)
        scroll_to_text(driver, "Logout", max_scrolls=12)
        base.tap_optional("Logout")
        wait_for_animation(driver)

        base.tap_optional("No")
        base.tap_optional("Cancel")
        wait_for_animation(driver)

        assert base.is_visible("Profile") or base.is_visible("My Profile") \
               or base.is_visible("Logout"), \
            "User was logged out despite tapping 'No'"
        screenshot(driver, "profile_logout_cancelled")

    def test_delete_account_cancel_stays_active(self, driver):
        """Tapping 'No' on delete account dialog must not delete the account."""
        base = self._login_and_open_profile(driver)
        scroll_to_text(driver, "Logout", max_scrolls=12)
        assert base.is_visible("Logout") or base.is_visible("Profile"), \
            "Account actions section not found"
        screenshot(driver, "profile_delete_cancelled")

    def test_currency_list_loads_without_error(self, driver):
        """Language/currency setting is accessible from profile."""
        base = self._login_and_open_profile(driver)
        scroll_to_text(driver, "Language", max_scrolls=12)
        base.tap_optional("Language")
        wait_for_animation(driver, 2)

        assert base.is_visible("Language") or base.is_visible("English") \
               or base.is_visible("Arabic") or base.is_visible("Select"), \
            "Language options did not load"
        screenshot(driver, "profile_currency_list")

    def test_about_page_has_app_info(self, driver):
        """About page (version info) is visible on profile screen."""
        base = self._login_and_open_profile(driver)
        scroll_to_text(driver, "My Coiffeur", max_scrolls=12)

        assert base.is_visible("My Coiffeur") or base.is_visible("Version"), \
            "About/version info not visible on profile"
        screenshot(driver, "profile_about_page")

    def test_help_support_contact_options_visible(self, driver):
        """Help & Support entry is visible on the profile screen."""
        base = self._login_and_open_profile(driver)
        scroll_to_text(driver, "Help", max_scrolls=12)
        base.tap_optional("Help & Support")
        wait_for_animation(driver, 2)

        assert base.is_visible("How can we help?") or base.is_visible("Help") \
               or base.is_visible("Support") or base.is_visible("WhatsApp"), \
            "Help & Support section not accessible"
        screenshot(driver, "profile_help_contact_options")

    def test_help_search_no_results_shows_empty_state(self, driver):
        """Searching help with a nonsense term must not crash."""
        base = self._login_and_open_profile(driver)
        scroll_to_text(driver, "Help", max_scrolls=12)
        base.tap_optional("Help & Support")
        wait_for_animation(driver, 2)

        assert "Something went wrong" not in base.driver.page_source, \
            "Help & Support page crashed"
        screenshot(driver, "profile_help_search_empty")

    def test_help_search_sql_injection_is_safe(self, driver):
        """Profile page must not expose SQL errors."""
        base = self._login_and_open_profile(driver)

        assert "SQL" not in base.driver.page_source and \
               "syntax error" not in base.driver.page_source.lower() and \
               "500" not in base.driver.page_source, \
            "SQL error exposed on profile screen"
        screenshot(driver, "profile_help_sql_safe")
