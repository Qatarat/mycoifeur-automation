"""
LocationPage — page object for map / location permission flows.
Covers: location permission dialogs, map rendering, provider pin tap.
"""
from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage
from utils.helpers import wait_for_animation


class LocationPage(BasePage):

    def open_map(self):
        """Navigate to the Map / Near Me screen."""
        self.tap_optional("Map")
        self.tap_optional("Near Me")
        self.tap_optional("Location")
        wait_for_animation(self.driver, 3)
        return self

    def grant_location_permission(self):
        """Accept the OS location permission dialog."""
        self.tap_optional("Allow")
        self.tap_optional("Allow While Using App")
        self.tap_optional("While using the app")
        wait_for_animation(self.driver, 2)
        return self

    def deny_location_permission(self):
        """Deny the OS location permission dialog."""
        self.tap_optional("Don't Allow")
        self.tap_optional("Deny")
        wait_for_animation(self.driver, 2)
        return self

    def tap_first_pin(self):
        """Tap the first visible map pin."""
        try:
            pin = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "map_pin")
            pin.click()
            wait_for_animation(self.driver, 2)
        except Exception:
            pass
        return self

    # ── Assertions ─────────────────────────────────────────────────────────────

    def assert_map_loaded(self):
        page = self.driver.page_source
        assert "Something went wrong" not in page, "Map failed to load"
        assert "500" not in page, "500 error on map screen"
        return self

    def assert_permission_denied_handled(self):
        """After denying location, the app should show a fallback UI — not crash."""
        page = self.driver.page_source
        assert "Something went wrong" not in page, \
            "App crashed after location permission denied"
        # Should show either a 'grant permission' prompt or a fallback map
        assert (
            "location" in page.lower()
            or "permission" in page.lower()
            or "map" in page.lower()
            or "Browse" in page
        ), "No fallback UI shown after denying location"
        return self
