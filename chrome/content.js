(()=>{
'use strict';
if(globalThis.__calendarSeasons)return;globalThis.__calendarSeasons=true;
let settings,host,shadow,timer,scanTimer,lastDay='',observer,currentPalette;
const dark=matchMedia('(prefers-color-scheme: dark)'),motion=matchMedia('(prefers-reduced-motion: reduce)');
// Only semantic calendar containers. Never inspect text, event attributes, or data.
function scan(){
 document.querySelectorAll('[data-cs-surface]').forEach(el=>el.removeAttribute('data-cs-surface'));
 if(!settings?.enabled)return;
 document.querySelectorAll('main,[role="main"],[role="grid"]').forEach(el=>{
 if(el.closest('[role="dialog"],[role="alertdialog"]'))return;
 if(el.matches('[role="grid"]')&&!el.querySelector('[role="gridcell"],[role="columnheader"]'))return;
 const rgb=getComputedStyle(el).color.match(/^rgba?\((\d+)[, ]+\s*(\d+)[, ]+\s*(\d+)/);
 if(rgb){const text='#'+rgb.slice(1,4).map(v=>Number(v).toString(16).padStart(2,'0')).join('');if(Seasons.ratio(text,currentPalette.surface)<4.5)return;}
 el.setAttribute('data-cs-surface','');
 });
}
function render(){
 if(!settings)return;
 document.documentElement.removeAttribute('data-cs-active');
 document.body.removeAttribute('data-cs-backdrop');
 if(host)host.remove();host=null;
 if(!settings.enabled){for(const key of ['background','surface','accent','ink'])document.documentElement.style.removeProperty('--cs-'+key);scan();return;}
 const name=Seasons.resolve(settings),p=Seasons.palette(settings,dark.matches);currentPalette=p;
 const nativeColor=getComputedStyle(document.body).color.match(/^rgba?\((\d+)[, ]+\s*(\d+)[, ]+\s*(\d+)/);
 if(nativeColor){const ink='#'+nativeColor.slice(1,4).map(v=>Number(v).toString(16).padStart(2,'0')).join('');if(Seasons.ratio(ink,p.background)>=4.5)document.body.setAttribute('data-cs-backdrop','');}
 document.documentElement.setAttribute('data-cs-active',name);
 for(const k of ['background','surface','accent'])document.documentElement.style.setProperty('--cs-'+k,p[k]);
 document.documentElement.style.setProperty('--cs-ink',Seasons.contrast(p.surface));
 host=document.createElement('div');host.id='calendar-seasons-decor';host.setAttribute('aria-hidden','true');host.style.cssText='position:fixed;inset:0;pointer-events:none;z-index:1;contain:strict;';
 shadow=host.attachShadow({mode:'closed'});
 const style=document.createElement('style');style.textContent=`:host{pointer-events:none}*{box-sizing:border-box;pointer-events:none}.corner{position:absolute;bottom:0;right:0;width:clamp(100px,18vw,230px);opacity:.45}.badge{position:absolute;top:12px;right:16px;width:30px;height:30px;opacity:.5}.particle{position:absolute;top:-35px;left:var(--x);width:var(--size);height:var(--size);opacity:.45;animation:drift var(--duration) linear infinite;animation-delay:var(--delay);will-change:transform}.paused .particle{animation-play-state:paused}@keyframes drift{from{transform:translate3d(0,-20px,0) rotate(0)}to{transform:translate3d(35px,105vh,0) rotate(180deg)}}@media(prefers-reduced-motion:reduce){.particle{display:none}}`;
 shadow.append(style);const layer=document.createElement('div');shadow.append(layer);
 const url=path=>(globalThis.browser||chrome).runtime.getURL('assets/'+path+'.svg');
 function art(cls,file){const img=document.createElement('img');img.className=cls;img.src=url(file);img.alt='';layer.append(img);return img;}
 if(settings.level!=='minimal')art('corner',name+(name==='winter'&&settings.holiday?'-holiday':''));
 if(settings.icons)art('badge',name+'-icon');
 if(settings.level==='magical'&&settings.animation&&!settings.reducedMotion&&!motion.matches){for(let i=0;i<12;i++){const img=art('particle',p.particle);img.style.cssText=`--x:${(i*37)%100}%;--size:${12+i%4*3}px;--duration:${18+i%5*4}s;--delay:-${i*3}s`;}}
 document.body.append(host);layer.classList.toggle('paused',document.hidden);scan();
}
SeasonStore.read().then(s=>{settings=s;render();}).catch(()=>{});
SeasonStore.watch(s=>{settings=s;render();});
for(const q of [dark,motion])q.addEventListener('change',render);
document.addEventListener('visibilitychange',()=>{if(!document.hidden)render();else shadow?.querySelector('div')?.classList.add('paused');});
observer=new MutationObserver(records=>{if(records.some(r=>[...r.addedNodes].some(n=>n.nodeType===1&&n!==host))){clearTimeout(scanTimer);scanTimer=setTimeout(scan,180);}});
observer.observe(document.body,{childList:true,subtree:true});
timer=setInterval(()=>{const day=new Date().toDateString();if(day!==lastDay){lastDay=day;render();}},60000);
addEventListener('pagehide',()=>{clearInterval(timer);clearTimeout(scanTimer);observer.disconnect();});
addEventListener('pageshow',e=>{if(e.persisted){observer.observe(document.body,{childList:true,subtree:true});timer=setInterval(render,60000);render();}});
})();
