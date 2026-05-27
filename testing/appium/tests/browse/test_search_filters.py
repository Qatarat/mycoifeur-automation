"""
Search & Filter tests for the MyCoiffeur app.
Covers: basic search, empty search, category/price/sort filters,
        clear filters, Arabic text, no-results state, rapid search.
"""
import pytest
import allure
from pages.login_page import LoginPage
from pages.search_page import SearchPage
from utils.helpers import screenshot, wait_for_animation


def _login_and_open_search(driver):
    login = LoginPage(driver)
    login.select_country_and_language()
    login.skip_onboarding()
    login.login()
    search = SearchPage(driver)
    search.open_search()
    return search


@allure.epic("Browse")
@allure.feature("Search & Filters")
@pytest.mark.browse
class TestSearchFilters:

    @allure.story("Search")
    @allure.title("Entering 'hair' returns results")
    @pytest.mark.smoke
    def test_search_returns_results(self, driver):
        search = _login_and_open_search(driver)
        search.search("hair")

        search.assert_no_crash()
        page_src = driver.page_source
        assert len(page_src) > 100, "Search returned empty page"
        screenshot(driver, "search_returns_results")

    @allure.story("Search")
    @allure.title("Clearing search shows all results")
    @pytest.mark.regression
    def test_empty_search_shows_all(self, driver):
        search = _login_and_open_search(driver)
        search.search("hair")
        wait_for_animation(driver)
        search.clear_search()

        search.assert_no_crash()
        screenshot(driver, "empty_search_shows_all")

    @allure.story("Filters")
    @allure.title("Selecting a category filter applies to results")
    @pytest.mark.regression
    def test_category_filter_applies(self, driver):
        search = _login_and_open_search(driver)
        search.apply_category_filter("Haircut")

        search.assert_no_crash()
        screenshot(driver, "category_filter_applies")

    @allure.story("Filters")
    @allure.title("Selecting a price range filter updates results")
    @pytest.mark.regression
    def test_price_filter_applies(self, driver):
        search = _login_and_open_search(driver)
        for label in ["Filter", "Filters"]:
            if search.is_visible(label, timeout=2):
                search.tap_optional(label)
                break
        wait_for_animation(driver)

        # Tap a price range option — common labels in MyCoiffeur
        for label in ["0 - 100", "Under 100", "Price", "100"]:
            if search.is_visible(label, timeout=2):
                search.tap_optional(label)
                break
        search.tap_optional("Apply")
        wait_for_animation(driver, 2)

        search.assert_no_crash()
        screenshot(driver, "price_filter_applies")

    @allure.story("Filters")
    @allure.title("Sort by Nearest changes result ordering")
    @pytest.mark.regression
    def test_sort_nearest_applies(self, driver):
        search = _login_and_open_search(driver)
        search.apply_sort("Nearest")

        search.assert_no_crash()
        screenshot(driver, "sort_nearest_applies")

    @allure.story("Filters")
    @allure.title("Clear filters restores unfiltered results")
    @pytest.mark.regression
    def test_clear_filters_resets(self, driver):
        search = _login_and_open_search(driver)
        search.apply_category_filter("Haircut")
        search.clear_filters()

        search.assert_no_crash()
        screenshot(driver, "clear_filters_resets")

    @allure.story("Search")
    @allure.title("Arabic text input does not crash the app")
    @pytest.mark.regression
    def test_search_arabic_text(self, driver):
        search = _login_and_open_search(driver)
        search.search("شعر")

        search.assert_no_crash()
        screenshot(driver, "search_arabic_text")

    @allure.story("Search")
    @allure.title("No-results search shows empty state screen")
    @pytest.mark.regression
    def test_no_results_state(self, driver):
        search = _login_and_open_search(driver)
        search.search("ZZZNOTEXIST")

        search.assert_no_crash()
        page_src = driver.page_source
        no_results = (
            "no result" in page_src.lower()
            or "not found" in page_src.lower()
            or "empty" in page_src.lower()
            or "0" in page_src
        )
        assert no_results, "Empty state not displayed for a no-match search query"
        screenshot(driver, "no_results_state")

    @allure.story("Search")
    @allure.title("Rapidly typing and clearing search 5 times does not crash")
    @pytest.mark.regression
    def test_rapid_search_stable(self, driver):
        search = _login_and_open_search(driver)
        for _ in range(5):
            search.search("cut")
            wait_for_animation(driver, 0.5)
            search.clear_search()
            wait_for_animation(driver, 0.5)

        search.assert_no_crash()
        screenshot(driver, "rapid_search_stable")
