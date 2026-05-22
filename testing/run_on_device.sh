#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════
#   Qatarat — Wireless Device Test Runner
#   Select a platform → pick your device from a list → tests run in
#   the background.  No USB required, no emulator needed.
# ═══════════════════════════════════════════════════════════════════

set -euo pipefail

# ── Colours ─────────────────────────────────────────────────────────
BOLD='\033[1m';    RESET='\033[0m'
GREEN='\033[0;32m'; YELLOW='\033[1;33m'
RED='\033[0;31m';   CYAN='\033[0;36m'
BLUE='\033[0;34m';  DIM='\033[2m'

log()   { echo -e "${GREEN}${BOLD}[✓]${RESET} $1"; }
warn()  { echo -e "${YELLOW}${BOLD}[!]${RESET} $1"; }
error() { echo -e "${RED}${BOLD}[✗]${RESET} $1" >&2; }
step()  { echo -e "\n${CYAN}${BOLD}▶  $1${RESET}"; }

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FLOWS_DIR="$SCRIPT_DIR/maestro/flows"
REPORTS_DIR="$SCRIPT_DIR/reports/maestro"
APK_PATH="$SCRIPT_DIR/../Qatarat (Lambda-Stage).apk"
REPORT_TS=$(date +%Y%m%d-%H%M%S)
LOG_FILE="$REPORTS_DIR/run_${REPORT_TS}.log"
DEVICE_TARGET=""

# ── PATH setup ──────────────────────────────────────────────────────
for _java in /opt/homebrew/opt/openjdk@17 /usr/local/opt/openjdk@17; do
  [ -d "$_java" ] && { export JAVA_HOME="$_java"; break; }
done
for _sdk in "$HOME/Library/Android/sdk" "$HOME/Android/sdk" "$HOME/.qatarat-android-sdk"; do
  [ -d "$_sdk" ] && { export ANDROID_HOME="$_sdk"; break; }
done
export PATH="${JAVA_HOME:+$JAVA_HOME/bin:}$HOME/.maestro/bin:${ANDROID_HOME:+$ANDROID_HOME/platform-tools:}/opt/homebrew/bin:/usr/local/bin:$PATH"

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
echo -e "  ${BOLD}Qatarat (قطرات) — Device Test Runner${RESET}"
echo -e "  ${DIM}Pick your device · tests run in the background${RESET}"
echo ""
echo "  ─────────────────────────────────────────────────────────"
echo ""

# ── Prerequisites ────────────────────────────────────────────────────
MISSING=()
command -v maestro &>/dev/null || MISSING+=(maestro)

if [ ${#MISSING[@]} -gt 0 ]; then
  error "Missing: ${MISSING[*]}"
  echo -e "  Install: ${CYAN}cd testing && bash install.sh${RESET}"
  exit 1
fi

# ════════════════════════════════════════════════════════════════════
#   PLATFORM SELECT
# ════════════════════════════════════════════════════════════════════
echo -e "  ${BOLD}Which platform?${RESET}"
echo ""
echo -e "  ${BOLD}  1)${RESET} ${GREEN}Android${RESET}"
echo -e "  ${BOLD}  2)${RESET} ${CYAN}iOS  (iPhone / iPad)${RESET}"
echo ""
read -rp "  Choice [1/2, default=1]: " _PC
_PC="${_PC:-1}"
case "$_PC" in
  2) PLATFORM="ios" ;;
  *) PLATFORM="android" ;;
esac
echo ""

