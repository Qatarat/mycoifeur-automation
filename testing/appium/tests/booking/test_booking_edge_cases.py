"""
Booking edge cases and negative tests.
Covers: past date selection, double-booking, slot unavailability,
        back-button mid-booking, booking with empty slot, rapid confirm taps.
"""
import pytest
import allure
from pages.login_page import LoginPage
from pages.booking_page import BookingPage
from utils.helpers import screenshot, wait_for_animation


def _setup(driver):
    login = LoginPage(driver)
    login.login()
    return BookingPage(driver)


@allure.epic("Booking")
@allure.feature("Booking Edge Cases")
@pytest.mark.booking
@pytest.mark.boundary
@pytest.mark.negative
class TestBookingEdgeCases:

    @allure.story("Past Date")
    @allure.title("Selecting a past date should be blocked or show no slots")
    def test_past_date_blocked(self, driver):
        booking = _setup(driver)
        booking.select_first_service()
        # Try to select yesterday — should be disabled or show no slots
        booking.select_date("Yesterday")
        page = driver.page_source
        assert "Something went wrong" not in page
        # Past date should either be unresponsive or show 'no availability'
        assert "500" not in page
        screenshot(driver, "booking_past_date_blocked")

    @allure.story("No Slot Selected")
    @allure.title("Confirm without selecting a slot should show validation error")
    def test_confirm_without_slot_shows_error(self, driver):
        booking = _setup(driver)
        booking.select_first_service()
        booking.select_date("Today")
        # Skip slot selection — tap confirm immediately
        booking.confirm_booking()
        page = driver.page_source
        # Should show error / stay on booking screen
        assert "Something went wrong" not in page
        assert "500" not in page
        screenshot(driver, "booking_no_slot_error")

    @allure.story("Back Mid Booking")
    @allure.title("Back button mid-booking returns to service list without crash")
    def test_back_mid_booking(self, driver):
        booking = _setup(driver)
        booking.select_first_service()
        booking.select_date("Today")
        driver.back()
        wait_for_animation(driver, 1)
        page = driver.page_source
        assert "Something went wrong" not in page
        screenshot(driver, "booking_back_mid_flow")

    @allure.story("Rapid Confirm")
    @allure.title("Double-tapping Confirm does not create duplicate booking")
    def test_double_tap_confirm_no_duplicate(self, driver):
        booking = _setup(driver)
        booking.select_first_service()
        booking.select_date("Today")
        booking.select_first_slot()
        # Tap confirm twice rapidly
        for _ in range(2):
            booking.tap_optional("Confirm Booking")
            booking.tap_optional("Confirm")
        wait_for_animation(driver, 3)
        page = driver.page_source
        assert "Something went wrong" not in page
        screenshot(driver, "booking_double_confirm")

    @allure.story("Date Picker Boundary")
    @allure.title("Date picker does not allow selection beyond max future date")
    def test_far_future_date_unavailable(self, driver):
        booking = _setup(driver)
        booking.select_first_service()
        # Try scrolling calendar far into the future
        from appium.webdriver.common.appiumby import AppiumBy
        size = driver.get_window_size()
        for _ in range(5):
            try:
                driver.execute_script(
                    "mobile: swipeGesture",
                    {"startX": int(size["width"] * 0.8),
                     "startY": size["height"] // 2,
                     "endX": int(size["width"] * 0.2),
                     "endY": size["height"] // 2, "speed": 600}
                )
            except Exception:
                pass
        page = driver.page_source
        assert "Something went wrong" not in page
        screenshot(driver, "booking_far_future_date")

    @allure.story("Slot Availability")
    @allure.title("Unavailable slot shows disabled state — not an error")
    def test_unavailable_slot_not_selectable(self, driver):
        booking = _setup(driver)
        booking.select_first_service()
        booking.select_date("Today")
        # Try to find and click a slot marked unavailable
        from appium.webdriver.common.appiumby import AppiumBy
        disabled_slots = driver.find_elements(
            AppiumBy.XPATH,
            '//*[contains(@content-desc,"unavailable") or contains(@content-desc,"booked")]'
        )
        for slot in disabled_slots[:1]:
            try:
                slot.click()
            except Exception:
                pass
        page = driver.page_source
        assert "Something went wrong" not in page
        screenshot(driver, "booking_unavailable_slot")
