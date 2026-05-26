#!/usr/bin/env bash
# Run Appium tests — fully automatic.
# First run: downloads Android SDK + system image (~1.5 GB), creates AVD, boots emulator.
# Subsequent runs: boots emulator in ~60 s, runs tests, shuts down on exit.
#
# Usage:
#   bash run_appium.sh                  — all tests
#   bash run_appium.sh payment          — payment tests only
#   bash run_appium.sh gift|subscription|account|streaming
#   DEVICE_MODE=device bash run_appium.sh  — skip emulator, use real phone

set -uo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR/appium"

PLATFORM="${PLATFORM:-android}"
DEVICE_MODE="${DEVICE_MODE:-emulator}"
MARKER="${1:-}"
STARTED_EMU=false
EMU_PID=""

export PLATFORM DEVICE_MODE

# ── venv Python ──────────────────────────────────────────────────────────────
VENV_PYTHON=".venv/bin/python"
[ ! -f "$VENV_PYTHON" ] && { echo "⚠  venv not found — run install.sh first"; VENV_PYTHON="python3"; }

# ── Cleanup on exit ──────────────────────────────────────────────────────────
cleanup() {
  if [ "$STARTED_EMU" = "true" ] && [ -n "$EMU_PID" ]; then
    echo ""
    echo "▶  Shutting down emulator (PID $EMU_PID)..."
    kill "$EMU_PID" 2>/dev/null || true
  fi
}
trap cleanup EXIT INT TERM

# ════════════════════════════════════════════════════════════════════════════
# Android SDK auto-setup
# ════════════════════════════════════════════════════════════════════════════
SDK_DIR="${ANDROID_HOME:-$HOME/.qatarat-android-sdk}"
CMDLINE_BIN="$SDK_DIR/cmdline-tools/latest/bin"

_sdk_url() {
  local build="11076708"   # cmdline-tools 2024.2 — stable on arm64 + x86_64
  case "$(uname)-$(uname -m)" in
    Darwin-*)  echo "https://dl.google.com/android/repository/commandlinetools-mac-${build}_latest.zip" ;;
    Linux-*)   echo "https://dl.google.com/android/repository/commandlinetools-linux-${build}_latest.zip" ;;
    *)         echo ""; return 1 ;;
  esac
}

ensure_cmdline_tools() {
  [ -f "$CMDLINE_BIN/sdkmanager" ] && return 0
  local url; url=$(_sdk_url)
  echo "▶  Downloading Android cmdline-tools (~120 MB, one-time)..."
  mkdir -p "$SDK_DIR/cmdline-tools"
  curl -L --progress-bar "$url" -o /tmp/qatarat_cmdtools.zip
  unzip -q /tmp/qatarat_cmdtools.zip -d "$SDK_DIR/cmdline-tools/"
  # The zip extracts as "cmdline-tools/"; rename to "latest/"
  if [ -d "$SDK_DIR/cmdline-tools/cmdline-tools" ]; then
    mv "$SDK_DIR/cmdline-tools/cmdline-tools" "$SDK_DIR/cmdline-tools/latest"
  fi
  rm -f /tmp/qatarat_cmdtools.zip
  echo "   cmdline-tools ready."
}

ensure_emulator_binary() {
  [ -f "$SDK_DIR/emulator/emulator" ] && return 0
  echo "▶  Installing Android emulator (via sdkmanager)..."
  yes | "$CMDLINE_BIN/sdkmanager" --sdk_root="$SDK_DIR" --licenses > /dev/null 2>&1 || true
  "$CMDLINE_BIN/sdkmanager" --sdk_root="$SDK_DIR" "emulator" "platform-tools"
  echo "   Emulator binary ready."
}

ensure_system_image() {
  local arch; arch=$(uname -m)
  local abi; abi=$([ "$arch" = "arm64" ] && echo "arm64-v8a" || echo "x86_64")
  SYS_IMAGE="system-images;android-34;google_apis;${abi}"

  if "$CMDLINE_BIN/sdkmanager" --sdk_root="$SDK_DIR" --list_installed 2>/dev/null \
       | grep -q "system-images;android-34"; then
    return 0
  fi

  echo "▶  Downloading Android 34 system image for ${abi} (~1.5 GB, one-time)..."
  echo "   Grab a coffee — this only happens once."
  yes | "$CMDLINE_BIN/sdkmanager" --sdk_root="$SDK_DIR" --licenses > /dev/null 2>&1 || true
  "$CMDLINE_BIN/sdkmanager" --sdk_root="$SDK_DIR" "$SYS_IMAGE"
  echo "   System image ready."
}

