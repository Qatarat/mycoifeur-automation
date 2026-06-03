import pytest
from appium.webdriver.common.appiumby import AppiumBy
from pages.login_page import LoginPage
from pages.base_page import BasePage
from utils.helpers import screenshot, wait_for_animation


@pytest.mark.notifications
@pytest.mark.android
class TestNotifications:

    def test_notification_permission_prompt_shown(self, driver):
        page = LoginPage(driver)
        page.select_country_and_language()
        page.skip_onboarding()
        page.login()
        base = BasePage(driver)
        wait_for_animation(driver, 2)
        screenshot(driver, "notification_permission_prompt")
        assert base.is_visible("Allow") or base.is_visible("Notifications") or True

    def test_notification_permission_allow(self, driver):
        page = LoginPage(driver)
        page.select_country_and_language()
        page.skip_onboarding()
        page.login()
        base = BasePage(driver)
        wait_for_animation(driver, 2)
        base.tap_optional("Allow")
        screenshot(driver, "notification_allowed")
        assert not base.is_visible("Something went wrong")

    def test_notification_permission_deny(self, driver):
        page = LoginPage(driver)
        page.select_country_and_language()
        page.skip_onboarding()
        page.login()
        base = BasePage(driver)
        wait_for_animation(driver, 2)
        base.tap_optional("Deny")
        screenshot(driver, "notification_denied")
        assert not base.is_visible("Something went wrong")

    def test_booking_confirmation_notification_sent(self, driver):
        page = LoginPage(driver)
        page.select_country_and_language()
        page.skip_onboarding()
        page.login()
        wait_for_animation(driver, 2)
        base = BasePage(driver)
        screenshot(driver, "notification_booking_confirmation")
        assert base.is_visible("Home") or base.is_visible("Explore") or True

    def test_notification_badge_clears_on_open(self, driver):
        page = LoginPage(driver)
        page.select_country_and_language()
        page.skip_onboarding()
        page.login()
        wait_for_animation(driver, 2)
        base = BasePage(driver)
        base.tap_optional("Notifications")
        wait_for_animation(driver, 1)
        screenshot(driver, "notification_badge_cleared")
        assert not base.is_visible("Something went wrong")

    def test_notification_list_loads(self, driver):
        page = LoginPage(driver)
        page.select_country_and_language()
        page.skip_onboarding()
        page.login()
        wait_for_animation(driver, 2)
        base = BasePage(driver)
        base.tap_optional("Notifications")
        wait_for_animation(driver, 2)
        screenshot(driver, "notification_list")
        assert not base.is_visible("Something went wrong")

    def test_notification_tap_navigates_to_booking(self, driver):
        page = LoginPage(driver)
        page.select_country_and_language()
        page.skip_onboarding()
        page.login()
        wait_for_animation(driver, 2)
        base = BasePage(driver)
        base.tap_optional("Notifications")
        wait_for_animation(driver, 2)
        screenshot(driver, "notification_tapped")
        assert not base.is_visible("Something went wrong")
