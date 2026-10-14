#!/usr/bin/env bash
# Compile both iOS targets without publisher credentials; verify the embedded extension.
set -euo pipefail
if [[ "$(uname -s)" != "Darwin" ]] || ! command -v xcodebuild >/dev/null 2>&1; then
  echo "This check requires a Mac with full Xcode installed and selected with xcode-select." >&2
  exit 1
fi
seasons_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
seasons_derived="${SEASONS_DERIVED_DATA:-$seasons_root/test-results/DerivedData}"
python3 "$seasons_root/scripts/build.py"
xcodebuild -project "$seasons_root/safari/CalendarSeasons.xcodeproj" \
  -scheme CalendarSeasons -configuration Debug \
  -destination 'generic/platform=iOS Simulator' \
  -derivedDataPath "$seasons_derived" CODE_SIGNING_ALLOWED=NO build
python3 - "$seasons_derived/Build/Products/Debug-iphonesimulator" <<'PY'
from pathlib import Path
import json, plistlib, sys
products = Path(sys.argv[1])
app = products / 'Calendar Seasons.app'
ext = app / 'PlugIns' / 'Calendar Seasons Extension.appex'
assert app.is_dir(), 'Missing compiled containing app'
assert ext.is_dir(), 'Missing embedded Safari extension'
manifest = json.loads((ext / 'manifest.json').read_text())
assert manifest['manifest_version'] == 3
assert manifest['host_permissions'] == ['https://calendar.google.com/*']
for relative in [manifest['action']['default_popup'], *manifest['icons'].values(),
                 *manifest['content_scripts'][0]['js'], *manifest['content_scripts'][0]['css']]:
    assert (ext / relative).is_file(), f'Missing extension bundle resource: {relative}'
info = plistlib.loads((ext / 'Info.plist').read_bytes())
assert info['NSExtension']['NSExtensionPointIdentifier'] == 'com.apple.Safari.web-extension'
assert (app / 'PrivacyInfo.xcprivacy').is_file()
assert (ext / 'PrivacyInfo.xcprivacy').is_file()
print('PASS: Apple simulator compilation and embedded-extension bundle validation.')
print('Physical iPhone activation, live Calendar testing, signing, and store upload remain separate checks.')
PY
