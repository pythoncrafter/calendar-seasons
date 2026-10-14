# Validation results — 2026-10-14

Environment: Linux, Node 24, Python 3.12, Chromium 154. Initial local checks had no macOS/Xcode. Subsequent GitHub checks compiled successfully on macOS 15 using Xcode 26.3. No physical iPhone, Apple signing credentials, or authenticated Google session was available to the agent.

| Validation | Result |
|---|---|
| Theme engine unit suite | Passed: local-month season mapping, manual override, international schedule, malformed/null settings, custom palettes, contrast calculations, independent defaults |
| Static repository checks | Passed: JS syntax, JSON, plists, privacy declarations, SVG/XML schemes, manifest resource paths, shared/build parity |
| Xcode project structural checks | Passed: OpenStep syntax, object references, both target phases, embedded-extension resources; not compiled |
| Chromium script/UI fixture suite | Passed: theme selection, simulated local storage, default reset, reload, DOM replacement, native event color, editable dialog, motion toggles, OS reduced motion, icon/intensity controls, narrow and landscape viewports, dark-mode media, CSS parsing |
| Real unpacked extension activation | Blocked: Chromium administrative policy explicitly disables unpacked extension loading. No policy bypass attempted. `tests/browser.cjs` is supplied for an unrestricted development machine. |
| Mobile Google website observation | Follow-up request succeeded (HTTP 200 after three redirects) with an iPhone Safari user agent. The response was Google Calendar sign-in, with one semantic main container and zero calendar grids. This is an unauthenticated HTTP observation, not a Safari rendering or authenticated mobile-calendar test. |
| Safari/Xcode compilation | Passed on GitHub macOS 15 with Xcode 26.3; app and Safari extension compiled; embedded resource checks passed |
| Physical iPhone activation | Not run; signed TestFlight/device build still requires Apple configuration |
| Live calendar creation/editing/search/views | Not run; synthetic event/dialog/navigation fixtures only |
| Signing, archive, TestFlight, store submissions | Not run; publisher credentials and review required |

Fixture tests execute the real shared browser scripts with simulated extension storage/runtime APIs. They do not establish Safari compatibility, browser permission/activation behavior, or current authenticated Google DOM compatibility. Preview screenshots depict the implemented popup UI using those fixtures.

Release gates: complete `docs/testing.md` on current Chrome and iPhone Safari, resolve any native theme/readability issues, compile/archive with Xcode, and validate final packaged resources before store submission.

## Follow-up readiness

The user confirmed that a Mac with Xcode and developer accounts are not currently available. The Chrome activation retry still returned “Loading of unpacked extensions is disabled by the administrator.” No signing or store access is configured. `scripts/validate-macos.sh` now provides an unsigned Apple simulator build and compiled-bundle resource check for a future Mac; it has been syntax-checked on Linux but not executed with Xcode.

## GitHub cloud-build preparation

Added public-repository shared/unsigned macOS build jobs and a manual default-branch TestFlight workflow. Added release-configuration tests (five passing checks), workflow YAML parsing, disposable bundle-ID/build-number configuration, a Fastlane signing/upload lane, encrypted identity recovery/reuse, and an iPhone-only setup guide. Fixed both Info.plist build numbers to follow CURRENT_PROJECT_VERSION so subsequent TestFlight uploads can use new build numbers.

No GitHub repository has been connected. Ruby is not installed here, so Fastlane syntax/execution and Apple signing APIs remain unverified; the workflow runs `ruby -c` before the credentialed lane. No cloud build, certificate generation, profile creation, or TestFlight upload has been performed.

## Published source and successful hosted-Mac build

GitHub repository-app authorization was completed. Source files and workflows were pushed to `pythoncrafter/calendar-seasons/main`. The imported ZIP was removed after the source was published. The first unsigned Mac build passed; the Chrome artifact upload path was corrected after GitHub rejected `../` in an artifact pattern. Both jobs then passed. The toolchain was updated to the newest stable Xcode on macOS 15 and both jobs passed again.

Latest code build: <https://github.com/pythoncrafter/calendar-seasons/actions/runs/38563870039>, code commit `ed7ff32068ec90123c189c9ea3557cdf6c472149`. Evidence: Xcode 26.3; `BUILD SUCCEEDED`; `PASS: Apple simulator compilation and embedded-extension bundle validation.` The run includes Chrome-extension and iOS-simulator-build-not-for-iPhone artifacts. This supersedes earlier statements that no repository/cloud build was available.

Signed archive, Apple signing/profile/API configuration, TestFlight upload, and physical-device/live Calendar validation remain pending. The GitHub integration does not allow environment/secret administration; those credentials must be configured in the user's GitHub Settings.

## Signed build and remaining Apple app-record requirement

Apple accepted the saved API key, signing certificate creation and provisioning profile creation. The missing extension bundle identifier was registered through the Apple API. Run 38586506379 built and signed the IPA successfully; upload then stopped because the containing app has no App Store Connect app record. An API creation attempt in run 38587207318 was explicitly rejected: the `apps` resource permits GET_COLLECTION, GET_INSTANCE and UPDATE, not CREATE. The account holder must create that record using My Apps > + > New App. The workflow now reports this requirement before rebuilding. The arbitrary password-length gate was removed; the configured nonempty signing password is used, and subsequent runs reuse the encrypted certificate artifact. No TestFlight upload or physical-device validation has succeeded yet.

## TestFlight upload succeeded

After the App Store Connect app record was changed to the correct containing-app bundle identifier, run <https://github.com/pythoncrafter/calendar-seasons/actions/runs/38588034814> succeeded. The workflow reused the existing signing identity, built/exported the signed IPA, and uploaded version 1.0 build 1 to App Store Connect. Apple build processing and internal tester assignment are separate from upload; physical-device Safari activation and live Calendar behavior have not been tested by the agent. Earlier pending-upload statements are historical and superseded by this result.
