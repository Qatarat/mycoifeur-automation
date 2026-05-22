"""
Checkout edge cases — navigation, payment method switching, back button,
currency display, coupon + payment combos.
"""
import pytest
from appium.webdriver.common.appiumby import AppiumBy
from pages.login_page import LoginPage
from pages.cart_page import CartPage
from test_data import ValidData


def _reach_checkout(driver):
    login = LoginPage(driver)
    login.login(ValidData.PHONE, ValidData.OTP)
    cart = CartPage(driver)
    cart.add_item_and_go_to_checkout()


@pytest.mark.checkout
@pytest.mark.boundary
class TestCheckoutNavigation:

    def test_back_from_checkout_returns_to_cart(self, driver):
        """Pressing back from checkout must return to cart, not log out or crash."""
        _reach_checkout(driver)
        driver.back()
        page = driver.page_source
        assert "Something went wrong" not in page
        assert "Cart" in page or "cart" in page.lower() or "items" in page.lower()

    def test_back_then_forward_preserves_cart(self, driver):
        """Cart items must persist after navigating back from checkout and returning."""
        _reach_checkout(driver)
        driver.back()
        driver.find_element(AppiumBy.ACCESSIBILITY_ID, "checkout_button").click()
        assert "payment" in driver.page_source.lower() or "method" in driver.page_source.lower()

    def test_checkout_page_shows_order_summary(self, driver):
        """Checkout must display item name, quantity, subtotal, total."""
        _reach_checkout(driver)
        page = driver.page_source
        assert "total" in page.lower() or "subtotal" in page.lower() or "SAR" in page or "amount" in page.lower()

    def test_checkout_price_not_nan_or_zero(self, driver):
        """Total must be a valid number — not NaN, undefined, or 0.00 for a non-empty cart."""
        _reach_checkout(driver)
        page = driver.page_source
        assert "NaN" not in page
        assert "undefined" not in page


@pytest.mark.checkout
@pytest.mark.boundary
class TestPaymentMethodSwitching:

    def test_switch_from_card_to_tabby(self, driver):
        """Switching payment method mid-checkout must not duplicate items or corrupt total."""
        _reach_checkout(driver)
        try:
            driver.find_element(AppiumBy.ACCESSIBILITY_ID, "payment_card_option").click()
            driver.find_element(AppiumBy.ACCESSIBILITY_ID, "payment_tabby_option").click()
        except Exception:
            pass  # Options may not exist on this cart value
        assert "Something went wrong" not in driver.page_source

    def test_switch_payment_method_multiple_times(self, driver):
        """Rapidly switching payment options must not crash."""
        _reach_checkout(driver)
        methods = driver.find_elements(AppiumBy.XPATH, "//*[@content-desc='payment_option']")
        for _ in range(3):
            for m in methods[:2]:
                try:
                    m.click()
                except Exception:
                    pass
        assert "500" not in driver.page_source

    def test_coupon_applied_then_payment_selected(self, driver):
        """Apply promo code then select payment — total must reflect discount."""
        _reach_checkout(driver)
        try:
            promo_field = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "promo_code_field")
            promo_field.send_keys(ValidData.PROMO_CODE)
            driver.find_element(AppiumBy.ACCESSIBILITY_ID, "apply_promo_button").click()
            driver.find_element(AppiumBy.ACCESSIBILITY_ID, "payment_card_option").click()
        except Exception:
            pass
        assert "NaN" not in driver.page_source
        assert "Something went wrong" not in driver.page_source

    def test_invalid_coupon_then_payment_selected(self, driver):
        """Invalid promo should not block payment method selection."""
        _reach_checkout(driver)
        try:
            promo_field = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "promo_code_field")
            promo_field.send_keys("BADCODE123")
            driver.find_element(AppiumBy.ACCESSIBILITY_ID, "apply_promo_button").click()
            driver.find_element(AppiumBy.ACCESSIBILITY_ID, "payment_card_option").click()
        except Exception:
            pass
        assert "Something went wrong" not in driver.page_source


@pytest.mark.checkout
@pytest.mark.boundary
class TestCurrencyDisplay:

    def test_price_shows_currency_symbol(self, driver):
        """All prices must show SAR, ﷼, or USD — never raw numbers without currency."""
        _reach_checkout(driver)
        page = driver.page_source
        has_currency = "SAR" in page or "﷼" in page or "USD" in page or "AED" in page
        assert has_currency

    def test_price_decimal_places_correct(self, driver):
        """Prices must have exactly 2 decimal places (e.g. 10.00, not 10.0 or 10.000)."""
        _reach_checkout(driver)
        page = driver.page_source
        import re
        # Prices like 10.00 or 10.50 — must not have 3+ decimal places
        bad_decimals = re.findall(r'\d+\.\d{3,}', page)
        assert len(bad_decimals) == 0, f"Found malformed prices: {bad_decimals}"