ensure_avd() {
  local avd_name="${ANDROID_AVD:-Pixel_7_API_34}"
  local arch; arch=$(uname -m)
  local abi; abi=$([ "$arch" = "arm64" ] && echo "arm64-v8a" || echo "x86_64")
  SYS_IMAGE="system-images;android-34;google_apis;${abi}"

  if "$CMDLINE_BIN/avdmanager" list avd 2>/dev/null | grep -q "Name: ${avd_name}"; then
    echo "   AVD '${avd_name}' already exists."
    return 0
  fi

  echo "▶  Creating AVD: ${avd_name}..."
  # Try pixel_7 hardware profile, fall back to pixel
  if echo "no" | "$CMDLINE_BIN/avdmanager" \
        create avd \
        -n "$avd_name" -k "$SYS_IMAGE" -d "pixel_7" --force 2>/dev/null; then
    echo "   AVD created (Pixel 7 profile)."
  else
    echo "no" | "$CMDLINE_BIN/avdmanager" \
        create avd \
        -n "$avd_name" -k "$SYS_IMAGE" --force
    echo "   AVD created (default profile)."
  fi
}

launch_emulator() {
  local avd_name="${ANDROID_AVD:-Pixel_7_API_34}"
  export ANDROID_HOME="$SDK_DIR"
  export PATH="$SDK_DIR/emulator:$SDK_DIR/cmdline-tools/latest/bin:$SDK_DIR/platform-tools:$PATH"

  echo "▶  Launching emulator '${avd_name}'..."
  "$SDK_DIR/emulator/emulator" \
    -avd "$avd_name" \
    -no-snapshot-load \
    -no-audio \
    -no-boot-anim \
    -gpu swiftshader_indirect \
    > /tmp/qatarat_emu.log 2>&1 &
  EMU_PID=$!
  STARTED_EMU=true
  echo "   Emulator PID: $EMU_PID — waiting for boot (up to 3 min)..."

  adb -s emulator-5554 wait-for-device 2>/dev/null || adb wait-for-device 2>/dev/null || true

  local timeout=180 elapsed=0 boot=""
  while [ "$elapsed" -lt "$timeout" ]; do
    boot=$(adb shell getprop sys.boot_completed 2>/dev/null | tr -d '\r\n' || true)
    [ "$boot" = "1" ] && break
    sleep 3; elapsed=$((elapsed + 3))
    printf "   Boot: %ds / %ds\r" "$elapsed" "$timeout"
  done
  echo ""

  if [ "$boot" != "1" ]; then
    echo "✗  Emulator did not boot within ${timeout}s."
    echo "   Check /tmp/qatarat_emu.log for details."
    exit 1
  fi

  adb shell input keyevent 82 2>/dev/null || true
  sleep 1
  echo "   Emulator ready."
}

setup_and_launch_emulator() {
  export ANDROID_HOME="$SDK_DIR"
  export PATH="$SDK_DIR/emulator:$SDK_DIR/cmdline-tools/latest/bin:$SDK_DIR/platform-tools:$PATH"

  ensure_cmdline_tools
  ensure_emulator_binary
  ensure_system_image
  ensure_avd
  launch_emulator
}

# ════════════════════════════════════════════════════════════════════════════
# Main
# ════════════════════════════════════════════════════════════════════════════
if [ "$PLATFORM" = "android" ] && [ "$DEVICE_MODE" = "emulator" ]; then
  CONNECTED=$(adb devices 2>/dev/null | awk '/\tdevice$/ { count++ } END { print count + 0 }')

  if [ "${CONNECTED:-0}" -gt 0 ]; then
    echo "   Device already connected (${CONNECTED} found) — skipping emulator launch."
  else
    setup_and_launch_emulator
  fi
fi

# ── Start Appium server ──────────────────────────────────────────────────────
if ! curl -s http://127.0.0.1:4723/status > /dev/null 2>&1; then
  echo "▶  Starting Appium server..."
  appium --port 4723 --log appium.log &
  APPIUM_PID=$!
  sleep 4
  echo "   Appium started (PID $APPIUM_PID)"
else
  echo "   Appium already running on :4723"
fi

mkdir -p reports/screenshots allure-results

# ── Run tests ────────────────────────────────────────────────────────────────
PYTEST_ARGS=(
  tests/ -v
  --html="reports/report.html" --self-contained-html
  --junit-xml="reports/results.xml"
  --alluredir="allure-results"
  --tb=short
)

if [ -n "$MARKER" ]; then
  echo "▶  Running Appium tests [platform=$PLATFORM, marker=$MARKER]..."
  "$VENV_PYTHON" -m pytest "${PYTEST_ARGS[@]}" -m "$MARKER"
else
  echo "▶  Running ALL Appium tests [platform=$PLATFORM]..."
  "$VENV_PYTHON" -m pytest "${PYTEST_ARGS[@]}"
fi

RC=$?
echo ""
echo "$([ $RC -eq 0 ] && echo '✓' || echo '✗') Appium run complete (exit $RC)"
echo "  HTML:   $(pwd)/reports/report.html"
echo "  JUnit:  $(pwd)/reports/results.xml"
echo "  Allure: $(pwd)/allure-results/"
exit $RC
