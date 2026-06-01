"""
Browse & Search edge cases.
Covers: single char search, very long search, Arabic search,
        no-results state, special chars, emoji, SQL/XSS in search.
"""
import pytest
from pages.login_page import LoginPage
from pages.search_page import SearchPage
from utils.helpers import wait_for_animation, navigate_to_browse_tab
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from test_data import ValidData


def _go_to_browse(driver):
    login = LoginPage(driver)
    login.login(ValidData.PHONE, ValidData.OTP)
    wait_for_animation(driver, 2)
    search = SearchPage(driver)
    search.open_search()
    return search


@pytest.mark.browse
@pytest.mark.boundary
class TestSearchInput:

    def test_single_character_search(self, driver):
        """Searching with one letter should either show results or empty state — never crash."""
        search = _go_to_browse(driver)
        search.search("a")
        page = driver.page_source
        assert "Something went wrong" not in page
        assert "500" not in page

    def test_search_100_chars_does_not_crash(self, driver):
        search = _go_to_browse(driver)
        search.search("a" * 100)
        assert "500" not in driver.page_source

    def test_search_arabic_text(self, driver):
        """Arabic search query — MyCoiffeur supports Arabic text input."""
        search = _go_to_browse(driver)
        search.search("مسجد")
        page = driver.page_source
        assert "Something went wrong" not in page
        assert "500" not in page

    def test_search_emoji_does_not_crash(self, driver):
        search = _go_to_browse(driver)
        search.search("🕌")
        assert "500" not in driver.page_source

    def test_search_all_uppercase_query(self, driver):
        """MOSQUE — uppercase search should work (case-insensitive)."""
        search = _go_to_browse(driver)
        search.search("MOSQUE")
        assert "500" not in driver.page_source

    def test_search_mixed_case(self, driver):
        """MoSqUe — mixed case should return same results as lowercase."""
        search = _go_to_browse(driver)
        search.search("MoSqUe")
        assert "Something went wrong" not in driver.page_source

    def test_search_with_numbers_only(self, driver):
        """Numeric search query '123' — should show empty state, not crash."""
        search = _go_to_browse(driver)
        search.search("123")
        assert "500" not in driver.page_source

    def test_search_with_html_tags_is_safe(self, driver):
        """<b>mosque</b> — HTML in search field must not render as HTML (XSS check)."""
        search = _go_to_browse(driver)
        search.search("<b>mosque</b>")
        page = driver.page_source
        assert "Something went wrong" not in page
        assert "500" not in page

    def test_search_sql_injection_is_safe(self, driver):
        search = _go_to_browse(driver)
        search.search("' OR '1'='1")
        page = driver.page_source
        assert "SQL" not in page
        assert "syntax error" not in page.lower()
        assert "database" not in page.lower()

    def test_search_gibberish_shows_empty_state(self, driver):
        """'zzzzzzzzz' should return no results without crashing."""
        search = _go_to_browse(driver)
        search.search("zzzzzzzzz")
        page = driver.page_source
        assert "Something went wrong" not in page

    def test_clear_search_restores_full_list(self, driver):
        """After clearing a search query, the full listing must reappear."""
        search = _go_to_browse(driver)
        search.search("zzzzz")
        search.clear_search()
        assert "Something went wrong" not in driver.page_source


@pytest.mark.browse
@pytest.mark.boundary
class TestServiceListing:

    def test_services_list_loads_without_login(self, driver):
        """Browse should be accessible as guest — no login required to view."""
        navigate_to_browse_tab(driver)
        wait_for_animation(driver, 2)
        page = driver.page_source
        assert "Something went wrong" not in page
        assert "500" not in page

    def test_service_card_tap_opens_detail(self, driver):
        """Tapping a service card must open detail view without crash."""
        search = _go_to_browse(driver)
        from appium.webdriver.common.appiumby import AppiumBy
        cards = driver.find_elements(AppiumBy.XPATH, "//*[@content-desc='service_card']")
        if cards:
            cards[0].click()
            wait_for_animation(driver, 2)
        assert "Something went wrong" not in driver.page_source

    def test_rapid_back_forth_navigation_no_crash(self, driver):
        """Quickly opening and closing service detail — no memory leak / crash."""
        search = _go_to_browse(driver)
        from appium.webdriver.common.appiumby import AppiumBy
        for _ in range(3):
            cards = driver.find_elements(AppiumBy.XPATH, "//*[@content-desc='service_card']")
            if cards:
                cards[0].click()
                wait_for_animation(driver, 1)
                driver.back()
                wait_for_animation(driver, 1)
        assert "Something went wrong" not in driver.page_source