# ════════════════════════════════════════════════════════════════════
#   ANDROID — discover devices, show list, let user pick or add new
# ════════════════════════════════════════════════════════════════════
if [ "$PLATFORM" = "android" ]; then

  command -v adb &>/dev/null || { error "adb not found — run: bash install.sh"; exit 1; }

  # ── helper: collect currently authorised ADB devices ──────────────
  _android_scan() {
    # populates ANDROID_SERIALS[] and ANDROID_LABELS[]
    ANDROID_SERIALS=()
    ANDROID_LABELS=()
    while IFS= read -r line; do
      [[ "$line" =~ ^List ]] && continue
      [[ -z "$line" ]] && continue
      local serial status
      serial=$(awk '{print $1}' <<< "$line")
      status=$(awk '{print $2}' <<< "$line")
      [[ "$status" != "device" ]] && continue
      local brand model android_ver conn_type
      brand=$(adb -s "$serial" shell getprop ro.product.brand      2>/dev/null | tr -d '\r' || echo "")
      model=$(adb -s "$serial" shell getprop ro.product.model       2>/dev/null | tr -d '\r' || echo "Unknown")
      android_ver=$(adb -s "$serial" shell getprop ro.build.version.release 2>/dev/null | tr -d '\r' || echo "?")
      # detect WiFi vs USB by serial format (WiFi serials look like 192.168.x.x:port)
      if [[ "$serial" =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+:[0-9]+$ ]]; then
        conn_type="${DIM}WiFi${RESET}"
      else
        conn_type="${DIM}USB${RESET}"
      fi
      ANDROID_SERIALS+=("$serial")
      ANDROID_LABELS+=("${brand} ${model}  (Android ${android_ver})  [${conn_type}]  ${DIM}${serial}${RESET}")
    done < <(adb devices 2>/dev/null)
  }

  # ── helper: connect a new WiFi/USB device ─────────────────────────
  _android_add_device() {
    echo ""
    echo -e "  ${BOLD}How to connect a new device:${RESET}"
    echo ""
    echo -e "  ${BOLD}  A)${RESET} WiFi — Android 11+ Wireless Debugging ${DIM}(no USB ever)${RESET}"
    echo -e "  ${BOLD}  B)${RESET} WiFi — Enter IP address ${DIM}(toggle 'ADB over network' in Dev Options)${RESET}"
    echo -e "  ${BOLD}  C)${RESET} USB cable"
    echo ""
    read -rp "  Choice [A/B/C]: " _CC
    echo ""

    case "${_CC,,}" in
      a)
        echo -e "  ${YELLOW}${BOLD}On your phone:${RESET}"
        echo -e "  ${DIM}1. Settings → About phone → tap Build number 7 times${RESET}"
        echo -e "  ${DIM}2. Settings → Developer options → Wireless debugging → ON${RESET}"
        echo -e "  ${DIM}3. Tap  'Pair device with pairing code'${RESET}"
        echo -e "  ${DIM}   A popup shows:  IP address  192.168.x.x:XXXXX  and a 6-digit code${RESET}"
        echo -e "  ${YELLOW}   ⚠ Enter the IP:port exactly as shown — use a colon (:) before the port${RESET}"
        echo ""
        while true; do
          read -rp "  IP:port from popup (e.g. 192.168.0.197:39753): " _PAIR_ADDR
          # validate format: must be digits.digits.digits.digits:digits
          if [[ "$_PAIR_ADDR" =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+:[0-9]+$ ]]; then
            break
          fi
          warn "Wrong format. Must be like 192.168.0.197:39753 (IP, colon, port number)"
          warn "If you see a MAC address like 44:E2:BA:30:CE:14 — that is the wrong screen."
        done
        read -rp "  6-digit pairing code: " _PAIR_CODE
        echo ""
        step "Pairing..."
        # adb pair sometimes exits non-zero even on success; check output text instead
        _PAIR_OUT=$(adb pair "$_PAIR_ADDR" "$_PAIR_CODE" 2>&1) || true
        if echo "$_PAIR_OUT" | grep -qi "successfully paired\|success"; then
          log "Paired  ($( echo "$_PAIR_OUT" | head -1 ))"
        else
          echo "$_PAIR_OUT"
          error "Pairing failed — check the IP:port and 6-digit code then try again"
          return 1
        fi
        echo ""
        echo -e "  ${DIM}Now go back to the 'Wireless debugging' main screen (not the Pair popup).${RESET}"
        echo -e "  ${DIM}It shows a connection IP:port like  192.168.0.197:38613  — enter that below.${RESET}"
        echo ""
        local _WIP="${_PAIR_ADDR%%:*}"
        while true; do
          read -rp "  IP:port from Wireless debugging main screen [default ${_WIP}:5555]: " _CONN
          _CONN="${_CONN:-${_WIP}:5555}"
          [[ "$_CONN" =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+:[0-9]+$ ]] && break
          warn "Must be IP:port format (e.g. 192.168.0.197:38613)"
        done
        step "Connecting to $_CONN..."
        _CONN_OUT=$(adb connect "$_CONN" 2>&1) || true
        echo "$_CONN_OUT"
        if echo "$_CONN_OUT" | grep -qi "connected\|already connected"; then
          log "Connected to $_CONN"
        else
          error "Connection failed — is Wireless debugging still ON on the device?"
          return 1
        fi
        ;;
      b)
        echo -e "  ${DIM}On your phone: Developer options → enable 'ADB over network'${RESET}"
        echo -e "  ${DIM}or: Developer options → Wireless debugging → ON  (the IP is shown there)${RESET}"
        echo -e "  ${DIM}You can enter just the IP or the full IP:port${RESET}"
        echo ""
        read -rp "  Device IP (e.g. 192.168.0.197 or 192.168.0.197:5555): " _WIP
        # if user already included a port, use it; otherwise ask
        if [[ "$_WIP" =~ ^([0-9.]+):([0-9]+)$ ]]; then
          _CONN_ADDR="$_WIP"
        else
          read -rp "  Port [default 5555]: " _WPORT
          _CONN_ADDR="$_WIP:${_WPORT:-5555}"
        fi
        step "Connecting to $_CONN_ADDR..."
        _CONN_OUT=$(adb connect "$_CONN_ADDR" 2>&1) || true
        echo "$_CONN_OUT"
        if echo "$_CONN_OUT" | grep -qi "connected\|already connected"; then
          log "Connected"
        else
          error "Cannot reach $_CONN_ADDR — is the device on the same WiFi network?"
          return 1
        fi
        ;;
      c)
        echo -e "  ${DIM}Settings → Developer options → USB debugging → ON${RESET}"
        echo -e "  ${DIM}Connect USB cable → tap 'Allow' on the phone${RESET}"
        echo ""
        adb kill-server 2>/dev/null; adb start-server 2>/dev/null
        local _W=0 _MAX=60 _LAST=""
        while [ $_W -lt $_MAX ]; do
          local _RAW
          _RAW=$(adb devices 2>/dev/null | tail -n +2 | grep -v "^$" || true)
          if echo "$_RAW" | grep -q "device$"; then break; fi
          if echo "$_RAW" | grep -q "unauthorized" && [ "$_LAST" != "ua" ]; then
            warn "Phone detected but not authorised — tap 'Allow' on the USB debugging dialog"
            _LAST="ua"
          else
            printf "\r  Waiting for USB device... %ds   " "$_W"
          fi
          sleep 2; _W=$((_W+2))
        done
        echo ""
        adb devices | tail -n +2 | grep "device$" | head -1 | grep -q "device" || { error "No USB device found"; return 1; }
        log "USB device connected"
        ;;
      *)
        error "Invalid choice"; return 1 ;;
    esac
  }

  # ── Main Android device picker loop ──────────────────────────────
  while true; do
    step "Scanning for Android devices..."
    adb start-server &>/dev/null || true
    sleep 1
    _android_scan

    echo ""
    echo "  ─────────────────────────────────────────────────────────"
    echo -e "  ${BOLD}  Available Android devices${RESET}"
    echo "  ─────────────────────────────────────────────────────────"
    echo ""

    if [ ${#ANDROID_SERIALS[@]} -eq 0 ]; then
      echo -e "  ${YELLOW}  No devices found yet.${RESET}"
      echo ""
    else
      for i in "${!ANDROID_SERIALS[@]}"; do
        printf "  ${BOLD}  %d)${RESET}  " "$((i+1))"
        echo -e "${ANDROID_LABELS[$i]}"
      done
      echo ""
    fi

    local_next=$((${#ANDROID_SERIALS[@]}+1))
    echo -e "  ${BOLD}  ${local_next})${RESET}  ${CYAN}+ Connect a new device (WiFi or USB)${RESET}"
    echo ""
    read -rp "  Select device [1-${local_next}]: " _SEL

    if [ "$_SEL" = "$local_next" ]; then
      _android_add_device || true
      # re-scan and loop
      continue
    fi

    # validate numeric selection
    if [[ "$_SEL" =~ ^[0-9]+$ ]] && [ "$_SEL" -ge 1 ] && [ "$_SEL" -le "${#ANDROID_SERIALS[@]}" ]; then
      DEVICE_TARGET="${ANDROID_SERIALS[$((  _SEL - 1))]}"
      _CHOSEN_LABEL="${ANDROID_LABELS[$((_SEL - 1))]}"
      break
    else
      warn "Invalid selection — try again"
    fi
  done

  echo ""
  echo "  ─────────────────────────────────────────────────────────"
  log "Selected device:"
  echo -e "  $_CHOSEN_LABEL"
  echo ""

  # ── Install APK ──────────────────────────────────────────────────
  if [ -f "$APK_PATH" ]; then
    step "Installing Qatarat APK..."
    if adb -s "$DEVICE_TARGET" install -r "$APK_PATH" 2>&1 | grep -q "Success"; then
      log "App installed"
    else
      warn "Install had warnings (app may already be current) — continuing"
    fi
  else
    warn "APK not found at project root — assuming app is pre-installed on device"
  fi

# ════════════════════════════════════════════════════════════════════
#   iOS — discover devices, show list, let user pick
# ════════════════════════════════════════════════════════════════════
else

  # Install idb-companion if missing
  if ! command -v idb_companion &>/dev/null; then
    warn "idb-companion not found — required for Maestro on iOS"
    if command -v brew &>/dev/null; then
      step "Installing idb-companion..."
      brew install facebook/fb/idb-companion 2>/dev/null || \
        { error "brew install facebook/fb/idb-companion failed"; exit 1; }
    else
      error "Install idb-companion: brew install facebook/fb/idb-companion"; exit 1
    fi
  fi

  # ── Scan for real iOS devices ─────────────────────────────────────
  _ios_scan() {
    IOS_UDIDS=()
    IOS_LABELS=()
    local raw
    raw=$(xcrun xctrace list devices 2>/dev/null || true)
    while IFS= read -r line; do
      [[ -z "$line" ]] && continue
      [[ "$line" =~ ^= ]] && continue
      [[ "$line" =~ Simulator ]] && continue
      local udid name ver
      udid=$(grep -oE '\([A-F0-9a-f-]{36,}\)' <<< "$line" | tr -d '()' | head -1 || true)
      [[ -z "$udid" ]] && continue
      # strip the UDID and version parentheses to get the device name
      name=$(sed 's/ ([^)]*) ([^)]*)$//' <<< "$line" | sed 's/^ *//')
      ver=$(grep -oE '\([0-9]+\.[0-9]+[^)]*\)' <<< "$line" | tr -d '()' | head -1 || echo "?")
      IOS_UDIDS+=("$udid")
      IOS_LABELS+=("${name}  (iOS ${ver})  ${DIM}${udid:0:8}…${RESET}")
    done <<< "$raw"
  }

  # ── Main iOS device picker ────────────────────────────────────────
  echo ""
  echo -e "  ${YELLOW}${BOLD}Before scanning:${RESET}"
  echo -e "  ${DIM}1. Connect iPhone/iPad via USB (or enable Wi-Fi sync in Finder)${RESET}"
  echo -e "  ${DIM}2. Unlock device → tap 'Trust This Computer' → enter passcode${RESET}"
  echo -e "  ${DIM}3. App must be pre-installed via Xcode or TestFlight${RESET}"
  echo ""
  read -rp "  Press Enter when device is connected and trusted..." _IGNORE

  step "Scanning for iOS devices..."
  sleep 2
  _ios_scan

  if [ ${#IOS_UDIDS[@]} -eq 0 ]; then
    error "No iPhone/iPad found."
    echo ""
    echo -e "  ${DIM}Make sure:${RESET}"
    echo -e "  ${DIM}• Device is unlocked and 'Trust' was tapped${RESET}"
    echo -e "  ${DIM}• Try: xcrun xctrace list devices${RESET}"
    exit 1
  fi

  echo ""
  echo "  ─────────────────────────────────────────────────────────"
  echo -e "  ${BOLD}  Available iOS devices${RESET}"
  echo "  ─────────────────────────────────────────────────────────"
  echo ""
  for i in "${!IOS_UDIDS[@]}"; do
    printf "  ${BOLD}  %d)${RESET}  " "$((i+1))"
    echo -e "${IOS_LABELS[$i]}"
  done
  echo ""

  if [ "${#IOS_UDIDS[@]}" -eq 1 ]; then
    read -rp "  Select device [1, default=1]: " _SEL
    _SEL="${_SEL:-1}"
  else
    read -rp "  Select device [1-${#IOS_UDIDS[@]}]: " _SEL
  fi

  if [[ "$_SEL" =~ ^[0-9]+$ ]] && [ "$_SEL" -ge 1 ] && [ "$_SEL" -le "${#IOS_UDIDS[@]}" ]; then
    DEVICE_TARGET="${IOS_UDIDS[$((_SEL - 1))]}"
    _CHOSEN_LABEL="${IOS_LABELS[$((_SEL - 1))]}"
  else
    error "Invalid selection"; exit 1
  fi

  echo ""
  echo "  ─────────────────────────────────────────────────────────"
  log "Selected device:"
  echo -e "  $_CHOSEN_LABEL"
  echo ""

fi  # end platform branch

# ════════════════════════════════════════════════════════════════════
#   TEST SUITE MENU
# ════════════════════════════════════════════════════════════════════
echo "  ─────────────────────────────────────────────────────────"
echo -e "  ${BOLD}  Which flows to run?${RESET}"
echo "  ─────────────────────────────────────────────────────────"
echo ""
echo -e "  ${BOLD}  1)${RESET} ${GREEN}All 25 flows${RESET}     ${DIM}~40 min · complete regression${RESET}"
echo -e "  ${BOLD}  2)${RESET} Smoke (01-05)   ${DIM}~10 min · login, onboard, browse, cart${RESET}"
echo -e "  ${BOLD}  3)${RESET} Single flow     ${DIM}enter flow number, e.g. 12${RESET}"
echo ""
read -rp "  Choice [1/2/3, default=1]: " SUITE_CHOICE
SUITE_CHOICE="${SUITE_CHOICE:-1}"
echo ""

FLOW_FILES=()
case "$SUITE_CHOICE" in
  1)
    while IFS= read -r -d '' f; do FLOW_FILES+=("$f"); done \
      < <(find "$FLOWS_DIR" -maxdepth 1 -name '[0-9][0-9]_*.yaml' -print0 | sort -z)
    SUITE_LABEL="All 25 flows"
    ;;
  2)
    while IFS= read -r -d '' f; do FLOW_FILES+=("$f"); done \
      < <(find "$FLOWS_DIR" -maxdepth 1 -name '0[1-5]_*.yaml' -print0 | sort -z)
    SUITE_LABEL="Smoke (01-05)"
    ;;
  3)
    read -rp "  Flow number (e.g. 12): " _FN
    _FN=$(printf "%02d" "${_FN#0}" 2>/dev/null || echo "$_FN")
    _MATCH=$(find "$FLOWS_DIR" -maxdepth 1 -name "${_FN}_*.yaml" 2>/dev/null | head -1 || true)
    [ -z "$_MATCH" ] && { error "No flow found matching ${_FN}_*.yaml"; exit 1; }
    FLOW_FILES+=("$_MATCH")
    SUITE_LABEL="Flow $_FN"
    ;;
  *)
    error "Invalid choice"; exit 1 ;;
esac

[ ${#FLOW_FILES[@]} -eq 0 ] && { error "No flow YAML files found in $FLOWS_DIR"; exit 1; }

# ════════════════════════════════════════════════════════════════════
#   BUILD & LAUNCH BACKGROUND RUNNER
# ════════════════════════════════════════════════════════════════════
mkdir -p "$REPORTS_DIR"
RUN_SCRIPT="/tmp/qatarat_run_${REPORT_TS}.sh"

# Write the runner sub-script
{
  echo "#!/usr/bin/env bash"
  echo "export PATH=\"$HOME/.maestro/bin:\$HOME/Android/sdk/platform-tools:/opt/homebrew/bin:/usr/local/bin:\$PATH\""
  # Ensure ADB server is alive in the background process (WiFi connections need it)
  echo "adb start-server 2>/dev/null || true"
  echo "PASS=0; FAIL=0; TOTAL=${#FLOW_FILES[@]}"
  echo "echo '════════════════════════════════════════════════════════'"
  echo "echo '  Qatarat Maestro — ${#FLOW_FILES[@]} flows on $DEVICE_TARGET'"
  echo "echo '  Suite : $SUITE_LABEL'"
  echo "echo \"  Start : \$(date '+%Y-%m-%d %H:%M:%S')\""
  echo "echo '════════════════════════════════════════════════════════'"
  echo "echo ''"

  # ── Pre-flight block ─────────────────────────────────────────────
  echo "echo '── Pre-flight ─────────────────────────────────────────'"
  echo "echo \"Maestro : \$(maestro --version 2>&1 | head -1 || echo NOT FOUND)\""
  echo "_ADB_CHECK=\$(adb -s \"$DEVICE_TARGET\" shell echo OK 2>&1 | tr -d '\\r')"
  echo "echo \"ADB     : \$_ADB_CHECK\""
  echo "if [ \"\$_ADB_CHECK\" != 'OK' ]; then"
  echo "  echo 'ERROR: Device $DEVICE_TARGET is unreachable — reconnect and retry'"
  echo "  echo 'Run:  adb connect $DEVICE_TARGET'"
  echo "  exit 1"
  echo "fi"
  # Forward Maestro's port so it works over WiFi (Maestro uses port 7001 on device)
  echo "adb -s \"$DEVICE_TARGET\" forward tcp:7001 tcp:7001 2>&1 | sed 's/^/  port-fwd: /'"
  echo "_PKG=\$(adb -s \"$DEVICE_TARGET\" shell pm list packages 2>/dev/null | grep -i qatarat | head -1 | tr -d '\\r' || true)"
  echo "if [ -z \"\$_PKG\" ]; then"
  echo "  echo 'App     : NOT FOUND — com.qatarat.app is not installed on the device'"
  echo "  echo 'Aborting — install the APK first (adb install -r <apk>)'"
  echo "  exit 1"
  echo "else"
  echo "  echo \"App     : \$_PKG  ← installed OK\""
  echo "fi"
  # Check if Maestro companion is installed
  echo "_MAESTRO_APP=\$(adb -s \"$DEVICE_TARGET\" shell pm list packages 2>/dev/null | grep maestro | tr -d '\\r' || true)"
  echo "if [ -n \"\$_MAESTRO_APP\" ]; then"
  echo "  echo \"Maestro : companion installed (\$_MAESTRO_APP)\""
  echo "else"
  echo "  echo 'Maestro : companion NOT yet installed — will install on first run'"
  echo "fi"
  echo "echo '───────────────────────────────────────────────────────'"
  echo "echo '  NOTE: If flows fail at 0s, go to device:'"
  echo "echo '  Settings → Accessibility → Maestro → Enable'"
  echo "echo '  (required on Android 11+ physical devices)'"
  echo "echo '───────────────────────────────────────────────────────'"
  echo "echo ''"

  for flow_yaml in "${FLOW_FILES[@]}"; do
    flow_name="$(basename "$flow_yaml" .yaml)"
    echo "echo '──────────────────────────────────────────────────────'"
    echo "echo '  [RUN]  $flow_name'"
    # Capture full Maestro output (stdout+stderr) so error reasons appear in the log.
    # --format is omitted: Maestro auto-detects JUnit format from the .xml extension.
    if [ "$PLATFORM" = "ios" ]; then
      echo "_FLOW_LOG=\$(MAESTRO_DRIVER=ios maestro --device \"$DEVICE_TARGET\" test \\"
    else
      echo "_FLOW_LOG=\$(maestro --device \"$DEVICE_TARGET\" test \\"
    fi
    echo "    --output \"$REPORTS_DIR/${flow_name}-results.xml\" \\"
    echo "    \"$flow_yaml\" 2>&1); _EC=\$?"
    echo "echo \"\$_FLOW_LOG\""
    echo "if [ \$_EC -eq 0 ]; then"
    echo "  echo '  [PASS] $flow_name'; PASS=\$((PASS+1))"
    echo "else"
    echo "  echo '  [FAIL] $flow_name'; FAIL=\$((FAIL+1))"
    echo "  echo '  Error detail:'"
    echo "  echo \"\$_FLOW_LOG\" | grep -iE 'error|fail|unable|exception|not found|timeout|crash' | head -10 || true"
    echo "fi"
    echo "echo ''"
  done

  echo "echo '════════════════════════════════════════════════════════'"
  echo "echo \"  DONE — \$(date '+%Y-%m-%d %H:%M:%S')\""
  echo "echo \"  PASS: \$PASS   FAIL: \$FAIL   TOTAL: \$TOTAL\""
  echo "echo '  Reports: $REPORTS_DIR'"
  echo "echo '════════════════════════════════════════════════════════'"
  echo "[ \$FAIL -eq 0 ] && exit 0 || exit 1"
} > "$RUN_SCRIPT"
chmod +x "$RUN_SCRIPT"

# ── Physical-device readiness reminder ──────────────────────────────
if [ "$PLATFORM" = "android" ]; then
  echo ""
  echo "  ─────────────────────────────────────────────────────────"
  echo -e "  ${YELLOW}${BOLD}Before flows run — one-time device setup:${RESET}"
  echo -e "  ${DIM}Maestro installs a helper app on the device on first run.${RESET}"
  echo -e "  ${DIM}If all flows fail at 0s, do this on the phone:${RESET}"
  echo -e "  ${YELLOW}  Settings → Accessibility → Installed apps → Maestro → Enable${RESET}"
  echo -e "  ${DIM}Also ensure: Developer options → Disable permission monitoring = ON${RESET}"
  echo "  ─────────────────────────────────────────────────────────"
fi

# Launch
echo ""
echo -e "  ${BOLD}Launching ${#FLOW_FILES[@]} flows on${RESET} ${GREEN}$_CHOSEN_LABEL${RESET}${BOLD}...${RESET}"
echo ""

# Pre-create the log so tail -f never races a missing file
touch "$LOG_FILE"
nohup bash "$RUN_SCRIPT" >> "$LOG_FILE" 2>&1 &
TEST_PID=$!

echo -e "  ${GREEN}${BOLD}Tests are running in the background!${RESET}"
echo ""
echo -e "  ${BOLD}PID     :${RESET}  $TEST_PID"
echo -e "  ${BOLD}Log     :${RESET}  $LOG_FILE"
echo -e "  ${BOLD}Reports :${RESET}  $REPORTS_DIR"
echo ""
echo "  ─────────────────────────────────────────────────────────"
echo -e "  ${DIM}Live output below.  ${BOLD}Ctrl+C${RESET}${DIM} detaches — tests keep running.${RESET}"
echo -e "  ${DIM}Rejoin :  tail -f $LOG_FILE${RESET}"
echo -e "  ${DIM}Done?  :  kill -0 $TEST_PID 2>/dev/null && echo running || echo done${RESET}"
echo "  ─────────────────────────────────────────────────────────"
echo ""

# ── Detachable live tail ─────────────────────────────────────────────
_detach() {
  echo ""
  echo -e "  ${YELLOW}${BOLD}Detached.${RESET}  Tests are still running on the device (PID $TEST_PID)."
  echo ""
  echo -e "  Rejoin  :  ${CYAN}tail -f $LOG_FILE${RESET}"
  echo -e "  Results :  ${CYAN}ls $REPORTS_DIR${RESET}"
  echo ""
  exit 0
}
trap '_detach' INT TERM

tail -f "$LOG_FILE" &
TAIL_PID=$!

set +e
wait "$TEST_PID"
EXIT_CODE=$?
set -e
sleep 1
kill "$TAIL_PID" 2>/dev/null || true

# ── Final result ─────────────────────────────────────────────────────
echo ""
echo "  ─────────────────────────────────────────────────────────"
if [ "$EXIT_CODE" -eq 0 ]; then
  log "${GREEN}All flows passed!${RESET}"
else
  error "Some flows failed — see logs in $REPORTS_DIR"
fi
echo ""
echo -e "  ${BOLD}Full log :${RESET}  $LOG_FILE"
echo -e "  ${BOLD}XML      :${RESET}  $REPORTS_DIR/*-results.xml"
echo -e "  ${BOLD}Run again:${RESET}  cd testing && bash run_on_device.sh"
echo ""
