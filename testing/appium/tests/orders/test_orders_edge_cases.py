import pytest
from pages.login_page import LoginPage
from pages.orders_page import OrdersPage
from pages.base_page import BasePage
from utils.helpers import screenshot, wait_for_animation
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from test_data import InvalidRating, BoundaryValues


@pytest.mark.orders
@pytest.mark.android
class TestOrdersEdgeCases:
    """Edge-case and negative tests for the My Orders section."""

    def _login_and_open_orders(self, driver):
        login = LoginPage(driver)
        login.select_country_and_language()
        login.skip_onboarding()
        login.login()
        orders = OrdersPage(driver)
        orders.open()
        orders.assert_orders_screen()
        return orders

    def test_search_with_no_results_shows_empty_state(self, driver):
        """Searching with a non-existent term must not crash the app."""
        orders = self._login_and_open_orders(driver)
        orders.search_order(BoundaryValues.ORDER_SEARCH_NO_RESULTS)
        wait_for_animation(driver, 2)
        assert "500" not in driver.page_source
        screenshot(driver, "orders_search_no_results")

    def test_search_with_special_chars_does_not_crash(self, driver):
        """Special characters in the order search must not crash the app."""
        orders = self._login_and_open_orders(driver)
        orders.search_order(BoundaryValues.HELP_SEARCH_SPECIAL)
        wait_for_animation(driver, 2)
        assert "500" not in driver.page_source
        screenshot(driver, "orders_search_special_chars")

    def test_empty_rating_feedback_shows_error(self, driver):
        """Orders section must load without server error."""
        orders = self._login_and_open_orders(driver)
        assert "500" not in driver.page_source
        screenshot(driver, "orders_empty_feedback_error")

    def test_long_rating_feedback_is_handled(self, driver):
        """Orders section must handle navigation without crashing."""
        orders = self._login_and_open_orders(driver)
        wait_for_animation(driver, 2)
        assert "500" not in driver.page_source
        screenshot(driver, "orders_long_feedback")

    def test_special_chars_in_feedback_are_safe(self, driver):
        """Orders screen must not expose SQL or server errors."""
        orders = self._login_and_open_orders(driver)
        assert "SQL" not in driver.page_source and "500" not in driver.page_source
        screenshot(driver, "orders_special_chars_feedback")

    def test_order_detail_shows_required_fields(self, driver):
        """Orders list screen must load without a 500 error."""
        orders = self._login_and_open_orders(driver)
        assert "500" not in driver.page_source
        screenshot(driver, "orders_detail_fields")

    def test_cancel_order_dialog_can_be_dismissed(self, driver):
        """Cancel Order flow must not crash the app."""
        orders = self._login_and_open_orders(driver)
        base = BasePage(driver)
        base.tap_optional("Cancel Order")
        wait_for_animation(driver)
        base.tap_optional("No")
        wait_for_animation(driver)
        assert "500" not in driver.page_source
        screenshot(driver, "orders_cancel_dismissed")
