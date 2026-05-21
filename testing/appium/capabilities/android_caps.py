import os

ANDROID_CAPS = {
    "platformName": "Android",
    "appium:automationName": "Flutter",           # uses appium-flutter-driver
    "appium:app": os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../../Qatarat (Lambda-Stage).apk")
    ),
    "appium:appPackage": "com.qatarat.app",
    "appium:appActivity": "com.qatarat.app.MainActivity",
    "appium:noReset": False,
    "appium:fullReset": False,
    "appium:newCommandTimeout": 120,
    "appium:androidInstallTimeout": 90000,
    "appium:autoGrantPermissions": True,
    "appium:skipDeviceInitialization": False,
    # Flutter-specific
    "appium:retryBackoffTime": 500,
    "appium:maxRetryCount": 3,
}

# Caps for running on a real device (override UDID)
ANDROID_DEVICE_CAPS = {
    **ANDROID_CAPS,
    "appium:deviceName": os.environ.get("ANDROID_DEVICE_NAME", "Android Device"),
    "appium:udid": os.environ.get("ANDROID_UDID", ""),
    "appium:platformVersion": os.environ.get("ANDROID_VERSION", "13"),
}

# Caps for emulator
ANDROID_EMULATOR_CAPS = {
    **ANDROID_CAPS,
    "appium:deviceName": os.environ.get("ANDROID_EMU_NAME", "Pixel_7_API_34"),
    "appium:avd": os.environ.get("ANDROID_AVD", "Pixel_7_API_34"),
    "appium:platformVersion": "14",
    "appium:isHeadless": False,
}
