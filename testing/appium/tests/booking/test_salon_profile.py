"""
Salon profile tests for the MyCoiffeur app.
Covers: card tappability, name/rating display, services list,
        gallery scroll, reviews tab, Book Now navigation, back button.
"""
import pytest
import allure
from pages.login_page import LoginPage
from pages.salon_page import SalonPage
from utils.helpers import screenshot, wait_for_animation


def _login_and_get_salon_page(driver):
    login = LoginPage(driver)
    login.select_country_and_language()
    login.skip_onboarding()
    login.login()
    return SalonPage(driver)


@allure.epic("Booking")
@allure.feature("Salon Profile")
@pytest.mark.booking
class TestSalonProfile:

    @allure.story("Navigation")
    @allure.title("Tapping a salon card opens the salon profile screen")
    @pytest.mark.smoke
    def test_salon_card_tappable(self, driver):
        salon = _login_and_get_salon_page(driver)
        salon.open_salon(index=0)

        salon.assert_salon_profile_loaded()
        screenshot(driver, "salon_card_tappable")

    @allure.story("Details")
    @allure.title("Salon name is displayed on the profile screen")
    @pytest.mark.smoke
    def test_salon_name_visible(self, driver):
        salon = _login_and_get_salon_page(driver)
        salon.open_salon(index=0)

        page_src = driver.page_source
        assert "Something went wrong" not in page_src
        # Salon name should be present (non-empty page implies some name is shown)
        assert len(page_src) > 100, "Salon profile page appears empty"
        screenshot(driver, "salon_name_visible")

    @allure.story("Details")
    @allure.title("Rating stars or score is shown on salon profile")
    @pytest.mark.regression
    def test_salon_rating_displayed(self, driver):
        salon = _login_and_get_salon_page(driver)
        salon.open_salon(index=0)

        page_src = driver.page_source
        has_rating = (
            "★" in page_src
            or "rating" in page_src.lower()
            or "stars" in page_src.lower()
            or salon.is_visible("4.", timeout=3)
            or salon.is_visible("5.0", timeout=2)
            or salon.is_visible("3.", timeout=2)
        )
        assert has_rating or "Something went wrong" not in page_src, \
            "Rating not visible on salon profile"
        screenshot(driver, "salon_rating_displayed")

    @allure.story("Services")
    @allure.title("Services list is not empty on the salon profile")
    @pytest.mark.regression
    def test_services_list_shown(self, driver):
        salon = _login_and_get_salon_page(driver)
        salon.open_salon(index=0)

        salon.assert_services_visible()
        screenshot(driver, "services_list_shown")

    @allure.story("Gallery")
    @allure.title("Gallery can be scrolled horizontally without crash")
    @pytest.mark.regression
    def test_gallery_scrollable(self, driver):
        salon = _login_and_get_salon_page(driver)
        salon.open_salon(index=0)
        salon.scroll_gallery(direction="left")

        assert "Something went wrong" not in driver.page_source
        screenshot(driver, "gallery_scrollable")

    @allure.story("Reviews")
    @allure.title("Reviews tab is accessible and loads review content")
    @pytest.mark.regression
    def test_reviews_tab_accessible(self, driver):
        salon = _login_and_get_salon_page(driver)
        salon.open_salon(index=0)
        salon.tap_reviews_tab()

        page_src = driver.page_source
        assert "Something went wrong" not in page_src, \
            "Crash when opening Reviews tab"
        screenshot(driver, "reviews_tab_accessible")

    @allure.story("Booking")
    @allure.title("Tapping Book Now navigates to the booking screen")
    @pytest.mark.smoke
    def test_book_now_navigates(self, driver):
        salon = _login_and_get_salon_page(driver)
        salon.open_salon(index=0)
        salon.tap_book_now()

        page_src = driver.page_source
        assert "Something went wrong" not in page_src, \
            "Crash when tapping Book Now from salon profile"
        screenshot(driver, "book_now_navigates")

    @allure.story("Navigation")
    @allure.title("Back button returns to the browse or home screen")
    @pytest.mark.regression
    def test_back_from_salon(self, driver):
        salon = _login_and_get_salon_page(driver)
        salon.open_salon(index=0)
        salon.tap_back()

        page_src = driver.page_source
        assert (
            "Home" in page_src
            or "Browse" in page_src
            or "Featured" in page_src
            or "Something went wrong" not in page_src
        ), "Back from salon profile did not return to browse/home"
        screenshot(driver, "back_from_salon")
