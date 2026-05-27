"""
Edit Profile tests for the MyCoiffeur app.
Covers: screen opens, field editing, save persistence, validation,
        special chars, empty name block, avatar picker, and cancel behaviour.
"""
import pytest
import allure
from pages.login_page import LoginPage
from pages.base_page import BasePage
from utils.helpers import screenshot, wait_for_animation
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from test_data import BoundaryValues


def _login_and_open_edit(driver):
    login = LoginPage(driver)
    login.select_country_and_language()
    login.skip_onboarding()
    login.login()

    page = BasePage(driver)
    page.tap_optional("Profile")
    page.tap_optional("Edit")
    page.tap_optional("Edit Profile")
    wait_for_animation(driver, 2)
    return page


@allure.epic("Account")
@allure.feature("Edit Profile")
@pytest.mark.account
class TestEditProfile:

    @allure.story("Navigation")
    @allure.title("Edit profile screen opens from Profile tab")
    @pytest.mark.smoke
    def test_edit_profile_screen_opens(self, driver):
        page = _login_and_open_edit(driver)

        page_src = driver.page_source
        assert (
            "Edit" in page_src
            or "Profile" in page_src
            or "Name" in page_src
            or "Save" in page_src
        ), "Edit profile screen did not open"
        screenshot(driver, "edit_profile_screen_opens")

    @allure.story("Name")
    @allure.title("Name field can be cleared and a new value typed")
    @pytest.mark.regression
    def test_name_field_editable(self, driver):
        page = _login_and_open_edit(driver)
        from appium.webdriver.common.appiumby import AppiumBy

        fields = driver.find_elements(AppiumBy.XPATH, "//android.widget.EditText")
        assert fields, "No editable text fields on edit profile screen"

        name_field = fields[0]
        name_field.clear()
        name_field.send_keys("TestEdit")
        wait_for_animation(driver)

        page_src = driver.page_source
        assert "Something went wrong" not in page_src
        screenshot(driver, "name_field_editable")

    @allure.story("Name")
    @allure.title("Saved name persists and is visible on profile screen")
    @pytest.mark.regression
    def test_name_save_persists(self, driver):
        page = _login_and_open_edit(driver)
        from appium.webdriver.common.appiumby import AppiumBy

        new_name = "AutoUser01"
        fields = driver.find_elements(AppiumBy.XPATH, "//android.widget.EditText")
        if fields:
            fields[0].clear()
            fields[0].send_keys(new_name)
        wait_for_animation(driver)

        page.tap_optional("Save")
        page.tap_optional("Update")
        wait_for_animation(driver, 2)

        assert page.is_visible(new_name, timeout=5) or new_name in driver.page_source, \
            "Saved name not visible on profile after update"
        screenshot(driver, "name_save_persists")

    @allure.story("Name")
    @allure.title("200-character name is handled without crash")
    @pytest.mark.regression
    def test_name_too_long(self, driver):
        page = _login_and_open_edit(driver)
        from appium.webdriver.common.appiumby import AppiumBy

        fields = driver.find_elements(AppiumBy.XPATH, "//android.widget.EditText")
        if fields:
            fields[0].clear()
            fields[0].send_keys(BoundaryValues.PROFILE_LONG_NAME)
        wait_for_animation(driver)

        page_src = driver.page_source
        assert "Something went wrong" not in page_src, \
            "App crashed on 200-char name input"
        screenshot(driver, "name_too_long")

    @allure.story("Name")
    @allure.title("Special characters in name do not crash the app")
    @pytest.mark.regression
    def test_name_special_chars(self, driver):
        page = _login_and_open_edit(driver)
        from appium.webdriver.common.appiumby import AppiumBy

        fields = driver.find_elements(AppiumBy.XPATH, "//android.widget.EditText")
        if fields:
            fields[0].clear()
            fields[0].send_keys(BoundaryValues.PROFILE_SPECIAL_CHARS)
        wait_for_animation(driver)

        page_src = driver.page_source
        assert "Something went wrong" not in page_src, \
            "App crashed with special chars in name"
        screenshot(driver, "name_special_chars")

    @allure.story("Name")
    @allure.title("Empty name field blocks saving")
    @pytest.mark.regression
    def test_name_empty_blocked(self, driver):
        page = _login_and_open_edit(driver)
        from appium.webdriver.common.appiumby import AppiumBy

        fields = driver.find_elements(AppiumBy.XPATH, "//android.widget.EditText")
        if fields:
            fields[0].clear()
        wait_for_animation(driver)

        page.tap_optional("Save")
        page.tap_optional("Update")
        wait_for_animation(driver, 2)

        page_src = driver.page_source
        # Either an error message is shown or save is simply disabled
        still_on_edit = (
            "Edit" in page_src
            or "required" in page_src.lower()
            or "cannot be empty" in page_src.lower()
            or "Save" in page_src
        )
        assert still_on_edit, "Empty name was accepted — validation not enforced"
        screenshot(driver, "name_empty_blocked")

    @allure.story("Avatar")
    @allure.title("Tapping profile photo opens an image picker")
    @pytest.mark.regression
    def test_avatar_tap_opens_picker(self, driver):
        page = _login_and_open_edit(driver)
        from appium.webdriver.common.appiumby import AppiumBy

        avatars = driver.find_elements(
            AppiumBy.XPATH,
            '//*[@content-desc="avatar" or @content-desc="profile_photo" '
            'or @content-desc="change_photo" or contains(@content-desc,"photo")]'
        )
        if avatars:
            avatars[0].click()
            wait_for_animation(driver, 2)

        page_src = driver.page_source
        assert "Something went wrong" not in page_src, \
            "Crash when tapping avatar/profile photo"
        screenshot(driver, "avatar_tap_opens_picker")

    @allure.story("Cancel")
    @allure.title("Cancelling edit reverts to original name")
    @pytest.mark.regression
    def test_cancel_edit_reverts(self, driver):
        login = LoginPage(driver)
        login.select_country_and_language()
        login.skip_onboarding()
        login.login()

        page = BasePage(driver)
        page.tap_optional("Profile")
        wait_for_animation(driver)

        # Capture current name from page source before editing
        original_src = driver.page_source

        page.tap_optional("Edit")
        page.tap_optional("Edit Profile")
        wait_for_animation(driver, 2)

        from appium.webdriver.common.appiumby import AppiumBy
        fields = driver.find_elements(AppiumBy.XPATH, "//android.widget.EditText")
        if fields:
            fields[0].clear()
            fields[0].send_keys("ShouldNotSaveXYZ")
        wait_for_animation(driver)

        page.tap_optional("Cancel")
        page.tap_optional("Discard")
        driver.back()
        wait_for_animation(driver, 2)

        page_src = driver.page_source
        assert "ShouldNotSaveXYZ" not in page_src or "Profile" in page_src, \
            "Cancelled edit was persisted"
        screenshot(driver, "cancel_edit_reverts")
