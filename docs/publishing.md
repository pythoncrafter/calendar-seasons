# Publishing

## Cloud builds without owning a Mac

The [iPhone/GitHub guide](github-iphone.md) covers the included unsigned build and manual TestFlight workflow, Apple API-key setup, and encrypted signing-identity reuse. The unsigned workflow passed with Xcode 26.3. The repository's [validation record](validation-results.md#testflight-upload-succeeded) records a successful signed upload of version 1.0 build 1. Apple processing, tester assignment, and physical-device validation are separate steps.

## TestFlight and App Store

1. Run the build/static tests and complete the physical-iPhone matrix. On Mac, run `xcodebuild -list -project safari/CalendarSeasons.xcodeproj`, then build the shared scheme for a simulator/device to validate the generated project with Apple's compiler. Example unsigned simulator check:

   ```sh
   xcodebuild -project safari/CalendarSeasons.xcodeproj -scheme CalendarSeasons -configuration Debug -sdk iphonesimulator CODE_SIGNING_ALLOWED=NO build
   ```

   Alternatively, run `bash scripts/validate-macos.sh` on the Mac to build both targets without signing and verify the compiled app contains the Safari extension and its root manifest/resources. This does not test physical-device activation or upload anything.

2. Join the Apple Developer Program. Choose your development team for both targets; set unique app and extension bundle identifiers, version and build number. Create the matching App Store Connect app. Check app icon generation and minimum OS deployment on your selected Xcode version.
3. Confirm the embedded `.appex` contains **manifest.json at its bundle root** and the `assets` directory, and uses `com.apple.Safari.web-extension` as the extension point. The Xcode resource phases copy each browser file to the bundle root. No App Groups or Safari app-extension entitlements are needed for this Web Extension MVP.
4. Select a generic iOS device destination and **Product → Archive** with the Release configuration. Validate in Organizer, then **Distribute App → App Store Connect → Upload** using your real signing credentials.
5. After processing, complete encryption/export-compliance questions accurately (the product adds no custom cryptography), privacy disclosures, beta contact and review notes. Add internal testers, then submit for external TestFlight review if needed.
6. Complete App Store metadata: screenshots from actual iPhones, support URL, public privacy URL, description, age rating and pricing. Explain in review notes how to enable the Safari extension and that it styles the web Calendar only. Do not advertise native Google Calendar app support.
7. Submit only after validation. Apple review and approval are not guaranteed. Avoid presenting Google's branding as your own or implying affiliation.

## Chrome Web Store

1. Run `npm run build`, all tests, and the live Chrome matrix. Run `npm run package`.
2. Register a Chrome Web Store developer account and upload `Calendar-Seasons-Chrome.zip`. Its manifest is at the ZIP root; do not upload the complete repository ZIP.
3. Supply actual screenshots (recommended store sizes per current dashboard), 128px icon, descriptions, support contact and a public privacy-policy URL. This repository includes a 128px icon; create and validate any additional promotional assets the store currently requires.
4. Describe the single purpose: local visual personalization of Google Calendar. Justify `storage` for preferences and calendar.google.com host access for scoped appearance customization. Declare no collection or sale of user data and no remote code.
5. Test the packaged ZIP locally, submit for review, and handle reviewer questions truthfully. No store upload or approval was performed here.

## Maintain

Increment both extension manifest and iOS versions for releases. Make theme changes in `shared`, then rebuild both platforms. Keep a dedicated test Google account for DOM regression checks. Never expand permissions silently to compensate for redirects.
