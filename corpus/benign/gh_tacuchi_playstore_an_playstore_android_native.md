---
name: playstore-android-native
description: >
  Guide and review the preparation of a native Android (Java/Kotlin) project for Google Play Store
  release. Covers keystore generation, signing configuration, ProGuard/R8 rules, and AAB build.
  Use when the user wants to publish, release, deploy, sign, or prepare a native Android app
  for Play Store, or when they mention "bundleRelease", "release signing", "play store android",
  "proguard rules", "R8 errors", "signing config", or "generate keystore".
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: Tacuchi/playstore-android-native
# corpus-url: https://github.com/Tacuchi/playstore-android-native/blob/80c9c43b84d2624483502fffab563f68b1875ba9/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Play Store Release — Android Native

Build a signed Android App Bundle (AAB) from a native Android (Java/Kotlin) project, ready for Google Play Store.

## Before You Start — Assess the Project

Ask these questions BEFORE touching any files:

1. **Gradle DSL?** Check `app/build.gradle` vs `build.gradle.kts`
   - `.kts` → use `isMinifyEnabled` (with `is` prefix)
   - `.gradle` → use `minifyEnabled` (without `is` prefix)
   - NEVER mix — using the wrong property is a **silent no-op** (no error, no minification)

2. **Existing signing config?** Search for `signingConfigs` in the app build file
   - Already exists → Verify it reads from a properties file, don't duplicate
   - Missing → Add from scratch

3. **Existing keystore?** Ask the user before generating a new one
   - Already has `.jks` → Reuse it, skip Step 1
   - First release → Generate new keystore

4. **Which libraries need ProGuard rules?** Check `build.gradle` dependencies block:
   - Uses Retrofit/OkHttp → Add network rules
   - Uses Gson → Add serialization rules (or better: suggest migrating to kotlinx.serialization)
   - Uses kotlinx.serialization → Add `@Serializable` keep rules
   - Uses Room/Hilt/Dagger → No custom rules needed (compile-time code generation)
   - Only Jetpack Compose → No custom rules needed (Compose compiler handles it)

5. **AGP version?** Check `libs.versions.toml` or root `build.gradle`
   - AGP 8+ → Requires Java 17. Verify `JAVA_HOME` or `org.gradle.java.home`
   - AGP 7.x → Java 11 sufficient

6. **Flavors?** Search for `productFlavors` in the build file
   - Has flavors → Each flavor needs its own or a shared signing config; build command changes to `bundleProdRelease` etc.
   - No flavors → Single release config

---

## Workflow

| Step | Action | Key file |
|------|--------|----------|
| 1 | Generate upload keystore | `upload-keystore.jks` |
| 2 | Create credentials file | `keystore.properties` |
| 3 | Configure signing in Gradle | `app/build.gradle.kts` |
| 4 | Configure ProGuard / R8 (by dependency) | `app/proguard-rules.pro` |
| 5 | Build release AAB | CLI |
| 6 | Verify output | CLI + checklist |

---

## Step 1 — Generate Upload Keystore

```bash
keytool -genkeypair \
  -alias upload \
  -keyalg RSA -keysize 2048 \
  -validity 10000 \
  -storetype PKCS12 \
  -keystore upload-keystore.jks
```

Critical details:
- `-validity 10000` = ~27 years. Google requires validity beyond Oct 22 2033.
- `-storetype PKCS12` — avoids JKS migration warnings. But with PKCS12, **store password and key password must be identical**. `keytool` silently uses the store password for the key. Different passwords → signing fails later with misleading "Cannot recover key" error.
- Store the `.jks` outside the project. Recommended: `~/.android/keystores/` or a secrets manager.

---

## Step 2 — Create Credentials File

Create `keystore.properties` in the project root (must NOT be committed):

```properties
storePassword=<password>
keyPassword=<same-password-as-store>
keyAlias=upload
storeFile=<absolute-or-relative-path-to-upload-keystore.jks>
```

Add to `.gitignore`:

```gitignore
keystore.properties
*.jks
*.keystore
local.properties
```

---

## Step 3 — Configure Signing in Gradle

