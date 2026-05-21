#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════
#   Qatarat — USB Device Test Runner
#   Connect your Android phone via USB and run any test suite.
#   No emulator, no setup knowledge needed.
# ═══════════════════════════════════════════════════════════════════

set -e

# ── Colours ─────────────────────────────────────────────────────────
BOLD='\033[1m';    RESET='\033[0m'
GREEN='\033[0;32m'; YELLOW='\033[1;33m'
RED='\033[0;31m';   CYAN='\033[0;36m'
BLUE='\033[0;34m';  DIM='\033[2m'

log()     { echo -e "${GREEN}${BOLD}[✓]${RESET} $1"; }
warn()    { echo -e "${YELLOW}${BOLD}[!]${RESET} $1"; }
error()   { echo -e "${RED}${BOLD}[✗]${RESET} $1"; }
step()    { echo -e "\n${CYAN}${BOLD}▶  $1${RESET}"; }
info()    { echo -e "${DIM}    $1${RESET}"; }

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APK_PATH="$SCRIPT_DIR/../Qatarat (Lambda-Stage).apk"

# ── PATH setup ──────────────────────────────────────────────────────
export JAVA_HOME="/opt/homebrew/opt/openjdk@17"
export ANDROID_HOME="$HOME/Library/Android/sdk"
export PATH="$JAVA_HOME/bin:$HOME/.maestro/bin:$ANDROID_HOME/platform-tools:$PATH"

# ── Banner ──────────────────────────────────────────────────────────
clear
echo ""
echo -e "${CYAN}${BOLD}"
echo "  ██████╗  █████╗ ████████╗ █████╗ ██████╗  █████╗ ████████╗"
echo "  ██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝"
echo "  ██║  ██║███████║   ██║   ███████║██████╔╝███████║   ██║   "
echo "  ██║  ██║██╔══██║   ██║   ██╔══██║██╔══██╗██╔══██║   ██║   "
echo "  ██████╔╝██║  ██║   ██║   ██║  ██║██║  ██║██║  ██║   ██║   "
echo "  ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   "
echo -e "${RESET}"
echo -e "  ${BOLD}Qatarat (قطرات) — Mobile Test Runner${RESET}"
echo -e "  ${DIM}Android USB Device Edition${RESET}"
echo ""
echo "  ─────────────────────────────────────────────────────────"
echo ""

# ── Prerequisites check ─────────────────────────────────────────────
step "Checking tools..."

MISSING=()
command -v java    &>/dev/null || MISSING+=("Java 17  →  run: cd testing && ./install.sh")
command -v adb     &>/dev/null || MISSING+=("ADB      →  run: cd testing && ./install.sh")
command -v maestro &>/dev/null || MISSING+=("Maestro  →  run: cd testing && ./install.sh")

