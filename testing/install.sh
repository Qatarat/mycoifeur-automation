#!/usr/bin/env bash
# Qatarat App — Full Test Environment Installer
# Installs: Java 17, Android SDK (ADB), Maestro, Appium + drivers, Python venv + deps
set -e

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; NC='\033[0m'
log()  { echo -e "${GREEN}[✓]${NC} $1"; }
warn() { echo -e "${YELLOW}[!]${NC} $1"; }
fail() { echo -e "${RED}[✗]${NC} $1"; exit 1; }

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo ""
echo "================================================"
echo "  Qatarat Test Suite — Environment Setup"
echo "================================================"
echo ""

# ── Homebrew ────────────────────────────────────────
if ! command -v brew &>/dev/null; then
  fail "Homebrew not found. Install from https://brew.sh first."
fi
log "Homebrew found: $(brew --version | head -1)"

# ── Java 17 (required by Maestro + Appium) ──────────
# Check properly: java -version exits 0 even when JRE missing on macOS, so test the output
JAVA_OK=false
# Check openjdk@17 keg-only path first, then fall back to java_home
if [ -x "/opt/homebrew/opt/openjdk@17/bin/java" ]; then
  JAVA_OK=true
elif /usr/libexec/java_home -v 17 &>/dev/null 2>&1; then
  JAVA_OK=true
fi

if [ "$JAVA_OK" = false ]; then
  warn "Java 17 not found — installing openjdk@17 via Homebrew..."
  # Use formula (not cask) — no sudo required
  brew install openjdk@17
  log "openjdk@17 installed"
fi

# openjdk@17 is keg-only, must use explicit path
export JAVA_HOME="/opt/homebrew/opt/openjdk@17"
export PATH="$JAVA_HOME/bin:$PATH"

# Persist to shell config (only add once)
if ! grep -q 'openjdk@17' ~/.zshrc 2>/dev/null; then
  echo '' >> ~/.zshrc
  echo '# Java 17 via Homebrew openjdk@17 (added by Qatarat test installer)' >> ~/.zshrc
  echo 'export JAVA_HOME="/opt/homebrew/opt/openjdk@17"' >> ~/.zshrc
  echo 'export PATH="$JAVA_HOME/bin:$PATH"' >> ~/.zshrc
fi
log "Java OK: $(java -version 2>&1 | head -1)"

# ── Android Command-Line Tools + platform-tools (ADB) ──
ANDROID_HOME="${ANDROID_HOME:-$HOME/Library/Android/sdk}"

if ! command -v adb &>/dev/null && [ ! -f "$ANDROID_HOME/platform-tools/adb" ]; then
  warn "ADB not found — installing Android command-line tools..."
  brew install --cask android-commandlinetools 2>/dev/null || warn "android-commandlinetools already installed"
  mkdir -p "$ANDROID_HOME"
  warn "Installing platform-tools via sdkmanager..."
  yes | JAVA_HOME="$JAVA_HOME" sdkmanager \
    --sdk_root="$ANDROID_HOME" \
    "platform-tools" \
    "platforms;android-34" \
    "build-tools;34.0.0" 2>&1 | grep -v "^[[:space:]]*$" | tail -5 || true
fi

export ANDROID_HOME="$ANDROID_HOME"
export PATH="$ANDROID_HOME/platform-tools:$PATH"

if ! grep -q 'ANDROID_HOME' ~/.zshrc 2>/dev/null; then
  echo '' >> ~/.zshrc
  echo '# Android SDK (added by Qatarat test installer)' >> ~/.zshrc
  echo "export ANDROID_HOME=\"$ANDROID_HOME\"" >> ~/.zshrc
  echo 'export PATH="$ANDROID_HOME/platform-tools:$PATH"' >> ~/.zshrc
fi

command -v adb &>/dev/null && log "ADB OK: $(adb version | head -1)" || warn "ADB not in PATH yet — will work after: source ~/.zshrc"

# ── Maestro ─────────────────────────────────────────
export PATH="$HOME/.maestro/bin:$PATH"
if ! command -v maestro &>/dev/null; then
  warn "Maestro not found — installing..."
  curl -Ls "https://get.maestro.mobile.dev" | bash
  export PATH="$HOME/.maestro/bin:$PATH"
  if ! grep -q '.maestro/bin' ~/.zshrc 2>/dev/null; then
    echo 'export PATH="$HOME/.maestro/bin:$PATH"' >> ~/.zshrc
  fi
fi
command -v maestro &>/dev/null && log "Maestro OK: $(maestro --version)" || warn "Maestro not in PATH yet"

# ── Node / npm ──────────────────────────────────────
if ! command -v node &>/dev/null; then
  fail "Node.js not found. Install from https://nodejs.org first."
fi
log "Node OK: $(node --version)"

# ── Appium ──────────────────────────────────────────
if ! command -v appium &>/dev/null; then
  warn "Appium not found — installing globally..."
  npm install -g appium
fi
log "Appium OK: $(appium --version)"

# ── Appium Drivers ───────────────────────────────────
warn "Installing/verifying Appium drivers..."
appium driver install uiautomator2 2>/dev/null || true
appium driver install xcuitest 2>/dev/null || true
appium driver install --source=npm appium-flutter-driver 2>/dev/null || true
appium plugin install execute-driver 2>/dev/null || true
log "Appium drivers OK"

# ── Python venv + deps ───────────────────────────────
# macOS 12+ blocks system pip — use a virtualenv instead
VENV_DIR="$SCRIPT_DIR/appium/.venv"
if [ ! -d "$VENV_DIR" ]; then
  warn "Creating Python virtualenv at appium/.venv ..."
  python3 -m venv "$VENV_DIR"
fi

warn "Installing Python dependencies into venv..."
"$VENV_DIR/bin/pip" install --upgrade pip --quiet
"$VENV_DIR/bin/pip" install -r "$SCRIPT_DIR/appium/requirements.txt" --quiet
log "Python deps OK (venv: appium/.venv)"

# Patch run_appium.sh to use venv python automatically
sed -i '' "s|python3 -m pytest|\"$VENV_DIR/bin/python\" -m pytest|g" "$SCRIPT_DIR/run_appium.sh" 2>/dev/null || true

# ── Verify ───────────────────────────────────────────
echo ""
echo "================================================"
echo "  Setup Complete — Status"
echo "================================================"
echo ""
java -version 2>&1 | head -1 && log "Java 17" || warn "Java: check failed"
command -v adb &>/dev/null      && log "ADB: $(adb version | head -1 | cut -c1-50)" || warn "ADB: run 'source ~/.zshrc' then check again"
command -v maestro &>/dev/null  && log "Maestro: $(maestro --version)"               || warn "Maestro: run 'source ~/.zshrc' then check again"
command -v appium &>/dev/null   && log "Appium: $(appium --version)"                 || warn "Appium: not found"
[ -f "$VENV_DIR/bin/python" ]   && log "Python venv: $VENV_DIR"                      || warn "Python venv: not found"
echo ""
warn "Reload your shell:  source ~/.zshrc"
echo ""
echo "  Next steps:"
echo "  1. source ~/.zshrc"
echo "  2. Connect Android device  OR  start an Android emulator"
echo "  3. adb devices                    # confirm device is listed"
echo "  4. cd testing && ./run_maestro.sh          # Phase 1 smoke"
echo "  5. cd testing && ./run_appium.sh           # Phase 2 deep tests"
echo ""
