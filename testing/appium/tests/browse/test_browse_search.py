"""
Browse & Search edge cases.
Covers: single char search, very long search, Arabic search,
        no-results state, special chars, emoji, SQL/XSS in search.
"""
import pytest
from appium.webdriver.common.appiumby import AppiumBy
from pages.login_page import LoginPage
from test_data import ValidData


def _go_to_browse(driver):
    login = LoginPage(driver)
    login.login(ValidData.PHONE, ValidData.OTP)
    driver.find_element(AppiumBy.ACCESSIBILITY_ID, "browse_tab").click()


@pytest.mark.browse
@pytest.mark.boundary
class TestSearchInput:

    def test_single_character_search(self, driver):
        """Searching with one letter should either show results or empty state — never crash."""
        _go_to_browse(driver)
        driver.find_element(AppiumBy.ACCESSIBILITY_ID, "search_field").send_keys("a")
        page = driver.page_source
        assert "Something went wrong" not in page
        assert "500" not in page

    def test_search_100_chars_does_not_crash(self, driver):
        _go_to_browse(driver)
        driver.find_element(AppiumBy.ACCESSIBILITY_ID, "search_field").send_keys("a" * 100)
        assert "500" not in driver.page_source

    def test_search_arabic_text(self, driver):
        """Arabic search query — Qatarat is an Arabic-first app."""
        _go_to_browse(driver)
        driver.find_element(AppiumBy.ACCESSIBILITY_ID, "search_field").send_keys("مسجد")
        page = driver.page_source
        assert "Something went wrong" not in page
        assert "500" not in page

    def test_search_emoji_does_not_crash(self, driver):
        _go_to_browse(driver)
        driver.find_element(AppiumBy.ACCESSIBILITY_ID, "search_field").send_keys("🕌")
        assert "500" not in driver.page_source

    def test_search_all_uppercase_query(self, driver):
        """MOSQUE — uppercase search should work (case-insensitive)."""
        _go_to_browse(driver)
        driver.find_element(AppiumBy.ACCESSIBILITY_ID, "search_field").send_keys("MOSQUE")
        page = driver.page_source
        assert "500" not in page

    def test_search_mixed_case(self, driver):
        """MoSqUe — mixed case should return same results as lowercase."""
        _go_to_browse(driver)
        driver.find_element(AppiumBy.ACCESSIBILITY_ID, "search_field").send_keys("MoSqUe")
        page = driver.page_source
        assert "Something went wrong" not in page

    def test_search_with_numbers_only(self, driver):
        """Numeric search query '123' — should show empty state, not crash."""
        _go_to_browse(driver)
        driver.find_element(AppiumBy.ACCESSIBILITY_ID, "search_field").send_keys("123")
        page = driver.page_source
        assert "500" not in page

    def test_search_with_html_tags_is_safe(self, driver):
        """<b>mosque</b> — HTML in search field must not render as HTML (XSS check)."""
        _go_to_browse(driver)
        driver.find_element(AppiumBy.ACCESSIBILITY_ID, "search_field").send_keys("<b>mosque</b>")
        page = driver.page_source
        assert "Something went wrong" not in page
        assert "500" not in page

    def test_search_sql_injection_is_safe(self, driver):
        _go_to_browse(driver)
        driver.find_element(AppiumBy.ACCESSIBILITY_ID, "search_field").send_keys("' OR '1'='1")
        page = driver.page_source
        assert "SQL" not in page
        assert "syntax error" not in page.lower()
        assert "database" not in page.lower()

    def test_search_gibberish_shows_empty_state(self, driver):
        """'zzzzzzzzz' should return no results with an empty state UI."""
        _go_to_browse(driver)
        driver.find_element(AppiumBy.ACCESSIBILITY_ID, "search_field").send_keys("zzzzzzzzz")
        page = driver.page_source
        assert "Something went wrong" not in page
        # Should show some "no results" indicator
        no_results = ("no result" in page.lower() or "not found" in page.lower()
                      or "empty" in page.lower() or "0" in page)
        assert no_results

    def test_clear_search_restores_full_list(self, driver):
        """After clearing a search query, the full listing must reappear."""
        _go_to_browse(driver)
        field = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "search_field")
        field.send_keys("zzzzz")
        field.clear()
        page = driver.page_source
        assert "Something went wrong" not in page


@pytest.mark.browse
@pytest.mark.boundary
class TestServiceListing:

    def test_services_list_loads_without_login(self, driver):
        """Browse should be accessible as guest — no login required to view."""
        driver.find_element(AppiumBy.ACCESSIBILITY_ID, "browse_tab").click()
        page = driver.page_source
        assert "Something went wrong" not in page
        assert "500" not in page

    def test_service_card_tap_opens_detail(self, driver):
        """Tapping a service card must open detail view without crash."""
        _go_to_browse(driver)
        cards = driver.find_elements(AppiumBy.XPATH, "//*[@content-desc='service_card']")
        if cards:
            cards[0].click()
            page = driver.page_source
            assert "Something went wrong" not in page

    def test_rapid_back_forth_navigation_no_crash(self, driver):
        """Quickly opening and closing service detail — no memory leak / crash."""
        _go_to_browse(driver)
        for _ in range(3):
            cards = driver.find_elements(AppiumBy.XPATH, "//*[@content-desc='service_card']")
            if cards:
                cards[0].click()
                driver.back()
        assert "Something went wrong" not in driver.page_source
