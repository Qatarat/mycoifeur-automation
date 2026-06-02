#!/usr/bin/env bash
# Smoke CI runner — called from reactivecircus/android-emulator-runner script:
# Each flow runs independently; failures are counted but don't stop the suite.
#
# LOCAL USAGE:
#   bash testing/run_smoke_ci.sh                          # use already-installed APK
#   APK_PATH=/path/to/MyCoiffeur.apk bash testing/run_smoke_ci.sh  # install new APK first
set -uo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
FLOWS_DIR="$SCRIPT_DIR/maestro/flows"
REPORTS_DIR="$SCRIPT_DIR/maestro/reports"
mkdir -p "$REPORTS_DIR"

# ── Optional: install a new APK before testing ──────────────────────────────
if [ -n "${APK_PATH:-}" ]; then
  echo "📱 Installing new APK: $APK_PATH"
  adb install -r "$APK_PATH"
  echo "✅ APK installed"
fi

FLOW_TIMEOUT=300   # 5 min hard cap per flow — prevents a stuck flow from eating the budget

FAIL=0
for flow_yaml in "$FLOWS_DIR"/[0-9][0-9]_*.yaml; do
  flow="$(basename "$flow_yaml" .yaml)"
  xml_out="$REPORTS_DIR/${flow}-results.xml"
  echo "▶  Running flow: $flow"
  timeout "$FLOW_TIMEOUT" maestro test --format junit \
    --output "$xml_out" \
    "$flow_yaml" \
    && echo "   ✓ $flow" \
    || {
      RC=$?
      [ "$RC" -eq 124 ] && echo "   ✗ $flow TIMED OUT (>${FLOW_TIMEOUT}s)" \
                        || echo "   ✗ $flow FAILED (exit $RC)"
      FAIL=$((FAIL + 1))
      # Write a minimal failure XML when maestro didn't produce one
      # (happens on timeout — ensures the report shows 'fail' not 'idle')
      if [ ! -f "$xml_out" ] || [ ! -s "$xml_out" ]; then
        local_msg="Flow timed out after ${FLOW_TIMEOUT}s"
        [ "$RC" -ne 124 ] && local_msg="Flow failed with exit code $RC"
        cat > "$xml_out" <<FAILXML
<?xml version="1.0" encoding="utf-8"?>
<testsuites>
  <testsuite name="${flow}" tests="1" errors="0" failures="1" skipped="0" time="0">
    <testcase name="${flow}"><failure message="${local_msg}" /></testcase>
  </testsuite>
</testsuites>
FAILXML
      fi
    }
  # Capture device screenshot via ADB after every flow (works even on failure)
  adb exec-out screencap -p > "$REPORTS_DIR/${flow}-screenshot.png" 2>/dev/null \
    && echo "   📸 screenshot saved" || true
done

echo ""
echo "Smoke complete: $FAIL flow(s) failed."
exit $FAIL
