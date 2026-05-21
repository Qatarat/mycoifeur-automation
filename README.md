# Qatarat (قطرات) — Mobile App Test Suite

[![Maestro Smoke](../../actions/workflows/01-maestro-smoke.yml/badge.svg)](../../actions/workflows/01-maestro-smoke.yml)
[![Maestro Regression](../../actions/workflows/02-maestro-regression.yml/badge.svg)](../../actions/workflows/02-maestro-regression.yml)
[![Appium Deep Tests](../../actions/workflows/03-appium-android.yml/badge.svg)](../../actions/workflows/03-appium-android.yml)

**Flutter app** · Android & iOS · Package: `com.qatarat.app`

---

## Test on your phone (USB) — anyone can do this

```bash
# 1. Clone the repo
git clone https://github.com/mejbaurbahar/Qatarat.git
cd Qatarat/testing

# 2. Install all tools (Java, ADB, Maestro, Appium, Python)
./install.sh
source ~/.zshrc

# 3. Enable USB Debugging on your phone:
#    Settings → About Phone → tap Build Number 7 times
#    Settings → Developer Options → turn on USB Debugging
#    Connect phone via USB → tap Allow on the dialog

# 4. Run — an interactive menu will appear
./run_on_device.sh
```

The script auto-detects your phone, installs the app, and shows a menu to pick what to test. No commands to memorize.

---

## Test credentials

| Field | Value |
|-------|-------|
| Phone | `8801685220417` |
| OTP   | `1234` |

---

## CI / CD — GitHub Actions (fully free)

| Workflow | Trigger | Duration | What it tests |
|----------|---------|----------|---------------|
| Maestro Smoke | Every push / PR | ~10 min | Login, cart, checkout |
| Maestro Regression | Nightly 01:00 UTC | ~30 min | All 11 user flows |
| Appium Deep Tests | Every Monday | ~60 min | Payment, gifts, subscriptions |
| Maestro iOS | Manual only | ~20 min | Smoke on iOS Simulator |

### Run a workflow manually

Go to **[Actions tab](../../actions)** → pick a workflow → click **Run workflow**.

- Regression accepts a flow number (e.g. `07` to run only the gift card flow)
- Appium accepts a marker: `payment`, `gift`, `subscription`, or leave empty for all

---

## What is tested

### Phase 1 — Maestro flows

| Flow | Coverage |
|------|----------|
| `01` Splash / Onboarding | Country + language selection |
| `02` Login OTP | Phone `8801685220417` → OTP `1234` |
| `03` Guest User | Browsing without login + gate check |
| `04` Browse Services | Mosque listing + selection |
| `05` Cart | Add items, quantity, price |
| `06` Checkout | Payment method selection + promo code |
| `07` Gift Card | Full send flow + WhatsApp preview |
| `08` My Orders | List, detail view, rating |
| `09` Subscription | Weekly / monthly recurring donation |
| `10` Multi-language | Arabic, Turkish, Urdu, English |
| `11` No Internet | Offline error screen |

### Phase 2 — Appium deep tests

| File | Coverage |
|------|----------|
| `test_card_payment.py` | HyperPay card, expired card, declined, promo |
| `test_tabby_bnpl.py` | Tabby BNPL, Shariah info, cancel flow |
| `test_bank_transfer.py` | Account details, receipt upload prompt |
| `test_gift_card.py` | Fields, preview accuracy, validation errors |
| `test_subscription.py` | Weekly, monthly, skip, unavailable items |
| `test_live_broadcast.py` | Live broadcast screen, visual docs |

---

## Local commands (after install)

```bash
cd testing

./run_on_device.sh              # interactive USB device menu

./run_maestro.sh                # smoke suite (emulator/CI)
./run_maestro.sh regression     # full regression
./run_maestro.sh flow 07        # single flow (e.g. gift card)

./run_appium.sh payment         # payment tests only
./run_appium.sh gift            # gift card tests only
./run_appium.sh subscription    # subscription tests only
./run_appium.sh                 # all Appium tests
```
