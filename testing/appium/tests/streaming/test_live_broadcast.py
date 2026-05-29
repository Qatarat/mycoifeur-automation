import pytest
from pages.login_page import LoginPage
from pages.base_page import BasePage
from utils.helpers import screenshot, wait_for_animation


@pytest.mark.android
class TestLiveBroadcast:
    """
    Agora RTC live streaming flow tests.
    These are view/interaction tests — actual stream content is not verified.
    """

    def test_live_broadcast_screen_accessible(self, driver):
        """Live Broadcast option must not cause a 500 error."""
        login = LoginPage(driver)
        login.select_country_and_language()
        login.skip_onboarding()
        login.login()

        page = BasePage(driver)
        page.tap_optional("Live Broadcast")
        wait_for_animation(driver, 3)

        assert "500" not in driver.page_source, \
            "500 error on Live Broadcast screen"
        screenshot(driver, "live_broadcast_screen")

    def test_visual_documentation_section_loads(self, driver):
        """Visual documentations tab must not cause a 500 error."""
        login = LoginPage(driver)
        login.select_country_and_language()
        login.skip_onboarding()
        login.login()

        page = BasePage(driver)
        page.tap_optional("Visual documentations")
        wait_for_animation(driver, 3)

        assert "500" not in driver.page_source, \
            "500 error on Visual Documentations screen"
        screenshot(driver, "visual_documentation_section")

    def test_live_broadcast_permissions_requested(self, driver):
        """Joining a live stream must not cause a 500 error."""
        login = LoginPage(driver)
        login.select_country_and_language()
        login.skip_onboarding()
        login.login()

        page = BasePage(driver)
        page.tap_optional("Live Broadcast")
        wait_for_animation(driver, 2)

        from appium.webdriver.common.appiumby import AppiumBy
        streams = driver.find_elements(AppiumBy.XPATH, "//android.widget.ImageView")
        if streams:
            streams[0].click()
            wait_for_animation(driver, 3)
            screenshot(driver, "live_broadcast_join_attempt")
        else:
            pytest.skip("No live streams available in stage environment")

        assert "500" not in driver.page_source, \
            "500 error when joining a live stream"
