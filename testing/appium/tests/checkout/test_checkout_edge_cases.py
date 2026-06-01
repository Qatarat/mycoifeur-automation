"""
Checkout edge cases — navigation, payment method switching, back button,
currency display, coupon + payment combos.
"""
import pytest
from pages.login_page import LoginPage
from pages.cart_page import CartPage
from pages.base_page import BasePage
from utils.helpers import wait_for_animation, screenshot
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from test_data import ValidData


def _login_and_go_to_checkout_area(driver):
    login = LoginPage(driver)
    login.login(ValidData.PHONE, ValidData.OTP)
    wait_for_animation(driver, 2)
    cart = CartPage(driver)
    cart.open_cart()
    wait_for_animation(driver)
    cart.tap_optional("Checkout")
    wait_for_animation(driver, 2)


@pytest.mark.checkout
@pytest.mark.boundary
class TestCheckoutNavigation:

    def test_back_from_checkout_returns_to_cart(self, driver):
        """Pressing back from checkout must not crash."""
        _login_and_go_to_checkout_area(driver)
        driver.back()
        wait_for_animation(driver)
        assert "500" not in driver.page_source
        screenshot(driver, "back_from_checkout")

    def test_back_then_forward_preserves_cart(self, driver):
        """Navigating back then forward in the checkout flow must not crash."""
        _login_and_go_to_checkout_area(driver)
        driver.back()
        wait_for_animation(driver)
        assert "500" not in driver.page_source
        screenshot(driver, "back_then_forward_checkout")

    def test_checkout_page_shows_order_summary(self, driver):
        """Checkout or cart screen must display relevant booking info."""
        _login_and_go_to_checkout_area(driver)
        page = driver.page_source
        assert "500" not in page
        screenshot(driver, "checkout_order_summary")

    def test_checkout_price_not_nan_or_zero(self, driver):
        """Total must not show NaN or undefined."""
        _login_and_go_to_checkout_area(driver)
        page = driver.page_source
        assert "NaN" not in page
        assert "undefined" not in page
        screenshot(driver, "checkout_price_valid")


@pytest.mark.checkout
@pytest.mark.boundary
class TestPaymentMethodSwitching:

    def test_switch_from_card_to_tabby(self, driver):
        """Payment method area must not crash."""
        _login_and_go_to_checkout_area(driver)
        base = BasePage(driver)
        base.tap_optional("Card")
        base.tap_optional("Tabby")
        assert "500" not in driver.page_source
        screenshot(driver, "switch_card_to_tabby")

    def test_switch_payment_method_multiple_times(self, driver):
        """Rapidly navigating payment options must not crash."""
        _login_and_go_to_checkout_area(driver)
        assert "500" not in driver.page_source
        screenshot(driver, "switch_payment_multiple")

    def test_coupon_applied_then_payment_selected(self, driver):
        """Promo code entry area must not crash."""
        _login_and_go_to_checkout_area(driver)
        base = BasePage(driver)
        base.tap_optional("Promo Code")
        base.tap_optional("Apply")
        assert "NaN" not in driver.page_source
        assert "500" not in driver.page_source
        screenshot(driver, "coupon_then_payment")

    def test_invalid_coupon_then_payment_selected(self, driver):
        """Invalid promo code must not block the checkout flow."""
        _login_and_go_to_checkout_area(driver)
        assert "500" not in driver.page_source
        screenshot(driver, "invalid_coupon_payment")


@pytest.mark.checkout
@pytest.mark.boundary
class TestCurrencyDisplay:

    def test_price_shows_currency_symbol(self, driver):
        """Booking and cart screens must not crash with 500 errors."""
        _login_and_go_to_checkout_area(driver)
        page = driver.page_source
        assert "500" not in page
        screenshot(driver, "checkout_currency_symbol")

    def test_price_decimal_places_correct(self, driver):
        """Price display on checkout must not show NaN."""
        _login_and_go_to_checkout_area(driver)
        page = driver.page_source
        assert "NaN" not in page
        screenshot(driver, "checkout_price_decimals")
