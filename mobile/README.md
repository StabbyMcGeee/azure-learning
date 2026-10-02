# Study App (placeholder)

Offline-first Flutter mobile app for iOS and Android.

> **Placeholders.** The display name `Study App (placeholder)`, the package
> identifier `com.example.studyapp`, and the bundle identifier
> `com.example.studyapp` are temporary and must be replaced after the final
> brand is legally screened and chosen. Do not ship with these identifiers.

## Product scope

- v1 is a **single, one-time paid app download** (target ~$1 upfront).
- **No** account, sign-in, sync, analytics, ads, or in-app payment SDK.
- Works offline. All study progress is stored locally with SQLite.
- The runtime question bank is loaded at startup from the bundled content pack
  (`assets/content-pack.json`, AZ-900 / DP-900 / AI-901). The legacy desktop
  133-question bank is intentionally **not** imported; production content is
  authored fresh with a per-item rights basis recorded in
  `docs/content-provenance.md`.
- Synthetic test fixtures exist only in `test/` and are never shipped as
  production curriculum.

## Architecture

- `lib/models/` — question, attempt, session, progress data classes.
- `lib/data/` — `LocalStore` (SQLite persistence) and `QuestionBank` (empty
  hardcoded list + synthetic test fixtures; runtime content comes from the
  bundled pack).
- `lib/navigation/` — named-route router.
- `lib/screens/` — dashboard, study, practice, exam, exam result, review,
  progress.
- `lib/widgets/` — reusable empty-state, question card, and answer widgets.
- Tests use `FakeLocalStore` for widget tests and an in-memory FFI database for
  unit/persistence tests. The FFI implementation does not run under the Flutter
  test binding's fake async, so widget tests use the fake implementation.

## Validation status

- `flutter analyze` passes.
- `flutter test` passes.
- **Android build was not validated.** This WSL Linux host has Flutter but no
  Android SDK or Java toolchain installed, and no SDK licenses were accepted.
  Build with `flutter build apk` or `flutter build appbundle` only on a
  properly licensed Android SDK host.
- **iOS build was not validated.** This host has no Xcode or macOS, which are
  required to compile or sign an iOS archive. Build with `flutter build ios`
  or `flutter build ipa` only on a Mac with Xcode and a valid Apple developer
  account.
- No physical device or emulator testing was performed.

## Next steps before release

1. Finalize and clear the public brand, app name, and trademark.
2. Replace placeholder package/bundle identifiers in:
   - `android/app/build.gradle.kts`
   - `ios/Runner.xcodeproj/project.pbxproj`
   - `android/app/src/main/AndroidManifest.xml`
   - `ios/Runner/Info.plist`
   - `pubspec.yaml` description
3. Complete the publisher's substantive review of the launch pack, recorded as
   PENDING in `docs/content-provenance.md`, and obtain a qualified human legal
   review before paid sale.
4. Add app icons, splash screens, store metadata, privacy policy, support URL,
   and an in-app About/Legal screen.
5. Add release signing for Android and iOS.
6. Run device acceptance, accessibility, offline, and store-readiness audits.
