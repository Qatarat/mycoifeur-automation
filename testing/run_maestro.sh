#!/usr/bin/env bash
# Run Maestro tests against a connected Android device / emulator
# Usage:
#   ./run_maestro.sh                  — runs smoke suite
#   ./run_maestro.sh regression       — runs full regression suite
#   ./run_maestro.sh flow 02          — runs a single flow by number prefix
#   ./run_maestro.sh ios              — smoke suite on iOS (requires iOS device)

set -e
export PATH="$HOME/.maestro/bin:$PATH"

SUITE="${1:-smoke}"
FLOWS_DIR="maestro/flows"

case "$SUITE" in
  smoke)
    echo "▶  Running Maestro SMOKE suite..."
    maestro test "$FLOWS_DIR/suites/smoke.yaml"
    ;;
  regression)
    echo "▶  Running Maestro REGRESSION suite (all flows)..."
    maestro test "$FLOWS_DIR/suites/regression.yaml"
    ;;
  flow)
    PATTERN="${2:-01}"
    FLOW_FILE=$(ls "$FLOWS_DIR/${PATTERN}"*.yaml 2>/dev/null | head -1)
    if [ -z "$FLOW_FILE" ]; then
      echo "No flow found matching: $PATTERN"
      exit 1
    fi
    echo "▶  Running single flow: $FLOW_FILE"
    maestro test "$FLOW_FILE"
    ;;
  ios)
    echo "▶  Running Maestro SMOKE suite on iOS..."
    MAESTRO_DRIVER=ios maestro test "$FLOWS_DIR/suites/smoke.yaml"
    ;;
  *)
    echo "Usage: $0 [smoke|regression|flow <num>|ios]"
    exit 1
    ;;
esac

echo ""
echo "✓ Maestro run complete. Screenshots saved in ~/.maestro/"
