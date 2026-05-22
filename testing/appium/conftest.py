import os
import pytest
import allure
from appium import webdriver

# AppiumOptions moved out of __init__ in client v4.x — try both import paths
try:
    from appium.options import AppiumOptions
except ImportError:
    from appium.options.base_options import AppiumOptions

from capabilities.android_caps import ANDROID_DEVICE_CAPS, ANDROID_EMULATOR_CAPS
from capabilities.ios_caps import IOS_DEVICE_CAPS, IOS_SIMULATOR_CAPS
from utils.helpers import APPIUM_SERVER, screenshot

PLATFORM = os.environ.get("PLATFORM", "android").lower()
DEVICE_MODE = os.environ.get("DEVICE_MODE", "emulator").lower()


def get_caps():
    if PLATFORM == "android":
        return ANDROID_DEVICE_CAPS if DEVICE_MODE == "device" else ANDROID_EMULATOR_CAPS
    elif PLATFORM == "ios":
        return IOS_DEVICE_CAPS if DEVICE_MODE == "device" else IOS_SIMULATOR_CAPS
    raise ValueError(f"Unknown platform: {PLATFORM}")


@pytest.fixture(scope="function")
def driver():
    options = AppiumOptions().load_capabilities(get_caps())
    d = webdriver.Remote(APPIUM_SERVER, options=options)
    d.implicitly_wait(10)
    yield d
    d.quit()


@pytest.fixture(scope="module")
def driver_module():
    caps = {**get_caps(), "appium:noReset": True}
    options = AppiumOptions().load_capabilities(caps)
    d = webdriver.Remote(APPIUM_SERVER, options=options)
    d.implicitly_wait(10)
    yield d
    d.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver") or item.funcargs.get("driver_module")
        if driver:
            # Attach screenshot to Allure report
            try:
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name=f"FAIL — {item.name}",
                    attachment_type=allure.attachment_type.PNG,
                )
            except Exception:
                pass
            # Also save to file for plain HTML report
            os.makedirs("reports/screenshots", exist_ok=True)
            screenshot(driver, f"FAIL_{item.name}")
