# Build and install from an iPhone with GitHub

You do not need to own a Mac. The included GitHub Actions jobs use a hosted macOS runner with Xcode. Standard runners for public repositories are generally free under GitHub's public-repository allowance; check your account's current Actions terms and billing settings. New accounts may require verification. Codespaces has a separate limited personal allowance—check it and keep paid spending disabled if you want a free setup.

This repository includes workflows and a successful unsigned cloud build, but no TestFlight upload. GitHub, Apple Developer and App Store Connect setup must be completed in your own accounts. Never paste passwords, API keys or signing files into ChatGPT or public source files.

## 1. Source and cloud build are ready

The source files and workflows are already published at <https://github.com/pythoncrafter/calendar-seasons>. No ZIP unpacking or Codespaces terminal step is needed for this repository.

The [verified cloud run](https://github.com/pythoncrafter/calendar-seasons/actions/runs/38563870039) passed the shared tests, created the Chrome extension artifact, and compiled the iOS app and embedded Safari extension using Xcode 26.3. The simulator artifact is not installable on an iPhone. Continue below to configure Apple signing and upload a real TestFlight build.

## 2. Register the app with Apple

Use Safari to open the Apple Developer website and App Store Connect. Desktop website mode may make these pages easier to use.

1. In **Certificates, Identifiers & Profiles → Identifiers**, register two explicit App IDs:
   - Your unique app ID, such as `com.yourcompany.CalendarSeasons`.
   - The same ID followed by `.Extension`, such as `com.yourcompany.CalendarSeasons.Extension`.
2. Find your 10-character **Team ID** in Apple Developer membership details.
3. In App Store Connect, create a new iOS app record using the containing app's bundle ID. The extension does not get a separate app record. Use your own unique SKU and publisher information.
4. In **Users and Access → Integrations → App Store Connect API**, request API access if necessary and create a **team API key** with the **Admin** role. This workflow creates signing certificates/profiles, so an app-only upload key is insufficient. For an individual membership, use the account holder's available team API access. Record the Key ID and Issuer ID; download the `.p8` key once and keep it in Files securely. Apple permits that download only once.

## 3. Configure GitHub

In the repository's **Settings → Environments**, create an environment named `testflight`. Restrict it to your default branch. In that environment add these **Variables**:

| Name | Value |
|---|---|
| `APPLE_TEAM_ID` | Your Apple 10-character Team ID |
| `APP_BUNDLE_ID` | Your registered containing app bundle ID |
| `ASC_KEY_ID` | The Apple API key's 10-character Key ID |
| `ASC_ISSUER_ID` | Its Issuer UUID |

Add these **Secrets** in the same environment:

| Name | Value |
|---|---|
| `ASC_PRIVATE_KEY` | Entire `.p8` file contents, including BEGIN/END lines |
| `SIGNING_P12_PASSWORD` | A unique random password, at least 20 characters; save it in your password manager |

Do not add `SIGNING_P12_BASE64` for the first run unless you already have a reusable distribution identity. GitHub Secrets keeps these values out of the source repository. Protect your GitHub account and limit who can edit workflows or trigger the release environment.

## 4. Upload the first TestFlight build

1. Open **Actions → Upload to TestFlight → Run workflow**. Choose the default branch and enter a positive build number, starting with `1` if that version has never been uploaded. Every new upload needs a higher number.
2. The job validates configuration, prepares a temporary keychain, creates an Apple Distribution certificate and App Store provisioning profiles if needed, builds/signs both targets, then uploads the IPA. It does not submit to the App Store or distribute to external testers.
3. Apple limits distribution certificates. If the account is already at its limit, the job fails; it does not revoke existing certificates. Review the developer portal instead of repeatedly retrying or revoking certificates used by other apps.
4. After upload, wait for Apple processing. In App Store Connect → your app → **TestFlight**, resolve any missing compliance information truthfully and add yourself as an internal tester. If you cannot use internal testing, external TestFlight testing requires Apple's beta review.
5. Accept the invitation in the **TestFlight** iPhone app and install Calendar Seasons. Enable it in **Settings → Apps → Safari → Extensions**, allow Google Calendar, then select a theme in Safari's Page Menu.

A cloud build cannot validate the current authenticated Calendar website or taps on your iPhone. Follow the manual matrix after installation. If the unsigned build or signed build fails, use the job's compiler error to fix the source before retrying. Unsigned Apple compilation passed on the hosted Mac; the signed archive/upload remains to be validated.

## 5. Keep the signing identity for later uploads

An ephemeral GitHub runner loses its private key after the job. The workflow exports an **encrypted** reusable distribution identity into the `encrypted-signing-identity` artifact, protected by your `SIGNING_P12_PASSWORD`. It retains the artifact for only one day. The artifact can exist even when compilation/upload fails after signing preparation.

1. Download that artifact promptly from the run page and unzip it in Files.
2. Open `SigningCertificate.base64.txt`, copy its entire contents, and add a new GitHub environment **Secret** named `SIGNING_P12_BASE64`.
3. Keep the same `SIGNING_P12_PASSWORD`. Later runs import this identity and reuse it, rather than creating another distribution certificate each time.
4. Delete the recovery artifact after storing the secret and keep any backup encrypted. The artifact includes no password, `.p8` API key or unencrypted private key. Because the repository is public, treat downloadable encrypted signing artifacts as accessible to others and use a strong unique password.

If you change that password, first re-encrypt the signing identity; changing only the GitHub secret makes import fail. Do not repeatedly run without the reusable identity, because that can consume Apple's certificate slots.

## Current status

Source files are published and [Build and validate](https://github.com/pythoncrafter/calendar-seasons/actions/runs/38563870039) passed on GitHub. The iOS app and Safari extension compiled with Xcode 26.3, and the embedded-extension resource check passed. Chrome’s ZIP artifact is also available in that run.

Fastlane signing/API execution, certificate issuance, and TestFlight upload have not run because Apple account configuration is still required. Physical iPhone Safari activation and authenticated Calendar behavior remain untested. The repository connection permits code publication; GitHub environment/secret administration is performed by you in GitHub Settings.
