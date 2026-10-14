from pathlib import Path
import zipfile,subprocess
root=Path(__file__).resolve().parents[1]
subprocess.run(['python3',str(root/'scripts/build.py')],check=True)
for name,base,prefix in [('Calendar-Seasons-complete.zip',root,'calendar-seasons/'),('Calendar-Seasons-Chrome.zip',root/'chrome','')]:
 with zipfile.ZipFile(root.parent/name,'w',zipfile.ZIP_DEFLATED) as z:
  for p in sorted(base.rglob('*')):
   if p.is_file() and not any(x in p.parts for x in ['node_modules','.git','test-results','__pycache__']):z.write(p,prefix+str(p.relative_to(base)))
 print(root.parent/name)
