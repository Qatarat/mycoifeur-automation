"""
SearchPage — page object for the search & filter screen.
Covers: search bar input, category filter, price range filter,
        sort options, results list, and clear filters.
"""
from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage
from utils.helpers import wait_for_animation


class SearchPage(BasePage):

    # ── Locators ───────────────────────────────────────────────────────────────

    SEARCH_BAR_IDS = ["search_field", "search_bar", "search_input"]
    FILTER_BUTTON_LABELS = ["Filter", "Filters", "filter"]
    CLEAR_FILTERS_LABELS = ["Clear", "Clear Filters", "Reset", "Reset Filters"]
    SORT_BUTTON_LABELS = ["Sort", "Sort By", "sort_button"]
    RESULTS_XPATH = (
        '//*[@content-desc="result_item" or @content-desc="service_card" '
        'or @content-desc="salon_card" or @content-desc="provider_card"]'
    )

    # ── Navigation ─────────────────────────────────────────────────────────────

    def open_search(self):
        """Navigate to the search/browse screen and focus the search bar."""
        self.tap_optional("Browse")
        self.tap_optional("Search")
        wait_for_animation(self.driver)
        self._focus_search_bar()
        return self

    def _focus_search_bar(self):
        for aid in self.SEARCH_BAR_IDS:
            fields = self.driver.find_elements(AppiumBy.ACCESSIBILITY_ID, aid)
            if fields:
                fields[0].click()
                return
        # Fallback: tap first EditText
        fields = self.driver.find_elements(AppiumBy.XPATH, "//android.widget.EditText")
        if fields:
            fields[0].click()

    def _get_search_field(self):
        for aid in self.SEARCH_BAR_IDS:
            els = self.driver.find_elements(AppiumBy.ACCESSIBILITY_ID, aid)
            if els:
                return els[0]
        els = self.driver.find_elements(AppiumBy.XPATH, "//android.widget.EditText")
        return els[0] if els else None

    # ── Actions ─────────────────────────────────────────────────────────────────

    def search(self, query: str):
        """Type *query* into the search bar and wait for results."""
        self._focus_search_bar()
        field = self._get_search_field()
        if field:
            field.clear()
            field.send_keys(query)
        wait_for_animation(self.driver, 2)
        return self

    def clear_search(self):
        """Clear the search bar contents."""
        field = self._get_search_field()
        if field:
            field.clear()
        wait_for_animation(self.driver, 2)
        return self

    def apply_category_filter(self, name: str):
        """Tap the filter button then select a category chip by name."""
        for label in self.FILTER_BUTTON_LABELS:
            if self.is_visible(label, timeout=2):
                self.tap_optional(label)
                break
        wait_for_animation(self.driver)
        self.tap_optional(name)
        wait_for_animation(self.driver, 2)
        return self

    def apply_sort(self, option: str):
        """Open sort sheet and select *option* (e.g. 'Nearest', 'Price: Low to High')."""
        for label in self.SORT_BUTTON_LABELS:
            if self.is_visible(label, timeout=2):
                self.tap_optional(label)
                break
        wait_for_animation(self.driver)
        self.tap_optional(option)
        wait_for_animation(self.driver, 2)
        return self

    def clear_filters(self):
        """Tap Clear Filters / Reset to restore full results."""
        for label in self.CLEAR_FILTERS_LABELS:
            if self.is_visible(label, timeout=2):
                self.tap_optional(label)
                wait_for_animation(self.driver, 2)
                return self
        return self

    # ── Data retrieval ─────────────────────────────────────────────────────────

    def get_results_count(self) -> int:
        """Return the number of visible result items."""
        try:
            items = self.driver.find_elements(AppiumBy.XPATH, self.RESULTS_XPATH)
            return len(items)
        except Exception:
            return 0

    # ── Assertions ─────────────────────────────────────────────────────────────

    def assert_no_crash(self):
        page = self.driver.page_source
        assert "Something went wrong" not in page, "Crash banner visible on search screen"
        assert "500" not in page, "500 error visible on search screen"
        return self

    def assert_empty_state_visible(self):
        page = self.driver.page_source
        assert (
            "no result" in page.lower()
            or "not found" in page.lower()
            or "empty" in page.lower()
            or "0 results" in page.lower()
        ), "Empty state not shown for no-results search"
        return self
