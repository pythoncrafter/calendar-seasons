(function(root){
'use strict';
const themes={
 winter:{name:'Winter Vibes',mood:'Snowy mornings & warm blankets',background:'#eaf3f9',surface:'#f7fbfe',accent:'#397d9c',ink:'#24465b',particle:'snow',symbol:'❄',dark:{background:'#172b39',surface:'#223e50',accent:'#93cbe2',ink:'#eaf5fb'}},
 fall:{name:'Cozy Fall',mood:'Cinnamon coffee & sweater weather',background:'#f5e9d9',surface:'#fff8ee',accent:'#a55327',ink:'#563c30',particle:'leaf',symbol:'🍂',dark:{background:'#30261f',surface:'#44342a',accent:'#efb486',ink:'#fff0df'}},
 spring:{name:'Spring Bloom',mood:'Fresh starts & flowers blooming',background:'#f8edf2',surface:'#fff9fc',accent:'#94617d',ink:'#554052',particle:'petal',symbol:'✿',dark:{background:'#302632',surface:'#443649',accent:'#e1aecb',ink:'#f9edf6'}},
 summer:{name:'Summer Glow',mood:'Sunshine & little adventures',background:'#fff3d3',surface:'#fffcf0',accent:'#167c80',ink:'#3c514a',particle:'sun',symbol:'☀',dark:{background:'#24352f',surface:'#344a42',accent:'#9bddd2',ink:'#fff6d8'}}
};
const schedule=['winter','winter','spring','spring','spring','summer','summer','summer','fall','fall','fall','winter'];
const defaults={enabled:true,theme:'fall',automatic:true,schedule,level:'cozy',animation:true,icons:true,reducedMotion:false,holiday:false,colors:{background:null,accent:null,surface:null}};
function normalize(raw={}){raw=raw&&typeof raw==='object'?raw:{};const s={...defaults,...raw};for(const k of ['enabled','automatic','animation','icons','reducedMotion','holiday'])s[k]=typeof raw[k]==='boolean'?raw[k]:defaults[k];s.theme=themes[s.theme]?s.theme:'fall';s.level=['minimal','cozy','magical'].includes(s.level)?s.level:'cozy';s.schedule=Array.isArray(s.schedule)&&s.schedule.length===12&&s.schedule.every(x=>themes[x])?[...s.schedule]:[...schedule];s.colors={};for(const k of ['background','accent','surface'])s.colors[k]=/^#[0-9a-f]{6}$/i.test(raw.colors?.[k])?raw.colors[k]:null;return s;}
function resolve(s,date=new Date()){return s.automatic?s.schedule[date.getMonth()]:s.theme;}
function palette(s,dark=false,date=new Date()){const t=themes[resolve(s,date)],p=dark?t.dark:t;return {...p,...Object.fromEntries(Object.entries(s.colors).filter(([,v])=>v)),name:t.name,particle:t.particle};}
function luminance(hex){const a=hex.slice(1).match(/../g).map(x=>parseInt(x,16)/255).map(x=>x<=.04045?x/12.92:((x+.055)/1.055)**2.4);return a[0]*.2126+a[1]*.7152+a[2]*.0722;}
function ratio(a,b){const x=luminance(a),y=luminance(b);return (Math.max(x,y)+.05)/(Math.min(x,y)+.05);}
function contrast(hex){return luminance(hex)>.179?'#17252c':'#ffffff';}
const api={themes,defaults,normalize,resolve,palette,contrast,ratio};root.Seasons=api;if(typeof module!=='undefined')module.exports=api;
})(globalThis);
