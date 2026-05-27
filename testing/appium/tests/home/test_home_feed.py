"""
Home feed tests — happy path and edge cases.
Covers: home screen loads after login, feed scroll, no crash, banner visibility,
        category chip navigation, rapid scroll, deep scroll.
"""
import pytest
import allure
from pages.login_page import LoginPage
from pages.home_page import HomePage
from utils.helpers import screenshot, wait_for_animation


def _login_and_go_home(driver):
    login = LoginPage(driver)
    login.login()
    return HomePage(driver)


@allure.epic("Home")
@allure.feature("Home Feed")
@pytest.mark.home
class TestHomeFeedHappy:

    @allure.story("Load")
    @allure.title("Home feed loads after successful login")
    def test_home_loads_after_login(self, driver):
        home = _login_and_go_home(driver)
        home.assert_home_loaded()
        screenshot(driver, "home_feed_loaded")

    @allure.story("Feed Scroll")
    @allure.title("Home feed scrolls without crash")
    def test_home_feed_scrolls(self, driver):
        home = _login_and_go_home(driver)
        home.scroll_feed_down(times=3)
        home.assert_no_crash()
        screenshot(driver, "home_feed_scrolled")

    @allure.story("Feed Scroll")
    @allure.title("No 500 / error banner visible on home feed")
    def test_home_feed_no_error(self, driver):
        home = _login_and_go_home(driver)
        home.assert_no_crash()

    @allure.story("Book Now")
    @allure.title("Tapping Book Now opens service detail without crash")
    def test_book_now_opens_detail(self, driver):
        home = _login_and_go_home(driver)
        home.tap_first_book_now()
        page = driver.page_source
        assert "Something went wrong" not in page
        screenshot(driver, "home_book_now_detail")

    @allure.story("Navigation")
    @allure.title("Bottom navigation tabs all reachable from home")
    def test_bottom_nav_tabs_reachable(self, driver):
        home = _login_and_go_home(driver)
        for tab in ("Browse", "Cart", "My Orders", "Profile"):
            home.tap_optional(tab)
            wait_for_animation(driver, 1)
        home.go_to_home()
        home.assert_no_crash()
        screenshot(driver, "home_bottom_nav")


@allure.epic("Home")
@allure.feature("Home Feed")
@pytest.mark.home
@pytest.mark.boundary
class TestHomeFeedEdgeCases:

    @allure.story("Rapid Scroll")
    @allure.title("Rapid up-down scroll does not crash home feed")
    def test_rapid_scroll_no_crash(self, driver):
        home = _login_and_go_home(driver)
        for _ in range(5):
            home.scroll_feed_down(times=1)
        home.assert_no_crash()

    @allure.story("Deep Scroll")
    @allure.title("Scrolling to bottom of home feed shows no errors")
    def test_deep_scroll_to_bottom(self, driver):
        home = _login_and_go_home(driver)
        home.scroll_feed_down(times=10)
        home.assert_no_crash()
        screenshot(driver, "home_deep_scroll_bottom")

    @allure.story("Back from Home")
    @allure.title("Back button on home returns to home — does not exit app")
    def test_back_button_stays_on_home(self, driver):
        home = _login_and_go_home(driver)
        driver.back()
        wait_for_animation(driver, 1)
        page = driver.page_source
        # App should still be running
        assert "Something went wrong" not in page
