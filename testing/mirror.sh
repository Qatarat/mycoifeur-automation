#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════
#   Qatarat — Phone Screen Mirror (scrcpy wrapper)
#
#   Mirrors your Android phone screen to this PC via USB in real
#   time. Testers can watch every tap, animation, and assertion as
#   it happens — no emulator, no Android Studio, works on any PC.
#
#   Usage:
#     bash mirror.sh                # basic mirror
#     bash mirror.sh --record       # mirror + save video
#     bash mirror.sh --watch        # auto-relaunch when reconnected
#     bash mirror.sh --help
# ═══════════════════════════════════════════════════════════════════

set -e

BOLD='\033[1m';    RESET='\033[0m'
GREEN='\033[0;32m'; YELLOW='\033[1;33m'
RED='\033[0;31m';   CYAN='\033[0;36m'
DIM='\033[2m'

log()   { echo -e "${GREEN}${BOLD}[✓]${RESET} $1"; }
warn()  { echo -e "${YELLOW}${BOLD}[!]${RESET} $1"; }
error() { echo -e "${RED}${BOLD}[✗]${RESET} $1"; }
info()  { echo -e "${CYAN}${BOLD}[→]${RESET} $1"; }

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ── PATH: load ADB / scrcpy from known locations ─────────────────────
if [ -z "$ANDROID_HOME" ]; then
  if   [ -d "$HOME/Library/Android/sdk" ]; then ANDROID_HOME="$HOME/Library/Android/sdk"
  elif [ -d "$HOME/Android/sdk" ];          then ANDROID_HOME="$HOME/Android/sdk"
  fi
fi
export ANDROID_HOME
export PATH="${ANDROID_HOME:+$ANDROID_HOME/platform-tools:}/opt/homebrew/bin:/usr/local/bin:$PATH"

# ── Parse arguments ──────────────────────────────────────────────────
MODE="mirror"          # mirror | record | watch
RECORD_FILE=""
EXTRA_FLAGS=""
MAX_SIZE=1080          # cap resolution for low-storage PCs

for arg in "$@"; do
  case "$arg" in
    --record)
      MODE="record"
      RECORD_FILE="$SCRIPT_DIR/mirror_recordings/session_$(date +%Y%m%d_%H%M%S).mkv"
      ;;
    --watch)
      MODE="watch"
      ;;
    --low-cpu)
      MAX_SIZE=720
      EXTRA_FLAGS="$EXTRA_FLAGS --no-audio"
      ;;
    --help|-h)
      echo ""
      echo -e "${BOLD}Usage:${RESET}  bash mirror.sh [option]"
      echo ""
      echo "  (no option)   Basic mirror — see the phone screen on your PC"
      echo "  --record      Mirror + record session to a .mkv video file"
      echo "  --watch       Auto-relaunch mirror each time the phone reconnects"
      echo "  --low-cpu     Lower resolution (720p) + no audio (saves CPU)"
      echo "  --help        Show this help"
      echo ""
      echo -e "${BOLD}Keyboard shortcuts while mirroring:${RESET}"
      echo "  Ctrl+C / Cmd+W   Close mirror"
      echo "  Ctrl+Shift+H     Home button"
      echo "  Ctrl+Shift+B     Back button"
      echo "  Ctrl+Shift+P     Power / wake screen"
      echo "  Ctrl+Shift+M     Menu button"
      echo "  Ctrl+V           Paste clipboard to phone"
      echo ""
      exit 0
      ;;
  esac
done

# ── Banner ───────────────────────────────────────────────────────────
clear
echo ""
echo -e "${CYAN}${BOLD}  ╔══════════════════════════════════════════╗${RESET}"
echo -e "${CYAN}${BOLD}  ║   Qatarat — Phone Screen Mirror          ║${RESET}"
echo -e "${CYAN}${BOLD}  ║   USB · Real device · Zero install       ║${RESET}"
echo -e "${CYAN}${BOLD}  ╚══════════════════════════════════════════╝${RESET}"
echo ""

# ── Check: scrcpy installed ──────────────────────────────────────────
if ! command -v scrcpy &>/dev/null; then
  error "scrcpy is not installed."
  echo ""
  echo -e "  Install it with one command:"
  echo ""
  if [[ "$OSTYPE" == "darwin"* ]]; then
    echo -e "    ${CYAN}brew install scrcpy${RESET}"
  else
    echo -e "    ${CYAN}sudo apt install scrcpy${RESET}   # Ubuntu 22.04+"
    echo -e "    ${CYAN}sudo snap install scrcpy${RESET}  # older Ubuntu"
  fi
  echo ""
  echo -e "  Or run:  ${CYAN}bash install.sh${RESET}  (installs scrcpy + all other tools)"
  echo ""
  exit 1
fi

log "scrcpy $(scrcpy --version 2>&1 | head -1 | grep -oE '[0-9]+\.[0-9]+[^ ]*' || echo OK)"

# ── Check: ADB installed ─────────────────────────────────────────────
if ! command -v adb &>/dev/null; then
  error "ADB not found. Run:  bash install.sh"
  exit 1
fi

# ── Ensure record directory exists ───────────────────────────────────
if [ "$MODE" = "record" ]; then
  mkdir -p "$SCRIPT_DIR/mirror_recordings"
  info "Session will be recorded to:"
  echo -e "    ${DIM}$RECORD_FILE${RESET}"
  echo ""
fi

