from pathlib import Path
import shutil,json
root=Path(__file__).resolve().parents[1]
manifest={'manifest_version':3,'name':'Calendar Seasons','version':'1.0.0','description':'A little seasonal joy for Google Calendar. Private, lightweight, and locally personalized.','permissions':['storage'],'host_permissions':['https://calendar.google.com/*'],'action':{'default_popup':'popup.html','default_title':'Calendar Seasons','default_icon':{'16':'assets/icon-16.png','32':'assets/icon-32.png'}},'icons':{str(n):f'assets/icon-{n}.png' for n in [16,32,48,128]},'content_scripts':[{'matches':['https://calendar.google.com/*'],'js':['engine.js','storage.js','content.js'],'css':['calendar.css'],'run_at':'document_idle'}],'web_accessible_resources':[{'resources':['assets/*.svg'],'matches':['https://calendar.google.com/*']}],'content_security_policy':{'extension_pages':"script-src 'self'; object-src 'self'"}}
for target in [root/'chrome',root/'safari/Resources']:
 target.mkdir(parents=True,exist_ok=True)
 for src in (root/'shared').iterdir():
  dest=target/src.name
  if src.is_dir():shutil.copytree(src,dest,dirs_exist_ok=True)
  else:shutil.copy2(src,dest)
 (target/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Built Chrome and Safari resources from shared source.')