Claude knows Gradle signing config syntax. These are the traps:

- **`isMinifyEnabled` vs `minifyEnabled`**: KTS requires the `is` prefix. Groovy does NOT. Wrong prefix = **silent no-op** — build succeeds, APK is unminified, 3x larger, and exposes source code. No error, no warning. This is the #1 Android release mistake.
- **`isShrinkResources` requires `isMinifyEnabled`**: Resource shrinking without code minification silently does nothing. Always set both together.
- **`signingConfigs` before `buildTypes`**: Gradle evaluates blocks in declaration order. Referencing a signingConfig before it's declared → build error.
- **`rootProject.file()` vs `project.file()`**: `keystore.properties` lives in project root. `rootProject` = project root. `project` = `app/` module. Wrong root = file not found silently, null properties at build time.

### Kotlin DSL (`app/build.gradle.kts`)

```kotlin
import java.util.Properties
import java.io.FileInputStream

val keystoreProperties = Properties().apply {
    val file = rootProject.file("keystore.properties")
    if (file.exists()) load(FileInputStream(file))
}

android {
    signingConfigs {
        create("release") {
            keyAlias = keystoreProperties["keyAlias"] as String
            keyPassword = keystoreProperties["keyPassword"] as String
            storeFile = file(keystoreProperties["storeFile"] as String)
            storePassword = keystoreProperties["storePassword"] as String
        }
    }
    buildTypes {
        release {
            isMinifyEnabled = true
            isShrinkResources = true
            signingConfig = signingConfigs.getByName("release")
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }
}
```

For Groovy DSL: same structure but use `def keystoreProperties = new Properties()`, untyped property access `keystoreProperties['keyAlias']`, `minifyEnabled true` (no `is` prefix), `shrinkResources true`, and `signingConfig signingConfigs.release` (no `=`).

---

## Step 4 — ProGuard / R8 (Add Rules By Dependency)

R8 is NOT enabled by default in native Android — you must explicitly set `isMinifyEnabled = true`. Then add rules ONLY for libraries the project actually uses:

| Dependency | Needs rules? | Why |
|------------|-------------|-----|
| Retrofit | YES | Uses reflection for interface proxies |
| OkHttp | YES | Uses reflection for platform detection |
| Gson | YES | Deserializes via reflection on field names |
| kotlinx.serialization | YES | Compiler plugin generates serializers that R8 strips |
| Coroutines | YES | Internal classes loaded via ServiceLoader |
| Room | NO | Annotation processor, compile-time only |
| Hilt/Dagger | NO | Compile-time code generation |
| Jetpack Compose | NO | Compose compiler handles it |
| Coil/Glide | MAYBE | Only if using custom transformations |

When R8 reports `Missing class:` — copy rules from the error output verbatim.
When a crash occurs only in release build — the stripped class is in the stack trace.

### Common rules (add only what applies):

```proguard
# Kotlin (always needed with minification)
-keep class kotlin.Metadata { *; }
-dontwarn kotlin.**

# Coroutines
-keepnames class kotlinx.coroutines.internal.MainDispatcherFactory {}
-keepnames class kotlinx.coroutines.CoroutineExceptionHandler {}
-keepclassmembers class kotlinx.coroutines.** { volatile <fields>; }

# kotlinx.serialization
-keepattributes *Annotation*, InnerClasses
-dontnote kotlinx.serialization.AnnotationsKt
-keepclassmembers class kotlinx.serialization.json.** { *** Companion; }
-keep,includedescriptorclasses class **$$serializer { *; }
-keepclassmembers class * { @kotlinx.serialization.Serializable *; }

# Retrofit + OkHttp
-keepattributes Signature, Exceptions
-keep class retrofit2.** { *; }
-keepclasseswithmembers class * { @retrofit2.http.* <methods>; }
-dontwarn okhttp3.**
-dontwarn okio.**

# Gson (consider migrating to kotlinx.serialization)
-keep class * extends com.google.gson.TypeAdapter
-keep class * implements com.google.gson.TypeAdapterFactory
-keepclassmembers,allowobfuscation class * {
    @com.google.gson.annotations.SerializedName <fields>;
}
```

