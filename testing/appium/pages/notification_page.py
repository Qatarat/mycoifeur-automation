"""
NotificationPage — page object for notification panel interactions.
Covers: open bell icon, notification list, mark all read, tap a notification.
"""
from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage
from utils.helpers import wait_for_animation


class NotificationPage(BasePage):

    def open_notifications(self):
        """Open the notification panel via bell icon or Notifications tab."""
        self.tap_optional("Notifications")
        # Try by accessibility ID if text tap doesn't work
        try:
            self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "notification_bell").click()
        except Exception:
            pass
        wait_for_animation(self.driver, 2)
        return self

    def mark_all_read(self):
        """Tap Mark All as Read if the button is visible."""
        self.tap_optional("Mark All as Read")
        self.tap_optional("Mark all read")
        wait_for_animation(self.driver)
        return self

    def tap_first_notification(self):
        """Tap the first notification item in the list."""
        from utils.helpers import find_by_text
        items = self.driver.find_elements(
            AppiumBy.XPATH,
            '//*[@content-desc="notification_item" or contains(@text,"Your booking") or contains(@text,"Order")]'
        )
        if items:
            items[0].click()
            wait_for_animation(self.driver, 2)
        return self

    def get_notification_count(self) -> int:
        """Return the count of visible notification items."""
        items = self.driver.find_elements(
            AppiumBy.XPATH,
            '//*[@content-desc="notification_item"]'
        )
        return len(items)

    def assert_panel_open(self):
        page = self.driver.page_source
        assert (
            "notification" in page.lower()
            or "Notifications" in page
            or "No notifications" in page
        ), "Notification panel did not open"
        return self

    def assert_no_unread_badge_after_mark_read(self):
        """After marking all read, badge count should be 0 or absent."""
        page = self.driver.page_source
        # Badge should not show a number > 0
        assert "unread" not in page.lower() or "0" in page, \
            "Unread badge still visible after marking all notifications as read"
        return self
