# Qatarat — Full Automation Testing Suite

**App:** Qatarat (قطرات) — Flutter, `com.qatarat.app`
**Environment:** Lambda Stage APK

---

## Quick Start — USB Device (easiest)

```bash
# 1. Install all tools (includes scrcpy for screen mirroring)
cd testing && ./install.sh && source ~/.zshrc

# 2. Plug in your Android phone → enable USB Debugging → run:
./run_on_device.sh
```

The script detects your phone, installs the APK, and shows a menu.
If scrcpy is installed it immediately asks **"Mirror phone screen? [Y/n]"** — say Y and the phone screen appears on your PC so you can watch every test step live.

---

## Phase 0 — Screen Mirror (new)

See the real device screen on your PC while any test runs. Works even on low-storage machines — the phone's GPU does the encoding, your PC only decodes (~2–5% CPU).

```bash
# Standalone mirror commands
./mirror.sh                   # basic mirror via USB
./mirror.sh --record          # mirror + auto-save session video
./mirror.sh --watch           # auto-relaunch when phone reconnects
./mirror.sh --low-cpu         # 720p + no audio (for older PCs)
./mirror.sh --help
```

**Inside `run_on_device.sh`:** after the device connects, the script offers to start the mirror automatically. From the test menu you can also:
- Press `m` — toggle mirror on/off mid-session
- Press `r` — start mirror + recording at any point

**Install scrcpy** (if not already done by `install.sh`):

| OS | Command |
|----|---------|
| macOS | `brew install scrcpy` |
| Ubuntu 22.04+ | `sudo apt install scrcpy` |
| Older Ubuntu | `sudo snap install scrcpy` |
| Windows (WSL) | Install scrcpy on **Windows** side from [github.com/Genymobile/scrcpy](https://github.com/Genymobile/scrcpy/releases) — WSL can't open GUI windows directly |

> **Windows note:** On Windows run scrcpy.exe natively, not inside WSL. Plug in your phone, open a regular PowerShell/CMD window in the scrcpy folder, and run `scrcpy.exe`. Maestro/Appium can still run from WSL simultaneously.

---

## Quick Start — CI / Emulator

```bash
# Local emulator or CI
./run_maestro.sh           # smoke (5 min)
./run_maestro.sh regression  # all flows (20 min)
./run_appium.sh payment    # payment deep tests
./run_appium.sh            # all Appium tests
```

---

## Test credentials

| Field | Value |
|-------|-------|
| Phone | `8801685220417` |
| OTP   | `1234` |

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
| **scrcpy** | **Phase 0 (mirror)** | **`brew install scrcpy`** (Mac) · `sudo apt install scrcpy` (Linux) |

> All of the above are installed automatically by running **`bash install.sh`**.

> For iOS testing you also need **full Xcode** (not just Command Line Tools).
> Run: `! xcode-select --install` and then install Xcode from the App Store.