---

## Step 5 — Build Release AAB

```bash
./gradlew bundleRelease
```

Useful flags:
- `--stacktrace` — full stack trace on R8/signing errors.
- `-Pandroid.injected.signing.store.file=...` — override signing via CLI (CI use).
- `./gradlew clean bundleRelease` — clean before building after Gradle config changes.

Output: `app/build/outputs/bundle/release/app-release.aab`

---

## Step 6 — Verify Before Upload

```bash
# Verify signing — confirm alias is "upload", NOT "androiddebugkey"
keytool -printcert -jarfile app/build/outputs/bundle/release/app-release.aab

# Verify version (requires bundletool)
bundletool dump manifest --bundle=app/build/outputs/bundle/release/app-release.aab \
  | grep -E "versionCode|versionName"
```

Checklist:
- [ ] AAB signed with **upload** key (not debug) — debug key = #1 rejection reason
- [ ] `versionCode` higher than the previous upload
- [ ] `keystore.properties` and `*.jks` in `.gitignore`
- [ ] `isMinifyEnabled = true` and `isShrinkResources = true` both set
- [ ] ProGuard rules added only for reflection-heavy dependencies

---

## NEVER Do

1. **NEVER use the wrong minify property name** — KTS: `isMinifyEnabled`. Groovy: `minifyEnabled`. The wrong one compiles fine but is a **silent no-op** — your release build is unminified, 3x larger, and exposes full source code. No error, no warning. Test by checking AAB size.

2. **NEVER enable `isShrinkResources` without `isMinifyEnabled`** — Resource shrinking depends on code minification to determine which resources are referenced. Without minify, shrink silently does nothing. Always set both.

3. **NEVER set different store/key passwords with PKCS12** — `keytool` silently uses store password for key. Different passwords → signing fails with "Cannot recover key" (misleading — it's a password mismatch, not a corrupt key).

4. **NEVER dump all ProGuard rules blindly** — Add rules ONLY for libraries the project uses. Unnecessary `-keep` rules defeat the purpose of R8 by preventing dead code removal and increasing APK size.

5. **NEVER skip testing the signed AAB** — R8 stripping is invisible until runtime. Install the release build on a real device and test all screens, especially those using serialization, reflection, or native code. Crashes that only appear in release builds are always R8-related.

6. **NEVER ignore lint errors by default** — `abortOnError = false` in `lint {}` block is a common workaround, but it hides real issues. Fix lint errors first. Only suppress specific lint IDs you've reviewed: `disable += "SomeSpecificCheck"`.

---

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `Missing class: ...` during R8 | R8 strips classes used via reflection | Add `-keep` rules from error output |
| `NoSuchMethodError` at runtime | R8 removed constructor needed by serialization | Add `-keep` for affected data class |
| Serialization crash only in release | `@Serializable` classes stripped by R8 | Add kotlinx-serialization ProGuard rules |
| `Lint found errors` blocking build | `abortOnError` is true by default | Fix lint issues or suppress specific IDs |
| "debug certificate" rejection | Built without release signing config | Verify `signingConfig` in `buildTypes.release` |
| Build succeeds but APK is huge | `isMinifyEnabled` silently not applied | Check property name matches DSL (is/no-is) |

---

## Gotchas

1. **Java 17 is required for AGP 8+** — If build fails with "Unsupported class file major version", set `org.gradle.java.home` in `gradle.properties` to a JDK 17+ path. Or set `JAVA_HOME` in your shell environment.

2. **`local.properties` must not be committed** — Contains machine-specific SDK path. Always in `.gitignore`. If it's committed and another dev has a different SDK path, builds fail with confusing "SDK not found" errors.

3. **App Signing by Google Play** — Google re-signs your app with their app signing key. The keystore you generate is the **upload key** only. If you lose it, request a reset through Play Console (takes days, requires identity verification).

4. **Flavor-aware build commands** — With `productFlavors`, `bundleRelease` builds ALL flavors. To build a specific one: `./gradlew bundleProdRelease` (capitalize flavor name). The output path also changes: `app/build/outputs/bundle/prodRelease/`.