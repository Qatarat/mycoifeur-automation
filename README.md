# MyCoiffeur — Mobile App Test Suite

[![Maestro Smoke](https://github.com/mejbaurbahar/MyCoifeur/actions/workflows/01-maestro-smoke.yml/badge.svg)](https://github.com/mejbaurbahar/MyCoifeur/actions/workflows/01-maestro-smoke.yml)
[![Maestro Regression](https://github.com/mejbaurbahar/MyCoifeur/actions/workflows/02-maestro-regression.yml/badge.svg)](https://github.com/mejbaurbahar/MyCoifeur/actions/workflows/02-maestro-regression.yml)
[![Appium Deep Tests](https://github.com/mejbaurbahar/MyCoifeur/actions/workflows/03-appium-android.yml/badge.svg)](https://github.com/mejbaurbahar/MyCoifeur/actions/workflows/03-appium-android.yml)

**Flutter app** · Android & iOS · Package `com.example.my_coiffeur`

📊 **[View Live Test Report →](https://mejbaurbahar.github.io/MyCoifeur/)**

🔗 **[GitHub Repository →](https://github.com/mejbaurbahar/MyCoifeur)**

---

## Test on your phone (USB) — anyone can do this

### macOS / Linux

```bash
# 1. Clone the repo
git clone https://github.com/mejbaurbahar/MyCoifeur.git
cd MyCoifeur/testing

# 2. Install all tools (Java, ADB, Maestro, Appium, Python, scrcpy)
bash install.sh
source ~/.zshrc        # or source ~/.bashrc on Linux

# 3. Enable USB Debugging on your Android phone:
#    Settings → About Phone → tap Build Number 7 times
#    Settings → Developer Options → turn on USB Debugging
#    Connect phone via USB → tap Allow on the dialog that appears

# 4. Launch the interactive menu (auto-detects device + offers screen mirror)
bash run_on_device.sh
```

### Windows (WSL — recommended)

WSL (Windows Subsystem for Linux) lets you run the full test suite on Windows without any manual tool installation.

**One-time WSL setup (PowerShell as Administrator):**

```powershell
wsl --install
# Restart your PC when prompted
```

**After restart — open the WSL (Ubuntu) terminal:**

```bash
# Clone into WSL filesystem (faster I/O than /mnt/c or /mnt/h)
cd ~
git clone https://github.com/mejbaurbahar/MyCoifeur.git
cd MyCoifeur/testing

# Install everything automatically
bash install.sh
source ~/.bashrc

# Connect your Android phone via USB, then:
bash run_on_device.sh
```

> **USB devices in WSL:** WSL 2 needs [usbipd-win](https://github.com/dorssel/usbipd-win) to pass USB devices through.
> Install it from that link, then in an **elevated PowerShell**:
> ```powershell
> usbipd list                    # find your phone's BUSID
> usbipd attach --wsl --busid <BUSID>
> ```
> Then in WSL: `adb devices` should show your phone.

**Alternatively — run directly from Windows (no WSL):**

If you prefer native Windows, install each tool manually:

| Tool | Download |
|------|----------|
| Java 17 | https://adoptium.net/temurin/releases/?version=17 |
| Android Platform Tools (ADB) | https://developer.android.com/tools/releases/platform-tools |
| Node.js LTS | https://nodejs.org |
| Python 3 | https://www.python.org/downloads/ |

Then in **PowerShell**:
```powershell
# Maestro
iex "& { $(irm 'https://get.maestro.mobile.dev') }"

# Appium
npm install -g appium
appium driver install uiautomator2
appium driver install --source=npm appium-flutter-driver

# Python deps
cd H:\MyCoifeur\testing
python -m venv appium\.venv
appium\.venv\Scripts\pip install -r appium\requirements.txt

# Run Maestro flows (use Git Bash for .sh scripts)
bash run_maestro.sh
```

---

## Screen mirror (see the real device while tests run)

Connect your Android phone via USB and see every tap, animation, and assertion on your PC screen in real time — on any PC, even low-storage ones.

```bash
cd testing

bash mirror.sh             # basic mirror
bash mirror.sh --record    # mirror + save video to mirror_recordings/
bash mirror.sh --watch     # auto-relaunch mirror each time phone reconnects
bash mirror.sh --low-cpu   # 720p + no audio (saves CPU on slow machines)
bash mirror.sh --help      # show all options
```

> **Runs inside `run_on_device.sh`** — when you use the interactive menu it asks automatically if you want to start the mirror. You can also toggle it mid-session with option `m`, or start a recording session with option `r`.

**Why it works on low-storage / slow PCs:**
- The phone's own GPU encodes the video stream (H.264) — the PC only decodes
- Binary is ~10 MB, no Android Studio needed
- Typical CPU usage: 2–5%
- No temp files written during mirroring

**Keyboard shortcuts while mirroring:**

| Shortcut | Action |
|----------|--------|
| Ctrl+Shift+H | Home button |
| Ctrl+Shift+B | Back button |
| Ctrl+Shift+P | Power / wake |
| Ctrl+V | Paste clipboard to phone |
| Close window / Ctrl+C | Stop mirror |

---

## Tech stack

| Layer | Technology |
|-------|-----------|
| **App** | Flutter / Dart |
| **UI automation** | [Maestro](https://maestro.mobile.dev) 2.x — YAML flows |
| **Deep tests** | [Appium](https://appium.io) 2.x + `appium-flutter-driver` + `uiautomator2` |
| **Test language** | Python 3 with `pytest` |
| **Screen mirror** | [scrcpy](https://github.com/Genymobile/scrcpy) — USB, zero install on phone |
| **Reporting** | [Allure](https://allurereport.org) + GitHub Pages dashboard |
| **CI / CD** | GitHub Actions (free — Ubuntu + Android emulator) |
| **Device** | Android API 34 emulator (CI) or any USB Android phone (local) |

---

## CI / CD — GitHub Actions (all free)

| Workflow | Trigger | Duration | Coverage |
|----------|---------|----------|----------|
| Maestro Smoke | Every push / PR | ~10 min | Login, booking, home feed |
| Maestro Regression | Nightly 01:00 UTC | ~35 min | All 40 flows |
| Appium Deep Tests | Every Monday | ~60 min | Booking, payment, wallet, account |
| Maestro iOS | Manual only | ~20 min | Smoke on iOS Simulator |
| Publish Report | After any test run | ~3 min | Deploys to GitHub Pages |

**Run any workflow manually:** [Actions tab](https://github.com/mejbaurbahar/MyCoifeur/actions) → pick workflow → **Run workflow**

> **First-time setup:** Go to **Settings → Pages → Source → GitHub Actions** to enable the report page.

---

## What is tested (full coverage)

### Maestro flows — 40 flows (25 happy-path + 15 MyCoiffeur-specific)

**Core happy-path flows**

| # | Flow | What it covers |
|---|------|---------------|
| 01 | Splash / Onboarding | Country + language selection |
| 02 | Login OTP | Phone → OTP → logged in |
| 03 | Guest User | Guest browsing + login gate |
| 04 | Browse Services | Salon listing + selection |
| 05 | Cart | Add items, quantity, price, tax |
| 06 | Checkout | Payment method + promo code |
| 07 | Gift Card | Full send flow + WhatsApp preview |
| 08 | My Orders | List, detail, rating |
| 09 | Subscription | Weekly / monthly recurring |
| 10 | Multi-language | Arabic, Turkish, Urdu, English |
| 11 | No Internet | Offline error screen |
| 12 | Profile & Settings | Currency, About, Logout dialog |
| 13 | Help & Support | Help centre, WhatsApp, email |
| 14 | Manage Subscriptions | Active list, billing history, cancel |
| 15 | Cancel Order | Cancel dialog, confirm/decline |
| 16 | Share App | Referral link sharing |

**Negative & boundary flows**

| # | Flow | What it covers |
|---|------|---------------|
| 17 | Login Invalid Phone | Empty, too-short, alpha, special-char phone all blocked |
| 18 | Login Wrong OTP | Wrong digits, all-zeros OTP rejected; resend link visible |
| 19 | Invalid Promo Codes | Wrong, empty, special-char, SQL injection all rejected |
| 20 | Empty Cart Checkout | Checkout blocked when cart is empty |
| 21 | Gift Card Validation | Empty form, invalid phone, XSS, SQL injection |
| 22 | Cart Quantity Boundary | 10× increment, decrement below 1, NaN check |
| 23 | App Background Resume | Cart state preserved after backgrounding |
| 24 | Browse Search Edges | Empty, Arabic, XSS, SQL, gibberish queries |
| 25 | Payment Input Edges | Spaces, CAPS, far-future expiry, zeros |

**MyCoiffeur-specific flows**

| # | Flow | What it covers |
|---|------|---------------|
| 26 | Home Feed | Carousel scrolling, banner taps, featured providers |
| 27 | Booking Flow | Select provider, date, time slot → confirm |
| 28 | Booking Reschedule | Change date and time of existing booking |
| 29 | Booking Cancel | Cancel booking, confirm dialog |
| 30 | Notifications | Notification list, mark-read, deep link |
| 31 | Wallet Balance | Balance display, top-up CTA, history |
| 32 | Ratings & Reviews | Post booking rating, comment, star picker |
| 33 | Map Location | Salon map pins, detail sheet, directions |
| 34 | Favourites | Add/remove favourite, list persistence |
| 35 | Refer a Friend | Referral link share sheet, copy link |
| 36 | Dark Mode | Toggle dark/light, colour-scheme preserves state |
| 37 | Accessibility Labels | Content descriptions, focus order, TalkBack |
| 38 | Session Timeout | Idle 30 min, auto-logout, re-login prompt |
| 39 | Deep Link / QR | Open via QR code, deep-link to booking screen |
| 40 | App Update Prompt | In-app update dialog, dismiss, force-update |

### Appium deep tests — 119 tests (across 18 test files)

| Group | File | Tests |
|-------|------|-------|
| Payment | `test_card_payment.py` | HyperPay card success, expired card, declined, promo code |
| Payment | `test_tabby_bnpl.py` | Tabby visibility, Shariah badge, Learn More, cancel |
| Payment | `test_bank_transfer.py` | Account details, receipt upload prompt, photo/gallery options |
| Payment | `test_payment_negative.py` | Invalid card numbers, bad expiry, empty CVV, blank name |
| Payment | `test_payment_extended.py` | Card formatting, expiry edge cases, cardholder validation |
| Commerce | `test_gift_card.py` | Field validation, preview accuracy, gifts received section |
| Commerce | `test_gift_card_boundary.py` | XSS in message, SQL injection, Arabic names, invalid phone |
| Commerce | `test_subscription.py` | Weekly, monthly, skip, success banner, unavailable items |
| Commerce | `test_subscription_boundary.py` | Back-button resets, frequency options, cancel declined |
| Commerce | `test_cart_boundary.py` | Empty cart checkout, NaN on high quantity, decrement below 1 |
| Commerce | `test_promo_codes.py` | Expired codes, SQL injection, case sensitivity, spaces |
| Auth | `test_login_negative.py` | Alpha/empty/short phone accepted? Wrong OTP lets you in? |
| Auth | `test_auth_edge_cases.py` | Leading spaces, plus prefix, emoji, special chars |
| Catalog | `test_browse_search.py` | Single char, Arabic text, XSS, SQL, gibberish, clear search |
| Checkout | `test_checkout_edge_cases.py` | Back navigation, payment switching, coupon + payment |
| Account | `test_profile.py` | Currency, About page, logout dialog, delete account |
| Account | `test_profile_edge_cases.py` | SQL in help search, logout cancel, empty search state |
| Account | `test_orders_edge_cases.py` | Empty feedback, special-char search, cancel flow |

---

## Local commands

```bash
cd testing

bash run_on_device.sh              # interactive USB device menu (auto-detects phone)

# Screen mirror (standalone)
bash mirror.sh                     # mirror phone screen to PC
bash mirror.sh --record            # mirror + record to mirror_recordings/
bash mirror.sh --watch             # auto-relaunch on reconnect
bash mirror.sh --low-cpu           # 720p mode for older / low-storage PCs

bash run_maestro.sh                # smoke suite (5 flows)
bash run_maestro.sh regression     # full regression (all 40 flows)
bash run_maestro.sh negative       # negative/boundary flows only
bash run_maestro.sh flow 27        # single flow by number (e.g. booking flow)

bash run_appium.sh payment         # payment tests
bash run_appium.sh gift            # gift card tests
bash run_appium.sh subscription    # subscription tests
bash run_appium.sh account         # profile & account tests
bash run_appium.sh                 # all Appium tests

# Run only negative tests (Appium)
cd appium && python -m pytest tests/ -m negative -v

# Run only boundary tests
cd appium && python -m pytest tests/ -m boundary -v
```
