from pathlib import Path
import json,plistlib,subprocess,xml.etree.ElementTree as ET,re
r=Path(__file__).resolve().parents[1]
count=0
for p in r.rglob('*'):
 if not p.is_file():continue
 if p.suffix=='.json':json.loads(p.read_text());count+=1
 if p.suffix in ['.plist','.xcprivacy']:plistlib.loads(p.read_bytes());count+=1
 if p.suffix in ['.svg','.xcscheme']:ET.parse(p);count+=1
 if p.suffix in ['.js','.cjs']:subprocess.run(['node','--check',str(p)],check=True,capture_output=True);count+=1
for folder in ['chrome','safari/Resources']:
 base=r/folder;m=json.loads((base/'manifest.json').read_text());assert m['manifest_version']==3;assert m['permissions']==['storage'];assert m['host_permissions']==['https://calendar.google.com/*']
 for path in [m['action']['default_popup'],*m['icons'].values(),*m['content_scripts'][0]['js'],*m['content_scripts'][0]['css']]:assert (base/path).is_file(),path
 for p in (r/'shared').rglob('*'):
  if p.is_file():assert p.read_bytes()==(base/p.relative_to(r/'shared')).read_bytes(),f'Stale built resource {p}'
p=(r/'safari/CalendarSeasons.xcodeproj/project.pbxproj').read_text();ids=re.findall(r'^([0-9A-F]{24}) =',p,re.M);assert len(ids)==len(set(ids));assert set(re.findall(r'\b[0-9A-F]{24}\b',p))==set(ids)
# Xcode's OpenStep parser/compiler still must run on macOS.
assert p.count('PBXNativeTarget;')==2;assert 'Embed App Extensions' in p
print(f'Validated {count} JSON, JS, plist, privacy, SVG and scheme files; resource parity and Xcode object references pass.')
from openstep import loads
project=loads(p);objects=project['objects'];root=objects[project['rootObject']]
assert root['isa']=='PBXProject'
for targetid in root['targets']:
 target=objects[targetid];assert target['isa']=='PBXNativeTarget'
 for phaseid in target['buildPhases']:
  for fileid in objects[phaseid]['files']:
   reference=objects[objects[fileid]['fileRef']]
   if reference['sourceTree']=='SOURCE_ROOT':assert (r/'safari'/reference['path']).exists(),reference['path']
 if target['productType']=='com.apple.product-type.app-extension':
  resources=[objects[objects[x]['fileRef']]['path'] for phaseid in target['buildPhases'] if objects[phaseid]['isa']=='PBXResourcesBuildPhase' for x in objects[phaseid]['files']]
  assert 'Resources/manifest.json' in resources and 'Resources/assets' in resources
print('Xcode OpenStep project parses; target phases and resource paths validated.')
