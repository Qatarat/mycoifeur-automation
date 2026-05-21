# Qatarat — Full Automation Testing Suite

**App:** Qatarat (قطرات) — Flutter, `com.qatarat.app`
**Environment:** Lambda Stage APK

---

## Quick Start

```bash
# 1. Install everything (Java, ADB, Maestro, Appium, Python deps)
cd testing
./install.sh

# 2. Restart terminal (reload PATH)
source ~/.zshrc

# 3. Connect Android device or start emulator, then:
./run_maestro.sh           # Phase 1 smoke (5 min)
./run_maestro.sh regression  # Phase 1 full (20 min)
./run_appium.sh payment    # Phase 2 payment deep tests
./run_appium.sh            # Phase 2 all tests
```

---

## Phase 1 — Maestro (smoke + regression)

| Flow | What it tests |
|------|---------------|
| `01_splash_onboarding` | Country + language selection |
| `02_login_otp` | Phone + OTP login |
| `03_guest_user` | Guest browsing + login gate |
| `04_browse_services` | Mosque listing + selection |
| `05_cart_add_items` | Add items, quantity, price |
| `06_checkout_payment_select` | Payment method selection + promo code |
| `07_gift_card` | Full gift card send flow |
| `08_my_orders` | Orders list + detail + rating |
| `09_subscription` | Weekly/monthly recurring donation |
| `10_multilanguage` | Arabic, Turkish, Urdu, English |
| `11_no_internet` | Offline error screen |

### Run a single flow
```bash
./run_maestro.sh flow 07   # runs 07_gift_card.yaml
```

### iOS (Maestro)
```bash
./run_maestro.sh ios       # requires iOS device or simulator connected
```

---

## Phase 2 — Appium (deep payment + complex flows)

| Test file | What it tests |
|-----------|---------------|
| `tests/payment/test_card_payment.py` | HyperPay card, expired card, declined, promo |
| `tests/payment/test_tabby_bnpl.py` | Tabby BNPL visibility, Shariah info, cancel |
| `tests/payment/test_bank_transfer.py` | Bank account info, receipt upload prompt |
| `tests/gift/test_gift_card.py` | Fields, preview, validation, received section |
| `tests/subscription/test_subscription.py` | Weekly/monthly, skip, banner, unavailable items |
| `tests/streaming/test_live_broadcast.py` | Live Broadcast screen, visual docs |

### Run by category
```bash
cd appium
python3 -m pytest tests/ -m payment       # payment tests only
python3 -m pytest tests/ -m gift          # gift tests only
python3 -m pytest tests/ -m subscription  # subscription tests only
python3 -m pytest tests/ -v               # all tests
```

### Switch platform
```bash
PLATFORM=ios ./run_appium.sh
PLATFORM=android DEVICE_MODE=device ./run_appium.sh
```

### Reports
- HTML report: `appium/reports/report.html`
- Screenshots (on failure): `appium/reports/screenshots/`

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PLATFORM` | `android` | `android` or `ios` |
| `DEVICE_MODE` | `emulator` | `emulator` or `device` |
| `ANDROID_UDID` | — | Real device UDID (from `adb devices`) |
| `IOS_UDID` | — | Real iOS device UDID |
| `APPIUM_SERVER` | `http://127.0.0.1:4723` | Appium server URL |
| `IOS_APP_PATH` | — | Path to `.ipa` or `.app` for iOS |

---

## Prerequisites Summary

| Tool | Required by | Install |
|------|-------------|---------|
| Java 17 | Maestro, Appium | `brew install --cask temurin@17` |
| Android Studio / ADB | Both | `brew install --cask android-commandlinetools` |
| Maestro | Phase 1 | `curl -Ls https://get.maestro.mobile.dev \| bash` |
| Node.js 18+ | Phase 2 | Already installed (v25) |
| Appium 2 | Phase 2 | `npm install -g appium` |
| appium-flutter-driver | Phase 2 | `appium driver install --source=npm appium-flutter-driver` |
| uiautomator2 driver | Phase 2 Android | `appium driver install uiautomator2` |
| xcuitest driver | Phase 2 iOS | `appium driver install xcuitest` |
| Python 3 + deps | Phase 2 | `pip3 install -r appium/requirements.txt` |

> For iOS testing you also need **full Xcode** (not just Command Line Tools).
> Run: `! xcode-select --install` and then install Xcode from the App Store.
