# Build and install from an iPhone with GitHub

You do not need to own a Mac. The included GitHub Actions jobs use a hosted macOS runner with Xcode. Standard runners for public repositories are generally free under GitHub's public-repository allowance; check your account's current Actions terms and billing settings. New accounts may require verification. Codespaces has a separate limited personal allowance—check it and keep paid spending disabled if you want a free setup.

This repository now includes the workflows, not a successful cloud build or a TestFlight upload. GitHub, Apple Developer and App Store Connect setup must be completed in your own accounts. Never paste passwords, API keys or signing files into ChatGPT or public source files.

## 1. Put the complete project on GitHub

1. In iPhone Safari, sign in to GitHub and create a **new public repository** named `calendar-seasons`. Initialize it with a README. If you already have a repository containing work, do not use the import steps below without reviewing what will be replaced.
2. Download the latest **Calendar-Seasons-complete.zip** from this conversation to Files. In the new repository, use **Add file → Upload files** to upload that ZIP. Use Safari's Request Desktop Website if the controls are hidden. Commit the upload.
3. Open **Code → Codespaces → Create codespace on main** (or your default branch) in the browser. On iPhone you may need desktop website mode. Check your personal free Codespaces allowance before creating it. Do not enable paid overages for this setup.
4. In the Codespace terminal, run these commands in the new repository:

   ```sh
   unzip Calendar-Seasons-complete.zip -d /tmp/calendar-seasons-import
   cp -R /tmp/calendar-seasons-import/calendar-seasons/. .
   git rm Calendar-Seasons-complete.zip
   git add shared chrome safari ios-app tests docs scripts .github fastlane Gemfile package.json README.md LICENSE .gitignore
   git commit -m "Add Calendar Seasons and cloud build workflows"
   git push
   ```

   The `cp` includes the hidden `.github` workflow directory. It replaces the placeholder README in this newly created repository. The source ZIP is removed from version control after import.
5. Stop/delete the Codespace when finished so it does not consume your remaining allowance. Open the repository's **Actions** tab. **Build and validate** runs the shared tests and an unsigned iOS simulator build. Wait for both jobs to pass. An unsigned simulator artifact cannot be installed on your iPhone.

If you cannot use Codespaces on your phone, someone with a computer can upload the extracted project for you, including `.github`. A GitHub ZIP upload by itself does not unpack source files or activate the workflows.

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

A cloud build cannot validate the current authenticated Calendar website or taps on your iPhone. Follow the manual matrix after installation. If the unsigned build or signed build fails, use the job's compiler error to fix the source before retrying. The first Apple compilation has not been run from this workspace.

## 5. Keep the signing identity for later uploads

An ephemeral GitHub runner loses its private key after the job. The workflow exports an **encrypted** reusable distribution identity into the `encrypted-signing-identity` artifact, protected by your `SIGNING_P12_PASSWORD`. It retains the artifact for only one day. The artifact can exist even when compilation/upload fails after signing preparation.

1. Download that artifact promptly from the run page and unzip it in Files.
2. Open `SigningCertificate.base64.txt`, copy its entire contents, and add a new GitHub environment **Secret** named `SIGNING_P12_BASE64`.
3. Keep the same `SIGNING_P12_PASSWORD`. Later runs import this identity and reuse it, rather than creating another distribution certificate each time.
4. Delete the recovery artifact after storing the secret and keep any backup encrypted. The artifact includes no password, `.p8` API key or unencrypted private key. Because the repository is public, treat downloadable encrypted signing artifacts as accessible to others and use a strong unique password.

If you change that password, first re-encrypt the signing identity; changing only the GitHub secret makes import fail. Do not repeatedly run without the reusable identity, because that can consume Apple's certificate slots.

## Current status

Workflow YAML and release configuration tests pass in the provided Linux environment. Ruby/Fastlane execution, Apple compilation, certificate issuance, and the upload have not been run here. The cloud build becomes reviewable once these files are pushed to your GitHub account and the workflow runs. No GitHub repository or Apple resource was created on your behalf in this conversation.
