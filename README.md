# OfflineOTP - Android OTP Authenticator

![OfflineOTP](./assets/logo.png)

## Intro

OfflineOTP is a two-factor authentication app for Android 9.0+.

It implements Time-based One-time Passwords (TOTP) and HMAC-Based One-Time Passwords (HOTP).
Simply scan the QR code and log in with the generated 6-digit code.

This project started out as a fork of the great [OTP Authenticator](https://github.com/0xbb/otp-authenticator) app written by [Bruno Bierbaumer](https://github.com/0xbb),
which has sadly been inactive since 2015. By now almost every aspect of the app has been changed/re-written so the fork status of the Github repository got
detached upon [user request](https://github.com/andOTP/andOTP/issues/145). But all credit for the original version and for starting this project still goes to Bruno!

## Features:

 * Free and Open-Source
 * Requires minimal permissions
   - Camera access for QR code scanning
   - Storage access for import and export of the database
 * Encrypted storage with two backends:
   - Android KeyStore
   - Password / PIN
 * Multiple backup options:
   - Password-protected
   - OpenPGP-encrypted
 * Sleek minimalistic Material Design with three different themes:
   - Light
   - Dark
   - Black (for OLED screens)
 * Great Usability
 * Compatible with Google Authenticator
 * Supported algorithms:
   - TOTP (Time-based One-time Passwords) as specified in [RFC 6238](https://tools.ietf.org/html/rfc6238)
   - HOTP (HMAC-based One-time Passwords) as specified in [RFC 4226](https://tools.ietf.org/html/rfc4226)

## Backups:

To keep your account information as secure as possible OfflineOTP only stores it in
encrypted data files. A part of the encryption key used for that is stored in the
Android KeyStore system. The advantage of this approach is that the key is kept
separate from the apps data and, as a bonus, can be backed by hardware cryptography
(if your device supports this).

However, due to that separation, backups with 3rd-party apps like Titanium Backup can not
be used with OfflineOTP. Such apps only backup the encrypted data files and not the encryption
key, which renders them useless.

**Please only use the internal backup functions provided by OfflineOTP to backup your accounts!**
**Everything else WILL result in data loss.**

### Opening the backups on your PC:

 * [OpenPGP](https://openpgp.org/): OpenPGP can be used to easily decrypt the **OpenPGP-encrypted backups** on your PC.
 * [WebDecrypt](https://flocke.shadowice.org/andOTP/decrypt/): JavaScript-based decryption of the **new password-protected backup format** in the browser ([source code](https://github.com/andOTP/WebDecrypt)).
 * [andOTP-decrypt](https://github.com/asmw/andOTP-decrypt): Python script written by @asmw to decrypt the **old and new password-protected backup format** on your PC.
 * [mac2fa](https://github.com/lorenzo2897/mac2fa): Electron app for macOS that lives in your system tray and generates OTPs from an encrypted backup file.
 * [go-andotp](https://github.com/grijul/go-andotp): CLI Program written in go to encrypt/decrypt andOTP files on your PC. Decrypted files can be encrypted and imported back to andOTP.

### Automatic backups:

 * **Signature-authorized automation only:** `org.shadowice.flocke.andotp.broadcast.ENCRYPTED_BACKUP` requires `${applicationId}.permission.CONTROL_VAULT`, requested by a companion app signed with the **same signing identity** as OfflineOTP. An explicit package/component is also required on modern Android, but is not authorization. Independently signed Tasker/PanicKit apps and ordinary `adb shell` commands no longer have access. This compatibility break also applies to panic IPC.
 * Broadcast backups require opt-in, KeyStore database encryption, a configured backup directory and a nonempty encrypted backup password. Duplicate requests are coalesced and rate-limited. Automatic exports use new UUID-named documents to avoid overwriting the last recoverable backup.
 * **Android cloud backup/device transfer are disabled.** Use portable password-encrypted or OpenPGP backups and verify that you can restore them before changing devices, clearing keys or switching signing identities.

See [Vault security hardening](docs/vault-security-hardening.md) for input limits,
fail-closed behavior, process-only sessions, credential transactions, backup lifecycle
and remaining verification requirements.

## Contribute:

 * **Bug reports and feature requests**: You can report bugs and request features in the [Issue tracker](https://github.com/andOTP/andOTP/issues) on GitHub.
 * **Requesting thumbnails**: If you are missing a thumbnail you can request it by [opening a thumbnail request](https://github.com/andOTP/andOTP/issues/new/choose).

#### Donations:

If you want to show your appreciation for the predecessor to our work with a small donation you can do so using the following links:

 * [Donate to Jakob Nixdorf](https://flocke.shadowice.org/donate.html) (Main developer, maintainer)
 * [Donate to Richy HBM](https://richyhbm.co.uk/donate) (Developer)

## Acknowledgments:
#### Open-source components used:

 * [AboutLibraries](https://github.com/mikepenz/AboutLibraries)
 * [Apache Commons Codec](https://commons.apache.org/proper/commons-codec/)
 * [Expandable Layout](https://github.com/AAkira/ExpandableLayout)
 * [Floating Action Button Speed Dial](https://github.com/leinardi/FloatingActionButtonSpeedDial)
 * [material-intro](https://github.com/heinrichreimer/material-intro)
 * [MaterialProgressBar](https://github.com/DreaminginCodeZH/MaterialProgressBar)
 * [OpenPGP API library](https://github.com/open-keychain/openpgp-api)
 * [ZXing Android Embedded](https://github.com/journeyapps/zxing-android-embedded)
 * [Droid Sans Mono Zeromod](https://github.com/AlbertoDorado/droid-sans-mono-zeromod)

## License:
```
# LICENSE

Copyright (c) 2026 unsubstantiation (fairuniversal.com)

This software is licensed under the PolyForm Noncommercial License 1.0.0. 
You may use, copy, modify, and distribute this software for noncommercial purposes only.

### Attribution Requirement
Any copying, distribution, or modification of this code or its contents strictly requires 
prominent attribution to the original author (unsubstantiation) by retaining the above 
copyright notice in all copies or substantial portions of the software.

To view the full terms, visit: https://polyformproject.org

--------------------------------------------------------------------------------

# ATTRIBUTION

This project is a complete update from android 5.1+ to android 9+ rewrite in Kotlin of andOTP, originally copyright 
(C) 2017-2020 Jakob Nixdorf and (C) 2015 Bruno Bierbaumer.
