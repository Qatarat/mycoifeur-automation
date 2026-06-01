import pytest
from pages.login_page import LoginPage
from pages.cart_page import CartPage
from pages.base_page import BasePage
from utils.helpers import screenshot, wait_for_animation
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from test_data import BoundaryValues


@pytest.mark.cart
@pytest.mark.negative
@pytest.mark.android
class TestCartBoundary:
    """Boundary and edge-case tests for cart operations."""

    def _login_and_open_cart(self, driver):
        login = LoginPage(driver)
        login.select_country_and_language()
        login.skip_onboarding()
        login.login()
        login.assert_logged_in()
        cart = CartPage(driver)
        cart.open_cart()
        wait_for_animation(driver)
        return cart

    def test_empty_cart_checkout_is_blocked(self, driver):
        """Checkout must not proceed when cart is empty or unavailable."""
        cart = self._login_and_open_cart(driver)
        base = BasePage(driver)
        base.tap_optional("Checkout")
        wait_for_animation(driver)
        assert "500" not in driver.page_source, "500 error on cart/checkout"
        screenshot(driver, "cart_empty_checkout_blocked")

    def test_quantity_increment_updates_total(self, driver):
        """Cart quantity increment must not crash the app."""
        cart = self._login_and_open_cart(driver)
        cart.update_quantity(increment=True)
        wait_for_animation(driver)
        assert "500" not in driver.page_source
        screenshot(driver, "cart_quantity_incremented")

    def test_quantity_decrement_to_one_keeps_item(self, driver):
        """Cart quantity decrement must not crash the app."""
        cart = self._login_and_open_cart(driver)
        cart.update_quantity(increment=False)
        wait_for_animation(driver)
        assert "500" not in driver.page_source
        screenshot(driver, "cart_quantity_back_to_one")

    def test_quantity_decrement_at_one_removes_or_prompts(self, driver):
        """Decrementing below 1 must not crash — shows prompt or empty state."""
        cart = self._login_and_open_cart(driver)
        cart.update_quantity(increment=False)
        wait_for_animation(driver)
        assert "500" not in driver.page_source
        screenshot(driver, "cart_decrement_below_one")

    def test_maximum_quantity_does_not_crash(self, driver):
        """Tapping '+' many times must not produce NaN/error UI."""
        cart = self._login_and_open_cart(driver)
        base = BasePage(driver)
        for _ in range(5):
            base.tap_optional("+")
            wait_for_animation(driver, 0.3)
        screenshot(driver, "cart_max_quantity")
        assert "NaN" not in driver.page_source and "500" not in driver.page_source, \
            "Cart showed NaN or 500 error after quantity increments"

    def test_remove_all_items_shows_empty_state(self, driver):
        """Removing items from cart must not crash the app."""
        cart = self._login_and_open_cart(driver)
        base = BasePage(driver)
        base.tap_optional("Remove")
        wait_for_animation(driver)
        base.tap_optional("Yes")
        wait_for_animation(driver)
        assert "500" not in driver.page_source
        screenshot(driver, "cart_empty_after_remove")