# ── wait_for_device: blocks until a device is authorised ─────────────
wait_for_device() {
  local MAX_WAIT=90 WAIT=0 LAST_STATE=""

  echo ""
  echo -e "  ${YELLOW}USB Debugging setup (one-time):${RESET}"
  echo -e "  ${DIM}1. Settings → About Phone → tap Build Number 7 times${RESET}"
  echo -e "  ${DIM}2. Settings → Developer Options → USB Debugging → ON${RESET}"
  echo -e "  ${DIM}3. Plug phone in via USB → tap Allow on the dialog${RESET}"
  echo ""

  adb kill-server 2>/dev/null; adb start-server 2>/dev/null

  while [ $WAIT -lt $MAX_WAIT ]; do
    RAW=$(adb devices 2>/dev/null | tail -n +2 | grep -v "^$" || true)
    DEVICE_LINE=$(echo "$RAW" | grep "device$" | head -1)
    if [ -n "$DEVICE_LINE" ]; then
      DEVICE_ID=$(echo "$DEVICE_LINE" | awk '{print $1}')
      return 0
    fi
    UNAUTH=$(echo "$RAW" | grep "unauthorized" | head -1)
    if [ -n "$UNAUTH" ]; then
      UNAUTH_ID=$(echo "$UNAUTH" | awk '{print $1}')
      if [ "$LAST_STATE" != "unauth:$UNAUTH_ID" ]; then
        echo -e "\r  ${YELLOW}${BOLD}[!]${RESET} Phone detected — unlock it and tap ${BOLD}Allow${RESET} on the USB dialog."
        LAST_STATE="unauth:$UNAUTH_ID"
      fi
    else
      printf "\r  ${YELLOW}Waiting for device...${RESET} ${DIM}%ds${RESET}   " "$WAIT"
      LAST_STATE="none"
    fi
    sleep 2; WAIT=$((WAIT + 2))
  done

  error "No device found after ${MAX_WAIT}s."
  echo ""
  echo -e "  ${BOLD}Common fixes:${RESET}"
  echo -e "  ${CYAN}•${RESET} Use a data USB cable (charge-only cables have no data pins)"
  echo -e "  ${CYAN}•${RESET} Unlock the phone and check for the 'Allow USB Debugging' popup"
  echo -e "  ${CYAN}•${RESET} Try a different USB port"
  echo -e "  ${CYAN}•${RESET} Developer Options → Revoke USB authorizations → reconnect"
  echo -e "  ${CYAN}•${RESET} Run: ${CYAN}adb kill-server && adb start-server && adb devices${RESET}"
  return 1
}

# ── start_mirror: launch scrcpy for detected DEVICE_ID ───────────────
start_mirror() {
  local BRAND MODEL ANDROID_VER TITLE FLAGS

  BRAND=$(adb -s "$DEVICE_ID" shell getprop ro.product.brand 2>/dev/null | tr -d '\r')
  MODEL=$(adb -s "$DEVICE_ID" shell getprop ro.product.model 2>/dev/null | tr -d '\r')
  ANDROID_VER=$(adb -s "$DEVICE_ID" shell getprop ro.build.version.release 2>/dev/null | tr -d '\r')

  echo ""
  log "Device connected!"
  echo ""
  echo -e "  ${BOLD}Device:${RESET}  $BRAND $MODEL"
  echo -e "  ${BOLD}Android:${RESET} $ANDROID_VER"
  echo -e "  ${BOLD}ID:${RESET}      $DEVICE_ID"
  echo ""

  TITLE="Qatarat · $BRAND $MODEL · Android $ANDROID_VER"

  FLAGS="--serial $DEVICE_ID"
  FLAGS="$FLAGS --window-title \"$TITLE\""
  FLAGS="$FLAGS --stay-awake"
  FLAGS="$FLAGS --max-size $MAX_SIZE"
  FLAGS="$FLAGS --window-width 360"
  FLAGS="$FLAGS --window-height 780"
  FLAGS="$FLAGS $EXTRA_FLAGS"

  if [ "$MODE" = "record" ]; then
    FLAGS="$FLAGS --record \"$RECORD_FILE\""
    info "Recording to: $RECORD_FILE"
  fi

  echo -e "  ${DIM}Keyboard shortcuts: Ctrl+Shift+H = Home  |  Ctrl+Shift+B = Back"
  echo -e "  Ctrl+V = paste to phone  |  Ctrl+C or close window to stop${RESET}"
  echo ""
  info "Launching mirror... (close the window or press Ctrl+C to stop)"
  echo ""

  eval scrcpy $FLAGS
}

# ── Mode: single run ─────────────────────────────────────────────────
if [ "$MODE" = "mirror" ] || [ "$MODE" = "record" ]; then
  wait_for_device || exit 1
  start_mirror
  echo ""
  [ "$MODE" = "record" ] && log "Recording saved: $RECORD_FILE" || log "Mirror closed."

# ── Mode: watch — auto-relaunch on every reconnect ───────────────────
elif [ "$MODE" = "watch" ]; then
  info "Watch mode — mirror will restart automatically each time the phone reconnects."
  echo -e "  ${DIM}Press Ctrl+C to exit.${RESET}"
  echo ""

  while true; do
    if wait_for_device 2>/dev/null; then
      start_mirror 2>/dev/null || true
      echo ""
      warn "Mirror closed. Waiting for reconnect..."
    else
      warn "Device disconnected. Waiting for reconnect..."
    fi
    sleep 3
  done
fi
