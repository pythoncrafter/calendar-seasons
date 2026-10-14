#!/usr/bin/env bash
set -euo pipefail
seasons_xcode_path="$(python3 - <<'PY'
from pathlib import Path
import re, subprocess
candidates=[]
for app in Path('/Applications').glob('Xcode*.app'):
    if 'beta' in app.name.lower():
        continue
    binary=app/'Contents/Developer/usr/bin/xcodebuild'
    if not binary.exists():
        continue
    result=subprocess.run([str(binary),'-version'],capture_output=True,text=True)
    match=re.search(r'^Xcode ([0-9.]+)',result.stdout,re.M)
    if result.returncode==0 and match:
        candidates.append((tuple(map(int,match.group(1).split('.'))),str(app/'Contents/Developer')))
if not candidates:
    raise SystemExit('No stable Xcode installation found.')
print(max(candidates)[1])
PY
)"
sudo xcode-select --switch "$seasons_xcode_path"
xcodebuild -version
