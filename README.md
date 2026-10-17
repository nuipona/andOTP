# OfflineOTP

OfflineOTP is an open-source Android authenticator that generates time-based (TOTP), counter-based (HOTP), and mOTP one-time passwords. It supports Android 9 (API 28) and later. The current app version is **0.9.0.1**; the Android application ID remains `org.shadowice.flocke.andotp`.

## Features

- Add accounts by scanning an authenticator QR code or entering details manually.
- Store the vault encrypted using Android KeyStore-backed or password/PIN-based protection.
- Create portable password-encrypted or OpenPGP-encrypted backups.
- Use light, dark, or black themes; organize entries with tags.
- Generate TOTP (RFC 6238), HOTP (RFC 4226), and mOTP codes.

## Protecting and restoring your vault

Use OfflineOTP's in-app backup and restore functions. Android cloud backup and device transfer are disabled, and copying app data with third-party backup tools does not preserve the separate KeyStore key. Export a portable backup and verify that it can be restored before changing devices, reinstalling, clearing app data, or switching to a build signed with a different key. A signing-key change requires uninstalling the old build and can erase its data.

Automatic backup broadcasts are restricted to explicitly authorized companion apps signed with the same identity; ordinary shell commands and independently signed automation apps are not authorized. See [Vault security hardening](docs/vault-security-hardening.md) for the current behavior and compatibility details.

## Build and test

The project uses Gradle, Android Gradle Plugin, Kotlin and Android SDK; current pinned toolchain details, local commands, CI gates, and limitations are documented in [Build and security tests](docs/build-and-security-tests.md). Main app sources and test suites have been migrated to Kotlin. Some checked-in sandbox/source checks are intentionally non-authoritative; successful Gradle builds and Android instrumentation are required for release confidence.

## Documentation

- [Changelog](CHANGELOG.md) — published release history.
- [Build and security tests](docs/build-and-security-tests.md) — toolchain, CI, verification steps and caveats.
- [Vault security hardening](docs/vault-security-hardening.md) — storage, session, backup and IPC security behavior.
- [Kotlin conversion record](docs/kotlin-extracted-helpers.md) — conversion scope and verification limits.
- [OTP URI parser](docs/kotlin-otp-parser-pilot.md) and [vault/session/task contracts](docs/kotlin-vault-session-task-contracts.md) — implementation details and contract boundaries.
- [UI decomposition plan](docs/ui-decomposition-plan.md) — remaining architectural extraction work.

## Contributing

Report bugs and request features through the [GitHub issue tracker](https://github.com/andOTP/andOTP/issues). For bug reports, include the app version, Android version, reproduction steps, and relevant logs; remove secrets and account data before sharing logs.

## Credits and license

OfflineOTP began as a fork of [OTP Authenticator](https://github.com/0xbb/otp-authenticator) by Bruno Bierbaumer. See the [changelog](CHANGELOG.md) for project history and [LICENSE.txt](LICENSE.txt) for the license. Open-source component acknowledgments are maintained in the app's About/Libraries screen.
