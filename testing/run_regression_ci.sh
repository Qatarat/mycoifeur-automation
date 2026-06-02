#!/usr/bin/env bash
# Regression CI runner — called from reactivecircus/android-emulator-runner script:
# Pass a flow number prefix (e.g. "07") as $1 to run a single flow; omit for all flows.
#
# LOCAL USAGE:
#   bash testing/run_regression_ci.sh                          # use already-installed APK
#   APK_PATH=/path/to/MyCoiffeur.apk bash testing/run_regression_ci.sh  # install new APK first
set -uo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
FLOWS_DIR="$SCRIPT_DIR/maestro/flows"
REPORTS_DIR="$SCRIPT_DIR/maestro/reports"
SOLO_FLOW="${1:-}"
mkdir -p "$REPORTS_DIR"

FLOW_TIMEOUT=300   # 5 min hard cap per flow (consistent with smoke; keeps 50 flows within 150 min)

# ── Emulator warm-up ────────────────────────────────────────────────────────
echo "⏳ Waiting for emulator to be fully booted and responsive..."
adb wait-for-device
# Poll until sys.boot_completed=1
for i in $(seq 1 60); do
  if adb shell getprop sys.boot_completed 2>/dev/null | grep -q "^1$"; then
    break
  fi
  sleep 2
done
# Unlock screen and dismiss any system dialogs
adb shell input keyevent 82 2>/dev/null || true
adb shell input keyevent 4  2>/dev/null || true
# Give the launcher time to settle before the first flow
sleep 8
echo "✅ Emulator ready — starting flows"
# ────────────────────────────────────────────────────────────────────────────

# ── Optional: install a new APK before testing ──────────────────────────────
if [ -n "${APK_PATH:-}" ]; then
  echo "📱 Installing new APK: $APK_PATH"
  adb install -r "$APK_PATH"
  echo "✅ APK installed"
fi

_run_flow() {
  local flow_file="$1"
  local name
  name="$(basename "$flow_file" .yaml)"
  local xml_out="$REPORTS_DIR/${name}-results.xml"
  echo "▶  Running flow: $name"
  timeout "$FLOW_TIMEOUT" maestro test --format junit \
    --output "$xml_out" \
    "$flow_file" \
    && echo "   ✓ $name" \
    || {
      RC=$?
      [ "$RC" -eq 124 ] && echo "   ✗ $name TIMED OUT (>${FLOW_TIMEOUT}s)" \
                        || echo "   ✗ $name FAILED (exit $RC)"
      # Write a minimal failure XML when maestro didn't produce one
      # (happens on timeout — ensures the report shows 'fail' not 'idle')
      if [ ! -f "$xml_out" ] || [ ! -s "$xml_out" ]; then
        local msg
        [ "$RC" -eq 124 ] && msg="Flow timed out after ${FLOW_TIMEOUT}s" || msg="Flow failed with exit code $RC"
        cat > "$xml_out" <<FAILXML
<?xml version="1.0" encoding="utf-8"?>
<testsuites>
  <testsuite name="${name}" tests="1" errors="0" failures="1" skipped="0" time="0">
    <testcase name="${name}"><failure message="${msg}" /></testcase>
  </testsuite>
</testsuites>
FAILXML
      fi
      adb exec-out screencap -p > "$REPORTS_DIR/${name}-screenshot.png" 2>/dev/null || true
      return 1
    }
  # Capture device screenshot via ADB after every flow (even on pass)
  adb exec-out screencap -p > "$REPORTS_DIR/${name}-screenshot.png" 2>/dev/null \
    && echo "   📸 screenshot saved" || true
}

FAIL=0
if [ -n "$SOLO_FLOW" ]; then
  FLOW_FILE="$(ls "$FLOWS_DIR/${SOLO_FLOW}"*.yaml 2>/dev/null | head -1)"
  if [ -z "$FLOW_FILE" ]; then
    echo "ERROR: no flow file found for prefix '$SOLO_FLOW'"
    exit 1
  fi
  _run_flow "$FLOW_FILE" || FAIL=1
else
  for flow_file in "$FLOWS_DIR"/[0-9][0-9]_*.yaml; do
    _run_flow "$flow_file" || FAIL=$((FAIL + 1))
  done
fi

echo ""
echo "Regression complete: $FAIL flow(s) failed."
exit $FAIL
