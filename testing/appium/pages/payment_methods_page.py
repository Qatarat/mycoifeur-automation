"""
PaymentMethodsPage — page object for the saved payment methods screen.
Covers: listing saved cards, adding a new card, deleting a card,
        and form field interactions.
"""
from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage
from utils.helpers import wait_for_animation


class PaymentMethodsPage(BasePage):

    # ── Locators ───────────────────────────────────────────────────────────────

    SCREEN_LABELS = ["Payment Methods", "Saved Cards", "My Cards", "Cards"]
    ADD_CARD_LABELS = ["Add Card", "Add New Card", "+ Add Card", "Add Payment Method"]
    SAVE_LABELS = ["Save", "Save Card", "Add", "Confirm"]
    DELETE_LABELS = ["Delete", "Remove", "delete_card"]
    EMPTY_STATE_LABELS = ["No cards", "No payment methods", "Add your first card", "No saved cards"]

    CARD_NUMBER_IDS = ["card_number", "cardNumber", "card_number_field"]
    EXPIRY_IDS = ["expiry", "expiry_date", "card_expiry", "expiryDate"]
    CVV_IDS = ["cvv", "cvc", "security_code", "cvv_field"]
    CARDHOLDER_IDS = ["cardholder_name", "cardholderName", "card_name", "holder_name"]

    CARD_LIST_XPATH = (
        '//*[@content-desc="card_item" or @content-desc="payment_method_item" '
        'or contains(@content-desc,"card_item")]'
    )

    # ── Navigation ─────────────────────────────────────────────────────────────

    def navigate_to_payment_methods(self):
        """Navigate from home to the Payment Methods screen via coordinate Profile tab."""
        from utils.helpers import navigate_to_profile_tab
        navigate_to_profile_tab(self.driver)
        wait_for_animation(self.driver)
        self.tap_optional("Account")
        wait_for_animation(self.driver)
        for label in self.SCREEN_LABELS:
            if self.is_visible(label, timeout=2):
                self.tap_optional(label)
                wait_for_animation(self.driver, 2)
                return self
        self.tap_optional("Payment Methods")
        wait_for_animation(self.driver, 2)
        return self

    def tap_add_card(self):
        """Tap the Add Card button to open the card entry form."""
        for label in self.ADD_CARD_LABELS:
            if self.is_visible(label, timeout=2):
                self.tap_optional(label)
                wait_for_animation(self.driver, 2)
                return self
        return self

    # ── Form interactions ──────────────────────────────────────────────────────

    def _fill_field_by_ids(self, ids, value):
        """Try accessibility IDs first, then EditText by hint/content-desc."""
        for aid in ids:
            els = self.driver.find_elements(AppiumBy.ACCESSIBILITY_ID, aid)
            if els:
                els[0].clear()
                els[0].send_keys(value)
                return True
        # Fallback: XPATH by hint or content-desc
        for aid in ids:
            els = self.driver.find_elements(
                AppiumBy.XPATH,
                f'//android.widget.EditText[contains(@hint,"{aid}") '
                f'or contains(@content-desc,"{aid}")]'
            )
            if els:
                els[0].clear()
                els[0].send_keys(value)
                return True
        return False

    def add_card(self, number: str, expiry: str, cvv: str, name: str):
        """
        Fill and submit the add-card form.
        Calls tap_add_card() first if the form is not already open.
        """
        if not self._fill_field_by_ids(self.CARD_NUMBER_IDS, number):
            self.tap_add_card()
            self._fill_field_by_ids(self.CARD_NUMBER_IDS, number)

        self._fill_field_by_ids(self.EXPIRY_IDS, expiry)
        self._fill_field_by_ids(self.CVV_IDS, cvv)
        self._fill_field_by_ids(self.CARDHOLDER_IDS, name)
        wait_for_animation(self.driver)

        for label in self.SAVE_LABELS:
            if self.is_visible(label, timeout=2):
                self.tap_optional(label)
                break
        wait_for_animation(self.driver, 3)
        return self

    def delete_card(self, index: int = 0):
        """Tap the delete icon on the card at *index* and confirm if prompted."""
        # First try accessibility ID for delete button
        for label in self.DELETE_LABELS:
            btns = self.driver.find_elements(AppiumBy.ACCESSIBILITY_ID, label)
            if btns and index < len(btns):
                btns[index].click()
                wait_for_animation(self.driver)
                # Confirm deletion dialog if it appears
                self.tap_optional("Delete")
                self.tap_optional("Yes")
                self.tap_optional("Confirm")
                wait_for_animation(self.driver, 2)
                return self
        # Fallback XPATH
        btns = self.driver.find_elements(
            AppiumBy.XPATH,
            '//*[@content-desc="delete_card" or contains(@content-desc,"delete")]'
        )
        if btns and index < len(btns):
            btns[index].click()
            wait_for_animation(self.driver)
            self.tap_optional("Delete")
            self.tap_optional("Yes")
            wait_for_animation(self.driver, 2)
        return self

    # ── Data retrieval ─────────────────────────────────────────────────────────

    def get_cards_count(self) -> int:
        """Return the number of saved card entries visible on screen."""
        try:
            items = self.driver.find_elements(AppiumBy.XPATH, self.CARD_LIST_XPATH)
            return len(items)
        except Exception:
            return 0

    # ── Assertions ─────────────────────────────────────────────────────────────

    def assert_screen_loaded(self):
        page = self.driver.page_source
        loaded = any(label in page for label in self.SCREEN_LABELS)
        assert loaded, f"Payment methods screen did not load; page: {page[:200]}"
        return self

    def assert_no_crash(self):
        page = self.driver.page_source
        assert "500" not in page, "500 error on payment methods screen"
        return self

    def assert_empty_state(self):
        page = self.driver.page_source
        has_empty = any(label in page for label in self.EMPTY_STATE_LABELS)
        assert has_empty or self.get_cards_count() == 0, \
            "Expected empty state or 0 cards on fresh account"
        return self
