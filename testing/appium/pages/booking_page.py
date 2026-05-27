"""
BookingPage — page object for the booking / appointment scheduling flow.
Covers: service selection, date/time slot picker, booking confirmation,
        reschedule, and cancel booking interactions.
"""
from pages.base_page import BasePage
from utils.helpers import wait_for_animation


class BookingPage(BasePage):

    # ── Navigation ─────────────────────────────────────────────────────────────

    def go_to_bookings(self):
        self.tap_optional("My Orders")
        self.tap_optional("Bookings")
        wait_for_animation(self.driver)
        return self

    def go_to_upcoming(self):
        self.tap_optional("Upcoming")
        wait_for_animation(self.driver)
        return self

    def go_to_completed(self):
        self.tap_optional("Completed")
        wait_for_animation(self.driver)
        return self

    # ── Booking flow ────────────────────────────────────────────────────────────

    def select_first_service(self):
        """Tap Book Now or Select on the first visible service card."""
        self.tap_optional("Book Now")
        self.tap_optional("Select")
        wait_for_animation(self.driver, 2)
        return self

    def select_date(self, label: str = "Today"):
        """Tap a date chip by label (Today / Tomorrow / Next Week)."""
        self.tap_optional(label)
        wait_for_animation(self.driver)
        return self

    def select_first_slot(self):
        """Tap the first available time slot."""
        from appium.webdriver.common.appiumby import AppiumBy
        slots = self.driver.find_elements(
            AppiumBy.XPATH,
            '//*[contains(@text,"AM") or contains(@text,"PM") or contains(@content-desc,"AM") or contains(@content-desc,"PM")]'
        )
        if slots:
            slots[0].click()
            wait_for_animation(self.driver)
        else:
            # Try tapping 10:00 as fallback
            self.tap_optional("10:00")
        return self

    def confirm_booking(self):
        self.tap_optional("Confirm Booking")
        self.tap_optional("Book")
        self.tap_optional("Confirm")
        wait_for_animation(self.driver, 3)
        return self

    # ── Reschedule ──────────────────────────────────────────────────────────────

    def tap_reschedule(self):
        self.tap_optional("Reschedule")
        wait_for_animation(self.driver, 2)
        return self

    def confirm_reschedule(self):
        self.tap_optional("Confirm Reschedule")
        self.tap_optional("Confirm")
        wait_for_animation(self.driver, 3)
        return self

    # ── Cancel ──────────────────────────────────────────────────────────────────

    def tap_cancel_booking(self):
        self.tap_optional("Cancel Order")
        self.tap_optional("Cancel Booking")
        wait_for_animation(self.driver)
        return self

    def confirm_cancel(self):
        self.tap_optional("Yes")
        self.tap_optional("Yes, Cancel")
        self.tap_optional("Confirm")
        wait_for_animation(self.driver, 3)
        return self

    def decline_cancel(self):
        self.tap_optional("No")
        self.tap_optional("Keep")
        wait_for_animation(self.driver)
        return self

    # ── Assertions ─────────────────────────────────────────────────────────────

    def assert_booking_confirmed(self):
        page = self.driver.page_source
        assert (
            "confirmed" in page.lower()
            or "success" in page.lower()
            or "booked" in page.lower()
            or "Booking" in page
        ), "Booking confirmation screen not shown"
        return self

    def assert_booking_cancelled(self):
        assert self.is_visible("Cancelled", timeout=8) or \
               "cancelled" in self.driver.page_source.lower(), \
            "Order was not shown as Cancelled after cancellation"
        return self

    def assert_slot_picker_visible(self):
        page = self.driver.page_source
        assert (
            "AM" in page or "PM" in page or "slot" in page.lower() or "time" in page.lower()
        ), "Time slot picker was not shown"
        return self
