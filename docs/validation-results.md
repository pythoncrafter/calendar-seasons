# Validation results — 2026-10-14

Environment: Linux, Node 24, Python 3.12, Chromium 154. No macOS, Xcode, Safari, physical iPhone, Apple team, signing profile, or authenticated Google session was available.

| Validation | Result |
|---|---|
| Theme engine unit suite | Passed: local-month season mapping, manual override, international schedule, malformed/null settings, custom palettes, contrast calculations, independent defaults |
| Static repository checks | Passed: JS syntax, JSON, plists, privacy declarations, SVG/XML schemes, manifest resource paths, shared/build parity |
| Xcode project structural checks | Passed: OpenStep syntax, object references, both target phases, embedded-extension resources; not compiled |
| Chromium script/UI fixture suite | Passed: theme selection, simulated local storage, default reset, reload, DOM replacement, native event color, editable dialog, motion toggles, OS reduced motion, icon/intensity controls, narrow and landscape viewports, dark-mode media, CSS parsing |
| Real unpacked extension activation | Blocked: Chromium administrative policy explicitly disables unpacked extension loading. No policy bypass attempted. `tests/browser.cjs` is supplied for an unrestricted development machine. |
| Mobile Google website observation | Follow-up request succeeded (HTTP 200 after three redirects) with an iPhone Safari user agent. The response was Google Calendar sign-in, with one semantic main container and zero calendar grids. This is an unauthenticated HTTP observation, not a Safari rendering or authenticated mobile-calendar test. |
| Safari/Xcode build and device activation | Not run; requires Mac and physical iPhone |
| Live calendar creation/editing/search/views | Not run; synthetic event/dialog/navigation fixtures only |
| Signing, archive, TestFlight, store submissions | Not run; publisher credentials and review required |

Fixture tests execute the real shared browser scripts with simulated extension storage/runtime APIs. They do not establish Safari compatibility, browser permission/activation behavior, or current authenticated Google DOM compatibility. Preview screenshots depict the implemented popup UI using those fixtures.

Release gates: complete `docs/testing.md` on current Chrome and iPhone Safari, resolve any native theme/readability issues, compile/archive with Xcode, and validate final packaged resources before store submission.

## Follow-up readiness

The user confirmed that a Mac with Xcode and developer accounts are not currently available. The Chrome activation retry still returned “Loading of unpacked extensions is disabled by the administrator.” No signing or store access is configured. `scripts/validate-macos.sh` now provides an unsigned Apple simulator build and compiled-bundle resource check for a future Mac; it has been syntax-checked on Linux but not executed with Xcode.

## GitHub cloud-build preparation

Added public-repository shared/unsigned macOS build jobs and a manual default-branch TestFlight workflow. Added release-configuration tests (five passing checks), workflow YAML parsing, disposable bundle-ID/build-number configuration, a Fastlane signing/upload lane, encrypted identity recovery/reuse, and an iPhone-only setup guide. Fixed both Info.plist build numbers to follow CURRENT_PROJECT_VERSION so subsequent TestFlight uploads can use new build numbers.

No GitHub repository has been connected. Ruby is not installed here, so Fastlane syntax/execution and Apple signing APIs remain unverified; the workflow runs `ruby -c` before the credentialed lane. No cloud build, certificate generation, profile creation, or TestFlight upload has been performed.
