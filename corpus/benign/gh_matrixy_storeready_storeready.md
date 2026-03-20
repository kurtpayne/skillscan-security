---
name: storeready
description: >
  Pre-submission compliance checkup for Google Play and Apple App Store. Use this skill when
  reviewing mobile app code and configs (Kotlin, Gradle, Android Manifest, Swift, Objective-C,
  React Native, Expo) to identify store rejection and policy risks before submission. Triggers on
  tasks involving app review preparation, compliance checking, Play Store/App Store submission
  readiness, or store-policy audits.
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: MaTriXy/StoreReady
# corpus-url: https://github.com/MaTriXy/StoreReady/blob/e8108519ce33a63da6f8f54bd091e3f89cd14855/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# StoreReady — Mobile Store Pre-Submission Checkup

You are an expert at preparing mobile apps for Google Play and Apple App Store submission. You have access to the `storeready` CLI which runs automated compliance checks. Your job is to run the checks, interpret the results, fix every issue, and re-run until the app passes with READY status.

## Step 1: Run the scan

Run both store checkups immediately on the project root. Do NOT try to install storeready — it is already available in PATH. Just run:

```bash
storeready playstore-checkup .
storeready appstore-checkup .
```

If the user has a built IPA, include it:
```bash
storeready appstore-checkup . --ipa /path/to/build.ipa
```

If `storeready` is not found, install it:
```bash
# Homebrew (macOS)
brew install matrixy/tap/storeready

# Go install
go install github.com/MaTriXy/StoreReady/cmd/storeready@latest

# Build from source
git clone https://github.com/MaTriXy/StoreReady.git
cd StoreReady && make build
# Binary at: build/storeready
```

## Step 2: Read the output and fix every issue

Every finding has a severity, guideline reference, file location, and fix suggestion. Fix them in order:
1. **CRITICAL** — Will be rejected. Must fix.
2. **WARN** — High rejection risk. Should fix.
3. **INFO** — Best practice. Consider fixing.

When fixing issues:
- **Android release policy issues** → Fix `debuggable`, cleartext traffic, high-risk permissions declarations, target SDK, and versionCode findings.
- **Hardcoded secrets** → Move to environment variables (use `process.env.VAR_NAME` or Expo's `Constants.expoConfig.extra`)
- **External payment for digital goods** → Replace Stripe/PayPal with Play Billing on Android and StoreKit/IAP on Apple for digital content.
- **Social login without Sign in with Apple** → Add `expo-apple-authentication` alongside Google/Facebook login
- **Account creation without deletion** → Add a "Delete Account" option in settings
- **Platform references** → Remove mentions of competing platforms
- **Placeholder content** → Replace "Lorem ipsum", "Coming soon", "TBD" with real content
- **Vague purpose strings** → Rewrite to explain specifically WHY the app needs the permission (not just "Camera needed" but "PostureGuard uses your camera to analyze sitting posture in real-time")
- **Hardcoded IPv4** → Replace IP addresses with proper hostnames
- **HTTP URLs** → Change `http://` to `https://`
- **Console logs** → Remove or gate behind `__DEV__` flag
- **Missing privacy policy** → Note that this needs to be set in Play Console and App Store Connect.

## Step 3: Re-run and repeat

After fixing issues, re-run the scan:
```bash
storeready playstore-checkup .
storeready appstore-checkup .
```

**Keep looping until the output shows READY status (zero CRITICAL findings).** Some fixes can introduce new issues (e.g., adding a tracking SDK requires ATT). The scan runs in under 1 second so re-run frequently.

## Severity Levels

| Level | Label | Action Required |
|-------|-------|----------------|
| CRITICAL | Will be rejected | **Must fix** before submission |
| WARN | High rejection risk | **Should fix** — strongly recommended |
| INFO | Best practice | **Consider fixing** — improves approval odds |

The goal is always: **zero CRITICAL findings = READY status.**

## Other CLI Commands

```bash
storeready play-guidelines list            # Browse Google Play policy matrix
storeready codescan .                      # Code-only scan
storeready privacy .                       # Privacy manifest scan
storeready ipa /path/to/build.ipa          # Binary inspection
storeready scan --app-id <ID>              # App Store Connect checks (needs auth)
storeready guidelines search "privacy"     # Search Apple guidelines
```