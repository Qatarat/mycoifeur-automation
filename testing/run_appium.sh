#!/usr/bin/env bash
# Run Appium tests
# Usage:
#   ./run_appium.sh                        — all tests (Android emulator)
#   ./run_appium.sh payment                — payment tests only
#   ./run_appium.sh gift                   — gift card tests only
#   ./run_appium.sh subscription           — subscription tests only
#   PLATFORM=ios ./run_appium.sh           — iOS tests
#   DEVICE_MODE=device ./run_appium.sh     — real device

set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR/appium"

PLATFORM="${PLATFORM:-android}"
DEVICE_MODE="${DEVICE_MODE:-emulator}"
MARKER="${1:-}"

export PLATFORM DEVICE_MODE

# Use virtualenv Python if present, otherwise fall back to system python3
VENV_PYTHON=".venv/bin/python"
if [ ! -f "$VENV_PYTHON" ]; then
  echo "⚠  venv not found — run ./install.sh first"
  VENV_PYTHON="python3"
fi

# Start Appium server in background if not already running
if ! curl -s http://127.0.0.1:4723/status > /dev/null 2>&1; then
  echo "▶  Starting Appium server..."
  appium --port 4723 --log appium.log &
  APPIUM_PID=$!
  sleep 4
  echo "   Appium started (PID $APPIUM_PID)"
fi

mkdir -p reports/screenshots

if [ -n "$MARKER" ]; then
  echo "▶  Running Appium tests [platform=$PLATFORM, marker=$MARKER]..."
  "$VENV_PYTHON" -m pytest tests/ -m "$MARKER" -v
else
  echo "▶  Running ALL Appium tests [platform=$PLATFORM]..."
  "$VENV_PYTHON" -m pytest tests/ -v
fi

echo ""
echo "✓ Appium run complete. HTML report: appium/reports/report.html"
