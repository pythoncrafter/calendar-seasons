globalThis.SeasonStore=(()=>{
 const api=globalThis.browser||globalThis.chrome;
 async function read(){return Seasons.normalize((await api.storage.local.get('settings')).settings);}
 async function write(settings){await api.storage.local.set({settings:Seasons.normalize(settings)});}
 return {read,write,watch(fn){api.storage.onChanged.addListener((changes,area)=>{if(area==='local'&&changes.settings)fn(Seasons.normalize(changes.settings.newValue));});}};
})();
