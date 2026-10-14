# Calendar Seasons

A private, seasonal customization layer for the **Google Calendar website**. Four coordinated palettes, custom SVG botanical illustrations, a bubbly settings panel, gentle floating effects, and a native iPhone onboarding app. No account, backend, analytics, remote code, or access to event data.

## Install on desktop Chrome

1. Download and extract `Calendar-Seasons-complete.zip` (or the smaller Chrome ZIP).
2. Open `chrome://extensions` and enable **Developer mode**.
3. Choose **Load unpacked** and select the repository's `chrome` directory. For the smaller Chrome ZIP, select its extracted root containing `manifest.json`.
4. Open <https://calendar.google.com/calendar/> and pin **Calendar Seasons** from Chrome's Extensions menu.
5. Open its popup. Pick a season to override automatic switching, or turn on **Follow the seasons**. Settings apply immediately.
6. Choose **Default Google appearance** to remove styling while keeping your saved preferences. Disable/remove the extension in Chrome to uninstall.

## iPhone-only setup with GitHub

Have an Apple Developer membership but no Mac? Use the included public-repository GitHub Actions workflows to build on a hosted Mac and upload to TestFlight. Follow the [iPhone setup guide](docs/github-iphone.md). The unsigned build requires no Apple secrets; signed uploads require your own Apple account configuration. The hosted Mac build is passing, and version 1.0 build 1 was successfully uploaded to App Store Connect for TestFlight. Apple processing and internal tester setup remain separate steps.

## Install on iPhone using Xcode

Requires a Mac, Xcode 16 or newer, and an iPhone running iOS 16 or newer. The project has compiled successfully on GitHub’s hosted Mac with Xcode 26.3. Signed physical-device installation still requires your Apple configuration.

1. Extract the complete ZIP. Open `safari/CalendarSeasons.xcodeproj` in Xcode.
2. Select the project, then **each of the two targets**. Under **Signing & Capabilities**, choose your Apple development team and replace `com.example.CalendarSeasons` with a unique identifier. Keep the extension identifier prefixed by the app identifier (for example `com.yourcompany.CalendarSeasons.Extension`). Automatic signing is enabled; no credentials or profiles are included.
3. Select the shared **CalendarSeasons** scheme and your connected iPhone. Enable Developer Mode on the phone if Xcode requests it. Build and run the containing app.
4. On current iOS, go to **Settings → Apps → Safari → Extensions → Calendar Seasons**, then enable **Allow Extension**. On older iOS, use **Settings → Safari → Extensions**.
5. In **Safari**, visit <https://calendar.google.com/calendar/> and sign in normally. Use Safari's Page Menu (aA on older versions) → **Manage Extensions** to enable Calendar Seasons if needed. Grant website access to Google Calendar when Safari asks. UI wording can vary by iOS version.
6. Use the Page Menu → **Calendar Seasons** to choose your theme and settings.

The app's Open Calendar button uses your default browser. If Safari is not the default, open the URL in Safari yourself. The extension **does not style the native Google Calendar iOS app**. Mobile Google Calendar can expose different or limited website layouts; see [compatibility](docs/compatibility.md). iPhone support requires the Mac and physical-device checks below before release.

## Develop and validate

Shared source is authoritative. Do not edit generated copies in `chrome` or `safari/Resources`.

```sh
npm run build
npm test
# Requires Playwright and a Chromium binary; no product dependencies.
npm install --no-save --package-lock=false playwright
npm run test:browser
# Script/UI fixtures when extension loading is administratively blocked:
npm run test:fixture
npm run package
# On a Mac with full Xcode, compile and check the embedded extension:
bash scripts/validate-macos.sh
```

`npm run package` creates complete and Chrome-store ZIPs next to the repository. Node 20+ and Python 3.10+ are sufficient for build/static tests. Browser tests default to `/usr/bin/chromium`; change the test launch configuration on another OS. Test fixtures use synthetic data and do not log in to Google.

- `shared/`: shared engine, preferences, popup, scoped integration, SVG/PNG assets
- `chrome/`: ready-to-load Manifest V3 extension
- `safari/`: iOS Safari Web Extension target, generated browser resources, Xcode project
- `ios-app/`: SwiftUI containing app, icons, privacy manifest
- `tests/`: unit, resource/configuration and browser fixture checks
- `docs/`: privacy, compatibility, publishing, test matrix

## Release status

Chrome resources are ready for local unpacked installation. The Safari containing app and extension compile successfully in GitHub’s macOS workflow; signed device installation and live Safari validation remain pending. Apple signing and the first TestFlight upload succeeded in the hosted workflow. No store approval, authenticated Google Calendar test, or physical-device test is claimed. See [publishing](docs/publishing.md) and [test matrix](docs/testing.md) for the remaining release gates.