if [ ${#MISSING[@]} -gt 0 ]; then
  error "Missing tools:"
  for m in "${MISSING[@]}"; do echo -e "    ${RED}•${RESET} $m"; done
  echo ""
  read -p "  Run install.sh now? (y/n): " DO_INSTALL
  if [[ "$DO_INSTALL" =~ ^[Yy]$ ]]; then
    "$SCRIPT_DIR/install.sh"
    source ~/.zshrc 2>/dev/null || true
    export PATH="$JAVA_HOME/bin:$HOME/.maestro/bin:$ANDROID_HOME/platform-tools:$PATH"
  else
    exit 1
  fi
fi
log "All tools found"

# ── APK check ───────────────────────────────────────────────────────
if [ ! -f "$APK_PATH" ]; then
  error "APK not found at: $APK_PATH"
  echo ""
  echo "  Put 'Qatarat (Lambda-Stage).apk' in the project root folder."
  exit 1
fi
APK_SIZE=$(du -sh "$APK_PATH" | cut -f1)
log "APK found ($APK_SIZE)"

# ── USB device detection ────────────────────────────────────────────
step "Looking for a connected Android device..."
echo ""
echo -e "  ${YELLOW}How to enable USB Debugging on your Android phone:${RESET}"
echo -e "  ${DIM}1. Settings → About Phone → tap 'Build Number' 7 times${RESET}"
echo -e "  ${DIM}2. Settings → Developer Options → turn on 'USB Debugging'${RESET}"
echo -e "  ${DIM}3. Connect your phone via USB cable${RESET}"
echo -e "  ${DIM}4. Accept the 'Allow USB Debugging' dialog on your phone${RESET}"
echo ""

# Wait up to 30 seconds for a device
WAIT=0
while true; do
  DEVICE_LINE=$(adb devices 2>/dev/null | grep -v "^List\|^$\|^*" | grep "device$" | head -1)
  if [ -n "$DEVICE_LINE" ]; then
    DEVICE_ID=$(echo "$DEVICE_LINE" | awk '{print $1}')
    break
  fi
  if [ $WAIT -ge 30 ]; then
    error "No device found after 30 seconds."
    echo ""
    echo "  Make sure:"
    echo "  • USB Debugging is ON (see steps above)"
    echo "  • Phone is unlocked"
    echo "  • USB cable is properly connected"
    echo "  • You tapped 'Allow' on the USB debugging dialog"
    exit 1
  fi
  printf "\r  ${YELLOW}Waiting for device... ${WAIT}s${RESET} "
  sleep 1
  WAIT=$((WAIT + 1))
done

echo ""
echo ""
# Get device info
DEVICE_MODEL=$(adb -s "$DEVICE_ID" shell getprop ro.product.model 2>/dev/null | tr -d '\r')
DEVICE_ANDROID=$(adb -s "$DEVICE_ID" shell getprop ro.build.version.release 2>/dev/null | tr -d '\r')
DEVICE_NAME=$(adb -s "$DEVICE_ID" shell getprop ro.product.brand 2>/dev/null | tr -d '\r')

log "Device connected!"
echo ""
echo -e "  ${BOLD}Device:${RESET}  $DEVICE_NAME $DEVICE_MODEL"
echo -e "  ${BOLD}Android:${RESET} $DEVICE_ANDROID"
echo -e "  ${BOLD}ID:${RESET}      $DEVICE_ID"
echo ""

# ── Install APK ─────────────────────────────────────────────────────
step "Installing Qatarat app on device..."
adb -s "$DEVICE_ID" install -r "$APK_PATH" 2>&1 | grep -E "Success|Failure|error" || true
log "App installed"

# ── Test menu ───────────────────────────────────────────────────────
echo ""
echo "  ─────────────────────────────────────────────────────────"
echo -e "  ${BOLD}  What do you want to test?${RESET}"
echo "  ─────────────────────────────────────────────────────────"
echo ""
echo -e "  ${CYAN}${BOLD}  MAESTRO (quick UI flows)${RESET}"
echo -e "  ${BOLD}  1)${RESET} Smoke Suite        ${DIM}~5 min  — login, cart, checkout${RESET}"
echo -e "  ${BOLD}  2)${RESET} Full Regression     ${DIM}~20 min — all 11 flows${RESET}"
echo ""
echo -e "  ${CYAN}${BOLD}  SINGLE FLOWS${RESET}"
echo -e "  ${BOLD}  3)${RESET} Login / OTP"
echo -e "  ${BOLD}  4)${RESET} Cart + Add Items"
echo -e "  ${BOLD}  5)${RESET} Checkout + Payment selection"
echo -e "  ${BOLD}  6)${RESET} Gift Card"
echo -e "  ${BOLD}  7)${RESET} My Orders + Rating"
echo -e "  ${BOLD}  8)${RESET} Subscription"
echo -e "  ${BOLD}  9)${RESET} Multi-language"
echo ""
echo -e "  ${CYAN}${BOLD}  APPIUM (deep tests — needs Appium running)${RESET}"
echo -e "  ${BOLD}  a)${RESET} Payment Tests      ${DIM}card, Tabby, bank transfer${RESET}"
echo -e "  ${BOLD}  b)${RESET} Gift Card Tests"
echo -e "  ${BOLD}  c)${RESET} Subscription Tests"
echo -e "  ${BOLD}  d)${RESET} All Appium Tests    ${DIM}~45 min${RESET}"
echo ""
echo "  ─────────────────────────────────────────────────────────"
echo ""
read -p "  Enter choice [1-9, a-d]: " CHOICE
echo ""

# ── Run selection ───────────────────────────────────────────────────
run_maestro() {
  local FLOW="$1"
  local LABEL="$2"
  step "Running: $LABEL"
  maestro \
    --device "$DEVICE_ID" \
    test "$FLOW" \
    --format junit \
    --output "$SCRIPT_DIR/maestro/reports/device-run-$(date +%Y%m%d-%H%M%S).xml"
}

run_appium() {
  local MARKER="$1"
  local LABEL="$2"
  step "Running: $LABEL"

  # Start Appium if not running
  if ! curl -s http://127.0.0.1:4723/status &>/dev/null; then
    warn "Starting Appium server..."
    appium --port 4723 --log /tmp/appium-device.log &
    sleep 4
  fi

  DEVICE_MODE=device \
  ANDROID_UDID="$DEVICE_ID" \
    "$SCRIPT_DIR/appium/.venv/bin/python" -m pytest \
      "$SCRIPT_DIR/appium/tests/" \
      -m "$MARKER" -v \
      --html="$SCRIPT_DIR/appium/reports/device-run-$(date +%Y%m%d-%H%M%S).html" \
      --self-contained-html \
      --tb=short
}

mkdir -p "$SCRIPT_DIR/maestro/reports" "$SCRIPT_DIR/appium/reports/screenshots"

case "$CHOICE" in
  1) run_maestro "$SCRIPT_DIR/maestro/flows/suites/smoke.yaml"      "Smoke Suite" ;;
  2) run_maestro "$SCRIPT_DIR/maestro/flows/suites/regression.yaml" "Full Regression" ;;
  3) run_maestro "$SCRIPT_DIR/maestro/flows/02_login_otp.yaml"      "Login / OTP" ;;
  4) run_maestro "$SCRIPT_DIR/maestro/flows/05_cart_add_items.yaml" "Cart + Add Items" ;;
  5) run_maestro "$SCRIPT_DIR/maestro/flows/06_checkout_payment_select.yaml" "Checkout" ;;
  6) run_maestro "$SCRIPT_DIR/maestro/flows/07_gift_card.yaml"      "Gift Card" ;;
  7) run_maestro "$SCRIPT_DIR/maestro/flows/08_my_orders.yaml"      "My Orders + Rating" ;;
  8) run_maestro "$SCRIPT_DIR/maestro/flows/09_subscription.yaml"   "Subscription" ;;
  9) run_maestro "$SCRIPT_DIR/maestro/flows/10_multilanguage.yaml"  "Multi-language" ;;
  a|A) run_appium "payment"      "Payment Tests (card, Tabby, bank)" ;;
  b|B) run_appium "gift"         "Gift Card Tests" ;;
  c|C) run_appium "subscription" "Subscription Tests" ;;
  d|D) run_appium ""             "All Appium Tests" ;;
  *)
    warn "Invalid choice: $CHOICE"
    exit 1
    ;;
esac

# ── Summary ─────────────────────────────────────────────────────────
echo ""
echo "  ─────────────────────────────────────────────────────────"
log "Run complete!"
echo ""
echo -e "  ${BOLD}Reports saved to:${RESET}"
echo -e "  ${DIM}  Maestro: testing/maestro/reports/${RESET}"
echo -e "  ${DIM}  Appium:  testing/appium/reports/${RESET}"
echo ""
echo -e "  ${DIM}Run again anytime:  cd testing && ./run_on_device.sh${RESET}"
echo ""
