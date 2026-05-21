# Qatarat (قطرات) — Mobile App Test Suite

[![Maestro Smoke](../../actions/workflows/01-maestro-smoke.yml/badge.svg)](../../actions/workflows/01-maestro-smoke.yml)
[![Maestro Regression](../../actions/workflows/02-maestro-regression.yml/badge.svg)](../../actions/workflows/02-maestro-regression.yml)
[![Appium Deep Tests](../../actions/workflows/03-appium-android.yml/badge.svg)](../../actions/workflows/03-appium-android.yml)

**Flutter app** · Android `com.qatarat.app` · iOS `com.qatarat.app`

---

## CI Workflows

| Workflow | Trigger | Duration | Coverage |
|----------|---------|----------|----------|
| Maestro Smoke | Every push / PR | ~10 min | Login, cart, checkout |
| Maestro Regression | Nightly 01:00 UTC | ~30 min | All 11 user flows |
| Appium Deep Tests | Weekly Monday | ~60 min | Payment, gifts, subscriptions |
| Maestro iOS | Manual only | ~20 min | Smoke on iOS Simulator |

## Manual Triggers

Go to **Actions** tab → choose a workflow → **Run workflow**.

The Appium workflow accepts a `marker` input:
- `payment` — card, Tabby, bank transfer
- `gift` — gift card flows
- `subscription` — weekly/monthly recurring
- *(empty)* — all tests

## Local Setup

```bash
cd testing && ./install.sh
source ~/.zshrc
```

See [testing/README.md](testing/README.md) for full local setup instructions.
