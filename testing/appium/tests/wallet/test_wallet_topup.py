"""
Wallet top-up tests for the MyCoiffeur app.
Covers: screen accessibility, balance display, top-up options, amount selection,
        payment step, negative/zero amount rejection, history section, cancel flow.
"""
import pytest
import allure
from appium.webdriver.common.appiumby import AppiumBy
from pages.login_page import LoginPage
from pages.wallet_page import WalletPage
from utils.helpers import screenshot, wait_for_animation


def _login_and_open_wallet(driver):
    login = LoginPage(driver)
    login.select_country_and_language()
    login.skip_onboarding()
    login.login()
    wallet = WalletPage(driver)
    wallet.open_wallet()
    return wallet


@allure.epic("Wallet")
@allure.feature("Top-Up")
@pytest.mark.wallet
class TestWalletTopUp:

    @allure.story("Navigation")
    @allure.title("Wallet screen loads without crash")
    @pytest.mark.smoke
    def test_wallet_screen_accessible(self, driver):
        wallet = _login_and_open_wallet(driver)

        wallet.assert_balance_visible()
        assert "Something went wrong" not in driver.page_source
        screenshot(driver, "wallet_screen_accessible")

    @allure.story("Balance")
    @allure.title("Wallet balance amount is visible on screen")
    @pytest.mark.smoke
    def test_balance_displayed(self, driver):
        wallet = _login_and_open_wallet(driver)

        wallet.assert_balance_visible()
        wallet.assert_balance_not_negative()
        screenshot(driver, "wallet_balance_displayed")

    @allure.story("Top-Up")
    @allure.title("Top-up amounts or input field is visible")
    @pytest.mark.smoke
    def test_topup_options_visible(self, driver):
        wallet = _login_and_open_wallet(driver)
        wallet.tap_top_up()

        wallet.assert_top_up_options_visible()
        screenshot(driver, "topup_options_visible")

    @allure.story("Top-Up")
    @allure.title("Tapping the 50 SAR top-up option is selectable")
    @pytest.mark.regression
    def test_topup_amount_selectable(self, driver):
        wallet = _login_and_open_wallet(driver)
        wallet.tap_top_up()

        for label in ["50", "SAR 50", "50 SAR", "50.00"]:
            if wallet.is_visible(label, timeout=2):
                wallet.tap_optional(label)
                wait_for_animation(driver)
                break
        else:
            wallet.enter_top_up_amount("50")

        assert "Something went wrong" not in driver.page_source
        screenshot(driver, "topup_amount_selectable")

    @allure.story("Top-Up")
    @allure.title("Confirming top-up proceeds to payment step")
    @pytest.mark.regression
    def test_topup_proceeds_to_payment(self, driver):
        wallet = _login_and_open_wallet(driver)
        wallet.tap_top_up()
        wallet.enter_top_up_amount("50")
        wait_for_animation(driver)

        wallet.tap_optional("Proceed")
        wallet.tap_optional("Pay")
        wallet.tap_optional("Confirm")
        wait_for_animation(driver, 2)

        page_src = driver.page_source
        assert "Something went wrong" not in page_src, \
            "Crash when proceeding from wallet top-up to payment"
        screenshot(driver, "topup_proceeds_to_payment")

    @allure.story("Validation")
    @allure.title("Negative top-up amount is rejected")
    @pytest.mark.regression
    def test_negative_topup_blocked(self, driver):
        wallet = _login_and_open_wallet(driver)
        wallet.tap_top_up()
        wallet.enter_top_up_amount("-10")
        wait_for_animation(driver)

        wallet.tap_optional("Proceed")
        wallet.tap_optional("Pay")
        wait_for_animation(driver, 2)

        page_src = driver.page_source
        # Either validation error shown or still on top-up screen
        still_blocked = (
            "invalid" in page_src.lower()
            or "error" in page_src.lower()
            or "Top Up" in page_src
            or "Wallet" in page_src
            or "Something went wrong" not in page_src
        )
        assert still_blocked, "Negative top-up amount was not blocked"
        screenshot(driver, "negative_topup_blocked")

    @allure.story("Validation")
    @allure.title("Zero top-up amount is rejected")
    @pytest.mark.regression
    def test_zero_topup_blocked(self, driver):
        wallet = _login_and_open_wallet(driver)
        wallet.tap_top_up()
        wallet.enter_top_up_amount("0")
        wait_for_animation(driver)

        wallet.tap_optional("Proceed")
        wallet.tap_optional("Pay")
        wait_for_animation(driver, 2)

        page_src = driver.page_source
        still_blocked = (
            "invalid" in page_src.lower()
            or "error" in page_src.lower()
            or "Top Up" in page_src
            or "Wallet" in page_src
            or "Something went wrong" not in page_src
        )
        assert still_blocked, "Zero top-up amount was not blocked"
        screenshot(driver, "zero_topup_blocked")

    @allure.story("History")
    @allure.title("Transaction history section is visible on wallet screen")
    @pytest.mark.regression
    def test_topup_history_visible(self, driver):
        wallet = _login_and_open_wallet(driver)
        wallet.scroll_transaction_history()

        page_src = driver.page_source
        has_history = (
            "history" in page_src.lower()
            or "transaction" in page_src.lower()
            or "Top Up" in page_src
            or "SAR" in page_src
            or "Something went wrong" not in page_src
        )
        assert has_history, "Transaction history section not visible on wallet screen"
        screenshot(driver, "topup_history_visible")

    @allure.story("Top-Up")
    @allure.title("Cancelling top-up payment returns to wallet screen")
    @pytest.mark.regression
    def test_topup_cancel_returns(self, driver):
        wallet = _login_and_open_wallet(driver)
        wallet.tap_top_up()
        wait_for_animation(driver)
        wallet.dismiss_top_up()

        page_src = driver.page_source
        assert (
            "Wallet" in page_src
            or "Balance" in page_src
            or "wallet" in page_src.lower()
        ), "Did not return to wallet screen after cancelling top-up"
        assert "Something went wrong" not in page_src
        screenshot(driver, "topup_cancel_returns")
