import os
import pytest
from appium import webdriver
from capabilities.android_caps import ANDROID_DEVICE_CAPS, ANDROID_EMULATOR_CAPS
from capabilities.ios_caps import IOS_DEVICE_CAPS, IOS_SIMULATOR_CAPS
from utils.helpers import APPIUM_SERVER, screenshot

PLATFORM = os.environ.get("PLATFORM", "android").lower()
DEVICE_MODE = os.environ.get("DEVICE_MODE", "emulator").lower()  # emulator | device


def get_caps():
    if PLATFORM == "android":
        return ANDROID_DEVICE_CAPS if DEVICE_MODE == "device" else ANDROID_EMULATOR_CAPS
    elif PLATFORM == "ios":
        return IOS_DEVICE_CAPS if DEVICE_MODE == "device" else IOS_SIMULATOR_CAPS
    raise ValueError(f"Unknown platform: {PLATFORM}")


@pytest.fixture(scope="function")
def driver():
    caps = get_caps()
    d = webdriver.Remote(APPIUM_SERVER, caps)
    d.implicitly_wait(10)
    yield d
    d.quit()


@pytest.fixture(scope="module")
def driver_module():
    """Module-scoped driver — reused across tests in the same module (faster)."""
    caps = get_caps()
    caps = {**caps, "appium:noReset": True}      # keep state between tests
    d = webdriver.Remote(APPIUM_SERVER, caps)
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
            os.makedirs("reports/screenshots", exist_ok=True)
            path = screenshot(driver, f"FAIL_{item.name}")
            print(f"\nScreenshot saved: {path}")
