#!/usr/bin/env bash
# Run Appium tests — auto-starts an Android emulator if none is connected.
# Usage:
#   bash run_appium.sh                        — all tests (Android emulator)
#   bash run_appium.sh payment                — payment tests only
#   bash run_appium.sh gift                   — gift card tests only
#   bash run_appium.sh subscription           — subscription tests only
#   bash run_appium.sh account                — profile & account tests only
#   PLATFORM=ios bash run_appium.sh           — iOS tests
#   DEVICE_MODE=device bash run_appium.sh     — real device (skip emulator launch)

set -uo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR/appium"

PLATFORM="${PLATFORM:-android}"
DEVICE_MODE="${DEVICE_MODE:-emulator}"
MARKER="${1:-}"
STARTED_EMU=false
EMU_PID=""

export PLATFORM DEVICE_MODE

# ── Use venv Python ──────────────────────────────────────────────────────────
VENV_PYTHON=".venv/bin/python"
if [ ! -f "$VENV_PYTHON" ]; then
  echo "⚠  venv not found — run install.sh first"
  VENV_PYTHON="python3"
fi

# ── Cleanup on exit ──────────────────────────────────────────────────────────
cleanup() {
  if [ "$STARTED_EMU" = "true" ] && [ -n "$EMU_PID" ]; then
    echo ""
    echo "▶  Shutting down emulator (PID $EMU_PID)..."
    kill "$EMU_PID" 2>/dev/null || true
  fi
}
trap cleanup EXIT

# ── Find Android emulator binary ─────────────────────────────────────────────
find_emulator() {
  local candidates=(
    "${ANDROID_HOME:-}/emulator/emulator"
    "$HOME/Library/Android/sdk/emulator/emulator"
    "$HOME/Android/Sdk/emulator/emulator"
    "/usr/local/bin/emulator"
    "$(which emulator 2>/dev/null || true)"
  )
  for c in "${candidates[@]}"; do
    [ -x "$c" ] && echo "$c" && return 0
  done
  return 1
}

# ── Auto-start emulator if needed ────────────────────────────────────────────
if [ "$PLATFORM" = "android" ] && [ "$DEVICE_MODE" = "emulator" ]; then
  CONNECTED=$(adb devices 2>/dev/null | grep -v "List of devices" | grep -v "^$" | grep -c "device$" || true)

  if [ "${CONNECTED:-0}" -eq 0 ]; then
    echo "▶  No Android device connected — looking for emulator..."

    EMU_BIN=$(find_emulator || true)

    if [ -z "$EMU_BIN" ]; then
      echo ""
      echo "✗  Android emulator not found."
      echo "   Install it via Android Studio:"
      echo "     1. Download Android Studio: https://developer.android.com/studio"
      echo "     2. Open SDK Manager → SDK Tools → check 'Android Emulator'"
      echo "     3. Open Device Manager → Create Virtual Device → Pixel 7 / API 34"
      echo "     4. Re-run: bash run_appium.sh"
      echo ""
      echo "   Or install SDK command-line tools and run:"
      echo "     sdkmanager 'emulator' 'system-images;android-34;google_apis;arm64-v8a'"
      echo "     avdmanager create avd -n Pixel_7_API_34 -k 'system-images;android-34;google_apis;arm64-v8a'"
      exit 1
    fi

    # Pick AVD: prefer what caps expect, fall back to first available
    PREFERRED_AVD="${ANDROID_AVD:-Pixel_7_API_34}"
    AVDS=$("$EMU_BIN" -list-avds 2>/dev/null || true)

    if echo "$AVDS" | grep -qxF "$PREFERRED_AVD"; then
      AVD="$PREFERRED_AVD"
    else
      AVD=$(echo "$AVDS" | grep -v "^$" | head -1)
    fi

    if [ -z "$AVD" ]; then
      echo ""
      echo "✗  No AVDs found. Create one first:"
      echo "   Android Studio → Device Manager → Create Virtual Device"
      echo "   Recommended: Pixel 7 / API 34 (arm64)"
      echo ""
      echo "   Or via command line:"
      echo "     sdkmanager 'system-images;android-34;google_apis;arm64-v8a'"
      echo "     avdmanager create avd -n Pixel_7_API_34 -k 'system-images;android-34;google_apis;arm64-v8a'"
      exit 1
    fi

    echo "   Launching AVD: $AVD"
    "$EMU_BIN" -avd "$AVD" -no-snapshot-load -no-audio -no-boot-anim -no-window &
    EMU_PID=$!
    STARTED_EMU=true
    echo "   Emulator PID: $EMU_PID — waiting for boot (up to 3 min)..."

    # Wait for adb to see the device
    adb wait-for-device 2>/dev/null

    # Wait for sys.boot_completed=1
    BOOT_TIMEOUT=180
    ELAPSED=0
    BOOT=""
    while [ "$ELAPSED" -lt "$BOOT_TIMEOUT" ]; do
      BOOT=$(adb shell getprop sys.boot_completed 2>/dev/null | tr -d '\r\n' || true)
      [ "$BOOT" = "1" ] && break
      sleep 3
      ELAPSED=$((ELAPSED + 3))
      printf "   Boot wait: %ds / %ds\r" "$ELAPSED" "$BOOT_TIMEOUT"
    done
    echo ""

    if [ "$BOOT" != "1" ]; then
      echo "✗  Emulator did not boot within ${BOOT_TIMEOUT}s — aborting."
      exit 1
    fi

    # Dismiss keyguard
    adb shell input keyevent 82 2>/dev/null || true
    sleep 1
    echo "   Emulator ready."
  else
    echo "   Device already connected (${CONNECTED} found)."
  fi
fi

# ── Start Appium server if not running ───────────────────────────────────────
if ! curl -s http://127.0.0.1:4723/status > /dev/null 2>&1; then
  echo "▶  Starting Appium server..."
  appium --port 4723 --log appium.log &
  APPIUM_PID=$!
  sleep 4
  echo "   Appium started (PID $APPIUM_PID)"
else
  echo "   Appium already running on :4723"
fi

mkdir -p reports/screenshots

# ── Run tests ────────────────────────────────────────────────────────────────
if [ -n "$MARKER" ]; then
  echo "▶  Running Appium tests [platform=$PLATFORM, marker=$MARKER]..."
  "$VENV_PYTHON" -m pytest tests/ -m "$MARKER" -v \
    --html="reports/report.html" --self-contained-html \
    --junit-xml="reports/results.xml" \
    --alluredir="allure-results" \
    --tb=short
else
  echo "▶  Running ALL Appium tests [platform=$PLATFORM]..."
  "$VENV_PYTHON" -m pytest tests/ -v \
    --html="reports/report.html" --self-contained-html \
    --junit-xml="reports/results.xml" \
    --alluredir="allure-results" \
    --tb=short
fi

RC=$?
echo ""
echo "✓ Appium run complete (exit $RC)"
echo "  HTML report: $(pwd)/reports/report.html"
exit $RC
